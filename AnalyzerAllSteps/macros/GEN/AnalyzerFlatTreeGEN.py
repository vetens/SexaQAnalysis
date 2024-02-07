#macro to plot the kinemaics of the generated Sbar of different masses

#from ROOT import TFile, TH1F, TH2F, TEfficiency, TH1D, TH2D, TCanvas, gROOT
from ROOT import *
import numpy as np
import sys
#sys.path.append('/user/jdeclerc/CMSSW_8_0_30_bis/src/SexaQAnalysis/AnalyzerAllSteps/macros/tdrStyle')
sys.path.append('/afs/cern.ch/work/w/wvetens/Sexaquarks/CMSSW_10_2_26/src/SexaQAnalysis/AnalyzerAllSteps/macros/tdrStyle')
import CMSStyle

gROOT.SetBatch(kTRUE)
gStyle.SetLegendTextSize(0.08)

CMSStyle.cmsText = "Private Work "
CMSStyle.extraText = " (CMS Simulation)"
CMSStyle.cmsTextFont = 42
CMSStyle.extraTextFont = 42
CMSStyle.lumiTextSize = 0.74
CMSStyle.cmsTextSize = 0.74
CMSStyle.relPosX = 2.36*0.045
CMSStyle.outOfFrame = True
CMSStyle.setTDRStyle()

colours = [1,2,4,35,38,41]

def ReadyCanvas(name):
    c = TCanvas(name, "")
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

#fIn = [
#TFile('/afs/cern.ch/work/w/wvetens/Sexaquarks/CMSSW_10_2_26/src/SexaQAnalysis/AnalyzerAllSteps/test/FlatTreeProducerGEN/output.root', 'read'),
#TFile('/afs/cern.ch/work/w/wvetens/Sexaquarks/CMSSW_10_2_26/src/SexaQAnalysis/AnalyzerAllSteps/test/FlatTreeProducerGEN/MultiSQEV.root', 'read'),
#TFile('/afs/cern.ch/work/w/wvetens/Sexaquarks/CMSSW_10_2_26/src/SexaQAnalysis/AnalyzerAllSteps/test/FlatTreeProducerGEN/MultiSQEV.root', 'read')
#]

#mass = ["Single #bar{S} Events at mass = 1.8","Multi-#bar{S} Events at mass = 1.8","All Events at mass = 1.8"]
#fIn = [
#TFile('/afs/cern.ch/work/w/wvetens/Sexaquarks/CMSSW_10_2_26/src/SexaQAnalysis/AnalyzerAllSteps/test/FlatTreeProducerGEN/output.root', 'read')
#]
#mass = ["1.8"]

fIn = [
#TFile.Open('root://cmsxrootd.hep.wisc.edu//store/user/wvetens/crmc_Sexaq/FlatTree_GEN/MCSbar_Trial1_1p7GeV.root', 'read'),
#TFile.Open('root://cmsxrootd.hep.wisc.edu//store/user/wvetens/crmc_Sexaq/FlatTree_GEN/MCSbar_Trial6_1p8GeV.root', 'read'),
#TFile.Open('root://cmsxrootd.hep.wisc.edu//store/user/wvetens/crmc_Sexaq/FlatTree_GEN/MCSbar_Trial1_1p85GeV.root', 'read'),
#TFile.Open('root://cmsxrootd.hep.wisc.edu//store/user/wvetens/crmc_Sexaq/FlatTree_GEN/MCSbar_Trial1_1p9GeV.root', 'read'),
#TFile.Open('root://cmsxrootd.hep.wisc.edu//store/user/wvetens/crmc_Sexaq/FlatTree_GEN/MCSbar_Trial1_2GeV.root', 'read')
TFile.Open('root://cmsxrootd.hep.wisc.edu//store/user/wvetens/crmc_Sexaq/FlatTree_GEN/NoEtaCut_1p7GeV.root', 'read'),
TFile.Open('root://cmsxrootd.hep.wisc.edu//store/user/wvetens/crmc_Sexaq/FlatTree_GEN/NoEtaCut_1p8GeV.root', 'read'),
TFile.Open('root://cmsxrootd.hep.wisc.edu//store/user/wvetens/crmc_Sexaq/FlatTree_GEN/NoEtaCut_1p85GeV.root', 'read'),
TFile.Open('root://cmsxrootd.hep.wisc.edu//store/user/wvetens/crmc_Sexaq/FlatTree_GEN/NoEtaCut_1p9GeV.root', 'read'),
TFile.Open('root://cmsxrootd.hep.wisc.edu//store/user/wvetens/crmc_Sexaq/FlatTree_GEN/NoEtaCut_2GeV.root', 'read')
]

