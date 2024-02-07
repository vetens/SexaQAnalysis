#script to overlap for signal MC and different background samples the distributions of the variables used in the BDT for different steps after doing the pre-BDT cuts
#So, first you have to prepare for a certain configuration of the pre-BDT cuts the ntuples to which a brach with the BDT classifier has been added. This can be done with the src/SexaQAnalysis/TMVA/Step2/DiscrApplication.py

#from ROOT import TFile, TH1F, TH2F, TEfficiency, TH1D, TH2D, TCanvas, gROOT
import ROOT
from ROOT import *
import numpy as np
import sys
sys.path.append('/afs/cern.ch/work/w/wvetens/Sexaquarks/CMSSW_10_2_26/src/SexaQAnalysis/AnalyzerAllSteps/macros/tdrStyle')
import  CMS_lumi, tdrstyle

import sys
sys.path.insert(1, '../')
import configBDT as config

config_dict = config.config_dict

gROOT.SetBatch(kTRUE)
gStyle.SetLegendTextSize(0.08)

CMS_lumi.writeExtraText = 1
CMS_lumi.extraText = "CMS work in progress"
tdrstyle.setTDRStyle()


maxEvents = 1e12

applyFiducial = True
#applyFiducial = False
applyPreselection = True
apply_optional_Preselection = True
#applyPreselection = False
#apply_optional_Preselection = False


l_y_axis_ranges = [
0.07,                   #nGoodPVs
0.1,                    #S_vz_interaction_vertex
13,                     #S_lxy_interaction_vertex
1.5,                    #S_daughters_deltaphi
1,                      #S_daughters_deltaeta
2.6,                    #S_daughters_openingsangle
1.5,                    #S_daughters_DeltaR
2.5,                    #S_Ks_openingsangle
3.5,                    #S_Lambda_openingsangle
0.75,                   #S_eta
0.85,                   #Ks_eta
30,                     #S_dxy_over_lxy
15,                     #Ks_dxy_over_lxy
15,                     #Lambda_dxy_over_lxy
10,                     #S_dz_min
5,                      #Ks_dz_min
5,                      #Lambda_dz_min
1.6,                    #Ks_pt
0.2,                    #Lambda_lxy_decay_vertex
3,                      #S_chi2_ndof
0.85,                   #S_mass
33,                     #GEN_S_mass
100                     #BDT Classifier y-axis range
]

#the below is a bit historical, it is by default "all" now
configuration = "all"
#cut on the BDT parameter to select a minimal BDT, to go and look in the tail of the BDT distribution (towards the signal), put to -999 if you want all the events
min_BDT_classifier = -999. #-999 or -0.15


MC_Signal_Truth_cutoff_deltaR = 0.5
MC_Signal_Truth_cutoff_deltaL = 2.0

### BDT APPLIED #################################################################################

MC_AntiS_Sgn_File_M2SReweigh_AllMass = ROOT.TFile.Open("/afs/cern.ch/work/w/wvetens/Sexaquarks/CMSSW_10_2_26/src/SexaQAnalysis/TMVA/Step2/BDTApplied_unblindMC_dataset_BDT_AllFeatures_dataset_BDT_BPH_Full_AllPreSelection_SignalWeighing_PV_MultiToSingle_Eta_OverlapCheckFalse/DiscrApplied_SignalSbar_FULL.root")
MC_AntiS_Sgn_Tree_M2SReweigh_AllMass = MC_AntiS_Sgn_File_M2SReweigh_AllMass.Get("FlatTree")

#MC S BKG from QCD MuEnriched sample 
MC_S_Bkg_File = ROOT.TFile.Open("/afs/cern.ch/work/w/wvetens/Sexaquarks/CMSSW_10_2_26/src/SexaQAnalysis/TMVA/Step2/BDTApplied_bkgReference_dataset_BDT_AllFeatures_dataset_BDT_BPH_Full_AllPreSelection_SignalWeighing_PV_MultiToSingle_Eta_OverlapCheckFalse/DiscrApplied_QCD_MC_BG.root")
MC_S_Bkg_Tree = MC_S_Bkg_File.Get("FlatTree")

#MC Sbar BKG from QCD MuEnriched sample
MC_AntiS_Bkg_File = ROOT.TFile.Open("/afs/cern.ch/work/w/wvetens/Sexaquarks/CMSSW_10_2_26/src/SexaQAnalysis/TMVA/Step2/BDTApplied_unblindMC_BG_dataset_BDT_AllFeatures_dataset_BDT_BPH_Full_AllPreSelection_SignalWeighing_PV_MultiToSingle_Eta_OverlapCheckFalse/DiscrApplied_QCD_MC_BG.root")
MC_AntiS_Bkg_Tree = MC_AntiS_Bkg_File.Get("FlatTree")

