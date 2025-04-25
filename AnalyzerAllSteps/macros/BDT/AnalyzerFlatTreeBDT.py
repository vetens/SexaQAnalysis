#script to overlap for signal MC and different background samples the distributions of the variables used in the BDT for different steps after doing the pre-BDT cuts
#So, first you have to prepare for a certain configuration of the pre-BDT cuts the ntuples to which a brach with the BDT classifier has been added. This can be done with the src/SexaQAnalysis/TMVA/Step2/DiscrApplication.py

#from ROOT import TFile, TH1F, TH2F, TEfficiency, TH1D, TH2D, TCanvas, gROOT
import ROOT
from ROOT import *
import numpy as np
import sys
sys.path.append('/afs/cern.ch/work/w/wvetens/Sexaquarks/CMSSW_10_2_26/src/SexaQAnalysis/AnalyzerAllSteps/macros/tdrStyle')
import argparse
import  CMSStyle

import sys
sys.path.insert(1, '../../../TMVA')
import configBDT as config

config_dict = config.config_dict

#earlykill = 0
parser = argparse.ArgumentParser()
parser.add_argument('--preCuts', dest='preCuts', action='store_true', default=False)
parser.add_argument('--CompareGenMass', dest='CompareGenMass', action='store_true', default=False)
parser.add_argument('--HighBDTOnly', dest='HighBDTOnly', action='store_true', default=False)
#NOTE: for CompareDataBGs and CompareDataMCBG, these assume BDT Evaluation
parser.add_argument('--CompareDataBGs', dest='CompareDataBGs', action='store_true', default=False)
parser.add_argument('--CompareDataMCBG', dest='CompareDataMCBG', action='store_true', default=False)
parser.add_argument('--PVBeforeAfterCuts', dest='PVBeforeAfterCuts', action='store_true', default=False)
parser.add_argument('--addXevtWeights', dest='addXevtWeights', action='store_true', default=False)

args = parser.parse_args()

gROOT.SetBatch(kTRUE)
gStyle.SetLegendTextSize(0.08)

CMSStyle.extraText = " (CMS data/simulation)"
#CMSStyle.extraText = " (CMS simulation)"
CMSStyle.lumiText = "Parked 2018 data, "+"237 #times 10^{9}"+" Collisions (13 TeV)"
CMSStyle.cmsText = "Private Work "
CMSStyle.cmsTextFont = 42
CMSStyle.extraTextFont = 42
CMSStyle.lumiTextSize = 0.74
CMSStyle.cmsTextSize = 0.74
CMSStyle.relPosX = 2.36*0.045
CMSStyle.outOfFrame = False

CMSStyle.setTDRStyle()
fXevtPUWeights = '/afs/cern.ch/work/w/wvetens/Sexaquarks/CMSSW_10_2_26/src/SexaQAnalysis/AnalyzerAllSteps/data/PUReweigh_nPV_XevtToDataBPH2018_FULL_POSTCUTS.txt'
weights_PU_Xevt = {line.split()[0] : line.split()[1] for line in open(fXevtPUWeights)}

def ReadyCanvas(name, W=700, H=500):
    c = TCanvas(name, "", W, H)
    c.Draw()
    c.SetFillColor(0)
    c.SetRightMargin(0.05)
    c.SetBorderMode(0)
    c.SetFrameFillStyle(0)
    c.SetFrameBorderMode(0)
#    c.SetTickx(0)
#    c.SetTicky(0)
    c.cd()
    return c
maxEvents = 1e5
#maxEvents = 10

UseXevtWeights = args.addXevtWeights
applyFiducial = True
applyPreselection = True
apply_optional_Preselection = True
if args.preCuts:
    applyFiducial = False
    applyPreselection = False
    apply_optional_Preselection = False
DoBeforeAfterPV = args.PVBeforeAfterCuts
DoBGComparison = args.CompareDataBGs
BGMCCompare = args.CompareDataMCBG
HighBDT = args.HighBDTOnly
DoGenMass = args.CompareGenMass
DoPostCuts = (not args.preCuts)
if not DoPostCuts:
    print "Doing pre-cut!"
if DoGenMass:
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
    1.1,                    #S_mass
    33,                     #GEN_S_mass
    10                      #tprof_reweighing_factor
    ]
elif not DoBGComparison and not BGMCCompare:
#elif not DoBGComparison:
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
    10                      #tprof_reweighing_factor
    ]
else:
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
    100,                     #SexaqBDT
    10                      #tprof_reweighing_factor
    ]

#the below is a bit historical, it is by default "all" now
configuration = "all"
#cut on the BDT parameter to select a minimal BDT, to go and look in the tail of the BDT distribution (towards the signal), put to -999 if you want all the events
if HighBDT:
    min_BDT_classifier = -0.15 #-999 #or -0.15
else:
    min_BDT_classifier = -999


