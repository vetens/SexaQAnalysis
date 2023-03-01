#include "../interface/PileUpScraper.h"
#include <typeinfo>

PileUpScraper::PileUpScraper(edm::ParameterSet const& pset):
  m_runningOnData(pset.getUntrackedParameter<bool>("runningOnData")),
  m_offlinePVTag(pset.getParameter<edm::InputTag>("offlinePV")),

  m_offlinePVToken    (consumes<reco::VertexCollection>(m_offlinePVTag))
{

}


void PileUpScraper::beginJob() {

        // Initialize when class is created
        edm::Service<TFileService> fs ;

	//PV information
        _tree_PV = fs->make <TTree>("FlatTreePV","tree_PV");

	_tree_PV->Branch("_nGoodPVPOG",&_nGoodPVPOG);
	_tree_PV->Branch("_goodPVxPOG",&_goodPVxPOG);
	_tree_PV->Branch("_goodPVyPOG",&_goodPVyPOG);
	_tree_PV->Branch("_goodPVzPOG",&_goodPVzPOG);


}

void PileUpScraper::analyze(edm::Event const& iEvent, edm::EventSetup const& iSetup) {

  //primary vertex
  edm::Handle<reco::VertexCollection> h_offlinePV;
  iEvent.getByToken(m_offlinePVToken, h_offlinePV);

  //first store some info on the PV
  unsigned int ngoodPVsPOG = 0;
  Init_PV();
  if(h_offlinePV.isValid()){
	for(unsigned int i = 0; i < h_offlinePV->size(); i++ ){
	    ngoodPVsPOG++;
            _goodPVxPOG.push_back(h_offlinePV->at(i).x());
            _goodPVyPOG.push_back(h_offlinePV->at(i).y());
            _goodPVzPOG.push_back(h_offlinePV->at(i).z());
	}
  }
  _nGoodPVPOG.push_back(ngoodPVsPOG);
  _tree_PV->Fill();
 } //end of analyzer

void PileUpScraper::endJob()
{
}

void
PileUpScraper::beginRun(edm::Run const& iRun, edm::EventSetup const& iSetup)
{
  srand(time(NULL));
}

// ------------ method called when ending the processing of a run  ------------
void
PileUpScraper::endRun(edm::Run const&, edm::EventSetup const&)
{
}

// ------------ method called when starting to processes a luminosity block  ------------
void
PileUpScraper::beginLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&)
{
}

// ------------ method called when ending the processing of a luminosity block  ------------
void
PileUpScraper::endLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&)
{
}

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void
PileUpScraper::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}

PileUpScraper::~PileUpScraper()
{

}

void PileUpScraper::Init_PV()
{
        _nGoodPVPOG.clear();
        _goodPVxPOG.clear();
        _goodPVyPOG.clear();
        _goodPVzPOG.clear();
}

DEFINE_FWK_MODULE(PileUpScraper);
