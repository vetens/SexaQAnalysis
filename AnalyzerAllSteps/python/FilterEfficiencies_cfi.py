import FWCore.ParameterSet.Config as cms

FilterEfficiencies = cms.EDAnalyzer('FilterEfficiencies',
    nEvTotal = cms.InputTag("nEvTotal"),
    nEvLambdaKshort = cms.InputTag("nEvLambdaKshort"),
    nEvFiducial = cms.InputTag("nEvFiducial"),
    nEvLambdaKshortVertex = cms.InputTag("nEvLambdaKshortVertex"),
    nEvSdauDeltaPhi = cms.InputTag("nEvSdauDeltaPhi"),
    nEvlxy = cms.InputTag("nEvlxy"),
    nEvPointing = cms.InputTag("nEvPointing"),
    nEvVz = cms.InputTag("nEvVz"),
    nEvSdauDeltaEta = cms.InputTag("nEvSdauDeltaEta"),
    nEvSdauDeltaOpe = cms.InputTag("nEvSdauDeltaOpe"),
    nEvSKsDeltaOpe = cms.InputTag("nEvSKsDeltaOpe"),
    nEvSLambdaDeltaOpe = cms.InputTag("nEvSLambdaDeltaOpe"),
    nEvEta = cms.InputTag("nEvEta"),
    nEvMinDz = cms.InputTag("nEvMinDz"),
    nEvKsEta = cms.InputTag("nEvKsEta"),
    nEvKsPt = cms.InputTag("nEvKsPt"),
    nEvSMass = cms.InputTag("nEvSMass")
)
