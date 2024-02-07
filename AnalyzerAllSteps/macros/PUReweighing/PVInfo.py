# script to ready MC Sample for creation of the PU Reweighting map
# Takes as input MC Tracking NTuples
# TODO: do for data (see AnalyzerAllSteps/test/MeasurePVDistributions/MeasurePVDistributions.py for potential reference)

from ROOT import *
import random
import sys
import argparse
#sys.path.append('/user/jdeclerc/CMSSW_8_0_30_bis/src/SexaQAnalysis/AnalyzerAllSteps/macros/tdrStyle')
sys.path.append('/afs/cern.ch/work/w/wvetens/Sexaquarks/CMSSW_10_2_26/src/SexaQAnalysis/AnalyzerAllSteps/macros/tdrStyle')
import  CMS_lumi, tdrstyle 
import collections

parser = argparse.ArgumentParser(description = 'Prepare pileup distributions for reweighting map', formatter_class = argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument('--isMC', type=bool, help='Is it MC or data (include pileup weights or no?)', default = False)
parser.add_argument('--outputDir', type=str, help='Directory where output is saved', default = 'plots_MC/')
parser.add_argument('--inFiles', type=str, help='List of Input Files', default = 'TrackNtupleTrial4.txt')
parser.add_argument('--preScale', type=int, help='pick every one out of "x" events', default = 1000)
args = parser.parse_args()

gROOT.SetBatch(kTRUE)
gStyle.SetLegendTextSize(0.08)

if args.isMC:
    CMS_lumi.writeExtraText = 1
    CMS_lumi.extraText = "Simulation"
tdrstyle.setTDRStyle()

maxEvents1 = 1e4
maxEvents2 = 1e99

plots_output_dir = args.outputDir

inlist = open(args.inFiles, "r").readlines()
# For some reason, pyroot does not seem to want to work with xrootd or anything, so it will have to be run on local files...
#inlist = ["output_1.root"]
#inlist = ["TrackNtupleTrial4_Full.root"]
#inFiles = [TFile("file:/pnfs/iihe/cms/store/user/jdeclerc/crmc_Sexaq/FlatTree_Skimmed/CRAB_SimSexaq_trial21/crab_FlatTreeProducerTracking_trial21_02112019_v1_1p8GeV/191102_062811/0000/combined/combined_FlatTreeTracking_trial21_02112019_v1_1p8GeV.root",'read')]


#fOut = TFile(plots_output_dir+'macro_combined_FlatTree_Tracking_Skimmed_trial17.root','RECREATE')
fOut = TFile(plots_output_dir+'PVInfo.root','RECREATE')

#first make a few plots on the PV distribution to check the reweighing
PV_dir = fOut.mkdir("PV")
PV_dir.cd()

h_PVz = TH1F("h_PVz",";PV absolute z;Events/cm",600,-30,30)
h_nPV = TH1I('h_nPV','; # valid PV; Events',60,-0.5,59.5)
h2_nPV_vzPV = TH2F('h2_nPV_vzPV','; #PV; absolute v_{z} PV (cm);  Events',60,-0.5,59.5,600,-30,30)


for iFile, fIn in enumerate(inlist,start = 1):
        TFileIn = TFile.Open(fIn)
        PV_dir.cd()
        print "Starting with inputFile: ", str(iFile) ,"/",str(len(inlist)), ':', TFileIn.GetName()
	treePV = TFileIn.Get('PileUpScraper/FlatTreePV')
	for i in range(0,treePV.GetEntries(), 1000):
		if(i>maxEvents2):
			break
		treePV.GetEntry(i)
		for j in range(0,len(treePV._nGoodPVPOG)):
			h_PVz.Fill(treePV._goodPVzPOG[j],1.)
			h_PVz.Fill(treePV._nGoodPVPOG[j],1.)
			h2_nPV_vzPV.Fill(treePV._nGoodPVPOG[j],treePV._goodPVzPOG[j])
        TFileIn.Close()

h_PVz.Write()
h_nPV.Write()
h2_nPV_vzPV.Write()

fOut.Close()

print "Done"
