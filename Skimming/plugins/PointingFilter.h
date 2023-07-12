#ifndef PointingFilter_h
#define PointingFilter_h
 
#include "SexaQAnalysis/AnalyzerAllSteps/interface/AnalyzerAllSteps.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EDFilter.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"

#include "DataFormats/Candidate/interface/VertexCompositeCandidate.h"
#include "DataFormats/Candidate/interface/VertexCompositeCandidateFwd.h"
#include "DataFormats/Candidate/interface/Particle.h"
#include "DataFormats/Candidate/interface/VertexCompositePtrCandidate.h"
#include "DataFormats/Candidate/interface/Candidate.h"
#include <vector>
//#include "FWCore/ServiceRegistry/interface/Service.h"

class PointingFilter: public edm::EDFilter {

  public:

    explicit PointingFilter(edm::ParameterSet const& cfg);
    virtual ~PointingFilter() {}
    virtual bool filter(edm::Event & iEvent, edm::EventSetup const & iSetup);
 private:

    //edm::InputTag genCollectionTag_;
    edm::InputTag sCollectionTag_;
    edm::InputTag bsCollectionTag_;
    
    edm::EDGetTokenT<vector<reco::VertexCompositeCandidate> > sCollectionToken_;
    edm::EDGetTokenT<reco::BeamSpot> bsCollectionToken_;
    //edm::EDGetTokenT<std::vector<reco::GenParticle>> genCollectionToken_;

    bool IncludeXevt_S_;
    double minDxyOverLxy_SInteractionToBeamspot_, maxDxyOverLxy_SInteractionToBeamspot_;

};


#endif
