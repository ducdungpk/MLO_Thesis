#!/bin/bash

OUT="demo5_results.csv"

echo "scenario,mode,band,nSta,offeredPerSta,totalOffered,width,mcs,thrTotal,loss,delayMs,jitterMs,efficiency,fairness" > $OUT

echo "===== DEMO 5 Multiband Evaluation ====="

# Band comparison
for band in 5 6
do
  ./ns3 run demo-5-multiband-evaluation.cc -- --band=$band --nSta=5 --offeredLoad=20 --width=20 --mcs=EhtMcs7 \
  | tee /dev/tty \
  | grep "^RESULT," \
  | sed "s/RESULT,/band_compare,/" >> $OUT
done

# Width scaling
for width in 20 40 80
do
  ./ns3 run demo-5-multiband-evaluation.cc -- --band=5 --width=$width --nSta=5 --offeredLoad=40 --mcs=EhtMcs7 \
  | tee /dev/tty \
  | grep "^RESULT," \
  | sed "s/RESULT,/width_scaling,/" >> $OUT
done

# Load sweep
for load in 1 3 5 7 9 11 13 15 17 20 25 30
do
  ./ns3 run demo-5-multiband-evaluation.cc -- --band=5 --width=20 --nSta=5 --offeredLoad=$load --mcs=EhtMcs7 \
  | tee /dev/tty \
  | grep "^RESULT," \
  | sed "s/RESULT,/load_sweep,/" >> $OUT
done

# STA scaling
for sta in 1 2 3 4 5 6 8 10 12 14 16
do
  ./ns3 run demo-5-multiband-evaluation.cc -- --band=5 --width=20 --nSta=$sta --offeredLoad=10 --mcs=EhtMcs7 \
  | tee /dev/tty \
  | grep "^RESULT," \
  | sed "s/RESULT,/sta_scaling,/" >> $OUT
done

# Heavy stress
for sta in 10 15 20
do
  for load in 40 50 60
  do
    ./ns3 run demo-5-multiband-evaluation.cc -- --band=5 --width=20 --nSta=$sta --offeredLoad=$load --mcs=EhtMcs7 \
    | tee /dev/tty \
    | grep "^RESULT," \
    | sed "s/RESULT,/stress,/" >> $OUT
  done
done

echo "DONE. Results saved to $OUT"