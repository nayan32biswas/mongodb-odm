# Find RAW

We have a special classmethod `find_raw`.

We can use this classmethod as a raw find function provided by `PyMongo`.

The `find_raw` method will return the `Cursor` of `PyMongo`.

If we iterate over the result then we should get a dictionary-type item.

The `find_raw` is a very thin layer on top of the `find` from `PyMongo`.

Behind the hood, multiple classmethod of **MongoDB-ODM** use `find_raw` for simplicity.

### Database

We will start from the same database structure and the same number of data as previously.

## Filter Collection

We can filter document using `find_raw`

```python
# Code omitted above

{!./docs_src/tutorial/find_raw/tutorial000.py[ln:46-50]!}

# Code omitted below
```

<details>
<summary>Full file preview</summary>
```Python
{!./docs_src/tutorial/find_raw/tutorial000.py!}
```
</details>

## Same as PyMongo find

Let's see a comparison of `find_raw` with `find` from `PyMongo`.

```python
# Code omitted above

{!./docs_src/tutorial/find_raw/tutorial000.py[ln:53-61]!}

# Code omitted below
```

<details>
<summary>Full file preview</summary>
```Python
{!./docs_src/tutorial/find_raw/tutorial000.py!}
```
</details>

Here variable `py_players` and `odm_players` are both 100% identical.

We can use `limit`, `sort`, `skip`, etc on both of the variables. Visit <a class="external-link" target="_blank" href="https://pymongo.readthedocs.io/en/stable/tutorial.html#querying-for-more-than-one-document">PyMongo</a> for more details.

## Why find_raw Needed

- MongoDB is a very flexible and dynamic database. Data can change very frequently.
- Sometimes static type ODM becomes problematic though it has a great auto complication.
- In some scenarios, we may need projection on the query to optimize network bandwidth. But find classmethod was not fully serving the purpose because some fields are required in Class Model.
- And lots of other cases where we don't want to use a static modeling system

In the above scenario, `find_raw` becomes very useful.

## Note

Behind-the-scene `find`, `find_one`, `get` and `get_or_create` use the `find_raw` classmethod to pull data from the database.