mass = [
"1.7",
"1.8",
"1.85",
"1.9",
"2"
]
plots_output_dir = "plots_GEN/MassComparison/"

maxEvents = 2*1e6
#maxEvents = 2*1e3

TH1_ll = [] #list of list of 1D histos 
TH1_m2s_l = [] #list of list of 1D Multi-to-Single histos 
TH2_ll = [] #list of list of 2D histos

iFile = 0
for j, f in enumerate(fIn):
	tree = f.Get('FlatTreeProducerGEN/FlatTreeGENLevel') 

	#h_antiS_pt = TH1F('h_antiS_pt','; #bar{S} p_{T} (GeV/c); 1/N_{ev} Events/0.1GeV/c',100,0,10)
	#h_antiS_pz = TH1F('h_antiS_pz','; #bar{S} |p_{z}| (GeV/c); 1/N_{ev} Events/1GeV/c',80,0,80)
	#h_antiS_eta = TH1F('h_antiS_eta','; #bar{S} #eta ; 1/N_{ev} Events/0.1#eta',160,-8,8)
	#h_antiS_vz = TH1F('h_antiS_vz','; #bar{S} absolute creation vertex z (cm) ; 1/N_{ev} Events/cm',40,-20,20)
	#h_antiS_vz_interaction_vertex = TH1F('h_antiS_vz_interaction_vertex','; #bar{S} beampipe crossing location absolute z (cm) ; 1/N_{ev} Events/5cm',100,-250,250)
	#h_antiS_lxy = TH1F('h_antiS_lxy','; #bar{S} absolute creation vertex l_{0} (cm) ; 1/N_{ev} Events/mm',20,-1,1)

	#h_antiS_eta_pt = TH2F('h_antiS_eta_pt',';#bar{S} #eta; #bar{S} p_{T} (GeV/c); 1/N_{ev} Events/0.1#eta/0.1GeV/c',160,-8,8,100,0,10)
	#h_antiS_eta_pz = TH2F('h_antiS_eta_pz',';#bar{S} #eta; #bar{S} |p_{z}| (GeV/c); 1/N_{ev} Events/0.1#eta/1GeV/c',160,-8,8,100,0,100)
        h_antiS_N_Sbar = TH1F('h_N_antiS','; Number of #bar{S}; arbitrary units',20,0,20)
	h_antiS_pt = TH1F('h_antiS_pt','; #bar{S} p_{T} (GeV/c); arbitrary units',100,0,10)
	h_antiS_pz = TH1F('h_antiS_pz','; #bar{S} |p_{z}| (GeV/c); arbitrary units',80,0,80)
	h_antiS_eta = TH1F('h_antiS_eta','; #bar{S} #eta ; arbitrary units',160,-8,8)
	h_antiS_vz = TH1F('h_antiS_vz','; #bar{S} absolute creation vertex z (cm) ; arbitrary units',40,-20,20)
	h_antiS_vz_interaction_vertex = TH1F('h_antiS_vz_interaction_vertex','; #bar{S} beampipe crossing location absolute z (cm) ; arbitrary units',100,-250,250)
	h_antiS_lxy = TH1F('h_antiS_lxy','; #bar{S} absolute creation vertex l_{0} (cm) ; arbitrary units',20,-1,1)

	h_antiS_eta_pt = TH2F('h_antiS_eta_pt',';#bar{S} #eta; #bar{S} p_{T} (GeV/c); arbitrary units',160,-8,8,100,0,10)
	h_antiS_eta_pz = TH2F('h_antiS_eta_pz',';#bar{S} #eta; #bar{S} |p_{z}| (GeV/c); arbitrary units',160,-8,8,100,0,100)

	h_antiS_eta_multi = TH1F('h_antiS_eta_multi','; #bar{S} #eta ; arbitrary units',160,-8,8)
	h_antiS_eta_single = TH1F('h_antiS_eta_single','; #bar{S} #eta ; arbitrary units',160,-8,8)

	nEntries = tree.GetEntries()
	print 'Number of entries in the tree: ', nEntries
        print "input file", j
	for i in range(0,nEntries):
		if(i==maxEvents):
			break
		if(i%1e4 == 0):
			print "reached entry: ", i
		tree.GetEntry(i)
                #if( j == 1 and tree._N_Sbar[0] <= 1): continue
                if(tree._N_Sbar[0] == 1):
                    h_antiS_eta_single.Fill(tree._S_eta[0])
                elif(tree._N_Sbar[0] >= 1):
                    h_antiS_eta_multi.Fill(tree._S_eta[0])
                h_antiS_N_Sbar.Fill(tree._N_Sbar[0])
		h_antiS_pt.Fill(tree._S_pt[0])
		h_antiS_pz.Fill(tree._S_pz[0])
		h_antiS_eta.Fill(tree._S_eta[0])
		h_antiS_vz.Fill(tree._S_vz[0])
		vz_interaction_antiS = 2.21/np.tan( 2*np.arctan( np.exp(-tree._S_eta[0]) ) )
		h_antiS_vz_interaction_vertex.Fill(vz_interaction_antiS)
		h_antiS_lxy.Fill( np.sqrt( np.power(tree._S_vx[0],2) + np.power(tree._S_vy[0],2) ))

		h_antiS_eta_pt.Fill(tree._S_eta[0],tree._S_pt[0])
		h_antiS_eta_pz.Fill(tree._S_eta[0],abs(tree._S_pz[0]))

	TH1_l = [h_antiS_N_Sbar,h_antiS_pt,h_antiS_pz,h_antiS_eta,h_antiS_vz,h_antiS_vz_interaction_vertex,h_antiS_lxy]
	for h in TH1_l:
		h.SetDirectory(0) 
	TH1_ll.append(TH1_l)

	TH1_m2s = [h_antiS_eta_multi, h_antiS_eta_single]
	for h in TH1_m2s:
		h.SetDirectory(0) 
	TH1_m2s_l.append(TH1_m2s)
	TH2_l = [h_antiS_eta_pt, h_antiS_eta_pz]
	for h in TH2_l:
		h.SetDirectory(0) 
	TH2_ll.append(TH2_l)

	iFile+=1

