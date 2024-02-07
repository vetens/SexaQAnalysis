import sys
import FWCore.ParameterSet.Config as cms
from FWCore.ParameterSet.VarParsing import VarParsing

runningOnData = False #should be False as you will only run this on MC 
lookAtAntiS =   True  #should be False as you will only run this on MC

options = VarParsing ('analysis')
options.parseArguments()
## data or MC options
options.register(
	'isData',True,VarParsing.multiplicity.singleton,VarParsing.varType.bool,
	'flag to indicate data or MC')

options.register(
	'maxEvts',-1,VarParsing.multiplicity.singleton,VarParsing.varType.int,
#  	'maxEvts',10000,VarParsing.multiplicity.singleton,VarParsing.varType.int,
	'flag to indicate max events to process')
	
options.isData==True

process = cms.Process("SEXAQDATAANA")
process.load("FWCore.MessageService.MessageLogger_cfi")
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.load('Configuration/StandardSequences/MagneticField_38T_cff')
process.load('Configuration/StandardSequences/Reconstruction_cff')
process.load('Configuration/EventContent/EventContent_cff')

from Configuration.AlCa.GlobalTag import GlobalTag

if(options.isData==True):
    #Why is this here for gen? Regardless if I need it I will update when I look at data
    process.GlobalTag = GlobalTag(process.GlobalTag, '80X_dataRun2_2016SeptRepro_v7', '')
else:
    process.GlobalTag = GlobalTag(process.GlobalTag, '102X_upgrade2018_realistic_v15', '')

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(options.maxEvts))
process.MessageLogger.cerr.FwkReport.reportEvery = cms.untracked.int32(1000)
process.options = cms.untracked.PSet(wantSummary = cms.untracked.bool(True))

#inlist = open("EDM_MCSbar_Trial1_1p7GeV.txt", "r")
#inlist = open("EDM_MCSbar_Trial6_1p8GeV.txt", "r")
#inlist = open("EDM_MCSbar_Trial1_1p85GeV.txt", "r")
#inlist = open("EDM_MCSbar_Trial1_1p9GeV.txt", "r")
#inlist = open("EDM_MCSbar_Trial1_2GeV.txt", "r")

#inlist = open("GetEtaCutEffs_1p7.txt", "r")
#inlist = open("GetEtaCutEffs_1p8.txt", "r")
#inlist = open("GetEtaCutEffs_1p85.txt", "r")
#inlist = open("GetEtaCutEffs_1p9.txt", "r")
inlist = open("GetEtaCutEffs_2.txt", "r")
process.source = cms.Source("PoolSource",
	#fileNames = cms.untracked.vstring(options.inputFiles),
	fileNames = cms.untracked.vstring(inlist.readlines()),
  duplicateCheckMode = cms.untracked.string ("noDuplicateCheck")
)




process.load("SexaQAnalysis.AnalyzerAllSteps.FlatTreeProducerGEN_cfi")
process.FlatTreeProducerGEN.runningOnData = runningOnData
process.FlatTreeProducerGEN.lookAtAntiS = lookAtAntiS
process.flattreeproducer = cms.Path(process.FlatTreeProducerGEN)

process.p = cms.Schedule(
  process.flattreeproducer
)


# Output
process.TFileService = cms.Service('TFileService',
#    fileName = cms.string(options.outputFile)
#    fileName = cms.string('MCSbar_Trial1_1p7GeV.root')
#    fileName = cms.string('MCSbar_Trial6_1p8GeV.root')
#    fileName = cms.string('MCSbar_Trial1_1p85GeV.root')
#    fileName = cms.string('MCSbar_Trial1_1p9GeV.root')
#    fileName = cms.string('MCSbar_Trial1_2GeV.root')

#    fileName = cms.string('NoEtaCut_1p7GeV.root')
#    fileName = cms.string('NoEtaCut_1p8GeV.root')
#    fileName = cms.string('NoEtaCut_1p85GeV.root')
#    fileName = cms.string('NoEtaCut_1p9GeV.root')
    fileName = cms.string('NoEtaCut_2GeV.root')
)


#Keep edm output file --> used in the analyzer
#process.out = cms.OutputModule("PoolOutputModule",
#  outputCommands = cms.untracked.vstring(
#     'keep *'
#  ),
#   fileName = cms.untracked.string("AOD_test_matchingHits.root"),
# # SelectEvents = cms.untracked.PSet(  SelectEvents = cms.vstring('p') )
#)

#process.output_step = cms.EndPath(process.out)

