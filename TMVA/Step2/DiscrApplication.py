#script to take the ntuples and add a leaf to it with the BDT variable

import os
import array
import numpy
import random
import argparse

import ROOT
from ROOT import *

import sys
sys.path.insert(1, './..')
import configBDT as config

config_dict = config.config_dict
parser = argparse.ArgumentParser()
parser.add_argument('--useMassHyp', dest='UseMassHypothesis', action='store_true', default=False)
parser.add_argument('--isXevt', dest='isXevt', action='store_true', default=False)
parser.add_argument('--mass', dest='mass', action='store', default=1.7)
parser.add_argument('--splitno', dest='splitno', action='store', default='0')
parser.add_argument('--configuration', dest='configuration', action='store', default='bkgReference')
args = parser.parse_args()

#select the configuration which you want to apply, depends if you are looking at BKG, signal,...
#configuration = "bkgReference" #"partialUnblinding" (use antiS data, but do not look at stuff with BDT > 0.1), "bkgReference" (use the S as bkg reference) or unblind (use the antiS data fully) or unblindMC (use the antiS data fully, because it is MC so it is fine), or unblindMC_BG (use the antiS in BG MC, essentially the same as unblindMC without GEN Matching), 10%Unblind (unblind 10% of the data)
configuration = args.configuration #"partialUnblinding" (use antiS data, but do not look at stuff with BDT > 0.1), "bkgReference" (use the S as bkg reference) or unblind (use the antiS data fully) or unblindMC (use the antiS data fully, because it is MC so it is fine), or unblindMC_BG (use the antiS in BG MC, essentially the same as unblindMC without GEN Matching), 10%Unblind (unblind 10% of the data)
#UseMassHypothesis = False
UseMassHypothesis = args.UseMassHypothesis
#MassHypothesis = 1.7
MassHypothesis = float(args.mass)
#isXevt = True
isXevt = args.isXevt

#to make a check if there are duplicate S or Sbar due to duplicate events. This check runs pretty fast once you applied the pre-BDT cuts, but if not it is verry slow.
performOverlapCheck = False

#pointer to the results of the training:
dataset = "dataset_BDT_AllFeatures_dataset_BDT_BPH_Full_TrialB_AllPreSelection_SignalWeighing_PV_MultiToSingle_Eta"
#dataset = "dataset_BDT_AllFeatures_dataset_BDT_BPH_Full_TrialB_AllPreSelection_SignalWeighing_MultiToSingle_Eta_NoPV"
#for the data:
#fileIn= "/pnfs/iihe/cms/store/user/jdeclerc/data_Sexaq/trialR/ALL/ALL_v7"
#if you want to apply the BDT on the signal MC - Note: Do not use mass hypothesis here
#fileIn= "/afs/cern.ch/work/w/wvetens/Sexaquarks/CMSSW_10_2_26/src/SexaQAnalysis/AnalyzerAllSteps/macros/BDT/SignalSbar_FULL.root"
#if you want to apply the BDT on MC which for sure does not contain signal (the DYJets sample also used for systematics study is also used here):
#fileIn = "/afs/cern.ch/work/w/wvetens/Sexaquarks/CMSSW_10_2_26/src/SexaQAnalysis/AnalyzerAllSteps/macros/BDT/QCD_MC_BG.root"
#MC with Cross-event reconstruction (NOTE: Use isXevt = True)
#fileIn = "root://cmsxrootd.hep.wisc.edu//store/user/wvetens/data_Sexaq/FlatTree_BDT/QCD_MC_Xevt.root"
#MC without Cross-event reconstruction (NOTE: Use isXevt = True)
#fileIn = "/afs/cern.ch/work/w/wvetens/Sexaquarks/CMSSW_10_2_26/src/SexaQAnalysis/AnalyzerAllSteps/macros/BDT/QCD_MC_BG.root"
#for data BPH - DO NOT FULLY UNBLIND
fileIn= "/afs/cern.ch/work/w/wvetens/Sexaquarks/CMSSW_10_2_26/src/SexaQAnalysis/AnalyzerAllSteps/macros/BDT/Data_BPH_Full_trialB.root"
#Data with Cross-event reconstruction (NOTE: Use isXevt = True) (Ok to unblind)
#fileIn = "root://cmsxrootd.hep.wisc.edu//store/user/wvetens/data_Sexaq/FlatTree_BDT/BPH_XEVT_TrialB_Full_0.root"
#fileIn = "root://cmsxrootd.hep.wisc.edu//store/user/wvetens/data_Sexaq/FlatTree_BDT/BPH_XEVT_TrialB_Full_"+str(args.splitno)+".root"
#fileIn = "root://cmsxrootd.hep.wisc.edu//store/user/wvetens/data_Sexaq/FlatTree_BDT/BPH_XEVT_TrialB_50PrevEvt_Full_"+str(args.splitno)+".root"
#fileIn = "/afs/cern.ch/work/w/wvetens/Sexaquarks/CMSSW_10_2_26/src/SexaQAnalysis/AnalyzerAllSteps/macros/BDT/BPH_XEVT_TrialB_Full.root"

