# Find and Sort Data

To find and sort documents, we will use the same classmethod `find` that we are using for finding and filtering data.

### Database

We will start with the same database structure and the same amount of data as previously.

## Sort by ID desc

```python
# Code omitted above

{!./docs_src/tutorial/find_and_sort/tutorial000.py[ln:52-56]!}

# Code omitted below
```

<details>
<summary>Full file preview</summary>
```Python
{!./docs_src/tutorial/find_and_sort/tutorial000.py!}
```
</details>

## Sort With Multiple Keys

```python
# Code omitted above

{!./docs_src/tutorial/find_and_sort/tutorial000.py[ln:59-63]!}

# Code omitted below
```

<details>
<summary>Full file preview</summary>
```Python
{!./docs_src/tutorial/find_and_sort/tutorial000.py!}
```
</details>

!!! warning
    Sorting on non-indexed fields (`country_code`) is not efficient.
