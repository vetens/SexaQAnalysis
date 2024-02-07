#include <cstdlib>
#include <iostream>
#include <map>
#include <string>
#include "TChain.h"
#include "TFile.h"
#include "TTree.h"
#include "TString.h"
#include "TObjString.h"
#include "TSystem.h"
#include "TROOT.h"
#include "TMVA/Factory.h"
#include "TMVA/DataLoader.h"
#include "TMVA/Tools.h"
#include "TMVA/TMVAGui.h"

//std::string version = "dataset_BDT_BPH_Full_TrialB_AllPreSelection_SignalWeighing_PV_MultiToSingle_Eta";
std::string version = "dataset_BDT_BPH_Full_TrialB_AllPreSelection_SignalWeighing_MultiToSingle_Eta_NoPV";
std::vector<std::string> FeatureList = {"_S_vz_interaction_vertex", 
                "_S_lxy_interaction_vertex_beampipeCenter", 
                "_S_daughters_deltaphi",
                "_S_daughters_deltaeta", 
                "_S_daughters_openingsangle",
                "_S_daughters_DeltaR", 
                "_S_Ks_openingsangle", 
                "_S_Lambda_openingsangle", 
                "_S_eta", 
                "_Ks_eta", 
                "_S_dxy_over_lxy", 
                "_Ks_dxy_over_lxy", 
                "_Lambda_dxy_over_lxy", 
                "_S_dz_min",
                "_Ks_dz_min", 
                "_Lambda_dz_min", 
                "_Ks_pt",
                "_Lambda_lxy_decay_vertex",
                "_GEN_S_mass",
                "_S_mass",
                "_S_nGoodPVs",
                "_S_chi2_ndof"};

//std::string SignalFName = "root://cmsxrootd.hep.wisc.edu//store/user/wvetens/crmc_Sexaq/FlatTree_BDT/SbarSignalMC_FlatTreeProducerBDT_trial6_1p8GeV_06052023_v3/crab_FlatTreeProducerBDT_trial6_1p8GeV_06052023_v3/230506_140659/0000/output_3.root";
std::string SignalFName = "/afs/cern.ch/work/w/wvetens/Sexaquarks/CMSSW_10_2_26/src/SexaQAnalysis/AnalyzerAllSteps/macros/BDT/SignalSbar_FULL.root";
//std::string BkgFName = "root://cmsxrootd.hep.wisc.edu//store/user/wvetens/data_Sexaq/FlatTree_BDT/FlatTreeProducerBDT_BPH_FULL_trialA_08052023_v3/crab_FlatTreeProducerBDT_BPH_FULL_trialA_08052023_v3/230508_101423/0000/output_9.root";
std::string BkgFName = "/afs/cern.ch/work/w/wvetens/Sexaquarks/CMSSW_10_2_26/src/SexaQAnalysis/AnalyzerAllSteps/macros/BDT/Data_BPH_Full_trialB.root";

std::string GENRECO_matcher_AntiS_deltaL = "2.0";
std::string GENRECO_matcher_AntiS_deltaR = "0.5";
std::string GENRECO_matcher_Ks_deltaL = "2.0";
std::string GENRECO_matcher_Ks_deltaR = "0.03";
std::string GENRECO_matcher_AntiL_deltaL = "3.0";
std::string GENRECO_matcher_AntiL_deltaR = "0.03";

