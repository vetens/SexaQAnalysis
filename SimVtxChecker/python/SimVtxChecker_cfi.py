import FWCore.ParameterSet.Config as cms
SimVtxChecker = cms.EDAnalyzer('SimVtxChecker',
      #below should contain all g4SimHits, we are interested specifically in SimTrack and SimVertex
    g4SimHitsCollection =  cms.InputTag("g4SimHits","","SIM"),
)
