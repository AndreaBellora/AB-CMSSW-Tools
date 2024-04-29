#!/bin/bash
source /cvmfs/cms.cern.ch/cmsset_default.sh
cd /afs/cern.ch/user/a/abellora/workarea/Work/CT-PPS/Commissioning_2024/latencyAnalysis/CMSSW_14_0_1/src/RecoPPS/AB-CMSSW-Tools/test
cmsenv
python3 latencyAnalysis.py --debug --dataset /SpecialRandom0/Run2024A-v1/RAW,/SpecialRandom1/Run2024A-v1/RAW,/SpecialRandom2/Run2024A-v1/RAW,/SpecialRandom3/Run2024A-v1/RAW --inputDir highStatDQM