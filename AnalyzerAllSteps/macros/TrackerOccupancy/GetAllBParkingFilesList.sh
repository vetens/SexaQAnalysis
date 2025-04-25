#!/usr/bin/env bash
source ~/.bashrc
sampleLocation="${1:-/store/user/wvetens/data_Sexaq/TrackerOccupancy/trialB/}"
fOut="${2:-DataMiniAOD.txt}"
x=1
while [ $x -le 6 ]
    do
    folder="ParkingBPH$x"
    samplelist="ParkingSamples${x}.txt"
    rm -f $samplelist
    echo "Now doing for: $sampleLocation$folder"
    gfal-ls-wisc $sampleLocation$folder >> $samplelist
    sed -i -e 's&^&'$sampleLocation$folder'/&' $samplelist
    while read runslice 
        do
        prefix="$sampleLocation$folder/crab_2018BPH_Pileup_trialB_ParkingBPH${x}_Run2018"
        #suffix="-20Jun2021_UL2018-v1_TrackerOccupancy_trialB"
        suffix="-UL2018_MiniAODv2-v1_TrackerOccupancy_trialB"
        if [[ $runslice == *"xEvt"* ]]; then
            continue
        fi
        foo=${runslice#"$prefix"}
        run=${foo%"$suffix"}
        #echo "$runslice/"
        datimes=$( gfal-ls-wisc $runslice )
        datime=""
        for datetime in $datimes
            do
            if [[ $datetime == *"240802_"* ]]; then
                datime=$datetime
            fi
            done
        #echo "$datime"
        dir="$runslice/$datime/"
        echo $dir
        dirslist="${run}_${x}.txt"
        rm -f $dirslist
        gfal-ls-wisc $dir >> $dirslist
        sed -i -e 's&^&'$dir'&' $dirslist
        nSubFolder=0
        while read parts
            do
            flistName="${run}_${x}_${nSubFolder}.txt"
            echo "Making list for run $run slice $x part ${nSubFolder}"
            rm -f $flistName
            where="$parts/"
            MakeFileListOutputOnly $where $flistName
            nSubFolder=$(( $nSubFolder + 1 ))
            done < $dirslist
        rm -f $dirslist
        runsliceFiles="flist_${run}_${x}.txt"
        echo "Combining lists for run $run slice $x"
        rm -f $runsliceFiles
        cat ${run}_${x}_*.txt > $runsliceFiles
        rm -f ${run}_${x}_*.txt
        done < $samplelist
    rm -f $samplelist
    x=$(( $x + 1 ))
    done
for run in {A..D}
do
    RunFiles="B-Parking_trialB_Run2108${run}.txt"
    echo "Combining lists for run $run"
    rm -f $RunFiles
    cat flist_${run}_*.txt > $RunFiles
    rm -f flist_${run}_*.txt
done
rm -f $fOut
echo "Combining All Lists"
cat B-Parking_trialB_Run2108*.txt > $fOut
rm -f B-Parking_trialB_Run2108*.txt
