import FWCore.ParameterSet.Config as cms

from RecoVertex.V0Producer.generalV0Candidates_cff import *
### CMSSW command line parameter parser
from FWCore.ParameterSet.VarParsing import VarParsing
options = VarParsing('python')

collections_to_keep = cms.untracked.vstring(
    'drop *',
    'keep *_InitialProducer_*_*',
    'keep recoVertexs_offlinePrimaryVertices_*_*',
    'keep recoBeamSpot_offlineBeamSpot_*_*',
    'keep *_genParticles_*_HLT',
    'keep recoVertexCompositeCandidates_generalV0Candidates_*_*',
    'keep recoTracks_lambdaKshortVertexFilter_sParticlesTracks_*',
    'keep recoVertexCompositePtrCandidates_rMassFilter_sVertexCompositePtrCandidate_*',
    'keep recoVertexCompositePtrCandidates_sMassFilter_sVertexCompositePtrCandidate_*',
    'keep *_*_*_SEXAQ',
#dropping collections from intermediate filter steps
    'drop *_*_sParticles_*',
    'drop *_*_sParticlesXEvent_*',
    'keep *_sMassFilter_sParticles_*',
    'keep *_sMassFilter_sParticlesXEvent_*',
##Following two kept in Signal MC, but not originally here, so I will add them for now
    'keep *_lambdaKshortVertexFilter_sParticles_*',
    'keep *_lambdaKshortXevtVertexFilter_sParticlesXEvent_*',
    'keep *_offlinePrimaryVertices_*_*',
##Following two seem to be asked about by something, as I get an error without them
#    'keep *_pfIsolatedElectronsEI_*_*',
#    'keep *_pfIsolatedMuonsEI_*_*',
##the above two no longer seem to be in the EDM info for data..... strange, but I will try something which is of the same datatype since the muons and electrons don't actually seem to be used anywhere...
    'keep *_particleFlowPtrs_*_*',
    'keep *_particleFlowPtrs_*_*',
##
    "keep *_genParticlesPlusGEANT_*_*",
#    "keep *_g4SimHits_*_*",
    "keep *_simSiPixelDigis_*_*",
#    "keep *_simMuonRPCDigis_*_*",
    "keep *_simSiStripDigis_*_*",
    "keep *_mix_MergedTrackTruth_*",
#    "keep *_siPixelDigis_*_*",
#    "keep *_siStripDigis_*_*",
#    "keep *_siStripDigis_*_*",
    "keep *_siPixelClusters_*_*",
    "keep *_siStripClusters_*_*",
    "keep *_generalTracks_*_*"
  )



## data or MC options
options.register(
	'isData',True,VarParsing.multiplicity.singleton,VarParsing.varType.bool,
	'flag to indicate data or MC')

options.register(
	'maxEvts',-1,VarParsing.multiplicity.singleton,VarParsing.varType.int,
	#'maxEvts',1000,VarParsing.multiplicity.singleton,VarParsing.varType.int,
	'flag to indicate max events to process')


process = cms.Process("SEXAQ")

process.load("FWCore.MessageService.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = cms.untracked.int32(10000)
process.options = cms.untracked.PSet(wantSummary = cms.untracked.bool(True))

process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")

process.load('Configuration/StandardSequences/MagneticField_cff')
process.load('Configuration/StandardSequences/Reconstruction_cff')
process.load('Configuration/EventContent/EventContent_cff')

from Configuration.AlCa.GlobalTag import GlobalTag

if(options.isData==True):
    process.GlobalTag = GlobalTag(process.GlobalTag, '106X_dataRun2_v35', '') #was using 80X_dataRun2_2016SeptRepro_v7 before trialM, now changed to this one according to: https://twiki.cern.ch/twiki/bin/viewauth/CMS/PdmVAnalysisSummaryTable
else:
    process.GlobalTag = GlobalTag(process.GlobalTag, '102X_upgrade2018_realistic_v15', '')


process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(options.maxEvts))


