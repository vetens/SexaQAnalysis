import FWCore.ParameterSet.Config as cms

vzFilter = cms.EDFilter(
    'vzFilter',
    sexaqCandidates = cms.InputTag("lambdaKshortVertexFilter","sParticles", ""),
    beamspot = cms.InputTag("offlineBeamSpot"),
    maxVzInteraction_S = cms.double(28.0)
)
