# `flake8-airflow`

[![CI](https://github.com/bradleybonitatibus/flake8-airflow/actions/workflows/ci.yaml/badge.svg)](https://github.com/bradleybonitatibus/flake8-airflow/actions/workflows/ci.yaml)
[![PyPI version](https://badge.fury.io/py/flake8-airflow.svg)](https://badge.fury.io/py/flake8-airflow)
[![OpenSSF Best Practices](https://bestpractices.coreinfrastructure.org/projects/6705/badge)](https://bestpractices.coreinfrastructure.org/projects/6705)

An opinioned `flake8` plugin with Apache Airflow rules.

## Installing

You can install this extension from `pypi` using
```
pip install flake8-airflow
```

## Rules

The following is a table of rules, what they mean, and why they exist.

| Rule Name | Description | Purpose |
| --------- | ----------- | ------- |
| `AA101`   | Use of `SubDagOperator` | Airflow has deprecated `SubDagOperator` since 2.0 and should not be used |
| `AA102`   | Use of `BashOperator` | Airflow does not escape strings sent to the `bash_command` <sup>[1](https://registry.astronomer.io/providers/apache-airflow/modules/bashoperator)</sup> and is a potential security risk |
| `AA103`   | Missing `retries` default argument in `DAG` constructor | Retries improve DAG resiliency  |