#MC Xevt Bkg from QCD MuEnriched sample
MC_Xevt_AntiS_Bkg_File = ROOT.TFile.Open("/afs/cern.ch/work/w/wvetens/Sexaquarks/CMSSW_10_2_26/src/SexaQAnalysis/TMVA/Step2/BDTApplied_unblindMC_BG_dataset_BDT_AllFeatures_dataset_BDT_BPH_Full_AllPreSelection_SignalWeighing_PV_MultiToSingle_Eta_OverlapCheckFalse/DiscrApplied_QCD_MC_Xevt.root")
MC_Xevt_AntiS_Bkg_Tree = MC_Xevt_AntiS_Bkg_File.Get("FlatTree")
MC_Xevt_S_Bkg_File = ROOT.TFile.Open("/afs/cern.ch/work/w/wvetens/Sexaquarks/CMSSW_10_2_26/src/SexaQAnalysis/TMVA/Step2/BDTApplied_bkgReference_dataset_BDT_AllFeatures_dataset_BDT_BPH_Full_AllPreSelection_SignalWeighing_PV_MultiToSingle_Eta_OverlapCheckFalse/DiscrApplied_QCD_MC_Xevt.root")
MC_Xevt_S_Bkg_Tree = MC_Xevt_S_Bkg_File.Get("FlatTree")

#Data Xevt Bkg from Bparking UL 2018
Data_Sbar_Xevt_Bkg_File = ROOT.TFile.Open("/afs/cern.ch/work/w/wvetens/Sexaquarks/CMSSW_10_2_26/src/SexaQAnalysis/TMVA/Step2/BDTApplied_unblind_dataset_BDT_AllFeatures_dataset_BDT_BPH_Full_AllPreSelection_SignalWeighing_PV_MultiToSingle_Eta_OverlapCheckFalse/DiscrApplied_Data_BPH_Xevt.root")
Data_Sbar_Xevt_Bkg_Tree = Data_Sbar_Xevt_Bkg_File.Get("FlatTree")
Data_S_Xevt_Bkg_File = ROOT.TFile.Open("/afs/cern.ch/work/w/wvetens/Sexaquarks/CMSSW_10_2_26/src/SexaQAnalysis/TMVA/Step2/BDTApplied_bkgReference_dataset_BDT_AllFeatures_dataset_BDT_BPH_Full_AllPreSelection_SignalWeighing_PV_MultiToSingle_Eta_OverlapCheckFalse/DiscrApplied_Data_BPH_Xevt.root")
Data_S_Xevt_Bkg_Tree = Data_S_Xevt_Bkg_File.Get("FlatTree")

#Data S Bkg from Bparking UL 2018
Data_S_Bkg_File = ROOT.TFile.Open("/afs/cern.ch/work/w/wvetens/Sexaquarks/CMSSW_10_2_26/src/SexaQAnalysis/TMVA/Step2/BDTApplied_bkgReference_dataset_BDT_AllFeatures_dataset_BDT_BPH_Full_AllPreSelection_SignalWeighing_PV_MultiToSingle_Eta_OverlapCheckFalse/DiscrApplied_Data_BPH_Full.root")
Data_S_Bkg_Tree = Data_S_Bkg_File.Get("FlatTree")

#Data Sbar Bkg BDT CLASSIFIER < 0.1 from Bparking UL 2018
Data_Sbar_Bkg_File = ROOT.TFile.Open("/afs/cern.ch/work/w/wvetens/Sexaquarks/CMSSW_10_2_26/src/SexaQAnalysis/TMVA/Step2/BDTApplied_partialUnblinding_dataset_BDT_AllFeatures_dataset_BDT_BPH_Full_AllPreSelection_SignalWeighing_PV_MultiToSingle_Eta_OverlapCheckFalse/DiscrApplied_Data_BPH_Full.root")
Data_Sbar_Bkg_Tree = Data_Sbar_Bkg_File.Get("FlatTree")
#################################################################################################

#Legend = ["MC-S-BKG"   ,"MC-#bar{S}-BKG" ,"Data-S-BKG"   ,"Data-#bar{S}-BKG (BDT < 0.1)  ","Data-#bar{S}-X event BKG" ,"MC-#bar{S}-Signal"]
#l_tree = [MC_S_Bkg_Tree,MC_AntiS_Bkg_Tree,Data_S_Bkg_Tree,Data_AntiS_Bkg_Tree             , Data_AntiS_XEvent_Tree    , MC_AntiS_Sgn_Tree]
#Legend = ["Data-S-BKG"   ,"Data-#bar{S}-X event BKG" ,"MC-#bar{S}-Signal"]
#l_tree = [Data_S_Bkg_Tree, Data_AntiS_XEvent_Tree    , MC_AntiS_Sgn_Tree]

