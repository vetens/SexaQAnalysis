#!/usr/bin/env bash
source /cvmfs/cms.cern.ch/cmsset_default.sh
export SCRAM_ARCH=slc7_amd64_gcc700
cd /afs/cern.ch/work/w/wvetens/Sexaquarks/CMSSW_10_2_26/src/SexaQAnalysis/AnalyzerAllSteps/macros/Tracking ; eval `scram runtime -sh`>/dev/null
python AnalyzerFlatTreeTracking_AntiS_specific.py --mass=${1}
