#!/bin/bash

OUT="demo7_results.csv"

echo "scenario,nSta,mode,speed,m,offeredPerSta,totalOffered,thrTotal,loss,delayMs,jitterMs,efficiency,fairness" > $OUT

echo "===== DEMO 7 Robustness Evaluation ====="

run_and_parse () {
  ./ns3 run demo-7-robustness.cc -- "$@" \
  | tee /dev/tty \
  | grep "^RESULT," \
  | sed 's/RESULT,//'
}

# Baseline
run_and_parse \
--nSta=10 --speed=1.5 --nakagamiM=2 --offeredLoad=10 \
| sed "s/^/baseline,/" >> $OUT

# Repeatability test
for run in 1 2 3 4 5
do
  run_and_parse \
  --RngRun=$run --nSta=10 --speed=1.5 --nakagamiM=2 --offeredLoad=10 \
  | sed "s/^/repeat_test,/" >> $OUT
done

# Mobility sweep
for speed in 0 0.5 1 2 3 5 7 10 15 20
do
  run_and_parse \
  --nSta=10 --speed=$speed --nakagamiM=2 --offeredLoad=10 \
  | sed "s/^/mobility_sweep,/" >> $OUT
done

# Fading sweep
for m in 0.5 1 1.5 2 2.5 3 4
do
  run_and_parse \
  --nSta=10 --speed=1.5 --nakagamiM=$m --offeredLoad=10 \
  | sed "s/^/fading_sweep,/" >> $OUT
done

# Load sweep
for load in 10 20 30 40 50 60 70 80 90 100 110 120 150 180 200 250 300
do
  run_and_parse \
  --nSta=10 --speed=1.5 --nakagamiM=2 --offeredLoad=$load \
  | sed "s/^/load_sweep,/" >> $OUT
done

# Stress test (combined conditions)
for speed in 0 1 2 3
do
  for m in 1 2 3
  do
    for load in 30 40 50 60 70 80
    do
      run_and_parse \
      --nSta=10 --speed=$speed --nakagamiM=$m --offeredLoad=$load \
      | sed "s/^/stress_test,/" >> $OUT
    done
  done
done

echo "DONE. Results saved to $OUT"
