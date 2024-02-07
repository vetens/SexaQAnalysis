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


plots_output_dir = "Results/"

#have to reweigh on the z location of the PV
n_PVZ = 600
min_PVZ = -30
max_PVZ = 30
h_reweighingFactor_PVz = TH1F('h_reweighingFactor_PVz','; absolute v_{z} PV (cm); Events/mm',n_PVZ,min_PVZ,max_PVZ)
#have to reweigh on the number PVs in each event as well
n_PVn = 60
min_PVn = -0.5
max_PVn = 59.5
h_reweighingFactor_nPV = TH1F('h_reweighingFactor_nPV','; #PV; Events',n_PVn,min_PVn,max_PVn)

h2_reweighingFactor_nPV_PVz = TH2F('h2_reweighingFactor_nPV_PVz','; #PV; absolute v_{z} PV (cm);  Events',n_PVn,min_PVn,max_PVn,n_PVZ,min_PVZ,max_PVZ)

#Get the 2D histograms containing data and MC nPV versus PV_vz
fData = TFile.Open('file:/afs/cern.ch/work/w/wvetens/Sexaquarks/data/CMSSW_10_6_26/src/SexaQAnalysis/AnalyzerAllSteps/macros/PUReweighing/plots_data/PVInfo_BPH_FULL.root')
h2_nPV_vzPV_Data = fData.Get('PV/h2_nPV_vzPV') 
h2_nPV_vzPV_Data.SetName('h2_nPV_vzPV_Data')
fMC = TFile('file:/afs/cern.ch/work/w/wvetens/Sexaquarks/data/CMSSW_10_6_26/src/SexaQAnalysis/AnalyzerAllSteps/macros/PUReweighing/plots_MC/PVInfo_SbarSignal_PU.root')
#fMC = TFile('file:/afs/cern.ch/work/w/wvetens/Sexaquarks/data/CMSSW_10_6_26/src/SexaQAnalysis/AnalyzerAllSteps/macros/PUReweighing/plots_MC/PVInfo_QCD_MC.root')
h2_nPV_vzPV_MC = fMC.Get('PV/h2_nPV_vzPV')
h2_nPV_vzPV_MC.SetName('h2_nPV_vzPV_MC')

#you first need to scale the data to the number of events in MC
Data_mean_nPV = h2_nPV_vzPV_Data.GetMean(1)
MC_mean_nPV = h2_nPV_vzPV_MC.GetMean(1)
print "mean #PV in data: ", Data_mean_nPV
print "mean #PV in mc  : ", MC_mean_nPV
NEventsData = h2_nPV_vzPV_Data.GetEntries()
NEventsMC = h2_nPV_vzPV_MC.GetEntries()
print 'Events in the data: ', NEventsData
print 'Events in the MC: ', NEventsMC
h2_nPV_vzPV_Data.Sumw2(kTRUE)
h2_nPV_vzPV_Data.Scale(1.0/NEventsData)
h2_nPV_vzPV_MC.Sumw2(kTRUE)
h2_nPV_vzPV_MC.Scale(1.0/NEventsMC)

print 'PVs in the data: ', NEventsData * Data_mean_nPV 
print 'PVs in the MC:   ', NEventsMC * MC_mean_nPV

h_nPV_Data = h2_nPV_vzPV_Data.ProjectionX()
h_nPV_Data.SetName('h_nPV_Data')
h_nPV_Data.Scale(1.0/h_nPV_Data.Integral())
h_nPV_MC = h2_nPV_vzPV_MC.ProjectionX()
h_nPV_MC.SetName('h_nPV_MC')
h_nPV_MC.Scale(1.0/h_nPV_MC.Integral())

#print 'normalized Data integral: ', h_nPV_Data.Integral()
#print 'normalized MC integral: ', h_nPV_MC.Integral()

h_vzPV_Data = h2_nPV_vzPV_Data.ProjectionY()
h_vzPV_Data.SetName('h_vzPV_Data')
h_vzPV_Data.Scale(1.0/h_vzPV_Data.Integral())
h_vzPV_MC = h2_nPV_vzPV_MC.ProjectionY()
h_vzPV_MC.SetName('h_vzPV_MC')
h_vzPV_MC.Scale(1.0/h_vzPV_MC.Integral())

