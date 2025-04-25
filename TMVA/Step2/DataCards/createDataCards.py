from ROOT import *
import numpy as np
import ctypes as ct
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--tenPctUnblind', dest='tenPctUnblind', action='store_true', default=False)
parser.add_argument('--fullUnblind', dest='fullUnblind', action='store_true', default=False)
parser.add_argument('-c', dest='BDTCut', action='store', type=float, default=0.355)
parser.add_argument('--allCuts', dest='allCuts', action='store_true', default=False)
args = parser.parse_args()

outdir = "DataCardsSexaq/"
unblindType='blind'
inDir = ''

if args.tenPctUnblind:
    outdir = "DataCards10pctUnblind/"
    unblindType='10pct'
    inDir="../BDTApplied_10%Unblind_dataset_BDT_AllFeatures_dataset_BDT_BPH_Full_TrialB_AllPreSelection_SignalWeighing_PV_MultiToSingle_Eta_OverlapCheckFalse/"
elif args.fullUnblind:
    outdir = "DataCardsFullUnblind/"
    unblindType='Full'
    inDir="../BDTApplied_unblind_dataset_BDT_AllFeatures_dataset_BDT_BPH_Full_TrialB_AllPreSelection_SignalWeighing_PV_MultiToSingle_Eta_OverlapCheckFalse/"

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
def writeDataCard(BDTCut, signal_events, countsBkg, ext_factor, syst_BG, masspoint, unblindRegion, obs=0.0):
        #ext_factor is the ratio of S to Sbar fit from high BDT value region in data
	#ext_factor = 0.903
	#bkg_rate = countsBkg[1]*ext_factor
	bkg_rate = countsBkg[2]
        if unblindRegion == '10pct':
            bkg_rate *= 0.1
        syst_S_to_AntiS = syst_BG[0]
        syst_BKG_model = syst_BG[1]
        #if countsBkg[0] > 0:
        #    count_B = countsBkg[0]
        #else:
        #    count_B = 1
	#SmoothFactor = countsBkg[1]/count_B
        file = open(outdir+"datacard_"+masspoint+"GeV_BDTCUT"+str(BDTCut).replace('.','p')+"_signalRate_"+str(truncate(signal_events, 2)).replace('.','p')+".card","w")
	file.write("#"+str(BDTCut)+"\n")
	file.write("#"+str(signal_events)+"\n")
        file.write("imax 1  number of channels"+"\n")
        file.write("jmax 1  number of backgrounds"+"\n")
        file.write("kmax 4  number of nuisance parameters (sources of systematical uncertainties)"+"\n")
	file.write("------------"+"\n")
	file.write("bin bin1"+"\n")
        if unblindRegion=='Full' or unblindRegion=='10pct':
	    file.write("observation "+str(obs)+"\n")
        else:
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
	file.write("BKG_model       lnN    -  "+str(syst_BKG_model)+"\n")
	#file.write("BKG_norm_stat   lnN    -  "+str(1+1/TMath.Sqrt(bkg_rate))+"\n")
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
def BDTLoop(massString, MassPoint, unblindStyle=unblindType):
    #loop over the configurations you want to change: different BDT cuts and different signal rates
    for BDT_cut in l_BDT_cut:
    	#count = extractBGInfo(BDT_cut, MassPoint.BkgTree)
    	count = MassPoint.extractBGInfo(BDT_cut)
    	signal_eff = MassPoint.extractSignalEff(BDT_cut)
    	#syst_S_to_AntiS = 1.+l_counts[2]/l_counts[1]*np.sqrt(1./l_counts[2]+1./l_counts[1])
        MassPoint=MassPoints[mass]
        # For 10% unblind, the model is scaled by 10% within the writeDataCard function
        if unblindStyle == '10pct' or unblindStyle == 'Full':
            if mass == '2':
                massStr='2p0'
            else: massStr=mass
            UnblindFile = TFile.Open(inDir+"DiscrApplied_"+massStr+"GeV_Data_BPH_Full_trialB.root", "read")
            UnblindTree = UnblindFile.Get('FlatTree')
            obs = UnblindTree.GetEntries("SexaqBDT > "+ str(args.BDTCut))
        else:
            obs = count
            #Thoughts on S to AntiS systematics: fit ratio for all BDT compared to fit ratio for high BDT region. 1 + cartesian sum of Ratio and fit uncertainties is the systematic uncertainty
        # why is it this? ^
    	for signal_events in l_signal_events:
    		writeDataCard(BDT_cut,signal_events*signal_eff,count,MassPoint.ratio(BDT_cut),MassPoint.uncertainty(BDT_cut),massString, unblindStyle, obs)
    
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
        
        self.Ratio = TF1("fRatio_"+self.mass,"([0]*x+[1])", BDT_cut_min, 1)
        self.Ratio.SetParameters(kwargs['RatioSlope'], kwargs['RatioIntercept'])
        ##self.Ratio = TF1("fRatio_"+self.mass,"(" + str(kwargs['RatioSlope'])+"*x+"+str(kwargs['RatioIntercept'])+")", BDT_cut_min, BDT_cut_max)
        ##self.Ratio_LB = TF1("fLB_"+self.mass,"(" + str(kwargs['LBSlope'])+"*x+"+str(kwargs['LBIntercept'])+")", BDT_cut_min, BDT_cut_max)
        #self.Ratio_LB = TF1("fLB_"+self.mass,"([0]*x+[1])", BDT_cut_min, 1)
        #self.Ratio_LB.SetParameters(kwargs['LBSlope'], kwargs['LBIntercept'])
        self.SmoothedBGModel_slope = kwargs['SmoothedSlope']
        self.SmoothedBGModel_int = kwargs['SmoothedInt']
        self.SmoothedSlope_u = kwargs['SmoothedSlope_u']
        self.SmoothedInt_u = kwargs['SmoothedInt_u']
        ##self.SmoothedBGModel = TF1("fExp_"+self.mass, "exp("+str(kwargs['SmoothedSlope'])+"*x+"+str(kwargs['SmoothedInt'])+")", BDT_cut_min, BDT_cut_max)
        #self.SmoothedBGModel = TF1("fExp_"+self.mass, "exp([0]*x+[1])", BDT_cut_min, 1)
        #self.SmoothedBGModel.SetParameters(kwargs['SmoothedSlope'], kwargs['SmoothedInt'])
        self.SbarBG = TF1("fBG_"+self.mass, "(exp("+str(kwargs['SmoothedSlope'])+"*x+"+str(kwargs['SmoothedInt'])+")) * (" + str(kwargs['RatioSlope'])+"*x+"+str(kwargs['RatioIntercept'])+")", BDT_cut_min, BDT_cut_max)
        #self.SbarBG = TF1("fBG_"+self.mass, "(exp([0]*x+[1])) * ([2]*x+[3])", BDT_cut_min, 1)
        #self.SbarBG.SetParameters(kwargs['SmoothedSlope'], kwargs['SmoothedInt'],kwargs['RatioSlope'], kwargs['RatioIntercept'])
        self.SbarBG_LB = TF1("fBG_"+self.mass, "(exp("+str(kwargs['SmoothedSlope'])+"*x+"+str(kwargs['SmoothedInt'])+")) * (" + str(kwargs['LBSlope'])+"*x+"+str(kwargs['LBIntercept'])+")", BDT_cut_min, BDT_cut_max)
        #self.SbarBG_LB = TF1("fBG_LB_"+self.mass, "(exp([0]*x+[1])) * ([2]*x+[3])", BDT_cut_min, 1)
        #self.SbarBG_LB.SetParameters(kwargs['SmoothedSlope'], kwargs['SmoothedInt'],kwargs['LBSlope'], kwargs['LBIntercept'])

        #this is the analytic integral of the background model, evaluated from x to the maximum BDT classifier value of [4], which for now we take as 1
        self.SbarBG_int = TF1("fBG_int_"+self.mass, "(exp([0]*[4]) * ([0] * ([3]+[2]*[4])-[2]) - exp([0]*x) * ([0] * ([3]+[2]*x)-[2])) * exp([1])/([0] * [0] * "+str(BDT_cut_step)+")", BDT_cut_min, 1)
        self.SbarBG_int.SetParameters(kwargs['SmoothedSlope'], kwargs['SmoothedInt'],kwargs['RatioSlope'], kwargs['RatioIntercept'], 1)
        self.SbarBG_LB_int = TF1("fBG_LB_int_"+self.mass, "(exp([0]*[4]) * ([0] * ([3]+[2]*[4])-[2]) - exp([0]*x) * ([0] * ([3]+[2]*x)-[2])) * exp([1])/([0] * [0] * "+str(BDT_cut_step)+")", BDT_cut_min, 1)
        self.SbarBG_LB_int.SetParameters(kwargs['SmoothedSlope'], kwargs['SmoothedInt'],kwargs['LBSlope'], kwargs['LBIntercept'], 1)
        self.SignalDenom = 0.
        for i in xrange(0, self.SignalTree.GetEntries()):
            self.SignalTree.GetEntry(i)
            w = self.SignalTree._S_event_weighting_factorPU[0] * self.SignalTree._S_event_weighting_factorM2S[0] * self.SignalTree._S_event_weighting_factor[0]
            self.SignalHist.Fill(self.SignalTree.SexaqBDT, w)
            self.SignalDenom += w
        #print "Integral of signal hist, ", self.SignalHist.Integral()
        #signal and BG handled differently because the signal has weights!
    #extract some info from the histograms. The info which you need to extract is from the BDT distribution on MC how much events lie behind a certain cut. And from the BDT distribution of the S in data also the number of events which pass a certain cut
    def extractBGInfo(self, BDT_cut):
        numS = self.BkgTree.GetEntries("SexaqBDT > "+ str(BDT_cut))
        ratio = self.Ratio.Eval(BDT_cut)
        #numSmoothed = self.SmoothedBGModel.Integral(BDT_cut, BDT_cut_max)/BDT_cut_step
        #numSmoothed_test = self.SbarBG.Integral(BDT_cut, BDT_cut_max)/BDT_cut_step
        #numSmoothed_LB_test = self.SbarBG_LB.Integral(BDT_cut, BDT_cut_max)/BDT_cut_step
        numSmoothed = self.SbarBG_int.Eval(BDT_cut)
        numSmoothed_LB = self.SbarBG_LB_int.Eval(BDT_cut)
        
	print 'for BDT cut: ',BDT_cut,' BG count (Sbar): ', numS*ratio, ' Smoothed (Sbar): ', numSmoothed
	return [numS, numSmoothed, numSmoothed_LB]
    def ratio(self, bdtCut):
        s_over_sbar = self.RatioSlope * bdtCut + self.RatioIntercept
        return s_over_sbar
    def uncertainty(self, bdtCut):
        lowerbound = self.LBSlope * bdtCut + self.LBIntercept
        ratiopoint = self.ratio(bdtCut)
        countAtPoint = self.extractBGInfo(bdtCut)
        #extrap_uncert = (ratiopoint - lowerbound)/ratiopoint
        extrap_uncert = (countAtPoint[1] - countAtPoint[2])/countAtPoint[1]
        #error propagation
        c = self.SmoothedBGModel_slope
        d = self.SmoothedBGModel_int 
        #ratio_uncert2 = (self.RatioSlope_u**2 * bdtCut**2 + self.RatioIntercept_u**2)/ratiopoint**2
        #ratio_uncert2 = (self.RatioSlope_u**2 * (TMath.Exp(d + c*bdtCut)*(c * bdtCut-1)/(c**2*BDT_cut_step))**2 + self.RatioIntercept_u**2 * (TMath.Exp(d + c*bdtCut)/(c*BDT_cut_step))**2 )/countAtPoint[1]**2
        SmoothedSlopeGrad = self.SbarBG_int.GradientPar(int(0), ct.c_double(bdtCut))
        SmoothedIntGrad = self.SbarBG_int.GradientPar(int(1), ct.c_double(bdtCut))
        RatioSlopeGrad = self.SbarBG_int.GradientPar(int(2), ct.c_double(bdtCut))
        RatioIntGrad = self.SbarBG_int.GradientPar(int(3), ct.c_double(bdtCut))
        propagated_Ratio_uncert2 = 0
        propagated_Smoothed_uncert2 = 0
        propagated_Ratio_uncert2 = (self.RatioSlope_u**2 * RatioSlopeGrad**2 + self.RatioIntercept_u**2 * RatioIntGrad**2)/countAtPoint[1]**2
        propagated_Smoothed_uncert2 = (self.SmoothedSlope_u**2 * SmoothedSlopeGrad**2 + self.SmoothedInt_u**2 * SmoothedIntGrad**2)/countAtPoint[1]**2
        
        # Calculating for now without the uncertainty in the lower bound
        #lowerbound_uncert2 = (self.LBSlope_u**2 * bdtCut**2 + self.LBIntercept_u**2)/ratiopoint**2
        #adding uncertainties in quadrature
        #uncert = TMath.Sqrt(ratio_uncert2 + lowerbound_uncert2 + extrap_uncert**2)
        Ratio_uncert = TMath.Sqrt(propagated_Ratio_uncert2 + extrap_uncert**2)
        Model_uncert = TMath.Sqrt(propagated_Smoothed_uncert2)
        #print "Uncertainty: ", uncert, "from extrapolation: ", extrap_uncert, "from propagation: ", TMath.Sqrt(ratio_uncert2 + lowerbound_uncert2)
        #print "Uncertainty: ", uncert, "from extrapolation: ", extrap_uncert, "from propagation: ", TMath.Sqrt(ratio_uncert2)
        print "Uncertainty in S:Sbar correction factor: ", Ratio_uncert, "from X-evt vs normal: ", extrap_uncert, "from propagation: ", TMath.Sqrt(propagated_Ratio_uncert2)
        print "Uncertainty in Extrapolated BG: ", Model_uncert
        return [1+Ratio_uncert, 1+Model_uncert]
    def extractSignalEff(self, BDT_cut):
        binx = self.SignalHist.GetXaxis().FindBin(BDT_cut)
        num = self.SignalHist.Integral(binx,99999999)
    	eff = float(num)/float(self.SignalDenom)
    	print 'for BDT cut: ', BDT_cut, ' Signal efficiency: ', eff
    	return eff