//cuts to be applied pre BDT:
std::string pre_BDT_noCut = "Alt$(_S_lxy_interaction_vertex_beampipeCenter,0) < 99999999."; //essentially no cut, this is just for testing
//the 3 below cuts are the ones used pre-BDT (see AN for the explanation). The numbering is historical and not necessarily the order in which they are explained in the AN
std::string pre_BDT_cut1 =  "Alt$(_S_lxy_interaction_vertex_beampipeCenter,0) > 2.02 && Alt$(_S_lxy_interaction_vertex_beampipeCenter,0) < 2.4";
std::string pre_BDT_cut3 = "Alt$(_S_dxy_over_lxy,0) >= 0 && Alt$(_S_dxy_over_lxy,0) <= 0.5";
//std::string pre_BDT_cut4 = "(Alt$(_S_daughters_deltaphi,0) < -0.5 || Alt$(_S_daughters_deltaphi,0) > 0.5)"
std::string pre_BDT_cut4 = "(Alt$(_S_daughters_deltaphi,0) < -0.4 || Alt$(_S_daughters_deltaphi,0) > 0.4)";

//pre-BDT cuts also include the fiducial region in which we understand the systematics, this is defined by:
std::vector<std::string> CutVarsList = {"_Lambda_vz_decay_vertex", 
                "_Ks_vz_decay_vertex", 
                "_Ks_lxy_decay_vertex",
                "_RECO_Lambda_daughter0_pt", 
                "_RECO_Lambda_daughter0_pz", 
                "_RECO_Lambda_daughter0_dxy_beamspot", 
                "_RECO_Lambda_daughter0_dz_min_PV", 
                "_RECO_Lambda_daughter1_pt", 
                "_RECO_Lambda_daughter1_pz", 
                "_RECO_Lambda_daughter1_dxy_beamspot", 
                "_RECO_Lambda_daughter1_dz_min_PV", 
                "_RECO_Ks_daughter0_pt", 
                "_RECO_Ks_daughter0_pz", 
                "_RECO_Ks_daughter0_dxy_beamspot", 
                "_RECO_Ks_daughter0_dz_min_PV", 
                "_RECO_Ks_daughter1_pt", 
                "_RECO_Ks_daughter1_pz", 
                "_RECO_Ks_daughter1_dxy_beamspot", 
                "_RECO_Ks_daughter1_dz_min_PV"};
std::string FiducialRegionptMin = "0.33";
std::string FiducialRegionptMax = "999999999.0";

std::string FiducialRegionpzMin = "-22.0";
std::string FiducialRegionpzMax = "22.0";

std::string FiducialRegiondxyMin = "0.0";
std::string FiducialRegiondxyMax = "9.5";

std::string FiducialRegiondzMin = "-27.0";
std::string FiducialRegiondzMax = "27.0";

std::string FiducialRegionlxyMax = "44.5";

std::string FiducialRegionvzMin = "-125.0";
std::string FiducialRegionvzMax = "125.0";

