import FWCore.ParameterSet.Config as cms

lambdaKshortVertexFilter = cms.EDFilter(
    'LambdaKshortVertexFilter',
    lambdaCollection = cms.InputTag("generalV0Candidates","Lambda"),
    kshortCollection = cms.InputTag("generalV0Candidates","Kshort"),
    genparticlesCollection = cms.InputTag("genParticles",""), 
    #beamspot = cms.InputTag("offlineBeamSpot"),
    #offlinePV = cms.InputTag("offlinePrimaryVertices", "", ""),
    maxchi2ndofVertexFit = cms.double(10.)
    #isData = cms.bool(True),
    #doInitialPreselection = cms.bool(True),
    #doAdditionalPreselection = cms.bool(True),
    ##Initial Preselection Parameters
    #minDeltaPhi_LambdaKshort = cms.double(0.4),
    #minLxy_SInteractionToBPC = cms.double(2.02),
    #maxLxy_SInteractionToBPC = cms.double(2.4),
    #minDxyOverLxy_SInteractionToBeamspot = cms.double(0.0),
    #maxDxyOverLxy_SInteractionToBeamspot = cms.double(0.5),
    ##Additional Preselection Parameters
    #maxVzInteraction_S = cms.double(28.0),
    #maxDeltaEta_LambdaKs = cms.double(2.0),
    #minOpeningsAngle_LambdaKs = cms.double(0.4),
    #maxOpeningsAngle_LambdaKs = cms.double(2.0),
    #minOpeningsAngle_SKshort = cms.double(0.1),
    #maxOpeningsAngle_SKshort = cms.double(1.8),
    #minOpeningsAngle_SLambda = cms.double(0.05),
    #maxOpeningsAngle_SLambda = cms.double(1.0),
    #maxEta_S = cms.double(3.5),
    #maxDzmin_S = cms.double(6.),
    #maxEta_Kshort = cms.double(2.5),
    #minPT_Kshort = cms.double(0.8)
)
