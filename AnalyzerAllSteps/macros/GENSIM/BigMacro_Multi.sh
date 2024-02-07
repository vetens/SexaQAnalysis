#!/usr/bin/env bash
source /cvmfs/cms.cern.ch/cmsset_default.sh
export SCRAM_ARCH=slc7_amd64_gcc700
cd /afs/cern.ch/work/w/wvetens/Sexaquarks/CMSSW_10_2_26/src/SexaQAnalysis/AnalyzerAllSteps/macros/GENSIM ; eval `scram runtime -sh`>/dev/null
#hadd -f hadd_Trial5_MultiSQEV_v4.root @GENSIM_NTuples_Trial5_MultiSQEV_v4.txt
python AnalyzerFlatTreeGENSIM_Multi.py --mass=${1}
#DEBUG
#python -i runDIGIRECOSKIM_Sexaq_withCuts/BPH-RunIIFall18DigiRecoCombined_Sexaq_cfg.py inputFiles=file:GenSimTest3.root outputFile=file:FullSkimTest3.root > SkimTest3Out.txt 2>&1
