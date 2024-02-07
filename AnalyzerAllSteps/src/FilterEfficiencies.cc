#include "../interface/FilterEfficiencies.h"
#include <typeinfo>
#include <iostream>     
#include "DataFormats/Common/interface/Handle.h"

FilterEfficiencies::FilterEfficiencies(edm::ParameterSet const& pset):
  m_Total(pset.getParameter<edm::InputTag>("nEvTotal")),
  m_LambdaKshort(pset.getParameter<edm::InputTag>("nEvLambdaKshort")),
  m_Fiducial(pset.getParameter<edm::InputTag>("nEvFiducial")),
  m_LambdaKshortVertex(pset.getParameter<edm::InputTag>("nEvLambdaKshortVertex")),
  m_SdauDeltaPhi(pset.getParameter<edm::InputTag>("nEvSdauDeltaPhi")),
  m_lxy(pset.getParameter<edm::InputTag>("nEvlxy")),
  m_Pointing(pset.getParameter<edm::InputTag>("nEvPointing")),
  m_Vz(pset.getParameter<edm::InputTag>("nEvVz")),
  m_SdauDeltaEta(pset.getParameter<edm::InputTag>("nEvSdauDeltaEta")),
  m_SdauDeltaOpe(pset.getParameter<edm::InputTag>("nEvSdauDeltaOpe")),
  m_SKsDeltaOpe(pset.getParameter<edm::InputTag>("nEvSKsDeltaOpe")),
  m_SLambdaDeltaOpe(pset.getParameter<edm::InputTag>("nEvSLambdaDeltaOpe")),
  m_Eta(pset.getParameter<edm::InputTag>("nEvEta")),
  m_MinDz(pset.getParameter<edm::InputTag>("nEvMinDz")),
  m_KsEta(pset.getParameter<edm::InputTag>("nEvKsEta")),
  m_KsPt(pset.getParameter<edm::InputTag>("nEvKsPt")),
  m_SMass(pset.getParameter<edm::InputTag>("nEvSMass")),

  m_TotalToken(consumes<edm::MergeableCounter,edm::InLumi>(m_Total)),
  m_LambdaKshortToken(consumes<edm::MergeableCounter,edm::InLumi>(m_LambdaKshort)),
  m_FiducialToken(consumes<edm::MergeableCounter,edm::InLumi>(m_Fiducial)),
  m_LambdaKshortVertexToken(consumes<edm::MergeableCounter,edm::InLumi>(m_LambdaKshortVertex)),
  m_SdauDeltaPhiToken(consumes<edm::MergeableCounter,edm::InLumi>(m_SdauDeltaPhi)),
  m_lxyToken(consumes<edm::MergeableCounter,edm::InLumi>(m_lxy)),
  m_PointingToken(consumes<edm::MergeableCounter,edm::InLumi>(m_Pointing)),
  m_VzToken(consumes<edm::MergeableCounter,edm::InLumi>(m_Vz)),
  m_SdauDeltaEtaToken(consumes<edm::MergeableCounter,edm::InLumi>(m_SdauDeltaEta)),
  m_SdauDeltaOpeToken(consumes<edm::MergeableCounter,edm::InLumi>(m_SdauDeltaOpe)),
  m_SKsDeltaOpeToken(consumes<edm::MergeableCounter,edm::InLumi>(m_SKsDeltaOpe)),
  m_SLambdaDeltaOpeToken(consumes<edm::MergeableCounter,edm::InLumi>(m_SLambdaDeltaOpe)),
  m_EtaToken(consumes<edm::MergeableCounter,edm::InLumi>(m_Eta)),
  m_MinDzToken(consumes<edm::MergeableCounter,edm::InLumi>(m_MinDz)),
  m_KsEtaToken(consumes<edm::MergeableCounter,edm::InLumi>(m_KsEta)),
  m_KsPtToken(consumes<edm::MergeableCounter,edm::InLumi>(m_KsPt)),
  m_SMassToken(consumes<edm::MergeableCounter,edm::InLumi>(m_SMass))
{
}


