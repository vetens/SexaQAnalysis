#include "PointingFilter.h"
using namespace reco;
using namespace edm;
using namespace std;

PointingFilter::PointingFilter(edm::ParameterSet const& pset):
  //collections
  sCollectionTag_               (pset.getParameter<edm::InputTag>("sexaqCandidates")),
  bsCollectionTag_  		(pset.getParameter<edm::InputTag>("beamspot")),
  //parameters
  minDxyOverLxy_SInteractionToBeamspot_(pset.getParameter<double>("minDxyOverLxy_SInteractionToBeamspot")),
  maxDxyOverLxy_SInteractionToBeamspot_(pset.getParameter<double>("maxDxyOverLxy_SInteractionToBeamspot"))
{
  //collections
  sCollectionToken_ = consumes<vector<reco::VertexCompositeCandidate> >(sCollectionTag_);
  bsCollectionToken_    = consumes<reco::BeamSpot> (bsCollectionTag_);
  //genCollectionToken_    = consumes<std::vector<reco::GenParticle> > (genCollectionTag_);
  //producer
  produces<std::vector<reco::VertexCompositeCandidate> >("sParticles");
  //the reconstruction of X events S and Sbar is disabled for now as it was giving a mysterious seg violation
  //  produces<std::vector<reco::VertexCompositeCandidate> >("sParticlesXEvent");

}


//the filter
bool PointingFilter::filter(edm::Event & iEvent, edm::EventSetup const & iSetup)
{ 

  //these are for the producer
  auto sParticles = std::make_unique<std::vector<reco::VertexCompositeCandidate> >();
  //auto sParticlesXEvent = std::make_unique<std::vector<reco::VertexCompositeCandidate> >();


  // collections
  edm::Handle<vector<reco::VertexCompositeCandidate> > h_sCands;
  iEvent.getByToken(sCollectionToken_ , h_sCands);
  edm::Handle<reco::BeamSpot> h_bs;
  iEvent.getByToken(bsCollectionToken_ , h_bs);
  //check all the above collections and return false if any of them is invalid
  if (!h_sCands.isValid()) return false;
  if (!h_bs.isValid()) return false;
  TVector3 beamspot(h_bs->x0(), h_bs->y0(), h_bs->z0());

  for(unsigned int s = 0; s < h_sCands->size(); ++s){
    const VertexCompositeCandidate * S = &h_sCands->at(s);

    TVector3 T_SMomentum(S->px(), S->py(), S->pz());
    TVector3 SInteractionVertex(S->vx(), S->vy(), S->vz());
    if(S->vertexNdof() != 999.){
        if ( (AnalyzerAllSteps::dxy_signed_line_point(SInteractionVertex, T_SMomentum, beamspot) / AnalyzerAllSteps::lxy(beamspot, SInteractionVertex) < maxDxyOverLxy_SInteractionToBeamspot_) &&
             (AnalyzerAllSteps::dxy_signed_line_point(SInteractionVertex, T_SMomentum, beamspot) / AnalyzerAllSteps::lxy(beamspot, SInteractionVertex) > minDxyOverLxy_SInteractionToBeamspot_) ) {
          sParticles->push_back(std::move(*S)); 
        }
      }
  }
  int ns = sParticles->size();
  iEvent.put(std::move(sParticles),"sParticles"); 
  return (ns > 0);

}//end filter
#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(PointingFilter);
