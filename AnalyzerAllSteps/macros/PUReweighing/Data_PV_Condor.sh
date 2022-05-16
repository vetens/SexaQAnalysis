#!/usr/bin/env bash
source /cvmfs/cms.cern.ch/cmsset_default.sh
export SCRAM_ARCH=slc7_amd64_gcc700
cd /afs/cern.ch/work/w/wvetens/Sexaquarks/data/CMSSW_10_6_26/src/; eval `scram runtime -sh`>/dev/null
export X509_USER_PROXY=/afs/cern.ch/work/w/wvetens/Sexaquarks/CMSSW_10_2_26/src/userproxy
cd /afs/cern.ch/work/w/wvetens/Sexaquarks/data/CMSSW_10_6_26/src/SexaQAnalysis/AnalyzerAllSteps/macros/PUReweighing/
python PVInfo_data.py
