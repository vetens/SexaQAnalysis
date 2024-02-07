from WMCore.Configuration import Configuration

day = "27032023"
version = "v3"
trial = "1"
#mass = "1p8GeV"


config = Configuration()
config.section_('General')
config.General.transferOutputs = True
config.General.transferLogs = True
#config.General.requestName = 'PileupInfo_BdToDstarTauNu_BParking'+'trial'+trial+'_'+day+'_'+version
config.General.requestName = 'PileupInfo_BToHNLEMuX_BParking'+'trial'+trial+'_'+day+'_'+version

config.section_('JobType') 
config.JobType.pluginName = 'Analysis' 
config.JobType.psetName = '../PileUpScraper_cfg_MC.py' 
config.JobType.priority = 150

config.section_('Data') 
config.Data.unitsPerJob = 1
config.Data.totalUnits = 10000
config.Data.publication = True
config.Data.splitting = 'FileBased' 
config.Data.outLFNDirBase = '/store/user/wvetens/crmc_Sexaq/PileupInfo' 
#config.Data.userInputFiles = open('/afs/cern.ch/work/w/wvetens/Sexaquarks/data/CMSSW_10_6_26/src/SexaQAnalysis/AnalyzerAllSteps/test/FlatTreeProducerBDT/crab/BPH1_2018A_fragment_With_Xevt.txt').readlines() 
#config.Data.userInputFiles = open('/afs/cern.ch/work/w/wvetens/Sexaquarks/data/CMSSW_10_6_26/src/SexaQAnalysis/AnalyzerAllSteps/test/FlatTreeProducerBDT/crab/BPH2_Run2018B_BLOCK_A_Full.txt').readlines() 
#config.Data.inputDataset = '/BdToDstarTauNu_SoftQCDnonD_TuneCP5_13TeV-pythia8-evtgen/RunIIAutumn18MiniAOD-Custom_RDStar_BParking_102X_upgrade2018_realistic_v15-v2/MINIAODSIM'
config.Data.inputDataset = '/BToHNLEMuX_HNLToEMuPi_SoftQCD_b_mHNL1p0_ctau1000p0mm_TuneCP5_13TeV-pythia8-evtgen/RunIIAutumn18MiniAOD-Custom_RDStar_BParking_102X_upgrade2018_realistic_v15-v1/MINIAODSIM'
config.Data.inputDBS = 'global'
#config.Data.outputPrimaryDataset = "FlatTreeProducerBDT_BPH2_Run2018B_BLOCK_A_"+day+'_'+version
#config.Data.outputPrimaryDataset = "PileupInfo_BdToDstarTauNu_BParking_trial"+trial+"_"+day+'_'+version

config.section_('User') 
#config.User.voGroup = 'becms'

config.section_('Site') 
#config.Site.whitelist =['T2_BE_IIHE','T2_AT_Vienna','T2_BE_UCL','T2_CH_CERN_HLT','T2_DE_DESY','T2_DE_RWTH','T2_FR_IPHC','T1_DE_KIT','T1_UK_RAL','T2_HU_Budapest','T2_IT_Bari','T2_IT_Legnaro','T2_IT_Pisa']
config.Site.whitelist =['T2_*']
config.Site.storageSite = 'T2_US_Wisconsin'