#    def finish(self):
#        self.BkgFile.Close()
    
BkgFileDir = '../BDTApplied_bkgReference_dataset_BDT_AllFeatures_dataset_BDT_BPH_Full_TrialB_AllPreSelection_SignalWeighing_PV_MultiToSingle_Eta_OverlapCheckFalse/'
SignalFile = TFile.Open("../BDTApplied_unblindMC_dataset_BDT_AllFeatures_dataset_BDT_BPH_Full_TrialB_AllPreSelection_SignalWeighing_PV_MultiToSingle_Eta_OverlapCheckFalse/DiscrApplied_SignalSbar_FULL.root", "read")
SignalTreeAll = SignalFile.Get('FlatTree')
#RatioSlope and Intercept are for the fit in cross-event sample on (-0.1, 0.6): i.e. the ratio of S to Sbar 
#LBSlope and Intercept (LB refers to "lower bound") are for the fit in data on (-0.1, 0.1) to correct for difference between cross-event and data and for the extrapolation into the signal region 
#SmoothedSlope and Int are for the exponential fit to data S for smoothing purposes - to eliminate poisson noise due to binning in our BDT parameter optimization (slope and int refer to the exponand)
MassPoints = {
    "1p7": mass_point( mass='1p7', RatioSlope=-0.156518386175, RatioSlope_u=0.0745212636133, RatioIntercept=0.915807612023, RatioIntercept_u=0.00528085074924, LBSlope=-0.975154467757, LBSlope_u=0.361134235246, LBIntercept=0.842681638304, LBIntercept_u=0.0227171810756,  signalTree=SignalTreeAll.CopyTree("_GEN_S_mass[0] < 1.75")                          ,  s_hname="h_1p7GeV",  SmoothedSlope=-17.2948, SmoothedInt=4.61893, bkgFilename=BkgFileDir+'DiscrApplied_1p7GeV_Data_BPH_Full_trialB.root',    SmoothedSlope_u=0.537252, SmoothedInt_u=0.0417837),#, 
    "1p8": mass_point( mass='1p8', RatioSlope=-0.134350335274, RatioSlope_u=0.0756688036778, RatioIntercept=0.914543069738, RatioIntercept_u=0.00536564625548, LBSlope=-0.832628317724, LBSlope_u=0.365218783447, LBIntercept=0.846835855353, LBIntercept_u=0.02307587303307, signalTree=SignalTreeAll.CopyTree("_GEN_S_mass[0] > 1.75 && _GEN_S_mass[0] < 1.82") ,  s_hname="h_1p8GeV",  SmoothedSlope=-16.9275, SmoothedInt=4.59583, bkgFilename=BkgFileDir+'DiscrApplied_1p8GeV_Data_BPH_Full_trialB.root',    SmoothedSlope_u=0.569955, SmoothedInt_u=0.0433139),#, 
    "1p85": mass_point(mass='1p85', RatioSlope=-0.129968135633, RatioSlope_u=0.0800826422782, RatioIntercept=0.920726856539, RatioIntercept_u=0.00566091008763,   LBSlope=-0.939052449321, LBSlope_u=0.386333744641, LBIntercept=0.846588545575, LBIntercept_u=0.024165238549,  signalTree=SignalTreeAll.CopyTree("_GEN_S_mass[0] > 1.82 && _GEN_S_mass[0] < 1.87") ,  s_hname="h_1p85GeV", SmoothedSlope=-16.8354, SmoothedInt=4.50386, bkgFilename=BkgFileDir+'DiscrApplied_1p85GeV_Data_BPH_Full_trialB.root', SmoothedSlope_u=0.567286, SmoothedInt_u=0.0444274),#,
    "1p9": mass_point( mass='1p9',  RatioSlope=-0.121538002475, RatioSlope_u=0.0841682793972, RatioIntercept=0.919157846285, RatioIntercept_u=0.00596994162478,  LBSlope=-1.19724483395,  LBSlope_u=0.415457581051, LBIntercept=0.84234106571,  LBIntercept_u=0.0254235482808, signalTree=SignalTreeAll.CopyTree("_GEN_S_mass[0] > 1.87 && _GEN_S_mass[0] < 1.95") ,  s_hname="h_1p9GeV",  SmoothedSlope=-17.6040, SmoothedInt=4.42343, bkgFilename=BkgFileDir+'DiscrApplied_1p9GeV_Data_BPH_Full_trialB.root',   SmoothedSlope_u=0.631330, SmoothedInt_u=0.0473845),#, 
    "2": mass_point(   mass='2'  ,  RatioSlope=-0.145611286064, RatioSlope_u=0.0886911401767,  RatioIntercept=0.918547203901, RatioIntercept_u=0.00627843671708, LBSlope=-1.15437653457,  LBSlope_u=0.42554920078,  LBIntercept=0.834185477534, LBIntercept_u=0.0262440025893, signalTree=SignalTreeAll.CopyTree("_GEN_S_mass[0] > 1.95")                          ,  s_hname="h_2GeV",    SmoothedSlope=-18.0897, SmoothedInt=4.32909, bkgFilename=BkgFileDir+'DiscrApplied_2GeV_Data_BPH_Full_trialB.root',     SmoothedSlope_u=0.691266, SmoothedInt_u=0.0504933)#,   
}

