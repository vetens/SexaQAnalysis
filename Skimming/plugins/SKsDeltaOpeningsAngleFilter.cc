#include "SKsDeltaOpeningsAngleFilter.h"
using namespace reco;
using namespace edm;
using namespace std;

SKsDeltaOpeningsAngleFilter::SKsDeltaOpeningsAngleFilter(edm::ParameterSet const& pset):
  //collections
  sCollectionTag_               (pset.getParameter<edm::InputTag>("sexaqCandidates")),
  //parameters
  minOpeningsAngle_SKshort_     (pset.getParameter<double>("minOpeningsAngle_SKshort")),
  maxOpeningsAngle_SKshort_     (pset.getParameter<double>("maxOpeningsAngle_SKshort"))
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
bool SKsDeltaOpeningsAngleFilter::filter(edm::Event & iEvent, edm::EventSetup const & iSetup)
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
    const Candidate * Ks = S->daughter(1);

    reco::Candidate::Vector SMomentum(S->px(), S->py(), S->pz());

    reco::Candidate::Vector Kshort_p(Ks->px(), Ks->py(), Ks->pz());
    if(S->vertexNdof() != 999.){
        if ( ( AnalyzerAllSteps::openings_angle(Kshort_p,SMomentum) > minOpeningsAngle_SKshort_ )
          && ( AnalyzerAllSteps::openings_angle(Kshort_p,SMomentum) < maxOpeningsAngle_SKshort_ ) ) {
          sParticles->push_back(std::move(*S)); 
        }
      }
  }
  int ns = sParticles->size();
  iEvent.put(std::move(sParticles),"sParticles"); 
  return (ns > 0);

}//end filter
#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(SKsDeltaOpeningsAngleFilter);