#fOut = TFile('macro_FlatTree_GEN_trial4_MultiSQ_Comparison.root','RECREATE')
fOut = TFile('macro_FlatTree_GEN_Mass_Comparison.root','RECREATE')

nHistos = len(TH1_ll[0])
nMasses = len(TH1_ll)

for i in range(0,nHistos):#each list contains a list of histograms. Each list represents a specific mass. The histos need to be overlaid one list to the other
	h = TH1_ll[0][i]
	c_name = "c_"+h.GetName()
	c = ReadyCanvas(c_name)
        #c.SetLogy(1)
	legend = TLegend(0.6,0.8,0.9,0.9)
	legend.SetFillStyle(0)
	legend.SetBorderSize(0)
        upperbound = 0
	for j in range(0,nMasses):
		h = TH1_ll[j][i]
		if(h.GetSumw2N() == 0):
			h.Sumw2(kTRUE)
                if h.Integral() != 0:
		    h.Scale(1./h.Integral(), "width");
                    upperbound = max(h.GetMaximum()*1.5, upperbound)
                #    print upperbound
                #    h.SetMaximum(upperbound)
                #    #h.SetRangeUser(0,upperbound)
		#if j == 0:
		#	h.Draw("PCE1")
		#else:
		#	h.Draw("same")
		h.SetLineColor(colours[j])
		h.SetMarkerStyle(22+j)
		h.SetMarkerColor(colours[j])
		h.SetStats(0)
		#legend.AddEntry(h,"#bar{S} mass = "+ mass[j] +" GeV/c^{2}  ","lep")
	for j in range(0,nMasses):
		h = TH1_ll[j][i]
                h.SetMaximum(upperbound)
		if j == 0:
			h.Draw("PCE1")
		else:
			h.Draw("same")
		legend.AddEntry(h,mass[j] +" GeV/c^{2}  ","lep")
	legend.Draw()
        CMSStyle.setCMSLumiStyle(c,0, lumiTextSize_=0.74)
        gPad.Update()
	c.SaveAs(plots_output_dir+c_name.replace(".", "p")+".pdf")
	c.Write()

