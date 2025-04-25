#include "../interface/FlatTreeProducerTrackerOccupancy.h"
#include <typeinfo>

FlatTreeProducerTrackerOccupancy::FlatTreeProducerTrackerOccupancy(edm::ParameterSet const& pset):
  m_offlinePVTag(pset.getParameter<edm::InputTag>("offlinePV")),
  m_generalTracksTag(pset.getParameter<edm::InputTag>("generalTracksCollection")),
  m_V0KsTag(pset.getParameter<edm::InputTag>("V0KsCollection")),
  m_V0LTag(pset.getParameter<edm::InputTag>("V0LCollection")),
  m_PUReweighingMapIn(pset.getParameter<edm::FileInPath>("PUReweighting")),

  m_offlinePVToken    (consumes<vector<reco::Vertex>>(m_offlinePVTag)),
  m_generalTracksToken(consumes<vector<reco::Track> >(m_generalTracksTag)),
  m_V0KsToken(consumes<vector<reco::VertexCompositeCandidate> >(m_V0KsTag)),
  m_V0LToken(consumes<vector<reco::VertexCompositeCandidate> >(m_V0LTag))

{
}


void FlatTreeProducerTrackerOccupancy::beginJob() {

	// Initialize when class is created
        edm::Service<TFileService> fs ; 

	//PV info
	_tree_PV = fs->make <TTree>("FlatTreePV","treePV");
	_tree_PV->Branch("_goodPVxPOG",&_goodPVxPOG);
	_tree_PV->Branch("_goodPVyPOG",&_goodPVyPOG);
	_tree_PV->Branch("_goodPVzPOG",&_goodPVzPOG);
	_tree_PV->Branch("_goodPV_weightPU",&_goodPV_weightPU);

	//tree for all the tracks, normally I don't use this as it way too heavy (there are a looooot of tracks)	
	_tree_Tracks = fs->make <TTree>("FlatTreeTracks","tree_Tracks");
	//_tree_Tracks->Branch("_track_eta",&_track_eta);
	_tree_Tracks->Branch("_nTracksTotal",&_nTracksTotal);
        _tree_Tracks->Branch("_nTracks_1_eta_2",&_nTracks_1_eta_2);
        _tree_Tracks->Branch("_nTracks_2_eta_2p5",&_nTracks_2_eta_2p5);
        _tree_Tracks->Branch("_nTracks_2p5_l_eta",&_nTracks_2p5_l_eta);

	_tree_nV0s = fs->make <TTree>("FlatTreeV0s","tree_V0s");
	_tree_nV0s->Branch("_nKshort",&_nKshort);
	_tree_nV0s->Branch("_nLambda",&_nLambda);
}