#inlist = open("testDataFiles.txt", "r")
process.source = cms.Source("PoolSource",
        fileNames = cms.untracked.vstring(options.inputFiles),
#        fileNames = cms.untracked.vstring(*(inlist.readlines())),
  duplicateCheckMode = cms.untracked.string ("noDuplicateCheck")
)


process.nEvTotal                = cms.EDProducer("EventCountProducer")
process.nEvLambdaKshort         = cms.EDProducer("EventCountProducer")
process.nEvLambdaKshortVertex   = cms.EDProducer("EventCountProducer")
process.nEvFiducial             = cms.EDProducer("EventCountProducer")
process.nEvSdauDeltaPhi         = cms.EDProducer("EventCountProducer")
process.nEvlxy                  = cms.EDProducer("EventCountProducer")
process.nEvPointing             = cms.EDProducer("EventCountProducer")
process.nEvVz                   = cms.EDProducer("EventCountProducer")
process.nEvSdauDeltaEta         = cms.EDProducer("EventCountProducer")
process.nEvSdauDeltaOpe         = cms.EDProducer("EventCountProducer")
process.nEvSKsDeltaOpe          = cms.EDProducer("EventCountProducer")
process.nEvSLambdaDeltaOpe      = cms.EDProducer("EventCountProducer")
process.nEvEta                  = cms.EDProducer("EventCountProducer")
process.nEvMinDz                = cms.EDProducer("EventCountProducer")
process.nEvKsEta                = cms.EDProducer("EventCountProducer")
process.nEvKsPt                 = cms.EDProducer("EventCountProducer")
process.nEvSMass                = cms.EDProducer("EventCountProducer")

process.genParticlePlusGEANT = cms.EDProducer("GenPlusSimParticleProducer",
  src           = cms.InputTag("g4SimHits"),
  setStatus     = cms.int32(8),                # set status = 8 for GEANT GPs
  particleTypes = cms.vstring("Xi-","Xibar+","Lambda0","Lambdabar0","K_S0","K0"),      # also picks pi- (optional)
  filter        = cms.vstring("pt >= 0.0"),     # just for testing
  genParticles  = cms.InputTag("genParticles") # original genParticle list
)

process.load("RecoVertex.V0Producer.generalV0Candidates_cfi")
process.generalV0Candidates.innerHitPosCut = -1
process.generalV0Candidates.cosThetaXYCut = -1
process.generalV0Candidates.kShortMassCut = 0.03
process.generalV0Candidates.lambdaMassCut = 0.015

process.load("SexaQAnalysis.Skimming.LambdaKshortFilter_cfi")
process.lambdaKshortFilter.genCollection = cms.InputTag("genParticlePlusGEANT")
process.lambdaKshortFilter.isData = True
process.lambdaKshortFilter.minPtLambda = 0. 
process.lambdaKshortFilter.minPtKshort = 0. 
process.lambdaKshortFilter.checkLambdaDaughters = True
process.lambdaKshortFilter.prescaleFalse = 0

#Fiducial Cuts:
process.load("SexaQAnalysis.Skimming.FiducialCuts_cfi")
process.FiducialCuts.lambdaCollection = cms.InputTag("generalV0Candidates","Lambda")
process.FiducialCuts.kshortCollection = cms.InputTag("generalV0Candidates","Kshort")
process.FiducialCuts.maxVzDecayLambda = 125.
process.FiducialCuts.maxVzDecayKshort = 125.
process.FiducialCuts.maxLxyDecayLambda = 44.5
process.FiducialCuts.maxLxyDecayKshort = 44.5
process.FiducialCuts.minPTLambdaDau0 = 0.33
process.FiducialCuts.minPTLambdaDau1 = 0.33
process.FiducialCuts.minPTKshortDau0 = 0.33
process.FiducialCuts.minPTKshortDau1 = 0.33
process.FiducialCuts.maxPzLambdaDau0 = 22.
process.FiducialCuts.maxPzLambdaDau1 = 22.
process.FiducialCuts.maxPzKshortDau0 = 22.
process.FiducialCuts.maxPzKshortDau1 = 22.
process.FiducialCuts.minD0xyBeamspotLambdaDau0 = 0.
process.FiducialCuts.minD0xyBeamspotLambdaDau1 = 0.
process.FiducialCuts.minD0xyBeamspotKshortDau0 = 0.
process.FiducialCuts.minD0xyBeamspotKshortDau1 = 0.
process.FiducialCuts.maxD0xyBeamspotLambdaDau0 = 9.5
process.FiducialCuts.maxD0xyBeamspotLambdaDau1 = 9.5
process.FiducialCuts.maxD0xyBeamspotKshortDau0 = 9.5
process.FiducialCuts.maxD0xyBeamspotKshortDau1 = 9.5
process.FiducialCuts.maxDzMinPVLambdaDau0 = 27.
process.FiducialCuts.maxDzMinPVLambdaDau1 = 27.
process.FiducialCuts.maxDzMinPVKshortDau0 = 27.
process.FiducialCuts.maxDzMinPVKshortDau1 = 27.

