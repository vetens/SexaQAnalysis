import ROOT
from ROOT import *
import numpy as np
import sys
import argparse

sys.path.append('/afs/cern.ch/work/w/wvetens/Sexaquarks/CMSSW_10_2_26/src/SexaQAnalysis/AnalyzerAllSteps/macros/tdrStyle')
import  CMSStyle

import sys
sys.path.insert(1, '../../.')

gROOT.SetBatch(kTRUE)
gStyle.SetLegendTextSize(0.08)

CMSStyle.lumiText = "Parked 2018 data, "+"247 #times 10^{9}"+" Collisions (13 TeV)"
CMSStyle.cmsText = "Private Work"
CMSStyle.extraText = "(CMS data)"
CMSStyle.cmsTextFont = 42
CMSStyle.extraTextFont = 42
CMSStyle.lumiTextSize = 0.74
CMSStyle.cmsTextSize = 0.74
CMSStyle.relPosX = 2.36*0.045
CMSStyle.outOfFrame = False
CMSStyle.setTDRStyle()

parser = argparse.ArgumentParser()
#parser.add_argument('--fitType', dest='fitType', action='store', default='', type=str)
parser.add_argument('--mass', dest='mass', action='store', default="", type=str)
args = parser.parse_args()

BDT_cut_min = 0
BDT_cut_max = 0.605
BDT_cut_step = 0.005
#FitOpt = args.fitType
#FitOpt = "Pol0_-0.1"
#FitOpt = "Pol0_-0.2"
#FitOpt = "Pol0_-0.7"
#FitOpt = "Pol1_-0.1"
#FitOpt = "Pol1_-0.2"
#FitOpt = "Pol1_-0.7"
#FitOpt = "Pol2_-0.7"

#S is always going to be in the "...bkgReference..." folder, sbar is in "unblindMC_BG", "unblind", and "partialUnblinding" Depending on MC, Data Xevt, or Data BDT < 0.1 respectively
#samplename = "QCD_MC_Xevt"
#S_location = "../BDTApplied_bkgReference_dataset_BDT_AllFeatures_dataset_BDT_BPH_Full_TrialB_AllPreSelection_SignalWeighing_PV_MultiToSingle_Eta_OverlapCheckFalse/"
S_location = "BDTApplied_bkgReference_dataset_BDT_AllFeatures_dataset_BDT_BPH_Full_TrialB_AllPreSelection_SignalWeighing_PV_MultiToSingle_Eta_OverlapCheckFalse/"
#for remote files:
#Sbar_location = "../BDTApplied_unblindMC_BG_dataset_BDT_AllFeatures_dataset_BDT_BPH_Full_AllPreSelection_SignalWeighing_PV_MultiToSingle_Eta_OverlapCheckFalse/"
#samplename = "QCD_MC_BG"
#Sbar_location = "../BDTApplied_unblindMC_BG_dataset_BDT_AllFeatures_dataset_BDT_BPH_Full_AllPreSelection_SignalWeighing_PV_MultiToSingle_Eta_OverlapCheckFalse/"
if args.mass == "1p7" or args.mass == "1p8" or args.mass == "1p85" or args.mass == "1p9" or args.mass == "2": 
    samplename = args.mass+"GeV_Data_BPH_Full_trialB"
else:
    samplename = "Data_BPH_Full_trialB"
#for remote files:
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
    hMidA.GetXaxis().SetTitleOffset(1)
    hMidA.GetYaxis().SetTitleOffset(1.2)
    hMidA.GetYaxis().SetLabelSize(0.05)
    hMidA.SetTitleFont(42, "XYZ")
    hMidA.SetLabelFont(42, "XYZ")
#output_pdf_name = "Smoothed_BG/h_BDT_"+samplename+"_"+FitOpt+".pdf"
#output_root_name = "Smoothed_BG/BDT_"+samplename+"_"+FitOpt+".root"
output_pdf_name = "Smoothed_BG/h_BDT_"+samplename+"_PoissonLikeError.pdf"
output_logplot_pdf_name = "Smoothed_BG/h_BDT_"+samplename+"_PoissonLikeError_logscale.pdf"
output_root_name = "Smoothed_BG/BDT_"+samplename+"_PoissonLikeError.root"
gStyle.SetOptStat(0)
fOut = TFile(output_root_name, "RECREATE")
gStyle.SetOptStat(0)

fS = ROOT.TFile.Open(S_location + "DiscrApplied_" + samplename + ".root")
print "S file: ", S_location + "DiscrApplied_" + samplename + ".root"

tS = fS.Get("FlatTree")

