import FWCore.ParameterSet.Config as cms
from Validation.RecoTrack.TrackingParticleSelectionForEfficiency_cfi import * 
from SimTracker.TrackAssociation.LhcParametersDefinerForTP_cfi import * 
FlatTreeProducerTrackerOccupancy= cms.EDAnalyzer('FlatTreeProducerTrackerOccupancy',
    offlinePV = cms.InputTag("offlinePrimaryVertices","",""),
    generalTracksCollection =  cms.InputTag("generalTracks","",""),
    V0KsCollection = cms.InputTag("generalV0Candidates","Kshort",""), #can also be SEXAQ
    V0LCollection = cms.InputTag("generalV0Candidates","Lambda",""), #can also be SEXAQ
    PUReweighting = cms.FileInPath("SexaQAnalysis/AnalyzerAllSteps/data/PU_NoReweigh.txt"),
)
