import FWCore.ParameterSet.Config as cms

KsEtaFilter = cms.EDFilter(
    'KsEtaFilter',
    sexaqCandidates = cms.InputTag("lambdaKshortVertexFilter","sParticles", ""),
    maxEta_Kshort = cms.double(2.5)
)
