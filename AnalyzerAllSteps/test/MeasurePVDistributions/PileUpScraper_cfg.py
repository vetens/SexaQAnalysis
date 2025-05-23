import sys
import FWCore.ParameterSet.Config as cms
from FWCore.ParameterSet.VarParsing import VarParsing

runningOnData = False#important, because this will choose rather to calculate lxy of the antiS interaction vertex wrt  (0,0) (for MC) or wrt the location of the center of the beampipe (for data)
#runningOnData = True#important, because this will choose rather to calculate lxy of the antiS interaction vertex wrt  (0,0) (for MC) or wrt the location of the center of the beampipe (for data)
lookAtAntiS =   True 
#lookAtAntiS =   False 

options = VarParsing ('analysis')
options.parseArguments()
## data or MC options
options.register(
	'isData',True,VarParsing.multiplicity.singleton,VarParsing.varType.bool,
	'flag to indicate data or MC')

options.register(
	'maxEvts',-1,VarParsing.multiplicity.singleton,VarParsing.varType.int,
	#'maxEvts',1000,VarParsing.multiplicity.singleton,VarParsing.varType.int,
	'flag to indicate max events to process')
	
options.isData==False

process = cms.Process("SEXAQDATAANA")
process.load("FWCore.MessageService.MessageLogger_cfi")
process.load("FWCore.Modules.preScaler_cfi")
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.load('Configuration/StandardSequences/MagneticField_38T_cff')
process.load('Configuration/StandardSequences/Reconstruction_cff')
process.load('Configuration/EventContent/EventContent_cff')

from Configuration.AlCa.GlobalTag import GlobalTag

if(options.isData==True):
    #process.GlobalTag = GlobalTag(process.GlobalTag, '106X_dataRun2_v35', '') 
    process.GlobalTag = GlobalTag(process.GlobalTag, '80X_dataRun2_2016SeptRepro_v7', '') 
    # we are using 106X_dataRun2_v35 GlobalTag because it is what was used for the B-parking rereco according to: https://cms-pdmv.cern.ch/rereco/api/requests/get_cmsdriver/ReReco-Run2018D-ParkingBPH2-20Jun2021_UL2018-00002
    #using a different GlobalTag for data when running on MC because the 106X globaltag seems to have some issues with CMSSW_10_2_X...
else:
    process.GlobalTag = GlobalTag(process.GlobalTag, '102X_upgrade2018_realistic_v15', '')

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(options.maxEvts))
process.MessageLogger.cerr.FwkReport.reportEvery = cms.untracked.int32(1000)
process.preScaler.prescaleFactor = cms.int32(1)
process.options = cms.untracked.PSet(wantSummary = cms.untracked.bool(True))

inlist = open("SbarSignal_NoSelection_NoReconstruction.txt", "r")
process.source = cms.Source("PoolSource",
        fileNames = cms.untracked.vstring(*(inlist.readlines())),
	#fileNames = cms.untracked.vstring(options.inputFiles),
  duplicateCheckMode = cms.untracked.string ("noDuplicateCheck")
)




process.load("SexaQAnalysis.AnalyzerAllSteps.PileUpScraper_cfi")
process.PileUpScraper.runningOnData = runningOnData
process.pileupscraper= cms.Path(process.PileUpScraper)

process.p = cms.Schedule(
  process.pileupscraper
)


# Output
process.TFileService = cms.Service('TFileService',
    fileName = cms.string(options.outputFile)
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

