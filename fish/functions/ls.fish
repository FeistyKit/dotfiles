function ls --wraps='exa --long --all --git' --description 'alias ls=exa --long --all --git'
  exa --long --all --git $argv; 
end