#quit()
for mass in MassPoints:
    print "Now processing for ", mass, "GeV mass hypothesis"
#    print "There are ", MassPoints[mass].SignalDenom, "Signal Entries"
#    print "There are ", MassPoints[mass].SmoothedBGModel.Integral(0,BDT_cut_max)/BDT_cut_step, "Background Entries"
    if not args.fullUnblind and not args.tenPctUnblind:
        BDTLoop(mass,MassPoints[mass])
    elif not args.allCuts:
        MassPoint=MassPoints[mass]
        # For 10% unblind, the model is scaled by 10% within the writeDataCard function
    	countBGModel = MassPoint.extractBGInfo(args.BDTCut)
    	signal_eff = MassPoint.extractSignalEff(args.BDTCut)
        SSbarRatio = MassPoint.ratio(args.BDTCut)
        BGUncertainty = MassPoint.uncertainty(args.BDTCut)
        if mass == '2':
            massStr='2p0'
        else: massStr=mass
        UnblindFile = TFile.Open(inDir+"DiscrApplied_"+massStr+"GeV_Data_BPH_Full_trialB.root", "read")
        UnblindTree = UnblindFile.Get('FlatTree')
        obs = UnblindTree.GetEntries("SexaqBDT > "+ str(args.BDTCut))
    	for signal_events in l_signal_events:
    		writeDataCard(args.BDTCut,signal_events*signal_eff,countBGModel,SSbarRatio,BGUncertainty,mass,unblindType,obs)
    if (args.fullUnblind or args.tenPctUnblind) and args.allCuts:
        BDTLoop(mass,MassPoints[mass],unblindType)
        
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