##################################################################
##With all pre BDT cuts applied
##################################################################
#Open files and trees:
#MC S BKG from QCD MuEnriched sample
#MC_S_Bkg_File = ROOT.TFile.Open("/afs/cern.ch/work/w/wvetens/Sexaquarks/CMSSW_10_2_26/src/SexaQAnalysis/AnalyzerAllSteps/macros/BDT/MC_AntiS_Bkg_QCD.root")
#MC_S_Bkg_Tree = MC_S_Bkg_File.Get("FlatTreeProducerBDT/FlatTree")
#
##MC Sbar BKG from QCD MuEnriched sample (Same file, just look at sbar instead of s)
#MC_Sbar_Bkg_File = MC_S_Bkg_File
#MC_Sbar_Bkg_Tree = MC_Sbar_Bkg_File.Get("FlatTreeProducerBDT/FlatTree")
#
##MC Xevt Sbar BKG from QCD MuEnriched sample
#MC_Sbar_Xevt_Bkg_File = ROOT.TFile.Open("/afs/cern.ch/work/w/wvetens/Sexaquarks/CMSSW_10_2_26/src/SexaQAnalysis/AnalyzerAllSteps/macros/BDT/MC_Xevt_Bkg_QCD.root")
#MC_Sbar_Xevt_Bkg_Tree = MC_Sbar_Xevt_Bkg_File.Get("FlatTreeProducerBDT/FlatTree")
#
#
##Data Xevt Sbar Bkg from Bparking UL 2018
#Data_Sbar_Xevt_Bkg_File = ROOT.TFile.Open("/afs/cern.ch/work/w/wvetens/Sexaquarks/CMSSW_10_2_26/src/SexaQAnalysis/AnalyzerAllSteps/macros/BDT/Data_Xevt_Bkg.root")
#Data_Sbar_Xevt_Bkg_Tree = Data_Sbar_Xevt_Bkg_File.Get("FlatTreeProducerBDT/FlatTree")
#
##The signal MC
#MC_AntiS_Sgn_File_M2SReweigh = ROOT.TFile.Open("/afs/cern.ch/work/w/wvetens/Sexaquarks/CMSSW_10_2_26/src/SexaQAnalysis/AnalyzerAllSteps/macros/BDT/MC_AntiS_Sgn_Trial5_M2SReweigh.root")
#MC_AntiS_Sgn_Tree_M2SReweigh = MC_AntiS_Sgn_File_M2SReweigh.Get("FlatTreeProducerBDT/FlatTree")
##MC_AntiS_Sgn_File_SingleSQEV = ROOT.TFile.Open("/afs/cern.ch/work/w/wvetens/Sexaquarks/CMSSW_10_2_26/src/SexaQAnalysis/AnalyzerAllSteps/macros/BDT/MC_AntiS_Sgn_Trial4.root")
##MC_AntiS_Sgn_Tree_SingleSQEV = MC_AntiS_Sgn_File_SingleSQEV.Get("FlatTreeProducerBDT/FlatTree")
#MC_AntiS_Sgn_File_MultiSQEV = ROOT.TFile.Open("/afs/cern.ch/work/w/wvetens/Sexaquarks/CMSSW_10_2_26/src/SexaQAnalysis/AnalyzerAllSteps/macros/BDT/MC_AntiS_Sgn_Trial4_MultiSQEV.root")
#MC_AntiS_Sgn_Tree_MultiSQEV = MC_AntiS_Sgn_File_MultiSQEV.Get("FlatTreeProducerBDT/FlatTree")
MC_Signal_Truth_cutoff_deltaR = 0.5
MC_Signal_Truth_cutoff_deltaL = 2.0

#MC_S_Bkg_File = ROOT.TFile.Open("/afs/cern.ch/work/w/wvetens/Sexaquarks/CMSSW_10_2_26/src/SexaQAnalysis/AnalyzerAllSteps/macros/BDT/QCD_MC_BG.root")
#MC_S_Bkg_Tree = MC_S_Bkg_File.Get("FlatTreeProducerBDT/FlatTree")

#MC Sbar BKG from QCD MuEnriched sample (Same file, just look at sbar instead of s)
#MC_Sbar_Bkg_File = MC_S_Bkg_File
#MC_Sbar_Bkg_Tree = MC_Sbar_Bkg_File.Get("FlatTreeProducerBDT/FlatTree")

#MC Xevt Sbar BKG from QCD MuEnriched sample
#MC_Sbar_Xevt_Bkg_File = ROOT.TFile.Open("/afs/cern.ch/work/w/wvetens/Sexaquarks/CMSSW_10_2_26/src/SexaQAnalysis/AnalyzerAllSteps/macros/BDT/MC_Xevt_Bkg_QCD.root")
#MC_Sbar_Xevt_Bkg_Tree = MC_Sbar_Xevt_Bkg_File.Get("FlatTreeProducerBDT/FlatTree")

if not DoGenMass and not DoPostCuts:
    #Data S Bkg from Bparking UL 2018 NO PRESELECTION
    Data_S_Bkg_File = ROOT.TFile.Open("root://cmsxrootd.hep.wisc.edu//store/user/wvetens/data_Sexaq/FlatTree_BDT/Data_BPH_NoPresel_Fragment.root")
    Data_S_Bkg_Tree = Data_S_Bkg_File.Get("FlatTreeProducerBDT/FlatTree")
    
    #Data Xevt Sbar Bkg from Bparking UL 2018 NO PRESELECTION
    Data_Sbar_XEvt_Bkg_File = ROOT.TFile.Open("root://cmsxrootd.hep.wisc.edu//store/user/wvetens/data_Sexaq/FlatTree_BDT/Data_BPH_Xevt.root")
    Data_Sbar_XEvt_Bkg_Tree = Data_Sbar_XEvt_Bkg_File.Get("FlatTreeProducerBDT/FlatTree")
    #Data Xevt S Bkg from Bparking UL 2018 NO PRESELECTION
    Data_S_XEvt_Bkg_File = Data_Sbar_XEvt_Bkg_File
    Data_S_XEvt_Bkg_Tree = Data_Sbar_XEvt_Bkg_Tree
#if DoPostCuts:
#    #Data S Bkg from Bparking UL 2018
#    Data_S_Bkg_File = ROOT.TFile.Open("root://cmsxrootd.hep.wisc.edu//store/user/wvetens/data_Sexaq/FlatTree_BDT/ParkingBPH_FULL_trialB_BDTNTuple.root")
#    Data_S_Bkg_Tree = Data_S_Bkg_File.Get("FlatTreeProducerBDT/FlatTree")
if DoGenMass:
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
elif not DoBGComparison and not BGMCCompare and DoPostCuts:
    MC_AntiS_Sgn_File_M2SReweigh_AllMass = ROOT.TFile.Open("/afs/cern.ch/work/w/wvetens/Sexaquarks/CMSSW_10_2_26/src/SexaQAnalysis/AnalyzerAllSteps/macros/BDT/SignalSbar_FULL.root")
    MC_AntiS_Sgn_Tree_M2SReweigh_AllMass = MC_AntiS_Sgn_File_M2SReweigh_AllMass.Get("FlatTreeProducerBDT/FlatTree")
