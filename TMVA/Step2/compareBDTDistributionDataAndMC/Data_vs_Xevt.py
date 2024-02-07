import ROOT
from ROOT import *
import numpy as np
import sys
import argparse

sys.path.append('/afs/cern.ch/work/w/wvetens/Sexaquarks/CMSSW_10_2_26/src/SexaQAnalysis/AnalyzerAllSteps/macros/tdrStyle')
import  CMSStyle

import sys
sys.path.insert(1, '../../../.')

#maxevts = 1e3
maxevts = 1e9
gROOT.SetBatch(kTRUE)
gStyle.SetLegendTextSize(0.08)

CMSStyle.extraText = "(CMS Data)"
#CMSStyle.extraText = "(CMS Simulation)"
CMSStyle.lumiText = "Parked 2018 data, "+"237 #times 10^{9}"+" Collisions (13 TeV)"
CMSStyle.cmsText = "Private Work"
CMSStyle.cmsTextFont = 42
CMSStyle.extraTextFont = 42
CMSStyle.lumiTextSize = 0.74
CMSStyle.cmsTextSize = 0.74
CMSStyle.relPosX = 2.36*0.045
CMSStyle.outOfFrame = False

CMSStyle.setTDRStyle()
parser = argparse.ArgumentParser()
parser.add_argument('--mass', dest='mass', action='store', default="", type=str)
parser.add_argument('--reweighedXevt', dest='reweighedXevt', action='store_true', default=False)
parser.add_argument('--Sbar', dest='Sbar', action='store_true', default=False)
args = parser.parse_args()

fXevtPUWeights = '/afs/cern.ch/work/w/wvetens/Sexaquarks/CMSSW_10_2_26/src/SexaQAnalysis/AnalyzerAllSteps/data/PUReweigh_nPV_XevtToDataBPH2018_FULL_POSTCUTS.txt'
weights_PU_Xevt = {line.split()[0] : line.split()[1] for line in open(fXevtPUWeights)}
#S is always going to be in the "...bkgReference..." folder, sbar is in "unblindMC_BG", "unblind", and "partialUnblinding" Depending on MC, Data Xevt, or Data BDT < 0.1 respectively
#samplename = "QCD_MC_Xevt"
#S_location = "../BDTApplied_bkgReference_dataset_BDT_AllFeatures_dataset_BDT_BPH_Full_TrialB_AllPreSelection_SignalWeighing_PV_MultiToSingle_Eta_OverlapCheckFalse/"
if not args.Sbar:
    S_location_data = "../BDTApplied_bkgReference_dataset_BDT_AllFeatures_dataset_BDT_BPH_Full_TrialB_AllPreSelection_SignalWeighing_PV_MultiToSingle_Eta_OverlapCheckFalse/"
    #for remote files:
    S_location = "root://cmsxrootd.hep.wisc.edu//store/user/wvetens/data_Sexaq/FlatTree_BDT/DiscrApplied_bkgReference/50PrevEvt_XEVT_reco/bkgReference_"
else:
    #really these are Sbar, not S
    S_location = "root://cmsxrootd.hep.wisc.edu//store/user/wvetens/data_Sexaq/FlatTree_BDT/DiscrApplied_unblind/50PrevEvt_XEVT_reco/unblind_"
    S_location_data = "../BDTApplied_partialUnblinding_dataset_BDT_AllFeatures_dataset_BDT_BPH_Full_TrialB_AllPreSelection_SignalWeighing_PV_MultiToSingle_Eta_OverlapCheckFalse/"
#Sbar_location = "../BDTApplied_unblindMC_BG_dataset_BDT_AllFeatures_dataset_BDT_BPH_Full_AllPreSelection_SignalWeighing_PV_MultiToSingle_Eta_OverlapCheckFalse/"
#samplename = "QCD_MC_BG"
#Sbar_location = "../BDTApplied_unblindMC_BG_dataset_BDT_AllFeatures_dataset_BDT_BPH_Full_AllPreSelection_SignalWeighing_PV_MultiToSingle_Eta_OverlapCheckFalse/"
if args.mass == "1p7" or args.mass == "1p8" or args.mass == "1p85" or args.mass == "1p9" or args.mass == "2": 
    samplename = args.mass+"GeV_BPH_XEVT_TrialB_50PrevEvt_Full"
    samplename_data = args.mass+"GeV_Data_BPH_Full_trialB"