#Sbar Vertexing
process.load("SexaQAnalysis.Skimming.LambdaKshortXevtVertexFilter_cfi")
process.lambdaKshortXevtVertexFilter.lambdaCollection = cms.InputTag("FiducialCuts","lambda")
process.lambdaKshortXevtVertexFilter.kshortCollection = cms.InputTag("FiducialCuts","kshort")
process.lambdaKshortXevtVertexFilter.maxchi2ndofVertexFit = 10.

#Initial Preselection:
process.load("SexaQAnalysis.Skimming.daughtersDeltaPhiFilter_cfi")
process.daughtersDeltaPhiFilter.sexaqCandidates = cms.InputTag("lambdaKshortXevtVertexFilter","sParticlesXEvent", "")
process.daughtersDeltaPhiFilter.minDeltaPhi_LambdaKshort = 0.4
process.load("SexaQAnalysis.Skimming.lxyFilter_cfi")
process.lxyFilter.sexaqCandidates = cms.InputTag("daughtersDeltaPhiFilter","sParticles", "")
process.lxyFilter.minLxy_SInteractionToBPC = 2.02
process.lxyFilter.maxLxy_SInteractionToBPC = 2.4
process.load("SexaQAnalysis.Skimming.PointingFilter_cfi")
process.PointingFilter.sexaqCandidates = cms.InputTag("lxyFilter","sParticles", "")
process.PointingFilter.minDxyOverLxy_SInteractionToBeamspot = 0.
process.PointingFilter.maxDxyOverLxy_SInteractionToBeamspot = 0.5
#Additional Preselection:
process.load("SexaQAnalysis.Skimming.vzFilter_cfi")
process.vzFilter.sexaqCandidates = cms.InputTag("PointingFilter","sParticles", "")
process.vzFilter.maxVzInteraction_S = 28.
process.load("SexaQAnalysis.Skimming.daughtersDeltaEtaFilter_cfi")
process.daughtersDeltaEtaFilter.sexaqCandidates = cms.InputTag("vzFilter","sParticles", "")
process.daughtersDeltaEtaFilter.maxDeltaEta_LambdaKs = 2.
process.load("SexaQAnalysis.Skimming.daughtersDeltaOpeningsAngleFilter_cfi")
process.daughtersDeltaOpeningsAngleFilter.sexaqCandidates = cms.InputTag("daughtersDeltaEtaFilter","sParticles", "")
process.daughtersDeltaOpeningsAngleFilter.minOpeningsAngle_LambdaKs = 0.4
process.daughtersDeltaOpeningsAngleFilter.maxOpeningsAngle_LambdaKs = 2.
process.load("SexaQAnalysis.Skimming.SKsDeltaOpeningsAngleFilter_cfi")
process.SKsDeltaOpeningsAngleFilter.sexaqCandidates = cms.InputTag("daughtersDeltaOpeningsAngleFilter","sParticles", "")
process.SKsDeltaOpeningsAngleFilter.minOpeningsAngle_SKshort = 0.1
process.SKsDeltaOpeningsAngleFilter.maxOpeningsAngle_SKshort = 1.8
process.load("SexaQAnalysis.Skimming.SLambdaDeltaOpeningsAngleFilter_cfi")
process.SLambdaDeltaOpeningsAngleFilter.sexaqCandidates = cms.InputTag("SKsDeltaOpeningsAngleFilter","sParticles", "")
process.SLambdaDeltaOpeningsAngleFilter.minOpeningsAngle_SLambda = 0.05
process.SLambdaDeltaOpeningsAngleFilter.maxOpeningsAngle_SLambda = 1.0
process.load("SexaQAnalysis.Skimming.EtaFilter_cfi")
process.EtaFilter.sexaqCandidates = cms.InputTag("SLambdaDeltaOpeningsAngleFilter","sParticles", "")
process.EtaFilter.maxEta_S = 3.5
process.load("SexaQAnalysis.Skimming.mindzFilter_cfi")
process.mindzFilter.sexaqCandidates = cms.InputTag("EtaFilter","sParticles", "")
process.mindzFilter.maxDzmin_S = 6.
process.load("SexaQAnalysis.Skimming.KsEtaFilter_cfi")
process.KsEtaFilter.sexaqCandidates = cms.InputTag("mindzFilter","sParticles", "")
process.KsEtaFilter.maxEta_Kshort = 2.5
process.load("SexaQAnalysis.Skimming.KsPtFilter_cfi")
process.KsPtFilter.sexaqCandidates = cms.InputTag("KsEtaFilter","sParticles", "")
process.KsPtFilter.minPT_Kshort = 0.8

