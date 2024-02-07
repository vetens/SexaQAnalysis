#script to overlap for signal MC and different background samples the distributions of the variables used in the BDT for different steps after doing the pre-BDT cuts
#So, first you have to prepare for a certain configuration of the pre-BDT cuts the ntuples to which a brach with the BDT classifier has been added. This can be done with the src/SexaQAnalysis/TMVA/Step2/DiscrApplication.py

#from ROOT import TFile, TH1F, TH2F, TEfficiency, TH1D, TH2D, TCanvas, gROOT
import ROOT
from ROOT import *
import numpy as np
from collections import OrderedDict
maxEvents = 1e99

applyFiducial = True
applyPreselection = True
test_optional_Preselection = True

FiducialRegionptMin = 0.33
FiducialRegionptMax = 999999999.
FiducialRegionpzMax = 22.
FiducialRegiondxyMin = 0.
FiducialRegiondxyMax = 9.5
FiducialRegiondzMax = 27.
FiducialRegionlxyMax = 44.5
FiducialRegionvzMax = 125.
fiducialCuts = OrderedDict()
fiducialCuts["Lambda v_z decay vertex"] = "abs(tree._Lambda_vz_decay_vertex[0]) <= FiducialRegionvzMax"
fiducialCuts["Lambda l_xy decay vertex"] = "tree._Lambda_lxy_decay_vertex[0] <= FiducialRegionlxyMax"
fiducialCuts["Lambda Daughter 0 p_T"] = "tree._RECO_Lambda_daughter0_pt[0] <= FiducialRegionptMax and tree._RECO_Lambda_daughter0_pt[0] >= FiducialRegionptMin"
fiducialCuts["Lambda Daughter 1 p_T"] = "tree._RECO_Lambda_daughter1_pt[0] <= FiducialRegionptMax and tree._RECO_Lambda_daughter1_pt[0] >= FiducialRegionptMin"
fiducialCuts["Lambda Daughter 0 p_z"] = "abs(tree._RECO_Lambda_daughter0_pt[0]) <= FiducialRegionpzMax"
fiducialCuts["Lambda Daughter 1 p_z"] = "abs(tree._RECO_Lambda_daughter1_pt[0]) <= FiducialRegionpzMax"
fiducialCuts["Lambda Daughter 0 d_xy beamspot"] = "tree._RECO_Lambda_daughter0_dxy_beamspot[0] <= FiducialRegiondxyMax and tree._RECO_Lambda_daughter0_dxy_beamspot[0] >= FiducialRegiondxyMin"
fiducialCuts["Lambda Daughter 1 d_xy beamspot"] = "tree._RECO_Lambda_daughter1_dxy_beamspot[0] <= FiducialRegiondxyMax and tree._RECO_Lambda_daughter1_dxy_beamspot[0] >= FiducialRegiondxyMin"
fiducialCuts["Lambda Daughter 0 d_z Best PV"] = "abs(tree._RECO_Lambda_daughter0_dz_min_PV[0]) <= FiducialRegiondzMax"
fiducialCuts["Lambda Daughter 1 d_z Best PV"] = "abs(tree._RECO_Lambda_daughter1_dz_min_PV[0]) <= FiducialRegiondzMax"
fiducialCuts["K_s v_z decay vertex"] = "abs(tree._Ks_vz_decay_vertex[0]) <= FiducialRegionvzMax"
fiducialCuts["K_s l_xy decay vertex"] = "tree._Ks_lxy_decay_vertex[0] <= FiducialRegionlxyMax"
fiducialCuts["K_s Daughter 0 p_T"] = "tree._RECO_Ks_daughter0_pt[0] <= FiducialRegionptMax and tree._RECO_Ks_daughter0_pt[0] >= FiducialRegionptMin"
fiducialCuts["K_s Daughter 1 p_T"] = "tree._RECO_Ks_daughter1_pt[0] <= FiducialRegionptMax and tree._RECO_Ks_daughter1_pt[0] >= FiducialRegionptMin"
fiducialCuts["K_s Daughter 0 p_z"] = "abs(tree._RECO_Ks_daughter0_pt[0]) <= FiducialRegionpzMax"
fiducialCuts["K_s Daughter 1 p_z"] = "abs(tree._RECO_Ks_daughter1_pt[0]) <= FiducialRegionpzMax"
fiducialCuts["K_s Daughter 0 d_xy beamspot"] = "tree._RECO_Ks_daughter0_dxy_beamspot[0] <= FiducialRegiondxyMax and tree._RECO_Ks_daughter0_dxy_beamspot[0] >= FiducialRegiondxyMin"
fiducialCuts["K_s Daughter 1 d_xy beamspot"] = "tree._RECO_Ks_daughter1_dxy_beamspot[0] <= FiducialRegiondxyMax and tree._RECO_Ks_daughter1_dxy_beamspot[0] >= FiducialRegiondxyMin"
fiducialCuts["K_s Daughter 0 d_z Best PV"] = "abs(tree._RECO_Ks_daughter0_dz_min_PV[0]) <= FiducialRegiondzMax"
fiducialCuts["K_s Daughter 1 d_z Best PV"] = "abs(tree._RECO_Ks_daughter1_dz_min_PV[0]) <= FiducialRegiondzMax"

