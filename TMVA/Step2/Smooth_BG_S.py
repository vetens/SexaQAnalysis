import ROOT
from ROOT import *
import numpy as np
import ctypes
import math
import sys
import argparse

sys.path.append('/afs/cern.ch/work/w/wvetens/Sexaquarks/CMSSW_10_2_26/src/SexaQAnalysis/AnalyzerAllSteps/macros/tdrStyle')
import  CMSStyle

import sys
sys.path.insert(1, '../../.')

gROOT.SetBatch(kTRUE)
gStyle.SetLegendTextSize(0.08)

CMSStyle.lumiText = "Parked 2018 data, "+"237 #times 10^{9}"+" Collisions (13 TeV)"
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

def errorprop(fn, covmatrix, nparams, point, debug=False):
    covsum = 0
    varsum = 0
    di = 0
    si = 0
    dj = 0
    sj = 0
    for i in xrange(0, nparams):
        di = fn.GradientPar(i, ctypes.c_double(point))
        si = fn.GetParError(i)
        for j in xrange(0, i):
            dj = fn.GradientPar(j, ctypes.c_double(point))
            sj = fn.GetParError(j)
            covsum += 2*TMatrixDRow(covmatrix, i)[j]*di*dj*si*sj
            if debug:
                print "For row: ", i, "and column: ", j
                print "\tCovmatrix: ", TMatrixDRow(covmatrix, i)[j]
                print "\t row gradient: ", di, " col gradient: ", dj
        varsum += di**2 * si**2
    if debug:
        print "Sum of Covariant Terms: ", covsum
        print "Sum of Variant Terms: ", varsum
    return [math.sqrt(covsum+varsum), covsum]

print "-----------------------------------------------------------------------------------------------------------"
print "----------------------EXPONENTIAL DECAY--------------------------------------------------------------------"
#Exponential
fnS = TF1("fnS", "expo",BDT_cut_min,BDT_cut_max)
fitresult = hS.Fit(fnS,"S","",BDT_cut_min,BDT_cut_max)
ExpConst = fnS.GetParameter("Constant")
ExpConstErr = fnS.GetParError(0)
DecayConst = fnS.GetParameter("Slope")
DecayConstErr = fnS.GetParError(1)
covmatrix = fitresult.GetCovarianceMatrix()
print covmatrix

hS.SetStats(0)
confIntervals_data = TH1D("confIntervals_data", "Exponential Fit with .68 conf. band", int((BDT_cut_max-BDT_cut_min)/BDT_cut_step),BDT_cut_min,BDT_cut_max)
TVirtualFitter.GetFitter().GetConfidenceIntervals(confIntervals_data, 0.68)
#Get confidence interval at a certain point:
#uncertainty = math.sqrt(fnS.GradientPar(0, ctypes.c_double(0.365))**2 * ExpConstErr**2 + fnS.GradientPar(1, ctypes.c_double(0.365))**2 * DecayConstErr**2)/fnS.Eval(0.365)
uncertainty = errorprop(fnS, covmatrix, 2, 0.365)[0]/fnS.Eval(0.365)
print "Chi Square / NDF:", fitresult.Chi2(), "/", fitresult.Ndf(), ": ", fitresult.Chi2()/fitresult.Ndf()
print "Uncertainty at 0.365:", fnS.Eval(0.365), "+/-", uncertainty * fnS.Eval(0.365)
print "\t % err:", uncertainty * 100
print "\t covariance term:", errorprop(fnS, covmatrix, 2, 0.365)[1]
gStyle.SetOptStat(0)
fnS.SetLineColor(kRed)
fnS.SetMarkerSize(0)
confIntervals_data.SetStats(False)
confIntervals_data.SetMarkerSize(0)
confIntervals_data.SetFillColorAlpha(kRed-7, 0.5)
fnS.GetHistogram().SetStats(0)
fnS.Draw("c same")
confIntervals_data.Draw("ce3 same")
legend.AddEntry(fnS,"fit S in "+samplename+" with .68 conf. band","pl");
CMSStyle.setCMSLumiStyle(c1, 11, lumiTextSize_= 0.74)
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
print "-----------------------------------------------------------------------------------------------------------"
print "----------------------GAUSSIAN-----------------------------------------------------------------------------"
#Gaussian
output_pdf_name_g = "Smoothed_BG/h_BDT_gaus_"+samplename+"_PoissonLikeError.pdf"
output_logplot_pdf_name_g = "Smoothed_BG/h_BDT_gaus_"+samplename+"_PoissonLikeError_logscale.pdf"

