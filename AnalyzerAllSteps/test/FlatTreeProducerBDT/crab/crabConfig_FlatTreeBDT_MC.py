from WMCore.Configuration import Configuration

day = "08052023"
version = "v3"
trial = "1"


config = Configuration()
config.section_('General')
config.General.transferOutputs = True
config.General.transferLogs = True
config.General.requestName = 'FlatTreeProducerBDT_'+'SQRECO_In_QCDSIM_'+'trial'+trial+'_'+day+'_'+version

config.section_('JobType') 
config.JobType.pluginName = 'Analysis' 
config.JobType.psetName = '../FlatTreeProducerBDT_cfg_MC.py' 
config.JobType.priority = 150

config.section_('Data') 
config.Data.unitsPerJob = 1
config.Data.totalUnits = 10000
config.Data.publication = True
config.Data.splitting = 'FileBased' 
config.Data.outLFNDirBase = '/store/user/wvetens/crmc_Sexaq/FlatTree_BDT' 
config.Data.userInputFiles = open('/afs/cern.ch/work/w/wvetens/Sexaquarks/data/CMSSW_10_6_26/src/SexaQAnalysis/AnalyzerAllSteps/test/FlatTreeProducerBDT/crab/SQ_In_QCD_Pt-170to300_MuEnrichedPt5_TuneCP5_13TeV_pythia8.txt').readlines() 
#config.Data.inputDataset = '/CRAB_SimSexaq_trial21/lowette-crab_Step1_Step2_Skimming_FlatTree_trial21_1p8GeV_23102019_v1-8925145305413877174dac643a893255/USER'
config.Data.inputDBS = 'phys03'
config.Data.outputPrimaryDataset = "FlatTreeProducerBDT_SQ_In_QCD_Pt-170to300_MuEnrichedPt5_TuneCP5_13TeV_pythia8_"+day+'_'+version

config.section_('User') 
#config.User.voGroup = 'becms'

config.section_('Site') 
#config.Site.whitelist =['T2_BE_IIHE','T2_AT_Vienna','T2_BE_UCL','T2_CH_CERN_HLT','T2_DE_DESY','T2_DE_RWTH','T2_FR_IPHC','T1_DE_KIT','T1_UK_RAL','T2_HU_Budapest','T2_IT_Bari','T2_IT_Legnaro','T2_IT_Pisa']
config.Site.whitelist =['T2_*']
config.Site.storageSite = 'T2_US_Wisconsin'
