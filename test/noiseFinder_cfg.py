import FWCore.ParameterSet.Config as cms

from Configuration.StandardSequences.Eras import eras
process = cms.Process('ANALYSIS', eras.Run3)

# chose GT
from Configuration.AlCa.GlobalTag import GlobalTag
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
#  process.GlobalTag = GlobalTag(process.GlobalTag, "112X_dataRun2_v6")
process.GlobalTag = GlobalTag(process.GlobalTag, "123X_dataRun3_Prompt_v10")

# minimum of logs
process.MessageLogger = cms.Service("MessageLogger",
  statistics = cms.untracked.vstring(),
  destinations = cms.untracked.vstring("cout"),
  cout = cms.untracked.PSet(
    threshold = cms.untracked.string("INFO")
  )
)

# raw data source
process.source = cms.Source("PoolSource",
  fileNames = cms.untracked.vstring("file:/eos/project-c/ctpps/subsystems/Pixel/Commissioning_2022/Global/Run_353709/ALCAPPS_AOD.root"),
)

process.maxEvents = cms.untracked.PSet(
  input = cms.untracked.int32(15)
)

process.ctppsPixelNoiseFinder = cms.EDAnalyzer("CTPPSPixelNoiseFinder",
  tagDigis = cms.InputTag("ctppsPixelDigis"),
  outputFile = cms.string("NoiseAnalysis.root"),
  makeMasks = cms.bool(True),
  noiseThreshold = cms.double(0.00000000001),
  verbose = cms.bool(True),
# enabling 45-210, 45-220, 56-210, 56-220
  enabledRPs = cms.vuint32([2014838784,2023227392,2031616000,2040004608])
)

# processing sequences
process.path = cms.Path(
  process.ctppsPixelNoiseFinder
)

