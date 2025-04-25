#macro to plot the kinemaics of the generated Sbar of different masses

#from ROOT import TFile, TH1F, TH2F, TEfficiency, TH1D, TH2D, TCanvas, gROOT
from ROOT import *
import numpy as np
import sys
from collections import OrderedDict
#sys.path.append('/user/jdeclerc/CMSSW_8_0_30_bis/src/SexaQAnalysis/AnalyzerAllSteps/macros/tdrStyle')
sys.path.append('/afs/cern.ch/work/w/wvetens/Sexaquarks/CMSSW_10_2_26/src/SexaQAnalysis/AnalyzerAllSteps/macros/tdrStyle')
import CMSStyle

gROOT.SetBatch(kTRUE)
gStyle.SetLegendTextSize(0.08)

CMSStyle.cmsText = "CMS "
#CMSStyle.extraText = " Simulation"
CMSStyle.extraText = " "
CMSStyle.lumiText = "2018 data, 237 #times 10^{9} Collisions (13 TeV)"
CMSStyle.cmsTextFont = 42
CMSStyle.extraTextFont = 42
CMSStyle.lumiTextSize = 0.74
CMSStyle.cmsTextSize = 0.74
CMSStyle.relPosX = 2.36*0.045
CMSStyle.outOfFrame = True
CMSStyle.setTDRStyle()

class plotOpts():
    def __init__(self, **kwargs):
        self.tree = kwargs.get('tree', 'tree')
        self.xmin = kwargs.get('xmin', 0)
        self.xmax = kwargs.get('xmax', 1)
        self.nbins = kwargs.get('nbins', 1)
        self.name = kwargs.get('name', 'var')
        self.opts = kwargs.get('opts', "PCE1X0")
        self.normalize = kwargs.get('normalize', True)
        self.legendOpts = kwargs.get('legendOpts', "lep")
        self.output_dir = kwargs.get('outputDir', "TrackerOccupancy_PostSelectionAOD/")
        self.legendLoc = kwargs.get('legendLoc', [0.6, 0.6, 0.99, 0.9])
        self.title = kwargs.get('title', '; '+self.name+'; Entries')
    def makePlots(self, samples):
        canvas = TCanvas("c"+self.name, "")
        PlotHeight = 0
        for sampname, sample in samples.items():
            h = sample.histos[self.name]
            if self.normalize:
                h.Scale(1/h.Integral(), "width")
            if h.GetMaximum() > PlotHeight:
                PlotHeight = h.GetMaximum()
        legend = TLegend(self.legendLoc[0],self.legendLoc[1],self.legendLoc[2],self.legendLoc[3])
        i=0
        for sampname, sample in samples.items():
            h = sample.histos[self.name]
            if self.normalize:
                h.Scale(1/h.Integral(), "width")
            h.GetYaxis().SetRangeUser(0,PlotHeight*1.2)
            if (i == 0):
                h.Draw(self.opts)
            else:
                h.Draw(self.opts+" SAME")
            i += 1
            h.SetLineColor(sample.color)
            h.SetMarkerColor(sample.color)
            h.SetMarkerStyle(sample.style)
            h.SetStats(0)
            legend.AddEntry(h, sample.title, self.legendOpts)
        legend.Draw()
        CMSStyle.setCMSLumiStyle(canvas, 11, lumiTextSize_=0.74)
        canvas.SaveAs(self.output_dir+canvas.GetName()+".pdf")
        
class Sample():
    def __init__(self, **kwargs):
        self.name = kwargs.get('name', "sample")
        self.title = kwargs.get('title', "SAMPLENAME")
        self.prescale = kwargs.get('prescale', 1)
        self.color = kwargs.get('color', 1)
        self.style = kwargs.get('style', 22)
        self.histos = OrderedDict()
        self.weightTree = kwargs.get('weightTree', False)
        self.weightName = kwargs.get('weightName', "")
        self.iflist = kwargs.get('iflist', False)
        self.isMC = kwargs.get('isMC', None)
    def loopFillHistos(self, varlist):
        if self.weightTree:
            self.treenames = [self.weightTree]
        else: 
            self.treenames = []
        nfiles = len(self.iflist)
        iF = 1
        iE = 0
        for varkey, var in varlist.items():
            self.histos[varkey] = TH1F(varkey+"_"+self.name, var.title, var.nbins, var.xmin, var.xmax)
            if var.tree not in self.treenames:
                self.treenames+= [var.tree]
        for filename in self.iflist:
            if (iF%50 == 1 and not self.isMC):
                print "accessing file "+str(iF)+"/"+str(nfiles)+" for Sample: "+self.title
            elif (iF%10 == 1 and self.isMC):
                print "accessing file "+str(iF)+"/"+str(nfiles)+" for Sample: "+self.title
            iF += 1
            f = TFile.Open(filename, 'read')
            trees = dict([(treename, f.Get(treename)) for treename in self.treenames])
            #for treename, tree in trees.items():
            #    print treename
            #    print tree#.GetEntries()
            #Get n entries from a random tree (assumed to be same number of events in each tree)
            nEvts = trees[next(iter(trees))].GetEntries()
            for i in range(0, nEvts):
                #If prescaling isn't 1, skip events that don't match the prescaling
                if iE % self.prescale != 0: continue
                iE += 1
                for treename, tree in trees.items():
                    tree.GetEntry(i)
                weight = 1
                if self.isMC and self.weightTree:
                    weight = getattr(trees[self.weightTree],self.weightName)[0]
                for varkey, var in varlist.items():
                    value = getattr(trees[var.tree],varkey)[0]
                    self.histos[varkey].Fill(value, weight)
