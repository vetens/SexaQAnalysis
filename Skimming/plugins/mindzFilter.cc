#include "mindzFilter.h"
using namespace reco;
using namespace edm;
using namespace std;

mindzFilter::mindzFilter(edm::ParameterSet const& pset):
  //collections
  sCollectionTag_               (pset.getParameter<edm::InputTag>("sexaqCandidates")),
  PVCollectionTag_  		(pset.getParameter<edm::InputTag>("offlinePV")),
  //parameters
  //Initial Preselection parameters
  maxDzmin_S_                   (pset.getParameter<double>("maxDzmin_S"))
{
  //collections
  sCollectionToken_ = consumes<vector<reco::VertexCompositeCandidate> >(sCollectionTag_);
  PVCollectionToken_    = consumes<std::vector<reco::Vertex> > (PVCollectionTag_);
  //genCollectionToken_    = consumes<std::vector<reco::GenParticle> > (genCollectionTag_);
  //producer
  produces<std::vector<reco::VertexCompositeCandidate> >("sParticles");
  //the reconstruction of X events S and Sbar is disabled for now as it was giving a mysterious seg violation
  //  produces<std::vector<reco::VertexCompositeCandidate> >("sParticlesXEvent");

}


//the filter
bool mindzFilter::filter(edm::Event & iEvent, edm::EventSetup const & iSetup)
{ 

  //these are for the producer
  auto sParticles = std::make_unique<std::vector<reco::VertexCompositeCandidate> >();
  //auto sParticlesXEvent = std::make_unique<std::vector<reco::VertexCompositeCandidate> >();


  // collections
  edm::Handle<vector<reco::VertexCompositeCandidate> > h_sCands;
  iEvent.getByToken(sCollectionToken_ , h_sCands);
  edm::Handle<std::vector<reco::Vertex>> h_offlinePV;
  iEvent.getByToken(PVCollectionToken_ , h_offlinePV);
 
  //check all the above collections and return false if any of them is invalid
  if (!h_sCands.isValid()) return false;
  if (!h_offlinePV.isValid()) return false;

  for(unsigned int s = 0; s < h_sCands->size(); ++s){
    const VertexCompositeCandidate * S = &h_sCands->at(s);
    TVector3 SInteractionVertex(S->vx(), S->vy(), S->vz());
    TVector3 T_SMomentum(S->px(), S->py(), S->pz());
    TVector3 bestPVdzAntiS = AnalyzerAllSteps::dz_line_point_min(SInteractionVertex, T_SMomentum, h_offlinePV);
    if(S->vertexNdof() != 999.){
        if ( ( fabs(AnalyzerAllSteps::dz_line_point(SInteractionVertex, T_SMomentum, bestPVdzAntiS)) < maxDzmin_S_ )
          ) {
          sParticles->push_back(std::move(*S)); 
        }
      }
  }
  int ns = sParticles->size();
  iEvent.put(std::move(sParticles),"sParticles"); 
  return (ns > 0);

}//end filter
#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(mindzFilter);