else:
    samplename = "BPH_XEVT_TrialB_50PrevEvt_Full"
    # For nPV comparison
    #samplename = "Data_BPH_Full_trialB"
    samplename_data = "Data_BPH_Full_trialB"
#for remote files:
def ReadyCanvas(name, W=700, H=900):
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
def ReadyTopPad(n1, n2, xl, r, xh, yt):
    p = TPad(n1, n2, xl, r, xh, yt)
    p.SetTickx(0)
    p.SetFillStyle(0)
    p.SetTopMargin(0.07)
    p.SetBottomMargin(0.)
    p.SetRightMargin(0.02)
    p.Draw()
    p.cd()
    return p
def ReadyBotPad(n2, xl, yb, xh, r):
    p = TPad(n2, n2, xl, yb, xh, r)
    p.SetFillStyle(4000)
    p.SetTopMargin(0.)
    p.SetBottomMargin(0.3)
    p.SetRightMargin(0.02)
    p.Draw()
    p.cd()
    return p

def fixsplithist(htop, hbot):
    pmain = ROOT.TVirtualPad.Pad().GetCanvas()
    if not pmain:
        return
    p1 = pmain.cd(1)
    p2 = pmain.cd(2)
    
    if (not p1 or not p2):
        return
    scale = p1.GetHNDC() / p2.GetHNDC()
    
    #s = htop.GetYaxis().GetLabelSize() * scale
    #ss = htop.GetYaxis().GetLabelSize()

    hbot.GetYaxis().SetLabelSize(0.06)
    htop.GetYaxis().SetLabelSize(0.04)

    #s = htop.GetYaxis().GetTitleSize() * scale
    hbot.GetYaxis().SetTitleSize(0.06)
    
    hbot.GetYaxis().SetTitleOffset(0.8)
    htop.GetYaxis().SetTitleOffset(1.1)

    #s = htop.GetYaxis().GetLabelOffset() * scale

    #s = htop.GetXaxis().GetLabelSize() * scale

    hbot.GetXaxis().SetLabelSize(0.06)
    htop.GetXaxis().SetLabelSize(0.)
    #s = htop.GetXaxis().GetTitleSize() * scale
    hbot.GetXaxis().SetTitleSize(0.06)

    s = htop.GetXaxis().GetLabelOffset() * scale
    hbot.GetXaxis().SetLabelOffset(s)

    hbot.GetYaxis().SetNdivisions(5)

def colorIt(hMidA, kCyan):
    hMidA.SetMarkerColor(kCyan)
    hMidA.SetLineColor(kCyan)
    hMidA.SetMarkerStyle(22)
    hMidA.SetMarkerSize(0.8)
    #hMidA.SetFillColor(kCyan)
    #hMidA.SetFillStyle(0)
    hMidA.GetXaxis().SetLabelSize(0.05)
    hMidA.GetXaxis().SetTitleSize(0.06)
    hMidA.GetYaxis().SetTitleSize(0.05)
    #hMidA.GetYaxis().SetTitleOffset(0.55)
    hMidA.GetYaxis().SetTitleOffset(1)
    hMidA.GetYaxis().SetLabelSize(0.05)
    hMidA.SetTitleFont(42, "XYZ")
    hMidA.SetLabelFont(42, "XYZ")
if args.reweighedXevt:
    output_pdf_name = "../h_BDT_"+samplename+"_CompareDataXevt_Reweighed.pdf"
    output_root_name = "../BDT_"+samplename+"_CompareDataXevt_Reweighed.root"
else:
    output_pdf_name = "../h_BDT_"+samplename+"_CompareDataXevt.pdf"
    output_root_name = "../BDT_"+samplename+"_CompareDataXevt.root"