elif not DoGenMass and not DoPostCuts:
#only looking at 1.8 GeV for PreCuts because these decisions were made pre-multiple mass points
    MC_AntiS_Sgn_File_M2SReweigh_1p8GeV = ROOT.TFile.Open("root://cmsxrootd.hep.wisc.edu//store/user/wvetens/crmc_Sexaq/FlatTree_BDT/BlockAPUReweighed_Signal_1p8_M2S.root")
    MC_AntiS_Sgn_Tree_M2SReweigh_1p8GeV = MC_AntiS_Sgn_File_M2SReweigh_1p8GeV.Get("FlatTreeProducerBDT/FlatTree")
else:
    MC_AntiS_Sgn_File_M2SReweigh_AllMass = ROOT.TFile.Open("/afs/cern.ch/work/w/wvetens/Sexaquarks/CMSSW_10_2_26/src/SexaQAnalysis/TMVA/Step2/BDTApplied_unblindMC_dataset_BDT_AllFeatures_dataset_BDT_BPH_Full_TrialB_AllPreSelection_SignalWeighing_PV_MultiToSingle_Eta_OverlapCheckFalse/DiscrApplied_SignalSbar_FULL.root")
    MC_AntiS_Sgn_Tree_M2SReweigh_AllMass = MC_AntiS_Sgn_File_M2SReweigh_AllMass.Get("FlatTree")
if DoBGComparison:
    #bdt applied
    Data_S_Bkg_File = ROOT.TFile.Open("/afs/cern.ch/work/w/wvetens/Sexaquarks/CMSSW_10_2_26/src/SexaQAnalysis/TMVA/Step2/BDTApplied_bkgReference_dataset_BDT_AllFeatures_dataset_BDT_BPH_Full_TrialB_AllPreSelection_SignalWeighing_PV_MultiToSingle_Eta_OverlapCheckFalse/DiscrApplied_Data_BPH_Full_trialB.root")
    Data_S_Bkg_Tree = Data_S_Bkg_File.Get("FlatTree")
    #bdt < 0.1
    Data_Sbar_Bkg_File = ROOT.TFile.Open("/afs/cern.ch/work/w/wvetens/Sexaquarks/CMSSW_10_2_26/src/SexaQAnalysis/TMVA/Step2/BDTApplied_partialUnblinding_dataset_BDT_AllFeatures_dataset_BDT_BPH_Full_TrialB_AllPreSelection_SignalWeighing_PV_MultiToSingle_Eta_OverlapCheckFalse/DiscrApplied_Data_BPH_Full_trialB.root")
    Data_Sbar_Bkg_Tree = Data_Sbar_Bkg_File.Get("FlatTree")
    #Data Xevt Sbar Bkg from Bparking UL 2018
    Data_Sbar_XEvt_Bkg_File = ROOT.TFile.Open("root://cmsxrootd.hep.wisc.edu//store/user/wvetens/data_Sexaq/FlatTree_BDT/DiscrApplied_unblind/50PrevEvt_XEVT_reco/unblind_DiscrApplied_1p7GeV_BPH_XEVT_TrialB_50PrevEvt_Full.root")
    Data_Sbar_XEvt_Bkg_Tree = Data_Sbar_XEvt_Bkg_File.Get("FlatTree")
    #Data Xevt S Bkg from Bparking UL 2018
    Data_S_XEvt_Bkg_File = ROOT.TFile.Open("root://cmsxrootd.hep.wisc.edu//store/user/wvetens/data_Sexaq/FlatTree_BDT/DiscrApplied_bkgReference/50PrevEvt_XEVT_reco/bkgReference_DiscrApplied_1p7GeV_BPH_XEVT_TrialB_50PrevEvt_Full.root")
    Data_S_XEvt_Bkg_Tree = Data_S_XEvt_Bkg_File.Get("FlatTree")
elif BGMCCompare:
    #MC S BKG from QCD MuEnriched sample
    MC_S_Bkg_File = ROOT.TFile.Open("/afs/cern.ch/work/w/wvetens/Sexaquarks/CMSSW_10_2_26/src/SexaQAnalysis/TMVA/Step2/BDTApplied_bkgReference_dataset_BDT_AllFeatures_dataset_BDT_BPH_Full_TrialB_AllPreSelection_SignalWeighing_PV_MultiToSingle_Eta_OverlapCheckFalse/DiscrApplied_QCD_MC_BG.root")
    MC_S_Bkg_Tree = MC_S_Bkg_File.Get("FlatTree")
    
    #MC Sbar BKG from QCD MuEnriched sample (Same file, just look at sbar instead of s)
    MC_Sbar_Bkg_File = MC_S_Bkg_File
    MC_Sbar_Bkg_Tree = MC_Sbar_Bkg_File.Get("FlatTree")

    Data_S_Bkg_File = ROOT.TFile.Open("/afs/cern.ch/work/w/wvetens/Sexaquarks/CMSSW_10_2_26/src/SexaQAnalysis/TMVA/Step2/BDTApplied_bkgReference_dataset_BDT_AllFeatures_dataset_BDT_BPH_Full_TrialB_AllPreSelection_SignalWeighing_PV_MultiToSingle_Eta_OverlapCheckFalse/DiscrApplied_Data_BPH_Full_trialB.root")
    Data_S_Bkg_Tree = Data_S_Bkg_File.Get("FlatTree")


#Legend = ["MC-S-BKG"   ,"MC-#bar{S}-BKG" ,"Data-S-BKG"   ,"Data-#bar{S}-BKG (BDT < 0.1)  ","Data-#bar{S}-X event BKG" ,"MC-#bar{S}-Signal"]
#l_tree = [MC_S_Bkg_Tree,MC_AntiS_Bkg_Tree,Data_S_Bkg_Tree,Data_AntiS_Bkg_Tree             , Data_AntiS_XEvent_Tree    , MC_AntiS_Sgn_Tree]
#Legend = ["Data-S-BKG"   ,"Data-#bar{S}-X event BKG" ,"MC-#bar{S}-Signal"]
#l_tree = [Data_S_Bkg_Tree, Data_AntiS_XEvent_Tree    , MC_AntiS_Sgn_Tree]

#For Data S BG to Signal MC
#colours = [2,30]
#markerStyle = [22,23]
#Legend = ["Data-S-BKG"   ,"MC-AllMass-Multi-to-Single-Reweighed-#bar{S}-Signal"]
#l_tree = [Data_S_Bkg_Tree, MC_AntiS_Sgn_Tree_M2SReweigh_AllMass]

