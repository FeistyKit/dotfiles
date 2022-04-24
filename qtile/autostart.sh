#!/usr/bin/env sh
rm "$HOME"/.moc/pid
dunst &
mocp -S &
picom --corner-radius 30 &
setxkbmap -option compose:ralt
nitrogen --restore &
emacs --daemon &
sxhkd -c "$HOME/.config/sxhkd/sxhkdrc" &
../utils/xborder/xborders --border-rgba "#FABD2FFF" --border-radius 30 &
