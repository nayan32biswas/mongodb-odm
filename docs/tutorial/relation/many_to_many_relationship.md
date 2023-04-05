# Many to Many Relationship Intro

In a traditional SQL database, we use 3rd table to implement many-to-many relations. Where the middle table holds the id from table `A` and the id from `B`.

In this chapter, we will add skills for players.

In MongoDB, we can implement many-to-many relations with two-way embedded ways and traditional ways. MongoDB won't block us from doing any one of these.

We add another model `Skill` alongside `Country` and `Player` to illustrate many-to-many relations.

## Model definition

First, we will implement the traditional way of implementing many-to-many relations.

First declare the `Country`, `Skill`, and `Player` model.

Then declare the middle model `PlayerSkill` that will have `player_id`, `skill_id`, and `rating` fields.

```Python hl_lines="23"
# Code omitted above

{!./docs_src/tutorial/relation/many_to_many_relationship/tutorial000.py[ln:16-50]!}

# Code omitted below
```

<details>
<summary>Full file preview</summary>
```Python
{!./docs_src/tutorial/relation/many_to_many_relationship/tutorial000.py!}
```
</details>

### Multi key indexes

We will define a multi-key index for better performance. Also, we want `player_id` and `skill_id` to be unique.

```Python hl_lines="14"
# Code omitted above

{!./docs_src/tutorial/relation/many_to_many_relationship/tutorial000.py[ln:36-50]!}

# Code omitted below
```

Here we use `IndexModel` which is directly used from `Pymongo`.

### Read data

We will get one of the player data and his skills.

```Python
# Code omitted above

{!./docs_src/tutorial/relation/many_to_many_relationship/tutorial000.py[ln:77-82]!}

# Code omitted below
```

<details>
<summary>Full file preview</summary>
```Python
{!./docs_src/tutorial/relation/many_to_many_relationship/tutorial000.py!}
```
</details>

After running the `read_data` function console should print.

```bash
Player(id=ObjectId('id'), name='Pelé', country_id=ObjectId('id'), _id=ObjectId('id'))

[PlayerSkill(id=ObjectId('id'), player_id=ObjectId('id'), skill_id=ObjectId('id'), rating=49, _id=ObjectId('id')), PlayerSkill(id=ObjectId('id'), player_id=ObjectId('id'), skill_id=ObjectId('id'), rating=49, _id=ObjectId('id'))]
```

### Run Full Code

Run the code and check the MongoDB document viewer to see the impact.

```Python
{!./docs_src/tutorial/relation/many_to_many_relationship/tutorial000.py!}
```


## Model definition (Embedded way)

In this example, we use MongoDB Embedded way to implement many-to-many relations.

```Python hl_lines="7 11 21"
# Code omitted above

{!./docs_src/tutorial/relation/many_to_many_relationship/tutorial001.py[ln:17-40]!}

# Code omitted below
```

<details>
<summary>Full file preview</summary>
```Python
{!./docs_src/tutorial/relation/many_to_many_relationship/tutorial001.py!}
```
</details>

First, we define the new model `Skill`.

Then we define the Pydantic model `EmbeddedSkill`. Where the name is not special and we can you any name we want.

The `EmbeddedSkill` has two fields `ODMObjectId` type `skill_id` and `int` type rating.

We add the `List[EmbeddedSkill] `type `skills` field in `Player` mode.

### Insert Data

First, create a `country` and `skill` document.

Then create a player with a list of `EmbeddedSkill`.

```Python
# Code omitted above

{!./docs_src/tutorial/relation/many_to_many_relationship/tutorial001.py[ln:43-75]!}

# Code omitted below
```

<details>
<summary>Full file preview</summary>
```Python
{!./docs_src/tutorial/relation/many_to_many_relationship/tutorial001.py!}
```
</details>

### Read Data

Let's get one of the player data.

```Python
# Code omitted above

{!./docs_src/tutorial/relation/many_to_many_relationship/tutorial001.py[ln:78-80]!}

# Code omitted below
```

<details>
<summary>Full file preview</summary>
```Python
{!./docs_src/tutorial/relation/many_to_many_relationship/tutorial000.py!}
```
</details>

After running the `read_data` function console should print.

```bash
Player(id=ObjectId('id'), name='Pelé', country_id=ObjectId('id'), skills=[EmbeddedSkill(skill_id=ObjectId('id'), rating=49), EmbeddedSkill(skill_id=ObjectId('id'), rating=49)], _id=ObjectId('id'))

```

### Run Full Code

Run the code and check the MongoDB document viewer to see the impact.

```Python
{!./docs_src/tutorial/relation/many_to_many_relationship/tutorial001.py!}
```
