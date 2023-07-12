#ifndef mindzFilter_h
#define mindzFilter_h
 
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

class mindzFilter: public edm::EDFilter {

  public:

    explicit mindzFilter(edm::ParameterSet const& cfg);
    virtual ~mindzFilter() {}
    virtual bool filter(edm::Event & iEvent, edm::EventSetup const & iSetup);
 private:

    //edm::InputTag genCollectionTag_;
    edm::InputTag sCollectionTag_;
    edm::InputTag PVCollectionTag_;
    
    edm::EDGetTokenT<vector<reco::VertexCompositeCandidate> > sCollectionToken_;
    edm::EDGetTokenT<std::vector<reco::Vertex>> PVCollectionToken_;
    //edm::EDGetTokenT<std::vector<reco::GenParticle>> genCollectionToken_;

    bool IncludeXevt_S_;
    double maxDzmin_S_;

};


#endif
