# Help MongoDB-ODM - Get Help

## Contributing

MongoDB-ODM is an open-source package that provides a powerful and flexible way to work with MongoDB databases in a Python environment. If you're a developer looking for an exciting project to contribute to, you are welcome here to contribute.

If you need to deep dive in the code, here are some guidelines.

### Python

MongoDB-ODM supports Python 3.8 and above. Make sure at least python 3.8 is installed on your device.

### Poetry

**MongoDB-ODM** uses <a href="https://python-poetry.org" class="external-link" target="_blank">Poetry</a> to build, package, and publish the project.

Install Poetry on your device by following <a href="https://python-poetry.org/docs/#installation" class="external-link" target="_blank">Official Doc</a>.

After installing the poetry please visit their <a href="https://python-poetry.org/docs" class="external-link" target="_blank">Official Doc</a> to know more about them.

### [Repository](https://github.com/nayan32biswas/mongodb-odm){.internal-link target=_blank}

First, make sure you have the repository, and you navigate the directory.

And change the code or documentation you want to change.

After the change follows the next steps.

### Format

There is a script that you can run, that will format and clean all your code:

```bash
poetry run bash scripts/format.sh
```

### Docs

To start the docs locally you can run this script:

```bash
poetry run bash scripts/docs-serve.sh
```

### Testing

For testing the package first we need to install and activate MongoDB.

Install MongoDB by following the <a href="https://www.mongodb.com/docs/manual/installation/" class="external-link" target="_blank">installation doc</a>. And start the MongoDB server.

Set `MONGO_URL` URL for your environment.

```bash
export MONGO_URL=<your-connection-url>
```

After installing the MongoDB and setting the environment key run this script:

```bash
poetry run bash scripts/test.sh
```

#### Testing with Docker

If you have installed docker on your device run this command for testing the package:

```bash
./scripts/test-with-docker.sh
```

### Create a Pull Request

You can contribute to the source code with **Pull Requests**.

- To fix a typo you found on the documentation.
- To propose new documentation sections.
- To fix an existing issue/bug.
    - Make sure to add tests.
- To add a new feature.
    - Make sure to add tests.
- Make sure to add documentation if it's relevant.

## Stay Connected

### Announcements

You can <a href="https://github.com/nayan32biswas/mongodb-odm/discussions/categories/announcements" class="external-link" target="_blank">follow announcements</a> in the GitHub repository, for example:

- New **Release**
- Breaking **Changes**

### Ideas

If you have new a idea please <a href="https://github.com/nayan32biswas/mongodb-odm/discussions/new?category=ideas" class="external-link" target="_blank">create</a> it in the GitHub repository, for example:

- The idea about the new **feature**


### Ask Questions

You can <a href="https://github.com/nayan32biswas/mongodb-odm/discussions/new?category=questions" class="external-link" target="_blank">create a new question</a> in the GitHub repository, for example:

- Ask a **question** or ask about a **problem**

### Issue

Found a new bug/issue or want to help others please visit <a href="https://github.com/nayan32biswas/mongodb-odm/issues" class="external-link" target="_blank">Github Issue</a>

## Connect with the author

You can connect with me on several platforms.

* <a href="https://github.com/nayan32biswas" class="external-link" target="_blank">Follow me on **GitHub**</a>.
    * Follow me to see when I create a new Open Source project.
* <a href="https://www.linkedin.com/in/nayan32biswas/" class="external-link" target="_blank">Connect with me on **Linkedin**</a>.
    * You can message me there. And also I will update package-related updates here.