c2 = TCanvas("h_BDT_gaus_"+samplename, "", 700, 900)
c2.SetFillColor(0)
c2.SetRightMargin(0.05)
c2.SetBorderMode(0)
c2.SetFrameFillStyle(0)
c2.SetFrameBorderMode(0)
c2.SetTickx(0)
c2.SetTicky(0)
c2.cd()

gframe = c2.DrawFrame(BDT_cut_min,0.1, BDT_cut_max, 101)
gframe.GetYaxis().CenterTitle()
gframe.GetYaxis().SetTitleSize(0.05)
gframe.GetXaxis().SetTitleSize(0.05)
gframe.GetXaxis().SetLabelSize(0.04)
gframe.GetYaxis().SetLabelSize(0.04)
gframe.GetXaxis().SetNdivisions(121)
gframe.GetYaxis().CenterTitle(True)
gframe.GetYaxis().SetTitle('N_{ev}/'+str(BDT_cut_step)+" BDT class.")
gframe.GetXaxis().SetTitle("BDT classifier")
gframe.SetMinimum(0)
gframe.SetMaximum(hS.GetMaximum()*1.1)
c2.Draw()
glegend = TLegend(0.5, 0.6, 0.95, 0.95)

gStyle.SetOptStat(0)
hS.SetMarkerStyle(23)
hS.Draw("peXOC")

glegend.AddEntry(hS,samplename+" S","ple");
fnSg = TF1("fnSg", "gaus",BDT_cut_min,BDT_cut_max)
fnSg.SetParLimits(0, 0, 1e7)
fnSg.SetParameter(0, 1e5)
#fnSg.SetParLimits(1, -2, 0.5)
#fnSg.SetParameter(1, -2)
fnSg.SetParLimits(1, -0.5, 0.5)
fnSg.SetParameter(1, -0.5)
fnSg.SetParLimits(2, 0, 8)
fnSg.SetParameter(2, 1)
fitresultG = hS.Fit(fnSg,"S","",BDT_cut_min,BDT_cut_max)
Normg = fnSg.GetParameter(0)
NormErrg = fnSg.GetParError(0)
Meang = fnSg.GetParameter(1)
MeanErrg = fnSg.GetParError(1)
Sigmag = fnSg.GetParameter(2)
SigmaErrg = fnSg.GetParError(2)

hS.SetStats(0)
confIntervals_datag = TH1D("confIntervals_datag", "Gaussian Fit with .68 conf. band", int((BDT_cut_max-BDT_cut_min)/BDT_cut_step),BDT_cut_min,BDT_cut_max)
TVirtualFitter.GetFitter().GetConfidenceIntervals(confIntervals_datag, 0.68)
#Get confidence interval at a certain point:
uncertaintyg = math.sqrt(fnSg.GradientPar(0, ctypes.c_double(0.365))**2 * NormErrg**2 + fnSg.GradientPar(1, ctypes.c_double(0.365))**2 * MeanErrg**2 + fnSg.GradientPar(1, ctypes.c_double(0.365))**2 * SigmaErrg**2)/fnSg.Eval(0.365)
print "Chi Square / NDF:", fitresultG.Chi2(), "/", fitresultG.Ndf(), ": ", fitresultG.Chi2()/fitresultG.Ndf()
print "Uncertainty at 0.365:", fnSg.Eval(0.365), "+/-", uncertaintyg * fnSg.Eval(0.365)
print "\t % err:", uncertaintyg * 100
gStyle.SetOptStat(0)
fnSg.SetLineColor(kRed)
fnSg.SetMarkerSize(0)
confIntervals_datag.SetStats(False)
confIntervals_datag.SetMarkerSize(0)
confIntervals_datag.SetFillColorAlpha(kRed-7, 0.5)
fnSg.GetHistogram().SetStats(0)
fnSg.Draw("c same")
confIntervals_datag.Draw("ce3 same")
glegend.AddEntry(fnSg,"fit S in "+samplename+" with .68 conf. band","pl");
CMSStyle.setCMSLumiStyle(c2, 11, lumiTextSize_= 0.74)
glegend.SetTextFont(42)
glegend.SetFillStyle(0)
glegend.SetBorderSize(0)
glegend.Draw("same")
c2.cd()
c2.SetName(output_pdf_name_g)
c2.Write()
c2.SaveAs(output_pdf_name_g, ".pdf")
gPad.SetLogy()
c2.Write()
c2.SaveAs(output_logplot_pdf_name_g, ".pdf")