varslist = OrderedDict()
varslist["_nTracksTotal"] = plotOpts(name="_nTracksTotal", xmin = 0, xmax = 3500, nbins = 100, title = "; Total #Tracks; A.U.", tree="FlatTreeProducerTrackerOccupancy/FlatTreeTracks")
varslist["_nTracks_1_eta_2"] = plotOpts(name="_nTracks_1_eta_2", xmin = 0, xmax = 1500, nbins = 30, title = "; #Tracks with 1 < |#eta| < 2; A.U.", tree="FlatTreeProducerTrackerOccupancy/FlatTreeTracks")
varslist["_nTracks_2_eta_2p5"] = plotOpts(name="_nTracks_2_eta_2p5", xmin = 0, xmax = 800, nbins = 16, title = "; #Tracks with 2 < |#eta| < 2.5; A.U.", tree="FlatTreeProducerTrackerOccupancy/FlatTreeTracks")
varslist["_nTracks_2p5_l_eta"] = plotOpts(name="_nTracks_2p5_l_eta", xmin = 0, xmax = 300, nbins = 12, title = "; #Tracks with |#eta| > 2.5; A.U.", tree="FlatTreeProducerTrackerOccupancy/FlatTreeTracks")
varslist["_nKshort"] = plotOpts(name="_nKshort", xmin = 0, xmax = 50, nbins = 25, title = "; # Ks/evt; A.U.", tree="FlatTreeProducerTrackerOccupancy/FlatTreeV0s")
varslist["_nLambda"] = plotOpts(name="_nLambda", xmin = 0, xmax = 8, nbins = 8, title = "; # #Lambda/evt; A.U.", tree="FlatTreeProducerTrackerOccupancy/FlatTreeV0s")
        
Samples = OrderedDict()
Samples["MC_1p7GeV"] = Sample(name = "MC_1p7GeV", title = "1.7 GeV Signal MC", iflist = open("1p7.txt", "r").readlines(), color = 2, style = 21, isMC = True, weightTree = "FlatTreeProducerTrackerOccupancy/FlatTreePV", weightName = "_goodPV_weightPU", prescale = 1)
Samples["MC_1p8GeV"] = Sample(name = "MC_1p8GeV", title = "1.8 GeV Signal MC", iflist = open("1p8.txt", "r").readlines(), color = 4, style = 22, isMC = True, weightTree = "FlatTreeProducerTrackerOccupancy/FlatTreePV", weightName = "_goodPV_weightPU", prescale = 1)
Samples["MC_1p85GeV"] = Sample(name = "MC_1p85GeV", title = "1.85 GeV Signal MC", iflist = open("1p85.txt", "r").readlines(), color = 6, style = 23, isMC = True, weightTree = "FlatTreeProducerTrackerOccupancy/FlatTreePV", weightName = "_goodPV_weightPU", prescale = 1)
Samples["MC_1p9GeV"] = Sample(name = "MC_1p9GeV", title = "1.9 GeV Signal MC", iflist = open("1p9.txt", "r").readlines(), color = 30, style = 25, isMC = True, weightTree = "FlatTreeProducerTrackerOccupancy/FlatTreePV", weightName = "_goodPV_weightPU", prescale = 1)
Samples["MC_2GeV"] = Sample(name = "MC_2GeV", title = "2 GeV Signal MC", iflist = open("2.txt", "r").readlines(), color = 46, style = 26, isMC = True, weightTree = "FlatTreeProducerTrackerOccupancy/FlatTreePV", weightName = "_goodPV_weightPU", prescale = 1)
Samples["Data"] = Sample(name = "Data", title = "Data", iflist = open("Data.txt", "r").readlines(), color = 1, style = 20, isMC = False, prescale = 1)

for sampname, samp in Samples.items():
    samp.loopFillHistos(varslist)
for varname, variable in varslist.items():
    variable.makePlots(Samples)
