#!/usr/bin/env zsh
set -e
rni 10 3

LOGFILE=execute-all.$$.log
rm -f $LOGFILE
for i in `cat ~/servers/all-locations`; do
  (timeout 30 ssh $i.ddnet.tw "echo '$1' > servers/servers/*.fifo"
  if [ $? -eq 0 ]; then
    echo -e "\e[1;32m$i executed successfully\e[0m" >> $LOGFILE
  else
    echo -e "\e[1;33mExecuting on $i failed\e[0m" >> $LOGFILE
  fi) &
done
wait

echo -e "\e[1;31m$(grep successfully $LOGFILE | wc -l)/$(wc -w < all-locations) servers executed successfully\e[0m"
grep failed $LOGFILE || true
rm $LOGFILE
