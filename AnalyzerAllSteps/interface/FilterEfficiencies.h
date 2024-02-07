#ifndef FilterEfficiencies_h
#define FilterEfficiencies_h
#include <stdio.h>     
#include <iostream>     
#include <stdlib.h> 
#include <time.h> 
#include "FWCore/Framework/interface/LuminosityBlock.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/Common/interface/MergeableCounter.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "TTree.h"
#include "TFile.h"
#include "TProfile.h"
 
using namespace edm;
using namespace std; 
class FilterEfficiencies : public edm::EDAnalyzer
 {
  public:
    explicit FilterEfficiencies(edm::ParameterSet const& cfg);
    virtual ~FilterEfficiencies();
    static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);

  private:

    virtual void beginJob();
    virtual void analyze(edm::Event const& iEvent, edm::EventSetup const& iSetup);
    virtual void endJob();
    
    virtual void beginRun(edm::Run const&, edm::EventSetup const&);
    virtual void endRun(edm::Run const&, edm::EventSetup const&);
    virtual void beginLuminosityBlock(edm::LuminosityBlock const& lumi, edm::EventSetup const& setup);
    virtual void endLuminosityBlock(edm::LuminosityBlock const& lumi, edm::EventSetup const& setup);

    void InitCounter();
    void InitTree();

    //the collections 
    edm::InputTag m_Total;
    edm::InputTag m_LambdaKshort;
    edm::InputTag m_Fiducial;
    edm::InputTag m_LambdaKshortVertex;
    edm::InputTag m_SdauDeltaPhi;
    edm::InputTag m_lxy;
    edm::InputTag m_Pointing;
    edm::InputTag m_Vz;
    edm::InputTag m_SdauDeltaEta;
    edm::InputTag m_SdauDeltaOpe;
    edm::InputTag m_SKsDeltaOpe;
    edm::InputTag m_SLambdaDeltaOpe;
    edm::InputTag m_Eta;
    edm::InputTag m_MinDz;
    edm::InputTag m_KsEta;
    edm::InputTag m_KsPt;
    edm::InputTag m_SMass;

    edm::EDGetTokenT<edm::MergeableCounter> m_TotalToken;
    edm::EDGetTokenT<edm::MergeableCounter> m_LambdaKshortToken;
    edm::EDGetTokenT<edm::MergeableCounter> m_FiducialToken;
    edm::EDGetTokenT<edm::MergeableCounter> m_LambdaKshortVertexToken;
    edm::EDGetTokenT<edm::MergeableCounter> m_SdauDeltaPhiToken;
    edm::EDGetTokenT<edm::MergeableCounter> m_lxyToken;
    edm::EDGetTokenT<edm::MergeableCounter> m_PointingToken;
    edm::EDGetTokenT<edm::MergeableCounter> m_VzToken;
    edm::EDGetTokenT<edm::MergeableCounter> m_SdauDeltaEtaToken;
    edm::EDGetTokenT<edm::MergeableCounter> m_SdauDeltaOpeToken;
    edm::EDGetTokenT<edm::MergeableCounter> m_SKsDeltaOpeToken;
    edm::EDGetTokenT<edm::MergeableCounter> m_SLambdaDeltaOpeToken;
    edm::EDGetTokenT<edm::MergeableCounter> m_EtaToken;
    edm::EDGetTokenT<edm::MergeableCounter> m_MinDzToken;
    edm::EDGetTokenT<edm::MergeableCounter> m_KsEtaToken;
    edm::EDGetTokenT<edm::MergeableCounter> m_KsPtToken;
    edm::EDGetTokenT<edm::MergeableCounter> m_SMassToken;

    edm::Service<TFileService> m_fs;

    TTree* _Cutflow;

    std::vector<int> v_nEvTotal, v_nEvLambdaKshort, v_nEvFiducial, v_nEvLambdaKshortVertex, v_nEvSdauDeltaPhi, v_nEvlxy, v_nEvPointing, v_nEvVz, v_nEvSdauDeltaEta, v_nEvSdauDeltaOpe, v_nEvSKsDeltaOpe, v_nEvSLambdaDeltaOpe, v_nEvEta, v_nEvMinDz, v_nEvKsEta, v_nEvKsPt, v_nEvSMass;
    Int_t nEvTotal, nEvLambdaKshort, nEvFiducial, nEvLambdaKshortVertex, nEvSdauDeltaPhi, nEvlxy, nEvPointing, nEvVz, nEvSdauDeltaEta, nEvSdauDeltaOpe, nEvSKsDeltaOpe, nEvSLambdaDeltaOpe, nEvEta, nEvMinDz, nEvKsEta, nEvKsPt, nEvSMass;

    };

#endif

