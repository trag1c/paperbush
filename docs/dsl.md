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
you only need to specify the long name when the short name would be the first
letter of the long name.

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
They're added the same way as `type` or `nargs`, by adding a container
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

Defining a parser using a single string has one major issue: working with
variables. Since it's all a string, passing the variable name would need
Paperbush to manually evaluate it when parsing, which would require the user
to pass `globals()`, which doesn't look the best. Also evaluating the variable
on the spot (e.g. using an f-string) doesn't work for most types and it quite often
comes with copying data.

Therefore Paperbush uses value references, which let you refer to variables
without using them directly in the string, which is both a speed and memory
improvement (even though they're not necessarily relevant for an argument
parser).

Value references are marked with `$n`. All of these parser definitions are equivalent:

=== "argparse"

    ```py
    from argparse import ArgumentParser
    options = list(range(10_000))
    parser = ArgumentParser()
    parser.add_argument("-o", "--option", choices=options)
    ```

=== "Paperbush"

    ```py
    from paperbush import Paperbush
    options = list(range(10_000))
    parser = Paperbush(f"--option:{options}")
    # we're lucky that str(options) is valid syntax
    # this takes ~25 seconds
    ```

=== "Paperbush (with value references)"

    ```py
    from paperbush import Paperbush
    options = list(range(10_000))
    parser = Paperbush("--option:$0", options)
    # this takes 0.002s
    # (~14K times faster for a very extreme case)
    ```

*(the above runtimes were measured on a MacBook Air M1)*

Another example of using value references:

=== "Paperbush"

    ```py
    from paperbush import Paperbush
    parser = Paperbush("--verbose:int:1:(0, 1, 2, 3)=0")
    ```

=== "Paperbush (with value references)"

    ```py
    from paperbush import Paperbush
    parser = Paperbush("--verbose:int:1:$0=$1", (0, 1, 2, 3), 0)
    ```

!!! note
    Because of implementation details, value references currently can only be
    used for choices and default values.


## Mutually exclusive groups

Mutually exclusive groups are made by XORing 2 or more arguments:

=== "argparse"

    ```py
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument("x", type=int)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-v", "--verbose", action="store_true")
    group.add_argument("-s", "--silent", action="store_true")
    ```

=== "Paperbush"

    ```py
    from paperbush import Paperbush
    parser = Paperbush("x:int --verbose ^ --silent")
    ```

