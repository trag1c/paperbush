from __future__ import annotations

from argparse import ArgumentParser, Namespace
from shlex import split
from sys import argv
from typing import Any, cast

from .exceptions import PaperbushError, PaperbushSyntaxError
from .parser import Argument, parse_argument, split_args


class Paperbush:
    """
    A Paperbush parser; takes a string pattern written in the\
    [Paperbush custom language](https://trag1c.github.io/paperbush/dsl/),\
    an arbitrary number of\
    [reference values](https://trag1c.github.io/paperbush/dsl/#value-references),
    and the `infer_names` flag which specifies whether arguments with only long names
    should have the short names inferred (`True` by default).
    """

    __slots__ = ("args", "_parser", "_infer_names", "_values", "pattern")

    def __init__(self, pattern: str, *values: Any, infer_names: bool = True) -> None:
        self.pattern = pattern
        self.args: list[Argument | tuple[Argument, ...]] = []
        self._parser = ArgumentParser(add_help=False)
        self._infer_names = infer_names
        self._values = list(values)
        self._translate()

    def parse_args(self) -> Namespace:
        """
        Equivalent to `Paperbush.parse(sys.argv)`.
        """
        return self.parse(argv[1:])

    def parse(self, args: str | list[str]) -> Namespace:
        """
        Parses command line arguments using the predefined pattern and returns an
        `argparse.Namespace` object. Accepts either a list of strings or a single string
        (which is split with `shlex.split`).
        """
        if isinstance(args, str):
            args = split(args)
        return self._parser.parse_args(args)

    def _translate(self) -> None:
        args: list[Argument | str] = [
            parse_argument(arg, infer_name=self._infer_names, values=self._values)
            for arg in split_args(self.pattern)
        ]

        if not args:
            raise PaperbushError("cannot create a parser with no arguments")
        if not are_xors_correctly_placed(args):
            raise PaperbushSyntaxError("invalid '^' placement")
        group_indexes = merge_group_indexes(
            [(i - 1, i + 1) for i, v in enumerate(args) if v == "^"]
        )
        self.args = grouped_args = group_args(args, group_indexes)
        for arg_or_args in grouped_args:
            if isinstance(arg_or_args, tuple):
                args_ = arg_or_args
                group = self._parser.add_mutually_exclusive_group()
                for arg in args_:
                    if arg.required:
                        group.required = True
                        arg.required = False
                    group.add_argument(*arg, **arg.kwargs)
            else:
                arg = arg_or_args
                self._parser.add_argument(*arg, **arg.kwargs)


def are_xors_correctly_placed(args: list[Argument | str]) -> bool:
    if "^" in (args[0], args[-1]):
        return False
    return all(not (v == args[i - 1] == "^") for i, v in enumerate(args[1:], 1))


def group_args(
    args: list[Argument | str], group_indexes: list[tuple[int, ...]]
) -> list[Argument | tuple[Argument, ...]]:
    grouped: list[Argument | tuple[Argument, ...]] = []
    indexes = [i for i, v in enumerate(args) if v != "^"]
    for group in group_indexes:
        grouped.append(tuple(cast(Argument, args[i]) for i in group))
        for i in group:
            indexes.remove(i)
    for i in indexes:
        grouped.append(cast(Argument, args[i]))
    return grouped


def merge_group_indexes(indexes: list[tuple[int, int]]) -> list[tuple[int, ...]]:
    if not indexes:
        return indexes
    grouped: list[tuple[int, ...]] = [indexes.pop(0)]
    for i in indexes:
        last = grouped[-1]
        if i[0] == last[-1]:
            grouped[-1] = (*last, i[1])
        else:
            grouped.append(i)
    return grouped