Presel_DeltaPhiMin = 0.4
Presel_LxyInteractionVertexMin = 2.02
Presel_LxyInteractionVertexMax = 2.40
Presel_dxyOverLxyMin = 0
Presel_dxyOverLxyMax = 0.5
preselectionCuts = OrderedDict()
preselectionCuts["S Daughters delta phi"] = "abs(tree._S_daughters_deltaphi[0]) >= Presel_DeltaPhiMin"
preselectionCuts["S l_xy interaction vertex to beampipe center"] = "tree._S_lxy_interaction_vertex_beampipeCenter[0] >= Presel_LxyInteractionVertexMin and tree._S_lxy_interaction_vertex_beampipeCenter[0] <= Presel_LxyInteractionVertexMax"
preselectionCuts["S d_xy/l_xy"] = "tree._S_dxy_over_lxy[0] >= Presel_dxyOverLxyMin and tree._S_dxy_over_lxy[0] <= Presel_dxyOverLxyMax"

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
optionalPreselectionCuts = OrderedDict()
optionalPreselectionCuts["S v_z interaction vertex"] = "abs(tree._S_vz_interaction_vertex[0]) <= Opt_VzMax"
optionalPreselectionCuts["Delta eta of S daughters"] = "abs(tree._S_daughters_deltaeta[0]) <= Opt_DeltaEtaMax"
optionalPreselectionCuts["3D Openingsangle of S daughters"] = "tree._S_daughters_openingsangle[0] <= Opt_DeltaAlpha_daughters_Max and tree._S_daughters_openingsangle[0] >= Opt_DeltaAlpha_daughters_Min"
optionalPreselectionCuts["3D Openingsangle of S and Ks"] = "tree._S_Ks_openingsangle[0] <= Opt_DeltaAlpha_S_Kshort_Max and tree._S_Ks_openingsangle[0] >= Opt_DeltaAlpha_S_Kshort_Min"
optionalPreselectionCuts["3D Openingsangle of S and Lambda"] = "tree._S_Lambda_openingsangle[0] <= Opt_DeltaAlpha_S_Lambda_Max and tree._S_Lambda_openingsangle[0] >= Opt_DeltaAlpha_S_Lambda_Min"
optionalPreselectionCuts["S eta"] = "abs(tree._S_eta[0]) <= Opt_EtaSMax"
optionalPreselectionCuts["minimum impact parameter of S"] = "abs(tree._S_dz_min[0]) <= Opt_SdzminMax"
optionalPreselectionCuts["K_s eta"] = "abs(tree._Ks_eta[0]) <= Opt_EtaKshortMax"
optionalPreselectionCuts["K_s p_T"] = "tree._Ks_pt[0] >= Opt_pTKshortMin"

fOut = open("Efficiencies.txt", "w")

