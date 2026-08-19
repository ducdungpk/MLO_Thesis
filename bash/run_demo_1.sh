#!/bin/bash

OUTPUT_FILE="demo1_results.csv"

echo "scenario,nSta,offeredPerSta,totalOffered,throughput,loss,delayMs,jitterMs,efficiency,fairness" > $OUTPUT_FILE

echo "===== DEMO 1 FULL EXPERIMENT ====="

########################################
# Offered Load Sweep (Single STA)
########################################

for load in 10 20 30 40 50 60 65 70 80 90 100 120 140 160 180 200 300 400 
do
  echo "Running: nSta=1 load=$load Mbps"

  ./ns3 run demo-1-single-link-baseline.cc -- \
    --nSta=1 --offeredLoad=$load \
  | tee /dev/tty \
  | grep "^RESULT," \
  | sed "s/RESULT,/single_sta_load_sweep,/" \
  >> $OUTPUT_FILE

done

########################################
# Multi-STA Scaling
########################################

for sta in 1 5 10 15 18 21 24 27 30 35 40
do
  echo "Running: nSta=$sta load=5 Mbps"

  ./ns3 run demo-1-single-link-baseline.cc -- \
    --nSta=$sta --offeredLoad=5 \
  | tee /dev/tty \
  | grep "^RESULT," \
  | sed "s/RESULT,/multi_sta_scaling,/" \
  >> $OUTPUT_FILE

done

########################################
# Stress Test
########################################

for sta in 5 10 15 20
do
  for load in 10 20 40
  do
    echo "Running: nSta=$sta load=$load Mbps"

    ./ns3 run demo-1-single-link-baseline.cc -- \
      --nSta=$sta --offeredLoad=$load \
    | tee /dev/tty \
    | grep "^RESULT," \
    | sed "s/RESULT,/stress_test,/" \
    >> $OUTPUT_FILE

  done
done

echo "===== DONE ====="
echo "Results saved to $OUTPUT_FILE"