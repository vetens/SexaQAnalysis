import FWCore.ParameterSet.Config as cms

daughtersDeltaOpeningsAngleFilter = cms.EDFilter(
    'daughtersDeltaOpeningsAngleFilter',
    sexaqCandidates = cms.InputTag("lambdaKshortVertexFilter","sParticles", ""),
    minOpeningsAngle_LambdaKs = cms.double(0.4),
    maxOpeningsAngle_LambdaKs = cms.double(2.0)
)
