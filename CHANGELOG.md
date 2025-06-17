# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.0.1] - 2025-06-15

### Added

- Added `@overload` annotations for the `execute(...)` method to improve type inference
for `select(...)`, `insert(...)`, and `update(...)` statements.

---

## [1.0.0] - 2025-06-15

### Changed

- Completely redesigned the library API to follow a cleaner, context-based execution model.
- Introduced the `SQLAlchemyTransactionContext` class as the core and only public interface.

### Removed

- Removed all previous experimental and `ProxyQuery`-style APIs.
- Dropped support for legacy GINO-style `.select()` / `.update()` helpers.
- Internal architecture and usage were fully rewritten. Old behavior is no longer supported.

### Notes

- This version introduces **breaking changes**. Previous integrations relying on global `db.select(...)` and
other dynamic helpers must migrate to the new `db.execute(...)` model.
- Use context managers like `.session()` and `.transaction()` to manage execution scopes explicitly
or enable `auto_context_on_execute` for implicit behavior.
- See the `example/` directory for a complete demo of insert/select/rollback flows.
