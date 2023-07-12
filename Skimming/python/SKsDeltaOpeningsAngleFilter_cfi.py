import FWCore.ParameterSet.Config as cms

SKsDeltaOpeningsAngleFilter = cms.EDFilter(
    'SKsDeltaOpeningsAngleFilter',
    sexaqCandidates = cms.InputTag("lambdaKshortVertexFilter","sParticles", ""),
    minOpeningsAngle_SKshort = cms.double(0.1),
    maxOpeningsAngle_SKshort = cms.double(1.8)
)
