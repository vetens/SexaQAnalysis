# script to ready MC Sample for creation of the PU Reweighting map
# Takes as input MC Tracking NTuples
# TODO: do for data (see AnalyzerAllSteps/test/MeasurePVDistributions/MeasurePVDistributions.py for potential reference)

from ROOT import *
import random
import math
import sys
import array
import argparse
#sys.path.append('/user/jdeclerc/CMSSW_8_0_30_bis/src/SexaQAnalysis/AnalyzerAllSteps/macros/tdrStyle')
sys.path.append('/afs/cern.ch/work/w/wvetens/Sexaquarks/CMSSW_10_2_26/src/SexaQAnalysis/AnalyzerAllSteps/macros/tdrStyle')
import  CMSStyle
import collections
parser = argparse.ArgumentParser()
parser.add_argument('--mass', dest='mass', action='store', default='1p7')
args = parser.parse_args()

gROOT.SetBatch(kTRUE)
gStyle.SetLegendTextSize(0.08)
gStyle.SetOptFit(1111)
gStyle.SetOptStat(1)

CMSStyle.extraText = "(CMS Simulation) "
CMSStyle.cmsText = " Private Work"
CMSStyle.cmsTextFont = 42
CMSStyle.extraTextFont = 42
CMSStyle.lumiTextSize = 0.74
CMSStyle.cmsTextSize = 0.74
CMSStyle.relPosX = 2.36*0.045
CMSStyle.outOfFrame = False 

CMSStyle.setTDRStyle()

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
maxEvents1 = 1e4
maxEvents2 = 1e99


plots_output_dir = "../GENSIM/"
ReweighMap = "MultiToSingleSbar_"+args.mass+"GeV_EtaReweigh"

fSingleIn = TFile(plots_output_dir+'MacroOut_SingleSbar_'+args.mass+'.root','read')
SingleSbar_EtaReco = fSingleIn.Get('all_antiS/teff_h_nom_eta_antiS_reconstructable')
SingleSbar_EtaReco.SetMarkerColor(kBlack)
SingleSbar_EtaReco.SetLineColor(kBlack)
fMultiIn = TFile(plots_output_dir+'MacroOut_MultiSbar_'+args.mass+'.root','read')
MultiSbar_EtaReco = fMultiIn.Get('all_antiS/teff_h_nom_eta_antiS_reconstructable')
SingleSbar_EtaReco.SetMarkerColor(kRed)
SingleSbar_EtaReco.SetLineColor(kRed)
SingleReco_Integral = SingleSbar_EtaReco.CreateGraph().Integral()

print SingleReco_Integral
fOut = TFile("FitResult_"+args.mass+".root", "RECREATE")
fOut.cd()
#fit eta reconstructability for the single sbar to a sum of 3 gaussians with left and right gaussians having equal standard deviations and opposite means, the middle gaussian fixed at mean of zero. 
#arguments as follows: TMath::Gaus(x, mean, SD, Norm)
#SingleSbar_fit = TF1("SingleSbar_EtaRecobility_fit", " [2] * TMath::Gaus(x, [0], [1]) + [3] * TMath::Gaus(x, -[0], [1]) + [5] * TMath::Gaus(x, 0, [4])", -5, 5)
SingleSbar_fit = TF1("SingleSbar_EtaRecobility_fit", " [4] * ROOT::Math::crystalball_function(x, [0], [1], [2], [3]) + [5] * ROOT::Math::crystalball_function(-x, [0], [1], [2], [3]) - [6]", -5, 5)
## Mean of the left and right gaussians
#SingleSbar_fit.SetParameter(0,3)
#SingleSbar_fit.SetParLimits(0,0, 5)
## Standard Deviation of the left and right gaussians
#SingleSbar_fit.SetParameter(1,1)
#SingleSbar_fit.SetParLimits(1,0.000001, 5)
## Norms of the left and right gaussians
#SingleSbar_fit.SetParameter(2,2 * SingleReco_Integral / 10)
#SingleSbar_fit.SetParLimits(2,0, SingleReco_Integral)
#SingleSbar_fit.SetParameter(3,2 * SingleReco_Integral / 10)
#SingleSbar_fit.SetParLimits(3,0, SingleReco_Integral)
### Standard Deviation of the central gaussian
##SingleSbar_fit.SetParameter(4,1)
##SingleSbar_fit.SetParLimits(4,0.000001, 5)
### Norm of the central gaussian
##SingleSbar_fit.SetParameter(5,SingleReco_Integral / 10)
##SingleSbar_fit.SetParLimits(5,0, SingleReco_Integral)
#CBF Fit
# alpha (crystal ball cutoff) of the left and right gaussians
SingleSbar_fit.SetParameter(0,1)
SingleSbar_fit.SetParLimits(0,0, 10)
# n (power law for cbf) of the left and right gaussians
SingleSbar_fit.SetParameter(1,1)
SingleSbar_fit.SetParLimits(1,0.0001, 10)
#sigma of left and right gaussians
SingleSbar_fit.SetParameter(2, 1)
SingleSbar_fit.SetParLimits(2,0, 5)
# Mean of the left and right gaussians
SingleSbar_fit.SetParameter(3, 2)
SingleSbar_fit.SetParLimits(3,0, 5)
# Norms of the left and right gaussians
SingleSbar_fit.SetParameter(4,2 * SingleReco_Integral / 10)
SingleSbar_fit.SetParLimits(4,0, SingleReco_Integral)
SingleSbar_fit.SetParameter(5,2 * SingleReco_Integral / 10)
SingleSbar_fit.SetParLimits(5,0, SingleReco_Integral)
#constant offset
SingleSbar_fit.SetParameter(6, 0.08)
SingleSbar_fit.SetParLimits(6, -1, 1)

