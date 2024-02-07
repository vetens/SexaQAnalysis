#this file contains common settings used in the BDT scripts and also in the macros to generate plots
import numpy as np

#BDT classifier cut
#BDT_classifier_cut = 0.35
BDT_classifier_cut = -999.0

#matching criteria for the GEN and RECO for the Ks, AntiLambda and AntiS
GENRECO_matcher_AntiS_deltaL = 2.
GENRECO_matcher_AntiS_deltaR = 0.5
GENRECO_matcher_Ks_deltaL = 2.
GENRECO_matcher_Ks_deltaR = 0.03
GENRECO_matcher_AntiL_deltaL = 3.
GENRECO_matcher_AntiL_deltaR = 0.03

#cuts to be applied pre BDT:
pre_BDT_noCut = "Alt$(_S_lxy_interaction_vertex_beampipeCenter,0) < 99999999." #essentially no cut, this is just for testing
#the 3 below cuts are the ones used pre-BDT (see AN for the explanation). The numbering is historical and not necessarily the order in which they are explained in the AN
pre_BDT_cut1 =  "Alt$(_S_lxy_interaction_vertex_beampipeCenter,0) > 2.02 && Alt$(_S_lxy_interaction_vertex_beampipeCenter,0) < 2.4"
pre_BDT_cut3 = "Alt$(_S_dxy_over_lxy,0) >= 0 && Alt$(_S_dxy_over_lxy,0) <= 0.5"
#pre_BDT_cut4 = "(Alt$(_S_daughters_deltaphi,0) < -0.5 || Alt$(_S_daughters_deltaphi,0) > 0.5)"
pre_BDT_cut4 = "(Alt$(_S_daughters_deltaphi,0) < -0.4 || Alt$(_S_daughters_deltaphi,0) > 0.4)"

#pre-BDT cuts also include the fiducial region in which we understand the systematics, this is defined by:
FiducialRegionptMin = 0.33
FiducialRegionptMax = 999999999.

FiducialRegionpzMin = -22.
FiducialRegionpzMax = 22.

FiducialRegiondxyMin = 0.
FiducialRegiondxyMax = 9.5

FiducialRegiondzMin = -27.
FiducialRegiondzMax = 27.

FiducialRegionlxyMax = 44.5

FiducialRegionvzMin = -125.
FiducialRegionvzMax = 125.



#apply the above limits on all 4 final state particles
fiducial_region_cuts = "Alt$(_Lambda_vz_decay_vertex,0) >= "+str(FiducialRegionvzMin)\
+" && Alt$(_Lambda_vz_decay_vertex,0) <= "+str(FiducialRegionvzMax)\
+" && Alt$(_Lambda_lxy_decay_vertex,0) <= "+str(FiducialRegionlxyMax)\
+" && Alt$(_Ks_vz_decay_vertex,0) >= "+str(FiducialRegionvzMin)\
+" && Alt$(_Ks_vz_decay_vertex,0) <= "+str(FiducialRegionvzMax)\
+" && Alt$(_Ks_lxy_decay_vertex,0) <= "+str(FiducialRegionlxyMax)\
+" && Alt$(_RECO_Lambda_daughter0_pt,0) >= "+str(FiducialRegionptMin)\
+" && Alt$(_RECO_Lambda_daughter0_pz,0) >= "+str(FiducialRegionpzMin)\
+" && Alt$(_RECO_Lambda_daughter0_pz,0) <= "+str(FiducialRegionpzMax)\
+" && Alt$(_RECO_Lambda_daughter0_dxy_beamspot,0) >= "+str(FiducialRegiondxyMin)\
+" && Alt$(_RECO_Lambda_daughter0_dxy_beamspot,0) <= "+str(FiducialRegiondxyMax)\
+" && Alt$(_RECO_Lambda_daughter0_dz_min_PV,0) >= "+str(FiducialRegiondzMin)\
+" && Alt$(_RECO_Lambda_daughter0_dz_min_PV,0) <= "+str(FiducialRegiondzMax)\
+" && Alt$(_RECO_Lambda_daughter1_pt,0) >= "+str(FiducialRegionptMin)\
+" && Alt$(_RECO_Lambda_daughter1_pz,0) >= "+str(FiducialRegionpzMin)\
+" && Alt$(_RECO_Lambda_daughter1_pz,0) <= "+str(FiducialRegionpzMax)\
+" && Alt$(_RECO_Lambda_daughter1_dxy_beamspot,0) >= "+str(FiducialRegiondxyMin)\
+" && Alt$(_RECO_Lambda_daughter1_dxy_beamspot,0) <= "+str(FiducialRegiondxyMax)\
+" && Alt$(_RECO_Lambda_daughter1_dz_min_PV,0) >= "+str(FiducialRegiondzMin)\
+" && Alt$(_RECO_Lambda_daughter1_dz_min_PV,0) <= "+str(FiducialRegiondzMax)\
+" && Alt$(_RECO_Ks_daughter0_pt,0) >= "+str(FiducialRegionptMin)\
+" && Alt$(_RECO_Ks_daughter0_pz,0) >= "+str(FiducialRegionpzMin)\
+" && Alt$(_RECO_Ks_daughter0_pz,0) <= "+str(FiducialRegionpzMax)\
+" && Alt$(_RECO_Ks_daughter0_dxy_beamspot,0) >= "+str(FiducialRegiondxyMin)\
+" && Alt$(_RECO_Ks_daughter0_dxy_beamspot,0) <= "+str(FiducialRegiondxyMax)\
+" && Alt$(_RECO_Ks_daughter0_dz_min_PV,0) >= "+str(FiducialRegiondzMin)\
+" && Alt$(_RECO_Ks_daughter0_dz_min_PV,0) <= "+str(FiducialRegiondzMax)\
+" && Alt$(_RECO_Ks_daughter1_pt,0) >= "+str(FiducialRegionptMin)\
+" && Alt$(_RECO_Ks_daughter1_pz,0) >= "+str(FiducialRegionpzMin)\
+" && Alt$(_RECO_Ks_daughter1_pz,0) <= "+str(FiducialRegionpzMax)\
+" && Alt$(_RECO_Ks_daughter1_dxy_beamspot,0) >= "+str(FiducialRegiondxyMin)\
+" && Alt$(_RECO_Ks_daughter1_dxy_beamspot,0) <= "+str(FiducialRegiondxyMax)\
+" && Alt$(_RECO_Ks_daughter1_dz_min_PV,0) >= "+str(FiducialRegiondzMin)\
+" && Alt$(_RECO_Ks_daughter1_dz_min_PV,0) <= "+str(FiducialRegiondzMax)

