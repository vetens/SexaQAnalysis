from ROOT import *
import numpy as np

BDT_cut_min = 0
BDT_cut_max = 0.605 #0.56
#BDT_cut_max = 0.65 #0.56
BDT_cut_step = 0.005
#BDT_cut_step = 0.05
def truncate(n, decimals=0):
    multiplier = 10 ** decimals
    return int(n * multiplier) / float(multiplier)


#fIn = TFile('../../Step1/BDTOutput_2016_dataset_BDT_2016vSelected19Parameters_CutFiducialRegion_CutDeltaPhi_CutLxy_CutDxyOverLxy_SignalWeighing.root', 'read')
	

#write a datacard
def writeDataCard(BDTCut, signal_events, countsBkg, ext_factor, syst_S_to_AntiS, masspoint):
        #ext_factor is the ratio of S to Sbar fit from high BDT value region in data
	#ext_factor = 0.903
	bkg_rate = countsBkg[1]*ext_factor
        if countsBkg[0] > 0:
            count_B = countsBkg[0]
        else:
            count_B = 1
	SmoothFactor = countsBkg[1]/count_B
        file = open("DataCardsSexaq/datacard_"+masspoint+"GeV_BDTCUT"+str(BDTCut).replace('.','p')+"_signalRate_"+str(truncate(signal_events, 2)).replace('.','p')+".card","w")
	file.write("#"+str(BDTCut)+"\n")
	file.write("#"+str(signal_events)+"\n")
        file.write("imax 1  number of channels"+"\n")
        file.write("jmax 1  number of backgrounds"+"\n")
        file.write("kmax 4  number of nuisance parameters (sources of systematical uncertainties)"+"\n")
	file.write("------------"+"\n")
	file.write("bin bin1"+"\n")
	file.write("observation "+str(bkg_rate)+"\n")
	#file.write("observation_B "+str(countsBkg[0]*ext_factor*SmoothFactor)+"\n")
	#file.write("observation_NoSmooth "+str(countsBkg[0]*ext_factor)+"\n")
	file.write("------------"+"\n")
	file.write("bin             bin1            bin1"+"\n")
	file.write("process         Sexaq_"+masspoint+"       BKG"+"\n")
	file.write("process         0               1"+"\n")
	file.write("rate           "+str(signal_events)+ "    "  +str(bkg_rate)+"\n")
	#file.write("rate_NoSmooth           "+str(signal_events)+ "    "  +str(countsBkg[0]*ext_factor)+"\n")
	file.write("------------"+"\n")
	file.write("lumi            lnN    1.05    -"+"\n")
	file.write("tracking        lnN    1.24    -"+"\n")
	file.write("S_to_AntiS      lnN    -  "+str(syst_S_to_AntiS)+"\n")
	file.write("BKG_norm_stat   lnN    -  "+str(1+1/TMath.Sqrt(bkg_rate))+"\n")
	#file.write("BKG_norm_stat_B        gmN "+str(int(count_B))+"   -   "+str(ext_factor*SmoothFactor)+"\n")
	#file.write("BKG_norm_stat_C        gmN "+str(int(countsBkg[1]))+"   -   "+str(ext_factor)+"\n")
	#file.write("BKG_norm_stat_NoSmooth        gmN "+str(int(countsBkg[0]))+"   -   "+str(ext_factor)+"\n")
	#file.write("BKG_norm_stat   lnN    -  "+str(1/TMath.Sqrt(bkg_rate))+"\n")

	file.close()

l_BDT_cut = []
i_e=0.
for e in range(0,int(BDT_cut_max/BDT_cut_step)):
	l_BDT_cut.append(BDT_cut_min+i_e*BDT_cut_step)
	i_e+=1	
l_signal_events = [1]
def BDTLoop(massString, MassPoint):
    #loop over the configurations you want to change: different BDT cuts and different signal rates
    for BDT_cut in l_BDT_cut:
    	#count = extractBGInfo(BDT_cut, MassPoint.BkgTree)
    	count = MassPoint.extractBGInfo(BDT_cut)
    	signal_eff = MassPoint.extractSignalEff(BDT_cut)
    	#syst_S_to_AntiS = 1.+l_counts[2]/l_counts[1]*np.sqrt(1./l_counts[2]+1./l_counts[1])
            #Thoughts on S to AntiS systematics: fit ratio for all BDT compared to fit ratio for high BDT region. 1 + cartesian sum of Ratio and fit uncertainties is the systematic uncertainty
        # why is it this? ^
    	for signal_events in l_signal_events:
    		writeDataCard(BDT_cut,signal_events*signal_eff,count,MassPoint.ratio(BDT_cut),MassPoint.uncertainty(BDT_cut),massString)
    