print "-----------------------------------------------------------------------------------------------------------"
print "----------------------POWER LAW----------------------------------------------------------------------------"
#powerlaw*exp
output_pdf_name_p = "Smoothed_BG/h_BDT_pexp_"+samplename+"_PoissonLikeError.pdf"
output_logplot_pdf_name_p = "Smoothed_BG/h_BDT_pexp_"+samplename+"_PoissonLikeError_logscale.pdf"

c3 = TCanvas("h_BDT_pexp_"+samplename, "", 700, 900)
c3.SetFillColor(0)
c3.SetRightMargin(0.05)
c3.SetBorderMode(0)
c3.SetFrameFillStyle(0)
c3.SetFrameBorderMode(0)
c3.SetTickx(0)
c3.SetTicky(0)
c3.cd()

pframe = c3.DrawFrame(BDT_cut_min,0.1, BDT_cut_max, 101)
pframe.GetYaxis().CenterTitle()
pframe.GetYaxis().SetTitleSize(0.05)
pframe.GetXaxis().SetTitleSize(0.05)
pframe.GetXaxis().SetLabelSize(0.04)
pframe.GetYaxis().SetLabelSize(0.04)
pframe.GetXaxis().SetNdivisions(121)
pframe.GetYaxis().CenterTitle(True)
pframe.GetYaxis().SetTitle('N_{ev}/'+str(BDT_cut_step)+" BDT class.")
pframe.GetXaxis().SetTitle("BDT classifier")
pframe.SetMinimum(0)
pframe.SetMaximum(hS.GetMaximum()*1.1)
c3.Draw()
plegend = TLegend(0.5, 0.6, 0.95, 0.95)

gStyle.SetOptStat(0)
hS.SetMarkerStyle(23)
hS.Draw("peXOC")

plegend.AddEntry(hS,samplename+" S","ple");
fnSp = TF1("fnSp", "x^[0]*expo(1)",BDT_cut_min,BDT_cut_max)
fitresultP = hS.Fit(fnSp,"S","",BDT_cut_min,BDT_cut_max)
PowerLawp = fnSp.GetParameter(1)
PowerLawErrp = fnSp.GetParError(1)
ExpConstp = fnSp.GetParameter(1)
ExpConstErrp = fnSp.GetParError(1)
DecayConstp = fnSp.GetParameter(2)
DecayConstErrp = fnSp.GetParError(2)
covmatrixp = fitresultP.GetCovarianceMatrix()
uncertaintyp = errorprop(fnSp, covmatrixp, 3, 0.365)[0]/fnSp.Eval(0.365)

