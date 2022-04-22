# script to ready MC Sample for creation of the PU Reweighting map
# Takes as input MC Tracking NTuples
# TODO: do for data (see AnalyzerAllSteps/test/MeasurePVDistributions/MeasurePVDistributions.py for potential reference)

from ROOT import *
import random
import sys
#sys.path.append('/user/jdeclerc/CMSSW_8_0_30_bis/src/SexaQAnalysis/AnalyzerAllSteps/macros/tdrStyle')
sys.path.append('/afs/cern.ch/work/w/wvetens/Sexaquarks/CMSSW_10_2_26/src/SexaQAnalysis/AnalyzerAllSteps/macros/tdrStyle')
import  CMS_lumi, tdrstyle 
import collections

gROOT.SetBatch(kTRUE)
gStyle.SetLegendTextSize(0.08)

CMS_lumi.writeExtraText = 1
CMS_lumi.extraText = "Simulation"
tdrstyle.setTDRStyle()

maxEvents1 = 1e4
maxEvents2 = 1e99


plots_output_dir = "plots_MC/"

inlist = open("TrackNtupleTrial4.txt", "r").readlines()
# For some reason, pyroot does not seem to want to work with xrootd or anything, so it will have to be run on local files...
#inlist = ["output_1.root"]
#inlist = ["TrackNtupleTrial4_Full.root"]
#inFiles = [TFile("file:/pnfs/iihe/cms/store/user/jdeclerc/crmc_Sexaq/FlatTree_Skimmed/CRAB_SimSexaq_trial21/crab_FlatTreeProducerTracking_trial21_02112019_v1_1p8GeV/191102_062811/0000/combined/combined_FlatTreeTracking_trial21_02112019_v1_1p8GeV.root",'read')]


#fOut = TFile(plots_output_dir+'macro_combined_FlatTree_Tracking_Skimmed_trial17.root','RECREATE')
fOut = TFile(plots_output_dir+'Trial4_Full.root','RECREATE')

#first make a few plots on the PV distribution to check the reweighing
PV_dir = fOut.mkdir("PV")
PV_dir.cd()
h_PVz_non_weighed = TH1F("h_PVz_non_weighed",";PV absolute z;Events/cm",600,-30,30)
h_PVz_PUweighed = TH1F("h_PVz_PUweighed",";PV absolute z;Events/cm",600,-30,30)
h_weight_parameter_PVz = TH1F("h_weight_parameter_PVz",";weight parameter PVz;",200,0,2)

h_nPV_MC_non_weighed = TH1I('h_nPV_MC_non_weighed','; # valid PV; Events',60,-0.5,59.5)
h_nPV_MC_PUweighed = TH1I('h_nPV_MC_PUweighed','; # valid PV; Events',60,-0.5,59.5)
h_weight_parameter_nPV = TH1F("h_weight_parameter_nPV",";weight parameter PVz;",200,0,2)

h2_nPV_vzPV_MC = TH2F('h2_nPV_vzPV_MC','; #PV; absolute v_{z} PV (cm);  Events',60,-0.5,59.5,600,-30,30)

for iFile, fIn in enumerate(inlist,start = 1):
        TFileIn = TFile.Open(fIn)
        PV_dir.cd()
        print "Starting with inputFile: ", str(iFile) ,"/",str(len(inlist)), ':', TFileIn.GetName()
	treePV = TFileIn.Get('FlatTreeProducerTracking/FlatTreePV')
	for i in range(0,treePV.GetEntries()):
		if(i>maxEvents1):
			break

		treePV.GetEntry(i)

		#draw a random vertex (you should be able to reweigh using a random vertex as a random vertex is representative for the event and this is an event by event reweighing) from the distribution and do nPV reweighing on this vertex
		randomVertexIndex = random.randint(0,len(treePV._goodPV_weightPU)-1)
		sum_weight = 0.
		for j in range(0,len(treePV._goodPV_weightPU)):
			weightPU = treePV._goodPV_weightPU[j]
			sum_weight = weightPU + sum_weight
			#print 'weightPU: ',weightPU

			h_PVz_non_weighed.Fill(treePV._goodPVzPOG[j],1.)
			h_PVz_PUweighed.Fill(treePV._goodPVzPOG[j],weightPU)
			h2_nPV_vzPV_MC.Fill(len(treePV._goodPV_weightPU),treePV._goodPVzPOG[j])	
			h_weight_parameter_PVz.Fill(weightPU)
			if j==randomVertexIndex: random_weight = weightPU

			#dic_PVz_weight.update({treePV._goodPVzPOG[j]:weightPU})
		

		#random weight
		h_nPV_MC_non_weighed.Fill(len(treePV._goodPV_weightPU),1.)
		h_nPV_MC_PUweighed.Fill(len(treePV._goodPV_weightPU),random_weight*len(treePV._goodPV_weightPU)/18.479)#/17.88*1.5) #the last two factors are just to get the overall distribution in the same ballpark as the unweighed one for MC. These are constant weights so they just represent an overall scaling to the histogram and in the end only relative weights are important
		h_weight_parameter_nPV.Fill(random_weight)
        TFileIn.Close()


h_PVz_non_weighed.Write()
h_PVz_PUweighed.Write()
h_weight_parameter_PVz.Write()

h_nPV_MC_non_weighed.Write()
h_nPV_MC_PUweighed.Write()
h_weight_parameter_nPV.Write()

h2_nPV_vzPV_MC.Write()

fOut.Close()

print "Done"
