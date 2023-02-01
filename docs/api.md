Paperbush's public API consists of just one class with 2 methods.

## Paperbush

```py
Paperbush(pattern: str, *values: Any, infer_names: bool = True)
```
Creates a Paperbush parser; takes a string pattern written in the [Paperbush custom language](dsl.md), an arbitrary number of [reference values](dsl.md#value-references), and the `infer_names` flag which specifies whether arguments with only long names should have the short names inferred (`True` by default).

!!! warning
    Keeping `infer_names` true is going to cause name collisions between arguments which start with the same letter (for example `Paperbush("--fix --force")`).

## Paperbush.parse

```py
Paperbush.parse(args: str | list[str]) -> argparse.Namespace
```

Parses command line arguments using the predefined pattern and returns an `argparse.Namespace` object. Accepts either a list of strings or a single string which is split with [`shlex.split`](https://docs.python.org/3/library/shlex.html#shlex.split)).


## Paperbush.parse_args

```py
Paperbush.parse_args() -> argparse.Namespace
```
Equivalent to `Paperbush.parse(sys.argv)`.