hS.SetStats(0)
confIntervals_datap = TH1D("confIntervals_datap", "Gaussian Fit with .68 conf. band", int((BDT_cut_max-BDT_cut_min)/BDT_cut_step),BDT_cut_min,BDT_cut_max)
TVirtualFitter.GetFitter().GetConfidenceIntervals(confIntervals_datap, 0.68)
#Get confidence interval at a certain point:
#uncertaintyp = math.sqrt(fnSp.GradientPar(0, ctypes.c_double(0.365))**2 * PowerLawErrp**2 + fnSp.GradientPar(1, ctypes.c_double(0.365))**2 * ExpConstErrp**2 + fnSp.GradientPar(2, ctypes.c_double(0.365))**2 * DecayConstErrp**2)/fnSp.Eval(0.365)
#uncertaintyp = math.sqrt(fnSp.GradientPar(0, ctypes.c_double(0.365))**2 * PowerLawErrp**2 + fnSp.GradientPar(1, ctypes.c_double(0.365))**2 * ExpConstErrp**2 + fnSp.GradientPar(2, ctypes.c_double(0.365))**2 * DecayConstErrp**2)/fnSp.Eval(0.365)
print "Chi Square / NDF:", fitresultP.Chi2(), "/", fitresultP.Ndf(), ": ", fitresultP.Chi2()/fitresultP.Ndf()
print "Uncertainty at 0.365:", fnSp.Eval(0.365), "+/-", uncertaintyp * fnSp.Eval(0.365)
print "\t % err:", uncertaintyp * 100
gStyle.SetOptStat(0)
fnSp.SetLineColor(kRed)
fnSp.SetMarkerSize(0)
confIntervals_datap.SetStats(False)
confIntervals_datap.SetMarkerSize(0)
confIntervals_datap.SetFillColorAlpha(kRed-7, 0.5)
fnSp.GetHistogram().SetStats(0)
fnSp.Draw("c same")
confIntervals_datap.Draw("ce3 same")
plegend.AddEntry(fnSp,"fit S in "+samplename+" with .68 conf. band","pl");
CMSStyle.setCMSLumiStyle(c3, 11, lumiTextSize_= 0.74)
plegend.SetTextFont(42)
plegend.SetFillStyle(0)
plegend.SetBorderSize(0)
plegend.Draw("same")
c3.cd()
c3.SetName(output_pdf_name_p)
c3.Write()
c3.SaveAs(output_pdf_name_p, ".pdf")
gPad.SetLogy()
c3.Write()
c3.SaveAs(output_logplot_pdf_name_p, ".pdf")

print "-----------------------------------------------------------------------------------------------------------"
print "----------------------FIRST ORDER POLYNOMIAL TIMES EXPONENTIAL DECAY---------------------------------------"
#p1*exp
output_pdf_name_p1 = "Smoothed_BG/h_BDT_p1exp_"+samplename+"_PoissonLikeError.pdf"
output_logplot_pdf_name_p1 = "Smoothed_BG/h_BDT_p1exp_"+samplename+"_PoissonLikeError_logscale.pdf"

c4 = TCanvas("h_BDT_p1exp_"+samplename, "", 700, 900)
c4.SetFillColor(0)
c4.SetRightMargin(0.05)
c4.SetBorderMode(0)
c4.SetFrameFillStyle(0)
c4.SetFrameBorderMode(0)
c4.SetTickx(0)
c4.SetTicky(0)
c4.cd()

p1frame = c4.DrawFrame(BDT_cut_min,0.1, BDT_cut_max, 101)
p1frame.GetYaxis().CenterTitle()
p1frame.GetYaxis().SetTitleSize(0.05)
p1frame.GetXaxis().SetTitleSize(0.05)
p1frame.GetXaxis().SetLabelSize(0.04)
p1frame.GetYaxis().SetLabelSize(0.04)
p1frame.GetXaxis().SetNdivisions(121)
p1frame.GetYaxis().CenterTitle(True)
p1frame.GetYaxis().SetTitle('N_{ev}/'+str(BDT_cut_step)+" BDT class.")
p1frame.GetXaxis().SetTitle("BDT classifier")
p1frame.SetMinimum(0)
p1frame.SetMaximum(hS.GetMaximum()*1.1)
c4.Draw()
p1legend = TLegend(0.5, 0.6, 0.95, 0.95)

gStyle.SetOptStat(0)
hS.SetMarkerStyle(23)
hS.Draw("peXOC")

p1legend.AddEntry(hS,samplename+" S","ple");
fnSp1 = TF1("fnSp1", "([0]*x+1)*expo(1)",BDT_cut_min,BDT_cut_max)
fitresultP1 = hS.Fit(fnSp1,"S","",BDT_cut_min,BDT_cut_max)
#Slopep1 = fnSp1.GetParameter(0)
#SlopeErrp1 = fnSp1.GetParError(0)
#Intp1 = fnSp1.GetParameter(1)
#IntErrp1 = fnSp1.GetParError(1)
#ExpConstp1 = fnSp1.GetParameter(2)
#ExpConstErrp1 = fnSp1.GetParError(2)
#DecayConstp1 = fnSp1.GetParameter(3)
#DecayConstErrp1 = fnSp1.GetParError(3)
covmatrixp1 = fitresultP1.GetCovarianceMatrix()
uncertaintyp1 = errorprop(fnSp1, covmatrixp1, 2, 0.365)[0]/fnSp1.Eval(0.365)

