# Paperbush 🌿

Paperbush is a dead easy argument parsing tool that simplifies the process of creating command-line argument parsers in Python. With Paperbush, you can define your parser in just a single line of code using a custom built-in language, which is then translated directly into the built-in `argparse` module equivalent. This means that moving to Paperbush is just a matter of changing the parser definition, as `Paperbush.parse_args()` returns an `argparse.Namespace` object.

## Features
- short name inferrence
- mutually exclusive groups
- choices
- default values
- required args
- type conversion

## Known Limitations
- no help messages
- no subparser support

## Examples
```py
from argparse import ArgumentParser

parser = ArgumentParser()
group = parser.add_mutually_exclusive_group()
parser.add_argument("x", type=int)
parser.add_argument("y", type=int)
group.add_argument("-v", "--verbosity", action="count", default=0)
group.add_argument("-q", "--quiet", action="count", default=0)



from paperbush import Paperbush

parser = Paperbush("x:int y:int --verbosity++ ^ --quiet++")
```
```py
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("string")
parser.add_argument("-v", "--verbosity", action="count", default=0)



from paperbush import Paperbush

parser = Paperbush("string --verbosity++")
```

## License
Paperbush is licensed under the MIT License.
