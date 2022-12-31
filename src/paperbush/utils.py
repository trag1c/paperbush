from __future__ import annotations

from string import digits


def bisect(string: str, index: int | str) -> tuple[str, str]:
    if isinstance(index, str):
        index = string.index(index)
    return string[:index], string[index:]


def is_int(string: str) -> bool:
    return bool(string) and all(char in digits for char in string)


def slice_until(string: str, target: str) -> str:
    return string[:string.find(target)]


def stripped_len(string: str, chars: str) -> int:
    return len(string) - len(string.lstrip(chars))
