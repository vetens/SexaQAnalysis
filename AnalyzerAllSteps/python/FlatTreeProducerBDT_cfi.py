import FWCore.ParameterSet.Config as cms
from Validation.RecoTrack.TrackingParticleSelectionForEfficiency_cfi import * 
from SimTracker.TrackAssociation.LhcParametersDefinerForTP_cfi import * 
FlatTreeProducerBDT = cms.EDAnalyzer('FlatTreeProducerBDT',
    lookAtAntiS = cms.untracked.bool(False),
    runningOnData = cms.untracked.bool(False),
    beamspot = cms.InputTag("offlineBeamSpot"),
    offlinePV = cms.InputTag("offlinePrimaryVertices","",""),
    genCollection_GEN =  cms.InputTag("genParticles","","GEN"),
    genCollection_SIM_GEANT =  cms.InputTag("genParticlesPlusGEANT","",""),
    generalTracksCollection =  cms.InputTag("generalTracks","","RECO"),
    sexaqCandidates = cms.InputTag("lambdaKshortVertexFilter", "sParticles",""),
    V0KsCollection = cms.InputTag("generalV0Candidates","Kshort",""),
    V0LCollection = cms.InputTag("generalV0Candidates","Lambda",""),
)
