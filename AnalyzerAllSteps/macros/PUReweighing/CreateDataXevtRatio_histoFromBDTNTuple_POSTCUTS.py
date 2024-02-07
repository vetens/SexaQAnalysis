#from ROOT import TFile, TH1F, TH2F, TEfficiency, TH1D, TH2D, TCanvas, gROOT
from ROOT import *
import numpy as np
import sys
#sys.path.append('/user/jdeclerc/CMSSW_8_0_30_bis/src/SexaQAnalysis/AnalyzerAllSteps/macros/tdrStyle')
sys.path.append('/afs/cern.ch/work/w/wvetens/Sexaquarks/CMSSW_10_2_26/src/SexaQAnalysis/AnalyzerAllSteps/macros/tdrStyle')
import  CMSStyle

sys.path.insert(1, '../../../TMVA')
import configBDT as config
config_dict = config.config_dict

gROOT.SetBatch(kTRUE)
gStyle.SetLegendTextSize(0.08)

CMSStyle.extraText = "(CMS data/simulation)"
CMSStyle.lumiText = "Parked 2018 data, "+"237 #times 10^{9}"+" Collisions (13 TeV)"
CMSStyle.cmsText = "Private Work"
CMSStyle.cmsTextFont = 42
CMSStyle.extraTextFont = 42
CMSStyle.lumiTextSize = 0.74
CMSStyle.cmsTextSize = 0.74
CMSStyle.relPosX = 2.36*0.045
CMSStyle.outOfFrame = False

CMSStyle.setTDRStyle()

colours = [1,2,4,35,38,41]

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
MaxEvents = 1e7


plots_output_dir = "Results_Xevt/"

#have to reweigh on the number PVs in each event as well
n_PVn = 60
min_PVn = -0.5
max_PVn = 59.5
h_reweighingFactor_nPV = TH1F('h_reweighingFactor_nPV','; #PV; Events',n_PVn,min_PVn,max_PVn)

#Get the histograms containing data and Xevt nPV
fData = TFile.Open('file:/afs/cern.ch/work/w/wvetens/Sexaquarks/CMSSW_10_2_26/src/SexaQAnalysis/TMVA/Step2/BDTApplied_bkgReference_dataset_BDT_AllFeatures_dataset_BDT_BPH_Full_TrialB_AllPreSelection_SignalWeighing_PV_MultiToSingle_Eta_OverlapCheckFalse/DiscrApplied_Data_BPH_Full_trialB.root')
tData = fData.Get("FlatTree")
h_nPV_Data = TH1F("h_nPV_Data", '; number of Primary Vertices; Arbitrary Units', 60, -0.5, 59.5)
tData.Project('h_nPV_Data', "_S_nGoodPVs")
fXevt = TFile.Open('root://cmsxrootd.hep.wisc.edu//store/user/wvetens/data_Sexaq/FlatTree_BDT/DiscrApplied_bkgReference/50PrevEvt_XEVT_reco/bkgReference_DiscrApplied_1p8GeV_BPH_XEVT_TrialB_50PrevEvt_Full.root')
#fXevt = TFile('file:/afs/cern.ch/work/w/wvetens/Sexaquarks/data/CMSSW_10_6_26/src/SexaQAnalysis/AnalyzerAllSteps/macros/PUReweighing/plots_Xevt/PVInfo_QCD_Xevt.root')
tXevt = fXevt.Get("FlatTree")
h_nPV_Xevt = TH1F("h_nPV_Xevt", '; number of Primary Vertices; Arbitrary Units', 60, -0.5, 59.5)
tXevt.Project('h_nPV_Xevt', "_S_nGoodPVs")

#you first need to scale the data to the number of events in Xevt
Data_mean_nPV = h_nPV_Data.GetMean(1)
Xevt_mean_nPV = h_nPV_Xevt.GetMean(1)
print "mean #PV in data: ", Data_mean_nPV
print "mean #PV in Xevt  : ", Xevt_mean_nPV
NEventsData = h_nPV_Data.GetEntries()
NEventsXevt = h_nPV_Xevt.GetEntries()
print 'Events in the data: ', NEventsData
print 'Events in the Xevt: ', NEventsXevt
h_nPV_Data.Sumw2(kTRUE)
h_nPV_Xevt.Sumw2(kTRUE)

print 'PVs in the data: ', NEventsData * Data_mean_nPV 
print 'PVs in the Xevt:   ', NEventsXevt * Xevt_mean_nPV

h_nPV_Data.Scale(1.0/h_nPV_Data.Integral())
h_nPV_Xevt.Scale(1.0/h_nPV_Xevt.Integral())

#print 'normalized Data integral: ', h_nPV_Data.Integral()
#print 'normalized Xevt integral: ', h_nPV_Xevt.Integral()

if(h_nPV_Data.GetNbinsX() != h_nPV_Xevt.GetNbinsX()):
	print 'Data and Xevt plot have different number of bins'



#f = open(plots_output_dir+'PUReweigh_QCDBGToDataBPH2018_FULL.txt', "w")
f = open(plots_output_dir+'PUReweigh_nPV_XevtToDataBPH2018_FULL_POSTCUTS.txt', "w")

