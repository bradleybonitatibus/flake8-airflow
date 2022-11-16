# Contributing Guide

This is the contributing guide for `flake8-airflow`.
To contribute, you'll want to open a pull request from a fork, and make sure
that your fork is up to date with `main`.

The main things to contribute to on this project will be adding additional
rules to enforce against `apache-airflow`.

## Getting Started

You can get started with forking the repo, and setting up a development
environment

```sh
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt -r dev-requirements.txt
```

You can verify changes with the provided `Makefile` that can run tests
and some static analysis tasks.
