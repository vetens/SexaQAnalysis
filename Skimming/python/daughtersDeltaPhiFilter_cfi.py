import FWCore.ParameterSet.Config as cms

daughtersDeltaPhiFilter = cms.EDFilter(
    'daughtersDeltaPhiFilter',
    sexaqCandidates = cms.InputTag("lambdaKshortVertexFilter","sParticles", ""),
    minDeltaPhi_LambdaKshort = cms.double(0.4)
)
