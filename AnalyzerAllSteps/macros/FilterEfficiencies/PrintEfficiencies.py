#script to overlap for signal MC and different background samples the distributions of the variables used in the BDT for different steps after doing the pre-BDT cuts
#So, first you have to prepare for a certain configuration of the pre-BDT cuts the ntuples to which a brach with the BDT classifier has been added. This can be done with the src/SexaQAnalysis/TMVA/Step2/DiscrApplication.py

#from ROOT import TFile, TH1F, TH2F, TEfficiency, TH1D, TH2D, TCanvas, gROOT
import ROOT
from ROOT import *
import numpy as np
maxEntries = 1e99


fOut = open("Efficiencies.txt", "w")

Data_S_File = ROOT.TFile.Open("/afs/cern.ch/work/w/wvetens/Sexaquarks/data/CMSSW_10_6_26/src/SexaQAnalysis/AnalyzerAllSteps/test/AnalyzeFilterEfficiencies/FilterEfficienciesBParking_trialB_FULL.root")
tree = Data_S_File.Get("FilterEfficiencies/Cutflow")
#Data_AntiS_Tree = Data_S_Bkg_File.Get("FlatTreeProducerBDT/FlatTree")
#Data Xevt Sbar Bkg from Bparking UL 2018
#Data_Sbar_Xevt_Bkg_File = ROOT.TFile.Open("/afs/cern.ch/work/w/wvetens/Sexaquarks/CMSSW_10_2_26/src/SexaQAnalysis/AnalyzerAllSteps/macros/BDT/Data_Xevt_Bkg.root")
#Data_Sbar_Xevt_Bkg_Tree = Data_Sbar_Xevt_Bkg_File.Get("FlatTreeProducerBDT/FlatTree")


nTot = 0
nLKs = 0
nFiducial = 0
nLKsVtx = 0
nLKsDeltaPhi = 0
nlxy = 0
nPointing = 0
nVz = 0
nLKsDeltaEta = 0
nLKsDeltaOpe = 0
nSKsDeltaOpe = 0
nSLDeltaOpe = 0
nEta = 0
nMinDz = 0
nKsEta = 0
nKsPt = 0
nSMass = 0
nEntries1 = tree.GetEntries()
fOut.write("---------------------------------------------------\n")
fOut.write('Efficiencies of preselection: \n')
for i in range(0,nEntries1):
	if(i==maxEntries):
		break
	tree.GetEntry(i)
        nTot += tree._nEvTotal[0]
        nLKs += tree._nEvLambdaKshort[0]
        nFiducial += tree._nEvFiducial[0]
        nLKsVtx += tree._nEvLambdaKshortVertex[0]
        nLKsDeltaPhi += tree._nEvSdauDeltaPhi[0]
        nlxy += tree._nEvlxy[0]
        nPointing += tree._nEvPointing[0]
        nVz += tree._nEvVz[0]
        nLKsDeltaEta += tree._nEvSdauDeltaEta[0]
        nLKsDeltaOpe += tree._nEvSdauDeltaOpe[0]
        nSKsDeltaOpe += tree._nEvSKsDeltaOpe[0]
        nSLDeltaOpe += tree._nEvSLambdaDeltaOpe[0]
        nEta += tree._nEvEta[0]
        nMinDz += tree._nEvMinDz[0]
        nKsEta += tree._nEvKsEta[0]
        nKsPt += tree._nEvKsPt[0]
        nSMass += tree._nEvSMass[0]
	
fOut.write("Number of Events processed: " + str(nTot) + "\n")
fOut.write("Number of Events with valid Lambda and Kshort: " + str(nLKs) + ", efficiency: " + str(float(nLKs)/float(nTot)) + "\n")
fOut.write("Number of Events within Fiducial Region: " + str(nFiducial) + ", efficiency: " + str(float(nFiducial)/float(nLKs)) + "\n")
fOut.write("Number of Events with valid Lambda Kshort Vertex: " + str(nLKsVtx) + ", efficiency: " + str(float(nLKsVtx)/float(nFiducial)) + "\n")
fOut.write("Number of Events with LKs |Delta Phi| >= 0.4 : " + str(nLKsDeltaPhi) + ", efficiency: " + str(float(nLKsDeltaPhi)/float(nLKsVtx)) + "\n")
fOut.write("Number of Events with 2.02 cm <= lxy <= 2.4 cm: " + str(nlxy) + ", efficiency: " + str(float(nlxy)/float(nLKsDeltaPhi)) + "\n")
fOut.write("Number of Events with 0 <= dxy/lxy <= 0.5: " + str(nPointing) + ", efficiency: " + str(float(nPointing)/float(nlxy)) + "\n")
fOut.write("Number of Events with |vz| <= 28 cm: " + str(nVz) + ", efficiency: " + str(float(nVz)/float(nPointing)) + "\n")
fOut.write("Number of Events with LKs |Delta Eta| <= 2: " + str(nLKsDeltaEta) + ", efficiency: " + str(float(nLKsDeltaEta)/float(nVz)) + "\n")
fOut.write("Number of Events with 0.4 <= LKs Delta Openings Angle <= 2: " + str(nLKsDeltaOpe) + ", efficiency: " + str(float(nLKsDeltaOpe)/float(nLKsDeltaEta)) + "\n")
fOut.write("Number of Events with 0.1 <= SKs Delta Openings Angle <= 1.8: " + str(nSKsDeltaOpe) + ", efficiency: " + str(float(nSKsDeltaOpe)/float(nLKsDeltaOpe)) + "\n")
fOut.write("Number of Events with 0.05 <= SL Delta Openings Angle <= 1.0: " + str(nSLDeltaOpe) + ", efficiency: " + str(float(nSLDeltaOpe)/float(nSKsDeltaOpe)) + "\n")
fOut.write("Number of Events with S |Eta| <= 3.5: " + str(nEta) + ", efficiency: " + str(float(nEta)/float(nLKsDeltaOpe)) + "\n")
fOut.write("Number of Events with |dzmin| <= 6 cm: " + str(nMinDz) + ", efficiency: " + str(float(nMinDz)/float(nEta)) + "\n")
fOut.write("Number of Events with Ks |Eta| <= 2.5: " + str(nKsEta) + ", efficiency: " + str(float(nKsEta)/float(nMinDz)) + "\n")
fOut.write("Number of Events with Ks pT >= 0.8: " + str(nKsPt) + ", efficiency: " + str(float(nKsPt)/float(nKsEta)) + "\n")
fOut.write("Number of Events with any SMass (no filter atm): " + str(nSMass) + ", efficiency: " + str(float(nSMass)/float(nKsPt)) + "\n")
fOut.write("Total Efficiency: " + str(float(nSMass)/float(nTot)) + "\n")
fOut.write("---------------------------------------------------\n")

fOut.close()