class efficiencyTracker:
    def __init__(self, cutstring, cutstringSequential, title, samplename):
        self.cutstring = cutstring
        self.cutstringSequential = cutstringSequential
        self.title = title
        if('MC' in samplename):
            self.isMC = True
            self.nPassed = 0.
            self.nPassed_Seq = 0.
            self.nPassed_weighted = 0.
            self.nPassed_Seq_weighted = 0.
        else:
            self.isMC = False
            self.nPassed = 0.
            self.nPassed_Seq = 0.
    def TrackCut(self, PassedAllCuts, weight = 1.0):
        eventPassed = eval(self.cutstring)
        eventPassed_Seq = eval(self.cutstringSequential)
        if eventPassed:
            self.nPassed += 1.0
            if self.isMC:
                self.nPassed_weighted += weight
        if eventPassed_Seq:
            self.nPassed_Seq += 1.0
            if self.isMC:
                self.nPassed_Seq_weighted += weight
            return PassedAllCuts
        else:
            return False
        
    def EfficiencyPrintout(self, outputFile, denom, denom_weighted, denomTot, denomTot_weighted):
        outputFile.write("\t" + self.title + ":\n")
        outputFile.write("\t\t INDIVIDUAL EFF: " + str(self.nPassed) + "/" + str(denom) + " = " + str(self.nPassed / float(denom)) + "\n")
        outputFile.write("\t\t TOTAL EFF: " + str(self.nPassed_Seq) + "/" + str(denomTot) + " = " + str(self.nPassed_Seq / float(denomTot)) + "\n")
        if self.isMC:
            outputFile.write("\t weighted:\n")
            outputFile.write("\t\t INDIVIDUAL EFF:" + str(self.nPassed_weighted) + "/" + str(denom_weighted) + " = " + str(self.nPassed_weighted / float(denom_weighted)) + "\n")
            outputFile.write("\t\t TOTAL EFF:" + str(self.nPassed_Seq_weighted) + "/" + str(denomTot_weighted) + " = " + str(self.nPassed_Seq_weighted / float(denomTot_weighted)) + "\n")

#Open Files
#MC_S_Bkg_File = ROOT.TFile.Open("/afs/cern.ch/work/w/wvetens/Sexaquarks/CMSSW_10_2_26/src/SexaQAnalysis/AnalyzerAllSteps/macros/BDT/QCD_MC_BG.root")
#MC_S_Bkg_Tree = MC_S_Bkg_File.Get("FlatTreeProducerBDT/FlatTree")

#MC Sbar BKG from QCD MuEnriched sample (Same file, just look at sbar instead of s)
#MC_Sbar_Bkg_File = MC_S_Bkg_File
#MC_Sbar_Bkg_Tree = MC_Sbar_Bkg_File.Get("FlatTreeProducerBDT/FlatTree")

#MC Xevt Sbar BKG from QCD MuEnriched sample
#MC_Sbar_Xevt_Bkg_File = ROOT.TFile.Open("/afs/cern.ch/work/w/wvetens/Sexaquarks/CMSSW_10_2_26/src/SexaQAnalysis/AnalyzerAllSteps/macros/BDT/MC_Xevt_Bkg_QCD.root")
#MC_Sbar_Xevt_Bkg_Tree = MC_Sbar_Xevt_Bkg_File.Get("FlatTreeProducerBDT/FlatTree")

#Data S Bkg from Bparking UL 2018
#Data_S_Bkg_File = ROOT.TFile.Open("/afs/cern.ch/work/w/wvetens/Sexaquarks/CMSSW_10_2_26/src/SexaQAnalysis/AnalyzerAllSteps/macros/BDT/Data_BPH_Full.root")
#Data_S_Bkg_File = ROOT.TFile.Open("root://cmsxrootd.hep.wisc.edu//store/user/wvetens/data_Sexaq/FlatTree_BDT/Data_BPH_NoPresel_Fragment.root")
#Data_S_Bkg_Tree = Data_S_Bkg_File.Get("FlatTreeProducerBDT/FlatTree")
#Data_AntiS_Tree = Data_S_Bkg_File.Get("FlatTreeProducerBDT/FlatTree")
#Data Xevt Sbar Bkg from Bparking UL 2018
#Data_Sbar_Xevt_Bkg_File = ROOT.TFile.Open("/afs/cern.ch/work/w/wvetens/Sexaquarks/CMSSW_10_2_26/src/SexaQAnalysis/AnalyzerAllSteps/macros/BDT/Data_Xevt_Bkg.root")
#Data_Sbar_Xevt_Bkg_Tree = Data_Sbar_Xevt_Bkg_File.Get("FlatTreeProducerBDT/FlatTree")