//apply the above limits on all 4 final state particles
std::string fiducial_region_cuts = "Alt$(_Lambda_vz_decay_vertex,0) >= "+FiducialRegionvzMin
+" && Alt$(_Lambda_vz_decay_vertex,0) <= "+FiducialRegionvzMax
+" && Alt$(_Lambda_lxy_decay_vertex,0) <= "+FiducialRegionlxyMax
+" && Alt$(_Ks_vz_decay_vertex,0) >= "+FiducialRegionvzMin
+" && Alt$(_Ks_vz_decay_vertex,0) <= "+FiducialRegionvzMax
+" && Alt$(_Ks_lxy_decay_vertex,0) <= "+FiducialRegionlxyMax
+" && Alt$(_RECO_Lambda_daughter0_pt,0) >= "+FiducialRegionptMin
+" && Alt$(_RECO_Lambda_daughter0_pz,0) >= "+FiducialRegionpzMin
+" && Alt$(_RECO_Lambda_daughter0_pz,0) <= "+FiducialRegionpzMax
+" && Alt$(_RECO_Lambda_daughter0_dxy_beamspot,0) >= "+FiducialRegiondxyMin
+" && Alt$(_RECO_Lambda_daughter0_dxy_beamspot,0) <= "+FiducialRegiondxyMax
+" && Alt$(_RECO_Lambda_daughter0_dz_min_PV,0) >= "+FiducialRegiondzMin
+" && Alt$(_RECO_Lambda_daughter0_dz_min_PV,0) <= "+FiducialRegiondzMax
+" && Alt$(_RECO_Lambda_daughter1_pt,0) >= "+FiducialRegionptMin
+" && Alt$(_RECO_Lambda_daughter1_pz,0) >= "+FiducialRegionpzMin
+" && Alt$(_RECO_Lambda_daughter1_pz,0) <= "+FiducialRegionpzMax
+" && Alt$(_RECO_Lambda_daughter1_dxy_beamspot,0) >= "+FiducialRegiondxyMin
+" && Alt$(_RECO_Lambda_daughter1_dxy_beamspot,0) <= "+FiducialRegiondxyMax
+" && Alt$(_RECO_Lambda_daughter1_dz_min_PV,0) >= "+FiducialRegiondzMin
+" && Alt$(_RECO_Lambda_daughter1_dz_min_PV,0) <= "+FiducialRegiondzMax
+" && Alt$(_RECO_Ks_daughter0_pt,0) >= "+FiducialRegionptMin
+" && Alt$(_RECO_Ks_daughter0_pz,0) >= "+FiducialRegionpzMin
+" && Alt$(_RECO_Ks_daughter0_pz,0) <= "+FiducialRegionpzMax
+" && Alt$(_RECO_Ks_daughter0_dxy_beamspot,0) >= "+FiducialRegiondxyMin
+" && Alt$(_RECO_Ks_daughter0_dxy_beamspot,0) <= "+FiducialRegiondxyMax
+" && Alt$(_RECO_Ks_daughter0_dz_min_PV,0) >= "+FiducialRegiondzMin
+" && Alt$(_RECO_Ks_daughter0_dz_min_PV,0) <= "+FiducialRegiondzMax
+" && Alt$(_RECO_Ks_daughter1_pt,0) >= "+FiducialRegionptMin
+" && Alt$(_RECO_Ks_daughter1_pz,0) >= "+FiducialRegionpzMin
+" && Alt$(_RECO_Ks_daughter1_pz,0) <= "+FiducialRegionpzMax
+" && Alt$(_RECO_Ks_daughter1_dxy_beamspot,0) >= "+FiducialRegiondxyMin
+" && Alt$(_RECO_Ks_daughter1_dxy_beamspot,0) <= "+FiducialRegiondxyMax
+" && Alt$(_RECO_Ks_daughter1_dz_min_PV,0) >= "+FiducialRegiondzMin
+" && Alt$(_RECO_Ks_daughter1_dz_min_PV,0) <= "+FiducialRegiondzMax;

//additional preselection cuts:
std::string Opt_VzMax = "28.0";
std::string Opt_VzMin = "-28.0";
std::string Opt_DeltaEtaMax = "2";
std::string Opt_DeltaEtaMin = "-2";
std::string Opt_DeltaAlpha_daughters_Max = "2";
std::string Opt_DeltaAlpha_daughters_Min = "0.4";
std::string Opt_DeltaAlpha_S_Kshort_Max = "1.8";
std::string Opt_DeltaAlpha_S_Kshort_Min = "0.1";
std::string Opt_DeltaAlpha_S_Lambda_Max = "1.0";
std::string Opt_DeltaAlpha_S_Lambda_Min = "0.05";
std::string Opt_EtaSMax = "3.5";
std::string Opt_EtaSMin = "-3.5";
std::string Opt_EtaKshortMax = "2.5";
std::string Opt_EtaKshortMin = "-2.5";
std::string Opt_SdzminMax = "6";
std::string Opt_SdzminMin = "-6";
std::string Opt_pTKshortMin = "0.8";