#For Data S BG to Signal MC
#colours = [4,2,35,30]
#markerStyle = [20, 21, 22, 23]
#Legend = ["MC-S-BKG"   ,"MC-#bar{S}-BKG" ,"Data-S-BKG"   ,"MC-AllMass-Multi-to-Single-Reweighed-#bar{S}-Signal"]
#l_tree = [MC_S_Bkg_Tree,MC_AntiS_Bkg_Tree,Data_S_Bkg_Tree,MC_AntiS_Sgn_Tree_M2SReweigh_AllMass                 ]
colours = [4,2,38,46,5,3,41,30,1]
markerStyle = [20,20,24,24,21,21,25,25,23]
Legend = ["MC-S-BKG"   ,"MC-#bar{S}-BKG" ,"MC-S-Xevt-BKG"   ,"MC-#bar{S}-Xevt-BKG" ,"Data-S-BKG"   ,"Data-#bar{S}-BDT<0.1-BKG","Data-S-Xevt-BKG"   ,"Data-#bar{S}-Xevt-BKG","MC-AllMass-Multi-to-Single-Reweighed-#bar{S}-Signal"]
l_tree = [MC_S_Bkg_Tree,MC_AntiS_Bkg_Tree,MC_Xevt_S_Bkg_Tree,MC_Xevt_AntiS_Bkg_Tree,Data_S_Bkg_Tree,Data_Sbar_Bkg_Tree        ,Data_S_Xevt_Bkg_Tree,Data_Sbar_Xevt_Bkg_Tree, MC_AntiS_Sgn_Tree_M2SReweigh_AllMass                ]

#For comparisons of different GEN masses to the full sample:
#colours = [30,43,1,6,20,25]
#markerStyle = [23,21,22,24,25,26]
#Legend = ["MC-1.8GeV-Multi-to-Single-Reweighed-#bar{S}-Signal"         ,"MC-1.7GeV-Multi-to-Single-Reweighed-#bar{S}-Signal"         ,"MC-1.85GeV-Multi-to-Single-Reweighed-#bar{S}-Signal"         ,"MC-1.9GeV-Multi-to-Single-Reweighed-#bar{S}-Signal"         ,"MC-2GeV-Multi-to-Single-Reweighed-#bar{S}-Signal"         ,"MC-AllMass-Multi-to-Single-Reweighed-#bar{S}-Signal"         ]
#l_tree = [MC_AntiS_Sgn_Tree_M2SReweigh_1p8GeV                          ,MC_AntiS_Sgn_Tree_M2SReweigh_1p7GeV                          ,MC_AntiS_Sgn_Tree_M2SReweigh_1p85GeV                          ,MC_AntiS_Sgn_Tree_M2SReweigh_1p9GeV                          ,MC_AntiS_Sgn_Tree_M2SReweigh_2GeV                          ,MC_AntiS_Sgn_Tree_M2SReweigh_AllMass                          ]

#For MC QCD BG to Data S BG to MC Signal
#colours = [4,2,35,30,43,1,6]
#markerStyle = [20,21,22,23,33,34,35]
#Legend = ["MC-S-BKG"   ,"MC-#bar{S}-BKG","Data-S-BKG"   ,"MC-Multi-to-Single-Reweighed-#bar{S}-Signal"]
#l_tree = [MC_S_Bkg_Tree,MC_Sbar_Bkg_Tree,Data_S_Bkg_Tree,MC_AntiS_Sgn_Tree_M2SReweigh_AllMass         ]

#subdir = "BackgroundVsSignal/"
#subdir = "GENMass_comparison/"
#subdir = "NoCuts/"
#subdir = ""
#plots_output_dir = "plots_BDTApplied/"+subdir
plots_output_dir = "plots_BDTApplied/"