SingleSbar_fit.SetLineColor(4)

FitResult = SingleSbar_EtaReco.CreateGraph().Fit("SingleSbar_EtaRecobility_fit", "SRE")

FitResult.Print()

#with open("FitResult.txt", "w") as fFitResult:
#    FitResult.Print()
#    fFitResult.write("Chi2: " + FitResult.Chi2()+'\n')
#    fFitResult.write("NDOF: " + FitResult.Ndf()+'\n')
    
#Now to get the reweighting parameter

nPoints = 100
h_reweighingFactor_eta = TH1F('h_reweighingFactor_eta', ';#eta_{#bar{S}};Reweighting Parameter', nPoints, -5, 5)
h_reweighingFactor_eta.SetMarkerColor(kBlue)
h_reweighingFactor_eta.SetLineColor(kBlue)
h_reweighingFactor_eta_NoFit = TH1F('h_reweighingFactor_eta_NoFit', ';#eta_{#bar{S}};Reweighting Parameter', nPoints, -5, 5)
h_reweighingFactor_eta_NoFit.SetMarkerColor(kBlack)
h_reweighingFactor_eta_NoFit.SetLineColor(kBlack)

f1 = open(ReweighMap + ".txt", "w")
f2 = open(ReweighMap + "_NoFit.txt", "w")

f1.write('# eta         Weight        Error\n')
f2.write('# eta         Weight        Error\n')
for i in range(1, nPoints+1):
    iEta = -5.0 + 10.0 * (i-1.0) /nPoints
    Multi_Recobility_Eta = MultiSbar_EtaReco.CreateGraph().GetY()[i-1]
    Multi_Recobility_Eta_error = MultiSbar_EtaReco.CreateGraph().GetErrorY(i)
    Single_Recobility_Eta = SingleSbar_fit.Eval(iEta)
    Single_Recobility_Eta_error_squares = 0
    for j in range(0,6):
        #Silliness because root needs iEta to be a pointer and not just a double
        iEtaArray = array.array('d', [iEta])
        Single_Recobility_Eta_error_squares += (SingleSbar_fit.GradientPar(j,iEtaArray) * SingleSbar_fit.GetParError(j))**2 
    Single_Recobility_Eta_error = math.sqrt(Single_Recobility_Eta_error_squares)
    Single_Recobility_Eta_NoFit = SingleSbar_EtaReco.CreateGraph().GetY()[i-1]
    Single_Recobility_Eta_NoFit_error = SingleSbar_EtaReco.CreateGraph().GetErrorY(i)
    MultiToSingle = 0
    MultiToSingle_err = 0
    MultiToSingle_NoFit = 0
    MultiToSingle_NoFit_err = 0
    if ( Single_Recobility_Eta > 0 and Multi_Recobility_Eta > 0 ):
        MultiToSingle = Single_Recobility_Eta / Multi_Recobility_Eta
        MultiToSingle_err = math.sqrt((Single_Recobility_Eta / Multi_Recobility_Eta**2 * Multi_Recobility_Eta_error)**2 + (Single_Recobility_Eta_error / Multi_Recobility_Eta)**2)
    h_reweighingFactor_eta.SetBinContent(i, MultiToSingle)
    #h_reweighingFactor_eta.SetBinError(i, MultiToSingle_err)
    h_reweighingFactor_eta.SetBinError(i, 0)
    f1.write(str(iEta) + '      ' + str(MultiToSingle) + '     ' + str(MultiToSingle_err) + "\n")
    if ( Single_Recobility_Eta_NoFit > 0 and Multi_Recobility_Eta > 0 ):
        MultiToSingle_NoFit = Single_Recobility_Eta_NoFit / Multi_Recobility_Eta
        MultiToSingle_NoFit_err = math.sqrt((Single_Recobility_Eta_NoFit / Multi_Recobility_Eta**2 * Multi_Recobility_Eta_error)**2 + (Single_Recobility_Eta_NoFit_error / Multi_Recobility_Eta)**2)
    h_reweighingFactor_eta_NoFit.SetBinContent(i, MultiToSingle_NoFit)
    h_reweighingFactor_eta_NoFit.SetBinError(i, MultiToSingle_NoFit_err)
    f2.write(str(iEta) + '      ' + str(MultiToSingle_NoFit) + '     ' + str(MultiToSingle_NoFit_err) + "\n")
