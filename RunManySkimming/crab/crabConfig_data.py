from WMCore.Configuration import Configuration

day = "13062022"
version = "v2"

config = Configuration()
config.section_('General')
config.General.transferOutputs = True
config.General.transferLogs = True
config.General.requestName = 'ParkingBPH2_Run2018B-20Jun2021_UL2018-v1_BLOCK_A_SkimmingSexaq_'+day+'_'+version 

config.section_('JobType') 
config.JobType.pluginName = 'Analysis' 
config.JobType.psetName = 'treeproducer_data_cfg.py' 
config.JobType.priority = 150

config.section_('Data') 
config.Data.unitsPerJob = 1000 
config.Data.totalUnits = 1
config.Data.publication = False 
config.Data.splitting = 'Automatic' #FileBased 
config.Data.outLFNDirBase = '/store/user/wvetens/crmc_Sexaq/' 
#config.Data.userInputFiles = open('/user/jdeclerc/CMSSW_8_0_30/src/SexaQAnalysis/RunManySkimming/crab/inputFiles_DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_ADAPTED_VO_ALREADY_RAN_slimmed.txt').readlines() 
#config.Data.inputDataset = '/QCD_Pt-170to300_MuEnrichedPt5_TuneCP5_13TeV_pythia8/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v3/AODSIM'
config.Data.inputDataset = '/ParkingBPH2/Run2018B-20Jun2021_UL2018-v1/AOD'
config.Data.runRange = '318874,318876-318877'


#config.Data.inputDBS = 'global'
#config.Data.outputPrimaryDataset = "ParkingBPH2_Run2018B-20Jun2021_UL2018-v1_BLOCK_A_SkimmingSexaq"+day+"_"+version
#config.Data.ignoreLocality = True

config.section_('User') 
#config.User.voGroup = 'becms'

config.section_('Site') 
#config.Site.whitelist = ['T2_BE_IIHE','T2_AT_Vienna','T2_BE_UCL','T2_CH_CERN_HLT','T2_DE_DESY','T2_DE_RWTH','T2_FR_IPHC','T1_DE_KIT','T1_UK_RAL','T2_HU_Budapest','T2_IT_Bari','T2_IT_Legnaro','T2_IT_Pisa']
config.Site.whitelist = ['T2*']
config.Site.storageSite = 'T2_US_Wisconsin'
