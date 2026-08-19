#!/bin/bash

OUT="demo6_results.csv"

echo "scenario,mode,split,nSta,offeredPerSta,totalOffered,thr5,thr6,thrTotal,loss,delayMs,jitterMs,efficiency,fairness" > $OUT

echo "===== DEMO 6 Traffic Steering ====="

# Mode comparison
for mode in 0 1 2
do
  ./ns3 run demo-6-traffic-steering.cc -- \
  --mode=$mode --nSta=10 --offeredLoad=20 \
  | tee /dev/tty \
  | grep "^RESULT," \
  | sed "s/RESULT,/mode_compare,/" >> $OUT
done

# Split sweep
for split in 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9
do
  ./ns3 run demo-6-traffic-steering.cc -- \
  --mode=2 --splitRatio=$split --nSta=10 --offeredLoad=20 \
  | tee /dev/tty \
  | grep "^RESULT," \
  | sed "s/RESULT,/split_sweep,/" >> $OUT
done

# Load sweep
for load in 10 15 20 25 30 35 40
do
  ./ns3 run demo-6-traffic-steering.cc -- \
  --mode=2 --splitRatio=0.5 --nSta=10 --offeredLoad=$load \
  | tee /dev/tty \
  | grep "^RESULT," \
  | sed "s/RESULT,/load_sweep,/" >> $OUT
done

# STA scaling
for sta in 5 10 15 20 25 30
do
  ./ns3 run demo-6-traffic-steering.cc -- \
  --mode=2 --splitRatio=0.5 --nSta=$sta --offeredLoad=20 \
  | tee /dev/tty \
  | grep "^RESULT," \
  | sed "s/RESULT,/sta_scaling,/" >> $OUT
done

echo "DONE. Results saved to $OUT"