# AB-CMSSW-Tools
My tools for CMSSW (reco, noise masking, CRAB etc..)

## Installation (on lxplus)

```bash
CMSSW_version=CMSSW_13_0_0
cmsrel $CMSSW_version
cd $CMSSW_version/src
cmsenv
git cms-addpkg RecoPPS
cd RecoPPS
git clone git@github.com:AndreaBellora/AB-CMSSW-Tools.git -b $CMSSW_version
cd ..
scram b -j10
```