class mass_point():
#    def __init__(self, RatioSlope, RatioSlope_u, RatioIntercept, RatioIntercept_u, LBSlope, LBSlope_u, LBIntercept, LBIntercept_u, signalTree, bkgFilename, s_hname):
    def __init__(self, **kwargs):
        self.mass = kwargs['mass']
        self.RatioSlope = kwargs['RatioSlope']
        self.RatioSlope_u = kwargs['RatioSlope_u']
        self.RatioIntercept = kwargs['RatioIntercept']
        self.RatioIntercept_u = kwargs['RatioIntercept_u']
        #Here 'LB' Refers to 'Lower Bound' - this comes about from using another linear fit to characterize our uncertainty in the extrapolation of the Sbar to S ratio.
        self.LBSlope = kwargs['LBSlope']
        self.LBSlope_u = kwargs['LBSlope_u']
        self.LBIntercept = kwargs['LBIntercept']
        self.LBIntercept_u = kwargs['LBIntercept_u']
        self.SignalTree = kwargs['signalTree']
        self.SignalHist = TH1F(kwargs['s_hname'], "BDT Parameter", int(BDT_cut_max/BDT_cut_step), BDT_cut_min, BDT_cut_max)
        self.BkgFile = TFile(   kwargs['bkgFilename']           , "read")
        #print "Signal hist for mass: ", self.mass, "has name: ", self.SignalHist.GetName()
        self.BkgTree = self.BkgFile.Get('FlatTree')
        self.SmoothedBGModel = TF1("f_"+self.mass, "exp("+str(kwargs['SmoothedSlope'])+"*x+"+str(kwargs['SmoothedInt'])+")", BDT_cut_min, BDT_cut_max)
        self.SignalDenom = 0.
        for i in xrange(0, self.SignalTree.GetEntries()):
            self.SignalTree.GetEntry(i)
            w = self.SignalTree._S_event_weighting_factorPU[0] * self.SignalTree._S_event_weighting_factorM2S[0] * self.SignalTree._S_event_weighting_factor[0]
            self.SignalHist.Fill(self.SignalTree.SexaqBDT, w)
            self.SignalDenom += w
        #print "Integral of signal hist, ", self.SignalHist.Integral()
        #signal and BG handled differently because the signal has weights!
    def ratio(self, bdtCut):
        s_over_sbar = self.RatioSlope * bdtCut + self.RatioIntercept
        return s_over_sbar
    def uncertainty(self, bdtCut):
        lowerbound = self.LBSlope * bdtCut + self.LBIntercept
        ratiopoint = self.ratio(bdtCut)
        extrap_uncert = (ratiopoint - lowerbound)/ratiopoint
        #error propagation
        ratio_uncert2 = (self.RatioSlope_u**2 * bdtCut**2 + self.RatioIntercept_u**2)/ratiopoint**2
        # Calculating for now without the uncertainty in the lower bound
        #lowerbound_uncert2 = (self.LBSlope_u**2 * bdtCut**2 + self.LBIntercept_u**2)/ratiopoint**2
        #adding uncertainties in quadrature
        #uncert = TMath.Sqrt(ratio_uncert2 + lowerbound_uncert2 + extrap_uncert**2)
        uncert = TMath.Sqrt(ratio_uncert2 + extrap_uncert**2)
        #print "Uncertainty: ", uncert, "from extrapolation: ", extrap_uncert, "from propagation: ", TMath.Sqrt(ratio_uncert2 + lowerbound_uncert2)
        print "Uncertainty: ", uncert, "from extrapolation: ", extrap_uncert, "from propagation: ", TMath.Sqrt(ratio_uncert2)
        return 1+uncert
    def extractSignalEff(self, BDT_cut):
        binx = self.SignalHist.GetXaxis().FindBin(BDT_cut)
        num = self.SignalHist.Integral(binx,99999999)
    	eff = float(num)/float(self.SignalDenom)
    	print 'for BDT cut: ', BDT_cut, ' Signal efficiency: ', eff
    	return eff
    #extract some info from the histograms. The info which you need to extract is from the BDT distribution on MC how much events lie behind a certain cut. And from the BDT distribution of the S in data also the number of events which pass a certain cut
    def extractBGInfo(self, BDT_cut):
        num = self.BkgTree.GetEntries("SexaqBDT > "+ str(BDT_cut))
        numSmoothed = self.SmoothedBGModel.Integral(BDT_cut, BDT_cut_max)/BDT_cut_step
	print 'for BDT cut: ',BDT_cut,' BG count: ', num
	return [num, numSmoothed]
#    def finish(self):
#        self.BkgFile.Close()
    
