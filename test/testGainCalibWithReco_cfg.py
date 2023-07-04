# Basic test to check that the reconstruction does not fail

import FWCore.ParameterSet.Config as cms

from Configuration.StandardSequences.Eras import eras
process = cms.Process('TESTGAIN', eras.Run3)
#process = cms.Process('TEST', eras.Run2_2018, eras.run2_miniAOD_devel)

from conditions import *

def SetConditions(process):
  # chose GT
  process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
#  process.GlobalTag = GlobalTag(process.GlobalTag, "112X_dataRun2_v6")
  process.GlobalTag = GlobalTag(process.GlobalTag, "130X_dataRun3_Prompt_v1")

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
process.load("FWCore.MessageService.MessageLogger_cfi")
process.MessageLogger.cerr.enable = False
process.MessageLogger.cout.enable = True
process.MessageLogger.cout.statisticsThreshold = 'WARNING'
process.MessageLogger.cout.threshold = 'WARNING'
process.MessageLogger.cout.enableStatistics = True

# raw data source
process.source = cms.Source("PoolSource",
  fileNames = cms.untracked.vstring(
    # "file:/afs/cern.ch/work/a/abellora/Work/CT-PPS/Commissioning_2023/maskNoise/CMSSW_13_0_0/src/RecoPPS/AB-CMSSW-Tools/test/PPS_AOD_run364740.root"
    "/store/data/Run2023C/ZeroBias/RAW/v1/000/369/596/00000/abbfa3c0-2414-4dd3-9e89-8f2e22b1fd8e.root"
    ),
)

process.maxEvents = cms.untracked.PSet(
  input = cms.untracked.int32(10000)
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

process.GlobalTag.toGet = cms.VPSet(
  cms.PSet(record = cms.string("CTPPSPixelGainCalibrationsRcd"),
    tag = cms.string("CTPPSPixelGainCalibrations_test"),
    connect = cms.string("sqlite_file:/afs/cern.ch/work/a/abellora/Work/CT-PPS/Commissioning_2023/GainCalibrationsToDB/CMSSW_13_0_0/src/ctppsgains_test_postTS1.db")
  )
)

# Activate when analyzing ALCAPPS dataset
# process.ctppsPixelDigis.inputLabel = cms.InputTag("hltPPSCalibrationRaw")
# process.ctppsDiamondRawToDigi.rawDataTag = cms.InputTag("hltPPSCalibrationRaw")
# process.totemRPRawToDigi.rawDataTag = cms.InputTag("hltPPSCalibrationRaw")
# process.totemTimingRawToDigi.rawDataTag = cms.InputTag("hltPPSCalibrationRaw")

process.output = cms.OutputModule("PoolOutputModule",
    fileName = cms.untracked.string('PPS_AOD.root'),
    outputCommands = cms.untracked.vstring("keep *")
)

# processing sequences
process.path = cms.Path(
  process.ctppsRawToDigi
  * process.recoCTPPS
)

process.end_path = cms.EndPath(
  process.output
)
