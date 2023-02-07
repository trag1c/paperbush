# Examples

The following page shows a few examples comparing Paperbush to `argparse`.

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

---

=== "argparse"

    ```py
    from argparse import ArgumentParser

    parser = ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    parser.add_argument("x", type=int)
    parser.add_argument("y", type=int)
    group.add_argument("-v", "--verbose", action="count", default=0)
    group.add_argument("-q", "--quiet", action="store_true")
    ```

=== "Paperbush"

    ```py
    from paperbush import Paperbush

    parser = Paperbush("x:int y:int --verbose++ ^ --quiet")
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

---

=== "argparse"

    ```py
    from argparse import ArgumentParser

    parser = ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-m")
    group.add_argument("-c")
    parser.add_argument("-O", action="count")
    parser.add_argument("-q", action="store_true")
    ```

=== "Paperbush"

    ```py
    from paperbush import Paperbush

    parser = Paperbush("-m:str ^ -c:str -O++ -q")
    ```

---

=== "argparse"

    ```py
    import sys
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument("-i", "--inputs", nargs="*")
    parser.add_argument("-s", "--smart", action="store_true")
    parser.add_argument("-o", "--output", default=sys.stdout)
    ```

=== "Paperbush"

    ```py
    import sys
    from paperbush import Paperbush

    parser = Paperbush("--inputs:* --smart --output=$0", sys.stdout)
    ```
