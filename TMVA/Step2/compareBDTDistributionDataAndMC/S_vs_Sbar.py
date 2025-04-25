import ROOT
#from ctypes import c_longlong
import numpy as np
import sys
import argparse

sys.path.append('/afs/cern.ch/work/w/wvetens/Sexaquarks/CMSSW_10_2_26/src/SexaQAnalysis/AnalyzerAllSteps/macros/tdrStyle')
import CMSStyle

sys.path.insert(1, '../../../.')

#nSMax = 1e3
nSMax = 1e12
#nSMax = 1e6

ROOT.gROOT.SetBatch(ROOT.kTRUE)
ROOT.gStyle.SetLegendTextSize(0.08)

#CMSStyle.extraText = "(CMS Data)"
#CMSStyle.extraText = "(CMS Simulation)"
CMSStyle.lumiText = "2018 data, "+"237 #times 10^{9}"+" Collisions (13 TeV)"
CMSStyle.cmsText = "CMS"
#CMSStyle.cmsTextFont = 42
CMSStyle.cmsTextFont = 61
#CMSStyle.extraTextFont = 42
CMSStyle.lumiTextSize = 0.74
CMSStyle.cmsTextSize = 0.74
CMSStyle.relPosX = 2.36*0.045
#CMSStyle.outOfFrame = False
CMSStyle.outOfFrame = True

CMSStyle.setTDRStyle()
parser = argparse.ArgumentParser()
parser.add_argument('--fitType', dest='fitType', action='store', default=0, type=int)
parser.add_argument('--fitRange', dest='fitRange', action='store', default=0.1, type=float)
parser.add_argument('--mass', dest='mass', action='store', default="", type=str)
parser.add_argument('--compareToData', dest='compareToData', action='store_true', default=False)
parser.add_argument('--unblind', dest='unblind', action='store_true', default=False)
parser.add_argument('--compareExtrapRegion', dest='compareExtrapRegion', action='store_true', default=False)
parser.add_argument('--uncertaintyRegion', dest='uncertaintyRegion', action='store', default=0.3, type=float)
parser.add_argument('--reweighedXevt', dest='reweighedXevt', action='store_true', default=False)
args = parser.parse_args()

FitOpt = "Pol"+str(args.fitType)+"_-"+str(args.fitRange)
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
if args.compareToData:
    S_location_data = "../BDTApplied_bkgReference_dataset_BDT_AllFeatures_dataset_BDT_BPH_Full_TrialB_AllPreSelection_SignalWeighing_PV_MultiToSingle_Eta_OverlapCheckFalse/"
#for remote files:
S_location = "root://cmsxrootd.hep.wisc.edu//store/user/wvetens/data_Sexaq/FlatTree_BDT/DiscrApplied_bkgReference/50PrevEvt_XEVT_reco/bkgReference_"
#Sbar_location = "../BDTApplied_unblindMC_BG_dataset_BDT_AllFeatures_dataset_BDT_BPH_Full_AllPreSelection_SignalWeighing_PV_MultiToSingle_Eta_OverlapCheckFalse/"
#samplename = "QCD_MC_BG"
#Sbar_location = "../BDTApplied_unblindMC_BG_dataset_BDT_AllFeatures_dataset_BDT_BPH_Full_AllPreSelection_SignalWeighing_PV_MultiToSingle_Eta_OverlapCheckFalse/"
if args.mass == "1p7" or args.mass == "1p8" or args.mass == "1p85" or args.mass == "1p9" or args.mass == "2": 
    samplename = args.mass+"GeV_BPH_XEVT_TrialB_50PrevEvt_Full"
    if args.compareToData:
        samplename_data = args.mass+"GeV_Data_BPH_Full_trialB"
        if args.mass == "2":
            samplename_data_u = args.mass+"p0GeV_Data_BPH_Full_trialB"
        else:
            samplename_data_u = samplename_data
