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
from libqtile.config import Click, Drag, Group, EzKey as Key, Match, Screen, KeyChord
from libqtile.lazy import lazy
from libqtile import hook


# so I don't have to change the command many different times
def find_dmenu_command() -> str:
    with open(userpath + "/.config/dmscripts/config") as f:
        buf = f.read()
        for line in buf.splitlines():
            if line.startswith("DMENU="):
                return line.replace("DMENU=", "").replace("\"", "")
    sys.stderr.write("Could not find dmenu command!")
    os.system("notify-send \"Could not find dmenu command!\"")
    return "dmenu_run"

userpath = os.environ['HOME']
mod = "mod4"
terminal = "alacritty"
dmenu_command = find_dmenu_command()
editor = "emacsclient -c -a 'emacs' "

@hook.subscribe.startup_once
def autostart():
    scr = os.path.expanduser(userpath + '/.config/qtile/autostart.sh')
    subprocess.run([scr])

keys = [

    #dmscripts
    KeyChord([mod], "d", [
        Key("c", lazy.spawn("dm-confedit")),
        Key("k", lazy.spawn("dm-kill")),
        Key("h", lazy.spawn("dm-hub")),
        Key("u", lazy.spawn("dm-usbmount")),
        Key("r", lazy.spawn("dm-record")),
        Key("s", lazy.spawn("dm-maim"))
        ]),

    # Mocp things!
    KeyChord([mod], "p", [
        Key("<space>", lazy.spawn("mocp --toggle-pause"), desc="Toggle pause/play in mocp"),
        Key("<Right>", lazy.spawn("mocp --next"), desc="Go to the next song in mocp"),
        Key("<Left>", lazy.spawn("mocp --previous"), desc="Go to the previous song in mocp"),
        Key("p", lazy.spawn(userpath + "/.scripts/dm-mocp"), desc="Get songs to play"),
    ]),

    # Programs!
    # Much of this was taken from https://gitlab.com/dwt1/dotfiles/-/blob/master/.config/qtile/config.py
    KeyChord([mod], "e", [
        Key("e", lazy.spawn("emacsclient -c -a 'emacs'"), desc="Open emacs"),
        Key("m", lazy.spawn("emacsclient -c -a 'emacs' --eval '(mu4e)'"), desc="Launch mail client inside of emacs"),
        Key("d", lazy.spawn("discord"), desc="Open discord"),
        Key("f", lazy.spawn("firefox"), desc="Open firefox")
    ]),

    Key("M-S-<space>", lazy.window.toggle_floating(), desc="Toggle floating for a window"),

    Key("M-q", lazy.prev_screen(), desc="Move focus to previous screen"),
    Key("M-w", lazy.next_screen(), desc="Move focus to next screen"),

    Key("M-S-v", lazy.spawn(editor + f"{userpath}/.config/qtile/config.py"), desc="Quickly change config"),

    Key("M-v", lazy.spawn("diodon"), desc="Spawn clipboard manager."),

    # ---------------------------------------------

    # Switch between windows
    Key("M-h", lazy.layout.left(), desc="Move focus to left"),
    Key("M-l", lazy.layout.right(), desc="Move focus to right"),
    Key("M-j", lazy.layout.down(), desc="Move focus down"),
    Key("M-k", lazy.layout.up(), desc="Move focus up"),
    Key("M-<space>", lazy.layout.next(),
        desc="Move window focus to other window"),

    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key("M-C-h", lazy.layout.shuffle_left(),
        desc="Move window to the left"),
    Key("M-C-l", lazy.layout.shuffle_right(),
        desc="Move window to the right"),
    Key("M-C-j", lazy.layout.shuffle_down(),
        desc="Move window down"),
    Key("M-C-k", lazy.layout.shuffle_up(), desc="Move window up"),

    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key("M-S-h", lazy.layout.grow_left(),
        desc="Grow window to the left"),
    Key("M-S-l", lazy.layout.grow_right(),
        desc="Grow window to the right"),
    Key("M-S-j", lazy.layout.grow_down(),
        desc="Grow window down"),
    Key("M-S-k", lazy.layout.grow_up(), desc="Grow window up"),
    Key("M-n", lazy.layout.normalize(), desc="Reset all window sizes"),

    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key("M-C-<Return>", lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack"),
    Key("M-<Return>", lazy.spawn(terminal), desc="Launch terminal"),
    Key("M-S-<Return>", lazy.spawn(dmenu_command), desc="Dmenu"),

    # Toggle between different layouts as defined below
    Key("M-<Tab>", lazy.next_layout(), desc="Toggle between layouts"),
    Key("M-S-c", lazy.window.kill(), desc="Kill focused window"),

    Key("M-S-r", lazy.restart(), desc="Restart Qtile"),
    Key("M-C-q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key("M-r", lazy.spawncmd(),
        desc="Spawn a command using a prompt widget"),
]

groups = [Group(i) for i in "123456789"]

for num, group in enumerate(groups):
    keys.extend([
        # mod1 + letter of group = switch to group
        Key("M-" + str(num + 1), lazy.group[group.name].toscreen(toggle=True),
            desc="Switch to group {}".format(group.name)),

        # mod1 + shift + letter of group = switch to & move focused window to group
        Key("M-S-" + str(num + 1), lazy.window.togroup(group.name, switch_group=True),
            desc="Switch to & move focused window to group {}".format(group.name)),
        # Or, use below if you prefer not to switch to that group.
        # # mod1 + shift + letter of group = move focused window to group
        Key("M-C-S-" + str(num + 1), lazy.window.togroup(group.name),
            desc="move focused window to group {}".format(group.name)),
    ])

# https://gitlab.com/dwt1/dotfiles/-/blob/master/.config/qtile/config.py#L234
layout_theme = {"border_width": 2,
                "margin": 8,
                "border_focus": "fabd2f",
                "border_normal": "bdae93"
                }
layout_theme_clean = layout_theme.copy()
layout_theme_clean['margin'] = 0




layouts = [
    layout.Columns(**layout_theme_clean),
    layout.Max(**layout_theme),
    layout.Columns(**layout_theme)
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
    # colours stolen from https://github.com/chriskempson/base16-vim/blob/master/colors/base16-gruvbox-dark-hard.vim
    # I apologize for my naming, I am bad with colours
    DARKEST="#1d2021"
    DARK_BROWN="#3c3836"
    MED_DARK_BROWN="#504945"
    MED_BROWN="#665c54"
    DARKEST_TAN="#bdae93"
    MED_DARK_TAN="#d5c4a1"
    MED_LIGHT_TAN="#ebdbb2"
    NEAR_WHITE_TAN="#fbf1c7"
    RED="#fb4934"
    LIGHT_ORANGE="#fe8019"
    YELLOW="#fabd2f"
    GREEN="#b8bb26"
    TURQUOISE="#8ec07c"
    BLUE="#83a598"
    PINK="#d3869b"
    REDDIT_ORANGE="#d65d0e"

widget_defaults = dict(
    font='mononoki Nerd Font',
    fontsize=12,
    padding=3,
    background=Colours.DARKEST,
    foreground=Colours.DARKEST_TAN
)
extension_defaults = widget_defaults.copy()

def default_sep():
    return widget.TextBox(
        text=" | ",
        linewidth=0,
        padding=6,
        foreground=Colours.MED_DARK_BROWN,
        background=Colours.DARKEST
    )

def mk_widgets():
    to_ret = [
                widget.GroupBox(
                    margin_y = 3,
                    margin_x = 0,
                    padding_y = 5,
                    padding_x = 3,
                    borderwidth = 3,
                    active=Colours.PINK,
                    inactive=Colours.BLUE,
                    rounded=False,
                    highlight_color=Colours.MED_BROWN,
                    highlight_method="line",
                    foreground=Colours.MED_BROWN,
                    background=Colours.DARKEST
                ),
                default_sep(),
                widget.WindowName(
                    padding=0,
                    foreground=Colours.DARKEST_TAN,
                    background=Colours.DARKEST,
                ),
                widget.Sep(
                    linewidth=0,
                    padding=70,
                    foreground=Colours.MED_BROWN,
                    background=Colours.DARKEST
                ),
                widget.CPU(format="CPU {load_percent}%",
                ),
                default_sep(),
                widget.Memory(format="MEM {MemPercent: .0f}%",
                ),
                default_sep(),
                widget.Volume(fmt="VOL {}",
                ),
                default_sep(),
                widget.Net(
                    interface= 'wlp2s0',
                    format='REC {down} TRA {up}', # https://gitlab.com/dwt1/dotfiles/-/blob/master/.config/qtile/config.py#L374
                    ),
                default_sep(),
                widget.CheckUpdates(
                    update_interval = 1800,
                    distro = "Arch_checkupdates",
                    display_format = "PAC {updates}",
                    no_update_string = "UP TO DATE",
                    colour_no_updates = Colours.DARKEST_TAN,
                    colour_have_updates = Colours.DARKEST_TAN
                ),
                default_sep(),
                # widget.MOC(),
                widget.Clock(
                    format='NOW %Y-%m-%d %a %I:%M %p',
                ),
            ]
# whether or not to include the battery widget
# https://stackoverflow.com/a/41988627
    try:
        import psutil # type: ignore
        bat = psutil.sensors_battery()
        if bat is not None and bat.secsleft != 1:
            battery_index = 7 # we want it to be right before the volume widget
            to_ret.insert(battery_index, widget.Battery(foreground=Colours.DARKEST_TAN, background=Colours.DARKEST, format="BAT {char} {percent:2.0%}"))
            to_ret.insert(battery_index, default_sep())
    except ImportError:
        os.system("notify-send \"Could not use psutil library to detect battery!\"")
    return to_ret


# Find the index of the volume widget
def find_volume() -> int:
    # For some reason this does not work: I will do it later today
    # for i, wid in enumerate(widgets):
    #     if isinstance(wid, widget.Volume):
    #         return i
    # yield ValueError
    return -1


screens = [
    Screen(
        top=bar.Bar(
            mk_widgets(),
            24,
        ),
    ),
    Screen(
        top=bar.Bar(
            mk_widgets(),
            24,
        ),
    ),
]




# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    *layout.Floating.default_float_rules,
    Match(wm_class='confirmreset'),  # gitk
    Match(wm_class='makebranch'),  # gitk
    Match(wm_class='maketag'),  # gitk
    Match(wm_class='ssh-askpass'),  # ssh-askpass
    Match(title='branchdialog'),  # gitk
    Match(title='pinentry'),  # GPG key password entry
])
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
