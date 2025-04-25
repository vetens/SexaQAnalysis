#simle script to make a bit nicer looking plots for the BDT efficiency and the BDT overtraining check

from ROOT import *
import sys

sys.path.append('/afs/cern.ch/work/w/wvetens/Sexaquarks/CMSSW_10_2_26/src/SexaQAnalysis/AnalyzerAllSteps/macros/tdrStyle')
import  CMSStyle

gROOT.SetBatch(kTRUE)
gStyle.SetLegendTextSize(0.08)

CMSStyle.extraText = " (CMS Data/Simulation)"
#CMSStyle.extraText = "(CMS Simulation)"
#CMSStyle.lumiText = "Parked 2018 data, "+"237 #times 10^{9}"+" Collisions (13 TeV)"
CMSStyle.lumiText = "2018 data, "+"237 #times 10^{9}"+" Collisions (13 TeV)"
CMSStyle.cmsText = "Private Work "
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

colours = [1,2,4,35,38,41]

plots_output_dir = "plots_BDTEvaluationPlots_AllFeatures/" 

fIn = TFile('./BDTOutput_dataset_BDT_BPH_Full_TrialB_AllPreSelection_SignalWeighing_PV_MultiToSingle_Eta.root', 'read')

fIn.cd()

dir_name = 'dataset_BDT_AllFeatures_dataset_BDT_BPH_Full_TrialB_AllPreSelection_SignalWeighing_PV_MultiToSingle_Eta/Method_BDT/BDT/'

fOut = TFile(plots_output_dir+'plots_BDTEvaluationPlots.root','RECREATE')

l_overlap = [dir_name+"MVA_BDT_S",dir_name+"MVA_BDT_Train_S",dir_name+"MVA_BDT_B",dir_name+"MVA_BDT_Train_B"]
l_legend  = ["Signal (test sample)","Signal (trainging sample)","Background (test sample)","Background (training sample)"]

c = ReadyCanvas("TrainingAndTesting", 800, 600)
i = 0
#legend = TLegend(0.68,0.15,0.99,0.35)
legend = TLegend(0.6,0.7,0.9,0.9)
legend.SetFillStyle(0)
legend.SetBorderSize(0)
nentries = []
for h in l_overlap:
        h1 = fIn.Get(h)
	h1.SetTitle("")
	h1.GetXaxis().SetTitle("BDT classifier")
	#h1.GetYaxis().SetTitle("1/N_{ev} Events")
	h1.GetYaxis().SetTitle("Arbitrary Units")
	h1.GetYaxis().SetRangeUser(5*1e-5, 500)
	print h1.GetName()
	if(i==0):
        	h1.Draw()
	else:
		h1.Draw("same")
	h1.SetLineColor(colours[i])
	h1.SetMarkerStyle(22+i)
	h1.SetMarkerColor(colours[i])
	h1.SetStats(0)
        nentries += [h1.GetEntries()]
	legend.AddEntry(h1,l_legend[i],"lep")
	i+=1
c.SetLogy()
legend.Draw()
CMSStyle.setCMSLumiStyle(c, 11, lumiTextSize_= 0.74)
c.SaveAs(plots_output_dir+c.GetName()+".pdf")
for i, entries in enumerate(nentries):
    print l_legend[i], entries

c.Write()


l_overlap = [dir_name+"MVA_BDT_effS",dir_name+"MVA_BDT_effB"]
l_legend  = ["Signal efficiency","Background efficiency"]

c = ReadyCanvas("Efficiency", 800, 600)
i = 0
legend = TLegend(0.2,0.3,0.5,0.5)
legend.SetFillStyle(0)
legend.SetBorderSize(0)
for h in l_overlap:
        h1 = fIn.Get(h)
	h1.SetTitle("")
	h1.GetXaxis().SetTitle("BDT classifier")
	h1.GetYaxis().SetTitle("Efficiency")
	#h1.GetYaxis().SetRangeUser(1e-12, 1)
	h1.GetYaxis().SetRangeUser(5*1e-5, 1)
	print h1.GetName()
	if(i==0):
        	h1.Draw()
	else:
		h1.Draw("same")
	h1.SetLineColor(colours[i])
	h1.SetMarkerStyle(22+i)
	h1.SetMarkerColor(colours[i])
	h1.SetStats(0)
	legend.AddEntry(h1,l_legend[i],"l")
	i+=1
legend.Draw()
c.SetLogy()
CMSStyle.setCMSLumiStyle(c, 0, lumiTextSize_= 0.44, extraTextSize_= 0.44)
c.SaveAs(plots_output_dir+c.GetName()+".pdf")

c.Write()

#c = TCanvas("ROCCurve", "", 800, 600)
#legend = TLegend(0.2,0.3,0.5,0.5)
#effS = TGraph(fIn.Get(l_overlap[0]))
#effB = TGraph(fIn.Get(l_overlap[1]))
#ROC = TGraph()
#ROC.SetName("ROC")
#ROC.SetTitle("ROC Curve")
#ROC.GetXaxis().SetTitle("Signal Efficiency")
##ROC.GetXaxis().SetLimits(0.5, 1)
#ROC.GetYaxis().SetTitle("Background Rejection")
##ROC.GetYaxis().SetLimits(0.85, 1)
##ROC.GetXaxis().SetMoreLogLabels()
##ROC.GetYaxis().SetMoreLogLabels()
#granularity = 200.0
#for i in xrange(int(granularity)):
#        ROC.SetPoint(i,effS.Eval(i/granularity), 1-effB.Eval(i/granularity))
#ROC.Draw("L")
#legend.AddEntry(ROC,"ROC Curve for BDT","l")
#legend.Draw()
#c.SetLogy()
#c.SetLogx()
#CMS_lumi.CMS_lumi(c, 0, 11)
#c.SaveAs(plots_output_dir+c.GetName()+".pdf")
#
#c.Write()

fOut.Write()
fOut.Close()