else:
    samplename = "BPH_XEVT_TrialB_50PrevEvt_Full"
    # For nPV comparison
    #samplename = "Data_BPH_Full_trialB"
    if args.compareToData:
        samplename_data = "Data_BPH_Full_trialB"
#for remote files:
Sbar_location = "root://cmsxrootd.hep.wisc.edu//store/user/wvetens/data_Sexaq/FlatTree_BDT/DiscrApplied_unblind/50PrevEvt_XEVT_reco/unblind_"
#Sbar_location = "../BDTApplied_unblind_dataset_BDT_AllFeatures_dataset_BDT_BPH_Full_TrialB_AllPreSelection_SignalWeighing_PV_MultiToSingle_Eta_OverlapCheckFalse/"
if args.compareToData:
    Sbar_location_data = "../BDTApplied_partialUnblinding_dataset_BDT_AllFeatures_dataset_BDT_BPH_Full_TrialB_AllPreSelection_SignalWeighing_PV_MultiToSingle_Eta_OverlapCheckFalse/"
if args.unblind:
    Sbar_location_data_u = "../BDTApplied_unblind_dataset_BDT_AllFeatures_dataset_BDT_BPH_Full_TrialB_AllPreSelection_SignalWeighing_PV_MultiToSingle_Eta_OverlapCheckFalse/"
#samplename = "Data_BPH_Full_trialB"
#samplename = "1p7GeV_Data_BPH_Full_trialB"
#Below are the samples for comparing between BDT with and without nPV as a sensitive variable in the BDT (i.e. checking the correlation between charge and nPV)
#Sbar_location = "../BDTApplied_partialUnblinding_dataset_BDT_AllFeatures_dataset_BDT_BPH_Full_TrialB_AllPreSelection_SignalWeighing_MultiToSingle_Eta_NoPV_OverlapCheckFalse/"
#S_location = "../BDTApplied_bkgReference_dataset_BDT_AllFeatures_dataset_BDT_BPH_Full_TrialB_AllPreSelection_SignalWeighing_MultiToSingle_Eta_NoPV_OverlapCheckFalse/"
fXevtPUWeights = '/afs/cern.ch/work/w/wvetens/Sexaquarks/CMSSW_10_2_26/src/SexaQAnalysis/AnalyzerAllSteps/data/PUReweigh_nPV_XevtToDataBPH2018_FULL_POSTCUTS.txt'
weights_PU_Xevt = {line.split()[0] : line.split()[1] for line in open(fXevtPUWeights)}
def ReadyCanvas(name, W=700, H=900):
    c = ROOT.TCanvas(name, "", W, H)
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
    p = ROOT.TPad(n1, n2, xl, r, xh, yt)
    p.SetTickx(0)
    p.SetFillStyle(0)
    p.SetTopMargin(0.07)
    p.SetBottomMargin(0.)
    p.SetRightMargin(0.02)
    p.Draw()
    p.cd()
    return p
def ReadyBotPad(n2, xl, yb, xh, r):
    p = ROOT.TPad(n2, n2, xl, yb, xh, r)
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

def colorIt(hMidA, kColor = ROOT.kCyan):
    hMidA.SetMarkerColor(kColor)
    hMidA.SetLineColor(kColor)
    hMidA.SetMarkerStyle(22)
    hMidA.SetMarkerSize(0.8)
    #hMidA.SetFillColor(kColor)
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
    output_pdf_name = "../Signal_Bkg_Ratios_plots/h_BDT_"+samplename+"_"+FitOpt.replace(".","p")+"_XevtReweighed.pdf"
    output_C_name = "../Signal_Bkg_Ratios_plots/h_BDT_"+samplename+"_"+FitOpt.replace(".","p")+"_XevtReweighed.C"
    output_root_name = "../Signal_Bkg_Ratios_plots/BDT_"+samplename+"_"+FitOpt.replace(".","p")+"_XevtReweighed.root"