if not DoGenMass and DoPostCuts:
    #For Data S BG to Signal MC with Cross-Event as well
    if BGMCCompare:
        colours = [1,2,4,35,30,43,6]
        markerStyle = [21,20,22,23,33,34,35]
        Legend = ["MC-AllMass-Multi-to-Single-Reweighed-#bar{S}-Signal","Data-S-BKG"   ]
        l_tree = [MC_AntiS_Sgn_Tree_M2SReweigh_AllMass                 ,Data_S_Bkg_Tree]
        Legend += ["QCD_MC_S_Bkg", "QCD_MC_Sbar_Bkg"]
        l_tree += [MC_S_Bkg_Tree,  MC_Sbar_Bkg_Tree ]
    else:
        colours = [1,2,4,35,30,43,6]
        markerStyle = [21,20,22,23,33,34,35]
        Legend = ["MC-AllMass-Multi-to-Single-Reweighed-#bar{S}-Signal","Data-S-BKG"   ,"Data-#bar{S}-BKG BDT<0.1"   ]
        l_tree = [MC_AntiS_Sgn_Tree_M2SReweigh_AllMass                 ,Data_S_Bkg_Tree,Data_Sbar_Bkg_Tree]
        if DoBGComparison:
            Legend += ["Data-S-BKG-X-event","Data-#bar{S}-BKG-X-event"]
            l_tree += [Data_S_XEvt_Bkg_Tree,Data_Sbar_XEvt_Bkg_Tree   ]
elif not DoPostCuts and not DoGenMass:
    colours = [1,2,4,35,30,43,6]
    markerStyle = [21,20,22,23,33,34,35]
    Legend = ["MC-1.8GeV-Multi-to-Single-Reweighed-#bar{S}-Signal","Data-S-BKG"   ]#,"Data-#bar{S}-BKG BDT<0.1"   ]
    l_tree = [MC_AntiS_Sgn_Tree_M2SReweigh_1p8GeV                 ,Data_S_Bkg_Tree]#,Data_Sbar_Bkg_Tree           ]
    if DoBGComparison:
        Legend += ["Data-S-BKG-X-event","Data-#bar{S}-BKG-X-event"]
        l_tree += [Data_S_XEvt_Bkg_Tree,Data_Sbar_XEvt_Bkg_Tree   ]
    if BGMCCompare:
        Legend += ["QCD_MC_S_Bkg","QCD_MC_Sbar_Bkg"]
        l_tree += [MC_S_Bkg_Tree ,MC_Sbar_Bkg_Tree ]
elif BGMCCompare:
    colours = [1,2,4,35,30,43,6]
    markerStyle = [21,20,22,23,33,34,35]
    Legend = ["MC-AllMass-Multi-to-Single-Reweighed-#bar{S}-Signal","Data-S-BKG"   ]
    l_tree = [MC_AntiS_Sgn_Tree_M2SReweigh_AllMass                 ,Data_S_Bkg_Tree]
    Legend += ["QCD_MC_S_Bkg", "QCD_MC_Sbar_Bkg"]
    l_tree += [MC_S_Bkg_Tree,  MC_Sbar_Bkg_Tree ]

#For comparisons of different GEN masses to the full sample:
if DoGenMass:
    colours = [30,43,1,6,20,25]
    markerStyle = [23,21,22,24,25,26]
    Legend = ["MC-1.7GeV-Multi-to-Single-Reweighed-#bar{S}-Signal"         ,"MC-1.8GeV-Multi-to-Single-Reweighed-#bar{S}-Signal"         ,"MC-1.85GeV-Multi-to-Single-Reweighed-#bar{S}-Signal"         ,"MC-1.9GeV-Multi-to-Single-Reweighed-#bar{S}-Signal"         ,"MC-2GeV-Multi-to-Single-Reweighed-#bar{S}-Signal"         ]#,"MC-AllMass-Multi-to-Single-Reweighed-#bar{S}-Signal"         ]
    l_tree = [MC_AntiS_Sgn_Tree_M2SReweigh_1p7GeV                          ,MC_AntiS_Sgn_Tree_M2SReweigh_1p8GeV                          ,MC_AntiS_Sgn_Tree_M2SReweigh_1p85GeV                          ,MC_AntiS_Sgn_Tree_M2SReweigh_1p9GeV                          ,MC_AntiS_Sgn_Tree_M2SReweigh_2GeV                          ]#,MC_AntiS_Sgn_Tree_M2SReweigh_AllMass                          ]

#For MC QCD BG to Data S BG to MC Signal
#colours = [4,2,35,30,43,1,6]
#markerStyle = [20,21,22,23,33,34,35]
#Legend = ["MC-S-BKG"   ,"MC-#bar{S}-BKG","Data-S-BKG"   ,"MC-Multi-to-Single-Reweighed-#bar{S}-Signal"]
#l_tree = [MC_S_Bkg_Tree,MC_Sbar_Bkg_Tree,Data_S_Bkg_Tree,MC_AntiS_Sgn_Tree_M2SReweigh_AllMass         ]

#plots_output_dir = "plots_BackgroundVsSignal/"+configuration+"/"
#plots_output_dir = "plots_BDTInputs_NoPresel/"
#plots_output_dir = "plots_BDTInputs_MinPresel/"
#plots_output_dir = "plots_BDTInputs_NoCuts/"
#subdir = "BackgroundVsSignal/"
if DoGenMass:
    subdir = "GENMass_comparison/"
elif DoPostCuts:
    if HighBDT:
        subdir = "HighClassifier/"
    elif BGMCCompare:
        subdir = "BGMCCompare/"
    else:
        subdir = "BDTInputs/"
else:
    subdir = "NoCuts/"
if not args.addXevtWeights:
    subdir = 'NoXevtnPVWeight/'