overlapList = []
def checkInOverlapList(eta,S_lxy_interaction_vertex,BDT,fileIn): #checks if the S/Sbar under consideration is already in the list by comparing with the prev ones by looking at eta and lxy of interaction vertex
	entryFound = False
	for e in overlapList:#loop over the overlap list
		if (e[0] == eta and e[1] == S_lxy_interaction_vertex): #if the eta has already been found count plus 1 and append the file list to this entry
			e[3]+=1
			print "found a ", e[3], " th/nd/rd duplicate!!, with eta: ", eta 
			e.append(fileIn)
			entryFound = True
	
	if(not entryFound): 
		overlapList.append([eta,S_lxy_interaction_vertex,BDT,1,fileIn])
	return entryFound

class TreeCloner(object):
		
	#make a separate directory to store the result
	dirname = "BDTApplied_"+configuration+"_"+dataset+"_OverlapCheck"+str(performOverlapCheck)
	if not os.path.exists(dirname):
    		os.makedirs(dirname)
	cwd = os.getcwd()

	#get the reader
	getBDTSexaqReader    = TMVA.Reader();
        varsinitialized = {}
        for var in config.variablelist:
            varsinitialized[var] = array.array('f',[0])
            getBDTSexaqReader.AddVariable(var, (varsinitialized[var]))
        #var21 = array.array('f',[0])
	##add these variables to the reader, these should be the variables also used in the BDT.py script 
        #getBDTSexaqReader.AddVariable("_S_vz_interaction_vertex",           (var1))   
	#define some variables
	#add these variables to the reader, these should be the variables also used in the BDT.py script 

	#book the weights from the training to the Reader
        getBDTSexaqReader.BookMVA("BDT","/afs/cern.ch/work/w/wvetens/Sexaquarks/CMSSW_10_2_26/src/SexaQAnalysis/TMVA/Step1/"+dataset+"/weights/TMVAClassification_BDT.weights.xml")
	fileH  = TFile.Open(fileIn)
	inTree = fileH.Get('FlatTreeProducerBDT/FlatTree')
	gROOT.cd()
	#by default look at background:
	if(configuration == "bkgReference"):
	    inTreeSelected = inTree.CopyTree(config_dict["config_SelectionBkgS"] + ' && ' + config_dict["config_pre_BDT_cuts"])
	#(partial) unblinding here:
	if(configuration == "partialUnblinding" or configuration == "unblind" or configuration == "10%Unblind"or configuration == "unblindMC_BG"):
		inTreeSelected = inTree.CopyTree(config_dict["config_SelectionAntiS"] + ' && ' + config_dict["config_pre_BDT_cuts"])
	if(configuration == "unblindMC"):
		inTreeSelected = inTree.CopyTree(config_dict["config_SelectionSignalAntiS"] + ' && ' + config_dict["config_pre_BDT_cuts"])
        print "Preselection done"
        # Adding here because At The Moment, the X-event ntuples have not been re-produced with randomized GEN Masses, so that branch needs to be added here manually
	#inTreeSelected.Show(18)
	#inTreeSelected.Print()
        print "number of entries in the inTreeSelected: ", inTreeSelected.GetEntries()
	
	#now add the leave with the BDT variable
        if UseMassHypothesis:
            fileOut = cwd+'/'+dirname+'/DiscrApplied_'+str(MassHypothesis).replace(".","p")+"GeV_"+fileIn.rsplit('/', 1)[-1]
        else:
            fileOut = cwd+'/'+dirname+'/DiscrApplied_'+fileIn.rsplit('/', 1)[-1]
        ofile   = TFile(fileOut, 'recreate')
	#clone the input tree
        outTree = inTreeSelected.CloneTree(0)
	#add a branch to the tree where you will be adding the BDT variable
	SexaqBDT = numpy.ones(1, dtype=numpy.float32)
	outTree.Branch('SexaqBDT', SexaqBDT, 'SexaqBDT/F')
        if isXevt:
	    _GEN_S_mass = numpy.ones(1, dtype=numpy.float32)
            outTree.Branch('_GEN_S_mass', _GEN_S_mass, '_GEN_S_mass/F')
	#fill the BDT branch with -999 value
        SexaqBDT[0] = -999
        for i in range(inTreeSelected.GetEntries()):		      	
	     if(configuration == "10%Unblind" and i > float(inTreeSelected.GetEntries())/10.): continue
             inTreeSelected.GetEntry(i)
             for var in config.variablelist:
                if var == "_GEN_S_mass" and UseMassHypothesis:
                    varsinitialized[var][0] = MassHypothesis
                    if isXevt:
                        _GEN_S_mass[0] = MassHypothesis
                elif var == "_GEN_S_mass" and isXevt:
                    mgen = random.choice([1.7, 1.8, 1.85, 1.9, 2.0])
                    varsinitialized[var][0] = mgen
                    _GEN_S_mass[0] = mgen
                else:
                    varsinitialized[var][0] = eval("inTreeSelected." + var+ "[0]")
	     SexaqBDT[0] = getBDTSexaqReader.EvaluateMVA('BDT')
	     #checking duplicates
	     isDuplicate = False
	     if(performOverlapCheck): isDuplicate = checkInOverlapList(inTreeSelected._S_eta[0],inTreeSelected._S_lxy_interaction_vertex[0],SexaqBDT[0],fileIn.split('/')[-1][12:-23])

	     if(not isDuplicate):
		     if(configuration  == "unblind" or configuration == "bkgReference" or configuration == "unblindMC_BG"or configuration == "unblindMC" or configuration == "10%Unblind"):
			outTree.Fill()
		     if(configuration == "partialUnblinding"):
			if(SexaqBDT[0] <=0.1):
				outTree.Fill()
	#outTree.Show(18)
	#outTree.Print() 
	ofile.Write()
	ofile.Close()


