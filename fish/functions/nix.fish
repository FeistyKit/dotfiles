function nix --wraps='sudo nix --extra-experimental-features nix-command --extra-experimental-features flakes' --description 'alias nix=sudo nix --extra-experimental-features nix-command --extra-experimental-features flakes'
  sudo nix --extra-experimental-features nix-command --extra-experimental-features flakes $argv; 
end