#subdir = ""
plots_output_dir = "plots_BDTInputs_05Oct2023/"+subdir
print "Saving plots in: ", plots_output_dir
#plots_output_dir = "plots_BDTInputs_Test/"

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

	gROOT.cd()
	print "---------------------------------------------------"
	print "running for ", Legend[iTree]
	nEntries1 = tree.GetEntries()
        nFiducialPass = 0

	h_S_nGoodPVs = TH1F('h_S_nGoodPVs','; Number of Primary Vertices; Events/N_{ev}/Primary Vertex',60,0,60)
        if DoBeforeAfterPV:
	    h_S_nGoodPVs_before = TH1F('h_S_nGoodPVs_before','; Number of Primary Vertices; Events/N_{ev}/Primary Vertex',60,0,60)
	#h_S_bestPVz = TH1F('h_S_bestPVz','; PV Z location (cm); Events/N_{ev}/3cm',50,-25,25)

	h_S_vz_interaction_vertex= TH1F('h_S_vz_interaction_vertex','; absolute v_{z} iv ^{(}#bar{S} ^{)} (cm); Events/N_{ev}/cm',60,-30,30)
	#h_S_lxy_interaction_vertex = TH1F('h_S_lxy_interaction_vertex','; l_{0,bpc} iv ^{(}#bar{S} ^{)} (cm); Events/N_{ev}/0.01mm',38,2.02,2.4)

	h_S_daughters_deltaphi = TH1F('h_S_daughters_deltaphi','; #Delta#phi( ^{(} #bar{#Lambda} ^{)} ^{0} , K_{S}^{0}) (rad); Events/N_{ev}/0.2rad',32,-3.2,3.2)
	h_S_daughters_deltaeta = TH1F('h_S_daughters_deltaeta','; #Delta#eta( ^{(} #bar{#Lambda} ^{)} ^{0} , K_{S}^{0}) ; Events/N_{ev}/0.2rad',21,-2.1,2.1)
	#h_S_daughters_openingsangle = TH1F('h_S_daughters_openingsangle','; openings angle( ^{(} #bar{#Lambda} ^{)} ^{0} , K_{S}^{0} ) (rad); Events/N_{ev}/0.05rad',34,0.4,2.1)
	h_S_daughters_DeltaR = TH1F('h_S_daughters_DeltaR','; #DeltaR( ^{(} #bar{#Lambda} ^{)} ^{0} , K_{S}^{0} ); Events/N_{ev}/0.1rad',35,0.5,4)
	#h_S_Ks_openingsangle = TH1F('h_S_Ks_openingsangle','; openings angle( ^{(} #bar{S} ^{)} , K_{S}^{0}) (rad); Events/N_{ev}/0.1rad',20,0,2)
	#h_S_Lambda_openingsangle = TH1F('h_S_Lambda_openingsangle','; openings angle( ^{(} #bar{#Lambda} ^{)} ^{0} ,  ^{(} #bar{S} ^{)} ) (rad); Events/N_{ev}/0.05rad',20,0,1)

	h_S_eta = TH1F('h_S_eta','; #eta( ^{(} #bar{S} ^{)} ); Events/N_{ev}/0.25rad',38,-3.5,3.5)
	h_Ks_eta = TH1F('h_Ks_eta','; #eta(K_{S}^{0}) ; Events/N_{ev}/0.25rad',20,-2.5,2.5)
	#h_Lambda_eta = TH1F('h_Lambda_eta','; #eta( ^{(} #bar{#Lambda} ^{)} ^{0}); Events/N_{ev}/0.5#eta',20,-5,5)

	#h_S_dxy_over_lxy = TH1F('h_S_dxy_over_lxy','; d_{0,bs}/l_{0,bs} ( ^{(} #bar{S} ^{)} ); Events/N_{ev}/0.025',20,0,0.5)
	h_Ks_dxy_over_lxy = TH1F('h_Ks_dxy_over_lxy','; d_{0,bs}/l_{0,bs} (K_{S}^{0}); Events/N_{ev}/0.1',20,-1,1)
	h_Lambda_dxy_over_lxy = TH1F('h_Lambda_dxy_over_lxy','; d_{0,bs}/l_{0,bs} ( ^{(} #bar{#Lambda} ^{)} ^{0}) ; Events/N_{ev}/0.1',20,-1,1)

