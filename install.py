#!/usr/bin/env python3

import sys, argparse, os
from typing import Callable, TypeVar, Optional

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

HOME = (
    os.environ.get("XDG_CONFIG_HOME")
    if os.environ.get("XDG_CONFIG_HOME") is not None
    else "/home/" + os.environ["USER"]
)

HERE = os.getcwd() + "/"


def backup(path: str):
    path = os.path.normpath(path)
    if os.path.exists(path):
        if os.path.exists(path + ".backup"):
            counter = 1
            while os.path.exists(path + ".backup-" + str(counter)):
                counter += 1
            os.rename(path, path + ".backup-" + str(counter))
        else:
            os.rename(path, path + ".backup")


def install_alacritty():
    backup(HOME + "/.config/alacritty/")
    os.symlink(HERE + "./alacritty", HOME + "/.config/alacritty")


def install_qtile():
    backup(HOME + "/.config/qtile/")
    os.symlink(HERE + "./qtile", HOME + "/.config/qtile")


def install_fish():
    backup(HOME + "/.config/fish/")
    os.symlink(HERE + "./fish", HOME + "/.config/fish")


def install_dunst():
    backup(HOME + "/.config/dunst/")
    os.symlink(HERE + "./dunst", HOME + "/.config/dunst")


def install_kitty():
    backup(HOME + "/.config/kitty//")
    os.symlink(HERE + "./kitty", HOME + "/.config/kitty")


def install_doom_emacs():
    qs = [
        inquirer.List(
            "doom_path",
            message="Where to install Doom Emacs configuration?",
            choices=["~/.doom.d", "~/.config/doom"],
            default="~/.config/doom",
        ),
    ]
    res: str = inquirer.prompt(qs)["doom_path"]
    backup(HOME + "/.emacs.d")
    os.system(
        f"""git clone --depth 1 https://github.com/hlissner/doom-emacs ~/.emacs.d
{HOME}/.emacs.d/bin/doom install"""
    )
    backup(res)
    os.symlink(HERE + "./doom-emacs", os.path.abspath(res))
    os.system(f"{HOME}/.emacs.d/bin/doom sync")


def install_dmscripts():
    backup(HOME + "/.config/dmscripts")
    os.symlink(HERE + "./dmscripts", HOME + "/.config/dmscripts")


def install_fonts():
    backup(HOME + "/.fonts")
    os.symlink(HERE + "./fonts", HOME + "/.fonts")
    os.system("sudo fc-cache -fv")


actions: dict[str, Callable] = {
    "alacritty": install_alacritty,
    "qtile": install_qtile,
    "fish": install_fish,
    "dunst": install_dunst,
    "kitty": install_kitty,
    "doom-emacs": install_doom_emacs,
    "dmscripts": install_dmscripts,
    "fonts": install_fonts,
}

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
    prepared_folders: set[str] = set([x for x in actions])
    not_prepared, not_exist = anti_intersect(in_cur_dir, prepared_folders)
    if len(not_prepared) == 1:
        msg = (
            f'There is no automated installation for folder "{list(not_prepared)[0]}"!'
        )
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
    options = [x for x in actions]
    questions = [
        inquirer.Checkbox(
            "to_install",
            choices=options.copy(),
            default=options.copy(),
            message="What modules would you like to install? (This will back up the previous configurations if they exist)",
        ),
    ]
    conf = inquirer.prompt(questions)
    for folder in conf["to_install"]:
        if os.path.isdir(folder):
            actions[folder]()
            print(f"Installed {folder}!")


parser = argparse.ArgumentParser()
parser.add_argument("action", choices=["validate", "install"], default="install")
args = parser.parse_args()
if args.action == "validate":
    validate()
else:
    install()
