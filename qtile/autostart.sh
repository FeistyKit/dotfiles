#!/usr/bin/env sh
rm "$HOME"/.moc/pid
dunst &
mocp -S &
pnmixer &
# picom --corner-radius 30 &
picom &
setxkbmap -option compose:ralt
nitrogen --restore &
emacs --daemon &
sxhkd -c "$HOME/.config/sxhkd/sxhkdrc" &
../utils/xborder/xborders --border-rgba "#FABD2FFF" --border-radius 30 &