#	h_S_dz_min = TH1F('h_S_dz_min','; min d_{z,bs}  ^{(} #bar{S} ^{)}  (cm); Events/N_{ev}/0.5cm',24,-6,6)
	h_Ks_dz_min = TH1F('h_Ks_dz_min','; min d_{z,bs} K_{S}^{0} (cm); Events/N_{ev}/cm',60,-30,30)
	h_Lambda_dz_min = TH1F('h_Lambda_dz_min','; min d_{z,bs}  ^{(} #bar{#Lambda} ^{)} ^{0}  (cm); Events/N_{ev}/cm',60,-30,30)

	h_Ks_pt = TH1F('h_Ks_pt','; p_{t} K_{S}^{0} (GeV/c); Events/N_{ev}/0.4GeV/c',20,0,8)

	h_Lambda_lxy_decay_vertex = TH1F('h_Lambda_lxy_decay_vertex','; l_{0} ^{(} #bar{#Lambda} ^{)} ^{0} decay vertex (cm); Events/N_{ev}/cm',20,1.9,21.9)
	h_S_chi2_ndof = TH1F('h_S_chi2_ndof','; #chi^{2}/ndof ^{(}#bar{S} ^{)} annihilation vertex; Events/N_{ev}',44,0,11)

	#h_S_pz = TH1F('h_S_pz','; p_{z}  ( ^{(} #bar{S} ^{)} ) (GeV/c); Events/N_{ev}/5GeV/c',16,-40,40)

	#h_S_error_lxy_interaction_vertex = TH1F('h_S_error_lxy_interaction_vertex','; #sigma(l_{0,bpc} iv ^{(}#bar{S} ^{)} ) (cm); Events/N_{ev}/0.004mm',10,0,0.04)
	h_S_mass = TH1F('h_S_mass','; m_{ ^{(} #bar{S} ^{)} ,obs} (GeV/c^{2}); Events/N_{ev}/0.25GeV/c^{2}',40,-5,5)
        if DoPostCuts:
	    h_S_lxy_interaction_vertex = TH1F('h_S_lxy_interaction_vertex','; l_{0,bpc} iv ^{(}#bar{S} ^{)} (cm); Events/N_{ev}/0.01mm',38,2.02,2.4)
	    h_S_dxy_over_lxy = TH1F('h_S_dxy_over_lxy','; d_{0,bs}/l_{0,bs} ( ^{(} #bar{S} ^{)} ); Events/N_{ev}/0.025',20,0,0.5)
	    h_S_daughters_openingsangle = TH1F('h_S_daughters_openingsangle','; openings angle( ^{(} #bar{#Lambda} ^{)} ^{0} , K_{S}^{0} ) (rad); Events/N_{ev}/0.05rad',34,0.4,2.1)
	    h_S_Ks_openingsangle = TH1F('h_S_Ks_openingsangle','; openings angle( ^{(} #bar{S} ^{)} , K_{S}^{0}) (rad); Events/N_{ev}/0.1rad',20,0,2)
	    h_S_Lambda_openingsangle = TH1F('h_S_Lambda_openingsangle','; openings angle( ^{(} #bar{#Lambda} ^{)} ^{0} ,  ^{(} #bar{S} ^{)} ) (rad); Events/N_{ev}/0.05rad',20,0,1)
	    h_S_dz_min = TH1F('h_S_dz_min','; min d_{z,bs}  ^{(} #bar{S} ^{)}  (cm); Events/N_{ev}/0.5cm',24,-6,6)
        else:
            h_S_lxy_interaction_vertex = TH1F('h_S_lxy_interaction_vertex','; l_{0,bpc} iv ^{(}#bar{S} ^{)} (cm); Events/N_{ev}/0.01mm',100,2.00,3.0)
	    h_S_dxy_over_lxy = TH1F('h_S_dxy_over_lxy','; d_{0,bs}/l_{0,bs} ( ^{(} #bar{S} ^{)} ); Events/N_{ev}/0.025',80,-1,1)
	    h_S_daughters_openingsangle = TH1F('h_S_daughters_openingsangle','; openings angle( ^{(} #bar{#Lambda} ^{)} ^{0} , K_{S}^{0} ) (rad); Events/N_{ev}/0.05rad',64,0,3.2)
	    h_S_Ks_openingsangle = TH1F('h_S_Ks_openingsangle','; openings angle( ^{(} #bar{S} ^{)} , K_{S}^{0}) (rad); Events/N_{ev}/0.1rad',32,0,3.2)
	    h_S_Lambda_openingsangle = TH1F('h_S_Lambda_openingsangle','; openings angle( ^{(} #bar{#Lambda} ^{)} ^{0} ,  ^{(} #bar{S} ^{)} ) (rad); Events/N_{ev}/0.05rad',64,0,3.2)
	    h_S_dz_min = TH1F('h_S_dz_min','; min d_{z,bs}  ^{(} #bar{S} ^{)}  (cm); Events/N_{ev}/0.5cm',48,-12,12)
        if DoGenMass:
	    h_GEN_S_mass = TH1F('h_GEN_S_mass','; m_{ ^{(} #bar{S} ^{)} ,GEN} (GeV/c^{2}); Events/N_{ev}/10MeV/c^{2}',50,1.6,2.1)

	h2_S_daughters_DeltaR_vs_S_lxy_interaction_vertex = TH2F('h_S_daughters_DeltaR_vs_S_lxy_interaction_vertex','; #DeltaR( ^{(} #bar{#Lambda} ^{)} ^{0} , K_{S}^{0} ); l_{0,bpc} iv ^{(}#bar{S} ^{)} (cm); Events/N_{ev}/0.25GeV/c^{2}',35,0,3.5,31,1.9,2.52)
	h2_S_daughters_openingsangle_vs_S_lxy_interaction_vertex = TH2F('h_S_daughters_openingsangle_vs_S_lxy_interaction_vertex','; openings angle( ^{(} #bar{#Lambda} ^{)} ^{0} , K_{S}^{0} ) (rad); l_{0,bpc} iv ^{(}#bar{S} ^{)} (cm);Events/N_{ev}/0.25GeV/c^{2}',35,0,3.5,31,1.9,2.52)

        if DoBGComparison or BGMCCompare:
	    h_S_BDT = TH1F('h_S_BDT','; BDT classifier; Events/N_{ev}/0.05 BDT class.',40,-1,1)
	tprof_reweighing_factor = TProfile('tprof_reweighing_factor',';#eta ^{(}#bar{S} ^{)};reweighing factor',20,-5,5,0,50)

        if('#bar{S}-Signal' in Legend[iTree] or 'MC-Multi-#bar{S}-Signal' in Legend[iTree] or 'Multi-to-Single-Reweighed-#bar{S}-Signal' in Legend[iTree]): #if MC signal reweigh both for the pathlength through the beampipe and for the z location of the PV and PU
            print "N entries:", nEntries1
	for i in range(0,nEntries1):
		if(i==maxEvents):
			break
		if(i%1e4 == 0):
		#if(i%1e2 == 0):
			print "reached entry: ", i
		tree.GetEntry(i)
		#if(i%1e2 == 0):
		#	print "accessed entry: ", i
                    
		#if(i==0): print 'charge of the S/antiS: ', tree._S_charge[0]
		
		#for when you have the BDT parameter in your tree:
		if HighBDT and (tree.SexaqBDT <= min_BDT_classifier):continue

                ###OLD
		###need to reweigh the MC signal events, because the ones with high eta are more important, because they will pass more material
		##reweighing_factor = config.calc_reweighing_factor(tree._S_eta[0],'MC-#bar{S}-Signal' in Legend[iTree])
		reweighing_factor = 1
                #if 'x-event' not in Legend[iTree].lower():
                #    continue
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
                # PV Reweighting for Xevt
                if 'x-event' in Legend[iTree].lower() and DoPostCuts and DoBGComparison and UseXevtWeights:
                    reweighing_factor = float(weights_PU_Xevt[str(int(tree._S_nGoodPVs[0]))])
                    #print tree._S_nGoodPVs[0]
                    #print int(tree._S_nGoodPVs[0])
                    #earlykill += 1
                    #if earlykill >= 10:
                    #    quit()
		#elif('MC-S-BKG' in Legend[iTree] or 'MC-#bar{S}-BKG' or 'MC-#bar{S}-Xevt-BKG' in Legend[iTree]):#if MC background only reweigh for the z location of the PV and PU
		#	reweighing_factor = tree._S_event_weighting_factorPU[0]
                # for the S background we want to look at S, otherwise we want to look at Sbar
                if(('Data-S-BKG' in Legend[iTree] or 'MC-S-BKG' in Legend[iTree]) and tree._S_charge[0] == -1): 
                    continue
                elif(tree._S_charge[0] == 1 and '#bar{S}' in Legend[iTree]): continue
                if DoBeforeAfterPV:
	            h_S_nGoodPVs_before.Fill(tree._S_nGoodPVs[0],reweighing_factor)

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
		#h_S_bestPVz.Fill(tree._S_bestPVz[0],reweighing_factor)

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
		#h_Lambda_eta.Fill(tree._Lambda_eta[0],reweighing_factor)

		h_S_dxy_over_lxy.Fill(tree._S_dxy_over_lxy[0],reweighing_factor)
		h_Ks_dxy_over_lxy.Fill(tree._Ks_dxy_over_lxy[0],reweighing_factor)
		h_Lambda_dxy_over_lxy.Fill(tree._Lambda_dxy_over_lxy[0],reweighing_factor)

		h_S_dz_min.Fill(tree._S_dz_min[0],reweighing_factor)
		h_Ks_dz_min.Fill(tree._Ks_dz_min[0],reweighing_factor)
		h_Lambda_dz_min.Fill(tree._Lambda_dz_min[0],reweighing_factor)

		h_Ks_pt.Fill(tree._Ks_pt[0],reweighing_factor)
		
		h_Lambda_lxy_decay_vertex.Fill(tree._Lambda_lxy_decay_vertex[0],reweighing_factor)
		h_S_chi2_ndof.Fill(tree._S_chi2_ndof[0],reweighing_factor)

		#h_S_pz.Fill(tree._S_pz[0],reweighing_factor)

		#h_S_error_lxy_interaction_vertex.Fill(tree._S_error_lxy_interaction_vertex_beampipeCenter[0],reweighing_factor)  
		h_S_mass.Fill(tree._S_mass[0],reweighing_factor)
                if DoGenMass:
		    h_GEN_S_mass.Fill(round(tree._GEN_S_mass[0],2),reweighing_factor)
                
                if DoBGComparison or BGMCCompare:
		    h_S_BDT.Fill(tree.SexaqBDT,reweighing_factor)
	        h2_S_daughters_DeltaR_vs_S_lxy_interaction_vertex.Fill(tree._S_daughters_DeltaR[0], tree._S_lxy_interaction_vertex_beampipeCenter[0], reweighing_factor)
	        h2_S_daughters_openingsangle_vs_S_lxy_interaction_vertex.Fill(tree._S_daughters_openingsangle[0], tree._S_lxy_interaction_vertex_beampipeCenter[0], reweighing_factor)

		tprof_reweighing_factor.Fill(tree._S_eta[0],reweighing_factor)	

