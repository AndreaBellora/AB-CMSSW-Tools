import FWCore.ParameterSet.Config as cms

from Configuration.StandardSequences.Eras import eras
process = cms.Process('TEST', eras.Run3)
#process = cms.Process('TEST', eras.Run2_2018, eras.run2_miniAOD_devel)

from conditions import *

def SetConditions(process):
  # chose GT
  process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
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
process.MessageLogger = cms.Service("MessageLogger",
  statistics = cms.untracked.vstring(),
  destinations = cms.untracked.vstring("cout"),
  cout = cms.untracked.PSet(
    threshold = cms.untracked.string("WARNING")
  )
)

# raw data source

# streamer data source
process.source = cms.Source("NewEventStreamFileReader",
    fileNames = cms.untracked.vstring(
      # Beginning of 2023 data-taking
      # "file:/eos/project-c/ctpps/subsystems/Pixel/Commissioning_2023/MiniDAQ/run364748/run364748_ls0001_streamA_StorageManager.dat",
      # "file:/eos/project-c/ctpps/subsystems/Pixel/Commissioning_2023/MiniDAQ/run364748/run364748_ls0002_streamA_StorageManager.dat",
      # "file:/eos/project-c/ctpps/subsystems/Pixel/Commissioning_2023/MiniDAQ/run364748/run364748_ls0003_streamA_StorageManager.dat",
      # "file:/eos/project-c/ctpps/subsystems/Pixel/Commissioning_2023/MiniDAQ/run364748/run364748_ls0004_streamA_StorageManager.dat",
      # "file:/eos/project-c/ctpps/subsystems/Pixel/Commissioning_2023/MiniDAQ/run364748/run364748_ls0005_streamA_StorageManager.dat",
      # "file:/eos/project-c/ctpps/subsystems/Pixel/Commissioning_2023/MiniDAQ/run364748/run364748_ls0006_streamA_StorageManager.dat",
      # "file:/eos/project-c/ctpps/subsystems/Pixel/Commissioning_2023/MiniDAQ/run364748/run364748_ls0007_streamA_StorageManager.dat",
      # 07/06/2023 - 1 week before TS1
      "file:/eos/project-c/ctpps/subsystems/Pixel/Commissioning_2023/MiniDAQ/run368579/run368579_ls0001_streamA_StorageManager.dat",
      "file:/eos/project-c/ctpps/subsystems/Pixel/Commissioning_2023/MiniDAQ/run368579/run368579_ls0002_streamA_StorageManager.dat",
      "file:/eos/project-c/ctpps/subsystems/Pixel/Commissioning_2023/MiniDAQ/run368579/run368579_ls0003_streamA_StorageManager.dat",
      "file:/eos/project-c/ctpps/subsystems/Pixel/Commissioning_2023/MiniDAQ/run368579/run368579_ls0004_streamA_StorageManager.dat",
      "file:/eos/project-c/ctpps/subsystems/Pixel/Commissioning_2023/MiniDAQ/run368579/run368579_ls0005_streamA_StorageManager.dat",
      "file:/eos/project-c/ctpps/subsystems/Pixel/Commissioning_2023/MiniDAQ/run368579/run368579_ls0006_streamA_StorageManager.dat",
      "file:/eos/project-c/ctpps/subsystems/Pixel/Commissioning_2023/MiniDAQ/run368579/run368579_ls0007_streamA_StorageManager.dat",
      "file:/eos/project-c/ctpps/subsystems/Pixel/Commissioning_2023/MiniDAQ/run368579/run368579_ls0008_streamA_StorageManager.dat",
    ),
    inputFileTransitionsEachEvent = cms.untracked.bool(True)
    #firstEvent = cms.untracked.uint64(10123456835)
)

process.raw = cms.EDAnalyzer("StreamThingAnalyzer",
    product_to_get = cms.string('m1')
)


process.maxEvents = cms.untracked.PSet(
  input = cms.untracked.int32(1000000)
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

# Activate when analyzing ALCAPPS dataset
# process.ctppsPixelDigis.inputLabel = cms.InputTag("hltPPSCalibrationRaw")
# process.ctppsDiamondRawToDigi.rawDataTag = cms.InputTag("hltPPSCalibrationRaw")
# process.totemRPRawToDigi.rawDataTag = cms.InputTag("hltPPSCalibrationRaw")

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
