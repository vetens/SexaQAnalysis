#really basic script to have an idea about the charged pion multiplicity per event in function of eta

#from ROOT import TFile, TH1F, TH2F, TEfficiency, TH1D, TH2D, TCanvas, gROOT
from ROOT import *
import numpy as np
import sys
#sys.path.append('/user/jdeclerc/CMSSW_8_0_30_bis/src/SexaQAnalysis/AnalyzerAllSteps/macros/tdrStyle')
sys.path.append('/afs/cern.ch/work/w/wvetens/Sexaquarks/CMSSW_10_2_26/src/SexaQAnalysis/AnalyzerAllSteps/macros/tdrStyle')
fIn = [
TFile('/afs/cern.ch/work/w/wvetens/Sexaquarks/CMSSW_10_2_26/src/SexaQAnalysis/AnalyzerAllSteps/test/FlatTreeProducerGEN/output.root', 'read')
]

mass = ["1.8"]

maxEvents = 1e4


h_pion_eta = TH1F('h_pion_eta','; #pi^{#pm} #eta ; Events/1#eta',24,-12,12)

iFile = 0
iEvents = 0
for f in fIn:
	tree = f.Get('FlatTreeProducerGEN/FlatTreeGENLevelPi') 

	nEntries = tree.GetEntries()
	print 'Number of entries in the tree: ', nEntries
	for i in range(0,nEntries):
		if(i==maxEvents):
			break
		if(i%1e4 == 0):
			print "reached entry: ", i
		tree.GetEntry(i)
		print 'number of pi in this event: ', len(tree._pi_eta) 
		for eta in tree._pi_eta:
			h_pion_eta.Fill(eta)
		iEvents += 1

fOut = TFile('macro_FlatTree_GEN_pion.root','RECREATE')

xaxis = h_pion_eta.GetXaxis()
for i in range(1,xaxis.GetNbins()+1):
	entries = h_pion_eta.GetBinContent(i)
	width = h_pion_eta.GetBinWidth(i)
	h_pion_eta.SetBinContent(i,entries/width)
h_pion_eta.Scale(1./iEvents*5.42/7.1) #rescale to the measurement in https://arxiv.org/pdf/1507.05915.pdf
h_pion_eta.Write()

fOut.Write()
fOut.Close()
