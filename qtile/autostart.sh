#!/usr/bin/env sh
rm "$HOME"/.moc/pid
dunst &
mocp -S
picom &
setxkbmap -option compose:ralt
nitrogen --restore &
emacs --daemon
sxhkd -c "$HOME/.config/sxhkd/sxhkdrc" &
flatpak run net.christianbeier.Gromit-MPX &