void FilterEfficiencies::beginJob() {
        // Initialize when class is created
        edm::Service<TFileService> fs;
        _Cutflow = fs->make <TTree>("Cutflow", "_Cutflow");

        _Cutflow->Branch("_nEvTotal", &v_nEvTotal);
        _Cutflow->Branch("_nEvLambdaKshort", &v_nEvLambdaKshort);
        _Cutflow->Branch("_nEvFiducial", &v_nEvFiducial);
        _Cutflow->Branch("_nEvLambdaKshortVertex", &v_nEvLambdaKshortVertex);
        _Cutflow->Branch("_nEvSdauDeltaPhi", &v_nEvSdauDeltaPhi);
        _Cutflow->Branch("_nEvlxy", &v_nEvlxy);
        _Cutflow->Branch("_nEvPointing", &v_nEvPointing);
        _Cutflow->Branch("_nEvVz", &v_nEvVz);
        _Cutflow->Branch("_nEvSdauDeltaEta", &v_nEvSdauDeltaEta);
        _Cutflow->Branch("_nEvSdauDeltaOpe", &v_nEvSdauDeltaOpe);
        _Cutflow->Branch("_nEvSKsDeltaOpe", &v_nEvSKsDeltaOpe);
        _Cutflow->Branch("_nEvSLambdaDeltaOpe", &v_nEvSLambdaDeltaOpe);
        _Cutflow->Branch("_nEvEta", &v_nEvEta);
        _Cutflow->Branch("_nEvMinDz", &v_nEvMinDz);
        _Cutflow->Branch("_nEvKsEta", &v_nEvKsEta);
        _Cutflow->Branch("_nEvKsPt", &v_nEvKsPt);
        _Cutflow->Branch("_nEvSMass", &v_nEvSMass);
        InitCounter();
}

void FilterEfficiencies::analyze(edm::Event const& iEvent, edm::EventSetup const& iSetup)
{
    
}
void FilterEfficiencies::endJob()
{
    
}

void
FilterEfficiencies::beginRun(edm::Run const& iRun, edm::EventSetup const& iSetup)
{
}

// ------------ method called when ending the processing of a run  ------------
void
FilterEfficiencies::endRun(edm::Run const&, edm::EventSetup const&)
{
}

// ------------ method called when starting to processes a luminosity block  ------------
void
FilterEfficiencies::beginLuminosityBlock(edm::LuminosityBlock const& lumi, edm::EventSetup const& setup)
{
}

