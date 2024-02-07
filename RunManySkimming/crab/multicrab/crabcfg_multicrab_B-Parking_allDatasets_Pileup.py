#!/usr/bin/env python
import os
from optparse import OptionParser
import CRABClient

from CRABAPI.RawCommand import crabCommand
from CRABClient.ClientExceptions import ClientException
from httplib import HTTPException
def getOptions():
    """
    Parse and return the arguments provided by the user.
    """
    usage = ("Usage: %prog --crabCmd CMD [--workArea WAD --crabCmdOpts OPTS]"
             "\nThe multicrab command executes 'crab CMD OPTS' for each project directory contained in WAD"
             "\nUse multicrab -h for help")

    parser = OptionParser(usage=usage)

    parser.add_option('-c', '--crabCmd',
                      dest = 'crabCmd',
                      default = '',
                      help = "crab command",
                      metavar = 'CMD')

    parser.add_option('-w', '--workArea',
                      dest = 'workArea',
                      default = '',
                      help = "work area directory (only if CMD != 'submit')",
                      metavar = 'WAD')

    parser.add_option('-o', '--crabCmdOpts',
                      dest = 'crabCmdOpts',
                      default = '',
                      help = "options for crab command CMD",
                      metavar = 'OPTS')

    (options, arguments) = parser.parse_args()

    if arguments:
        parser.error("Found positional argument(s): %s." % (arguments))
    if not options.crabCmd:
        parser.error("(-c CMD, --crabCmd=CMD) option not provided.")
    if options.crabCmd != 'submit':
        if not options.workArea:
            parser.error("(-w WAR, --workArea=WAR) option not provided.")
        if not os.path.isdir(options.workArea):
            parser.error("'%s' is not a valid directory." % (options.workArea))

    return options
