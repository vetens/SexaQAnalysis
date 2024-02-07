import FWCore.ParameterSet.Config as cms

mindzFilter = cms.EDFilter(
    'mindzFilter',
    sexaqCandidates = cms.InputTag("lambdaKshortVertexFilter","sParticles", ""),
    offlinePV = cms.InputTag("offlinePrimaryVertices", "", ""),
    maxDzmin_S = cms.double(6.)
)
