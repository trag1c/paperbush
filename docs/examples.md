# Examples

The following page shows a few examples comparing Paperbush to `argparse`.

=== "argparse"

    ```py
    from argparse import ArgumentParser

    parser = ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    parser.add_argument("x", type=int)
    parser.add_argument("y", type=int, default=0)
    group.add_argument("-v", "--verbose", action="count", default=0)
    group.add_argument("-q", "--quiet", action="store_true")
    ```

=== "Paperbush"

    ```py
    from paperbush import Paperbush

    parser = Paperbush("x:int y:int=0 --verbose++ ^ --quiet")
    ```

---

=== "argparse"

    ```py
    from argparse import ArgumentParser

    UNSET = object()
    parser = ArgumentParser()
    parser.add_argument("string", nargs="?", default=UNSET)
    parser.add_argument(
        "-d",
        "--depth",
        type=int,
        choices=(3, 4, 8, 24),
        default=4
    )
    parser.add_argument("-c", "--clean", action="store_true")
    parser.add_argument("-t", "--test", action="store_true")
    ```

=== "Paperbush"

    ```py
    from paperbush import Paperbush

    UNSET = object()
    parser = Paperbush(
        "string:?=$0 --depth:int:(3, 4, 8, 24)=4 --clean --test",
        UNSET
    )
    ```