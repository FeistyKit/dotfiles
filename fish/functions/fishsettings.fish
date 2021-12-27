function fishsettings --wraps='nvim ~/.config/fish/config.fish' --description 'alias fishsettings nvim ~/.config/fish/config.fish'
  nvim ~/.config/fish/config.fish $argv; 
end