// ------------ method called when ending the processing of a luminosity block  ------------
void
FilterEfficiencies::endLuminosityBlock(edm::LuminosityBlock const& lumi, edm::EventSetup const& setup)
{
edm::Handle<edm::MergeableCounter> nEvTotalCounter;
lumi.getByToken(m_TotalToken, nEvTotalCounter);

edm::Handle<edm::MergeableCounter> nEvLambdaKshortCounter;
lumi.getByToken(m_LambdaKshortToken, nEvLambdaKshortCounter);

edm::Handle<edm::MergeableCounter> nEvFiducialCounter;
lumi.getByToken(m_FiducialToken, nEvFiducialCounter);

edm::Handle<edm::MergeableCounter> nEvLambdaKshortVertexCounter;
lumi.getByToken(m_LambdaKshortVertexToken, nEvLambdaKshortVertexCounter);

edm::Handle<edm::MergeableCounter> nEvSdauDeltaPhiCounter;
lumi.getByToken(m_SdauDeltaPhiToken, nEvSdauDeltaPhiCounter);

edm::Handle<edm::MergeableCounter> nEvlxyCounter;
lumi.getByToken(m_lxyToken, nEvlxyCounter);

edm::Handle<edm::MergeableCounter> nEvPointingCounter;
lumi.getByToken(m_PointingToken, nEvPointingCounter);

edm::Handle<edm::MergeableCounter> nEvVzCounter;
lumi.getByToken(m_VzToken, nEvVzCounter);

edm::Handle<edm::MergeableCounter> nEvSdauDeltaEtaCounter;
lumi.getByToken(m_SdauDeltaEtaToken, nEvSdauDeltaEtaCounter);

edm::Handle<edm::MergeableCounter> nEvSdauDeltaOpeCounter;
lumi.getByToken(m_SdauDeltaOpeToken, nEvSdauDeltaOpeCounter);

edm::Handle<edm::MergeableCounter> nEvSKsDeltaOpeCounter;
lumi.getByToken(m_SKsDeltaOpeToken, nEvSKsDeltaOpeCounter);

edm::Handle<edm::MergeableCounter> nEvSLambdaDeltaOpeCounter;
lumi.getByToken(m_SLambdaDeltaOpeToken, nEvSLambdaDeltaOpeCounter);

edm::Handle<edm::MergeableCounter> nEvEtaCounter;
lumi.getByToken(m_EtaToken, nEvEtaCounter);

edm::Handle<edm::MergeableCounter> nEvMinDzCounter;
lumi.getByToken(m_MinDzToken, nEvMinDzCounter);

edm::Handle<edm::MergeableCounter> nEvKsEtaCounter;
lumi.getByToken(m_KsEtaToken, nEvKsEtaCounter);

edm::Handle<edm::MergeableCounter> nEvKsPtCounter;
lumi.getByToken(m_KsPtToken, nEvKsPtCounter);

edm::Handle<edm::MergeableCounter> nEvSMassCounter;
lumi.getByToken(m_SMassToken, nEvSMassCounter);

InitTree();

nEvTotal += nEvTotalCounter->value;
v_nEvTotal.push_back(nEvTotalCounter->value);

nEvLambdaKshort += nEvLambdaKshortCounter->value;
v_nEvLambdaKshort.push_back(nEvLambdaKshortCounter->value);

nEvFiducial += nEvFiducialCounter->value;
v_nEvFiducial.push_back(nEvFiducialCounter->value);

nEvLambdaKshortVertex += nEvLambdaKshortVertexCounter->value;
v_nEvLambdaKshortVertex.push_back(nEvLambdaKshortVertexCounter->value);

nEvSdauDeltaPhi += nEvSdauDeltaPhiCounter->value;
v_nEvSdauDeltaPhi.push_back(nEvSdauDeltaPhiCounter->value);

nEvlxy += nEvlxyCounter->value;
v_nEvlxy.push_back(nEvlxyCounter->value);

nEvPointing += nEvPointingCounter->value;
v_nEvPointing.push_back(nEvPointingCounter->value);

nEvVz += nEvVzCounter->value;
v_nEvVz.push_back(nEvVzCounter->value);

nEvSdauDeltaEta += nEvSdauDeltaEtaCounter->value;
v_nEvSdauDeltaEta.push_back(nEvSdauDeltaEtaCounter->value);

nEvSdauDeltaOpe += nEvSdauDeltaOpeCounter->value;
v_nEvSdauDeltaOpe.push_back(nEvSdauDeltaOpeCounter->value);

nEvSKsDeltaOpe += nEvSKsDeltaOpeCounter->value;
v_nEvSKsDeltaOpe.push_back(nEvSKsDeltaOpeCounter->value);

nEvSLambdaDeltaOpe += nEvSLambdaDeltaOpeCounter->value;
v_nEvSLambdaDeltaOpe.push_back(nEvSLambdaDeltaOpeCounter->value);

nEvEta += nEvEtaCounter->value;
v_nEvEta.push_back(nEvEtaCounter->value);

nEvMinDz += nEvMinDzCounter->value;
v_nEvMinDz.push_back(nEvMinDzCounter->value);

nEvKsEta += nEvKsEtaCounter->value;
v_nEvKsEta.push_back(nEvKsEtaCounter->value);

nEvKsPt += nEvKsPtCounter->value;
v_nEvKsPt.push_back(nEvKsPtCounter->value);

nEvSMass += nEvSMassCounter->value;
v_nEvSMass.push_back(nEvSMassCounter->value);

_Cutflow->Fill();
}

