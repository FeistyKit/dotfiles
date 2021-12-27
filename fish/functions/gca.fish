function gca --wraps='git commit --all -m' --description 'alias gca git commit --all -m'
  git commit --all -m $argv; 
end
