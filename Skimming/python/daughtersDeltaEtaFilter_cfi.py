import FWCore.ParameterSet.Config as cms

daughtersDeltaEtaFilter = cms.EDFilter(
    'daughtersDeltaEtaFilter',
    sexaqCandidates = cms.InputTag("lambdaKshortVertexFilter","sParticles", ""),
    maxDeltaEta_LambdaKs = cms.double(2.0)
)