FiducialRegionptMin = 0.33
FiducialRegionptMax = 999999999.
FiducialRegionpzMax = 22.
FiducialRegiondxyMin = 0.
FiducialRegiondxyMax = 9.5
FiducialRegiondzMax = 27.
FiducialRegionlxyMax = 44.5
FiducialRegionvzMax = 125.
fiducialCuts = {
"Lambda v_z decay vertex":"abs(tree._Lambda_vz_decay_vertex[0]) <= FiducialRegionvzMax",
"Lambda l_xy decay vertex":"tree._Lambda_lxy_decay_vertex[0] <= FiducialRegionlxyMax",
"Lambda Daughter 0 p_T":"tree._RECO_Lambda_daughter0_pt[0] <= FiducialRegionptMax and tree._RECO_Lambda_daughter0_pt[0] >= FiducialRegionptMin",
"Lambda Daughter 1 p_T":"tree._RECO_Lambda_daughter1_pt[0] <= FiducialRegionptMax and tree._RECO_Lambda_daughter1_pt[0] >= FiducialRegionptMin",
"Lambda Daughter 0 p_z":"abs(tree._RECO_Lambda_daughter0_pt[0]) <= FiducialRegionpzMax",
"Lambda Daughter 1 p_z":"abs(tree._RECO_Lambda_daughter1_pt[0]) <= FiducialRegionpzMax",
"Lambda Daughter 0 d_xy beamspot":"tree._RECO_Lambda_daughter0_dxy_beamspot[0] <= FiducialRegiondxyMax and tree._RECO_Lambda_daughter0_dxy_beamspot[0] >= FiducialRegiondxyMin",
"Lambda Daughter 1 d_xy beamspot":"tree._RECO_Lambda_daughter1_dxy_beamspot[0] <= FiducialRegiondxyMax and tree._RECO_Lambda_daughter1_dxy_beamspot[0] >= FiducialRegiondxyMin",
"Lambda Daughter 0 d_z Best PV":"abs(tree._RECO_Lambda_daughter0_dz_min_PV[0]) <= FiducialRegiondzMax",
"Lambda Daughter 1 d_z Best PV":"abs(tree._RECO_Lambda_daughter1_dz_min_PV[0]) <= FiducialRegiondzMax",
"K_s v_z decay vertex":"abs(tree._Ks_vz_decay_vertex[0]) <= FiducialRegionvzMax",
"K_s l_xy decay vertex":"tree._Ks_lxy_decay_vertex[0] <= FiducialRegionlxyMax",
"K_s Daughter 0 p_T":"tree._RECO_Ks_daughter0_pt[0] <= FiducialRegionptMax and tree._RECO_Ks_daughter0_pt[0] >= FiducialRegionptMin",
"K_s Daughter 1 p_T":"tree._RECO_Ks_daughter1_pt[0] <= FiducialRegionptMax and tree._RECO_Ks_daughter1_pt[0] >= FiducialRegionptMin",
"K_s Daughter 0 p_z":"abs(tree._RECO_Ks_daughter0_pt[0]) <= FiducialRegionpzMax",
"K_s Daughter 1 p_z":"abs(tree._RECO_Ks_daughter1_pt[0]) <= FiducialRegionpzMax",
"K_s Daughter 0 d_xy beamspot":"tree._RECO_Ks_daughter0_dxy_beamspot[0] <= FiducialRegiondxyMax and tree._RECO_Ks_daughter0_dxy_beamspot[0] >= FiducialRegiondxyMin",
"K_s Daughter 1 d_xy beamspot":"tree._RECO_Ks_daughter1_dxy_beamspot[0] <= FiducialRegiondxyMax and tree._RECO_Ks_daughter1_dxy_beamspot[0] >= FiducialRegiondxyMin",
"K_s Daughter 0 d_z Best PV":"abs(tree._RECO_Ks_daughter0_dz_min_PV[0]) <= FiducialRegiondzMax",
"K_s Daughter 1 d_z Best PV":"abs(tree._RECO_Ks_daughter1_dz_min_PV[0]) <= FiducialRegiondzMax"
}

Presel_DeltaPhiMin = 0.4
Presel_LxyInteractionVertexMin = 2.02
Presel_LxyInteractionVertexMax = 2.40
Presel_dxyOverLxyMin = 0
Presel_dxyOverLxyMax = 0.5
preselectionCuts = {
"S Daughters delta phi":"abs(tree._S_daughters_deltaphi[0]) >= Presel_DeltaPhiMin",
"S l_xy interaction vertex to beampipe center":"tree._S_lxy_interaction_vertex_beampipeCenter[0] >= Presel_LxyInteractionVertexMin and tree._S_lxy_interaction_vertex_beampipeCenter[0] <= Presel_LxyInteractionVertexMax",
"S d_xy/l_xy":"tree._S_dxy_over_lxy[0] >= Presel_dxyOverLxyMin and tree._S_dxy_over_lxy[0] <= Presel_dxyOverLxyMax"
}