else:
    output_pdf_name = "../Signal_Bkg_Ratios_plots/h_BDT_"+samplename+"_"+FitOpt.replace(".","p")+".pdf"
    output_C_name = "../Signal_Bkg_Ratios_plots/h_BDT_"+samplename+"_"+FitOpt.replace(".","p")+".C"
    output_root_name = "../Signal_Bkg_Ratios_plots/BDT_"+samplename+"_"+FitOpt.replace(".","p")+".root"
ROOT.gStyle.SetOptStat(0)
fOut = ROOT.TFile(output_root_name, "RECREATE")
ROOT.gStyle.SetOptStat(0)

fSbar = ROOT.TFile.Open(Sbar_location + "DiscrApplied_" + samplename + ".root")
print "Sbar file:", Sbar_location + "DiscrApplied_" + samplename + ".root"
fS = ROOT.TFile.Open(S_location + "DiscrApplied_" + samplename + ".root")
print "S file: ", S_location + "DiscrApplied_" + samplename + ".root"

tSbar = fSbar.Get("FlatTree")
tS = fS.Get("FlatTree")
print "Files opened!"

nSbar = tSbar.GetEntries()
nS = tS.GetEntries()
print "There are ", nS, "S, and ", nSbar, "Sbar in cross-event"
hSbar = ROOT.TH1F("h_Sbar_BDT",'; BDT classifier; N_{ev}/0.02 BDT class.',60,-0.7,0.5)
hS = ROOT.TH1F("h_S_BDT",'; BDT classifier; N_{ev}/0.02 BDT class.',60,-0.7,0.5)

for i in range(0, nS):
    #if (i%1e4 == 0):
    #    print "reached entry", i
    if i > nSMax:
        break
    tS.GetEntry(i)
    w = 1
    if tS._S_nGoodPVs[0] >= 60 or tS._S_nGoodPVs[0] <= 0:
        w = 0
    elif args.reweighedXevt:
        w = float(weights_PU_Xevt[str(int(tS._S_nGoodPVs[0]))])
    hS.Fill(tS.SexaqBDT, w)
print "S filled with weights"
for i in range(0, nSbar):
    #if (i%1e4 == 0):
    #    print "reached entry", i
    if i > nSMax:
        break
    tSbar.GetEntry(i)
    w = 1
    if tSbar._S_nGoodPVs[0] >= 60 or tSbar._S_nGoodPVs[0] <= 0:
        w = 0
    elif args.reweighedXevt:
        w = float(weights_PU_Xevt[str(int(tSbar._S_nGoodPVs[0]))])
    hSbar.Fill(tSbar.SexaqBDT, w)
print "Sbar filled with weights"
#print "Max number of S allowed in Tree:\t", nSMax
#print "Integrals of Xevt S histo:\t", hS.Integral(), "\tAnd Sbar:\t", hSbar.Integral()

hSbar.Sumw2()
hS.Sumw2()

fOut.cd()
ROOT.gStyle.SetOptStat(0)
Mont = hS.Clone("Mont")
Mont.Divide(hSbar, hS, 1.0, 1.0)
print "Histos Divided"

#c1 = TCanvas("h_BDT_"+samplename, "", 700, 900)
#c1.Draw()
#c1.cd()
colorIt(hS, ROOT.kRed)
if args.unblind:
    c1 = ReadyCanvas("h_BDT_"+samplename, 700, 1200)
else:
    c1 = ReadyCanvas("h_BDT_"+samplename, 700, 900)
xlow = 0.0
xhigh = 1.0
ytop = 1.0
ybot = 0.0
#ratio = 0.3
ratio = 0.475

p1 = ReadyTopPad("p1", "p2", xlow, ratio, xhigh, ytop)
hS.GetYaxis().SetRangeUser(0.2, hS.GetMaximum()*100)
legend = ROOT.TLegend(0.6, 0.7, 0.95, 0.95)
ROOT.gPad.SetLogy()
#gPad.SetGridx()
#gPad.SetGridy()

hS.SetStats(0)
hSbar.SetStats(0)
colorIt(hSbar, ROOT.kBlue)