hS.SetStats(0)
confIntervals_datap1 = TH1D("confIntervals_datap1", "Gaussian Fit with .68 conf. band", int((BDT_cut_max-BDT_cut_min)/BDT_cut_step),BDT_cut_min,BDT_cut_max)
TVirtualFitter.GetFitter().GetConfidenceIntervals(confIntervals_datap1, 0.68)
#Get confidence interval at a certain point:
#uncertaintyp1 = math.sqrt(fnSp1.GradientPar(0, ctypes.c_double(0.365))**2 * SlopeErrp1**2 + fnSp1.GradientPar(1, ctypes.c_double(0.365))**2 * IntErrp1**2 + fnSp1.GradientPar(2, ctypes.c_double(0.365))**2 * ExpConstErrp1**2+ fnSp1.GradientPar(3, ctypes.c_double(0.365))**2 * DecayConstErrp1**2)/fnSp1.Eval(0.365)
print "Chi Square / NDF:", fitresultP1.Chi2(), "/", fitresultP1.Ndf(), ": ", fitresultP1.Chi2()/fitresultP1.Ndf()
print "Uncertainty at 0.365:", fnSp1.Eval(0.365), "+/-", uncertaintyp1 * fnSp1.Eval(0.365)
print "\t % err:", uncertaintyp1 * 100
gStyle.SetOptStat(0)
fnSp1.SetLineColor(kRed)
fnSp1.SetMarkerSize(0)
confIntervals_datap1.SetStats(False)
confIntervals_datap1.SetMarkerSize(0)
confIntervals_datap1.SetFillColorAlpha(kRed-7, 0.5)
fnSp1.GetHistogram().SetStats(0)
fnSp1.Draw("c same")
confIntervals_datap1.Draw("ce3 same")
p1legend.AddEntry(fnSp1,"fit S in "+samplename+" with .68 conf. band","pl");
CMSStyle.setCMSLumiStyle(c4, 11, lumiTextSize_= 0.74)
p1legend.SetTextFont(42)
p1legend.SetFillStyle(0)
p1legend.SetBorderSize(0)
p1legend.Draw("same")
c4.cd()
c4.SetName(output_pdf_name_p1)
c4.Write()
c4.SaveAs(output_pdf_name_p1, ".pdf")
gPad.SetLogy()
c4.Write()
c4.SaveAs(output_logplot_pdf_name_p1, ".pdf")

print "-----------------------------------------------------------------------------------------------------------"
print "----------------------SECOND ORDER POLYNOMIAL TIMES EXPONENTIAL DECAY--------------------------------------"
#p2*exp
output_pdf_name_p2 = "Smoothed_BG/h_BDT_p2exp_"+samplename+"_PoissonLikeError.pdf"
output_logplot_pdf_name_p2 = "Smoothed_BG/h_BDT_p2exp_"+samplename+"_PoissonLikeError_logscale.pdf"

c5 = TCanvas("h_BDT_p1exp_"+samplename, "", 700, 900)
c5.SetFillColor(0)
c5.SetRightMargin(0.05)
c5.SetBorderMode(0)
c5.SetFrameFillStyle(0)
c5.SetFrameBorderMode(0)
c5.SetTickx(0)
c5.SetTicky(0)
c5.cd()

p2frame = c5.DrawFrame(BDT_cut_min,0.1, BDT_cut_max, 101)
p2frame.GetYaxis().CenterTitle()
p2frame.GetYaxis().SetTitleSize(0.05)
p2frame.GetXaxis().SetTitleSize(0.05)
p2frame.GetXaxis().SetLabelSize(0.04)
p2frame.GetYaxis().SetLabelSize(0.04)
p2frame.GetXaxis().SetNdivisions(121)
p2frame.GetYaxis().CenterTitle(True)
p2frame.GetYaxis().SetTitle('N_{ev}/'+str(BDT_cut_step)+" BDT class.")
p2frame.GetXaxis().SetTitle("BDT classifier")
p2frame.SetMinimum(0)
p2frame.SetMaximum(hS.GetMaximum()*1.1)
c5.Draw()
p2legend = TLegend(0.5, 0.6, 0.95, 0.95)

