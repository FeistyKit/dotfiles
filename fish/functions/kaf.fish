function kaf --wraps='killall -9 /usr/lib/firefox/firefox' --description 'alias kaf=killall -9 /usr/lib/firefox/firefox'
  killall -9 /usr/lib/firefox/firefox $argv; 
end