hS.SetMarkerStyle(23)
hS.Draw("peXOC")
hSbar.Draw("peXOCsame")
CMSStyle.setCMSLumiStyle(c1, 11, lumiTextSize_=0.74)

#legend.AddEntry(hS,"No nPV " +samplename+" S","ple");
if "data" in samplename.lower() and "xevt" not in samplename.lower():
    legend.AddEntry(hS,"Data S","ple");
    legend.AddEntry(hSbar,"Data #bar{S} BDT class. < 0.1  ","ple");
    #legend.AddEntry(hSbar,"No nPV " + samplename + " #bar{S} BDT class. < 0.1  ","ple");
else:
    legend.AddEntry(hS,"Cross-Fifty-Event S","ple");
    legend.AddEntry(hSbar,"Cross-Fifty-Event #bar{S}","ple");

hSbar.SetMarkerSize(0.8)
legend.Draw()

c1.cd()
p2 = ReadyBotPad("p2", xlow, ybot, xhigh, ratio)

ROOT.gPad.SetGridy()
colorIt(Mont,ROOT.kBlack)
Mont.SetMinimum(0.5);
if args.unblind:
    Mont.SetMaximum(2);
else:
    Mont.SetMaximum(1.5);
Mont.GetXaxis().SetTitleOffset(1.2);
Mont.GetYaxis().SetTitleOffset(3.);
Mont.SetYTitle("#bar{S}/S");
Mont.SetStats(0)
if "data" in samplename.lower() and "xevt" not in samplename.lower():
    Mont.Fit("pol"+str(args.fitType),"","",-float(args.fitRange),0.1)
elif "xevt" in samplename.lower():
    if args.compareToData:
        if args.compareExtrapRegion:
            fMont = ROOT.TF1("fMont", "pol"+str(args.fitType), -float(args.fitRange), 0.1)
            Mont.Fit(fMont,"","",-float(args.fitRange),0.1)
            fMont.SetLineColor(ROOT.kBlack)
            confIntervals = ROOT.TH1D("confIntervals", "Cross-Fifty-Event Linear Fit with .95 conf. band", 10, -float(args.fitRange), 0.1)
            ROOT.TVirtualFitter.GetFitter().GetConfidenceIntervals(confIntervals)
        else:
            fMont = ROOT.TF1("fMont", "pol"+str(args.fitType), -float(args.fitRange), 0.4)
            Mont.Fit(fMont,"","",-float(args.fitRange),0.4)
            fMont.SetLineColor(ROOT.kBlack)
            confIntervals = ROOT.TH1D("confIntervals", "Cross-Fifty-Event Linear Fit with .68 conf. band", 10, -float(args.fitRange), 0.4)
            ROOT.TVirtualFitter.GetFitter().GetConfidenceIntervals(confIntervals, 0.68)
        confIntervals.SetStats(False)
        confIntervals.SetFillColorAlpha(ROOT.kGray, 0.5)
    else:
        Mont.Fit("pol"+str(args.fitType),"","",-float(args.fitRange),0.4)
print "Fit done"
Mont.Draw("peX0C")
fixsplithist(hS, Mont)

ROOT.gStyle.SetOptStat(0)
c1.cd()
c1.SetName(output_pdf_name.replace("-","m"))
if not args.compareExtrapRegion:
    c1.Write()
    c1.SaveAs(output_pdf_name.replace("-","m"), ".pdf")
    c1.SaveAs(output_C_name.replace("-","m"), ".C")


