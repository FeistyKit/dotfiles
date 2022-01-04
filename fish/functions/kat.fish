function kat --wraps='killall -9 $TERM' --description 'alias kat=killall -9 $TERM'
  killall -9 $TERM $argv; 
end