#The signal MC
MC_AntiS_Sgn_File_M2SReweigh_1p7GeV = ROOT.TFile.Open("/afs/cern.ch/work/w/wvetens/Sexaquarks/CMSSW_10_2_26/src/SexaQAnalysis/AnalyzerAllSteps/macros/BDT/Signal_1p7GeV.root")
MC_AntiS_Sgn_Tree_M2SReweigh_1p7GeV = MC_AntiS_Sgn_File_M2SReweigh_1p7GeV.Get("FlatTreeProducerBDT/FlatTree")
MC_AntiS_Sgn_File_M2SReweigh_1p8GeV = ROOT.TFile.Open("/afs/cern.ch/work/w/wvetens/Sexaquarks/CMSSW_10_2_26/src/SexaQAnalysis/AnalyzerAllSteps/macros/BDT/Signal_1p8GeV.root")
MC_AntiS_Sgn_Tree_M2SReweigh_1p8GeV = MC_AntiS_Sgn_File_M2SReweigh_1p8GeV.Get("FlatTreeProducerBDT/FlatTree")
MC_AntiS_Sgn_File_M2SReweigh_1p9GeV = ROOT.TFile.Open("/afs/cern.ch/work/w/wvetens/Sexaquarks/CMSSW_10_2_26/src/SexaQAnalysis/AnalyzerAllSteps/macros/BDT/Signal_1p9GeV.root")
MC_AntiS_Sgn_Tree_M2SReweigh_1p9GeV = MC_AntiS_Sgn_File_M2SReweigh_1p9GeV.Get("FlatTreeProducerBDT/FlatTree")
MC_AntiS_Sgn_File_M2SReweigh_1p85GeV = ROOT.TFile.Open("/afs/cern.ch/work/w/wvetens/Sexaquarks/CMSSW_10_2_26/src/SexaQAnalysis/AnalyzerAllSteps/macros/BDT/Signal_1p85GeV.root")
MC_AntiS_Sgn_Tree_M2SReweigh_1p85GeV = MC_AntiS_Sgn_File_M2SReweigh_1p85GeV.Get("FlatTreeProducerBDT/FlatTree")
MC_AntiS_Sgn_File_M2SReweigh_2GeV = ROOT.TFile.Open("/afs/cern.ch/work/w/wvetens/Sexaquarks/CMSSW_10_2_26/src/SexaQAnalysis/AnalyzerAllSteps/macros/BDT/Signal_2GeV.root")
MC_AntiS_Sgn_Tree_M2SReweigh_2GeV = MC_AntiS_Sgn_File_M2SReweigh_2GeV.Get("FlatTreeProducerBDT/FlatTree")
MC_AntiS_Sgn_File_M2SReweigh_AllMasses = ROOT.TFile.Open("/afs/cern.ch/work/w/wvetens/Sexaquarks/CMSSW_10_2_26/src/SexaQAnalysis/AnalyzerAllSteps/macros/BDT/SignalSbar_FULL.root")
MC_AntiS_Sgn_Tree_M2SReweigh_AllMasses = MC_AntiS_Sgn_File_M2SReweigh_AllMasses.Get("FlatTreeProducerBDT/FlatTree")
#MC_AntiS_Sgn_File_SingleSQEV = ROOT.TFile.Open("/afs/cern.ch/work/w/wvetens/Sexaquarks/CMSSW_10_2_26/src/SexaQAnalysis/AnalyzerAllSteps/macros/BDT/MC_AntiS_Sgn_Trial4.root")
#MC_AntiS_Sgn_Tree_SingleSQEV = MC_AntiS_Sgn_File_SingleSQEV.Get("FlatTreeProducerBDT/FlatTree")
#MC_AntiS_Sgn_File_MultiSQEV = ROOT.TFile.Open("/afs/cern.ch/work/w/wvetens/Sexaquarks/CMSSW_10_2_26/src/SexaQAnalysis/AnalyzerAllSteps/macros/BDT/MC_AntiS_Sgn_Trial4_MultiSQEV.root")
#MC_AntiS_Sgn_Tree_MultiSQEV = MC_AntiS_Sgn_File_MultiSQEV.Get("FlatTreeProducerBDT/FlatTree")
MC_Signal_Truth_cutoff = 0.5

