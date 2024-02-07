import FWCore.ParameterSet.Config as cms

SLambdaDeltaOpeningsAngleFilter = cms.EDFilter(
    'SLambdaDeltaOpeningsAngleFilter',
    sexaqCandidates = cms.InputTag("lambdaKshortVertexFilter","sParticles", ""),
    minOpeningsAngle_SLambda = cms.double(0.05),
    maxOpeningsAngle_SLambda = cms.double(1.0)
)
