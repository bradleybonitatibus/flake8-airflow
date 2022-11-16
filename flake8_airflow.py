"""Flake8 extension for Apache Airflow code."""
from __future__ import annotations

import ast
from typing import Generator, Any, List

AA101 = "AA101 `SubDagOperator` used, should use TaskGroups instead"
AA102 = "AA102 `BashOperator` used, potential security risk"
AA103 = "AA103 `retries` argument missing from `DAG` `default_args` constructor"


def contains_key(keys: List[ast.Constant], key: str) -> bool:
    """Check ast constants for seeing if a key exists.

    Args:
        keys (typing.List[ast.Constant]): Keys from Keywords
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
            kw: List[ast.keyword] = node.keywords
            for k in kw:
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