void FlatTreeProducerTrackerOccupancy::analyze(edm::Event const& iEvent, edm::EventSetup const& iSetup) {
  //primary vertex
  edm::Handle<vector<reco::Vertex>> h_offlinePV;
  iEvent.getByToken(m_offlinePVToken, h_offlinePV);

  //General tracks particles
  edm::Handle<vector<reco::Track>> h_generalTracks;
  iEvent.getByToken(m_generalTracksToken, h_generalTracks);

  //V0 Kshorts
  edm::Handle<vector<reco::VertexCompositeCandidate> > h_V0Ks;
  iEvent.getByToken(m_V0KsToken, h_V0Ks);

  //V0 Lambdas
  edm::Handle<vector<reco::VertexCompositeCandidate> > h_V0L;
  iEvent.getByToken(m_V0LToken, h_V0L);

  //save some info on the PVs
  InitPV();
  unsigned int nGoodPV = 0;
  if(h_offlinePV.isValid()){
	//first count the number of good vertices
	for(unsigned int i = 0; i < h_offlinePV->size(); i++){
		double r = sqrt(h_offlinePV->at(i).x()*h_offlinePV->at(i).x()+h_offlinePV->at(i).y()*h_offlinePV->at(i).y());
                if(h_offlinePV->at(i).ndof() > 4 && abs(h_offlinePV->at(i).z()) < 24 && r < 2)nGoodPV++;
	}

	//now that you know the good number of vertices store the location of the vertex and the reweighing factor (you need the nGoodPV to calculate the weighing factor)
	for(unsigned int i = 0; i < h_offlinePV->size(); i++){
		double r = sqrt(h_offlinePV->at(i).x()*h_offlinePV->at(i).x()+h_offlinePV->at(i).y()*h_offlinePV->at(i).y());
                if(h_offlinePV->at(i).ndof() > 4 && abs(h_offlinePV->at(i).z()) < 24 && r < 2){
			_goodPVxPOG.push_back(h_offlinePV->at(i).x());
                        _goodPVyPOG.push_back(h_offlinePV->at(i).y());
                        _goodPVzPOG.push_back(h_offlinePV->at(i).z());
			double weightPU = 0.;
			if(nGoodPV < 60) weightPU = AnalyzerAllSteps::PUReweighingFactor(nGoodPV, h_offlinePV->at(i).z(), m_PUReweighingMapIn);
        		_goodPV_weightPU.push_back(weightPU);
		}
	}
	
  }
  _tree_PV->Fill();
  InitTracker();
  if(h_generalTracks.isValid() ){
	for(size_t i=0; i<h_generalTracks->size(); ++i) {
	  const reco::Track track = h_generalTracks->at(i);
          _track_eta.push_back(track.eta());
	}
        int trackCount[4] = {0};
        for (std::vector<float>::iterator ieta = _track_eta.begin(); ieta != _track_eta.end(); ++ieta) {
            trackCount[0]++;
            if (abs(*ieta) > 1.0 && abs(*ieta) < 2.0) {
                trackCount[1]++;
            } else if (abs(*ieta) > 2.0 && abs(*ieta) < 2.5) {
                trackCount[2]++;
            } else if (abs(*ieta) > 2.5) {
                trackCount[3]++;
            }
        }
        _nTracksTotal.push_back(trackCount[0]);
        _nTracks_1_eta_2.push_back(trackCount[1]);
        _nTracks_2_eta_2p5.push_back(trackCount[2]);
        _nTracks_2p5_l_eta.push_back(trackCount[3]);

        _tree_Tracks->Fill();
  } else { std::cout << "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!generalTracks collection is not valid!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!" << std::endl;}
  InitV0s();
  if(h_V0Ks.isValid()){
        _nKshort.push_back(h_V0Ks->size());
    }
  if(h_V0L.isValid()){
        _nLambda.push_back(h_V0L->size());
    _tree_nV0s->Fill();
  }
  else{
	std::cout << "one of the collections for filling the tree for the antiS related particles is not valid:" << std::endl;
	std::cout << "h_V0Ks.isValid " << h_V0Ks.isValid() << std::endl;
	std::cout << "h_V0L.isValid " << h_V0L.isValid() << std::endl;
  }
} //end of analyzer

void FlatTreeProducerTrackerOccupancy::InitPV()
{
	_goodPVxPOG.clear();
	_goodPVyPOG.clear();
	_goodPVzPOG.clear();
	_goodPV_weightPU.clear();
}

void FlatTreeProducerTrackerOccupancy::InitTracker()
{
        _track_eta.clear();
        _nTracksTotal.clear();
        _nTracks_1_eta_2.clear();
        _nTracks_2_eta_2p5.clear();
        _nTracks_2p5_l_eta.clear();
}

void FlatTreeProducerTrackerOccupancy::InitV0s()
{
        _nKshort.clear();
        _nLambda.clear();
}

void FlatTreeProducerTrackerOccupancy::endJob()
{
}

void
FlatTreeProducerTrackerOccupancy::beginRun(edm::Run const& iRun, edm::EventSetup const& iSetup)
{
}

// ------------ method called when ending the processing of a run  ------------
void
FlatTreeProducerTrackerOccupancy::endRun(edm::Run const&, edm::EventSetup const&)
{
}

// ------------ method called when starting to processes a luminosity block  ------------
void
FlatTreeProducerTrackerOccupancy::beginLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&)
{
}

// ------------ method called when ending the processing of a luminosity block  ------------
void
FlatTreeProducerTrackerOccupancy::endLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&)
{
}

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void
FlatTreeProducerTrackerOccupancy::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}

FlatTreeProducerTrackerOccupancy::~FlatTreeProducerTrackerOccupancy()
{
}


DEFINE_FWK_MODULE(FlatTreeProducerTrackerOccupancy);