Opt_VzMax = 28.0
Opt_DeltaEtaMax = 2
Opt_DeltaAlpha_daughters_Max = 2
Opt_DeltaAlpha_daughters_Min = 0.4
Opt_DeltaAlpha_S_Kshort_Max = 1.8
Opt_DeltaAlpha_S_Kshort_Min = 0.1
Opt_DeltaAlpha_S_Lambda_Max = 1.0
Opt_DeltaAlpha_S_Lambda_Min = 0.05
Opt_EtaSMax = 3.5
Opt_EtaKshortMax = 2.5
Opt_SdzminMax = 6
Opt_pTKshortMin = 0.8
optionalPreselectionCuts = {
"S v_z interaction vertex":"abs(tree._S_vz_interaction_vertex[0]) <= Opt_VzMax",
"Delta eta of S daughters":"abs(tree._S_daughters_deltaeta[0]) <= Opt_DeltaEtaMax",
"3D Openingsangle of S daughters":"tree._S_daughters_openingsangle[0] <= Opt_DeltaAlpha_daughters_Max and tree._S_daughters_openingsangle[0] >= Opt_DeltaAlpha_daughters_Min",
"3D Openingsangle of S and Ks":"tree._S_Ks_openingsangle[0] <= Opt_DeltaAlpha_S_Kshort_Max and tree._S_Ks_openingsangle[0] >= Opt_DeltaAlpha_S_Kshort_Min",
"3D Openingsangle of S and Lambda":"tree._S_Lambda_openingsangle[0] <= Opt_DeltaAlpha_S_Lambda_Max and tree._S_Lambda_openingsangle[0] >= Opt_DeltaAlpha_S_Lambda_Min",
"S eta":"abs(tree._S_eta[0]) <= Opt_EtaSMax",
"K_s eta":"abs(tree._Ks_eta[0]) <= Opt_EtaKshortMax",
"minimum impact parameter of S":"abs(tree._S_dz_min[0]) <= Opt_SdzminMax",
"K_s p_T":"tree._Ks_pt[0] >= Opt_pTKshortMin"
}
TH1_ll = [] #list of list of 1D histos 
TH2_ll = [] #list of list of 2D histos