f1.close()
f2.close()

c1 = ReadyCanvas("c_fit_"+args.mass)
legend_fit = TLegend(0.5,0.7,0.95,0.95)
legend_fit.SetTextSize(0.02)
legend_fit.SetFillStyle(0)
legend_fit.SetBorderSize(0)
legend_fit.SetHeader("m_{#bar{S}}="+args.mass+"GeV/c^{2}", "C")
highval = 0.15 #MultiSbar_EtaReco.CreateGraph().GetMaximum()*1.2
SingleGraph = SingleSbar_EtaReco.CreateGraph()
MultiGraph = MultiSbar_EtaReco.CreateGraph()
SingleGraph.GetYaxis().SetRangeUser(0,highval)
MultiGraph.GetYaxis().SetRangeUser(0,highval)
SingleGraph.Draw("")
gPad.SetLogy(0)
legend_fit.AddEntry(SingleSbar_EtaReco, "Single-#bar{S} Reconstructability", "ep")
SingleSbar_fit.Draw("same")
legend_fit.AddEntry(SingleSbar_fit, "Fit to Single-#bar{S} Reconstructability", "l")
MultiSbar_EtaReco.Draw("same")
legend_fit.AddEntry(MultiSbar_EtaReco, "Multi-#bar{S} Reconstructability", "ep")
legend_fit.Draw("same")
CMSStyle.setCMSLumiStyle(c1,11, lumiTextSize_=0.74)
c1.Write()
c1.SaveAs(c1.GetName()+".pdf")

c2 = ReadyCanvas("c_reweigh_"+args.mass)
legend_reweigh = TLegend(0.5,0.7,0.95,0.95)
legend_reweigh.SetTextSize(0.02)
legend_reweigh.SetFillStyle(0)
legend_reweigh.SetBorderSize(0)
legend_reweigh.SetHeader("m_{#bar{S}}="+args.mass+"GeV/c^{2}", "C")
h_reweighingFactor_eta.Draw("")
gPad.SetLogy(1)
legend_reweigh.AddEntry(h_reweighingFactor_eta, "reweighting factor with Fit", "p")
h_reweighingFactor_eta_NoFit.Draw("same")
legend_reweigh.AddEntry(h_reweighingFactor_eta_NoFit, "reweighting factor without Fit", "p")
legend_reweigh.Draw("same")
CMSStyle.setCMSLumiStyle(c2,11, lumiTextSize_=0.74)
c2.Write()
c2.SaveAs(c2.GetName()+".pdf")

c3 = ReadyCanvas("c_Diffplot_"+args.mass)
trp = TRatioPlot(h_reweighingFactor_eta, h_reweighingFactor_eta_NoFit, "diff")
CMSStyle.setCMSLumiStyle(c3,11, lumiTextSize_=0.74)
c3.Write()
c3.SaveAs(c3.GetName()+".pdf")

fOut.Close()

print "Done"