from SexaQAnalysis.Skimming.MassFilter_cfi import massFilter
massFilter.lambdakshortCollection = cms.InputTag("KsPtFilter","sParticles", "")
massFilter.minMass = -10000 # effectively no filter
massFilter.maxMass = 10000  # effectively no filter
process.rMassFilter = massFilter.clone()
process.rMassFilter.targetMass = 0
process.sMassFilter = massFilter.clone()
process.sMassFilter.targetMass = 0.939565

process.load("SexaQAnalysis.Skimming.InitialProducer_cfi")

process.load("SexaQAnalysis.TreeProducer.Treeproducer_AOD_cfi")

process.p = cms.Path(
  process.generalV0Candidates* 
  process.tree*
  process.nEvTotal *
  process.InitialProducer * 
  process.lambdaKshortFilter *
  process.nEvLambdaKshort *
  process.FiducialCuts *
  process.nEvFiducial *
  process.lambdaKshortXevtVertexFilter *
  process.nEvLambdaKshortVertex *
  process.daughtersDeltaPhiFilter *
  process.nEvSdauDeltaPhi *
  process.lxyFilter *
  process.nEvlxy *
  process.PointingFilter *
  process.nEvPointing *
  process.vzFilter *
  process.nEvVz *
  process.daughtersDeltaEtaFilter *
  process.nEvSdauDeltaEta *
  process.daughtersDeltaOpeningsAngleFilter *
  process.nEvSdauDeltaOpe *
  process.SKsDeltaOpeningsAngleFilter *
  process.nEvSKsDeltaOpe *
  process.SLambdaDeltaOpeningsAngleFilter *
  process.nEvSLambdaDeltaOpe *
  process.EtaFilter *
  process.nEvEta *
  process.mindzFilter *
  process.nEvMinDz *
  process.KsEtaFilter *
  process.nEvKsEta *
  process.KsPtFilter *
  process.nEvKsPt *
  process.rMassFilter *
  process.sMassFilter *
  process.nEvSMass 
)

# Output --> not used in the analyzer
process.TFileService = cms.Service('TFileService',
    fileName = cms.string('preFilterInfo.root'), 
)

#Keep edm output file --> used in the analyzer
process.out = cms.OutputModule("PoolOutputModule",
  outputCommands = collections_to_keep,
   #fileName = cms.untracked.string("events_skimmed.root"),
   fileName = cms.untracked.string(options.outputFile),
    SelectEvents = cms.untracked.PSet(
    SelectEvents = cms.vstring('p')
  )
)

process.output_step = cms.EndPath(process.out)


#iFileName = "configDump_cfg.py"
#file = open(iFileName,'w')
#file.write(str(process.dumpPython()))
#file.close()
#print process.dumpPython()