iTree = 0
nSbar = 0
for tree in l_tree:

        print "Processing: ", Legend[iTree]
	gROOT.cd()
	nEntries1 = tree.GetEntries()
        nFiducialPass = 0
	print "---------------------------------------------------"
	print "running for ", Legend[iTree]
	h_S_nGoodPVs = TH1F('h_S_nGoodPVs','; Number of Primary Vertices; 1/N_{ev} Events/3cm',60,0,60)

	h_S_vz_interaction_vertex= TH1F('h_S_vz_interaction_vertex','; absolute v_{z} iv ^{(}#bar{S} ^{)} (cm); 1/N_{ev} Events/cm',60,-30,30)
	h_S_lxy_interaction_vertex = TH1F('h_S_lxy_interaction_vertex','; l_{0,bpc} iv ^{(}#bar{S} ^{)} (cm); 1/N_{ev} Events/0.01mm',38,2.02,2.4)

	h_S_daughters_deltaphi = TH1F('h_S_daughters_deltaphi','; #Delta#phi( ^{(} #bar{#Lambda} ^{)} ^{0} , K_{S}^{0}) (rad); 1/N_{ev} Events/0.2rad',32,-3.2,3.2)
	h_S_daughters_deltaeta = TH1F('h_S_daughters_deltaeta','; #Delta#eta( ^{(} #bar{#Lambda} ^{)} ^{0} , K_{S}^{0}) ; 1/N_{ev} Events/0.2rad',21,-2.1,2.1)
	h_S_daughters_openingsangle = TH1F('h_S_daughters_openingsangle','; openings angle( ^{(} #bar{#Lambda} ^{)} ^{0} , K_{S}^{0} ) (rad); 1/N_{ev} Events/0.05rad',34,0.4,2.1)
	h_S_daughters_DeltaR = TH1F('h_S_daughters_DeltaR','; #DeltaR( ^{(} #bar{#Lambda} ^{)} ^{0} , K_{S}^{0} ); 1/N_{ev} Events/0.1rad',35,0.5,4)
	h_S_Ks_openingsangle = TH1F('h_S_Ks_openingsangle','; openings angle( ^{(} #bar{S} ^{)} , K_{S}^{0}) (rad); 1/N_{ev} Events/0.1rad',20,0,2)
	h_S_Lambda_openingsangle = TH1F('h_S_Lambda_openingsangle','; openings angle( ^{(} #bar{#Lambda} ^{)} ^{0} ,  ^{(} #bar{S} ^{)} ) (rad); 1/N_{ev} Events/0.05rad',20,0,1)

	h_S_eta = TH1F('h_S_eta','; #eta( ^{(} #bar{S} ^{)} ); 1/N_{ev} Events/0.25rad',38,-3.5,3.5)
	h_Ks_eta = TH1F('h_Ks_eta','; #eta(K_{S}^{0}) ; 1/N_{ev} Events/0.25rad',20,-2.5,2.5)

	h_S_dxy_over_lxy = TH1F('h_S_dxy_over_lxy','; d_{0,bs}/l_{0,bs} ( ^{(} #bar{S} ^{)} ); 1/N_{ev} Events/0.025',20,0,0.5)
	h_Ks_dxy_over_lxy = TH1F('h_Ks_dxy_over_lxy','; d_{0,bs}/l_{0,bs} (K_{S}^{0}); 1/N_{ev} Events/0.1',20,-1,1)
	h_Lambda_dxy_over_lxy = TH1F('h_Lambda_dxy_over_lxy','; d_{0,bs}/l_{0,bs} ( ^{(} #bar{#Lambda} ^{)} ^{0}) ; 1/N_{ev} Events/0.1',20,-1,1)

	h_S_dz_min = TH1F('h_S_dz_min','; min d_{z,bs}  ^{(} #bar{S} ^{)}  (cm); 1/N_{ev} Events/0.5cm',24,-6,6)
	h_Ks_dz_min = TH1F('h_Ks_dz_min','; min d_{z,bs} K_{S}^{0} (cm); 1/N_{ev} Events/cm',60,-30,30)
	h_Lambda_dz_min = TH1F('h_Lambda_dz_min','; min d_{z,bs}  ^{(} #bar{#Lambda} ^{)} ^{0}  (cm); 1/N_{ev} Events/cm',60,-30,30)

	h_Ks_pt = TH1F('h_Ks_pt','; p_{t} K_{S}^{0} (GeV/c); 1/N_{ev} Events/0.4GeV/c',20,0,8)

	h_Lambda_lxy_decay_vertex = TH1F('h_Lambda_lxy_decay_vertex','; l_{0} ^{(} #bar{#Lambda} ^{)} ^{0} decay vertex (cm); 1/N_{ev} Events/cm',20,1.9,21.9)
	h_S_chi2_ndof = TH1F('h_S_chi2_ndof','; #chi^{2}/ndof ^{(}#bar{S} ^{)} annihilation vertex; 1/N_{ev} Events',44,0,11)

	h_S_mass = TH1F('h_S_mass','; m_{ ^{(} #bar{S} ^{)} ,obs} (GeV/c^{2}); 1/N_{ev} Events/0.25GeV/c^{2}',40,-5,5)
	h_GEN_S_mass = TH1F('h_GEN_S_mass','; m_{ ^{(} #bar{S} ^{)} ,GEN} (GeV/c^{2}); 1/N_{ev} Events/10MeV/c^{2}',50,1.6,2.1)


	h_S_BDT = TH1F('h_S_BDT','; BDT classifier; 1/N_{ev} Events/0.05 BDT class.',40,-1,1)

        if('#bar{S}-Signal' in Legend[iTree] or 'MC-Multi-#bar{S}-Signal' in Legend[iTree] or 'Multi-to-Single-Reweighed-#bar{S}-Signal' in Legend[iTree]): #if MC signal reweigh both for the pathlength through the beampipe and for the z location of the PV and PU
            print "N entries:", nEntries1
	for i in range(0,nEntries1):
		if(i==maxEvents):
			break
		if(i%1e4 == 0):
			print "reached entry: ", i
		tree.GetEntry(i)
		#if(i==0): print 'charge of the S/antiS: ', tree._S_charge[0]
		
		#for when you have the BDT parameter in your tree:
		#if(tree.SexaqBDT <= min_BDT_classifier):continue

                ###OLD
		###need to reweigh the MC signal events, because the ones with high eta are more important, because they will pass more material
		##reweighing_factor = config.calc_reweighing_factor(tree._S_eta[0],'MC-#bar{S}-Signal' in Legend[iTree])
		reweighing_factor = 1
		if('#bar{S}-Signal' in Legend[iTree] or 'MC-Multi-#bar{S}-Signal' in Legend[iTree] or 'Multi-to-Single-Reweighed-#bar{S}-Signal' in Legend[iTree]): #if MC signal reweigh both for the pathlength through the beampipe and for the z location of the PV and PU
                        nSbar+=1
                        if(tree._S_deltaLInteractionVertexAntiSmin[0] > MC_Signal_Truth_cutoff_deltaL and tree._S_deltaRAntiSmin[0] > MC_Signal_Truth_cutoff_deltaR): 
                            #print tree._S_deltaLInteractionVertexAntiSmin[0]
                            continue
                        if ('Multi-to-Single' in Legend[iTree]):
			    reweighing_factor = tree._S_event_weighting_factor[0]*tree._S_event_weighting_factorPU[0]*tree._S_event_weighting_factorM2S[0]
			    #reweighing_factor = tree._S_event_weighting_factor[0]*tree._S_event_weighting_factorM2S[0]
                        else:
			    reweighing_factor = tree._S_event_weighting_factor[0]*tree._S_event_weighting_factorPU[0]
			    #reweighing_factor = tree._S_event_weighting_factor[0]
		#elif('MC-S-BKG' in Legend[iTree] or 'MC-#bar{S}-BKG' or 'MC-#bar{S}-Xevt-BKG' in Legend[iTree]):#if MC background only reweigh for the z location of the PV and PU
		#	reweighing_factor = tree._S_event_weighting_factorPU[0]
                # for the S background we want to look at S, otherwise we want to look at Sbar
                if(('Data-S-BKG' in Legend[iTree] or 'MC-S-BKG' in Legend[iTree]) and tree._S_charge[0] == -1): 
                    continue
                elif(tree._S_charge[0] == 1 and '#bar{S}' in Legend[iTree]): continue

                #FIDUCIAL CUTS
                fiducialPassed = True
                preselPassed = True
                optpreselPassed = True
                if( applyFiducial ):
                    for title, cut in fiducialCuts.items():
                        if( fiducialPassed and not eval(cut)):
                            fiducialPassed = False
                            break
                        else: continue
                    if( applyPreselection and fiducialPassed ): 
                        for title, cut in preselectionCuts.items():
                            if( preselPassed and not eval(cut) ):
                                preselPassed = False
                                break
                            else: continue
                        if( apply_optional_Preselection and preselPassed ): 
                            for title, cut in optionalPreselectionCuts.items():
                                if( optpreselPassed and not eval(cut) ):
                                    optpreselPassed = False
                                    break
                                else: continue
                passedPreCuts = fiducialPassed and preselPassed and optpreselPassed
                if not passedPreCuts: continue

                nFiducialPass += 1

		h_S_nGoodPVs.Fill(tree._S_nGoodPVs[0],reweighing_factor)

		h_S_vz_interaction_vertex.Fill(tree._S_vz_interaction_vertex[0],reweighing_factor)
		h_S_lxy_interaction_vertex.Fill(tree._S_lxy_interaction_vertex_beampipeCenter[0],reweighing_factor)

		h_S_daughters_deltaphi.Fill(tree._S_daughters_deltaphi[0],reweighing_factor)
		h_S_daughters_deltaeta.Fill(tree._S_daughters_deltaeta[0],reweighing_factor)
		h_S_daughters_openingsangle.Fill(tree._S_daughters_openingsangle[0],reweighing_factor)
		h_S_daughters_DeltaR.Fill(tree._S_daughters_DeltaR[0],reweighing_factor)
		h_S_Ks_openingsangle.Fill(tree._S_Ks_openingsangle[0],reweighing_factor)
		h_S_Lambda_openingsangle.Fill(tree._S_Lambda_openingsangle[0],reweighing_factor)

		h_S_eta.Fill(tree._S_eta[0],reweighing_factor)
		h_Ks_eta.Fill(tree._Ks_eta[0],reweighing_factor)

		h_S_dxy_over_lxy.Fill(tree._S_dxy_over_lxy[0],reweighing_factor)
		h_Ks_dxy_over_lxy.Fill(tree._Ks_dxy_over_lxy[0],reweighing_factor)
		h_Lambda_dxy_over_lxy.Fill(tree._Lambda_dxy_over_lxy[0],reweighing_factor)

		h_S_dz_min.Fill(tree._S_dz_min[0],reweighing_factor)
		h_Ks_dz_min.Fill(tree._Ks_dz_min[0],reweighing_factor)
		h_Lambda_dz_min.Fill(tree._Lambda_dz_min[0],reweighing_factor)

		h_Ks_pt.Fill(tree._Ks_pt[0],reweighing_factor)
		
		h_Lambda_lxy_decay_vertex.Fill(tree._Lambda_lxy_decay_vertex[0],reweighing_factor)
		h_S_chi2_ndof.Fill(tree._S_chi2_ndof[0],reweighing_factor)

		h_S_mass.Fill(tree._S_mass[0],reweighing_factor)
                if "Xevt" in Legend[iTree]:
                    #This difference is because for the X-event samples I added in the GEN masses in post to save on computing time, so they should be handled like the BDT Parameter
		    h_GEN_S_mass.Fill(round(tree._GEN_S_mass,2),reweighing_factor)
                else:
		    h_GEN_S_mass.Fill(round(tree._GEN_S_mass[0],2),reweighing_factor)
		h_S_BDT.Fill(tree.SexaqBDT,reweighing_factor)
