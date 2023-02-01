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


## Argument type

Arguments can have their type specified by appending a colon followed by the
type name to the argument (`name:type`). The type name has to be a valid
variable name.

=== "argparse"

    ```py
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument("square", type=int)
    parser.add_argument("--verbosity", type=int)
    ```

=== "Paperbush"

    ```py
    from paperbush import Paperbush
    parser = Paperbush("square:int --verbosity:int")
    ```

By setting the default type (`str`) you can get the original behavior of
optional arguments in `argparse`:

=== "argparse"

    ```py
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument("--verbosity")
    ```

=== "Paperbush"

    ```py
    from paperbush import Paperbush
    parser = Paperbush("--verbosity:str")
    ```


## Required arguments

Arguments can be made mandatory by putting a `!` after their name.

=== "argparse"

    ```py
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument("-o", "--output", required=True)
    ```

=== "Paperbush"

    ```py
    from paperbush import Paperbush
    parser = Paperbush("--output!")
    ```


## Number of arguments

The number of arguments (nargs) is specified the same way as the argument
type, by following our argument with a colon and then either an integer,
`?`, `*`, or `+`:

=== "argparse"

    ```py
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument("-f", "--foo", nargs=3)
    parser.add_argument("-b", "--bar", nargs="*")
    ```

=== "Paperbush"

    ```py
    from paperbush import Paperbush
    parser = Paperbush("--foo:3 --bar:*")
    ```


## Choices

You can restrict what values an argument can accept by specifying `choices`.
They're added the same way as `type` or `nargs`, by adding an iterable
after a colon:

=== "argparse"

    ```py
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument("-v", "--verbosity", type=int, choices=[0, 1, 2])
    ```

=== "Paperbush"

    ```py
    from paperbush import Paperbush
    parser = Paperbush("--verbosity:int:[0, 1, 2]")
    ```

!!! note
    The order doesn't matter, `--verbosity:[0, 1, 2]:int` is as valid as
    `--verbosity:int:[0, 1, 2]`.


## Counting

Arguments can have the "count" action set by following the argument name
with `++`. Paperbush also sets the default to `0` for convenience:

=== "argparse"

    ```py
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument("-v", "--verbose", action="count", default=0)
    ```

=== "Paperbush"

    ```py
    from paperbush import Paperbush
    parser = Paperbush("--verbose++")
    ```

!!! note
    Just like with the "colon options", there's no difference between
    `--verbose!++` and `--verbose++!`.


## Default values

Default argument values are set at their very end, preceded by the `=` sign:

=== "argparse"

    ```py
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument("-b", "--base", type=float, required=True)
    parser.add_argument("-e", "--exponent", type=float, default=2.0)
    ```

=== "Paperbush"

    ```py
    from paperbush import Paperbush
    parser = Paperbush("--base!:float --exponent:float=2.0")
    ```


## Value references
## Mutually exclusive groups