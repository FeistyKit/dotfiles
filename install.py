#!/usr/bin/env python3

import sys, argparse, os
from typing import Callable, TypeVar

try:
    import inquirer
except ImportError:
    print(
        "Module inquirer not found. Please install it via 'python3 -m pip install inquirer'",
        file=sys.stderr,
    )
    sys.exit(1)

colored = False
try:
    import termcolor

    colored = True
except ImportError:
    print("Module termcolor not found. Continuing without colour.")

actions: dict[str, Callable] = {}

T = TypeVar("T")


def anti_intersect(lhs: set[T], rhs: set[T]) -> tuple[set[T], set[T]]:
    return lhs - rhs, rhs - lhs


def validate():
    in_cur_dir: set[str] = set(
        filter(
            lambda x: not x.startswith(".") and x not in ["install.py", "README.md"],
            os.listdir(),
        )
    )
    bad = False
    prepared_folders: set[str] = set([x[0] for x in actions])
    not_prepared, not_exist = anti_intersect(in_cur_dir, prepared_folders)
    if len(not_prepared) == 1:
        msg = f'There is no automated installation for folder "{not_prepared[0]}"!'
        if colored:
            msg = termcolor.colored(
                msg,
                "red",
            )
        bad = True
        print(msg, file=sys.stderr)
    elif len(not_prepared) > 1:
        msg = "There are no automated installation methods for folders "
        first = True
        for folder_name in not_prepared:
            msg_raw = f'"{folder_name}"'
            if not first:
                msg += ", " + msg_raw
            else:
                msg += msg_raw
                first = False
        msg += "!"
        bad = True
        if colored:
            msg = termcolor.colored(msg, "red")
        print(msg, file=sys.stderr)

    if len(not_exist) == 1:
        msg = (
            f'Useless automated installation for non-existant folder "{not_exist[0]}"!'
        )
        if colored:
            msg = termcolor.colored(
                msg,
                "yellow",
            )
        bad = True
        print(msg, file=sys.stderr)
    elif len(not_exist) > 1:
        msg = "Useless automated installation methods for non-existant folders "
        first = True
        for folder_name in not_exist:
            msg_raw = f'"{folder_name}"'
            if not first:
                msg += ", " + msg_raw
            else:
                msg += msg_raw
                first = False
        msg += "!"
        bad = True
        if colored:
            msg = termcolor.colored(msg, "yellow")
        print(msg, file=sys.stderr)

    sys.exit(1 if bad else 0)


def install():
    pass


parser = argparse.ArgumentParser()
parser.add_argument("action", choices=["validate", "install"])
args = parser.parse_args()
if args.action == "validate":
    validate()
else:
    install()