##additional preselection cuts:
Opt_VzMax = 28.0
Opt_VzMin = -28.0
Opt_DeltaEtaMax = 2
Opt_DeltaEtaMin = -2
Opt_DeltaAlpha_daughters_Max = 2
Opt_DeltaAlpha_daughters_Min = 0.4
Opt_DeltaAlpha_S_Kshort_Max = 1.8
Opt_DeltaAlpha_S_Kshort_Min = 0.1
Opt_DeltaAlpha_S_Lambda_Max = 1.0
Opt_DeltaAlpha_S_Lambda_Min = 0.05
Opt_EtaSMax = 3.5
Opt_EtaSMin = -3.5
Opt_EtaKshortMax = 2.5
Opt_EtaKshortMin = -2.5
Opt_SdzminMax = 6
Opt_SdzminMin = -6
Opt_pTKshortMin = 0.8

additional_preselection = "Alt$(_S_vz_interaction_vertex,0) <= " + str(Opt_VzMax)\
+" && Alt$(_S_vz_interaction_vertex,0) >= " + str(Opt_VzMin)\
+" && Alt$(_S_daughters_deltaeta,0) <= " + str(Opt_DeltaEtaMax)\
+" && Alt$(_S_daughters_deltaeta,0) >= " + str(Opt_DeltaEtaMin)\
+" && Alt$(_S_daughters_openingsangle,0) <= " + str(Opt_DeltaAlpha_daughters_Max)\
+" && Alt$(_S_daughters_openingsangle,0) >= " + str(Opt_DeltaAlpha_daughters_Min)\
+" && Alt$(_S_Ks_openingsangle,0) <= " + str(Opt_DeltaAlpha_S_Kshort_Max)\
+" && Alt$(_S_Ks_openingsangle,0) >= " + str(Opt_DeltaAlpha_S_Kshort_Min)\
+" && Alt$(_S_Lambda_openingsangle,0) <= " + str(Opt_DeltaAlpha_S_Lambda_Max)\
+" && Alt$(_S_Lambda_openingsangle,0) >= " + str(Opt_DeltaAlpha_S_Lambda_Min)\
+" && Alt$(_S_eta,0) <= " + str(Opt_EtaSMax)\
+" && Alt$(_S_eta,0) >= " + str(Opt_EtaSMin)\
+" && Alt$(_Ks_eta,0) <= " + str(Opt_EtaKshortMax)\
+" && Alt$(_Ks_eta,0) >= " + str(Opt_EtaKshortMin)\
+" && Alt$(_S_dz_min,0) <= " + str(Opt_SdzminMax)\
+" && Alt$(_S_dz_min,0) >= " + str(Opt_SdzminMin)\
+" && Alt$(_Ks_pt,0) >= " + str(Opt_pTKshortMin)