BkgFileDir = '../BDTApplied_bkgReference_dataset_BDT_AllFeatures_dataset_BDT_BPH_Full_TrialB_AllPreSelection_SignalWeighing_PV_MultiToSingle_Eta_OverlapCheckFalse/'
SignalFile = TFile.Open("../BDTApplied_unblindMC_dataset_BDT_AllFeatures_dataset_BDT_BPH_Full_TrialB_AllPreSelection_SignalWeighing_PV_MultiToSingle_Eta_OverlapCheckFalse/DiscrApplied_SignalSbar_FULL.root", "read")
SignalTreeAll = SignalFile.Get('FlatTree')
#RatioSlope and Intercept are for the fit in cross-event sample on (-0.1, 0.6): i.e. the ratio of S to Sbar 
#LBSlope and Intercept (LB refers to "lower bound") are for the fit in data on (-0.1, 0.1) to correct for difference between cross-event and data and for the extrapolation into the signal region 
#SmoothedSlope and Int are for the exponential fit to data S for smoothing purposes - to eliminate poisson noise due to binning in our BDT parameter optimization (slope and int refer to the exponand)
MassPoints = {
    "1p7": mass_point( mass='1p7', RatioSlope=-0.156518386175, RatioSlope_u=0.0745212636133, RatioIntercept=0.915807612023, RatioIntercept_u=0.00528085074924, LBSlope=-0.975154467757, LBSlope_u=0.361134235246, LBIntercept=0.842681638304, LBIntercept_u=0.0227171810756,  signalTree=SignalTreeAll.CopyTree("_GEN_S_mass[0] < 1.75")                          ,  s_hname="h_1p7GeV",  SmoothedSlope=-17.2948, SmoothedInt=4.61893, bkgFilename=BkgFileDir+'DiscrApplied_1p7GeV_Data_BPH_Full_trialB.root'),#, 
    "1p8": mass_point( mass='1p8', RatioSlope=-0.134350335274, RatioSlope_u=0.0756688036778, RatioIntercept=0.914543069738, RatioIntercept_u=0.00536564625548, LBSlope=-0.832628317724, LBSlope_u=0.365218783447, LBIntercept=0.846835855353, LBIntercept_u=0.02307587303307, signalTree=SignalTreeAll.CopyTree("_GEN_S_mass[0] > 1.75 && _GEN_S_mass[0] < 1.82") ,  s_hname="h_1p8GeV",  SmoothedSlope=-16.9275, SmoothedInt=4.59583, bkgFilename=BkgFileDir+'DiscrApplied_1p8GeV_Data_BPH_Full_trialB.root'),#, 
    "1p85": mass_point(mass='1p85', RatioSlope=-0.129968135633, RatioSlope_u=0.0800826422782, RatioIntercept=0.920726856539, RatioIntercept_u=0.00566091008763,   LBSlope=-0.939052449321, LBSlope_u=0.386333744641, LBIntercept=0.846588545575, LBIntercept_u=0.024165238549,  signalTree=SignalTreeAll.CopyTree("_GEN_S_mass[0] > 1.82 && _GEN_S_mass[0] < 1.87") ,  s_hname="h_1p85GeV", SmoothedSlope=-16.8354, SmoothedInt=4.50386, bkgFilename=BkgFileDir+'DiscrApplied_1p85GeV_Data_BPH_Full_trialB.root'),#,
    "1p9": mass_point( mass='1p9',  RatioSlope=-0.121538002475, RatioSlope_u=0.0841682793972, RatioIntercept=0.919157846285, RatioIntercept_u=0.00596994162478,  LBSlope=-1.19724483395,  LBSlope_u=0.415457581051, LBIntercept=0.84234106571,  LBIntercept_u=0.0254235482808, signalTree=SignalTreeAll.CopyTree("_GEN_S_mass[0] > 1.87 && _GEN_S_mass[0] < 1.95") ,  s_hname="h_1p9GeV",  SmoothedSlope=-17.6040, SmoothedInt=4.42343, bkgFilename=BkgFileDir+'DiscrApplied_1p9GeV_Data_BPH_Full_trialB.root'),#, 
    "2": mass_point(   mass='2'  ,  RatioSlope=-0.145611286064, RatioSlope_u=0.0886911401767,  RatioIntercept=0.918547203901, RatioIntercept_u=0.00627843671708, LBSlope=-1.15437653457,  LBSlope_u=0.42554920078,  LBIntercept=0.834185477534, LBIntercept_u=0.0262440025893, signalTree=SignalTreeAll.CopyTree("_GEN_S_mass[0] > 1.95")                          ,  s_hname="h_2GeV",    SmoothedSlope=-18.0897, SmoothedInt=4.32909, bkgFilename=BkgFileDir+'DiscrApplied_2GeV_Data_BPH_Full_trialB.root')#,   
}

for mass in MassPoints:
    print "Now processing for ", mass, "GeV mass hypothesis"
#    print "There are ", MassPoints[mass].SignalDenom, "Signal Entries"
#    print "There are ", MassPoints[mass].SmoothedBGModel.Integral(0,BDT_cut_max)/BDT_cut_step, "Background Entries"
    BDTLoop(mass,MassPoints[mass])
#    MassPoints[mass].finish()

#write the l_BDT_cut and l_signal_events to a file so that these ranges can be used when running combine later to make a 2D plot
conf_file = open("DataCardsSexaq/bin_ranges.dat","w")
a = BDT_cut_min-BDT_cut_step/2.
conf_file.write(str(a)+"\n")
for i in range(0,len(l_BDT_cut)-1):
	a = (l_BDT_cut[i]+l_BDT_cut[i+1])/2.
	conf_file.write(str(a)+"\n")
a = BDT_cut_max+BDT_cut_step/2.
conf_file.write(str(a)+"\n")

conf_file.write("###\n")

#what are these?
conf_file.write(str(0.1)+"\n")
for e in l_signal_events:
	conf_file.write(str(2*e)+"\n")


SignalFile.Close()
conf_file.close()
