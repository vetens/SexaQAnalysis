from WMCore.Configuration import Configuration

day = "14102019"
version = "v1"

config = Configuration()
config.section_('General')
config.General.transferOutputs = True
config.General.transferLogs = True
config.General.requestName = 'FlatTreeProducerV0_DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_'+day+'_'+version 
#config.General.requestName = 'FlatTreeProducerV0_DoubleMuonData_runH_'+day+'_'+version 

config.section_('JobType') 
config.JobType.pluginName = 'Analysis' 
config.JobType.psetName = 'FlatTreeProducerV0s_cfg.py' 
config.JobType.priority = 100

config.section_('Data') 
config.Data.unitsPerJob = 250
config.Data.totalUnits = 10000
config.Data.publication = False
config.Data.splitting = 'FileBased' 
config.Data.outLFNDirBase = '/store/user/jdeclerc/MC/FlatTreeV0s' 
config.Data.userInputFiles = open('/user/jdeclerc/CMSSW_8_0_30_bis/src/SexaQAnalysis/AnalyzerAllSteps/test/FlatTreeProducerV0s/inputFiles_DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8.txt').readlines()
config.Data.outputPrimaryDataset = "crab_FlatTreeV0_DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8"


config.section_('User') 
config.User.voGroup = 'becms'

config.section_('Site') 
config.Site.whitelist =['T2_BE_IIHE'] 
config.Site.storageSite = 'T2_BE_IIHE'
