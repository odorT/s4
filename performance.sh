#!/bin/bash
# usage : ./performance_test.sh MAX URL

max="$1"
date
echo "url: $2
rate: $max calls / second"
START=$(date +%s);
echo "start time : $(date +%H:%M:%S) on $(date +%D)"
echo "test"

get () {
  curl -s -v "$1" 2>&1 | tr '\r\n' '\\n' | awk -v date="$(date +'%r')" '{print $0"\n-----", date}' >> ./perf-test.log
  status_code=$(curl -I "$1" 2>/dev/null | head -n 1 | cut -d$' ' -f2)
  echo "Status code- HTTP/2 $status_code"
  firstchar=${status_code::1}
  
  if [[ "$firstchar" == '2' ]]; then
    echo 'success'
  elif [[ "$firstchar" == '3' ]]; then
    echo 'redirected'
  else
    echo 'failed'
  fi
}
echo "Sending $max requests at a time"

while true
do

  time=$(($(date +%s) - START))
  echo $(($(date +%s) - START)) | awk '{print int($1/60)":"int($1%60)}'
  sleep 1

  for i in `seq 1 $max`
  do
    get $2 &
  done
done