std::string additional_preselection = "Alt$(_S_vz_interaction_vertex,0) <= "  + Opt_VzMax
+" && Alt$(_S_vz_interaction_vertex,0) >= "  + Opt_VzMin
+" && Alt$(_S_daughters_deltaeta,0) <= "  + Opt_DeltaEtaMax
+" && Alt$(_S_daughters_deltaeta,0) >= "  + Opt_DeltaEtaMin
+" && Alt$(_S_daughters_openingsangle,0) <= "  + Opt_DeltaAlpha_daughters_Max
+" && Alt$(_S_daughters_openingsangle,0) >= "  + Opt_DeltaAlpha_daughters_Min
+" && Alt$(_S_Ks_openingsangle,0) <= "  + Opt_DeltaAlpha_S_Kshort_Max
+" && Alt$(_S_Ks_openingsangle,0) >= "  + Opt_DeltaAlpha_S_Kshort_Min
+" && Alt$(_S_Lambda_openingsangle,0) <= "  + Opt_DeltaAlpha_S_Lambda_Max
+" && Alt$(_S_Lambda_openingsangle,0) >= "  + Opt_DeltaAlpha_S_Lambda_Min
+" && Alt$(_S_eta,0) <= "  + Opt_EtaSMax
+" && Alt$(_S_eta,0) >= "  + Opt_EtaSMin
+" && Alt$(_Ks_eta,0) <= "  + Opt_EtaKshortMax
+" && Alt$(_Ks_eta,0) >= "  + Opt_EtaKshortMin
+" && Alt$(_S_dz_min,0) <= "  + Opt_SdzminMax
+" && Alt$(_S_dz_min,0) >= "  + Opt_SdzminMin
+" && Alt$(_Ks_pt,0) >= "  + Opt_pTKshortMin;

std::string pre_BDT_cuts = fiducial_region_cuts + " && " + pre_BDT_cut4 + " && " + pre_BDT_cut1 + " && " + pre_BDT_cut3 + " && " + additional_preselection;
//std::string pre_BDT_cuts = "";

std::string SelectionSignalAntiS = "Alt$(_S_charge,0) == -1 && Alt$(_S_deltaLInteractionVertexAntiSmin,0) < "+GENRECO_matcher_AntiS_deltaL+" && Alt$(_S_deltaRAntiSmin,0) < "+GENRECO_matcher_AntiS_deltaR;
std::string SelectionBkgAntiS = "Alt$(_S_charge,0) == -1 && Alt$(_S_deltaLInteractionVertexAntiSmin,0) > 10";

