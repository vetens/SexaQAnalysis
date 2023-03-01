#!/bin/bash
source /cvmfs/cms.cern.ch/cmsset_default.sh
export SCRAM_ARCH=slc7_amd64_gcc700
cd /afs/cern.ch/work/w/wvetens/Sexaquarks/CMSSW_10_2_26/src ; eval `scram runtime -sh` ; cd - >/dev/null
#echo 'ENVIRONMENT BEGIN:'
#env
#echo 'ENVIRONMENT END'
#echo 'LDD BEGIN:'
#ldd /afs/cern.ch/work/w/wvetens/Sexaquarks/CMSSW_10_2_26/src/CustomGenerator/Custom/crmc_Sexaq_incl_installed/bin/crmc
#echo 'LDD END'
cd /afs/cern.ch/work/w/wvetens/Sexaquarks/CMSSW_10_2_26/src/SexaQAnalysis/AnalyzerAllSteps/test/FlatTreeProducerGEN/
export X509_USER_PROXY=/afs/cern.ch/work/w/wvetens/Sexaquarks/CMSSW_10_2_26/src/userproxy
voms-proxy-init -voms cms -pwstdin < ~/pwstdin
cmsRun /afs/cern.ch/work/w/wvetens/Sexaquarks/CMSSW_10_2_26/src/SexaQAnalysis/AnalyzerAllSteps/test/FlatTreeProducerGEN/FlatTreeProducerGEN_cfg.py inputFiles=root://cmsxrootd.hep.wisc.edu//store/user/wvetens/crmc_Sexaq/crmc/Sexaquark_13TeV_trial_5_1p8GeV_MultiSQEV/0/crmc_Sexaq_0.root outputFile=file:output_Trial5MultiSQ_Test.root
#cmsRun /afs/cern.ch/work/w/wvetens/Sexaquarks/CMSSW_10_2_26/src/SexaQAnalysis/AnalyzerAllSteps/test/FlatTreeProducerGEN/FlatTreeProducerGEN_cfg.py inputFiles=root://cmsxrootd.hep.wisc.edu//store/user/wvetens/crmc_Sexaq/crmc/Sexaquark_13TeV_trial_4_1p8GeV/1/crmc_Sexaq_0.root outputFile=file:output.root
