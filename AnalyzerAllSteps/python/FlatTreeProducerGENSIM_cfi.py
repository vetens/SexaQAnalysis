import FWCore.ParameterSet.Config as cms
from Validation.RecoTrack.TrackingParticleSelectionForEfficiency_cfi import * 
from SimTracker.TrackAssociation.LhcParametersDefinerForTP_cfi import * 
FlatTreeProducerGENSIM = cms.EDAnalyzer('FlatTreeProducerGENSIM',
    lookAtAntiS = cms.untracked.bool(False),
    runningOnData = cms.untracked.bool(False),
    SingleSbarOnly = cms.untracked.bool(False),
    beamspot = cms.InputTag("offlineBeamSpot"),
    offlinePV = cms.InputTag("offlinePrimaryVertices"),
    genCollection_GEN =  cms.InputTag("genParticles","","GEN"),
    genCollection_SIM_GEANT =  cms.InputTag("genParticlesPlusGEANT","","SIM"),
    TrackingParticles = cms.InputTag("mix","MergedTrackTruth"),
    PUReweighting = cms.FileInPath("SexaQAnalysis/AnalyzerAllSteps/data/PU_NoReweigh.txt"),
    MC_MultiToSingleReweighting = cms.FileInPath("SexaQAnalysis/AnalyzerAllSteps/data/MultiToSingleSbar_NoReweigh.txt")
)
