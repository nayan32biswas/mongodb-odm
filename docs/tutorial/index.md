# Intro, Installation, and Overview

## Intro

This tutorial will guide you step by step on how to use this package from a simple project to a large-scale project.

It is also built to work as a future reference, so you can come back and see exactly what you need.

## Editor Support

Since this package is built on top of <a href="https://docs.pydantic.dev" class="external-link" target="_blank">Pydantic</a>, you will get all types of support in your editor.

As a developer, it's very frustrating to get unhandled type errors in production. Instead of getting errors in production, you will get type hints and type-checking suggestions while you are writing the code.

## Start New Project

To start a new project, make sure you have the correct version of Python by running `python3 --version`. Python version **3.9 and above** is supported by this package.

Create a new folder with the command `mkdir new-project && cd new-project`.

You may also want to create a new virtual environment to avoid package dependency collision with other packages.

=== "Linux, macOS, Linux in Windows"

    <div>
    ```console
    // Create the virtual environment using the module "venv"
    $ python3 -m venv env
    // The following command will create the virtual environment in the directory "env"
    // Activate the virtual environment with the command
    $ source ./env/bin/activate
    // Verify that the virtual environment is active
    # (env) $$ which python
    // The important part is that it is inside the project directory, at "new-project/env/bin/python"
    /home/user/new-project/env/bin/python
    // Use the module "pip" to install and upgrade the package "pip" if needed
    # (env) $$ python -m pip install --upgrade pip
    ```
    </div>

## Install **MongoDB-ODM**

=== "Linux, macOS, Linux in Windows"

    <div>
    ```console
    # (env) $$ python3 -m pip install mongodb-odm
    ```
    </div>

## Install MongoDB

To install MongoDB, follow these instructions from MongoDB's official installation documentation.

<a  href="https://www.mongodb.com/docs/manual/installation/" class="external-link" target="_blank">Install MongoDB</a> from the official installation documentation. Follow their suggested instructions to check the version and other necessary things. Make sure you can connect to the database.

<a  href="https://www.mongodb.com/docs/compass/current/install/" class="external-link" target="_blank">Download and Install Compass</a> and open the expected database with the connection URL or suggested method in their documentation.

After installing MongoDB and Compass, we inserted some dummy data in the database. The initial information will look something like this.

<img class="shadow" src="/img/tutorial/index/image000.png">