#	TH1_l = [h_S_vz_interaction_vertex,h_S_lxy_interaction_vertex,h_S_daughters_deltaphi,h_S_daughters_deltaeta,h_S_daughters_openingsangle,h_S_daughters_DeltaR,h_S_Ks_openingsangle,h_S_Lambda_openingsangle,h_S_eta,h_Ks_eta,h_Lambda_eta,h_S_dxy_over_lxy,h_Ks_dxy_over_lxy,h_Lambda_dxy_over_lxy,h_S_dz_min,h_Ks_dz_min,h_Lambda_dz_min,h_Ks_pt,h_Lambda_lxy_decay_vertex,h_S_chi2_ndof,h_S_pz,h_S_error_lxy_interaction_vertex,h_S_mass,h_S_BDT,tprof_reweighing_factor]
# For now, not doing the h_S_BDT
        TH1_l = []
        if DoGenMass:
	    TH1_l = [h_S_nGoodPVs, h_S_vz_interaction_vertex,h_S_lxy_interaction_vertex,h_S_daughters_deltaphi,h_S_daughters_deltaeta,h_S_daughters_openingsangle,h_S_daughters_DeltaR,h_S_Ks_openingsangle,h_S_Lambda_openingsangle,h_S_eta,h_Ks_eta,h_S_dxy_over_lxy,h_Ks_dxy_over_lxy,h_Lambda_dxy_over_lxy,h_S_dz_min,h_Ks_dz_min,h_Lambda_dz_min,h_Ks_pt,h_Lambda_lxy_decay_vertex,h_S_chi2_ndof,h_S_mass,h_GEN_S_mass,tprof_reweighing_factor]
        elif not DoBGComparison and not BGMCCompare:
	    TH1_l = [h_S_nGoodPVs, h_S_vz_interaction_vertex,h_S_lxy_interaction_vertex,h_S_daughters_deltaphi,h_S_daughters_deltaeta,h_S_daughters_openingsangle,h_S_daughters_DeltaR,h_S_Ks_openingsangle,h_S_Lambda_openingsangle,h_S_eta,h_Ks_eta,h_S_dxy_over_lxy,h_Ks_dxy_over_lxy,h_Lambda_dxy_over_lxy,h_S_dz_min,h_Ks_dz_min,h_Lambda_dz_min,h_Ks_pt,h_Lambda_lxy_decay_vertex,h_S_chi2_ndof,h_S_mass,tprof_reweighing_factor]
        else:
	    TH1_l = [h_S_nGoodPVs, h_S_vz_interaction_vertex,h_S_lxy_interaction_vertex,h_S_daughters_deltaphi,h_S_daughters_deltaeta,h_S_daughters_openingsangle,h_S_daughters_DeltaR,h_S_Ks_openingsangle,h_S_Lambda_openingsangle,h_S_eta,h_Ks_eta,h_S_dxy_over_lxy,h_Ks_dxy_over_lxy,h_Lambda_dxy_over_lxy,h_S_dz_min,h_Ks_dz_min,h_Lambda_dz_min,h_Ks_pt,h_Lambda_lxy_decay_vertex,h_S_chi2_ndof,h_S_mass,h_S_BDT,tprof_reweighing_factor]
	#TH1_l = [h_S_nGoodPVs, h_S_bestPVz]
	for h in TH1_l:
		h.SetDirectory(0) 
	TH1_ll.append(TH1_l)

	TH2_l = [h2_S_daughters_DeltaR_vs_S_lxy_interaction_vertex, h2_S_daughters_openingsangle_vs_S_lxy_interaction_vertex]
	#TH2_l = []
	for h in TH2_l:
		h.SetDirectory(0) 
	TH2_ll.append(TH2_l)

        #print "Integral of BDT Classifier Histogram:\t", h_S_BDT.Integral()
        print "Efficiency of cuts in ", Legend[iTree], ":", nFiducialPass, "/", nEntries1, "=", nFiducialPass/float(nEntries1)
        if DoBeforeAfterPV:
            genmass=""
            legendtext=""
            if "Signal" in Legend[iTree]:
                if "GeV" in Legend[iTree]:
                    if "1.85" in Legend[iTree]:
                        legendtext = "MC m_{#bar{S}} = 1.85 GeV Signal"
                        genmass = "1p85"
                    elif "1.8" in Legend[iTree]:
                        legendtext = "MC m_{#bar{S}} = 1.8 GeV Signal"
                        genmass = "1p8"
                    elif "1.7" in Legend[iTree]:
                        legendtext = "MC m_{#bar{S}} = 1.7 GeV Signal"
                        genmass = "1p7"
                    elif "1.9" in Legend[iTree]:
                        legendtext = "MC m_{#bar{S}} = 1.9 GeV Signal"
                        genmass = "1p9"
                    elif "2" in Legend[iTree]:
                        legendtext = "MC m_{#bar{S}} = 2 GeV Signal"
                        genmass = "2"
                else:
                    legendtext = "MC #bar{S} Signal All Masses"
                    genmass = "AllMass"
            c_PV_name = "c_PV_" + genmass
            c_PV = ReadyCanvas(c_PV_name)
            legend_PV = TLegend(0.6,0.7,0.9,0.9) 
            legend_PV.SetFillStyle(0)
            legend_PV.SetBorderSize(0)
            c_PV.cd()
            if(h_S_nGoodPVs_before.Integral() != 0):
            	h_S_nGoodPVs_before.Scale(1./h_S_nGoodPVs_before.Integral(), "width");
            h_S_nGoodPVs_before.Draw("L")
	    legend_PV.AddEntry(h_S_nGoodPVs_before, legendtext+" Before Cuts","ep")
            c_PV.Update()
            if(h_S_nGoodPVs.Integral() != 0):
            	h_S_nGoodPVs.Scale(1./h_S_nGoodPVs.Integral(), "width");
            h_S_nGoodPVs.Draw("PCE1same")
	    legend_PV.AddEntry(h_S_nGoodPVs, legendtext,"ep")
            c_PV.Update()
	    h_S_nGoodPVs_before.SetLineColor(kBlack)
	    h_S_nGoodPVs_before.SetLineWidth(2)
	    h_S_nGoodPVs_before.SetMarkerStyle(markerStyle[iTree])
	    h_S_nGoodPVs_before.SetMarkerColor(kBlack)
	    h_S_nGoodPVs_before.SetMarkerSize(0.8)
	    h_S_nGoodPVs_before.SetStats(0)
	    h_S_nGoodPVs.SetLineColor(kRed)
	    h_S_nGoodPVs.SetLineWidth(2)
	    h_S_nGoodPVs.SetMarkerStyle(markerStyle[iTree])
	    h_S_nGoodPVs.SetMarkerColor(kRed)
	    h_S_nGoodPVs.SetMarkerSize(0.8)
	    h_S_nGoodPVs.SetStats(0)
            legend_PV.Draw("same")
            CMSStyle.setCMSLumiStyle(c_PV,11, lumiTextSize_=0.74)
            c_PV.Update()
	    c_PV.SaveAs(plots_output_dir+c_PV_name.replace(".", "p")+".pdf")
	iTree+=1
