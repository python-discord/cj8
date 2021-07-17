# Python Summer Code Jam 2021
## Code Jam
* Theme: TUI
* Framework: [Blessed](https://github.com/chjj/blessed)


* Tooling to launch an IPython session with automatic reloading enabled

If you are instead looking for a [Python application](https://caremad.io/posts/2013/07/setup-vs-requirement/) template, check out one of the sibling projects:

* [jacebrowning/template-django](https://github.com/jacebrowning/template-django)
* [jacebrowning/template-flask](https://github.com/jacebrowning/template-flask)

## Examples

Here are a few sample projects based on this template:

* [jacebrowning/minilog](https://github.com/jacebrowning/minilog)
* [theovoss/Chess](https://github.com/theovoss/Chess)
* [sprout42/StarStruct](https://github.com/sprout42/StarStruct)
* [MichiganLabs/flask-gcm](https://github.com/MichiganLabs/flask-gcm)
* [flask-restful/flask-restful](https://github.com/flask-restful/flask-restful)

## Usage

Install `cookiecutter` and generate a project:

```
$ pip install cookiecutter
$ cookiecutter gh:jacebrowning/template-python -f
```

Cookiecutter will ask you for some basic info (your name, project name, python package name, etc.) and generate a base Python project for you.

If you still need to use legacy Python or `nose` as the test runner, older versions of this template are available on branches:

```
$ cookiecutter gh:jacebrowning/template-python -f --checkout=python2

$ cookiecutter gh:jacebrowning/template-python -f --checkout=nose
```

## Updates

Run the update tool, which is generated inside each project:

```
$ bin/update
```
