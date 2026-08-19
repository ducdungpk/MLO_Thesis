#!/bin/bash

OUT="demo2_results.csv"
echo "scenario,nSta,totalOffered,thr5,thr6,total,loss,delayMs,jitterMs,efficiency,fairness" > $OUT

echo "===== DEMO 2 (5G + 6G MLO) ====="

#####################################
# Load sweep
#####################################

for load in 20 60 100 140 180 220 260 280 300 320 340 380 420 460 500
do
  ./ns3 run demo-2-dual-link.cc -- --nSta=1 --offeredLoad=$load \
  | tee /dev/tty \
  | grep "^RESULT," \
  | sed "s/RESULT,/load_sweep,/" >> $OUT
done


#####################################
# STA scaling
#####################################

for sta in 1 5 10 15 18 21 24 27 30 35 40
do
  ./ns3 run demo-2-dual-link.cc -- --nSta=$sta --offeredLoad=100 \
  | tee /dev/tty \
  | grep "^RESULT," \
  | sed "s/RESULT,/sta_scaling,/" >> $OUT
done


#####################################
# Stress
#####################################

for sta in 5 10 15 20 25
do
  for load in 10 20 40 60 80
  do
    ./ns3 run demo-2-dual-link.cc -- --nSta=$sta --offeredLoad=$load \
    | tee /dev/tty \
    | grep "^RESULT," \
    | sed "s/RESULT,/stress,/" >> $OUT
  done
done

echo "DONE. Results saved to $OUT"