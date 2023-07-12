#include "SLambdaDeltaOpeningsAngleFilter.h"
using namespace reco;
using namespace edm;
using namespace std;

SLambdaDeltaOpeningsAngleFilter::SLambdaDeltaOpeningsAngleFilter(edm::ParameterSet const& pset):
  //collections
  sCollectionTag_               (pset.getParameter<edm::InputTag>("sexaqCandidates")),
  //parameters
  //Initial Preselection parameters
  minOpeningsAngle_SLambda     (pset.getParameter<double>("minOpeningsAngle_SLambda")),
  maxOpeningsAngle_SLambda     (pset.getParameter<double>("maxOpeningsAngle_SLambda"))
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
bool SLambdaDeltaOpeningsAngleFilter::filter(edm::Event & iEvent, edm::EventSetup const & iSetup)
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

    reco::Candidate::Vector SMomentum(S->px(), S->py(), S->pz());
    reco::Candidate::Vector Lambdap(Lambda->px(), Lambda->py(), Lambda->pz());

    if(S->vertexNdof() != 999.){
        if ( ( AnalyzerAllSteps::openings_angle(Lambdap,SMomentum) > minOpeningsAngle_SLambda )
          && ( AnalyzerAllSteps::openings_angle(Lambdap,SMomentum) < maxOpeningsAngle_SLambda )
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
DEFINE_FWK_MODULE(SLambdaDeltaOpeningsAngleFilter);
