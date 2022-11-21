# Dotfiles

My dotfiles! They're not very good, nor do they look particularly nice, but I like them!

## Install

``` sh
$ git clone https://github.com/feistykit/dotfiles
$ cd dotfiles
$ python3 install.py
```

If you want to not use one or more of my configs, pass `--exclude <CONFIGS..>` to the installer. The list of available configs can be found [here](./modules-list).

## Depends
I haven't gotten around to checking all of the dependencies, but here is an incomplete list (besides the obvious ones, like zsh requiring zsh, etc.)
 - zsh: exa, starship
 - fish: exa, zoxide
 - i3: sxhkd
