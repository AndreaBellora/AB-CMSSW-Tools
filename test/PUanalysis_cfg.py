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

import FWCore.ParameterSet.VarParsing as VarParsing
options = VarParsing.VarParsing ()
options.register('sourceFileList',
                '',
                VarParsing.VarParsing.multiplicity.singleton,
                VarParsing.VarParsing.varType.string,
                "source file list name")
options.parseArguments()

if options.sourceFileList != '':
    import FWCore.Utilities.FileUtils as FileUtils
    fileList = FileUtils.loadListFromFile(options.sourceFileList) 
    inputFiles = cms.untracked.vstring(*fileList)
else:
    inputFiles = cms.untracked.vstring(" ")
    
# raw data source
process.source = cms.Source("PoolSource",
  fileNames = inputFiles,
  inputCommands = cms.untracked.vstring(
    'keep *',
    # 'keep *_ctppsPixelDigis_*_*',
    # 'keep *_offlinePrimaryVertices_*_*',
  )
)

process.maxEvents = cms.untracked.PSet(
  input = cms.untracked.int32(1000000)
)

process.PUAnalysis = cms.EDAnalyzer("PUAnalyzer",
  tagPPSPixeldigi = cms.untracked.InputTag("ctppsPixelDigis"),
  tagRecoVertex = cms.untracked.InputTag("offlinePrimaryVertices"),
  outputFileName = cms.untracked.string("PUAnalysis.root"),
)

# processing sequences
process.path = cms.Path(
  process.PUAnalysis
)

