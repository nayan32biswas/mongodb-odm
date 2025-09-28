# Model Inheritance

We can implement model inheritance at the collection level.

## Scenario

Let's imagine we want to implement a course system.

The course can have multiple types of content like `text`, `video`, `image`, `file`, etc. But all share some common fields like `course_id`, `created_at`, etc. And content should be listed.

We can use this functionality relationally, but it will be expensive to query because we need multiple lookups.

In this scenario, we can implement **Model Inheritance** provided by **MongoDB-ODM**.
(Note: Currently, only **one level** of inheritance is supported.)

## Define Model

In this section, we will use multiple models to implement **model inheritance**.

### Overview

First look at all models in a single block for better understanding.

```python hl_lines="12 18 21-22"
# Code omitted above

{!./docs_src/advanced_tutorial/model_inheritance/tutorial000.py[ln:14-40]!}

# Code omitted below
```

<details>
<summary>Full file preview</summary>
```Python
{!./docs_src/advanced_tutorial/model_inheritance/tutorial000.py!}
```
</details>

We want to keep everything simple. First, we define the course, where courses only have one field: `title`.

### Content

We define the `Content` model. We want to inherit the content model in the `Text` and `Video` models.

In the `ODMConfig` class for the `Content` model, we define `allow_inheritance = True`. To make a model inheritable, we need to set this field to `True`.

```python hl_lines="6"
{!./docs_src/advanced_tutorial/model_inheritance/tutorial000.py[ln:18-26]!}
```

### Text

After defining the `Content` model, we will define the `Text` model that inherits from the `Content` model to have all the functionality of `Content`.

Set `allow_inheritance = False` for the `Text` model. Otherwise, **MongoDB-ODM** will throw an error.

```python hl_lines="5"
{!./docs_src/advanced_tutorial/model_inheritance/tutorial000.py[ln:29-33]!}
```

### Video

Like the `Text` functionality and declaration structure, the `Video` will be the same.

```python hl_lines="5"
{!./docs_src/advanced_tutorial/model_inheritance/tutorial000.py[ln:36-40]!}
```

## Insert Data

Let's insert some data in the `Course` and `Content` collection.

First, we create a course document.

Then we create two `Content` documents: one `Text` content and one video content.

```python
{!./docs_src/advanced_tutorial/model_inheritance/tutorial000.py[ln:48-56]!}
```

<details>
<summary>Full file preview</summary>
```Python
{!./docs_src/advanced_tutorial/model_inheritance/tutorial000.py!}
```
</details>

### Impact in Database

For model inheritance, we do not create a separate collection for each model. Instead, we create a single collection for all models, and the collection name will be according to the parent class. We add an extra field `_cls` with each document to distinguish between the different models.

!!!tip
    By default, we define the `_cls` field as an `index` field. We can remove the index for this field by defining `index_inheritance_field = False` in the parent ODMConfig.
    ```python hl_lines="4"
    class Content(Document):
        ...
        class ODMConfig(Document.ODMConfig):
            index_inheritance_field = False
    ```

## Retrieve Collection

We can use all our retrieval methods to retrieve data for the inherited model. We will add an extra filter key `{"_cls": '<Model Name>'}` to filter out the targeted children, or no extra filter for parents.

### Filter Content

To get all content, we can filter data with the parent class `Content`.

```python
{!./docs_src/advanced_tutorial/model_inheritance/tutorial000.py[ln:59-62]!}
```

<details>
<summary>Full file preview</summary>
```Python
{!./docs_src/advanced_tutorial/model_inheritance/tutorial000.py!}
```
</details>

After running this function, the printed object should look like this.

```bash
Text(id=ObjectId('id'), course_id=ObjectId('id'), title='Introduction', text='Introduction Text', _id=ObjectId('id'))
Video(id=ObjectId('id'), course_id=ObjectId('id'), title='Environment Setup', video_path='/media/video_path.mp4', _id=ObjectId('id'))
```

## Retrieve Text and Video

We can retrieve data using the `Text` and `Video` models.

```python
{!./docs_src/advanced_tutorial/model_inheritance/tutorial000.py[ln:65-74]!}
```

<details>
<summary>Full file preview</summary>
```Python
{!./docs_src/advanced_tutorial/model_inheritance/tutorial000.py!}
```
</details>

After executing the `retrieve_text` and `retrieve_video` functions the output should look like this.

```bash
Text(id=ObjectId('id'), course_id=ObjectId('id'), title='Introduction', text='Introduction Text', _id=ObjectId('id'))

Video(id=ObjectId('id'), course_id=ObjectId('id'), title='Environment Setup', video_path='/media/video_path.mp4', _id=ObjectId('id'))
```

### **find_one** and **get** with inheritance

Like the `find` method, we can retrieve the child object from the parent using the `find_one` and `get` methods. If the retrieved object appears to be one of the children, then the object will have all of the properties of that child.