#Data antiS from SingleElectron Run2016H with antiS reconstructed X events
#Data_AntiS_XEvent_File = ROOT.TFile.Open("/user/jdeclerc/Analysis/SexaQuark/CMSSW_9_4_9/src/TMVA/Step2/BDTApplied/Unblinded/Data_AntiS_BKG_XEvent/DiscrApplied_test_SingleMuonRun2016H_XEventAntiS.root")
#Data_AntiS_XEvent_Tree = Data_AntiS_XEvent_File.Get("FlatTreeProducerBDT/FlatTree")

#Legend = ["MC-S-BKG"   ,"MC-#bar{S}-BKG" ,"Data-S-BKG"   ,"Data-#bar{S}-BKG (BDT < 0.1)  ","Data-#bar{S}-X event BKG" ,"MC-#bar{S}-Signal"]
#l_tree = [MC_S_Bkg_Tree,MC_AntiS_Bkg_Tree,Data_S_Bkg_Tree,Data_AntiS_Bkg_Tree             , Data_AntiS_XEvent_Tree    , MC_AntiS_Sgn_Tree]
#Legend = ["Data-S-BKG"   ,"Data-#bar{S}-X event BKG" ,"MC-#bar{S}-Signal"]
#l_tree = [Data_S_Bkg_Tree, Data_AntiS_XEvent_Tree    , MC_AntiS_Sgn_Tree]
#Legend = ["Data-S-BKG"   ,"MC-#bar{S}-Signal","MC-Multi-#bar{S}-Signal"  ]
#l_tree = [Data_S_Bkg_Tree, MC_AntiS_Sgn_Tree, MC_AntiS_Sgn_Tree_MultiSQEV]
#Legend = ["MC-S-BKG"   ,"MC-#bar{S}-BKG","MC-#bar{S}-Xevt-BKG","Data-#bar{S}-Xevt-BKG","Data-S-BKG"   ,"MC-Single-#bar{S}-Signal"    ,"MC-Multi-#bar{S}-Signal"  ,"MC-Multi-to-Single-Reweighed-#bar{S}-Signal"]
#l_tree = [MC_S_Bkg_Tree,MC_Sbar_Bkg_Tree,MC_Sbar_Xevt_Bkg_Tree,Data_Sbar_Xevt_Bkg_Tree,Data_S_Bkg_Tree,MC_AntiS_Sgn_Tree_SingleSQEV  ,MC_AntiS_Sgn_Tree_MultiSQEV, MC_AntiS_Sgn_Tree_M2SReweigh                ]
#Legend = ["MC-S-BKG"   ,"MC-#bar{S}-BKG","MC-#bar{S}-Xevt-BKG","Data-#bar{S}-Xevt-BKG","Data-S-BKG"   ,"MC-Multi-to-Single-Reweighed-#bar{S}-Signal"]
#l_tree = [MC_S_Bkg_Tree,MC_Sbar_Bkg_Tree,MC_Sbar_Xevt_Bkg_Tree,Data_Sbar_Xevt_Bkg_Tree,Data_S_Bkg_Tree,MC_AntiS_Sgn_Tree_M2SReweigh                 ]
#Legend = ["Data-#bar{S}" ,"Data-S-BKG"   ,"MC-1.8GeV-#bar{S}-Signal"         ,"MC-1.7GeV-#bar{S}-Signal"         ,"MC-1.85GeV-#bar{S}-Signal"         ,"MC-1.9GeV-#bar{S}-Signal"         ,"MC-2GeV-#bar{S}-Signal"         ,"MC-AllMass-#bar{S}-Signal"           ]
#l_tree = [Data_AntiS_Tree,Data_S_Bkg_Tree,MC_AntiS_Sgn_Tree_M2SReweigh_1p8GeV,MC_AntiS_Sgn_Tree_M2SReweigh_1p7GeV,MC_AntiS_Sgn_Tree_M2SReweigh_1p85GeV,MC_AntiS_Sgn_Tree_M2SReweigh_1p9GeV,MC_AntiS_Sgn_Tree_M2SReweigh_2GeV,MC_AntiS_Sgn_Tree_M2SReweigh_AllMasses]
#Legend = ["Data-S-BKG"   ,"MC-1.8GeV-#bar{S}-Signal"         ,"MC-1.7GeV-#bar{S}-Signal"         ,"MC-1.85GeV-#bar{S}-Signal"         ,"MC-1.9GeV-#bar{S}-Signal"         ,"MC-2GeV-#bar{S}-Signal"         ,"MC-AllMass-#bar{S}-Signal"           ]
#l_tree = [Data_S_Bkg_Tree,MC_AntiS_Sgn_Tree_M2SReweigh_1p8GeV,MC_AntiS_Sgn_Tree_M2SReweigh_1p7GeV,MC_AntiS_Sgn_Tree_M2SReweigh_1p85GeV,MC_AntiS_Sgn_Tree_M2SReweigh_1p9GeV,MC_AntiS_Sgn_Tree_M2SReweigh_2GeV,MC_AntiS_Sgn_Tree_M2SReweigh_AllMasses]
Legend = ["MC-1.8GeV-#bar{S}-Signal"         ,"MC-1.7GeV-#bar{S}-Signal"         ,"MC-1.85GeV-#bar{S}-Signal"         ,"MC-1.9GeV-#bar{S}-Signal"         ,"MC-2GeV-#bar{S}-Signal"         ,"MC-AllMass-#bar{S}-Signal"           ]
l_tree = [MC_AntiS_Sgn_Tree_M2SReweigh_1p8GeV,MC_AntiS_Sgn_Tree_M2SReweigh_1p7GeV,MC_AntiS_Sgn_Tree_M2SReweigh_1p85GeV,MC_AntiS_Sgn_Tree_M2SReweigh_1p9GeV,MC_AntiS_Sgn_Tree_M2SReweigh_2GeV,MC_AntiS_Sgn_Tree_M2SReweigh_AllMasses]
#Legend = ["Data-S-BKG"   ,"MC-Multi-#bar{S}-Signal"]
#l_tree = [Data_S_Bkg_Tree, MC_AntiS_Sgn_Tree_MultiSQEV]



