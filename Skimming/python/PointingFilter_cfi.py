import FWCore.ParameterSet.Config as cms

PointingFilter = cms.EDFilter(
    'PointingFilter',
    sexaqCandidates = cms.InputTag("lambdaKshortVertexFilter","sParticles", ""),
    beamspot = cms.InputTag("offlineBeamSpot"),
    minDxyOverLxy_SInteractionToBeamspot = cms.double(0.0),
    maxDxyOverLxy_SInteractionToBeamspot = cms.double(0.5)
)
