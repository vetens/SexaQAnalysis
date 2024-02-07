import FWCore.ParameterSet.Config as cms

lxyFilter = cms.EDFilter(
    'lxyFilter',
    sexaqCandidates = cms.InputTag("lambdaKshortVertexFilter","sParticles", ""),
    isData = cms.bool(True),
    minLxy_SInteractionToBPC = cms.double(2.02),
    maxLxy_SInteractionToBPC = cms.double(2.4)
)
