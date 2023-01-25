Paperbush's public API consists of just one class with 2 methods.

## Paperbush

```py
Paperbush(pattern: str, *values: Any, infer_names: bool = True)
```

## Paperbush.parse

```py
Paperbush.parse(args: str | list[str]) -> argparse.Namespace
```

## Paperbush.parse_args

```py
Paperbush.parse_args() -> argparse.Namespace
```
Equivalent to `Paperbush.parse(sys.argv)`.