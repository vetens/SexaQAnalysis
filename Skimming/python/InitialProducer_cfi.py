import FWCore.ParameterSet.Config as cms

InitialProducer = cms.EDProducer(
  'InitialProducer',
  TrackCollection       = cms.InputTag("generalTracks"),
  lambdaCollection = cms.InputTag("generalV0Candidates","Lambda"),
  kshortCollection = cms.InputTag("generalV0Candidates","Kshort"),
  offlinePrimaryVerticesCollection = cms.InputTag("offlinePrimaryVertices"),
  ak4PFJetsCollection = cms.InputTag("ak4PFJets"),
  #The below two collections do not seem to be present in 2018 BPH AODs, so I will try some substitutes
  #muonsCollection = cms.InputTag("pfIsolatedMuonsEI"),
  #electronsCollection = cms.InputTag("pfIsolatedElectronsEI"), 
  # if it turns out that we need muon info I believe it is below. The datatype is an edm::Ptr rather than FwdPtr however from what I can tell, muons and electrons don't actually do anything.
  #muonsCollection = cms.InputTag("particleFlow", "muons"),
  #electronsCollection = cms.InputTag("particleFlow", "electrons"),
  #So instead I will just point them to the one collection which has the same datatype so that I don't have to change anything more hardcoded
  muonsCollection = cms.InputTag("particleFlowPtrs"),
  electronsCollection = cms.InputTag("particleFlowPtrs"), 
  METCollection = cms.InputTag("pfMet"),
  )
