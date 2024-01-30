# Release Notes

## 1.0.0

### Migration

- Add support for Pydantic V2. PR [#22](https://github.com/nayan32biswas/mongodb-odm/pull/22) by [@nayan32biswas](https://github.com/nayan32biswas).
- Add support for Python 3.12. PR [#22](https://github.com/nayan32biswas/mongodb-odm/pull/22) by [@nayan32biswas](https://github.com/nayan32biswas).
- Update all utcnow to now for 3.12 support. PR [#26](https://github.com/nayan32biswas/mongodb-odm/pull/26) by [@nayan32biswas](https://github.com/nayan32biswas).

### Breaking Changes

- Rename the model inner config class from `Config` to `ODMConfig`. PR [#22](https://github.com/nayan32biswas/mongodb-odm/pull/22) by [@nayan32biswas](https://github.com/nayan32biswas).
- Now `_id` field was a `PrivateAttr`. It will behave as private attr as Pydantic define. PR [#22](https://github.com/nayan32biswas/mongodb-odm/pull/22) by [@nayan32biswas](https://github.com/nayan32biswas).

### Fixes

- Fix connection issue of the database. PR [#23](https://github.com/nayan32biswas/mongodb-odm/pull/23) by [@nayan32biswas](https://github.com/nayan32biswas).
- Resolve apply_indexes issue. PR [#24](https://github.com/nayan32biswas/mongodb-odm/pull/24) by [@nayan32biswas](https://github.com/nayan32biswas).

### Features

- Add ObjectId serializer `ObjectIdStr` for json response. PR [#25](https://github.com/nayan32biswas/mongodb-odm/pull/25) by [@nayan32biswas](https://github.com/nayan32biswas).

### Docs

- Update docs according to Pydantic V2 migration and other changes. PR [#27](https://github.com/nayan32biswas/mongodb-odm/pull/27) by [@nayan32biswas](https://github.com/nayan32biswas).

## 0.2.5

### Fixes

- Configure Ruff for linting and formatting. PR [#17](https://github.com/nayan32biswas/mongodb-odm/pull/17) by [@nayan32biswas](https://github.com/nayan32biswas).
- Fix for model inheritance related issue. PR [#19](https://github.com/nayan32biswas/mongodb-odm/pull/19) by [@nayan32biswas](https://github.com/nayan32biswas).
- Drop exclude_none feature. PR [#20](https://github.com/nayan32biswas/mongodb-odm/pull/20) by [@nayan32biswas](https://github.com/nayan32biswas).

### Refactors

- Add code comment. PR [#18](https://github.com/nayan32biswas/mongodb-odm/pull/18) by [@nayan32biswas](https://github.com/nayan32biswas).

## 0.2.4

### Features

- Validation on Filter dict. PR [#13](https://github.com/nayan32biswas/mongodb-odm/pull/13) by [@nayan32biswas](https://github.com/nayan32biswas).
- Docker compose configuration and pydantic version change . PR [#15](https://github.com/nayan32biswas/mongodb-odm/pull/15) by [@nayan32biswas](https://github.com/nayan32biswas).

### Fixes

- Resolve apply-indexes for Text base index. PR [#14](https://github.com/nayan32biswas/mongodb-odm/pull/14) by [@nayan32biswas](https://github.com/nayan32biswas).

## 0.2.3

### Features

- Multiple databases. PR [#11](https://github.com/nayan32biswas/mongodb-odm/pull/11) by [@nayan32biswas](https://github.com/nayan32biswas).
- Implement Db replica-set. PR [#10](https://github.com/nayan32biswas/mongodb-odm/pull/10) by [@nayan32biswas](https://github.com/nayan32biswas).

### Fixes

- Remove mutable variable as default. PR [#9](https://github.com/nayan32biswas/mongodb-odm/pull/9) by [@nayan32biswas](https://github.com/nayan32biswas).

## 0.2.2

### Features

- Implement transactions and make package py.typed. PR [#6](https://github.com/nayan32biswas/mongodb-odm/pull/6) by [@nayan32biswas](https://github.com/nayan32biswas).

## 0.2.1

### Refactors

- Type checking according to the mypy. PR [#5](https://github.com/nayan32biswas/mongodb-odm/pull/5) by [@nayan32biswas](https://github.com/nayan32biswas).

## 0.2.0

- The initial release of MongoDB-ODM, an Object Document Mapper based on PyMongo.
- Provides easy mapping of Python objects to MongoDB documents.
- Allows seamless interaction with MongoDB databases in Python applications.
- Includes support for all MongoDB data types.
- Offers intuitive APIs for common CRUD operations.
- Provides flexible query APIs with support for advanced querying features.
- Includes detailed documentation and examples for easy integration.
- Compatible with Python 3.6 and higher.

## 0.1.0a3 (PRE-RELEASE)

The whole project was restructured. But small change on the core functionality. PR [#2](https://github.com/nayan32biswas/mongodb-odm/pull/2) by [@nayan32biswas](https://github.com/nayan32biswas).

## 0.1a2 (PRE-RELEASE)

Write initial code according to architectural thought.
Write a test with coverage up to 95%. PR [#1](https://github.com/nayan32biswas/mongodb-odm/pull/1) by [@nayan32biswas](https://github.com/nayan32biswas).
