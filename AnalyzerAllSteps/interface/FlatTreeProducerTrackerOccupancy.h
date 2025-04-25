#ifndef AnalyzerAllSteps_h
#define AnalyzerAllSteps_h
#include "SimDataFormats/PileupSummaryInfo/interface/PileupSummaryInfo.h"
#include "MagneticField/Records/interface/IdealMagneticFieldRecord.h"
#include "MagneticField/VolumeBasedEngine/interface/VolumeBasedMagneticField.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "TrackingTools/TransientTrack/interface/TransientTrack.h"
#include "RecoVertex/VertexPrimitives/interface/TransientVertex.h"
#include "RecoVertex/KalmanVertexFit/interface/KalmanVertexFitter.h"
#include "RecoVertex/AdaptiveVertexFit/interface/AdaptiveVertexFitter.h"
#include "MagneticField/Records/interface/IdealMagneticFieldRecord.h"
#include "MagneticField/VolumeBasedEngine/interface/VolumeBasedMagneticField.h"
#include "TrackingTools/PatternTools/interface/ClosestApproachInRPhi.h"
#include "DataFormats/RecoCandidate/interface/RecoChargedCandidate.h"
#include "CommonTools/CandUtils/interface/AddFourMomenta.h" 

#include "TrackingTools/PatternTools/interface/TSCPBuilderNoMaterial.h"
#include "TrackingTools/TrajectoryState/interface/FreeTrajectoryState.h"

#include "AnalyzerAllSteps.h"
using namespace edm;
using namespace std; 
class FlatTreeProducerTrackerOccupancy : public edm::EDAnalyzer
 {
  public:
    explicit FlatTreeProducerTrackerOccupancy(edm::ParameterSet const& cfg);
    virtual void beginJob();
    virtual void analyze(edm::Event const& iEvent, edm::EventSetup const& iSetup);
    static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);
    virtual void endJob();

    virtual void beginRun(edm::Run const&, edm::EventSetup const&);
    virtual void endRun(edm::Run const&, edm::EventSetup const&);
    virtual void beginLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&);
    virtual void endLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&);

    virtual ~FlatTreeProducerTrackerOccupancy();

  private:

    //initialization of the different trees 
    void InitPV();
    void InitTracker();
    void InitV0s();
    
    edm::Service<TFileService> m_fs;
 
    //the collections
    edm::InputTag m_offlinePVTag;
    edm::InputTag m_generalTracksTag;
    edm::InputTag m_V0KsTag;
    edm::InputTag m_V0LTag;

    edm::FileInPath m_PUReweighingMapIn;
//    edm::InputTag m_PileupInfoTag;

    edm::EDGetTokenT<vector<reco::Vertex>> m_offlinePVToken;
    edm::EDGetTokenT<vector<reco::Track>> m_generalTracksToken;
    edm::EDGetTokenT<vector<reco::VertexCompositeCandidate> > m_V0KsToken;
    edm::EDGetTokenT<vector<reco::VertexCompositeCandidate> > m_V0LToken;
//    edm::EDGetTokenT<vector<PileupSummaryInfo> > m_PileupInfoToken;

    TTree* _tree_PV;   
    std::vector<float> _goodPVxPOG,_goodPVyPOG,_goodPVzPOG,_goodPV_weightPU;

    TTree* _tree_Tracks;   
    std::vector<float> _track_eta;
    std::vector<int> _nTracksTotal, _nTracks_1_eta_2, _nTracks_2_eta_2p5, _nTracks_2p5_l_eta;
    TTree* _tree_nV0s;   
    std::vector<int> _nKshort, _nLambda;

     };
#endif