def main():
    options = getOptions()
    if options.crabCmd == 'submit':
        from CRABClient.UserUtilities import config
        trial = "B"
        config = config()
        
        pyCfgParams = ['isData=True']
        
        #config.General.requestName = 'SexaQ_SingleMuon'
        #config.General.workArea = 'crab_projects'
        config.section_('General')
        config.General.transferOutputs = True
        config.General.transferLogs = True
        config.General.workArea = 'crab_2018BPH_Pileup_trial'+trial
        
        config.section_('JobType') 
        config.JobType.pluginName = 'Analysis'
        config.JobType.psetName = '../PileUpScraper_cfg_data.py'
        
        config.section_('Data') 
        #config.Data.inputDataset = '/SingleMuon/Run2016G-23Sep2016-v1/AOD'
        config.Data.inputDBS = 'global'
        config.Data.partialDataset = True
        config.Data.unitsPerJob = 20
        #config.Data.lumiMask = 'https://cms-service-dqm.web.cern.ch/cms-service-dqm/CAF/certification/Collisions17/13TeV/ReReco/Cert_294927-306462_13TeV_EOY2017ReReco_Collisions17_JSON.txt'
        lumimaskdir = "processedLumis_trial" + trial + "/"
        #config.Data.runRange = ''
        config.Data.outLFNDirBase = '/store/user/wvetens/data_Sexaq/PileupInfo/trial'+trial
        config.Data.publication = False
        config.Data.outputDatasetTag = 'allSlices_2018BPH_Pileup_multicrab'
        config.Data.splitting = 'LumiBased'
        
        config.section_('Site') 
        config.Site.whitelist = ['T2*','T1*']
        config.Site.storageSite = 'T2_US_Wisconsin'
        inputDatasets = [
                        '/ParkingBPH1/Run2018A-UL2018_MiniAODv2-v1/MINIAOD',
                        '/ParkingBPH2/Run2018A-UL2018_MiniAODv2-v1/MINIAOD',
                        '/ParkingBPH3/Run2018A-UL2018_MiniAODv2-v1/MINIAOD',
                        '/ParkingBPH4/Run2018A-UL2018_MiniAODv2-v1/MINIAOD',
                        '/ParkingBPH5/Run2018A-UL2018_MiniAODv2-v1/MINIAOD',
                        '/ParkingBPH6/Run2018A-UL2018_MiniAODv2-v1/MINIAOD',
                        '/ParkingBPH1/Run2018B-UL2018_MiniAODv2-v1/MINIAOD',
                        '/ParkingBPH2/Run2018B-UL2018_MiniAODv2-v1/MINIAOD',
                        '/ParkingBPH3/Run2018B-UL2018_MiniAODv2-v1/MINIAOD',
                        '/ParkingBPH4/Run2018B-UL2018_MiniAODv2-v1/MINIAOD',
                        '/ParkingBPH5/Run2018B-UL2018_MiniAODv2-v1/MINIAOD',
                        '/ParkingBPH6/Run2018B-UL2018_MiniAODv2-v1/MINIAOD',
                        '/ParkingBPH1/Run2018C-UL2018_MiniAODv2-v1/MINIAOD',
                        '/ParkingBPH2/Run2018C-UL2018_MiniAODv2-v1/MINIAOD',
                        '/ParkingBPH3/Run2018C-UL2018_MiniAODv2-v1/MINIAOD',
                        '/ParkingBPH4/Run2018C-UL2018_MiniAODv2-v1/MINIAOD',
                        '/ParkingBPH5/Run2018C-UL2018_MiniAODv2-v1/MINIAOD',
                        '/ParkingBPH1/Run2018D-UL2018_MiniAODv2-v1/MINIAOD',
                        '/ParkingBPH2/Run2018D-UL2018_MiniAODv2-v1/MINIAOD',
                        '/ParkingBPH3/Run2018D-UL2018_MiniAODv2-v1/MINIAOD',
                        '/ParkingBPH4/Run2018D-UL2018_MiniAODv2-v1/MINIAOD',
                        '/ParkingBPH5/Run2018D-UL2018_MiniAODv2-v1/MINIAOD'
                        ]

        for inDS in inputDatasets:
        
            # inDS is of the form /A/B/C. Since B is unique for each inDS, use this in the CRAB request name.
            Remove = '-UL2018_MiniAODv2-v1'
            RunTag = inDS.split('/')[2].replace(Remove,'')
            config.Data.lumiMask = lumimaskdir + "processedLumis_" + inDS.split('/')[1] + '_' + RunTag + '.json'
            config.General.requestName = inDS.split('/')[1] + '_' + inDS.split('/')[2] + '_PVinfo_trial' + trial
            config.Data.inputDataset = inDS
            config.Data.outputDatasetTag = '%s_%s' % (config.General.workArea, config.General.requestName)
            # Submit.
            try:
                print "Submitting for input dataset %s" % (inDS)
                crabCommand(options.crabCmd, config = config, *options.crabCmdOpts.split())
            except HTTPException as hte:
                print "Submission for input dataset %s failed - HTTP Exception: %s" % (inDS, hte.headers)
            except ClientException as cle:
                print "Submission for input dataset %s failed - Client Exception: %s" % (inDS, cle)

    # All other commands can be simply executed.
    elif options.workArea:

        for dir in os.listdir(options.workArea):
            projDir = os.path.join(options.workArea, dir)
            if not os.path.isdir(projDir):
                continue
            # Execute the crab command.
            msg = "Executing (the equivalent of): crab %s --dir %s %s" % (options.crabCmd, projDir, options.crabCmdOpts)
            print "-"*len(msg)
            print msg
            print "-"*len(msg)
            try:
                crabCommand(options.crabCmd, dir = projDir, *options.crabCmdOpts.split())
            except HTTPException as hte:
                print "Failed executing command %s for task %s: %s" % (options.crabCmd, projDir, hte.headers)
            except ClientException as cle:
                print "Failed executing command %s for task %s: %s" % (options.crabCmd, projDir, cle)

if __name__ == '__main__':
    main()
