# `flake8-airflow`

An opinioned `flake8` plugin for Apache Airflow.


## Rules

The following is a table of rules, what they mean, and why they exist.

| Rule Name | Description | Purpose |
| --------- | ----------- | ------- |
| `AA101`   | Use of `SubDag` | Airflow has deprecated `SubDag` since 2.0 and should not be used |
| `AA102`   | Use of `BashOperator` | Airflow does not escape strings sent to the `bash_command` <sup>[1](https://registry.astronomer.io/providers/apache-airflow/modules/bashoperator)</sup> |
| `AA103`   | Missing `retries` default argument in `DAG` constructor | Retries improve DAG resiliency  | 
