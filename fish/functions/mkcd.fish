function mkcd --wraps='mkdir $1 && cd $1' --description 'alias mkcd=mkdir $1 && cd $1'
  mkdir $argv && cd $argv;
end
