#!/bin/bash

OUT="demo3_results.csv"

echo "scenario,nSta,offeredPerSta,totalOffered,thrTotal,loss,delayMs,jitterMs,efficiency,fairness" > $OUT

echo "===== DEMO 3 FULL EXPERIMENT ====="

# Load Sweep (Single STA)
for load in 1 4 7 10 13 17 20 23 26 29 32 35 40 50 60 70 
do
  ./ns3 run demo-3-multi-sta-single-link.cc -- --nSta=5 --offeredLoad=$load \
  | tee /dev/tty \
  | grep "^RESULT," \
  | sed "s/RESULT,/load_sweep,/" >> $OUT
done

# STA Scaling
for sta in 1 5 7 9 11 13 15 17 20 25 30 35 40 50
do
  ./ns3 run demo-3-multi-sta-single-link.cc -- --nSta=$sta --offeredLoad=5 \
  | tee /dev/tty \
  | grep "^RESULT," \
  | sed "s/RESULT,/sta_scaling,/" >> $OUT
done

# Heavy Stress
for sta in 15 20 25 30
do
  for load in 80 90 100 110
  do
    ./ns3 run demo-3-multi-sta-single-link.cc -- --nSta=$sta --offeredLoad=$load \
    | tee /dev/tty \
    | grep "^RESULT," \
    | sed "s/RESULT,/stress,/" >> $OUT
  done
done

echo "DONE. Results saved to $OUT"