gStyle.SetOptStat(0)
hS.SetMarkerStyle(23)
hS.Draw("peXOC")

p2legend.AddEntry(hS,samplename+" S","ple");
fnSp2 = TF1("fnSp2", "([0]*x+1+[3]*x^2)*expo(1)",BDT_cut_min,BDT_cut_max)
fitresultP2 = hS.Fit(fnSp2,"S","",BDT_cut_min,BDT_cut_max)
#Slopep2 = fnSp2.GetParameter(0)
#SlopeErrp2 = fnSp2.GetParError(0)
#Intp2 = fnSp2.GetParameter(1)
#IntErrp2 = fnSp2.GetParError(1)
#ExpConstp2 = fnSp2.GetParameter(2)
#ExpConstErrp2 = fnSp2.GetParError(2)
#DecayConstp2 = fnSp2.GetParameter(3)
#DecayConstErrp2 = fnSp2.GetParError(3)
#Squarep2 = fnSp2.GetParameter(4)
#SquareErrp2 = fnSp2.GetParError(4)
covmatrixp2 = fitresultP2.GetCovarianceMatrix()
uncertaintyp2 = errorprop(fnSp2, covmatrixp2, 4, 0.365)[0]/fnSp2.Eval(0.365)

hS.SetStats(0)
confIntervals_datap2 = TH1D("confIntervals_datap2", "Gaussian Fit with .68 conf. band", int((BDT_cut_max-BDT_cut_min)/BDT_cut_step),BDT_cut_min,BDT_cut_max)
TVirtualFitter.GetFitter().GetConfidenceIntervals(confIntervals_datap2, 0.68)
#Get confidence interval at a certain point:
#uncertaintyp2 = math.sqrt(fnSp2.GradientPar(0, ctypes.c_double(0.365))**2 * SlopeErrp2**2 + fnSp2.GradientPar(1, ctypes.c_double(0.365))**2 * IntErrp2**2 + fnSp2.GradientPar(2, ctypes.c_double(0.365))**2 * ExpConstErrp2**2+ fnSp2.GradientPar(3, ctypes.c_double(0.365))**2 * DecayConstErrp2**2+ fnSp2.GradientPar(4, ctypes.c_double(0.365))**2 * SquareErrp2**2)/fnSp2.Eval(0.365)
print "Chi Square / NDF:", fitresultP2.Chi2(), "/", fitresultP2.Ndf(), ": ", fitresultP2.Chi2()/fitresultP2.Ndf()
print "Uncertainty at 0.365:", fnSp2.Eval(0.365), "+/-", uncertaintyp2 * fnSp2.Eval(0.365)
print "\t % err:", uncertaintyp2 * 100
gStyle.SetOptStat(0)
fnSp2.SetLineColor(kRed)
fnSp2.SetMarkerSize(0)
confIntervals_datap2.SetStats(False)
confIntervals_datap2.SetMarkerSize(0)
confIntervals_datap2.SetFillColorAlpha(kRed-7, 0.5)
fnSp2.GetHistogram().SetStats(0)
fnSp2.Draw("c same")
confIntervals_datap2.Draw("ce3 same")
p1legend.AddEntry(fnSp2,"fit S in "+samplename+" with .68 conf. band","pl");
CMSStyle.setCMSLumiStyle(c5, 11, lumiTextSize_= 0.74)
p2legend.SetTextFont(42)
p2legend.SetFillStyle(0)
p2legend.SetBorderSize(0)
p2legend.Draw("same")
c5.cd()
c5.SetName(output_pdf_name_p2)
c5.Write()
c5.SaveAs(output_pdf_name_p2, ".pdf")
gPad.SetLogy()
c5.Write()
c5.SaveAs(output_logplot_pdf_name_p2, ".pdf")
fOut.Close()
