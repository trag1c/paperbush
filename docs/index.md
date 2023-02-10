# Paperbush 🌿

Paperbush is a dead easy argument parsing tool that simplifies the process of
creating command-line argument parsers in Python. With Paperbush, you can
define your parser in just a single line of code using a custom built-in
language, which is then translated directly into the built-in `argparse` module
equivalent. This means that in most cases, moving to Paperbush is just a matter
of changing the parser definition, as `Paperbush.parse_args()` returns an
`argparse.Namespace` object.

## Installation
Paperbush is available on PyPI and can be installed with `pip`, or any other
Python package manager:
```sh
$ pip install paperbush
```
(Some systems may require you to use `pip3`, `python -m pip`, or `py -m pip`)

## [Examples](examples.md)

## Features
- short name inferrence
- mutually exclusive groups
- choices and the count action
- default values
- required arguments
- type conversion

## Known Limitations
Currently Paperbush has no support for:
- aliases
- help messages
- subparsers

## License
Paperbush is licensed under the MIT License.
