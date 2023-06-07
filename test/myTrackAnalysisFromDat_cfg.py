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

# streamer data source
process.source = cms.Source("NewEventStreamFileReader",
    fileNames = cms.untracked.vstring(
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0001_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0002_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0003_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0004_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0005_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0006_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0007_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0008_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0009_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0010_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0011_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0012_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0013_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0014_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0015_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0016_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0017_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0018_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0019_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0020_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0021_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0022_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0023_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0024_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0025_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0026_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0027_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0028_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0029_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0030_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0031_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0032_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0033_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0034_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0035_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0036_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0037_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0038_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0039_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0040_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0041_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0042_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0043_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0044_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0045_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0046_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0047_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0048_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0049_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0050_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0051_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0052_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0053_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0054_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0055_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0056_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0057_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0058_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0059_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0060_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0061_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0062_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0063_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0064_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0065_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0066_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0067_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0068_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0069_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0070_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0071_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0072_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0073_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0074_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0075_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0076_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0077_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0078_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0079_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0080_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0081_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0082_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0083_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0084_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0085_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0086_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0087_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0088_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0089_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0090_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0091_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0092_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0093_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0094_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0095_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0096_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0097_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0098_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0099_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0100_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0101_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0102_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0103_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0104_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0105_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0106_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0107_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0108_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0109_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0110_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0111_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0112_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0113_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0114_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0115_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0116_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0117_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0118_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0119_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0120_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0121_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0122_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0123_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0124_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0125_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0126_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0127_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0128_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0129_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0130_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0131_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0132_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0133_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0134_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0135_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0136_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0137_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0138_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0139_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0140_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0141_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0142_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0143_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0144_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0145_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0146_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0147_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0148_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0149_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0150_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0151_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0152_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0153_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0154_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0155_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0156_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0157_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0158_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0159_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0160_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0161_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0162_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0163_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0164_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0165_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0166_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0167_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0168_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0169_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0170_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0171_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0172_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0173_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0174_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0175_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0176_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0177_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0178_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0179_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0180_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0181_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0182_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0183_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0184_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0185_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0186_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0187_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0188_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0189_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0190_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0191_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0192_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0193_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0194_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0195_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0196_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0197_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0198_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0199_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0200_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0201_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0202_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0203_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0204_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0205_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0206_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0207_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0208_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0209_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0210_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0211_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0212_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0213_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0214_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0215_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0216_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0217_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0218_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0219_streamALCAPPSPrompt_StorageManager.dat",
      "file:/eos/cms/store/t0streamer/Data/ALCAPPSPrompt/000/366/186/run366186_ls0220_streamALCAPPSPrompt_StorageManager.dat",
    ),
    inputFileTransitionsEachEvent = cms.untracked.bool(True)
    #firstEvent = cms.untracked.uint64(10123456835)
)

process.raw = cms.EDAnalyzer("StreamThingAnalyzer",
    product_to_get = cms.string('m1')
)


# Activate when analyzing ALCAPPS dataset
process.ctppsPixelDigis.inputLabel = cms.InputTag("hltPPSCalibrationRaw")
process.ctppsDiamondRawToDigi.rawDataTag = cms.InputTag("hltPPSCalibrationRaw")
process.totemRPRawToDigi.rawDataTag = cms.InputTag("hltPPSCalibrationRaw")
process.totemTimingRawToDigi.rawDataTag = cms.InputTag("hltPPSCalibrationRaw")

process.trackAnalysis = cms.EDAnalyzer("CTPPSPixelTrackAnalyzer",
  tagPPSPixelDigi = cms.untracked.InputTag("ctppsPixelDigis"),
  tagPPSPixelRecHit = cms.untracked.InputTag("ctppsPixelRecHits"),
  tagPPSPixelLocalTrack = cms.untracked.InputTag("ctppsPixelLocalTracks"),
)

process.TFileService = cms.Service("TFileService", 
      fileName = cms.string("trackAnalysis.root"),
      closeFileFast = cms.untracked.bool(True)
)

process.output = cms.OutputModule("PoolOutputModule",
    fileName = cms.untracked.string('PPS_AOD_366186.root'),
    outputCommands = cms.untracked.vstring("keep *")
)

# processing sequences
process.path = cms.Path(
  process.raw
  * process.ctppsRawToDigi
  * process.recoCTPPS
  * process.trackAnalysis
)

process.end_path = cms.EndPath(
  process.output
)