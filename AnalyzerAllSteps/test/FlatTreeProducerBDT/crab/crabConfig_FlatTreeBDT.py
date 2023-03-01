from WMCore.Configuration import Configuration

day = "23012023"
version = "v3"
#trial = "4"
#trial = "4_MultiSQEV"
trial = "5_MultiToSingleReweighed"
mass = "1p8GeV"


config = Configuration()
config.section_('General')
config.General.transferOutputs = True
config.General.transferLogs = True
config.General.requestName = 'FlatTreeProducerBDT_BlockAPUReweigh_trial'+trial+'_'+mass+'_'+day+'_'+version 

config.section_('JobType') 
config.JobType.pluginName = 'Analysis' 
config.JobType.psetName = '../FlatTreeProducerBDT_cfg.py' 
config.JobType.priority = 150
#config.JobType.maxMemoryMB = 5000

config.section_('Data') 
config.Data.unitsPerJob = 1
config.Data.totalUnits = 10000
config.Data.publication = True
config.Data.splitting = 'FileBased' 
config.Data.outLFNDirBase = '/store/user/wvetens/crmc_Sexaq/FlatTree_BDT' 
#config.Data.userInputFiles = open('MCSbar_MultiSQEV_Trial4.txt').readlines() 
config.Data.userInputFiles = open('EDM_RECOSKIM_Trial5_M2SReweigh.txt').readlines() 
#config.Data.inputDataset = '/CRAB_SimSexaq_trial21/lowette-crab_Step1_Step2_Skimming_FlatTree_trial21_1p8GeV_23102019_v1-8925145305413877174dac643a893255/USER'
config.Data.inputDBS = 'phys03'
config.Data.outputPrimaryDataset = "SbarSignalMC_FlatTreeProducerBDT_BlockAPUReweigh_trial"+trial+"_"+mass+"_"+day+'_'+version

config.section_('User') 
#config.User.voGroup = 'becms'

config.section_('Site') 
#config.Site.whitelist =['T2_BE_IIHE','T2_AT_Vienna','T2_BE_UCL','T2_CH_CERN_HLT','T2_DE_DESY','T2_DE_RWTH','T2_FR_IPHC','T1_DE_KIT','T1_UK_RAL','T2_HU_Budapest','T2_IT_Bari','T2_IT_Legnaro','T2_IT_Pisa']
config.Site.whitelist =['T2_US_*']
config.Site.storageSite = 'T2_US_Wisconsin'
