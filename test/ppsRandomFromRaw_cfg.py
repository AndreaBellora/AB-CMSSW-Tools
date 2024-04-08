from Configuration.Eras.Modifier_ctpps_cff import ctpps
import sys
import os
import subprocess
import fnmatch
import FWCore.ParameterSet.Config as cms
import FWCore.ParameterSet.VarParsing as VarParsing

options = VarParsing.VarParsing('analysis')
options.maxEvents = -1  # -1 means all events

options.register('runs', [], VarParsing.VarParsing.multiplicity.list,
                 VarParsing.VarParsing.varType.int, "Run numbers")
options.register('dataset', '', VarParsing.VarParsing.multiplicity.singleton,
                 VarParsing.VarParsing.varType.string, "Dataset to process")
options.register('outputDir', '', VarParsing.VarParsing.multiplicity.singleton,
                 VarParsing.VarParsing.varType.string, "Output directory")
options.parseArguments()

if not os.path.exists(options.outputDir) and options.outputDir != '':
    os.makedirs(options.outputDir)

if options.runs == []:
    print("No run numbers provided. Please use the 'runs' option to specify the runs to be processed.")
    sys.exit(1)

# Dataset selection
run = options.runs[0]
query = f'dasgoclient --query="dataset dataset=/*/*/RAW run={run}"'
result = subprocess.run(query, shell=True, capture_output=True, env=os.environ)
datasets = []
if result.returncode != 0:
    print(f'Failed DAS query with return code {result.returncode}: {query}')
    print(f'Output: {result.stdout}')
    print(f'Error: {result.stderr}')
    sys.exit(1)
else:
    output = result.stdout.decode('utf-8').split('\n')
    while ("" in output):
        output.remove("")
    from pprint import pprint
    print(f'Found datasets for run {run}:')
    pprint(output)

    # Let the user choose the desired dataset, using the unix pattern matching
    if len(output) > 0:
        dataset_sel = ''
        if options.dataset != '':
            dataset_sel = options.dataset
        else:
            print('Please choose the desired datasets to be analyzed for all runs (comma separated, wildcards accepted):')
            dataset_sel = input()
        if ',' not in dataset_sel:
            dataset = dataset_sel
            if '*' not in dataset:
                datasets.append(dataset)
            else:
                # Do pattern matching
                for dt in output:
                    if fnmatch.fnmatch(dt, dataset):
                        datasets.append(dt)
        else:
            datasets_sel = [dt.rstrip().lstrip()
                            for dt in dataset_sel.split(',')]
            if not any('*' in dt for dt in datasets_sel):
                datasets = datasets_sel
            else:
                # Do pattern matching
                for dt in output:
                    for ds in datasets_sel:
                        if fnmatch.fnmatch(dt, ds):
                            datasets.append(dt)
    else:
        print('No datasets found for the specified run.')
        sys.exit(1)
    datasets = set(datasets)
    print('Chosen datasets:')
    pprint(datasets)

# Produce list of files
for run in options.runs:
    for dataset in datasets:
        query = f'dasgoclient --query="file dataset={dataset} run={run}"'
        result = subprocess.run(
            query, shell=True, capture_output=True, env=os.environ)
        if result.returncode != 0:
            print(
                f'Failed DAS query with return code {result.returncode}: {query}')
            print(f'Output: {result.stdout}')
            print(f'Error: {result.stderr}')
        else:
            output = result.stdout.decode('utf-8').split('\n')
            while ("" in output):
                output.remove("")
            if len(output) == 0:
                print(f'No files found for run {run}.')
            print(
                f'Found {len(output)} files for run {run} in dataset {dataset}.')
            options.inputFiles.extend(output)
print(f'Found {len(options.inputFiles)} files in total.')
print('File list:')
pprint(options.inputFiles)

process = cms.Process('ppsRandomFromRaw', ctpps)

# minimum of logs
process.MessageLogger = cms.Service("MessageLogger",
                                    statistics=cms.untracked.vstring(),
                                    destinations=cms.untracked.vstring("cout"),
                                    cout=cms.untracked.PSet(
                                        threshold=cms.untracked.string("INFO"),
                                        FwkReport=cms.untracked.PSet(
                                            optionalPSet=cms.untracked.bool(
                                                True),
                                            reportEvery=cms.untracked.int32(
                                                1000),
                                            limit=cms.untracked.int32(50000000)
                                        ),
                                    ),
                                    suppressInfo=cms.untracked.vstring(
                                        'ctppsPixelDigis')
                                    )

# Add process report
process.options = cms.untracked.PSet(
    wantSummary=cms.untracked.bool(True)
)

# load DQM framework
process.load("DQM.Integration.config.environment_cfi")
process.dqmEnv.subSystemFolder = "PPSRANDOM"
process.dqmSaver.path = options.outputDir+"/" if options.outputDir != '' else ''
print(f'Output directory: {process.dqmSaver.path}')
process.dqmSaver.tag = "PPSRANDOM"

# raw data source
process.source = cms.Source("PoolSource",
                            fileNames=cms.untracked.vstring(
                                options.inputFiles),
                            inputCommands=cms.untracked.vstring(
                                'drop *',
                                'keep FEDRawDataCollection_*_*_*'
                            )
                            )

process.maxEvents = cms.untracked.PSet(
    input=cms.untracked.int32(options.maxEvents)
)

# global tag - conditions for P5 cluster
process.load("DQM.Integration.config.FrontierCondition_GT_cfi")

# raw-to-digi conversion
process.load("EventFilter.CTPPSRawToDigi.ctppsRawToDigi_cff")

# CTPPS DQM modules
process.load("DQM.CTPPS.ctppsDQM_cff")
process.ctppsRandomDQMSource.tagRPixDigi = (
    'ctppsPixelDigis', '', 'ppsRandomFromRaw')

process.path = cms.Path(
    process.ctppsPixelDigis *
    process.ctppsDQMRandomSource *
    process.ctppsDQMRandomHarvest
)

process.end_path = cms.EndPath(
    process.dqmEnv +
    process.dqmSaver
)

process.schedule = cms.Schedule(
    process.path,
    process.end_path
)
