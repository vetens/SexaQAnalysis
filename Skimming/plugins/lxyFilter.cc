#include "lxyFilter.h"
using namespace reco;
using namespace edm;
using namespace std;

lxyFilter::lxyFilter(edm::ParameterSet const& pset):
  //collections
  sCollectionTag_               (pset.getParameter<edm::InputTag>("sexaqCandidates")),
  isData_        	        (pset.getParameter<bool>("isData")),
  //parameters
  //Initial Preselection parameters
  minLxy_SInteractionToBPC_     (pset.getParameter<double>("minLxy_SInteractionToBPC")),
  maxLxy_SInteractionToBPC_     (pset.getParameter<double>("maxLxy_SInteractionToBPC"))
{
  //collections
  sCollectionToken_ = consumes<vector<reco::VertexCompositeCandidate> >(sCollectionTag_);
  //genCollectionToken_    = consumes<std::vector<reco::GenParticle> > (genCollectionTag_);
  //producer
  produces<std::vector<reco::VertexCompositeCandidate> >("sParticles");
  //the reconstruction of X events S and Sbar is disabled for now as it was giving a mysterious seg violation
  //  produces<std::vector<reco::VertexCompositeCandidate> >("sParticlesXEvent");

}


//the filter
bool lxyFilter::filter(edm::Event & iEvent, edm::EventSetup const & iSetup)
{ 

  //these are for the producer
  auto sParticles = std::make_unique<std::vector<reco::VertexCompositeCandidate> >();
  //auto sParticlesXEvent = std::make_unique<std::vector<reco::VertexCompositeCandidate> >();


  // collections
  edm::Handle<vector<reco::VertexCompositeCandidate> > h_sCands;
  iEvent.getByToken(sCollectionToken_ , h_sCands);
 
  //check all the above collections and return false if any of them is invalid
  if (!h_sCands.isValid()) return false;

  for(unsigned int s = 0; s < h_sCands->size(); ++s){
    const VertexCompositeCandidate * S = &h_sCands->at(s);

    if(S->vertexNdof() != 999.){
        TVector3 BeamPipeCenter(AnalyzerAllSteps::center_beampipe_x, AnalyzerAllSteps::center_beampipe_y, 0);
        if (!isData_) {BeamPipeCenter.SetXYZ(0, 0, 0);}
        if (  ( sqrt(pow(S->vx() - BeamPipeCenter.X(),2) + pow(S->vy() - BeamPipeCenter.Y(),2)) > minLxy_SInteractionToBPC_ )
           && ( sqrt(pow(S->vx() - BeamPipeCenter.X(),2) + pow(S->vy() - BeamPipeCenter.Y(),2)) < maxLxy_SInteractionToBPC_ )
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
DEFINE_FWK_MODULE(lxyFilter);
