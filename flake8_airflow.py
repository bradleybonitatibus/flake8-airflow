# Copyright 2022 Bradley Bonitatibus

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Flake8 extension for Apache Airflow code.

The main purpose of having flake8 rules specific to Apache Airflow code
is to constrain the use of some not so nice behaviours.

For example, SubDags have been deprecated, and before, were an anti-pattern that
caused issues like deadlocks.

Another example is BashOperators, which don't escape shell commands,
and can potentially run arbitrary code outside the Airflow process.
"""
from __future__ import annotations

import ast
from typing import Generator, Any

AA101 = "AA101 `SubDagOperator` used, should use TaskGroups instead"
AA102 = "AA102 `BashOperator` used, potential security risk"
AA103 = "AA103 `retries` argument missing from `DAG` `default_args` constructor"


def contains_key(keys: list[ast.Constant], key: str) -> bool:
    """Check ast constants for seeing if a key exists.

    Args:
        keys (list[ast.Constant]): Keys from Keywords
        key (str): Key looking for

    Returns:
        bool
    """
    for k in keys:
        if k.n == key:
            return True
    return False


class Visitor(ast.NodeVisitor):
    """AST Visitor to parse."""

    def __init__(self) -> None:
        """Custom ast.Visitor for plugin."""
        self.errors: list[tuple[int, int, str]] = []
        self._from_imports: dict[str, str] = {}

    def visit_Name(self, node: ast.Name) -> None:
        """Visits ast.Name nodes and checks for use of SubDag and Bash operators.

        Args:
            node (ast.Name): ast.Name node

        Returns:
            None
        """
        if node.id == "SubDagOperator":
            self.errors.append(
                (node.lineno, node.col_offset, AA101),
            )
        elif node.id == "BashOperator":
            self.errors.append(
                (node.lineno, node.col_offset, AA102),
            )
        self.generic_visit(node)

    def visit_Call(self, node: ast.Call) -> None:
        """Visits an ast.Call.

        Args:
            node (ast.Call): ast Call node

        Returns:
            None
        """
        n: ast.Name = node.func
        if n.id == "DAG":
            for k in node.keywords:
                if "default_args" in k.arg and not contains_key(
                    k.value.keys, "retries"
                ):
                    self.errors.append((k.lineno, node.col_offset, AA103))

        self.generic_visit(node)


class Plugin:
    """Custom flake8 plugin for Apache Airflow rules."""

    name = __name__

    def __init__(self, tree: ast.AST):
        """Instantiate Plugin.

        Args:
            tree (ast.Tree): AST Tree
        """
        self._tree = tree

    def run(self) -> Generator[tuple[int, int, str, type[Any]], None, None]:
        """Runs the plugin and yields errors if any.

        Yields:
            tuple[int, int, str, Type[Any]]
        """
        visitor = Visitor()

        visitor.visit(self._tree)

        for line, col, msg in visitor.errors:
            yield line, col, msg, type(self)
