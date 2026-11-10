"""Small helper functions used by every feature file."""


def ask(prompt):
    return input(prompt).strip()


def line():
    print("-" * 50)


def to_int(text):
    """'12' -> 12, anything else -> None."""
    return int(text) if text.isdigit() else None
