from WMCore.Configuration import Configuration

day = "24052022"
version = "v1"

config = Configuration()
config.section_('General')
config.General.transferOutputs = True
config.General.transferLogs = True
config.General.requestName = 'FlatTreeProducerV0_SignalSexaq_'+day+'_'+version 
#config.General.requestName = 'FlatTreeProducerV0_DoubleMuonData_runH_'+day+'_'+version 

config.section_('JobType') 
config.JobType.pluginName = 'Analysis' 
config.JobType.psetName = 'FlatTreeProducerV0s_cfg.py' 
#config.JobType.maxMemoryMB = 5000
#config.JobType.priority = 100

config.section_('Data') 
config.Data.unitsPerJob = 1
config.Data.totalUnits = 10000
config.Data.publication = True
config.Data.splitting = 'FileBased' 
config.Data.outLFNDirBase = '/store/user/wvetens/crmc_Sexaq/Skimmed/FlatTreeV0s' 
config.Data.userInputFiles = open('EDM_RECOSKIM_Trial4.txt').readlines()
config.Data.outputPrimaryDataset = "crab_FlatTreeV0_SignalSexaq"+day+'_'+version

config.section_('User') 
#config.User.voGroup = 'becms'

config.section_('Site') 
config.Site.whitelist =['T2_*'] 
config.Site.storageSite = 'T2_US_Wisconsin'
