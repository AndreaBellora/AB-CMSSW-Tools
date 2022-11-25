runNumber = 354330

from CRABClient.UserUtilities import config
config = config()

config.General.requestName = 'ZeroBias0_Run'+str(runNumber)
config.General.transferOutputs = True
config.General.transferLogs = True

config.JobType.pluginName = 'analysis'
config.JobType.psetName = 'myReco_cfg.py'
config.JobType.inputFiles = ['conditions.py']
config.JobType.allowUndistributedCMSSW = True

config.Data.inputDataset = "/ZeroBias0/Run2022A-v1/RAW"
config.Data.runRange = str(runNumber)

config.Data.inputDBS = 'global'

config.Data.splitting = 'Automatic'                                                                                             
# config.Data.splitting = 'FileBased'
# config.Data.unitsPerJob = 5

# If you want, you can mask with a JSON here, instead of using config.Data.runRange
config.Data.inputDBS = 'global'
# config.Data.lumiMask = '/eos/project/c/ctpps/Operations/DataExternalConditions/2018/CMSgolden_2RPGood_anyarms_EraB1.json'

config.Data.outLFNDirBase = '/store/group/dpg_ctpps/comm_ctpps/Commissioning_2022'
config.Data.publication = False
config.Data.outputDatasetTag = 'ZeroBias_Run'+str(runNumber)

config.Site.storageSite = 'T2_CH_CERN'

# config.Site.blacklist = ['T1_US_FNAL']