# For now, not doing the h_S_BDT
        TH1_l = []
	#TH1_l = [h_S_BDT]
	TH1_l = [h_S_nGoodPVs, h_S_vz_interaction_vertex,h_S_lxy_interaction_vertex,h_S_daughters_deltaphi,h_S_daughters_deltaeta,h_S_daughters_openingsangle,h_S_daughters_DeltaR,h_S_Ks_openingsangle,h_S_Lambda_openingsangle,h_S_eta,h_Ks_eta,h_S_dxy_over_lxy,h_Ks_dxy_over_lxy,h_Lambda_dxy_over_lxy,h_S_dz_min,h_Ks_dz_min,h_Lambda_dz_min,h_Ks_pt,h_Lambda_lxy_decay_vertex,h_S_chi2_ndof,h_S_mass,h_GEN_S_mass,h_S_BDT]
	#TH1_l = [h_S_nGoodPVs, h_S_bestPVz]
	for h in TH1_l:
		h.SetDirectory(0) 
	TH1_ll.append(TH1_l)


        print "Efficiency of cuts in ", Legend[iTree], ":", nFiducialPass, "/", nEntries1, "=", nFiducialPass/float(nEntries1)
	iTree+=1
print "n Sbar:", nSbar

fOut = TFile(plots_output_dir+'macro_FlatTree_BDT.root','RECREATE')

