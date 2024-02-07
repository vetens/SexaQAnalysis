import FWCore.ParameterSet.Config as cms

lambdaKshortXevtVertexFilter = cms.EDFilter(
    'LambdaKshortXevtVertexFilter',
    lambdaCollection = cms.InputTag("generalV0Candidates","Lambda"),
    kshortCollection = cms.InputTag("generalV0Candidates","Kshort"),
    genparticlesCollection = cms.InputTag("genParticles",""), 
    maxchi2ndofVertexFit = cms.double(10.)
)