iMass = 0
for l in TH2_ll:
	for h in l:
		c_name = "c_"+h.GetName()+"_"+mass[iMass]
		c = ReadyCanvas(c_name);
		c.SetRightMargin(0.25) #make room for the tile of the z scale
		if(h.GetSumw2N() == 0):
			h.Sumw2(kTRUE)
                if h.Integral() != 0:
		    h.Scale(1./h.Integral(), "width");
		h.Draw("colz")
		h.SetStats(0)
                CMSStyle.setCMSLumiStyle(c,0, lumiTextSize_=0.74)
                gPad.Update()
		c.SaveAs(plots_output_dir+c_name.replace(".", "p")+".pdf")
		c.Write()
iMass = 0
for l in TH1_m2s_l:
	c_name = "c_h_antiS_eta_MultiVsSingle_"+mass[iMass]
	c = ReadyCanvas(c_name)
        #c.SetLogy(1)
	legend = TLegend(0.5,0.7,0.9,0.9)
	legend.SetFillStyle(0)
	legend.SetBorderSize(0)
        upperbound = 0
        #hm = l[0]
        #hs = l[1]
        Single = False
	for h in l:
		h.SetStats(0)
                if h.Integral() != 0:
		    h.Scale(1./h.Integral(), "width");
                    upperbound = max(h.GetMaximum()*1.5, upperbound)
                    #print upperbound
                    #h.SetRangeUser(0,upperbound)
                    #h.SetMaximum(upperbound)
		if(h.GetSumw2N() == 0):
			h.Sumw2(kTRUE)
		if not Single:
			#h.Draw("PCE1")
                        Single = True
		        h.SetMarkerColor(1)
		        h.SetMarkerStyle(22)
		        #legend.AddEntry(h,mass[j] +" GeV/c^{2} Events with >1 #bar{S}","lep")
		else:
			#h.Draw("same")
		        h.SetMarkerColor(2)
		        h.SetMarkerStyle(23)
		        #legend.AddEntry(h,mass[j] +" GeV/c^{2} Events with 1 #bar{S}","lep")
        Single = False
	for h in l:
            h.SetMaximum(upperbound)
	    if not Single:
                Single = True
	        h.Draw("PCE1")
	        legend.AddEntry(h,"Generated " + mass[iMass] +" GeV/c^{2} Events with >= 1 #bar{S}","lep")
	    else:
	        h.Draw("same")
	        legend.AddEntry(h,"Generated " + mass[iMass] +" GeV/c^{2} Events with 1 #bar{S}","lep")
	legend.Draw()
        CMSStyle.setCMSLumiStyle(c,0, lumiTextSize_=0.74)
        gPad.Update()
	c.SaveAs(plots_output_dir+c_name.replace(".", "p")+".pdf")
	c.Write()
	iMass += 1


fOut.Write()
fOut.Close()
