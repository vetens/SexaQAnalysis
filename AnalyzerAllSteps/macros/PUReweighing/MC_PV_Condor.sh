#!/usr/bin/env bash
source /cvmfs/cms.cern.ch/cmsset_default.sh
export SCRAM_ARCH=slc7_amd64_gcc700
cd /afs/cern.ch/work/w/wvetens/Sexaquarks/CMSSW_10_2_26/src/; eval `scram runtime -sh`>/dev/null
export X509_USER_PROXY=/afs/cern.ch/work/w/wvetens/Sexaquarks/CMSSW_10_2_26/src/userproxy
cd /afs/cern.ch/work/w/wvetens/Sexaquarks/CMSSW_10_2_26/src/SexaQAnalysis/AnalyzerAllSteps/macros/PUReweighing/
python PVInfo.py --isMC=True --outputDir=plots_MC/ --inFiles=list.txt --preScale=1000
#DEBUG
#python -i runDIGIRECOSKIM_Sexaq_withCuts/BPH-RunIIFall18DigiRecoCombined_Sexaq_cfg.py inputFiles=file:GenSimTest3.root outputFile=file:FullSkimTest3.root > SkimTest3Out.txt 2>&1
