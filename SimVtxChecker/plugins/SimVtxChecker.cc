// -*- C++ -*-
//
// Package:    SexaQAnalysis/SimVtxChecker
// Class:      SimVtxChecker
//
/**\class SimVtxChecker SimVtxChecker.cc SexaQAnalysis/SimVtxChecker/plugins/SimVtxChecker.cc

 Description: Read out Sim Vertices and Sim Tracks and plot the sim vertex rho only for simtracks which are antilambda

 Implementation:
     [Notes on implementation]
*/
//
// Original Author:  Wren Vetens
//         Created:  Mon, 11 Jul 2022 11:30:24 GMT
//
//


// system include files
#include <memory>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/one/EDAnalyzer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
 #include "FWCore/Utilities/interface/InputTag.h"
 #include "SimDataFormats/Track/interface/SimTrack.h"
 #include "SimDataFormats/Vertex/interface/SimVertex.h"
 #include "FWCore/ServiceRegistry/interface/Service.h"
 #include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/GeometryVector/interface/GlobalVector.h"
 #include "TH1.h"
//
// class declaration
//

// If the analyzer does not use TFileService, please remove
// the template argument to the base class so the class inherits
// from  edm::one::EDAnalyzer<>
// This will improve performance in multithreaded jobs.


using namespace std;
using namespace edm;

class SimVtxChecker : public edm::one::EDAnalyzer<edm::one::SharedResources>  {
   public:
      explicit SimVtxChecker(edm::ParameterSet const& cfg);
      virtual ~SimVtxChecker();
      static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);

   private:
      virtual void beginJob() override;
      virtual void analyze(const edm::Event&, const edm::EventSetup&) override;
      virtual void endJob() override;

      // ----------member data ---------------------------
      //edm::EDGetTokenT<TrackCollection> tracksToken_;  //used to select what tracks to read from configuration file
      //
      edm::InputTag m_g4SimHitsTag;
  
      edm::EDGetTokenT<vector<SimTrack>> m_g4SimHits_Track_Token;
      edm::EDGetTokenT<vector<SimVertex>> m_g4SimHits_Vertex_Token;

       TH1F * LambdaBar_rho;
};

//
// constants, enums and typedefs
//

//
// static data member definitions
//

//
// constructors and destructor
//
SimVtxChecker::SimVtxChecker(const edm::ParameterSet& pset)
 :
//  tracksToken_(consumes<TrackCollection>(pset.getUntrackedParameter<edm::InputTag>("tracks")))
    m_g4SimHitsTag(pset.getParameter<edm::InputTag>("g4SimHitsCollection")),

    m_g4SimHits_Track_Token(consumes<vector<SimTrack> >(m_g4SimHitsTag)),
    m_g4SimHits_Vertex_Token(consumes<vector<SimVertex> >(m_g4SimHitsTag))

{
   //now do what ever initialization is needed
   usesResource("TFileService");
   edm::Service<TFileService> fs;
   LambdaBar_rho = fs->make<TH1F>("#bar{#Lambda} Creation Vertex" , "#bar{#Lambda} #rho (cm)" , 50 , 0 , 16 );

}


SimVtxChecker::~SimVtxChecker()
{

   // do anything here that needs to be done at desctruction time
   // (e.g. close files, deallocate resources etc.)

}


//
// member functions
//

// ------------ method called for each event  ------------
void
SimVtxChecker::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{
   using namespace edm;

    //G4SimHits Tracks
    Handle<vector<SimTrack>> h_SimTracks;
    iEvent.getByToken(m_g4SimHits_Track_Token, h_SimTracks);

    //G4SimHits Vertexs
    Handle<vector<SimVertex>> h_SimVertexs;
    iEvent.getByToken(m_g4SimHits_Vertex_Token, h_SimVertexs);
    
    for(unsigned int i = 0; i < h_SimVertexs->size(); i++) {
      // do something with track parameters, e.g, plot the charge.
      // int charge = itTrack->charge();
      const SimTrack * simTrack = &h_SimTracks->at(i);
      if(simTrack->type() != -3122) continue;
      const SimVertex * simVertex = &h_SimVertexs->at(i);
      LambdaBar_rho->Fill(simVertex->position().Rho());
    }

//#ifdef THIS_IS_AN_EVENT_EXAMPLE
//   Handle<ExampleData> pIn;
//   iEvent.getByLabel("example",pIn);
//#endif
//
//#ifdef THIS_IS_AN_EVENTSETUP_EXAMPLE
//   ESHandle<SetupData> pSetup;
//   iSetup.get<SetupRecord>().get(pSetup);
//#endif
}


// ------------ method called once each job just before starting event loop  ------------
void
SimVtxChecker::beginJob()
{
}

// ------------ method called once each job just after ending the event loop  ------------
void
SimVtxChecker::endJob()
{
}

// ------------ method fills histograms with the allowed parameters for the module  ------------
void
SimVtxChecker::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);

  //Specify that only 'tracks' is allowed
  //To use, remove the default given above and uncomment below
  //ParameterSetDescription desc;
  //desc.addUntracked<edm::InputTag>("tracks","ctfWithMaterialTracks");
  //descriptions.addDefault(desc);
}

//define this as a plug-in
DEFINE_FWK_MODULE(SimVtxChecker);
