from collections.abc import AsyncIterator, Callable
from contextlib import AbstractAsyncContextManager, asynccontextmanager
from contextvars import ContextVar
from typing import Any, Optional

from sqlalchemy import CompoundSelect, Executable, Select, util
from sqlalchemy.engine import Result
from sqlalchemy.engine.interfaces import (
    _CoreAnyExecuteParams,  # type: ignore[reportPrivateUsage]
)
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker
from sqlalchemy.orm._typing import (
    OrmExecuteOptionsParameter,  # type: ignore[reportPrivateUsage]
)
from sqlalchemy.orm.session import _BindArguments  # type: ignore[reportPrivateUsage]
from typing_extensions import Literal, overload

from sqlalchemy_tx_context.exceptions import (
    NoSessionError,
    SessionAlreadyActiveError,
    TransactionAlreadyActiveError,
)


class SQLAlchemyTransactionContext:
    """
    Transaction and session manager for SQLAlchemy AsyncSession using context-local state.

    This class allows executing SQLAlchemy statements without manually passing around session objects.
    """

    _engine: AsyncEngine
    _default_session_maker: async_sessionmaker[AsyncSession]
    _auto_context_on_execute: bool
    _auto_context_force_transaction: bool
    _session_var: ContextVar[AsyncSession]

    def __init__(
        self,
        engine: AsyncEngine,
        *,
        default_session_maker: Optional[async_sessionmaker[AsyncSession]] = None,
        auto_context_on_execute: bool = False,
        auto_context_force_transaction: bool = False,
    ):
        """
        Initialize a transaction context manager.

        :param engine: SQLAlchemy AsyncEngine instance.
        :param default_session_maker: Optional custom async session factory.
        :param auto_context_on_execute:
            If True, allows `execute(...)` to work even when no session is currently active.
            In this case, a temporary session will be created automatically:

            - For `INSERT`, `UPDATE`, and `DELETE` statements, a transaction block will be used.
            - For all other SQL constructs, a non-transactional session context will be used.

            If False (default), calling `execute(...)` without an active session will raise a `NoSessionError`.
        :param auto_context_force_transaction:
            Defines what type of temporary context is created by `execute(...)` if no session is active and
            `auto_context_on_execute=True`.

            - If `True` (default), always creates a managed transaction block regardless of the statement type.
            - If `False`, uses `.session()` only for instances of `Select` and `CompoundSelect`,
                and `.transaction()` for all others including raw SQL (`text(...)`), DML, and custom executable objects.

            This option has no effect unless `auto_context_on_execute=True`.
        """

        self._engine = engine
        if default_session_maker is None:
            default_session_maker = async_sessionmaker(
                self._engine,
                class_=AsyncSession,
                expire_on_commit=False,
            )
        self._default_session_maker = default_session_maker
        self._auto_context_on_execute = auto_context_on_execute
        self._auto_context_force_transaction = auto_context_force_transaction
        self._session_var = ContextVar("sqlalchemy_tx_context_session")

    @asynccontextmanager
    async def session(
        self,
        *,
        session_maker: Optional[async_sessionmaker[AsyncSession]] = None,
        reuse_if_exists: bool = False,
    ) -> AsyncIterator[AsyncSession]:
        """
        Enter a new session context or reuse the current one.

        :param session_maker: Optional custom session maker to use.
        :param reuse_if_exists: If True, reuses existing context-local session if present.

        :return: AsyncSession instance.

        :raise SessionAlreadyActiveError: If session already exists and `reuse_if_exists` is False.
        """

        current_session = self._session_var.get(None)

        if current_session is not None:
            if reuse_if_exists:
                yield current_session
                return
            raise SessionAlreadyActiveError()

        async with self._resolve_session_maker(session_maker) as session:
            token = self._session_var.set(session)
            try:
                yield session
            finally:
                self._session_var.reset(token)

    @asynccontextmanager
    async def transaction(
        self,
        *,
        session_maker: Optional[async_sessionmaker[AsyncSession]] = None,
        reuse_if_exists: bool = True,
        allow_nested_transactions: bool = True,
    ) -> AsyncIterator[AsyncSession]:
        """
        Enter a transaction context. Creates a new session if needed.

        If a transaction is already active, creates a nested transaction unless explicitly forbidden.

        :param session_maker: Optional custom session maker.
        :param reuse_if_exists: Whether to reuse current session if available.
        :param allow_nested_transactions: Whether to allow nested transactions.

        :return: AsyncSession with active transaction.

        :raise SessionAlreadyActiveError: If session already exists and `reuse_if_exists` is False.
        :raise TransactionAlreadyActiveError: If transaction is already active and nesting is disabled.
        """

        async with self.session(
            session_maker=session_maker,
            reuse_if_exists=reuse_if_exists,
        ) as session:
            if session.in_transaction():
                if allow_nested_transactions is False:
                    raise TransactionAlreadyActiveError()
                async with session.begin_nested():
                    yield session
            else:
                async with session.begin():
                    yield session

    async def execute(
        self,
        statement: Executable,
        params: Optional[_CoreAnyExecuteParams] = None,
        *,
        force_transaction: Optional[bool] = None,
        execution_options: OrmExecuteOptionsParameter = util.EMPTY_DICT,
        bind_arguments: Optional[_BindArguments] = None,
        **kw: Any,
    ) -> Result[Any]:
        """
        Execute a SQLAlchemy statement using the current context-bound session.

        If auto_context_on_execute is True and no session is active, a new session or transaction
        will be created depending on the statement type.

        :param statement: SQLAlchemy Executable (e.g., select, insert, update).
        :param params: Optional bound parameters.
        :param force_transaction: Overrides the default behavior defined by `auto_context_force_transaction`
               for this specific call.
        :param execution_options: SQLAlchemy execution options.
        :param bind_arguments: Additional bind arguments.
        :param kw: Additional arguments passed to `session.execute`.

        :return: SQLAlchemy Result object.

        :raise NoSessionError: If no session is currently active.
        """

        session: Optional[AsyncSession] = self.get_session(
            strict=not self._auto_context_on_execute,
        )
        if session is None:
            if self._need_force_transaction_on_context_execute(force_transaction):
                session_factory = self.transaction
            else:
                session_factory = self._get_context_for_statement(statement)
            async with session_factory() as session:
                return await session.execute(
                    statement,
                    params,
                    execution_options=execution_options,
                    bind_arguments=bind_arguments,
                    **kw,
                )
        return await session.execute(
            statement,
            params,
            execution_options=execution_options,
            bind_arguments=bind_arguments,
            **kw,
        )

    @overload
    def get_session(self, strict: Literal[True] = True) -> AsyncSession: ...

    @overload
    def get_session(self, strict: Literal[False]) -> Optional[AsyncSession]: ...

    @overload
    def get_session(self, strict: bool) -> Optional[AsyncSession]: ...

    def get_session(self, strict: bool = True) -> Optional[AsyncSession]:
        """
        Return the current context-local session, or raise if none exists.

        :param strict: If True, raises NoSessionError if session is not set.

        :return: AsyncSession or None.

        :raise NoSessionError: If no session is active and `strict=True`.
        """

        session = self._session_var.get(None)
        if session is None and strict is True:
            raise NoSessionError()
        return session

    @asynccontextmanager
    async def new_session(
        self,
        *,
        session_maker: Optional[async_sessionmaker[AsyncSession]] = None,
    ) -> AsyncIterator[AsyncSession]:
        """
        Start a new independent session, even if another is already active.

        This overrides the current context-local session during the block.

        :param session_maker: Optional custom session factory.

        :return: New AsyncSession.
        """

        async with self._resolve_session_maker(session_maker) as session:
            token = self._session_var.set(session)
            try:
                yield session
            finally:
                self._session_var.reset(token)

    @asynccontextmanager
    async def new_transaction(
        self,
        *,
        session_maker: Optional[async_sessionmaker[AsyncSession]] = None,
    ) -> AsyncIterator[AsyncSession]:
        """
        Start a new transaction in a fresh, independent session.

        Overrides the current session in the context for the duration.

        :param session_maker: Optional custom session factory.

        :return: New AsyncSession with active transaction.
        """

        async with self.new_session(  # noqa: SIM117
            session_maker=session_maker,
        ) as session:
            async with session.begin():
                yield session

    @staticmethod
    def _is_readonly_statement(statement: Executable) -> bool:
        """
        Check whether the statement is read-only (e.g., SELECT).

        This method is used to determine when a transaction is optional
        during automatic context creation.

        :return: True if statement is considered read-only.
        """

        return isinstance(statement, (Select, CompoundSelect))

    def _need_force_transaction_on_context_execute(
        self,
        force_transaction: Optional[bool],
    ) -> bool:
        """
        Determine whether a transactional context is required based on the call-specific and global flags.

        :param force_transaction: Optional per-call override of auto-context behavior.

        :return: True if a transactional context should be created, False otherwise.
        """

        if force_transaction is not None:
            return force_transaction
        else:
            return self._auto_context_force_transaction

    def _get_context_for_statement(
        self,
        statement: Executable,
    ) -> Callable[..., AbstractAsyncContextManager[AsyncSession]]:
        """
        Returns a context factory (`self.session` or `self.transaction`) appropriate for the given statement.

        Used to select `.session` or `.transaction` based on statement type during automatic context creation.

        :return: `.session` if the statement is a read-only query (instances of `Select` or `CompoundSelect`).
                 `.transaction` for all other statement types (e.g., `Insert`, `Update`, `Delete`, `text(...)`).
        """

        if self._is_readonly_statement(statement):
            session_factory = self.session
        else:
            session_factory = self.transaction
        return session_factory

    def _resolve_session_maker(
        self,
        session_maker: Optional[async_sessionmaker[AsyncSession]],
    ) -> AsyncSession:
        """
        Selects the session maker to use.

        :param session_maker: Optional override.

        :return: Async context manager producing AsyncSession.
        """

        return (session_maker or self._default_session_maker)()
