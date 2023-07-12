#include "daughtersDeltaOpeningsAngleFilter.h"
using namespace reco;
using namespace edm;
using namespace std;

daughtersDeltaOpeningsAngleFilter::daughtersDeltaOpeningsAngleFilter(edm::ParameterSet const& pset):
  //collections
  sCollectionTag_               (pset.getParameter<edm::InputTag>("sexaqCandidates")),
  //parameters
  //Initial Preselection parameters
  minOpeningsAngle_LambdaKs_    (pset.getParameter<double>("minOpeningsAngle_LambdaKs")),
  maxOpeningsAngle_LambdaKs_    (pset.getParameter<double>("maxOpeningsAngle_LambdaKs"))
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
bool daughtersDeltaOpeningsAngleFilter::filter(edm::Event & iEvent, edm::EventSetup const & iSetup)
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
    const Candidate * Lambda = S->daughter(0);
    const Candidate * Ks = S->daughter(1);

    reco::Candidate::Vector Lambda_p(Lambda->px(), Lambda->py(), Lambda->pz());

    reco::Candidate::Vector Kshort_p(Ks->px(), Ks->py(), Ks->pz());
    if(S->vertexNdof() != 999.){
        if ( ( AnalyzerAllSteps::openings_angle(Lambda_p,Kshort_p) > minOpeningsAngle_LambdaKs_ )
          && ( AnalyzerAllSteps::openings_angle(Lambda_p,Kshort_p) < maxOpeningsAngle_LambdaKs_ )
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
DEFINE_FWK_MODULE(daughtersDeltaOpeningsAngleFilter);
