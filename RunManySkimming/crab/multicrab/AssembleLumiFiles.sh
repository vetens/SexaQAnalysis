#!/bin/bash
mkdir -p processedLumis_trial${1}/
for folder in crab_2018BPH_trial${1}/*
    do prefix="crab_2018BPH_trial${1}/crab_ParkingBPH"; 
    suffix="-20Jun2021_UL2018-v1_trial${1}"; 
    noprefix=${folder#$prefix}; 
    noprefnosuff=${noprefix%$suffix}; 
    slice=${noprefnosuff:0:1}; 
    run=${noprefnosuff: -1}; 
    fname="processedLumis_ParkingBPH${slice}_Run2018${run}.json"; 
    cp $folder/results/processedLumis.json processedLumis_trial${1}/$fname; done
