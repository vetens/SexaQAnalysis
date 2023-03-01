import FWCore.ParameterSet.Config as cms
#from Validation.RecoTrack.TrackingParticleSelectionForEfficiency_cfi import * 
#from SimTracker.TrackAssociation.LhcParametersDefinerForTP_cfi import * 
PileUpScraper = cms.EDAnalyzer('PileUpScraper',
    runningOnData = cms.untracked.bool(False),
    offlinePV = cms.InputTag("offlinePrimaryVertices", "", "")
)