hS = TH1F("h_S_BDT",'; BDT classifier; N_{ev}/'+str(BDT_cut_step)+" BDT class.",int((BDT_cut_max-BDT_cut_min)/BDT_cut_step),BDT_cut_min,BDT_cut_max)
tS.Project("h_S_BDT","SexaqBDT")
#i_e = 0.
#for e in range(0, int(BDT_cut_max/BDT_cut_step)):
#    BDT_cut = BDT_cut_min+i_e*BDT_cut_step
#    i_e+=1
#    count = tS.GetEntries("SexaqBDT > " + str(BDT_cut))
#    hS.SetBinContent(int(i_e), float(count))
#    hS.SetBinError(int(i_e), TMath.Sqrt(count))
hS.Sumw2()
#if "bound" in FitOpt.lower():
#    hSUp = TH1F("h_S_BDT_u",'; BDT classifier; N_{ev}/0.02 BDT class.',30,0,0.6)
#    hSDown = TH1F("h_S_BDT_d",'; BDT classifier; N_{ev}/0.02 BDT class.',30,0,0.6)
#    for i in xrange(1, 31):
#        errUp = hS.GetBinError(i)
#        hSUp.SetBinContent(i, errUp)
#        errDown = hS.GetBinErrorLow(i)
#        hSDown.SetBinContent(i, errDown)
#    hSUp.Add(hSUp, hS, 1, 1)
#    hSDown.Add(hSDown, hS, -1, 1)
#
fOut.cd()
gStyle.SetOptStat(0)
#c1 = TCanvas("h_BDT_"+samplename, "", 700, 900)
#c1.Draw()
#c1.cd()
colorIt(hS, kBlack)
c1 = TCanvas("h_BDT_"+samplename, "", 700, 900)
c1.SetFillColor(0)
c1.SetRightMargin(0.05)
c1.SetBorderMode(0)
c1.SetFrameFillStyle(0)
c1.SetFrameBorderMode(0)
c1.SetTickx(0)
c1.SetTicky(0)
c1.cd()

frame = c1.DrawFrame(BDT_cut_min,0.1, BDT_cut_max, 101)
frame.GetYaxis().CenterTitle()
frame.GetYaxis().SetTitleSize(0.05)
frame.GetXaxis().SetTitleSize(0.05)
frame.GetXaxis().SetLabelSize(0.04)
frame.GetYaxis().SetLabelSize(0.04)
#frame.GetYaxis().SetTitleOffset(0.5)
frame.GetXaxis().SetNdivisions(121)
frame.GetYaxis().CenterTitle(True)
frame.GetYaxis().SetTitle('N_{ev}/'+str(BDT_cut_step)+" BDT class.")
frame.GetXaxis().SetTitle("BDT classifier")
frame.SetMinimum(0)
frame.SetMaximum(hS.GetMaximum()*1.1)
c1.Draw()
legend = TLegend(0.5, 0.6, 0.95, 0.95)
#if "log" in FitOpt.lower():
#    gPad.SetLogy()
#gPad.SetGridx()
#gPad.SetGridy()

gStyle.SetOptStat(0)
hS.SetMarkerStyle(23)
hS.Draw("peXOC")

legend.AddEntry(hS,samplename+" S","ple");

fnS = TF1("fnS", "expo",BDT_cut_min,BDT_cut_max)
hS.Fit(fnS,"","",BDT_cut_min,BDT_cut_max)
hS.SetStats(0)
#confIntervals_data = TH1D("confIntervals_data", "Exponential Fit with .68 conf. band", int((BDT_cut_max-BDT_cut_min)/BDT_cut_step),BDT_cut_min,BDT_cut_max)
#TVirtualFitter.GetFitter().GetConfidenceIntervals(confIntervals_data, 0.68)
#if "ac" in FitOpt.lower():
fnSUp = TF1("fnSUp", "fnS+sqrt(fnS)", BDT_cut_min,BDT_cut_max) 
fnSDown = TF1("fnSDown", "fnS-sqrt(fnS)", BDT_cut_min,BDT_cut_max) 
#elif "bound" in FitOpt.lower():
#    fnSUp = TF1("fnSUp", "expo", 0, 0.6) 
#    hSUp.Fit(fnSUp, "", "", 0, 0.6)
#    fnSDown = TF1("fnSDown", "expo", 0, 0.6) 
#    hSDown.Fit(fnSDown, "", "", 0, 0.6)
gStyle.SetOptStat(0)
fnS.SetLineColor(kRed)
fnS.SetMarkerSize(0)
#confIntervals_data.SetStats(False)
#confIntervals_data.SetMarkerSize(0)
#confIntervals_data.SetFillColorAlpha(kRed-7, 0.5)
fnS.GetHistogram().SetStats(0)
fnSUp.GetHistogram().SetStats(0)
fnSDown.GetHistogram().SetStats(0)
fnS.Draw("c same")
#confIntervals_data.Draw("ce3 same")
legend.AddEntry(fnS,"fit S in "+samplename,"pl");
#if "err" in FitOpt.lower():
fnSUp.SetMarkerSize(0)
fnSUp.SetLineColor(kBlue)
fnSUp.Draw("c same")
fnSDown.SetLineColor(kBlue)
fnSDown.SetMarkerSize(0)
fnSDown.Draw("c same")
#method=""
#if "ac" in FitOpt.lower():
#       method = "Poisson-esque "
#elif "bound" in FitOpt.lower():
#    method = "Upper and Lower Error Bars "
#legend.AddEntry(fnSUp,method+"Upper bound for fit S in "+samplename,"ple");
#legend.AddEntry(fnSDown,method+"Lower bound for fit S in "+samplename,"ple");
if args.mass == "":
    legend.AddEntry(fnSUp,"Poisson-like uncertainties for fit S with m_{S} = "+args.mass+" GeV/c^{2}","pl");
else:
    legend.AddEntry(fnSUp,"Poisson-like uncertainties for fit S with m_{S} = "+args.mass+" GeV/c^{2}","pl");
CMSStyle.setCMSLumiStyle(c1, 11, lumiTextSize_= 0.74)
#legend.SetTextSize(0.041)
legend.SetTextFont(42)
legend.SetFillStyle(0)
legend.SetBorderSize(0)
legend.Draw("same")
c1.cd()
c1.SetName(output_pdf_name)
c1.Write()
c1.SaveAs(output_pdf_name, ".pdf")
gPad.SetLogy()
c1.Write()
c1.SaveAs(output_logplot_pdf_name, ".pdf")

fOut.Close()
