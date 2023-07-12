#ifndef LambdaKshortFilter_h
#define LambdaKshortFilter_h
 
#include "SexaQAnalysis/AnalyzerAllSteps/interface/AnalyzerAllSteps.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EDFilter.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"

#include "DataFormats/Candidate/interface/VertexCompositeCandidate.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"

#include <vector>

  
class LambdaKshortFilter : public edm::EDFilter {

  public:

    explicit LambdaKshortFilter(edm::ParameterSet const& cfg);
    virtual ~LambdaKshortFilter() {}
    virtual bool filter(edm::Event & iEvent, edm::EventSetup const & iSetup);

  private:
  
    edm::InputTag lambdaCollectionTag_;
    edm::InputTag kshortCollectionTag_;
    edm::InputTag genCollectionTag_;
    //edm::InputTag bsCollectionTag_;
    //edm::InputTag PVCollectionTag_;
    edm::EDGetTokenT<std::vector<reco::VertexCompositeCandidate> > lambdaCollectionToken_;
    edm::EDGetTokenT<std::vector<reco::VertexCompositeCandidate> > kshortCollectionToken_;
    edm::EDGetTokenT<std::vector<reco::GenParticle> >              genCollectionToken_;
    //edm::EDGetTokenT<reco::BeamSpot>                               bsCollectionToken_;
    //edm::EDGetTokenT<std::vector<reco::Vertex> >                   PVCollectionToken_;
    bool isData_;
//    bool doFiducialCuts_;
    unsigned int minNrLambda_,   minNrKshort_;
    double       minPtLambda_,   minPtKshort_;
    double       maxEtaLambda_,  maxEtaKshort_;
    double       minMassLambda_, minMassKshort_;
    double       maxMassLambda_, maxMassKshort_;
    bool checkLambdaDaughters_;
    ////Fiducial Cuts
    //double maxVzDecayLambda_;
    //double maxVzDecayKshort_;
    //double maxLxyDecayLambda_;
    //double maxLxyDecayKshort_;
    //double minPTLambdaDau0_;
    //double minPTLambdaDau1_;
    //double minPTKshortDau0_;
    //double minPTKshortDau1_;
    //double maxPzLambdaDau0_;
    //double maxPzLambdaDau1_;
    //double maxPzKshortDau0_;
    //double maxPzKshortDau1_;
    //double minD0xyBeamspotLambdaDau0_;
    //double minD0xyBeamspotLambdaDau1_;
    //double minD0xyBeamspotKshortDau0_;
    //double minD0xyBeamspotKshortDau1_;
    //double maxD0xyBeamspotLambdaDau0_;
    //double maxD0xyBeamspotLambdaDau1_;
    //double maxD0xyBeamspotKshortDau0_;
    //double maxD0xyBeamspotKshortDau1_;
    //double maxDzMinPVLambdaDau0_;
    //double maxDzMinPVLambdaDau1_;
    //double maxDzMinPVKshortDau0_;
    //double maxDzMinPVKshortDau1_;
    unsigned int prescaleFalse_, nreject_;

};


#endif