print "n Sbar:", nSbar

fOut = TFile(plots_output_dir+'macro_FlatTree_BDT.root','RECREATE')

nHistos = len(TH1_ll[0])
nSamples = len(TH1_ll)

c_all  = ReadyCanvas("c_all",1800,1400)
c_all_log  = ReadyCanvas("c_all_log",1600,1200)
c_all.Divide(6,5)
for i in range(0,nHistos):#each list contains a list of histograms. Each list represents background or signal. The histos need to be overlaid one list to the other
        if "mass" in TH1_ll[0][i].GetName():
	    h = TH1_ll[-1][i]
        else:
	    h = TH1_ll[0][i]
        #if ("BDT" not in h.GetName()):
        #    continue
	c_name = "c_"+h.GetName()
	c = ReadyCanvas(c_name)
	legend = TLegend(0.6,0.7,0.9,0.9)
        legend.SetFillStyle(0)
        legend.SetBorderSize(0)
	for j in range(0,nSamples):
		h = TH1_ll[j][i]
                #if ("BDT" not in h.GetName()):
                #    continue
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
			h.GetYaxis().SetRangeUser(5*1e-4,l_y_axis_ranges[i])
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
        CMSStyle.setCMSLumiStyle(c,11, lumiTextSize_=0.74)
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


i = 0
for l in TH2_ll:
	for h in l:
		c_name = "c_"+h.GetName()+"_"+Legend[i]
		c = ReadyCanvas(c_name)
		c.SetRightMargin(0.2) #make room for the tile of the z scale
		if(h.GetSumw2N() == 0):
			h.Sumw2(kTRUE)
                if h.Integral() != 0:
		    h.Scale(1./h.Integral(), "width");
		h.Draw("colz")
		h.SetStats(0)
                CMSStyle.setCMSLumiStyle(c,11, lumiTextSize_=0.74)
		c.SaveAs(plots_output_dir+c_name.replace(".", "p")+".pdf")
		c.Write()
	i += 1


fOut.Write()
fOut.Close()
