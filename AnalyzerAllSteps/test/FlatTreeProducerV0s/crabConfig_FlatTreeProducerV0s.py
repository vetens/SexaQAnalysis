from WMCore.Configuration import Configuration

day = "15082023"
version = "v1"

config = Configuration()
config.section_('General')
config.General.transferOutputs = True
config.General.transferLogs = True
config.General.requestName = 'FlatTreeProducerV0_DataBPH1A_MinPresel_'+day+'_'+version 
#config.General.requestName = 'FlatTreeProducerV0_DoubleMuonData_runH_'+day+'_'+version 

config.section_('JobType') 
config.JobType.pluginName = 'Analysis' 
config.JobType.psetName = 'FlatTreeProducerV0s_cfg.py' 
config.JobType.priority = 100

config.section_('Data') 
config.Data.unitsPerJob = 2
config.Data.totalUnits = 10000
config.Data.publication = False
config.Data.splitting = 'FileBased' 
config.Data.outLFNDirBase = '/store/user/wvetens/data_Sexaq/FlatTreeV0s' 
config.Data.userInputFiles = open('Data_MinPresel_1A.txt').readlines()
config.Data.outputPrimaryDataset = "crab_FlatTreeV0_DataBPH1A_MinPresel"
config.Data.inputDBS = 'phys03'


config.section_('User') 
#config.User.voGroup = 'becms'

config.section_('Site') 
config.Site.whitelist =['T2_*'] 
config.Site.storageSite = 'T2_US_Wisconsin'