ROOT.gStyle.SetOptStat(0)
if args.compareToData:
    if args.reweighedXevt:
        opt = "_XevtReweighed"
    else:
        opt = ""
    if args.unblind:
        opt += "_unblind"
    if not args.compareExtrapRegion:
        output_pdf_name_compare = "../Signal_Bkg_Ratios_plots/h_BDT_ExtrapolationFactor_"+samplename+"_"+FitOpt.replace(".","p")+opt+".pdf"
        output_C_name_compare = "../Signal_Bkg_Ratios_plots/h_BDT_ExtrapolationFactor_"+samplename+"_"+FitOpt.replace(".","p")+opt+".C"
        output_root_name_compare = "../Signal_Bkg_Ratios_plots/BDT_ExtrapolationFactor_"+samplename+"_"+FitOpt.replace(".","p")+opt+".root"
    else:
        output_pdf_name_compare = "../Signal_Bkg_Ratios_plots/h_BDT_CompareDataXevt_"+samplename+"_"+FitOpt.replace(".","p")+opt+".pdf"
        output_C_name_compare = "../Signal_Bkg_Ratios_plots/h_BDT_CompareDataXevt_"+samplename+"_"+FitOpt.replace(".","p")+opt+".C"
        output_root_name_compare = "../Signal_Bkg_Ratios_plots/BDT_CompareDataXevt_"+samplename+"_"+FitOpt.replace(".","p")+opt+".root"
    ROOT.gStyle.SetOptStat(0)
    fOut_compare = ROOT.TFile(output_root_name_compare, "RECREATE")
    ROOT.gStyle.SetOptStat(0)
    
    hSbar_data = ROOT.TH1F("h_Sbar_BDT_data",'; BDT classifier; N_{ev}/0.02 BDT class.',60,-0.7,0.5)
    print "data Sbar file:", Sbar_location_data + "DiscrApplied_" + samplename_data + ".root"
    fSbar_data = ROOT.TFile.Open(Sbar_location_data + "DiscrApplied_" + samplename_data + ".root")
    tSbar_data = fSbar_data.Get("FlatTree")
    nSbar_data= tSbar_data.GetEntries()
    print "Sbar in Data Tree:\t",nSbar_data
    if args.unblind:
        hSbar_data_u = ROOT.TH1F("h_Sbar_BDT_data_u",'; BDT classifier; N_{ev}/0.02 BDT class.',60,-0.7,0.5)
        fSbar_data_u = ROOT.TFile.Open(Sbar_location_data_u + "DiscrApplied_" + samplename_data_u + ".root")
        print "Unblound data Sbar file:", Sbar_location_data_u + "DiscrApplied_" + samplename_data_u + ".root"
        tSbar_data_u = fSbar_data_u.Get("FlatTree")
        nSbar_data_u_total = tSbar_data_u.GetEntries()
        nSbar_data_u = tSbar_data_u.GetEntries("SexaqBDT >= 0.1")
        print "Unblound Data Sbar with high BDT score:\t", nSbar_data_u
    for i in range(0, nSbar_data):
        if i > nSMax:
            break
        tSbar_data.GetEntry(i)
        w = 1
        if tSbar_data._S_nGoodPVs[0] >= 60 or tSbar_data._S_nGoodPVs[0] <= 0:
            w = 0
        hSbar_data.Fill(tSbar_data.SexaqBDT, w)
    if args.unblind:
        for i in range(0, nSbar_data_u_total):
            if i > nSMax:
                break
            tSbar_data_u.GetEntry(i)
            if tSbar_data_u.SexaqBDT < 0.1: continue
            w = 1
            if tSbar_data_u._S_nGoodPVs[0] >= 60 or tSbar_data_u._S_nGoodPVs[0] <= 0:
                w = 0
            hSbar_data_u.Fill(tSbar_data_u.SexaqBDT, w)
    #print "Integral of data Sbar Histogram:\t", hSbar_data.Integral()
    hS_data = ROOT.TH1F("h_S_BDT_data",'; BDT classifier; N_{ev}/0.02 BDT class.',60,-0.7,0.5)
    print "data S file: ", S_location_data + "DiscrApplied_" + samplename_data + ".root"
    fS_data = ROOT.TFile.Open(S_location_data + "DiscrApplied_" + samplename_data + ".root")
    tS_data = fS_data.Get("FlatTree")
    nS_data = tS_data.GetEntries()
    print "S in Data Tree:\t", nS_data
    for i in range(0, nS_data):
        if i > nSMax:
            break
        tS_data.GetEntry(i)
        w = 1
        if tS_data._S_nGoodPVs[0] >= 60 or tS_data._S_nGoodPVs[0] <= 0:
            w = 0
        hS_data.Fill(tS_data.SexaqBDT, w)
    #print "Integral of data S Histogram:\t", hS_data.Integral()
    hSbar_data.Sumw2()
    hS_data.Sumw2()
    hS_data.SetStats(0)
    hSbar_data.SetStats(0)
    if args.unblind:
        hSbar_data_u.Sumw2()
        hSbar_data_u.SetStats(0)

    fOut_compare.cd()
    ROOT.gStyle.SetOptStat(0)
    Mont_data = hS_data.Clone("Mont_data")
    #print "S in Data Hist:\t", Mont_data.Integral()
    Mont_data.SetStats(0)
    Mont_data.Divide(hSbar_data, hS_data, 1.0, 1.0)
    #print "does the ratio work out?:\t", Mont_data.Integral()
    if args.unblind:
        Mont_data_u = hS_data.Clone("Mont_data_u")
        Mont_data_u.SetStats(0)
        Mont_data_u.Divide(hSbar_data_u, hS_data, 1.0, 1.0)
        colorIt(hSbar_data_u, ROOT.kBlack)
    
    #c1 = TCanvas("h_BDT_"+samplename, "", 700, 900)
    #c1.Draw()
    #c1.cd()
    colorIt(hS_data, ROOT.kMagenta)
    if not args.compareExtrapRegion:
        if args.unblind:
            c1_compare = ReadyCanvas("h_BDT_ExtrapolationFactor"+samplename, 700, 1200)
        else:
            c1_compare = ReadyCanvas("h_BDT_ExtrapolationFactor"+samplename, 700, 900)
    else:
        if args.unblind:
            c1_compare = ReadyCanvas("h_BDT_CompareDataXevt"+samplename, 700, 1200)
        else:
            c1_compare = ReadyCanvas("h_BDT_CompareDataXevt"+samplename, 700, 900)

    p1_compare = ReadyTopPad("p1_compare", "p2_compare", xlow, ratio, xhigh, ytop)
    ROOT.gPad.SetLogy()
    #gPad.SetGridx()
    #gPad.SetGridy()
    
    colorIt(hSbar_data, ROOT.kOrange)
    
    hS_data.SetMarkerStyle(23)
    hS.Draw("peXOC")
    hSbar.Draw("peXOCsame")
    hS_data.Draw("peXOCsame")
    hSbar_data.Draw("peXOCsame")
    if args.unblind:
        hSbar_data_u.Draw("peXOCsame")
    CMSStyle.setCMSLumiStyle(c1_compare, 11, lumiTextSize_=0.74)
    
    if "data" in samplename_data.lower() and "xevt" not in samplename_data.lower():
        legend.AddEntry(hS_data,"Data S","ple");
        legend.AddEntry(hSbar_data,"Data #bar{S} BDT class. < 0.1  ","ple");
    else:
        legend.AddEntry(hS_data,"Cross-Fifty-Event S","ple");
        legend.AddEntry(hSbar_data,"Cross-Fifty-Event #bar{S}","ple");
    if args.unblind:
        legend.AddEntry(hSbar_data_u,"Data #bar{S}, BDT class. #geq 0.1","ple");
    
    hSbar_data.SetMarkerSize(0.8)
    legend.Draw()
    
    c1_compare.cd()
    p2_compare = ReadyBotPad("p2_compare", xlow, ybot, xhigh, ratio)

    legend_ratios = ROOT.TLegend(0.65, 0.7, 0.99, 0.99)
    ROOT.gPad.SetGridy()
    colorIt(Mont_data,ROOT.kRed)
    Mont_data.SetMinimum(0.5);
    if args.unblind:
        Mont_data.SetMaximum(2);
    else:
        Mont_data.SetMaximum(1.5);
    Mont_data.GetXaxis().SetTitleOffset(1.2);
    Mont_data.GetYaxis().SetTitleOffset(3.);
    Mont_data.SetYTitle("#bar{S}/S");
    if "data" in samplename_data.lower() and "xevt" not in samplename_data.lower():
        if args.compareExtrapRegion:
            fMont_data = ROOT.TF1("fMont_data", "pol"+str(args.fitType), -float(args.fitRange), 0.1)
        else:
            fMont_data = ROOT.TF1("fMont_data", "pol"+str(args.fitType), -float(args.fitRange), 0.4)
        Mont_data.Fit(fMont_data,"","",-float(args.fitRange),0.1)
        #fMont_data.SetLineWidth(2)
        fMont_data.SetLineColor(ROOT.kRed)
        if args.compareExtrapRegion:
            confIntervals_data = ROOT.TH1D("confIntervals_data", "Cross-Fifty-Event Linear Fit with .95 conf. band", 10, -float(args.fitRange), 0.1)
            ROOT.TVirtualFitter.GetFitter().GetConfidenceIntervals(confIntervals_data)
        else:
            confIntervals_data = ROOT.TH1D("confIntervals_data", "Cross-Fifty-Event Linear Fit with .68 conf. band", 10, -float(args.fitRange), 0.4)
            ROOT.TVirtualFitter.GetFitter().GetConfidenceIntervals(confIntervals_data, 0.68)
        confIntervals_data.SetStats(False)
        confIntervals_data.SetFillColorAlpha(ROOT.kRed-7, 0.5)
    Mont.Draw("peX0C")
    fMont.Draw("c same")
    confIntervals.SetMarkerSize(0)
    confIntervals.Draw("ce3 same")
    Mont_data.Draw("peX0Csame")
    fMont_data.Draw("c same")
    confIntervals_data.SetMarkerSize(0)
    confIntervals_data.Draw("ce3 same")
    if args.unblind:
        colorIt(Mont_data_u, ROOT.kBlue)
        Mont_data_u.Draw("peX0Csame")
    masshypothesis=""
    if args.mass == "1p7" or args.mass == "1p8" or args.mass == "1p85" or args.mass == "1p9" or args.mass == "2": 
        masshypothesis= " "+args.mass+" GeV Mass Hypothesis"
    legend_ratios.AddEntry(Mont,"Cross-Fifty-Event #bar{S}/S Ratio", "ple")
    #legend_ratios.AddEntry(Mont,"No nPV training Data #bar{S}/S Ratio"+masshypothesis, "ple")
    if args.compareExtrapRegion:
        legend_ratios.AddEntry(fMont,"Linear Fit, with .95 CI", "l")
    else:
        legend_ratios.AddEntry(fMont,"Linear Fit, with .68 CI", "l")
    legend_ratios.AddEntry(Mont_data,"Data #bar{S}/S Ratio"+masshypothesis, "ple")
    if args.compareExtrapRegion:
        legend_ratios.AddEntry(fMont_data,"Linear Fit, with .95 CI", "l")
    else:
        legend_ratios.AddEntry(fMont_data,"Linear Fit, with .68 CI", "l")
    if args.unblind:
        legend_ratios.AddEntry(Mont_data_u,"Unblinded #bar{S}/S Ratio", "ple")
    legend_ratios.Draw()
    fixsplithist(hS, Mont)
    
    ROOT.gStyle.SetOptStat(0)
    c1_compare.cd()
    c1_compare.SetName(output_pdf_name_compare.replace("-","m"))
    c1_compare.Write()
    c1_compare.SaveAs(output_pdf_name_compare.replace("-","m"), ".pdf")
    c1_compare.SaveAs(output_C_name_compare.replace("-","m"), ".C")
    
    
    ROOT.gStyle.SetOptStat(0)
    if not args.compareExtrapRegion:
        print "Sbar/S = (", fMont.GetParameter(1), "+/-", fMont.GetParError(1), ")*[BDT] + ", fMont.GetParameter(0), "+/-", fMont.GetParError(0)
        factor = fMont.GetParameter(1)*args.uncertaintyRegion + fMont.GetParameter(0)
        print "\t at BDT of "+str(args.uncertaintyRegion)+": ", factor
        print "uncertainty in fit = (Sbar/S (BDT))^(-1) * sqrt(", fMont.GetParError(1)**2, "*[BDT]^2 + ", fMont.GetParError(0)**2, ")"
        fit_u2 = (fMont.GetParError(1)**2*args.uncertaintyRegion**2 + fMont.GetParError(0)**2)/(factor**2)
        print "\t at BDT of "+str(args.uncertaintyRegion)+": ", ROOT.TMath.Sqrt(fit_u2)
        print "Extrapolation Lower Estimate = (", fMont_data.GetParameter(1), "+/-", fMont_data.GetParError(1), ")*[BDT] + ", fMont_data.GetParameter(0), "+/-", fMont_data.GetParError(0)
        factor_lb = fMont_data.GetParameter(1)*args.uncertaintyRegion + fMont_data.GetParameter(0)
        print "\t at BDT of "+str(args.uncertaintyRegion)+": ", factor_lb
        u_diff = (factor - factor_lb)/factor
        print "\t uncertainty due to difference: ", u_diff
        print "uncertainty in Lower Estimate = (Extrapolation LE (BDT))^(-1) * sqrt(", fMont_data.GetParError(1)**2, "*[BDT]^2 + ", fMont_data.GetParError(0)**2, ")"
        lb_u2 = (fMont_data.GetParError(1)**2*args.uncertaintyRegion**2 + fMont_data.GetParError(0)**2)/(factor_lb**2)
        print "\t at BDT of "+str(args.uncertaintyRegion)+": ", ROOT.TMath.Sqrt(lb_u2)
        print "overall uncertainty at BDT of "+str(args.uncertaintyRegion)+": ", ROOT.TMath.Sqrt(lb_u2 + fit_u2 + u_diff**2)
        print "overall uncertainty at BDT of "+str(args.uncertaintyRegion)+" Without LE Uncertainty: ", ROOT.TMath.Sqrt(fit_u2 + u_diff**2)
        print "\n POISSON ERRORS at BDT "+str(args.uncertaintyRegion)+":"
        nS = tS.GetEntries("SexaqBDT > "+str(args.uncertaintyRegion))
        nSbar = tSbar.GetEntries("SexaqBDT > "+str(args.uncertaintyRegion))
        print "Number of Sbar: ", nSbar, "Number of S: ", nS
        print "\t uncertainty in Sbar: ", 1/ROOT.TMath.Sqrt(nSbar)
        print "\t uncertainty in S: ", 1/ROOT.TMath.Sqrt(nS)
        print "combined uncertainty: Sigma(Sbar/S) = Sbar/S * sqrt( (sigma(Sbar)/Sbar)^2 + (sigma(S)/S)^2 )"
        print "\t combined uncertainty: ", float(nSbar)/float(nS) * ROOT.TMath.Sqrt(1/float(nSbar) + 1/float(nS))
        print "\n2016 METHOD: Statistical error in Xevt Ratio as Integral for BDT > "+str(args.uncertaintyRegion)+":"
        #print "\n Statistical error in Xevt Ratio as Integral for BDT > -"+str(args.fitRange)+":"
        SbarErr = ROOT.Double(0)
        #nBeginning = Mont.FindBin(-float(args.fitRange))
        nBeginning = Mont.FindBin(args.uncertaintyRegion)
        nEnd = Mont.FindBin(0.5)
        Integral = Mont.IntegralAndError(nBeginning, nEnd, SbarErr, "")#*0.05/(0.5-0.1)
        #Integral = Mont.IntegralAndError(nBeginning, nEnd, SbarErr, "")/(0.5+float(args.fitRange))
        print "\tIntegrated ratio: ", Integral
        print "\tTotal Error: ", SbarErr
        if Integral > 0:
            print "\tPercent error: ", SbarErr/Integral
    fOut_compare.Close()
fOut.Close()
