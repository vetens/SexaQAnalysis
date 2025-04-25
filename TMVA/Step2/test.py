import numpy, random, array, ROOT, sys
from ROOT import *
sys.path.insert(1,'./..')
import configBDT as config
dataset = "dataset_BDT_AllFeatures_dataset_BDT_BPH_Full_AllPreSelection_SignalWeighing_PV_MultiToSingle_Eta"
fileIn = "root://cmsxrootd.hep.wisc.edu//store/user/wvetens/data_Sexaq/FlatTree_BDT/QCD_MC_Xevt.root"
config_dict = config.config_dict
getBDTSexaqReader = TMVA.Reader()
varsinitialized = {}
for var in config.variablelist:
     varsinitialized[var] = array.array('f',[0])
     getBDTSexaqReader.AddVariable(var, (varsinitialized[var]))

fileH  = TFile.Open(fileIn)
inTree = fileH.Get('FlatTreeProducerBDT/FlatTree')
gROOT.cd()

inTreeSelected = inTree.CopyTree(config_dict["config_SelectionAntiS"] + ' && ' + config_dict["config_pre_BDT_cuts"], "", 1000)          
print inTreeSelected.GetEntries()                                                                                                       

fileOut = "test.root"
ofile   = TFile(fileOut, 'recreate')
outTree = inTreeSelected.CloneTree(0)
SexaqBDT = numpy.ones(1, dtype=numpy.float32)
outTree.Branch('SexaqBDT', SexaqBDT, 'SexaqBDT/F')
_GEN_S_mass = numpy.ones(1, dtype=numpy.float32)
outTree.Branch('_GEN_S_mass', _GEN_S_mass, '_GEN_S_mass/F')
getBDTSexaqReader.BookMVA("BDT","/afs/cern.ch/work/w/wvetens/Sexaquarks/CMSSW_10_2_26/src/SexaQAnalysis/TMVA/Step1/"+dataset+"/weights/TMVAClassification_BDT.weights.xml")
for i in range(inTreeSelected.GetEntries()):
     inTreeSelected.GetEntry(i)
     for var in config.variablelist:
          if var == "_GEN_S_mass":
               mgen = random.choice([1.7, 1.8, 1.85, 1.9, 2.0])
               varsinitialized[var][0] = mgen
               _GEN_S_mass[0] = mgen
          else:
               varsinitialized[var][0] = eval("inTreeSelected." + var+ "[0]")
     SexaqBDT[0] = getBDTSexaqReader.EvaluateMVA('BDT')
     outTree.Fill()
ofile.Write()
