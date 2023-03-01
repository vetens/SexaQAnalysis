#!/usr/bin/env bash
source /cvmfs/cms.cern.ch/cmsset_default.sh
export SCRAM_ARCH=slc7_amd64_gcc700
cd /afs/cern.ch/work/w/wvetens/Sexaquarks/CMSSW_10_2_26/src/SexaQAnalysis/AnalyzerAllSteps/macros/BDT; eval `scram runtime -sh`>/dev/null
#hadd -f MC_AntiS_Sgn_Trial5_M2SReweigh.root @MC_AntiS_Sgn_Trial5_M2SReweigh.txt
#hadd -f MC_AntiS_Sgn_Trial4_MultiSQEV.root @MC_AntiS_Sgn_Trial4_MultiSQEV.txt
#hadd -f MC_AntiS_Bkg_QCD.root @MC_AntiS_Bkg_QCD.txt
#hadd -f MC_Xevt_Bkg_QCD.root @MC_Xevt_Bkg_QCD.txt
#hadd -f Data_S_Bkg.root @Data_S_Bkg.txt
#hadd -f Data_Xevt_Bkg.root @Data_Xevt_Bkg.txt
python AnalyzerFlatTreeBDT.py
#DEBUG
#python -i runDIGIRECOSKIM_Sexaq_withCuts/BPH-RunIIFall18DigiRecoCombined_Sexaq_cfg.py inputFiles=file:GenSimTest3.root outputFile=file:FullSkimTest3.root > SkimTest3Out.txt 2>&1
