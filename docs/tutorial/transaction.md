# Transaction

## Introduction

MongoDB transactions are needed to ensure data consistency in complex operations that involve multiple documents and collections. By grouping multiple operations into a single transaction, you can ensure that all operations either succeed or fail together, preventing data inconsistencies and race conditions.

We suggest reading the doc from <a href="https://www.mongodb.com/docs/manual/core/transactions/" class="external-link" target="_blank">MongoDB</a> about transactions.

## Start transaction

To implement transactions, we will use the default mechanism of <a href="https://pymongo.readthedocs.io/en/stable/api/pymongo/client_session.html#transactions" class="external-link" target="_blank">PyMongo Transactions</a>.

First, we will start a session using **with** to implement transactions.

Then start the transaction using the session object.

```Python hl_lines="15-16"
{!./docs_src/tutorial/transaction/tutorial000.py[ln:1-26]!}

# Code omitted below
```

<details>
<summary>Full file preview</summary>
```Python
{!./docs_src/tutorial/transaction/tutorial000.py!}
```
</details>

## Create document using transaction

To create an object with a transaction mechanism, we will pass the **session** object as **kwargs** in the create method.

If something goes wrong, then we need to abort the actions by manually calling the **abort** function. Otherwise, partial actions will be applied.

```Python hl_lines="10 15"
# Code omitted above

{!./docs_src/tutorial/transaction/tutorial000.py[ln:14-26]!}

# Code omitted below
```

<details>
<summary>Full file preview</summary>
```Python
{!./docs_src/tutorial/transaction/tutorial000.py!}
```
</details>

!!!warning
    We need to call the `session.abort_transaction()` explicitly to abort the actions. If a partial function is executed and something goes wrong, then we need to call the `abort_transaction`; otherwise, partial actions will be applied.

## Update document using transaction

We can use transactions on update operations.

We need to pass the **session** object as **kwargs** in the update method.

```Python hl_lines="9 13"
# Code omitted above

{!./docs_src/tutorial/transaction/tutorial000.py[ln:29-41]!}

# Code omitted below
```

<details>
<summary>Full file preview</summary>
```Python
{!./docs_src/tutorial/transaction/tutorial000.py!}
```
</details>

## Delete document using transaction

We can use transactions on delete operations.

We need to pass the **session** object as **kwargs** in the delete method.

```Python hl_lines="8 11"
# Code omitted above

{!./docs_src/tutorial/transaction/tutorial000.py[ln:44-54]!}

# Code omitted below
```

<details>
<summary>Full file preview</summary>
```Python
{!./docs_src/tutorial/transaction/tutorial000.py!}
```
</details>

## Full Code

```Python
{!./docs_src/tutorial/transaction/tutorial000.py!}
```
