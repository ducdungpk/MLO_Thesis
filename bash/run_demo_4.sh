#!/bin/bash

OUT="demo4_results.csv"

echo "scenario,nSta,offeredPerStaPerLink,totalOffered,thr5,thr6,thrTotal,loss,delayMs,jitterMs,efficiency,fairness" > $OUT

echo "===== DEMO 4 (MLO Multi-STA Dual-Link) ====="

# Load Sweep
for load in 2 8 14 20 26 32 38 44 50 56 65 80 90
do
  ./ns3 run demo-4-multi-sta-dual-link.cc -- --nSta=5 --offeredLoad=$load --RngRun=1 \
  | tee /dev/tty \
  | grep "^RESULT," \
  | sed "s/RESULT,/load_sweep,/" >> $OUT
done

# STA Scaling
for sta in 1 5 7 9 11 13 15 17 20 25 30 35 40 50
do
  ./ns3 run demo-4-multi-sta-dual-link.cc -- --nSta=$sta --offeredLoad=2.5 --RngRun=1 \
  | tee /dev/tty \
  | grep "^RESULT," \
  | sed "s/RESULT,/sta_scaling,/" >> $OUT
done

# Heavy Stress
for sta in 15 20 25 30
do
  for load in 80 90 100 110
  do
    ./ns3 run demo-4-multi-sta-dual-link.cc -- --nSta=$sta --offeredLoad=$load --RngRun=1 \
    | tee /dev/tty \
    | grep "^RESULT," \
    | sed "s/RESULT,/stress,/" >> $OUT
  done
done

echo "DONE. Results saved to $OUT"
