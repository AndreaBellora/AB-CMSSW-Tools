import FWCore.ParameterSet.Config as cms

from Configuration.StandardSequences.Eras import eras
process = cms.Process('TESTDQM', eras.Run3)
#process = cms.Process('TEST', eras.Run2_2018, eras.run2_miniAOD_devel)

from conditions import *

def SetConditions(process):
  # chose GT
  process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
#  process.GlobalTag = GlobalTag(process.GlobalTag, "112X_dataRun2_v6")
  process.GlobalTag = GlobalTag(process.GlobalTag, "auto:run3_data")

  # chose LHCInfo
  UseLHCInfoGT(process)
  #UseLHCInfoLocal(process)
  #UseLHCInfoDB(process, "frontier://FrontierProd/CMS_CONDITIONS", "LHCInfoEndFill_prompt_v2")

  # chose alignment
  UseAlignmentGT(process)
  #UseAlignmentLocal(process)
  #UseAlignmentFile(process, "sqlite_file:/afs/cern.ch/user/c/cmora/public/CTPPSDB/AlignmentSQlite/CTPPSRPRealAlignment_v13Jun19_v1.db", "PPSRPRealAlignment_v13Jun19")
  #UseAlignmentDB(process, "frontier://FrontierProd/CMS_CONDITIONS", "CTPPSRPAlignment_real_offline_v7")

  # chose optics
  UseOpticsGT(process)
  #UseOpticsLocal(process)
  #UseOpticsFile(process, "sqlite_file:/afs/cern.ch/user/w/wcarvalh/public/CTPPS/optical_functions/PPSOpticalFunctions_2016-2018_v9.db", "PPSOpticalFunctions_test")
  #UseOpticsDB(process, "frontier://FrontierProd/CMS_CONDITIONS", "PPSOpticalFunctions_offline_v6")

# minimum of logs
process.MessageLogger = cms.Service("MessageLogger",
  statistics = cms.untracked.vstring(),
  destinations = cms.untracked.vstring("cout"),
  cout = cms.untracked.PSet(
    threshold = cms.untracked.string("WARNING")
  )
)

# raw data source
process.source = cms.Source("PoolSource",
  fileNames = cms.untracked.vstring("file:/eos/project-c/ctpps/subsystems/Pixel/Commissioning_2022/Global/Run_352929/PPS_AOD.root"),
  inputCommands = cms.untracked.vstring(
    'keep *',
  )
)

process.maxEvents = cms.untracked.PSet(
  input = cms.untracked.int32(-1)
)

# load default alignment settings
process.load("CalibPPS.ESProducers.ctppsAlignment_cff")

# raw-to-digi conversion
process.load("EventFilter.CTPPSRawToDigi.ctppsRawToDigi_cff")

# local RP reconstruction chain with standard settings
process.load("RecoPPS.Configuration.recoCTPPS_cff")

# define conditions
SetConditions(process)
CheckConditions()

## load DQM framework
process.load("DQM.Integration.config.environment_cfi")
process.dqmEnv.subSystemFolder = "CTPPS"
process.dqmEnv.eventInfoFolder = "EventInfo"
process.dqmSaver.path = ""
process.dqmSaver.tag = "CTPPS"

## CTPPS DQM modules
process.load("DQM.CTPPS.ctppsDQM_cff")

# RP ids
rpIds = cms.PSet(
  rp_45_F = cms.uint32(23),
  rp_45_N = cms.uint32(3),
  rp_56_N = cms.uint32(103),
  rp_56_F = cms.uint32(123)
)

# track distribution plotter
process.ctppsTrackDistributionPlotter = cms.EDAnalyzer("CTPPSTrackDistributionPlotter",
  tagTracks = cms.InputTag("ctppsLocalTrackLiteProducer"),

  rpId_45_F = rpIds.rp_45_F,
  rpId_45_N = rpIds.rp_45_N,
  rpId_56_N = rpIds.rp_56_N,
  rpId_56_F = rpIds.rp_56_F,

  outputFile = cms.string("PPS_tracks.root")
)
# processing sequences
process.path = cms.Path(

 process.ctppsTrackDistributionPlotter
 * process.ctppsDQMOnlineSource
 * process.ctppsDQMOnlineHarvest
)

process.end_path = cms.EndPath(
 process.dqmEnv +
 process.dqmSaver
)
