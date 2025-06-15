class ContextStateError(RuntimeError):
    """
    Base exception for errors related to transaction/session context state.

    Raised when an operation violates the expected context assumptions.
    """


class NoSessionError(ContextStateError):
    """
    Raised when no active SQLAlchemy AsyncSession is found in the current context.

    This typically occurs when `get_session(strict=True)` is called
    outside of a `session()` or `transaction()` context.
    """


class SessionAlreadyActiveError(ContextStateError):
    """
    Raised when attempting to enter a new session context
    while another session is already active.

    This prevents implicit context shadowing, unless explicitly allowed
    with `reuse_if_exists=True`.
    """


class TransactionAlreadyActiveError(ContextStateError):
    """
    Raised when attempting to start a new transaction while a transaction
    is already active, and nested transactions are disallowed.

    This can occur when `allow_nested_transactions=False` is passed
    to `transaction()`.
    """
