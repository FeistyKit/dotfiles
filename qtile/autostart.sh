#!/usr/bin/sh
rm "$HOME"/.moc/pid
dunst &
mocp -S
picom &
setxkbmap -option compose:ralt
nitrogen --restore &
emacs --daemon
pyro4-ns &
diodon &
