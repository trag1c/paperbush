## Paperbush

```py
Paperbush(pattern: str, *values: Any, infer_names: bool = True)
```
Creates a Paperbush parser; takes a string pattern
written in the [Paperbush custom language](dsl.md), an arbitrary number of
[reference values](dsl.md#value-references), and the `infer_names` flag which
specifies whether arguments with only long names should have the short names
inferred (`True` by default).

!!! warning
    Keeping `infer_names` true is going to cause name collisions between
    arguments which start with the same letter (for example
    `Paperbush("--fix --force")`).


## Paperbush.from_iterable
```py
Paperbush.from_iterable(
    iterable: Iterable[str],
    *values: Any,
    infer_names: bool = True
)
```
Creates a Paperbush parser from an iterable of patterns.
!!! example
    ```py
    a = Paperbush.from_iterable(["x:int", "y:(3, 4, 5)=4"])
    b = Paperbush("x:int y:(3, 4, 5)=4")
    assert a == b
    ```

## Paperbush.from_mapping
```py
Paperbush.from_mapping(
    mapping: Mapping[str, str],
    *values: Any,
    infer_names: bool = True
)
```
Creates a Paperbush parser from a mapping, where keys are patterns and values
are help messages.

=== "argparse"

    ```py
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument("x", type=int, help="the base")
    parser.add_argument("y", type=int, help="the exponent")
    ```

=== "Paperbush"

    ```py
    from paperbush import Paperbush

    parser = Paperbush.from_mapping({
        "x:int": "the base",
        "y:int": "the exponent"
    })
    ```

## Paperbush.parse

```py
Paperbush.parse(self, args: str | list[str]) -> argparse.Namespace
```

Parses command line arguments using the predefined pattern and returns an
[`argparse.Namespace`](https://docs.python.org/3/library/argparse.html#argparse.Namespace)
object. Accepts either a list of strings or a single string (which is split
with [`shlex.split`](https://docs.python.org/3/library/shlex.html#shlex.split)).


## Paperbush.parse_args

```py
Paperbush.parse_args(self) -> argparse.Namespace
```
Equivalent to `Paperbush.parse(sys.argv)`.