nHistos = len(TH1_ll[0])
nSamples = len(TH1_ll)

c_all  = TCanvas("c_all","c_all",1800,1400)
c_all_log  = TCanvas("c_all_log","c_all_log",1600,1200)
c_all.Divide(6,5)
for i in range(0,nHistos):#each list contains a list of histograms. Each list represents background or signal. The histos need to be overlaid one list to the other
        if "mass" in TH1_ll[0][i].GetName():
	    h = TH1_ll[-1][i]
        else:
	    h = TH1_ll[0][i]
	c_name = "c_"+h.GetName()
	c = TCanvas(c_name,"")
	legend = TLegend(0.65,0.77,0.99,0.99)
	for j in range(0,nSamples):
		h = TH1_ll[j][i]
		if(h.GetName() != "tprof_reweighing_factor"):
			if(h.GetSumw2N() == 0):
				h.Sumw2(kTRUE)
			if(h.Integral() != 0):
				h.Scale(1./h.Integral(), "width");
		h.GetYaxis().SetRangeUser(0.,l_y_axis_ranges[i])
		if("dxy_over_lxy" in h.GetName()):
			h.GetYaxis().SetRangeUser(5*1e-3,l_y_axis_ranges[i])
		if("dz_min" in h.GetName()):
			h.GetYaxis().SetRangeUser(1e-5,l_y_axis_ranges[i])
		if("chi2_ndof" in h.GetName()):
			h.GetYaxis().SetRangeUser(1e-3,l_y_axis_ranges[i])
		if("BDT" in h.GetName()):
			h.GetYaxis().SetRangeUser(5*1e-5,l_y_axis_ranges[i])
		if j == 0:
			h.Draw("L")
			c.Update()
		else:
			h.Draw("PCE1same")
			c.Update()
		if("dxy_over_lxy" in h.GetName() or "dz_min" in h.GetName() or "chi2_ndof" in h.GetName() or "BDT" in h.GetName()):
			c.SetLogy()
		h.SetLineColor(colours[j])
		h.SetLineWidth(2)
		h.SetMarkerStyle(markerStyle[j])
		h.SetMarkerColor(colours[j])
		h.SetMarkerSize(0.8)
		h.SetStats(0)
#Legend = ["Data-S-BKG"   ,"MC-1.8GeV-Multi-to-Single-Reweighed-#bar{S}-Signal"         ,"MC-1.7GeV-Multi-to-Single-Reweighed-#bar{S}-Signal"         ,"MC-1.85GeV-Multi-to-Single-Reweighed-#bar{S}-Signal"         ,"MC-1.9GeV-Multi-to-Single-Reweighed-#bar{S}-Signal"         ,"MC-2GeV-Multi-to-Single-Reweighed-#bar{S}-Signal"         ,"MC-AllMass-Multi-to-Single-Reweighed-#bar{S}-Signal"         ]
                legendtext = ""
                if "Signal" in Legend[j]:
                    if "GeV" in Legend[j]:
                        if "1.85" in Legend[j]:
                            legendtext = "MC m_{#bar{S}} = 1.85 GeV Signal"
                        elif "1.8" in Legend[j]:
                            legendtext = "MC m_{#bar{S}} = 1.8 GeV Signal"
                        elif "1.7" in Legend[j]:
                            legendtext = "MC m_{#bar{S}} = 1.7 GeV Signal"
                        elif "1.9" in Legend[j]:
                            legendtext = "MC m_{#bar{S}} = 1.9 GeV Signal"
                        elif "2" in Legend[j]:
                            legendtext = "MC m_{#bar{S}} = 2 GeV Signal"
                    else:
                        legendtext = "MC #bar{S} Signal"
                else:
                    legendtext = Legend[j]
		legend.AddEntry(h, legendtext,"ep")
	legend.Draw()
	CMS_lumi.CMS_lumi(c, 0, 11)
	c.SaveAs(plots_output_dir+c_name.replace(".", "p")+".pdf")
	c.Write()

	c_all.cd(i+1)
	c.SetGridx(0)
	c.SetGridy(0)
	c.DrawClonePad()
	

c_all.Write()
c_all.SaveAs(plots_output_dir+"c_all.pdf")
c_all_log.Write()
c_all_log.SaveAs(plots_output_dir+"c_all_log.pdf")

fOut.Write()
fOut.Close()
