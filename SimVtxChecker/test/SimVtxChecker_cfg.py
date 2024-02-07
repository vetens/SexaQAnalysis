import FWCore.ParameterSet.Config as cms
from FWCore.ParameterSet.VarParsing import VarParsing


options = VarParsing('analysis')
options.parseArguments()
options.register(
        'maxEvts',-1,VarParsing.multiplicity.singleton,VarParsing.varType.int,
        'flag to indicate max events to process')
# Set up a process, named RECO in this case
process = cms.Process("SIMVTXCHECK")
process.load("FWCore.MessageService.MessageLogger_cfi")
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.load('Configuration/StandardSequences/MagneticField_38T_cff')
process.load('Configuration/StandardSequences/Reconstruction_cff')
process.load('Configuration/EventContent/EventContent_cff')
process.load("SexaQAnalysis.SimVtxChecker.SimVtxChecker_cfi")

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(options.maxEvts))
process.MessageLogger.cerr.FwkReport.reportEvery = cms.untracked.int32(1)
process.options = cms.untracked.PSet(wantSummary = cms.untracked.bool(True))

# Configure the object that reads the input file
inlist = open("GenSimList_Trial4_MultiSQEV.txt", "r")
#inlist = open("GenSimList_Trial4_MultiSQEV_test.txt", "r")
#inlist = open("GenSimList_Jarne_test.txt", "r")
process.source = cms.Source("PoolSource", 
    #fileNames = cms.untracked.vstring("test.root")
    fileNames = cms.untracked.vstring(*(inlist.readlines())),
    duplicateCheckMode = cms.untracked.string ("noDuplicateCheck")
)
process.p = cms.Path(process.SimVtxChecker)
# Configure the object that writes an output file
process.TFileService = cms.Service("TFileService",
    fileName = cms.string(options.outputFile)
)

# Add the contents of Foo.Bar.somefile_cff to the process
# Note that more commonly in CMS, we call process.load(Foo.Bar.somefile_cff)
# which both performs the import and calls extend.

# Configure a path and endpath to run the producer and output modules
#process.ep = cms.EndPath(process.out)
