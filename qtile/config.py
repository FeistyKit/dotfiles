# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import os, subprocess, sys

from typing import List  # noqa: F401

from libqtile import bar, layout, widget
from libqtile.config import Click, Drag, Group, EzKey as Key, Match, Screen
from libqtile.lazy import lazy
from libqtile import hook


# so I don't have to change the command many different times
def find_dmenu_command() -> str:
    with open(userpath + "/.config/dmscripts/config") as f:
        buf = f.read()
        for line in buf.splitlines():
            if line.startswith("DMENU="):
                return line.replace("DMENU=", "").replace('"', "")
    sys.stderr.write("Could not find dmenu command!")
    os.system('notify-send "Could not find dmenu command!"')
    return "dmenu_run"


userpath = os.environ["HOME"]
mod = "mod4"
terminal = "alacritty"
dmenu_command = find_dmenu_command()
editor = "emacsclient -c -a 'emacs' "


@hook.subscribe.startup_once
def autostart():
    scr = os.path.expanduser(userpath + "/.config/qtile/autostart.sh")
    subprocess.run([scr])


# Called whenever a new window is opened.
# https://github.com/qtile/qtile/discussions/2319#discussioncomment-536854
@hook.subscribe.client_new
def assign_app_group(client):
    d = {}
    d["COM"] = [
        "discord",
    ]
    d["GFX"] = ["vlc", "steam"]
    for k in d.keys():
        if k not in group_names:
            os.system(
                f'notify-send "Group \\"{k}\\" unknown! Note: located in assign_app_group()"'
            )

    wm_class = client.window.get_wm_class()[0]

    for i in range(len(d)):
        if wm_class in list(d.values())[i]:
            group = list(d.keys())[i]
            client.togroup(group)
            client.group.cmd_toscreen(toggle=False)