std::string cutSignal = pre_BDT_cuts + " && " + SelectionSignalAntiS;
std::string cutBkg = pre_BDT_cuts + " && " + SelectionBkgAntiS;
//std::string cutSignal = SelectionSignalAntiS;
//std::string cutBkg = SelectionBkgAntiS;
void BDT()
{
    TMVA::Tools::Instance();
    std::cout << std::endl;
    std::cout << "==> Start Data Loading:" << std::endl;

    TFile * SignalFile = TFile::Open(SignalFName.c_str());
    TTree * SignalTree = (TTree*)SignalFile->Get("FlatTreeProducerBDT/FlatTree");
    gROOT->cd();
    SignalTree->Draw(">>SignalElist", cutSignal.c_str(), "SignalEntrylist");
    TEntryList *SignalElist = (TEntryList*)gDirectory->Get("SignalElist");
    SignalTree->SetBranchStatus("*", 0);
    for(unsigned int i=0; i<FeatureList.size(); i++ ){
        SignalTree->SetBranchStatus(FeatureList.at(i).c_str(), 1);
    }
    for(unsigned int i=0; i<CutVarsList.size(); i++ ){
        SignalTree->SetBranchStatus(CutVarsList.at(i).c_str(), 1);
    }
    SignalTree->SetBranchStatus("_S_event_weighting_factorALL", 1);
    SignalTree->SetEntryList(SignalElist);
    auto CutSignalTree = SignalTree->CopyTree("");

    TFile * BkgFile = TFile::Open(BkgFName.c_str());
    TTree * BkgTree = (TTree*)BkgFile->Get("FlatTreeProducerBDT/FlatTree");
    gROOT->cd();
    BkgTree->Draw(">>BkgElist", cutBkg.c_str(), "BkgEntrylist");
    TEntryList *BkgElist = (TEntryList*)gDirectory->Get("BkgElist");
    BkgTree->SetBranchStatus("*", 0);
    for(unsigned int i=0; i<FeatureList.size(); i++ ){
        BkgTree->SetBranchStatus(FeatureList.at(i).c_str(), 1);
    }
    for(unsigned int i=0; i<CutVarsList.size(); i++ ){
        BkgTree->SetBranchStatus(CutVarsList.at(i).c_str(), 1);
    }
    BkgTree->SetBranchStatus("_S_event_weighting_factorALL", 1);
    BkgTree->SetEntryList(BkgElist);
    auto CutBkgTree = BkgTree->CopyTree("");

    std::string trainTestSplit = "0.8";

    TString outputfileName( "BDTOutput_" + version + ".root" );
    TFile* outputFile = TFile::Open (outputfileName, "RECREATE" );

    std::cout << "==> Set Up Factory:" << std::endl;
    TMVA::Factory *factory = new TMVA::Factory("TMVAClassification", outputFile, "!V:!Silent:Color:Transformations=I:AnalysisType=Classification");
    std::string dataloaderName("dataset_BDT_AllFeatures_" + version);
    TMVA::DataLoader *dataloader = new TMVA::DataLoader(dataloaderName.c_str());

    for(unsigned int i=0; i<FeatureList.size(); i++ ){
        std::string varstring( FeatureList.at(i) );
        dataloader->AddVariable(FeatureList.at(i).c_str(), varstring.c_str(), "", 'F');
    }

    Double_t signalWeight     = 1.0;
    Double_t backgroundWeight = 1.0;

    dataloader->AddSignalTree    (CutSignalTree, signalWeight    );
    dataloader->AddBackgroundTree(CutBkgTree   , backgroundWeight);
    dataloader->SetSignalWeightExpression("_S_event_weighting_factorALL");

    std::string dataloaderSplit( "TrainTestSplit_Signal="+trainTestSplit+":TrainTestSplit_Background="+trainTestSplit+":SplitMode=Random");
    dataloader->PrepareTrainingAndTestTree( TCut(pre_BDT_cuts.c_str()),dataloaderSplit.c_str() );
    //dataloader->PrepareTrainingAndTestTree( TCut(""),dataloaderSplit.c_str() );

    std::cout << "==> Begin Booking Method:" << std::endl;
    /*auto BDTMethod = */factory->BookMethod( dataloader, TMVA::Types::kBDT, "BDT", "H:!V:VarTransform=None:NTrees=400:BoostType=AdaBoost:SeparationType=GiniIndex:nCuts=20:PruneMethod=CostComplexity:PruneStrength=12:UseBaggedBoost=True" );

    std::cout << "==> Begin Training:" << std::endl;
    factory->TrainAllMethods();
    //for(unsigned int i=0; i<FeatureList.size(); i++ ){
    //    std::string varstring( FeatureList.at(i) );
    //    std::cout << BDTMethod->GetVariableImportance(varstring.c_str()) << std::endl;
    //}
    std::cout << "==> Begin Testing:" << std::endl;
    factory->TestAllMethods();
    std::cout << "==> Begin Evaluation:" << std::endl;
    factory->EvaluateAllMethods();
    
    TCanvas canvas = factory->GetROCCurve(dataloader);
    canvas.Draw();
    std::string ROCCurveName( "BDT_ROCcurve_2023_"+version+".root" );
    canvas.SaveAs(ROCCurveName.c_str());
    outputFile->Close();
    delete factory;
    delete dataloader;
    
    if (!gROOT->IsBatch()) TMVA::TMVAGui( outputfileName );

    return;
}
