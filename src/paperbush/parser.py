from __future__ import annotations

from collections.abc import Container, Iterator
from enum import Enum
from re import match
from string import ascii_letters, digits
from typing import Any

from .exceptions import PaperbushNameError, PaperbushSyntaxError


class Action(Enum):
    STORE_TRUE = "store_true"
    COUNT = "count"


class Argument:
    __slots__ = (
        "_action",
        "choices",
        "default",
        "infer_short",
        "name",
        "nargs",
        "pattern",
        "required",
        "_short",
        "type_",
    )

    def __init__(
        self,
        *,
        pattern: str,
        name: str | None = None,
        nargs: str | int | None = None,
        action: Action | None = None,
        required: bool | None = None,
        default: Any = None,
        choices: Container[Any] | None = None,
        type_: Any = None,
        infer_short: bool = False,
        short: str | None = None,
    ) -> None:
        self._action = None
        if not (name or short):
            raise PaperbushNameError("missing argument name")
        self.default = default
        self.action = action
        self.choices = choices
        self.infer_short = infer_short
        self.name = name
        self.nargs = nargs
        self.pattern = pattern
        self.required = required
        self._short = short
        self.type_ = type_

    def __hash__(self) -> int:
        return hash(tuple(self))

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Argument):
            return hash(self) == hash(other)
        return NotImplemented

    @property
    def action(self) -> Action | None:
        return self._action

    @action.setter
    def action(self, value: Action | None) -> None:
        if self.default is None and value is Action.COUNT:
            self.default = 0
        self._action = value

    @property
    def short(self) -> str | None:
        if (
            self._short is None
            and self.infer_short
            and self.name is not None
            and self.name.startswith("--")
        ):
            return "-" + self.name.lstrip("-")[0]
        return self._short

    @property
    def kwargs(self) -> dict[str, str | bool | int]:
        kwargs: dict[str, str | bool | int] = filtered_dict(
            required=self.required,
            nargs=self.nargs,
            type=self.type_,
            default=self.default,
            choices=self.choices,
        )
        if self.action:
            kwargs["action"] = self.action.value
        return kwargs

    def __iter__(self) -> Iterator[str]:
        if self.short:
            yield self.short
        if self.name:
            yield self.name

    def __repr__(self) -> str:
        return f"Argument[{self.pattern}]"


def bisect(string: str, index: int | str) -> tuple[str, str]:
    if isinstance(index, str):
        index = string.index(index)
    return string[:index], string[index:]


def is_int(string: str) -> bool:
    return bool(string) and all(char in digits for char in string)


def evaluate(string: str, values: list[Any]) -> Any:
    return values[value_ref(string)] if is_value_ref(string) else eval(string)


def is_value_ref(string: str) -> bool:
    return string[0] == "$" and is_int(string[1:])


def value_ref(string: str) -> int:
    return int(string[1:])


def slice_until(string: str, target: str) -> str:
    return string[: string.find(target)]


def stripped_len(string: str, chars: str) -> int:
    return len(string) - len(string.lstrip(chars))


def filtered_dict(**kwargs: Any) -> dict[str, Any]:
    return {k: v for k, v in kwargs.items() if v is not None}


def are_matching_brackets(string: str) -> bool:
    opening = "[({"
    closing = "])}"
    if not any(i in string for i in opening + closing):
        return True
    pairs = dict(zip(closing, opening))
    stack: list[str] = []
    is_string: str | None = None
    for char in string:
        if not is_string and char in "\"'":
            is_string = char
        elif is_string == char:
            is_string = None
        elif char in opening:
            stack.append(char)
        elif char in closing:
            top = stack.pop()
            if pairs[char] != top:
                raise PaperbushSyntaxError(f"unmatching brackets: {top!r} {char!r}")
    return not stack


def split_args(string: str) -> list[str]:
    frags = string.split()
    out = []
    temp = ""
    f = frags.pop(0)
    while frags or f:
        if temp:
            if are_matching_brackets(temp):
                out.append(temp)
                temp = ""
                continue
            temp += " " + f
        elif are_matching_brackets(f):
            out.append(f)
        else:
            temp = f
        if not frags:
            break
        f = frags.pop(0)
    if temp and are_matching_brackets(temp):
        out.append(temp)
    return out


def parse_argument(
    string: str, *, infer_name: bool = True, values: list[Any] | None = None
) -> Argument | str:
    if string == "^":
        return string

    values = values or []

    argument, string = parse_name(string)
    argument.infer_short = infer_name

    if string in "!":
        req = string == "!"
        if stripped_len(argument.name or "", "-"):
            argument.action = Action.STORE_TRUE
            argument.required = req
        elif req:
            raise PaperbushSyntaxError("cannot make a positional argument required")
        return argument

    if string[0] not in ":+=!":
        raise PaperbushSyntaxError(
            f"expected one of ':', '++', '!', or '=', found {string[0]!r} instead"
        )

    count, required, string = parse_togglables(string)
    argument.required = required or None
    if count:
        argument.action = Action.COUNT

    if not string:
        return argument

    if string[0] not in ":=":
        raise PaperbushSyntaxError(
            f"expected one of ':' or '=', found {string[0]!r} instead"
        )

    string, argument = parse_properties(string, argument, values)

    if string:
        argument.default = evaluate(string, values)

    return argument


def parse_name(arg: str) -> tuple[Argument, str]:

    pattern = arg
    full_name_allowed = True
    lh = stripped_len(arg, "-")
    name_charset = ascii_letters + digits + "-"

    if len(arg) == lh:
        raise PaperbushNameError("empty option name")

    if lh not in range(3):
        raise PaperbushNameError("invalid number of leading hyphens")

    short_name = name = ""
    if lh == 1:
        name_length = stripped_len(arg, name_charset)
        short_name, arg = bisect(arg, name_length)
        if full_name_allowed := arg.startswith("|"):
            arg = arg[1:]

    if full_name_allowed:
        name_length = stripped_len(arg, name_charset)
        name, arg = bisect(arg, name_length)

    if not (short_name or name):
        raise PaperbushNameError("empty option name")
    return Argument(name=name, short=short_name or None, pattern=pattern), arg


def parse_properties(
    string: str, argument: Argument, values: list[Any]
) -> tuple[str, Argument]:
    type_: str | None = None
    nargs: str | int | None = None
    choices: str | None = None

    while string:
        first, string = bisect(string, 1)
        if first == "=":
            break
        if None not in (type_, nargs, choices):
            raise PaperbushSyntaxError("too many properties")

        for sep in ":=":
            try:
                prop, string = bisect(string, sep)
            except ValueError:
                continue
            break
        else:
            prop = string

        if prop.isidentifier():
            type_ = prop
        elif (i := is_int(prop)) or prop in "?+*":
            nargs = int(prop) if i else prop
        else:
            choices = prop

        if prop == string:
            string = ""
            break

    if type_ is not None:
        argument.type_ = evaluate(type_, values)

    if nargs is not None:
        argument.nargs = nargs

    if choices is not None:
        argument.choices = evaluate(choices, values)

    return string, argument


def parse_togglables(string: str) -> tuple[bool, bool, str]:
    m = match(r"^(!)?(\+\+)?(?<!!)(!)?", string[:3])
    if m is None:
        return False, False, string
    return bool(m.group(2)), bool(m.group(1) or m.group(3)), string[len(m.group()) :]
