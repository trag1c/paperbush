from __future__ import annotations

from argparse import ArgumentParser, Namespace
from sys import argv

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
        indexes = extract_indexes(args)
        print(indexes)
        indexes = group_indexes(indexes)
        print(indexes)
        # TODO


def extract_indexes(args: list[Argument | str]) -> list[tuple[int, int]]:
    found = 0
    indexes = []
    for i, v in enumerate(args):
        if v == "^":
            indexes.append((i - 1 + found, i + found))  # FIXME
            found += 1
            args.pop(i)
    return indexes


def group_indexes(indexes: list[tuple[int, int]]) -> list[tuple[int, ...]]:
    if not indexes:
        return indexes
    grouped = [indexes.pop(0)]
    for i in indexes:
        last = grouped[-1]
        if i[0] == last[-1]:
            last = (*last, i[0])
        else:
            grouped.append(i)
    return grouped