keys = [
    # https://github.com/tsoding/boomer
    Key("M-b", lazy.spawn(userpath + "/bin/boomer")),
    # https://github.com/bk138/gromit-mpx
    Key("M-a", lazy.spawn("gromit-mpx --toggle")),
    Key(
        "M-S-<space>",
        lazy.window.toggle_floating(),
        desc="Toggle floating for a window",
    ),
    Key("M-q", lazy.prev_screen(), desc="Move focus to previous screen"),
    Key("M-w", lazy.next_screen(), desc="Move focus to next screen"),
    Key(
        "M-S-v",
        lazy.spawn(editor + f"{userpath}/.config/qtile/config.py"),
        desc="Quickly change config",
    ),
    Key("M-v", lazy.spawn("diodon"), desc="Spawn clipboard manager."),
    # ---------------------------------------------
    # Switch between windows
    Key("M-h", lazy.layout.left(), desc="Move focus to left"),
    Key("M-l", lazy.layout.right(), desc="Move focus to right"),
    Key("M-j", lazy.layout.down(), desc="Move focus down"),
    Key("M-k", lazy.layout.up(), desc="Move focus up"),
    Key("M-<space>", lazy.layout.next(), desc="Move window focus to other window"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key("M-C-h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key("M-C-l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key("M-C-j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key("M-C-k", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key("M-S-h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key("M-S-l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key("M-S-j", lazy.layout.grow_down(), desc="Grow window down"),
    Key("M-S-k", lazy.layout.grow_up(), desc="Grow window up"),
    Key("M-n", lazy.layout.normalize(), desc="Reset all window sizes"),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        "M-C-<Return>",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key("M-<Return>", lazy.spawn(terminal), desc="Launch terminal"),
    Key("M-S-<Return>", lazy.spawn("rofi -show run"), desc="Run an application"),
    Key(
        "M-C-<Return>",
        lazy.spawn("rofi -show drun"),
        desc="Run an application from .desktop files",
    ),
    # Toggle between different layouts as defined below
    Key("M-<Tab>", lazy.next_layout(), desc="Toggle between layouts"),
    Key("M-S-c", lazy.window.kill(), desc="Kill focused window"),
    Key("M-S-r", lazy.restart(), desc="Restart Qtile"),
    Key("M-C-q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key("M-r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
]

group_names = ["I", "II", "III", "IV", "COM", "DEV", "SYS", "GFX"]
groups = [Group(x) for x in group_names]

for num, group in enumerate(groups):
    keys.extend(
        [
            # mod1 + letter of group = switch to group
            Key(
                "M-" + str(num + 1),
                lazy.group[group.name].toscreen(toggle=True),
                desc="Switch to group {}".format(group.name),
            ),
            # mod1 + shift + letter of group = switch to & move focused window to group
            Key(
                "M-S-" + str(num + 1),
                lazy.window.togroup(group.name, switch_group=True),
                desc="Switch to & move focused window to group {}".format(group.name),
            ),
            # Or, use below if you prefer not to switch to that group.
            # # mod1 + shift + letter of group = move focused window to group
            Key(
                "M-C-S-" + str(num + 1),
                lazy.window.togroup(group.name),
                desc="move focused window to group {}".format(group.name),
            ),
        ]
    )

# https://gitlab.com/dwt1/dotfiles/-/blob/master/.config/qtile/config.py#L234
layout_theme = {
    "border_width": 0,
    "margin": 8,
    "border_focus": "fabd2f",
    "border_normal": "bdae93",
}
layout_theme_clean = layout_theme.copy()
layout_theme_clean["margin"] = 0


layouts = [
    layout.Columns(**layout_theme),
    layout.Max(**layout_theme),
    layout.Columns(**layout_theme_clean),
    # layout.Stack(**layout_theme),
    # layout.Bsp(**layout_theme),
    # layout.Matrix(**layout_theme),
    # layout.MonadTall(**layout_theme),
    # layout.MonadWide(**layout_theme),
    # layout.RatioTile(**layout_theme),
    # layout.Tile(**layout_theme),
    # layout.TreeTab(**layout_theme),
    # layout.VerticalTile(**layout_theme),
    # layout.Zoomy(**layout_theme**layout_theme),
]


class Colours:
    # colours from https://github.com/catppuccin/catppuccin
    BLACK_2 = "#1E1E2E"  # Black 2
    BLACK_4 = "#575268"  # Black 4
    GRAY_0 = "#6E6C7E"  # Gray 0
    GRAY_2 = "#C3BAC6"  # Gray 2
    BLUE = "#96CDFB"  # Blue
    MAROON = "#E8A2AF"  # Maroon


scale = None

try:
    import socket

    if socket.gethostname() == "helium":
        scale = 16
    else:
        scale = 12
except:
    scale = 12

widget_defaults = dict(
    font="mononoki Nerd Font",
    fontsize=int(12 * scale / 12),
    padding=int(3 * scale / 12),
    background=Colours.BLACK_2,
    foreground=Colours.GRAY_2,
)
extension_defaults = widget_defaults.copy()


def default_sep():
    return widget.TextBox(
        text=" | ",
        linewidth=int(0 * scale / 12),
        padding=int(6 * scale / 12),
        foreground=Colours.BLACK_4,
        background=Colours.BLACK_2,
    )


def mk_widgets():
    to_ret = [
        widget.GroupBox(
            margin_y=int(3 * scale / 12),
            margin_x=int(0 * scale / 12),
            padding_y=int(5 * scale / 12),
            padding_x=int(3 * scale / 12),
            borderwidth=int(3 * scale / 12),
            active=Colours.MAROON,
            inactive=Colours.BLUE,
            rounded=False,
            highlight_color=Colours.GRAY_0,
            highlight_method="line",
            foreground=Colours.GRAY_0,
            background=Colours.BLACK_2,
        ),
        default_sep(),
        widget.WindowName(
            padding=int(0 * scale / 12),
            foreground=Colours.GRAY_2,
            background=Colours.BLACK_2,
        ),
        widget.Sep(
            linewidth=int(0 * scale / 12),
            padding=int(70 * scale / 12),
            foreground=Colours.GRAY_0,
            background=Colours.BLACK_2,
        ),
        widget.CPU(
            format="CPU {load_percent}%",
        ),
        default_sep(),
        widget.Memory(
            format="MEM {MemPercent: .0f}%",
        ),
        default_sep(),
        widget.Volume(
            fmt="VOL {}",
        ),
        default_sep(),
        widget.Net(
            interface="wlp2s0",
            format="REC {down} TRA {up}",  # https://gitlab.com/dwt1/dotfiles/-/blob/master/.config/qtile/config.py#L374
        ),
        default_sep(),
        widget.CheckUpdates(
            update_interval=1800,
            distro="Arch_checkupdates",
            display_format="PAC {updates}",
            no_update_string="UP TO DATE",
            colour_no_updates=Colours.GRAY_2,
            colour_have_updates=Colours.GRAY_2,
        ),
        default_sep(),
        # widget.MOC(),
        widget.Clock(
            format="NOW %Y-%m-%d %a %I:%M %p",
        ),
    ]
    # whether or not to include the battery widget
    # https://stackoverflow.com/a/41988627
    try:
        import psutil  # type: ignore

        bat = psutil.sensors_battery()
        if bat is not None and bat.secsleft != -1:
            battery_index = 7  # we want it to be right before the volume widget
            to_ret.insert(
                battery_index,
                widget.Battery(
                    foreground=Colours.GRAY_2,
                    background=Colours.BLACK_2,
                    format="BAT {char} {percent:2.0%}",
                ),
            )
            to_ret.insert(battery_index, default_sep())
    except ImportError:
        os.system('notify-send "Could not use psutil library to detect battery!"')
    return to_ret


# Find the index of the volume widget
def find_volume() -> int:
    # For some reason this does not work: I will do it later today
    # for i, wid in enumerate(widgets):
    #     if isinstance(wid, widget.Volume):
    #         return i
    # yield ValueError
    return -1


# -- CODE STOLEN FROM https://github.com/qtile/qtile/wiki/screens -- #
from Xlib import display as xdisplay  # type: ignore


def get_num_monitors():
    num_monitors = 0
    try:
        display = xdisplay.Display()
        screen = display.screen()
        resources = screen.root.xrandr_get_screen_resources()

        for output in resources.outputs:
            monitor = display.xrandr_get_output_info(output, resources.config_timestamp)
            preferred = False
            if hasattr(monitor, "preferred"):
                preferred = monitor.preferred
            elif hasattr(monitor, "num_preferred"):
                preferred = monitor.num_preferred
            if preferred:
                num_monitors += 1
    except Exception:
        # always setup at least one monitor
        return 1
    else:
        return num_monitors


num_monitors = get_num_monitors()
# -- END STEAL -- #


def make_screen():
    return Screen(
        top=bar.Bar(mk_widgets(), int(24 * scale / 12), opacity=0.90, margin=4),
    )


screens = []
for _ in range(num_monitors):
    screens.append(make_screen())


# Drag floating layouts.
mouse = [
    Drag(
        [mod],
        "Button1",
        lazy.window.set_position_floating(),
        start=lazy.window.get_position(),
    ),
    Drag(
        [mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()
    ),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