if(h2_nPV_vzPV_Data.GetNbinsX() != h2_nPV_vzPV_MC.GetNbinsX()):
	print 'Data and MC plot have different number of bins in X'
if(h2_nPV_vzPV_Data.GetNbinsY() != h2_nPV_vzPV_MC.GetNbinsY()):
	print 'Data and MC plot have different number of bins in Y'



#f = open(plots_output_dir+'PUReweigh_QCDBGToDataBPH2018_FULL.txt', "w")
f = open(plots_output_dir+'PUReweigh_SignalToDataBPH2018_FULL.txt', "w")

#fill the plots with the reweighing parameter
for i in range(1,h_vzPV_Data.GetNbinsX()+1):
	data_PVvz = h_vzPV_Data.GetBinContent(i)
	mc_PVvz = h_vzPV_MC.GetBinContent(i)
	dataToMC_PVvz = 0.
	if(mc_PVvz > 0.):
		dataToMC_PVvz = data_PVvz/mc_PVvz
	h_reweighingFactor_PVz.SetBinContent(i,dataToMC_PVvz)
	

for i in range(1,h_nPV_Data.GetNbinsX()+1):
	data_nPV = h_nPV_Data.GetBinContent(i)
	mc_nPV = h_nPV_MC.GetBinContent(i)
	dataToMC_nPV = 0.
	if(mc_nPV > 0.):
		dataToMC_nPV = data_nPV/mc_nPV
	h_reweighingFactor_nPV.SetBinContent(i,dataToMC_nPV)	

#f.write(",")
#for j in range(1,h2_nPV_vzPV_Data.GetNbinsY()+1):
#	f.write(str(h2_reweighingFactor_nPV_PVz.GetYaxis().GetBinCenter(j))+",")
#f.write("\n")

#loop over the PU
f.write('# nPV   PVz     Weight\n')
for i in range(1,h2_nPV_vzPV_Data.GetNbinsX()+1):
#	f.write('map<double,double>AnalyzerAllSteps::mapPU'+str(int(h2_reweighingFactor_nPV_PVz.GetXaxis().GetBinCenter(i)))+' = ' + '{' )
	for j in range(1,h2_nPV_vzPV_Data.GetNbinsY()+1):
		data_nPV_vzPV = h2_nPV_vzPV_Data.GetBinContent(i,j)
		mc_nPV_vzPV = h2_nPV_vzPV_MC.GetBinContent(i,j)
		dataToMC_nPV_vzPV = 0.
		if(mc_nPV_vzPV>0.):
			dataToMC_nPV_vzPV = data_nPV_vzPV/mc_nPV_vzPV
		h2_reweighingFactor_nPV_PVz.SetBinContent(i,j,dataToMC_nPV_vzPV)	
#		f.write('{'+str(h2_reweighingFactor_nPV_PVz.GetYaxis().GetBinCenter(j)) + ','+str(dataToMC_nPV_vzPV)+"}")
		f.write(str(int(h2_reweighingFactor_nPV_PVz.GetXaxis().GetBinCenter(i))) + '       ' + str(h2_reweighingFactor_nPV_PVz.GetYaxis().GetBinCenter(j)) + ' ' + str(dataToMC_nPV_vzPV)+"\n")
#		if(j != h2_nPV_vzPV_Data.GetNbinsY()):
#			f.write(',')
#	f.write("};\n")
#f.write('vector<map<double,double>>AnalyzerAllSteps::v_mapPU{')
#for i in range(1,h2_nPV_vzPV_Data.GetNbinsX()+1):
#	f.write('mapPU'+str(int(h2_reweighingFactor_nPV_PVz.GetXaxis().GetBinCenter(i))))
#	if i != h2_nPV_vzPV_Data.GetNbinsX():
#		f.write(',')
#f.write('};')
    
f.close()

#now do the reweighing: loop over the events again and reeigh the mc to data. Do this for the vz distribution of the PV as a test that your reweighing works.


