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
class FlatTreeProducerTracking : public edm::EDAnalyzer
 {
  public:
    explicit FlatTreeProducerTracking(edm::ParameterSet const& cfg);
    virtual void beginJob();
    virtual void analyze(edm::Event const& iEvent, edm::EventSetup const& iSetup);
    static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);
    virtual void endJob();

    virtual void beginRun(edm::Run const&, edm::EventSetup const&);
    virtual void endRun(edm::Run const&, edm::EventSetup const&);
    virtual void beginLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&);
    virtual void endLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&);

    virtual ~FlatTreeProducerTracking();

    void FillTreesTracks(const TrackingParticle& tp, TVector3 beamspot, int nPVs, const reco::Track *matchedTrackPointer, bool matchingTrackFound, std::vector<double> tpIsGrandDaughterAntiS);
    int FillTreesAntiSAndDaughters(const TrackingParticle& tp, TVector3 beamspot, reco::BeamSpot::Point beamspotPoint, TVector3 beamspotVariance,int nPVs, edm::Handle<View<reco::Track>> h_generalTracks, edm::Handle<TrackingParticleCollection> h_TP, edm::Handle< reco::TrackToTrackingParticleAssociator> h_trackAssociator, edm::Handle<vector<reco::VertexCompositeCandidate> > h_V0Ks, edm::Handle<vector<reco::VertexCompositeCandidate> > h_V0L, edm::Handle<vector<reco::VertexCompositeCandidate> > h_sCands, TrackingParticleCollection const & TPColl, reco::SimToRecoCollection const & simRecColl, const reco::BeamSpot* theBeamSpot, const MagneticField* theMagneticField , unsigned int nGoodPV);
    void FillFlatTreeTpsAntiS(TVector3 beamspot, TVector3 AntiSCreationVertex, TrackingParticle trackingParticle, bool RECOFound, int type, double besteDeltaR, int returnCodeV0Fitter, double besteDeltaL, const MagneticField* theMagneticField);
    void FillFlatTreeTpsAntiSRECO(TVector3 beamspot, reco::BeamSpot::Point beamspotPoint, bool RECOFound, int type, reco::VertexCompositeCandidate  bestRECOCompositeCandidate);
    void FillFlatTreeTpsAntiSRECO(TVector3 beamspot, reco::BeamSpot::Point beamspotPoint, bool RECOFound, int type, const reco::Track *matchedTrackPointer);
    void FillFlatTreeTpsAntiSRECODummy();
    int V0Fitter_trackSelection(const reco::Track *matchedTrackPointer1, const reco::BeamSpot* theBeamSpot);
    int V0Fitter(const reco::Track *matchedTrackPointer1, const reco::Track *matchedTrackPointer2, const reco::BeamSpot* theBeamSpot, const MagneticField* theMagneticField, bool isGENKs, bool isGENLambda, bool isGENAntiLambda);

    
  private:

    //some counters
    int numberOfAntiSWithCorrectGranddaughters = 0;
    int totalNumberOfUniqueAntiS_FromTrackingParticles= 0;
    double nTotalUniqueGenS_weighted = 0.;
    double nTotalUniqueGenS_Nonweighted = 0.;
    double weighedRecoAntiS = 0.;
    double nonweighedRecoAntiS= 0.;

    //configurable parameters
    bool m_lookAtAntiS;

    //initialization of the different trees 
    void InitPV();
    void InitTracking();
    void InitTrackingAntiS();
    
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
    edm::InputTag m_trackAssociatorTag;
    edm::InputTag m_TPTag;
//    edm::InputTag m_PileupInfoTag;


    edm::EDGetTokenT<reco::BeamSpot> m_bsToken;
    edm::EDGetTokenT<vector<reco::Vertex>> m_offlinePVToken;
    edm::EDGetTokenT<vector<reco::GenParticle>> m_genParticlesToken_GEN;
    edm::EDGetTokenT<vector<reco::GenParticle>> m_genParticlesToken_SIM_GEANT;
    //edm::EDGetTokenT<vector<reco::Track>> m_generalTracksToken;
    edm::EDGetTokenT<View<reco::Track>> m_generalTracksToken;
    edm::EDGetTokenT<vector<reco::VertexCompositeCandidate> > m_sCandsToken;
    edm::EDGetTokenT<vector<reco::VertexCompositeCandidate> > m_V0KsToken;
    edm::EDGetTokenT<vector<reco::VertexCompositeCandidate> > m_V0LToken;
    edm::EDGetTokenT<reco::TrackToTrackingParticleAssociator>  m_trackAssociatorToken;
    edm::EDGetTokenT<vector<TrackingParticle> > m_TPToken;