if args.Sbar:
    output_pdf_name = output_pdf_name.replace(".pdf","_Sbar.pdf")
    output_root_name = output_root_name.replace(".root","_Sbar.root")
gStyle.SetOptStat(0)
fOut = TFile(output_root_name, "RECREATE")
gStyle.SetOptStat(0)

fS_data = ROOT.TFile.Open(S_location_data + "DiscrApplied_" + samplename_data + ".root")
print "data S file:", S_location_data + "DiscrApplied_" + samplename_data + ".root"
fS = ROOT.TFile.Open(S_location + "DiscrApplied_" + samplename + ".root")
print "S file: ", S_location + "DiscrApplied_" + samplename + ".root"

tS_data = fS_data.Get("FlatTree")
tS = fS.Get("FlatTree")

hS_data = TH1F("h_S_data_BDT",'; BDT classifier; N_{ev}/0.02 BDT class.',60,-0.7,0.5)
hS = TH1F("h_S_BDT",'; BDT classifier; N_{ev}/0.02 BDT class.',60,-0.7,0.5)
if args.reweighedXevt:
    nEntries = tS.GetEntries()
    for i in range(0, nEntries):
        if i > maxevts:
            break
        tS.GetEntry(i)
        if tS._S_nGoodPVs[0] >= 60 or tS._S_nGoodPVs[0] <= 0:
            w = 0
        else:
            w = float(weights_PU_Xevt[str(int(tS._S_nGoodPVs[0]))])
        hS.Fill(tS.SexaqBDT, w)
else:
    tS.Project("h_S_BDT","SexaqBDT")
tS_data.Project("h_S_data_BDT","SexaqBDT")

hS_data.Sumw2()
hS.Sumw2()

fOut.cd()
gStyle.SetOptStat(0)
Mont = hS.Clone("Mont")
Mont.Divide(hS_data, hS, 1.0, 1.0)

#c1 = TCanvas("h_BDT_"+samplename, "", 700, 900)
#c1.Draw()
#c1.cd()
colorIt(hS, kRed)
c1 = ReadyCanvas("h_BDT_"+samplename, 700, 900)
xlow = 0
xhigh = 1
ytop = 1
ybot = 0
ratio = 0.3

p1 = ReadyTopPad("p1", "p2", xlow, ratio, xhigh, ytop)
hS.GetYaxis().SetRangeUser(0.2, hS.GetMaximum()*100)
legend = TLegend(0.6, 0.7, 0.95, 0.95)
gPad.SetLogy()
#gPad.SetGridx()
#gPad.SetGridy()

hS.SetStats(0)
hS_data.SetStats(0)
colorIt(hS_data, kBlue)

hS.SetMarkerStyle(23)
hS.Draw("peXOC")
hS_data.Draw("peXOCsame")
CMSStyle.setCMSLumiStyle(c1, 11, lumiTextSize_=0.74)

legend.AddEntry(hS,samplename+" Xevt S","ple");
#legend.AddEntry(hS,"No nPV " +samplename+" S","ple");
legend.AddEntry(hS_data,samplename + " Data S","ple");

hS_data.SetMarkerSize(0.8)
legend.Draw()

c1.cd()
p2 = ReadyBotPad("p2", xlow, ybot, xhigh, ratio)

gPad.SetGridy()
colorIt(Mont,kBlack)
#Mont.SetMinimum(0.5);
#Mont.SetMaximum(1.5);
Mont.GetXaxis().SetTitleOffset(1.2);
Mont.GetYaxis().SetTitleOffset(3.);
Mont.SetYTitle("Data S/Xevt S");
Mont.SetStats(0)
Mont.Draw("peX0C")
fixsplithist(hS, Mont)

gStyle.SetOptStat(0)
c1.cd()
c1.SetName(output_pdf_name)
c1.Write()
c1.SaveAs(output_pdf_name, ".pdf")


gStyle.SetOptStat(0)
fOut.Close()
