from WMCore.Configuration import Configuration

day = "23082023"
version = "v1"
#mass = "1p8GeV"
trial = "4"

config = Configuration()
config.section_('General')
config.General.transferOutputs = True
config.General.transferLogs = True
#config.General.requestName = 'FlatTreeProducerTracking_trial'+trial+'_'+day+'_'+version+'_'+mass 
config.General.requestName = 'FlatTreeProducerTracking_trial'+trial+'_'+day+'_'+version

config.section_('JobType') 
config.JobType.pluginName = 'Analysis' 
config.JobType.psetName = '../FlatTreeProducerTracking_cfg.py' 
config.JobType.maxMemoryMB = 5000
#config.JobType.priority = 101

config.section_('Data') 
config.Data.unitsPerJob = 1
config.Data.totalUnits = 10000
config.Data.publication = False
config.Data.splitting = 'FileBased' 
config.Data.outLFNDirBase = '/store/user/wvetens/data_Sexaq/Skimmed/TrackingNtuple' 
#config.Data.outLFNDirBase = '/store/user/jdeclerc/data_Sexaq/Analyzed/trialK' 
#config.Data.userInputFiles = open('/user/jdeclerc/CMSSW_8_0_30/src/SexaQAnalysis/AnalyzerAllSteps/test/wihtMatchingOnHits/inputFiles.txt').readlines() 
#config.Data.inputDataset = '/Skimmed_trial17_1p8GeV_14102019_v1_191014_132642/lowette-crab_Step1_Step2_Skimming_FlatTree_trial17_1p8GeV_17102019_v1-8925145305413877174dac643a893255/USER'
#config.Data.inputDataset = '/CRAB_SimSexaq_trial4/wvetens-crab_Step1_Step2_Skimming_FlatTree_trial4_1p8GeV_11042022_v4-01cbc418214e94ff949e7f7dfd013f28/USER'
config.Data.userInputFiles = open('../Data_MinPresel_1A.txt').readlines()
config.Data.inputDBS = 'phys03'
#config.Data.outputPrimaryDataset = "CRAB_AnalyzerAllStep2_WithPU2016NeutrinoGun_tryToFix_8_"+day+'_'+version
#config.Data.outputPrimaryDataset = "CRAB_AnalyzerAllSkimmed_Data_completely_disabled_cosThetaXYCut_innerHitPosCut_"+day+'_'+version
config.Data.outputPrimaryDataset = "CRAB_AnalyzerAllSkimmed_Data_MinPresel_1A_TrackingNtuple_"+day+'_'+version

config.section_('User') 
#config.User.voGroup = 'becms'

config.section_('Site') 
config.Site.whitelist =['T2_*']
#config.Site.whitelist =['T2_BE_IIHE','T2_AT_Vienna','T2_BE_UCL','T2_CH_CERN_HLT','T2_DE_DESY','T2_DE_RWTH','T2_FR_IPHC','T1_DE_KIT','T1_UK_RAL','T2_HU_Budapest','T2_IT_Bari','T2_IT_Legnaro','T2_IT_Pisa']
config.Site.storageSite = 'T2_US_Wisconsin'
