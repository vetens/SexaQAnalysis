import FWCore.ParameterSet.Config as cms

FiducialCuts = cms.EDFilter(
    'FiducialCuts',
    lambdaCollection = cms.InputTag("LambdaKshortFilter","Lambda"),
    kshortCollection = cms.InputTag("LambdaKshortFilter","Kshort"),
    #genCollection    = cms.InputTag("genCollection"),
    #genCollection = cms.InputTag("genParticles","","HLT"),
    beamspot = cms.InputTag("offlineBeamSpot"),
    offlinePV = cms.InputTag("offlinePrimaryVertices", "", ""),
    #isData = cms.bool(True),
    doFiducialCuts = cms.bool(True),
    minNrLambda = cms.uint32(1),
    minNrKshort = cms.uint32(1),
    minPtLambda = cms.double(0),
    minPtKshort = cms.double(0),
    maxEtaLambda = cms.double(99999), #no eta cut any more
    maxEtaKshort = cms.double(99999), #no eta cut any more
    minMassLambda = cms.double(1.106), # -3sigma arXiv:1102.4282
    minMassKshort = cms.double(0.473), # +3sigma arXiv:1102.4282
    maxMassLambda = cms.double(1.126), # -3sigma arXiv:1102.4282
    maxMassKshort = cms.double(0.522), # +3sigma arXiv:1102.4282
    #Fiducial Cuts
    maxVzDecayLambda = cms.double(125),
    maxVzDecayKshort = cms.double(125),
    maxLxyDecayLambda = cms.double(44.5),
    maxLxyDecayKshort = cms.double(44.5),
    minPTLambdaDau0 = cms.double(0.33),
    minPTLambdaDau1 = cms.double(0.33),
    minPTKshortDau0 = cms.double(0.33),
    minPTKshortDau1 = cms.double(0.33),
    maxPzLambdaDau0 = cms.double(22),
    maxPzLambdaDau1 = cms.double(22),
    maxPzKshortDau0 = cms.double(22),
    maxPzKshortDau1 = cms.double(22),
    minD0xyBeamspotLambdaDau0 = cms.double(0),
    minD0xyBeamspotLambdaDau1 = cms.double(0),
    minD0xyBeamspotKshortDau0 = cms.double(0),
    minD0xyBeamspotKshortDau1 = cms.double(0),
    maxD0xyBeamspotLambdaDau0 = cms.double(9.5),
    maxD0xyBeamspotLambdaDau1 = cms.double(9.5),
    maxD0xyBeamspotKshortDau0 = cms.double(9.5),
    maxD0xyBeamspotKshortDau1 = cms.double(9.5),
    maxDzMinPVLambdaDau0 = cms.double(27),
    maxDzMinPVLambdaDau1 = cms.double(27),
    maxDzMinPVKshortDau0 = cms.double(27),
    maxDzMinPVKshortDau1 = cms.double(27),
    #checkLambdaDaughters = cms.bool(False),
    prescaleFalse = cms.uint32(0) # 0 means no prescale, reject all
)