#dictionary to load in several macros
config_dict = {
"GENRECO_matcher_AntiS_deltaL":GENRECO_matcher_AntiS_deltaL,
"GENRECO_matcher_AntiS_deltaR":GENRECO_matcher_AntiS_deltaR,
"GENRECO_matcher_Ks_deltaL":GENRECO_matcher_Ks_deltaL,
"GENRECO_matcher_Ks_deltaR":GENRECO_matcher_Ks_deltaR,
"GENRECO_matcher_AntiL_deltaL":GENRECO_matcher_AntiL_deltaL,
"GENRECO_matcher_AntiL_deltaR":GENRECO_matcher_AntiL_deltaR,
"fiducial_region_cuts":fiducial_region_cuts,
"pre_BDT_noCut":pre_BDT_noCut,
"pre_BDT_cut1":pre_BDT_cut1,
"pre_BDT_cut3":pre_BDT_cut3,
"pre_BDT_cut4":pre_BDT_cut4,
"additional_preselection":additional_preselection,
"config_pre_BDT_cuts":fiducial_region_cuts + " && "+pre_BDT_cut4 + " && "+pre_BDT_cut1 + " && " + pre_BDT_cut3 + " && " + additional_preselection,
#"config_pre_BDT_cuts":"",
"BDT_classifier_cut":BDT_classifier_cut ,
"config_SignalFile":"/afs/cern.ch/work/w/wvetens/Sexaquarks/CMSSW_10_2_26/src/SexaQAnalysis/AnalyzerAllSteps/macros/BDT/SignalSbar_FULL.root",
#"config_SignalFile":"root://cmsxrootd.hep.wisc.edu//store/user/wvetens/crmc_Sexaq/FlatTree_BDT/SbarSignalMC_FlatTreeProducerBDT_trial6_1p8GeV_06052023_v3/crab_FlatTreeProducerBDT_trial6_1p8GeV_06052023_v3/230506_140659/0000/output_3.root",
"config_BkgFileData":"/afs/cern.ch/work/w/wvetens/Sexaquarks/CMSSW_10_2_26/src/SexaQAnalysis/AnalyzerAllSteps/macros/BDT/Data_BPH_Full.root",
#"config_BkgFileData":"root://cmsxrootd.hep.wisc.edu//store/user/wvetens/data_Sexaq/FlatTree_BDT/FlatTreeProducerBDT_BPH_FULL_trialA_08052023_v3/crab_FlatTreeProducerBDT_BPH_FULL_trialA_08052023_v3/230508_101423/0000/output_9.root",
"config_BkgFileMC":"/afs/cern.ch/work/w/wvetens/Sexaquarks/CMSSW_10_2_26/src/SexaQAnalysis/AnalyzerAllSteps/macros/BDT/QCD_MC_BG.root",
#"config_BkgFileMC":"root://cmsxrootd.hep.wisc.edu//store/user/wvetens/crmc_Sexaq/FlatTree_BDT/FlatTreeProducerBDT_SQ_In_QCD_Pt-170to300_MuEnrichedPt5_TuneCP5_13TeV_pythia8_08052023_v4/crab_FlatTreeProducerBDT_SQRECO_In_QCDSIM_trial1_08052023_v4/230508_162203/0000/output_24.root",
"config_SelectionSignalAntiS":"Alt$(_S_charge,0) == -1 && Alt$(_S_deltaLInteractionVertexAntiSmin,0) < "+str(GENRECO_matcher_AntiS_deltaL)+" && Alt$(_S_deltaRAntiSmin,0) <"+str(GENRECO_matcher_AntiS_deltaR),
"config_SelectionBkgS":"Alt$(_S_charge,0) == 1",
"config_SelectionBkgAntiS":"Alt$(_S_charge,0) == -1 && Alt$(_S_deltaLInteractionVertexAntiSmin,0) > 10",
"config_SelectionAntiS":"Alt$(_S_charge,0) == -1",
"config_fidRegion_FiducialRegionptMin":FiducialRegionptMin,
"config_fidRegion_FiducialRegionptMax":FiducialRegionptMax,
"config_fidRegion_FiducialRegionpzMin":FiducialRegionpzMin,
"config_fidRegion_FiducialRegionpzMax":FiducialRegionpzMax,
"config_fidRegion_FiducialRegiondxyMin":FiducialRegiondxyMin,
"config_fidRegion_FiducialRegiondxyMax":FiducialRegiondxyMax,
"config_fidRegion_FiducialRegiondzMin":FiducialRegiondzMin,
"config_fidRegion_FiducialRegiondzMax":FiducialRegiondzMax,
"config_fidRegion_FiducialRegionlxyMax":FiducialRegionlxyMax,
"config_fidRegion_FiducialRegionvzMin":FiducialRegionvzMin,
"config_fidRegion_FiducialRegionvzMax":FiducialRegionvzMax
}

variablelist = ["_S_vz_interaction_vertex", 
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
                "_S_chi2_ndof"]

#to calculate the reweighing factor for the pathlength through the beampipe (normally not needed any more as this weigh factor is now also stored in the ntuple):
def calc_reweighing_factor(eta_S,isMCSignal):
        reweighing_factor = 1
        if(isMCSignal):
                theta = 2*np.arctan(np.exp(-eta_S))
                reweighing_factor = 1/np.sin(theta) #the reweiging factor has to scale with the path length of the particle through the beampipe which depends on theta
        return reweighing_factor