void
FilterEfficiencies::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}

FilterEfficiencies::~FilterEfficiencies() {

        std::cout << "Total number of Events: " << nEvTotal << std::endl;
        std::cout << "Number of Events with valid Lambda and Ks: " << nEvLambdaKshort << std::endl;
        std::cout << "Number of Events within Fiducial Region: " << nEvFiducial << std::endl;
        std::cout << "Number of Events with valid S Candidate Vertex: " << nEvLambdaKshortVertex << std::endl;
        std::cout << "Number of Events with S Daughters |DeltaPhi| => 0.4: " << nEvSdauDeltaPhi << std::endl;
        std::cout << "Number of Events with S annihilating at or near the Beampipe: " << nEvlxy << std::endl;
        std::cout << "Number of Events with S 0 <= dxy/lxy <= 0.5: " << nEvPointing << std::endl;
        std::cout << "Number of Events with S annihilation vertex z-component within 28 cm of the origin: "<< nEvVz << std::endl;
        std::cout << "Number of Events with S daughters abs Delta Eta <= 2: " << nEvSdauDeltaEta << std::endl;
        std::cout << "Number of Events with S daughters delta openingsangle between 0.4 and 2: " << nEvSdauDeltaOpe << std::endl;
        std::cout << "Number of Events with S Ks delta openingsangle between 0.1 and 1.8: " << nEvSKsDeltaOpe << std::endl;
        std::cout << "Number of Events with S Lambda delta openingsangle between 0.05 and 1: " << nEvSLambdaDeltaOpe << std::endl;
        std::cout << "Number of Events with abs S eta <= 3.5: " << nEvEta << std::endl;
        std::cout << "Number of Events with longitudinal impact parameter wrt the most-likely primary Vertex <= 6 cm: " << nEvMinDz << std::endl;
        std::cout << "Number of Events with abs Ks eta <= 2.5: "<< nEvKsEta << std::endl;
        std::cout << "Number of Events with Ks pT <= 2.5: " << nEvKsPt << std::endl;
        std::cout << "Number of Events passing all filters: " << nEvSMass << std::endl;
}
void FilterEfficiencies::InitCounter() {
        nEvTotal              = 0;
        nEvLambdaKshort       = 0;
        nEvFiducial           = 0;
        nEvLambdaKshortVertex = 0;
        nEvSdauDeltaPhi       = 0;
        nEvlxy                = 0;
        nEvPointing           = 0;
        nEvVz                 = 0;
        nEvSdauDeltaEta       = 0;
        nEvSdauDeltaOpe       = 0;
        nEvSKsDeltaOpe        = 0;
        nEvSLambdaDeltaOpe    = 0;
        nEvEta                = 0;
        nEvMinDz              = 0;
        nEvKsEta              = 0;
        nEvKsPt               = 0;
        nEvSMass              = 0;
}
void FilterEfficiencies::InitTree() {
        v_nEvTotal.clear();
        v_nEvLambdaKshort.clear();
        v_nEvFiducial.clear();
        v_nEvLambdaKshortVertex.clear();
        v_nEvSdauDeltaPhi.clear();
        v_nEvlxy.clear();
        v_nEvPointing.clear();
        v_nEvVz.clear();
        v_nEvSdauDeltaEta.clear();
        v_nEvSdauDeltaOpe.clear();
        v_nEvSKsDeltaOpe.clear();
        v_nEvSLambdaDeltaOpe.clear();
        v_nEvEta.clear();
        v_nEvMinDz.clear();
        v_nEvKsEta.clear();
        v_nEvKsPt.clear();
        v_nEvSMass.clear();
}

DEFINE_FWK_MODULE(FilterEfficiencies);
