from __future__ import annotations

from argparse import ArgumentParser, Namespace
from sys import argv
from typing import Any, cast

from .exceptions import PaperbushError, PaperbushSyntaxError
from .parser import Argument, parse_argument, split_args


class Paperbush:
    __slots__ = ("_parser", "_infer_names", "pattern")

    def __init__(self, pattern: str, *, infer_names: bool = True) -> None:
        self.pattern = pattern
        self._parser = ArgumentParser()
        self._infer_names = infer_names
        self._translate()

    def parse_args(self) -> Namespace:
        return self.parse(argv)

    def parse(self, args: str | list[str]) -> Namespace:
        if isinstance(args, str):
            args = args.split()
        return self._parser.parse_args(args)

    def _translate(self) -> None:
        args = [
            parse_argument(arg, infer_name=self._infer_names)
            for arg in split_args(self.pattern)
        ]
        for arg in args:
            if arg == "^":
                print(arg)
            else:
                assert isinstance(arg, Argument)
                print(arg, arg.type_, arg.action)
        if not args:
            raise PaperbushError("cannot create a parser with no arguments")
        if not are_xors_correctly_placed(args):
            raise PaperbushSyntaxError("invalid '^' placement")
        group_indexes = merge_group_indexes(
            [(i - 1, i + 1) for i, v in enumerate(args) if v == "^"]
        )
        print(group_indexes)
        grouped_args = group_args(args, group_indexes)
        print(grouped_args)
        for arg in grouped_args:
            if isinstance(arg, tuple):
                group = self._parser.add_mutually_exclusive_group()
                for argument in arg:
                    group.add_argument(*argument, **argument.kwargs)
            else:
                self._parser.add_argument(*arg, **arg.kwargs)


def are_xors_correctly_placed(args: list[Argument | str]) -> bool:
    if "^" in (args[0], args[-1]):
        return False
    for i, v in enumerate(args[1:], 1):
        if v == args[i - 1] == "^":
            return False
    return True


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
