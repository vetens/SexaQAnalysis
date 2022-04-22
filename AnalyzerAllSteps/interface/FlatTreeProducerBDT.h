#ifndef FlatTreeProducerBDT_h
#define FlatTreeProducerBDT_h
#include <stdio.h>     
#include <stdlib.h> 
#include <time.h> 
 
#include "AnalyzerAllSteps.h"
using namespace edm;
using namespace std; 
class FlatTreeProducerBDT : public edm::EDAnalyzer
 {
  public:
    explicit FlatTreeProducerBDT(edm::ParameterSet const& cfg);
    virtual ~FlatTreeProducerBDT();
    static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);
    void FillBranches(const reco::VertexCompositeCandidate * antiS, TVector3 beamspot, TVector3 beamspotVariance, edm::Handle<vector<reco::Vertex>> h_offlinePV,  bool m_runningOnData, edm::Handle<vector<reco::GenParticle>> h_genParticles, edm::Handle<vector<reco::VertexCompositeCandidate> > h_V0Ks, edm::Handle<vector<reco::VertexCompositeCandidate> > h_V0L, unsigned int ngoodPVsPOG, double randomPVz);    

  private:

    //some counters
    int nTotalRECOS=0;
    int nSavedRECOS=0;
    double nTotalRECOSWeighed=0.;
    double nSavedRECOSWeighed=0.;
    int nGENAntiSWithCorrectGranddaughters=0;

    bool m_lookAtAntiS;
    bool m_runningOnData; 

    virtual void beginJob();
    virtual void analyze(edm::Event const& iEvent, edm::EventSetup const& iSetup);
    virtual void endJob();
    
    virtual void beginRun(edm::Run const&, edm::EventSetup const&);
    virtual void endRun(edm::Run const&, edm::EventSetup const&);
    virtual void beginLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&);
    virtual void endLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&);

    //initialization of the different trees
    void Init_PV();
    void Init();
    void Init_Counter();

    edm::Service<TFileService> m_fs;

    //the collections 
    edm::InputTag m_bsTag;
    edm::InputTag m_offlinePVTag;
    edm::InputTag m_genParticlesTag_GEN;
    edm::InputTag m_genParticlesTag_SIM_GEANT;
    edm::InputTag m_generalTracksTag;
    edm::InputTag m_sCandsTag;
    edm::InputTag m_V0KsTag;
    edm::InputTag m_V0LTag;

    edm::EDGetTokenT<reco::BeamSpot> m_bsToken;
    edm::EDGetTokenT<vector<reco::Vertex>> m_offlinePVToken;
    edm::EDGetTokenT<vector<reco::GenParticle>> m_genParticlesToken_GEN; 
    edm::EDGetTokenT<vector<reco::GenParticle>> m_genParticlesToken_SIM_GEANT; 
    edm::EDGetTokenT<View<reco::Track>> m_generalTracksToken;
    edm::EDGetTokenT<vector<reco::VertexCompositeCandidate> > m_sCandsToken;
    edm::EDGetTokenT<vector<reco::VertexCompositeCandidate> > m_V0KsToken;
    edm::EDGetTokenT<vector<reco::VertexCompositeCandidate> > m_V0LToken;
   
    //the trees in the ntuples
    TTree* _tree_PV;   
    TTree* _tree;   
    TTree* _tree_counter;

    //definition of variables which should go to _tree_PV
    std::vector<int> _nPV,_nGoodPV,_nGoodPVPOG;
    std::vector<float> _PVx,_PVy,_PVz,_goodPVx,_goodPVy,_goodPVz,_goodPVxPOG,_goodPVyPOG,_goodPVzPOG;

    //definition of variables which should go to tree
    std::vector<float> _S_charge;
    std::vector<float> _S_deltaLInteractionVertexAntiSmin,_S_deltaRAntiSmin,_S_deltaRKsAntiSmin,_S_deltaRLambdaAntiSmin;
    std::vector<float> _S_lxy_interaction_vertex, _S_lxy_interaction_vertex_beampipeCenter, _S_error_lxy_interaction_vertex,_S_error_lxy_interaction_vertex_beampipeCenter,_Ks_lxy_decay_vertex,_Lambda_lxy_decay_vertex,_S_mass,_S_chi2_ndof,_S_event_weighting_factor,_S_event_weighting_factorPU,_S_event_weighting_factorALL;
    std::vector<float> _S_daughters_deltaphi,_S_daughters_deltaeta,_S_daughters_openingsangle,_S_Ks_openingsangle,_S_Lambda_openingsangle,_S_daughters_DeltaR,_S_eta,_Ks_eta,_Lambda_eta;
    std::vector<float> _S_dxy,_Ks_dxy,_Lambda_dxy,_S_dxy_dzPVmin,_Ks_dxy_dzPVmin,_Lambda_dxy_dzPVmin;
    std::vector<float> _S_dxy_over_lxy,_Ks_dxy_over_lxy,_Lambda_dxy_over_lxy;
    std::vector<float> _S_dz,_Ks_dz,_Lambda_dz,_S_dz_min,_Ks_dz_min,_Lambda_dz_min;
    std::vector<float> _S_pt,_Ks_pt,_Lambda_pt;
    std::vector<float> _S_pz,_Ks_pz,_Lambda_pz;
    std::vector<float> _S_vz_interaction_vertex,_Ks_vz_decay_vertex,_Lambda_vz_decay_vertex;
    std::vector<float> _S_vx,_S_vy,_S_vz;
    std::vector<float> _Lambda_mass,_Ks_mass;
    std::vector<float> _RECO_Lambda_daughter0_charge,_RECO_Lambda_daughter0_pt,_RECO_Lambda_daughter0_pz,_RECO_Lambda_daughter0_dxy_beamspot,_RECO_Lambda_daughter0_dz_beamspot;   
    std::vector<float> _RECO_Lambda_daughter1_charge,_RECO_Lambda_daughter1_pt,_RECO_Lambda_daughter1_pz,_RECO_Lambda_daughter1_dxy_beamspot,_RECO_Lambda_daughter1_dz_beamspot;   
    std::vector<float> _RECO_Ks_daughter0_charge,_RECO_Ks_daughter0_pt,_RECO_Ks_daughter0_pz,_RECO_Ks_daughter0_dxy_beamspot,_RECO_Ks_daughter0_dz_beamspot;   
    std::vector<float> _RECO_Ks_daughter1_charge,_RECO_Ks_daughter1_pt,_RECO_Ks_daughter1_pz,_RECO_Ks_daughter1_dxy_beamspot,_RECO_Ks_daughter1_dz_beamspot;   

    //definition of variables which should go to _tree_counter
    std::vector<float> _RECO_S_total_lxy_beampipeCenter, _RECO_S_saved_lxy_beampipeCenter;

    };

#endif

