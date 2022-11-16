from __future__ import annotations

import ast

import pytest

from flake8_airflow import Plugin


def result(s: str) -> set():
    return {"{}:{}: {}".format(*r) for r in Plugin(ast.parse(s)).run()}


@pytest.fixture
def subdag_fixture() -> str:
    return """from airflow.models import DAG

from airflow.operators.subdag import SubDagOperator
from airflow.operators.empty import EmptyOperator


with DAG(
    "test_sub_dag",
    schedule=None,
    default_args={
        "start_time": "2022-11-12",
        "retries": 3,
    },
) as dag:

    sd = SubDagOperator(
        "my_subdag",
        dag=dag,
    )

    dummy = EmptyOperator("empty", dag=sd)
"""


@pytest.fixture
def missing_retries_fixture() -> str:
    return """from airflow.models import DAG

from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator


with DAG(
    "test_sub_dag",
    schedule=None,
    default_args={
        "start_time": "2022-11-12",
    },
) as dag:

    sd = PythonOperator(
        "my_subdag",
        dag=dag,
    )

    dummy = EmptyOperator("empty", dag=sd)"""


@pytest.fixture
def bash_operator_fixture() -> str:
    return """from airflow.models import DAG

from airflow.operators.bash import BashOperator
from airflow.operators.empty import EmptyOperator


with DAG(
    "test_sub_dag",
    schedule=None,
    default_args={
        "start_time": "2022-11-12",
        "retries": 3,
    },
) as dag:

    sd = BashOperator(
        "my_subdag",
        dag=dag,
    )

    dummy = EmptyOperator("empty", dag=sd)
"""


def test_sub_dag_returns_errors(subdag_fixture) -> None:
    res = result(subdag_fixture)
    assert len(res) == 1
    res = res.pop()
    assert "AA101" in res


def test_missing_retries_errors(missing_retries_fixture) -> None:
    res = result(missing_retries_fixture)
    assert len(res) == 1
    res = res.pop()
    assert "AA103" in res


def test_bash_operators_returns_errors(bash_operator_fixture) -> None:
    res = result(bash_operator_fixture)
    assert len(res) == 1
    res = res.pop()
    assert "AA102" in res
