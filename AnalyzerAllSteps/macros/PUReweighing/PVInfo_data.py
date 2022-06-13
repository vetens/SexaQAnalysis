#script to get the z distribution of PVs and the number of PV distributions (PU). You need these specific distributions for MC reweighing to data.

from ROOT import *
import sys
from DataFormats.FWLite import Events, Handle
#sys.path.append('/user/jdeclerc/CMSSW_8_0_30_bis/src/SexaQAnalysis/AnalyzerAllSteps/macros/tdrStyle')
sys.path.append('/afs/cern.ch/work/w/wvetens/Sexaquarks/CMSSW_10_2_26/src/SexaQAnalysis/AnalyzerAllSteps/macros/tdrStyle')
import  CMS_lumi, tdrstyle 

gROOT.SetBatch(kTRUE)
gStyle.SetLegendTextSize(0.08)

tdrstyle.setTDRStyle()

plots_output_dir = "plots_data/"

inlist = open("BPH2_Run2018B_BLOCK_A_Full.txt", "r").readlines()
# For some reason, pyroot does not seem to want to work with xrootd or anything, so it will have to be run on local files...
#inlist = ["output_1.root"]
#inlist = ["TrackNtupleTrial4_Full.root"]
#inFiles = [TFile("file:/pnfs/iihe/cms/store/user/jdeclerc/crmc_Sexaq/FlatTree_Skimmed/CRAB_SimSexaq_trial21/crab_FlatTreeProducerTracking_trial21_02112019_v1_1p8GeV/191102_062811/0000/combined/combined_FlatTreeTracking_trial21_02112019_v1_1p8GeV.root",'read')]


#fOut = TFile(plots_output_dir+'macro_combined_FlatTree_Tracking_Skimmed_trial17.root','RECREATE')
fOut = TFile(plots_output_dir+'data_BlockA_Full_With1D.root','RECREATE')

#first make a few plots on the PV distribution to check the reweighing
PV_dir = fOut.mkdir("PV")
PV_dir.cd()

h2_nPV_vzPV_Data = TH2F('h2_nPV_vzPV_Data','; #PV; absolute v_{z} PV (cm);  Events',60,-0.5,59.5,600,-30,30)
h_PVz_Data = TH1F("h_PVz_non_weighed",";PV absolute z;Events/cm",600,-30,30)
h_nPV_Data = TH1I('h_nPV_MC_non_weighed','; # valid PV; Events',60,-0.5,59.5)

maxEvents1 = 1e4
maxEvents2 = 1e99

for iFile, fIn in enumerate(inlist,start = 1):
        TFileIn = TFile.Open(str(fIn).strip())
        PV_dir.cd()
        print "Starting with inputFile: ", str(iFile) ,"/",str(len(inlist)), ':', TFileIn.GetName()
	EvtTree = TFileIn.Get('FlatTreeProducerBDT/FlatTreePV')
	for ievt in range(0, EvtTree.GetEntries()):
                EvtTree.GetEntry(ievt)
		if(ievt>maxEvents2):
			break
                #print len(EvtTree._nGoodPVPOG), ", ", len(EvtTree._goodPVzPOG)
                nPV = EvtTree._nGoodPVPOG[0]
                for iPV in range(0, nPV):
                    h2_nPV_vzPV_Data.Fill(nPV, EvtTree._goodPVzPOG[iPV])
                    h_nPV_Data.Fill(nPV)
                    h_PVz_Data.Fill(EvtTree._goodPVzPOG[iPV])
        TFileIn.Close()
h2_nPV_vzPV_Data.Write()

fOut.Close()
print "Done"
