"""Write one roast line about my own AI agent to the entry file.

Stdlib only. Deterministic: the same line every run.
"""

import os

ROAST = (
    "My agent apologizes for the mistake, explains it in detail, "
    "then makes the exact same mistake \u2014 with better formatting."
)

MAX_CHARS = 140


def resolve_output_path():
    """Pick the destination, preferring the env vars the harness sets."""
    for var in ("ENTRY_OUTPUT", "OUTPUT_DIR", "MAKEFUN_OUTPUT_DIR"):
        value = os.environ.get(var)
        if value:
            if var == "ENTRY_OUTPUT":
                return value
            return os.path.join(value, "entry.txt")
    if os.path.isdir("/output"):
        return "/output/entry.txt"
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(here, "entry.txt")


def validate(line):
    """The gate: UTF-8, 1-140 characters, not blank, single line."""
    if not isinstance(line, str):
        raise ValueError("roast line must be text")
    if not line.strip():
        raise ValueError("roast line must not be blank")
    if line != line.strip():
        raise ValueError("roast line must not start or end with whitespace")
    if "\n" in line or "\r" in line:
        raise ValueError("roast line must be a single line")
    if len(line) > MAX_CHARS:
        raise ValueError(
            "roast line is %d characters, over the 140 limit" % len(line)
        )
    line.encode("utf-8")
    return line


def main():
    line = validate(ROAST)
    target = resolve_output_path()
    parent = os.path.dirname(target)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(target, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(line + "\n")
    os.chmod(target, 0o644)
    # Read back and verify: the file must hold exactly our line + newline.
    with open(target, "r", encoding="utf-8", newline="") as handle:
        written = handle.read()
    if written != line + "\n":
        raise ValueError("verification failed: entry file content mismatch")
    print("wrote %d chars to %s" % (len(line), target))


if __name__ == "__main__":
    main()
