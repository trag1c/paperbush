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

## Required arguments
## Number of arguments
## Argument type
## Choices
## Default values
## Value references
## Mutually exclusive groups