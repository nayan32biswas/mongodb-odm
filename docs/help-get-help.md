# Help MongoDB-ODM - Get Help

## Contributing

MongoDB-ODM is an open-source package that provides a powerful and flexible way to work with MongoDB databases in a Python environment. If you're a developer looking for an exciting project to contribute to, you are welcome to contribute here.

If you need to deep dive into the code, here are some guidelines.

### Python

MongoDB-ODM supports Python 3.9 and above. Make sure at least Python 3.9 is installed on your device.

### UV

**MongoDB-ODM** uses <a href="https://docs.astral.sh/uv" class="external-link" target="_blank">UV</a> to build, package, and publish the project.

Install UV on your device by following the <a href="https://docs.astral.sh/uv/getting-started/installation/" class="external-link" target="_blank">Official Documentation</a>.

After installing UV, please visit their <a href="https://docs.astral.sh/uv" class="external-link" target="_blank">Official Documentation</a> to learn more about it.

### [Repository](https://github.com/nayan32biswas/mongodb-odm){.internal-link target=\_blank}

First, make sure you have the repository, and navigate to the directory.

Change the code or documentation you want to modify.

After making changes, follow the next steps.

### Format

There is a script you can run that will format and clean all your code:

```bash
./scripts/format.sh
```

### Docs

To start the docs locally, you can run this script:

```bash
./scripts/docs.sh
```

### Testing

For testing the package, first we need to install and activate MongoDB.

Install MongoDB by following the <a href="https://www.mongodb.com/docs/manual/installation/" class="external-link" target="_blank">installation documentation</a> and start the MongoDB server.

Set the `MONGO_URL` environment variable:

```bash
export MONGO_URL=<your-connection-url>
```

After installing MongoDB and setting the environment variable, run this script:

```bash
./scripts/test.sh
```

#### Testing with Docker

If you have Docker installed on your device, run this command to test the package:

```bash
./scripts/test-with-docker.sh
```

### Create a Pull Request

You can contribute to the source code with **Pull Requests**.

- To fix a typo you found in the documentation.
- To propose new documentation sections.
- To fix an existing issue/bug.
  - Make sure to add tests.
- To add a new feature.
  - Make sure to add tests.
- Make sure to add documentation if it's relevant.

#### Steps to Follow Before Creating a PR

If you change the codebase, make sure to follow these steps before creating a PR.

- `./scripts/test.sh` Run the unit tests and make sure all tests pass and test coverage is more than 95%.
- `./scripts/lint.sh` Check that all formatting is implemented and code format is accurate.
- `./scripts/format.sh` Run auto-formatting like import sorting, etc.

## Stay Connected

### Announcements

You can <a href="https://github.com/nayan32biswas/mongodb-odm/discussions/categories/announcements" class="external-link" target="_blank">follow announcements</a> in the GitHub repository, for example:

- New **Release**
- Breaking **Changes**

### Ideas

If you have a new idea, please <a href="https://github.com/nayan32biswas/mongodb-odm/discussions/new?category=ideas" class="external-link" target="_blank">create</a> it in the GitHub repository, for example:

- An idea about a new **feature**

### Ask Questions

You can <a href="https://github.com/nayan32biswas/mongodb-odm/discussions/new?category=questions" class="external-link" target="_blank">create a new question</a> in the GitHub repository, for example:

- Ask a **question** or ask about a **problem**

### Issues

Found a new bug/issue or want to help others? Please visit <a href="https://github.com/nayan32biswas/mongodb-odm/issues" class="external-link" target="_blank">GitHub Issues</a>.

## Connect with the Author

You can connect with me on several platforms.

- <a href="https://github.com/nayan32biswas" class="external-link" target="_blank">Follow me on **GitHub**</a>.
  - Follow me to see when I create a new Open Source project.
- <a href="https://www.linkedin.com/in/nayan32biswas/" class="external-link" target="_blank">Connect with me on **Linkedin**</a>.
  - You can message me there. I will also update package-related information here.