h2_nPV_vzPV_MC_reweighed_2D = h2_nPV_vzPV_MC.Clone()
h2_nPV_vzPV_MC_reweighed_2D.SetName('h2_nPV_vzPV_MC_reweighed_2D')
h2_nPV_vzPV_MC_reweighed_2D.Sumw2(kTRUE)
h2_nPV_vzPV_MC_reweighed_2D.Multiply(h2_reweighingFactor_nPV_PVz)


h_nPV_MC_reweighed_2D  = h2_nPV_vzPV_MC_reweighed_2D.ProjectionX()
h_nPV_MC_reweighed_2D.SetName('h_nPV_MC_reweighed_2D')
h_vzPV_MC_reweighed_2D = h2_nPV_vzPV_MC_reweighed_2D.ProjectionY()
h_vzPV_MC_reweighed_2D.SetName('h_vzPV_MC_reweighed_2D')


#fOut = TFile(plots_output_dir+'QCDMC_PUReweighing.root','RECREATE')
fOut = TFile(plots_output_dir+'SignalMC_PUReweighing.root','RECREATE')

h_reweighingFactor_PVz.Write()

h_vzPV_Data.Write()
h_vzPV_MC.Write()

h_nPV_Data.Write()
h_nPV_MC.Write()

h2_nPV_vzPV_Data.Write()
h2_nPV_vzPV_MC.Write()

h2_reweighingFactor_nPV_PVz.Write()
h_nPV_MC_reweighed_2D.Write()
h_vzPV_MC_reweighed_2D.Write()
h2_nPV_vzPV_MC_reweighed_2D.Write()

h_vzPV_Data.SetTitle(';absolute v_{z} valid PVs (cm);Arbitrary Units')
h_vzPV_MC.SetTitle(';absolute v_{z} valid PVs (cm);Arbitrary Units')
h_vzPV_MC_reweighed_2D.SetTitle(';absolute v_{z} valid PVs (cm);Arbitrary Units')
h_vzPV_Data.Rebin(5)
h_vzPV_MC.Rebin(5)
h_vzPV_MC_reweighed_2D.Rebin(5)
#Flipping around the ordering so that the THistPainter scales to the plot with the greatest Y value. In our current situation this is the MC
TH1_l = [h_vzPV_Data,h_vzPV_MC_reweighed_2D,h_vzPV_MC]
#TH1_l = [h_vzPV_Data,h_vzPV_MC,h_vzPV_MC_reweighed_2D]
Legend_l = ["Data","MC reweighted","MC"]
#Legend_l = ["Data","MC","MC reweighted"]
Legend_l_type = ["l","p","l"]
#Legend_l_type = ["l","l","p"]
c_name = "c_PVz_2D_PUReweighing"
c = ReadyCanvas(c_name)
legend = TLegend(0.75,0.8,0.9,0.9)

for j in [2,1,0]:
#j=0
#while j < 3:
	h = TH1_l[j]
        print "Plotting ", Legend_l[j]
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
        #j+=1

legend.Draw()
CMSStyle.setCMSLumiStyle(c,11, lumiTextSize_=0.74)
#c.SaveAs(plots_output_dir+c_name.replace(".", "p")+".pdf")
c.SaveAs(plots_output_dir+c_name.replace(".", "p")+"_SignalMC.pdf")
c.Write()


c_name = "c_nPV_2D_PUReweighing"
c = ReadyCanvas(c_name)
legend = TLegend(0.75,0.8,0.9,0.9)
h_nPV_Data.SetTitle(';# valid PVs;Arbitrary Units')
h_nPV_MC.SetTitle(';# valid PVs;Arbitrary Units')
h_nPV_MC_reweighed_2D.SetTitle(';# valid PVs;Arbitrary Units')

TH1_l = [h_nPV_Data,h_nPV_MC_reweighed_2D,h_nPV_MC]
#TH1_l = [h_nPV_Data,h_nPV_MC,h_nPV_MC_reweighed_2D]

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
c.SaveAs(plots_output_dir+c_name.replace(".", "p")+"_SignalMC.pdf")
c.Write()

fOut.Write()
fOut.Close()