//    edm::EDGetTokenT<vector<PileupSummaryInfo> > m_PileupInfoToken;


    //the trees and the respective variables
    TTree* _tree_counter;
    std::vector<float> _nGENAntiS,_nRECOAntiS;
   
    TTree* _tree_PV;   
    std::vector<float> _goodPVxPOG,_goodPVyPOG,_goodPVzPOG,_goodPV_weightPU;

    TTree* _tree_tracks;   
    std::vector<float> _tp_pt,_tp_eta,_tp_phi,_tp_pz,_tp_Lxy_beamspot,_tp_vz_beamspot,_tp_dxy_beamspot,_tp_dz_beamspot,_tp_etaOfGrandMotherAntiS;
    std::vector<int> _tp_numberOfTrackerHits,_tp_charge,_tp_reconstructed,_tp_isAntiSTrack;
    std::vector<float> _matchedTrack_pt,_matchedTrack_eta,_matchedTrack_phi,_matchedTrack_pz,_matchedTrack_chi2,_matchedTrack_ndof,_matchedTrack_dxy_beamspot,_matchedTrack_dz_beamspot;
    std::vector<int> _matchedTrack_trackQuality,_matchedTrack_charge,_matchedTrack_isLooper;

    TTree* _tree_tpsAntiS;
    std::vector<float> _tpsAntiS_bestDeltaRWithRECO,_tpsAntiS_deltaLInteractionVertexAntiSmin,_tpsAntiS_mass,_tpsAntiS_pt,_tpsAntiS_eta,_tpsAntiS_phi,_tpsAntiS_pz,_tpsAntiS_Lxy_beampipeCenter,_tpsAntiS_Lxy_beamspot,_tpsAntiS_vz,_tpsAntiS_vz_beamspot,_tpsAntiS_dxy_beamspot,_tpsAntiS_dz_beamspot,_tpsAntiS_dz_AntiSCreationVertex,_tpsAntiS_dxyTrack_beamspot,_tpsAntiS_dzTrack_beamspot,_tpsAntiS_numberOfTrackerHits,_tpsAntiS_charge,_tpsAntiS_reconstructed,_tpsAntiS_event_weighting_factor,_tpsAntiS_event_weighting_factorPU;
    std::vector<float> _tpsAntiS_bestRECO_mass,_tpsAntiS_bestRECO_massMinusNeutron,_tpsAntiS_bestRECO_pt,_tpsAntiS_bestRECO_eta,_tpsAntiS_bestRECO_phi,_tpsAntiS_bestRECO_pz,_tpsAntiS_bestRECO_Lxy_beampipeCenter,_tpsAntiS_bestRECO_Lxy_beamspot,_tpsAntiS_bestRECO_error_Lxy_beampipeCenter,_tpsAntiS_bestRECO_error_Lxy_beamspot,_tpsAntiS_bestRECO_vz,_tpsAntiS_bestRECO_vz_beamspot,_tpsAntiS_bestRECO_dxy_beamspot,_tpsAntiS_bestRECO_dz_beamspot,_tpsAntiS_bestRECO_dxyTrack_beamspot,_tpsAntiS_bestRECO_dzTrack_beamspot,_tpsAntiS_bestRECO_charge,_tpsAntiS_returnCodeV0Fitter;
    std::vector<int> _tpsAntiS_type,_tpsAntiS_pdgId;

    //for the evaluation of the  V0Fitter:
    bool vertexFitter_;
    bool useRefTracks_;
    bool doKShorts_;
    bool doLambdas_;
    // cuts on initial track selection
    double tkChi2Cut_;
    int tkNHitsCut_;
    double tkPtCut_;
    double tkIPSigXYCut_;
    double tkIPSigZCut_;
    // cuts on the vertex
    double vtxChi2Cut_;
    double vtxDecaySigXYCut_;
    double vtxDecaySigXYZCut_;
    // miscellaneous cuts
    double tkDCACut_;
    double mPiPiCut_;
    double innerHitPosCut_;
    double cosThetaXYCut_;
    double cosThetaXYZCut_;
    // cuts on the V0 candidate mass
    double kShortMassCut_;
    double lambdaMassCut_;
    bool useVertex_;

     };

#endif