#loop over the PU
f.write('# nPV   Weight\n')
for i in range(1,h_nPV_Data.GetNbinsX()+1):
#	f.write('map<double,double>AnalyzerAllSteps::mapPU'+str(int(h_reweighingFactor_nPV_PVz.GetXaxis().GetBinCenter(i)))+' = ' + '{' )
	data_nPV = h_nPV_Data.GetBinContent(i)
	Xevt_nPV = h_nPV_Xevt.GetBinContent(i)
	dataToXevt_nPV = 0.
	if(Xevt_nPV>0.):
		dataToXevt_nPV = data_nPV/Xevt_nPV
	h_reweighingFactor_nPV.SetBinContent(i,dataToXevt_nPV)	
#	f.write('{'+str(h_reweighingFactor_nPV_PVz.GetYaxis().GetBinCenter(j)) + ','+str(dataToXevt_nPV_vzPV)+"}")
	f.write(str(int(h_reweighingFactor_nPV.GetXaxis().GetBinCenter(i))) + '  ' + str(dataToXevt_nPV)+"\n")
f.close()

#now do the reweighing: loop over the events again and reeigh the Xevt to data. Do this for the vz distribution of the PV as a test that your reweighing works.


h_nPV_Xevt_reweighed = h_nPV_Xevt.Clone()
h_nPV_Xevt_reweighed.SetName('h_nPV_Xevt_reweighed')
h_nPV_Xevt_reweighed.Sumw2(kTRUE)
h_nPV_Xevt_reweighed.Multiply(h_reweighingFactor_nPV)


h_nPV_Xevt_reweighed.SetName('h_nPV_Xevt_reweighed')


#fOut = TFile(plots_output_dir+'QCDXevt_PUReweighing.root','RECREATE')
fOut = TFile(plots_output_dir+'Xevt_PUReweighing.root','RECREATE')

h_nPV_Data.Write()
h_nPV_Xevt.Write()

h_reweighingFactor_nPV.Write()
h_nPV_Xevt_reweighed.Write()

h_nPV_Data.SetTitle(';absolute v_{z} valid PVs (cm);Arbitrary Units')
h_nPV_Xevt.SetTitle(';absolute v_{z} valid PVs (cm);Arbitrary Units')
h_nPV_Xevt_reweighed.SetTitle(';absolute v_{z} valid PVs (cm);Arbitrary Units')
#h_nPV_Data.Rebin(5)
#h_nPV_Xevt.Rebin(5)
#h_nPV_Xevt_reweighed.Rebin(5)
#Flipping around the ordering so that the THistPainter scales to the plot with the greatest Y value. In our current situation this is the Xevt

c_name = "c_nPV_PUReweighing"
c = ReadyCanvas(c_name)
legend = TLegend(0.75,0.8,0.9,0.9)
h_nPV_Data.SetTitle(';# valid PVs;Arbitrary Units')
h_nPV_Xevt.SetTitle(';# valid PVs;Arbitrary Units')
h_nPV_Xevt_reweighed.SetTitle(';# valid PVs;Arbitrary Units')

TH1_l = [h_nPV_Data,h_nPV_Xevt_reweighed,h_nPV_Xevt]
#TH1_l = [h_nPV_Data,h_nPV_Xevt,h_nPV_Xevt_reweighed]
Legend_l = ["Data","Xevt reweighted","Xevt"]
#Legend_l = ["Data","MC","MC reweighted"]
Legend_l_type = ["l","p","l"]
#Legend_l_type = ["l","l","p"]

for j in [2,1,0]:
#j=0
#while j < 3:
        print "Plotting ", Legend_l[j]
	h = TH1_l[j]
	#if(h.GetSumw2N() == 0):
	#	h.Sumw2(kTRUE)
	if j == 0:
		#h.Draw("C HIST")
		h.Draw("C HIST same")
	        h.SetLineWidth(2)
	        h.SetLineColor(colours[j])
	elif j == 1:
		h.Draw("P HIST same")
		#h.Draw("C HIST same")
	        h.SetMarkerStyle(23+j)
	        #h.SetLineWidth(2)
	        h.SetMarkerColor(colours[j+1])
	        #h.SetLineColor(colours[j])
	elif j == 2:
		h.Draw("C HIST")
		#h.Draw("P HIST same")
	        h.SetLineWidth(2)
	        #h.SetMarkerStyle(22+j)
	        h.SetLineColor(colours[j-1])
	        #h.SetMarkerColor(colours[j])
	h.SetStats(0)
	legend.AddEntry(h,Legend_l[j],Legend_l_type[j])
#        j+=1


legend.Draw()
CMSStyle.setCMSLumiStyle(c,11, lumiTextSize_=0.74)
#c.SaveAs(plots_output_dir+c_name.replace(".", "p")+".pdf")
c.SaveAs(plots_output_dir+c_name.replace(".", "p")+"_Xevt.pdf")
c.Write()

fOut.Write()
fOut.Close()
