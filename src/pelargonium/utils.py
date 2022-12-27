def bisect(string: str, index: int) -> tuple[str, str]:
    return string[:index], string[index:]


def stripped_len(string: str, chars: str) -> int:
    return len(string) - len(string.lstrip(chars))
