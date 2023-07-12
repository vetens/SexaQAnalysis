import FWCore.ParameterSet.Config as cms

EtaFilter = cms.EDFilter(
    'EtaFilter',
    sexaqCandidates = cms.InputTag("lambdaKshortVertexFilter","sParticles", ""),
    maxEta_S = cms.double(3.5)
)