iTree = 0
nSbar = 0
for tree in l_tree:
	nEntries1 = tree.GetEntries()
        if(applyFiducial):
            nPreFiducial = 0.
            nFiducialPass = 0.
            #Weighed counters
            nPreFiducial_w = 0.
            nFiducialPass = 0.
            nFiducialPass_w = 0.
            efficiencyTrackers_fiducial = []
            CutFlow = ""
            i=0
            for title, cut in fiducialCuts.items():
                if i==0:
                    CutFlow += cut
                else:
                    CutFlow += " and " + cut
                i += 1
                efficiencyTrackers_fiducial += [efficiencyTracker(cut, CutFlow, title, Legend[iTree])]
            if(applyPreselection):
                nPreselectionPass = 0.
                #Weighed counters
                nPreselectionPass_w = 0.
                efficiencyTrackers_presel = []
                for title, cut in preselectionCuts.items():
                    CutFlow += " and " + cut
                    efficiencyTrackers_presel += [efficiencyTracker(cut, CutFlow, title, Legend[iTree])]
                if(test_optional_Preselection):
                    nAllOptionalPass = 0.
                    #Weighed counters
                    nAllOptionalPass_w = 0.
                    efficiencyTrackers_opt = []
                    for title, cut in optionalPreselectionCuts.items():
                        CutFlow += " and " + cut
                        efficiencyTrackers_opt += [efficiencyTracker(cut, CutFlow, title, Legend[iTree])]

	fOut.write("---------------------------------------------------\n")
	fOut.write("running for " + Legend[iTree] + "\n")
        fOut.write("N entries:" + str(nEntries1) + "\n")
	for i in range(0,nEntries1):
		if(i==maxEvents):
			break
		#if(i%1e4 == 0):
		#	fOut.write("reached entry: ", i
		tree.GetEntry(i)
		if(i==0): fOut.write('charge of the S/antiS: ' + str(tree._S_charge[0]) + "\n")
		
		#for when you have the BDT parameter in your tree:
		#if(tree.SexaqBDT <= min_BDT_classifier):continue

		#need to reweigh the MC signal events, because the ones with high eta are more important, because they will pass more material
		reweighing_factor = 1
		if('#bar{S}-Signal' in Legend[iTree]): #if MC signal reweigh both for the pathlength through the beampipe and for the z location of the PV and PU
                        nSbar+=1
                        if(tree._S_deltaLInteractionVertexAntiSmin[0] > MC_Signal_Truth_cutoff): 
                            #fOut.write(tree._S_deltaLInteractionVertexAntiSmin[0]
                            continue
                        if ( 'Multi-to-Single-Reweighed' in Legend[iTree] ):
			    reweighing_factor = tree._S_event_weighting_factor[0]*tree._S_event_weighting_factorPU[0]*tree._S_event_weighting_factorM2S[0]
                        else:
			    reweighing_factor = tree._S_event_weighting_factor[0]*tree._S_event_weighting_factorPU[0]
		elif('MC-S-BKG' in Legend[iTree] or 'MC-#bar{S}-BKG' in Legend[iTree]):#if MC background only reweigh for the z location of the PV and PU
			reweighing_factor = tree._S_event_weighting_factorPU[0]
                # for the S background we want to look at S, otherwise we want to look at Sbar
                if(('Data-S-BKG' in Legend[iTree] or 'MC-S-BKG' in Legend[iTree]) and tree._S_charge[0] == -1): 
                    continue
                elif(tree._S_charge[0] == 1 and '#bar{S}' in Legend[iTree]): continue

                #FIDUCIAL CUTS
                if( applyFiducial ):
                    nPreFiducial += 1.0
                    nPreFiducial_w += reweighing_factor
                    passAllFiducial = True
                    for efficiency in efficiencyTrackers_fiducial:
                        passAllFiducial = efficiency.TrackCut(passAllFiducial, reweighing_factor)
                    if passAllFiducial:
                        nFiducialPass += 1.0
                        nFiducialPass_w += reweighing_factor
                    #PRESELECTION
                    if( applyPreselection and passAllFiducial ):
                        PassPreselection = True
                        for efficiency in efficiencyTrackers_presel:
                            PassPreselection = efficiency.TrackCut(PassPreselection, reweighing_factor)
                        if PassPreselection:
                            nPreselectionPass += 1.0
                            nPreselectionPass_w += reweighing_factor
                        #TEST OPTIONAL CUTS
                        if( test_optional_Preselection and PassPreselection ):
                            PassOptPreselection = True
                            for efficiency in efficiencyTrackers_opt:
                                PassOptPreselection = efficiency.TrackCut(PassOptPreselection, reweighing_factor)
                            if PassOptPreselection:
                                nAllOptionalPass += 1.0
                                nAllOptionalPass_w += reweighing_factor

        if(applyFiducial):
