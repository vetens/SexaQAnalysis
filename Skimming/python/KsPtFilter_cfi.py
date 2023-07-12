import FWCore.ParameterSet.Config as cms

KsPtFilter = cms.EDFilter(
    'KsPtFilter',
    sexaqCandidates = cms.InputTag("lambdaKshortVertexFilter","sParticles", ""),
    minPT_Kshort = cms.double(0.8)
)
