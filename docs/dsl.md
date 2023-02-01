# Language Reference

This page describes how to use the Paperbush custom language. Considering the
library is built on top of `argparse`, this page will contain many comparions
to that library.

## Positional arguments
Positional arguments are defined simply by specifying their names with no
leading hyphens.

=== "argparse"

    ```py
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument("echo")
    ```

=== "Paperbush"

    ```py
    from paperbush import Paperbush
    parser = Paperbush("echo")
    ```

## Optional arguments

Optional arguments are defined with leading hyphens:

- `-n` for the short name
- `--name` for the long name

If you wish to provide both names, they have to be separated with a `|`.

However, Paperbush does short name inference by default, which means that
you only need to specify the long name if the short name is the first letter
of the long name.

Also, bare optional arguments (without [type specification](#argument-type) or
[default values](#default-values) for example) have their action set to
`store_true`. This is the only case where this behavior occurs.

=== "argparse"

    ```py
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument("-v", "--verbose", action="store_true")
    ```

=== "Paperbush"

    ```py
    from paperbush import Paperbush
    parser = Paperbush("-v|--verbose")
    ```

=== "Paperbush (short name inference)"

    ```py
    from paperbush import Paperbush
    parser = Paperbush("--verbose")
    ```

If you don't want Paperbush to infer those names, define the parser with
the `infer_names` parameter disabled.

=== "argparse"

    ```py
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument("--verbose", action="store_true")
    ```

=== "Paperbush"

    ```py
    from paperbush import Paperbush
    parser = Paperbush("--verbose", infer_names=False)
    ```


## Required arguments
## Number of arguments
## Argument type
## Choices
## Default values
## Value references
## Mutually exclusive groups