#Fiducial cut printouts
            fOut.write("Number of valid Sbar before fiducial cuts in " + Legend[iTree] + ":" + str(nPreFiducial) + "\n")
            if "MC" in Legend[iTree]:
                fOut.write("Number of valid Sbar (weighed) before fiducial cuts in " + Legend[iTree] + ":" + str(nPreFiducial_w) + "\n")
            fOut.write("Individual efficiencies of fiducial cuts in " + Legend[iTree] + ":" + "\n")
            for efficiency in efficiencyTrackers_fiducial:
                efficiency.EfficiencyPrintout(fOut, nPreFiducial, nPreFiducial_w, nPreFiducial, nPreFiducial_w)
            fOut.write("Total efficiency of all fiducial cuts in " + Legend[iTree] + ":" + str(nFiducialPass) + "/" + str(nPreFiducial) + "=" + str(nFiducialPass/float(nPreFiducial)) + "\n")
            if "MC" in Legend[iTree]:
                fOut.write("Total efficiency (weighed) of all fiducial cuts in " + Legend[iTree] + ":" + str(nFiducialPass_w) + "/" + str(nPreFiducial_w) + "=" + str(nFiducialPass_w/float(nPreFiducial_w)) + "\n")
            fOut.write("\n")
            #Preselection printouts
            if(applyPreselection):
                fOut.write("Individual efficiencies of initial preselection in " + Legend[iTree] + ":" + "\n")
                for efficiency in efficiencyTrackers_presel:
                    efficiency.EfficiencyPrintout(fOut, nFiducialPass, nFiducialPass_w, nPreFiducial, nPreFiducial_w)
                fOut.write("Total efficiency of initial preselection in " + Legend[iTree] + ":" + str(nPreselectionPass) + "/" + str(nFiducialPass) + "=" + str(nPreselectionPass/float(nFiducialPass)) + "\n")
                if "MC" in Legend[iTree]:
                    fOut.write("Total efficiency (weighed) of initial preselection in " + Legend[iTree] + ":" + str(nPreselectionPass_w) + "/" + str(nFiducialPass_w) + "=" + str(nPreselectionPass_w/float(nFiducialPass_w)) + "\n")
                fOut.write("Total COMBINED efficiency of initial preselection and fiducial cuts in " + Legend[iTree] + ":" + str(nPreselectionPass) + "/" + str(nPreFiducial) + "=" + str(nPreselectionPass/float(nPreFiducial)) + "\n")
                if "MC" in Legend[iTree]:
                    fOut.write("Total COMBINED efficiency (weighed) of initial preselection and fiducial cuts in " + Legend[iTree] + ":" + str(nPreselectionPass_w) + "/" + str(nPreFiducial_w) + "=" + str(nPreselectionPass_w/float(nPreFiducial_w)) + "\n")
                fOut.write("\n")

                #Optional Preselection printouts
                if(test_optional_Preselection):
                    fOut.write("Individual efficiencies of optional preselection in " + Legend[iTree] + ":" + "\n")
                    for efficiency in efficiencyTrackers_opt:
                        efficiency.EfficiencyPrintout(fOut, nPreselectionPass, nPreselectionPass_w, nPreFiducial, nPreFiducial_w)
                    fOut.write("Total efficiency of optional preselection in " + Legend[iTree] + ":" + str(nAllOptionalPass) + "/" + str(nPreselectionPass) + "=" + str(nAllOptionalPass/float(nPreselectionPass)) + "\n")
                    if "MC" in Legend[iTree]:
                        fOut.write("Total efficiency (weighed) of optional preselection in " + Legend[iTree] + ":" + str(nAllOptionalPass_w) + "/" + str(nPreselectionPass_w) + "=" + str(nAllOptionalPass_w/float(nPreselectionPass_w)) + "\n")
                    fOut.write("Total efficiency of ALL preselection cuts (initial + optional) in " + Legend[iTree] + ":" + str(nAllOptionalPass) + "/" + str(nFiducialPass) + "=" + str(nAllOptionalPass/float(nFiducialPass)) + "\n")
                    if "MC" in Legend[iTree]:
                        fOut.write("Total efficiency (weighed) of ALL preselection cuts (initial + optional) in " + Legend[iTree] + ":" + str(nAllOptionalPass_w) + "/" + str(nFiducialPass_w) + "=" + str(nAllOptionalPass_w/float(nFiducialPass_w)) + "\n")
                    fOut.write("Total COMBINED efficiency of all considered cuts (fiducial + initial preselection + optional preselection) in " + Legend[iTree] + ":" + str(nAllOptionalPass) + "/" + str(nPreFiducial) + "=" + str(nAllOptionalPass/float(nPreFiducial)) + "\n")
                    if "MC" in Legend[iTree]:
                        fOut.write("Total COMBINED efficiency (weighed) of all considered cuts (fiducial + initial preselection + optional preselection) in " + Legend[iTree] + ":" + str(nAllOptionalPass_w) + "/" + str(nPreFiducial_w) + "=" + str(nAllOptionalPass_w/float(nPreFiducial_w)) + "\n")
        
	fOut.write("---------------------------------------------------\n")
	iTree+=1

fOut.close()
