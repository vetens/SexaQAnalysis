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

inlist = open("BPH2_Run2018B_BLOCK_A_Test.txt", "r").readlines()
# For some reason, pyroot does not seem to want to work with xrootd or anything, so it will have to be run on local files...
#inlist = ["output_1.root"]
#inlist = ["TrackNtupleTrial4_Full.root"]
#inFiles = [TFile("file:/pnfs/iihe/cms/store/user/jdeclerc/crmc_Sexaq/FlatTree_Skimmed/CRAB_SimSexaq_trial21/crab_FlatTreeProducerTracking_trial21_02112019_v1_1p8GeV/191102_062811/0000/combined/combined_FlatTreeTracking_trial21_02112019_v1_1p8GeV.root",'read')]


#fOut = TFile(plots_output_dir+'macro_combined_FlatTree_Tracking_Skimmed_trial17.root','RECREATE')
fOut = TFile(plots_output_dir+'data_BlockA_Full.root','RECREATE')

#first make a few plots on the PV distribution to check the reweighing
PV_dir = fOut.mkdir("PV")
PV_dir.cd()

h2_nPV_vzPV_Data = TH2F('h2_nPV_vzPV_Data','; #PV; absolute v_{z} PV (cm);  Events',60,-0.5,59.5,600,-30,30)

maxEvents1 = 1e4
maxEvents2 = 1e99

for iFile, fIn in enumerate(inlist,start = 1):
        TFileIn = TFile.Open(fIn)
        PV_dir.cd()
        print "Starting with inputFile: ", str(iFile) ,"/",str(len(inlist)), ':', TFileIn.GetName()
	EvtTree = TFileIn.Get('Events')
	for ievt in range(0, EvtTree.GetEntries()):
                EvtTree.GetEntry(ievt)
		if(ievt>maxEvents1):
			break
                nGoodPV = 0
                #PV_collection = event.recoVertexs_offlinePrimaryVertices__RECO.obj
                PV_collection = EvtTree.recoVertexs_offlinePrimaryVertices__RECO
                if not PV_collection.isValid(): continue
                print PV_collection
                for i in range(0, len(PV_collection)):
                    x = PV_collection[i].position_fCoordinates.fX
                    y = PV_collection[i].position_fCoordinates.fY
                    z = PV_collection[i].position_fCoordinates.fZ
                    ndof = PV_collection[i].ndof_
                    r = TMath.Sqrt(x * x + y * y)
                    if (ndof > 4 and r < 2 and TMath.Abs(z) < 24):
                        nGoodPV+=1
                for i in range(0, len(PV_collection)):
                    x = PV_collection[i].position_fCoordinates.fX
                    y = PV_collection[i].position_fCoordinates.fY
                    z = PV_collection[i].position_fCoordinates.fZ
                    ndof = PV_collection[i].ndof_
                    r = TMath.Sqrt(x * x + y * y)
                    if (ndof > 4 and r < 2 and TMath.Abs(z) < 24):
                        h2_nPV_vzPV_Data.Fill(nGoodPV, z)
        TFileIn.Close()
h2_nPV_vzPV_Data.Write()

fOut.Close()
print "Done"
