/****************************************************************************
 *
 * This is a part of CTPPS tracker software
 * Author:
 *   Andrea Bellora
 *
 ****************************************************************************/

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/one/EDAnalyzer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "DataFormats/Common/interface/DetSetVector.h"
#include "DataFormats/CTPPSDetId/interface/CTPPSPixelDetId.h"

#include "CondFormats/PPSObjects/interface/CTPPSPixelIndices.h"
#include "DataFormats/CTPPSDetId/interface/CTPPSDetId.h"
#include "DataFormats/CTPPSDigi/interface/CTPPSPixelDigi.h"

#include "TFile.h"
#include "TH2D.h"
#include "TSystem.h"


#include <map>
#include <string>
#include <memory>
#include <algorithm>
#include <fstream>

//----------------------------------------------------------------------------------------------------

class CTPPSPixelNoiseFinder : public edm::one::EDAnalyzer<> {
public:
  explicit CTPPSPixelNoiseFinder(const edm::ParameterSet&);

  ~CTPPSPixelNoiseFinder() override {}

private:
  void analyze(const edm::Event&, const edm::EventSetup&) override;
  void endJob() override;

  CTPPSPixelIndices thePixIndices;

  edm::EDGetTokenT<edm::DetSetVector<CTPPSPixelDigi>> digiToken_;

  std::string outputFile_;
  bool makeMasks_;
  double noiseThreshold_;
  bool verbose_;
  unsigned int events_total_;
  std::vector<unsigned> enabled_RPs_;
  std::map<unsigned,int> noisyPixels_;
  
  // Histograms to initialize
	std::map<unsigned,std::unique_ptr<TH2D>> hitMaps_;
  std::map<unsigned,std::unique_ptr<TH2D>> masks_;

	// Histograms not to initialize
  std::map<unsigned,std::unique_ptr<TH2D>> occupancy_;

  const int maxRows = 160;
  const int maxCols = 104;
  std::map<unsigned,int> rocsInPlane_;

};

//----------------------------------------------------------------------------------------------------

CTPPSPixelNoiseFinder::CTPPSPixelNoiseFinder(const edm::ParameterSet& iConfig)
    : digiToken_(consumes<edm::DetSetVector<CTPPSPixelDigi>>(iConfig.getParameter<edm::InputTag>("tagDigis"))),
      outputFile_(iConfig.getParameter<std::string>("outputFile")),
      makeMasks_(iConfig.getParameter<bool>("makeMasks")),
      noiseThreshold_(iConfig.getParameter<double>("noiseThreshold")),
      verbose_(iConfig.getParameter<bool>("verbose")),
      events_total_(0) {
  enabled_RPs_ = iConfig.getParameter<std::vector<unsigned>>("enabledRPs");
}

//----------------------------------------------------------------------------------------------------

void CTPPSPixelNoiseFinder::analyze(const edm::Event& iEvent, const edm::EventSetup&) {
  // get input
  edm::Handle<edm::DetSetVector<CTPPSPixelDigi>> digis;
  iEvent.getByToken(digiToken_, digis);

  // process digis
  for (const auto &digi_ds : *digis){
    auto digi_id = CTPPSPixelDetId(digi_ds.id);

    // The RP id of any plane corresponds to the one of plane 0
    auto digi_rpId = digi_id;
    digi_rpId.setPlane(0);
    
    // Skip RPs not to be analyzed 
    if(std::find(enabled_RPs_.begin(), enabled_RPs_.end(),digi_rpId) == enabled_RPs_.end())
        continue;
    
    // Initialize plots if not yet done
    if(hitMaps_.find(digi_id) == hitMaps_.end()){
        TString plot_tag = Form("Arm%i_St%i_Pln%i",digi_id.arm(),digi_id.station(),digi_id.plane());
        hitMaps_[digi_id] = std::make_unique<TH2D>("HitMap_"+plot_tag,"HitMap_"+plot_tag+";Column;Row",maxCols,0,maxCols,maxRows,0,maxRows);
        masks_[digi_id] = std::make_unique<TH2D>("Mask_"+plot_tag,"Mask_"+plot_tag+";Column;Row",maxCols,0,maxCols,maxRows,0,maxRows);
    }

    for (const auto &digi : digi_ds.data){
        // Row/column in the module reference frame
        int mod_row = digi.row(); 
        int mod_col = digi.column();
        
        if(verbose_)
            edm::LogInfo("CTPPSPixelNoiseFinder") << "Found digi in arm " << digi_id.arm() << 
          	  " station " << digi_id.station() << " plane " << digi_id.plane() << " col,row in the module RF: " << mod_col << "," << mod_row;

        hitMaps_[digi_id]->Fill(mod_col,mod_row);        
    }

  }

  // update counters
  events_total_++;

}

//----------------------------------------------------------------------------------------------------

void CTPPSPixelNoiseFinder::endJob() {
  auto f_out = std::make_unique<TFile>(outputFile_.c_str(), "recreate");

	// Create the necessary folders
  for(const auto &rp : enabled_RPs_){
    CTPPSPixelDetId rp_id(rp);
    TString folderName = Form("Arm%i_St%i",rp_id.arm(),rp_id.station());
    f_out->mkdir(folderName); 
  }

  for(const auto &idAndPlot : hitMaps_){
		CTPPSPixelDetId plane_id(idAndPlot.first);
		TString folderName = Form("Arm%i_St%i",plane_id.arm(),plane_id.station());
    TString plot_tag = Form("Arm%i_St%i_Pln%i",plane_id.arm(),plane_id.station(),plane_id.plane());

		f_out->cd(folderName);

		hitMaps_[plane_id]->Write();

		// Generate and write occupancy plot
		occupancy_[plane_id] = std::make_unique<TH2D>(*hitMaps_[plane_id]);
		occupancy_[plane_id]->SetNameTitle("Occupancy_"+plot_tag,"Occupancy_"+plot_tag+";Column;Row");
		occupancy_[plane_id]->Scale(1./events_total_);
		occupancy_[plane_id]->Write();

		// Compute the mask to apply - this assumes no mask was used during data-taking
		for(auto mod_col = 0; mod_col < maxCols; mod_col++){
			for(auto mod_row = 0; mod_row < maxRows; mod_row++){
				int x_bin = mod_col + 1;
				int y_bin = mod_row + 1;
				if(occupancy_[plane_id]->GetBinContent(x_bin,y_bin) > noiseThreshold_){
					if (verbose_)
						edm::LogInfo("CTPPSPixelNoiseFinder") << "Found noisy pixel in arm " << plane_id.arm() << 
							" station " << plane_id.station() << " plane " << plane_id.plane() << " col,row in the module RF: " << mod_col << "," 
							<< mod_row << ". Occupancy = " << occupancy_[plane_id]->GetBinContent(x_bin,y_bin);
					masks_[plane_id]->SetBinContent(x_bin,y_bin,0);
					if(noisyPixels_.find(plane_id) == noisyPixels_.end())
						noisyPixels_[plane_id] = 1;
					else
						noisyPixels_[plane_id]++;
				} else {
					masks_[plane_id]->SetBinContent(x_bin,y_bin,1);
				}
			}
		}
		masks_[plane_id]->Write();

		
		// Arrange data in a format easy to produce files
		// Data format rocMasks[roc_index][roc_col][roc_row] = masked?
		std::map<int,std::map<int,std::map<int,bool>>> rocMasks;
		
		for(auto mod_col = 0; mod_col < maxCols; mod_col++){
			for(auto mod_row = 0; mod_row < maxRows; mod_row++){
				int x_bin = mod_col + 1;
				int y_bin = mod_row + 1;
				bool masked = !masks_[plane_id]->GetBinContent(x_bin,y_bin);

				// Compute row/column in the roc reference frame and roc index
				int roc_row,roc_col,roc;
				if(thePixIndices.transformToROC(mod_col, mod_row, roc, roc_col, roc_row))
					edm::LogWarning("CTPPSPixelNoiseFinder") << "Something went wrong when converting from module to roc coordinates";

				rocMasks[roc][roc_col][roc_row] = masked;
			}
		}

		if(!makeMasks_)
			continue;
		
		// Translate names for POS notation
		int sector;
		TString rp;
		if(plane_id.arm() == 0){
			sector = 45;
			if(plane_id.station() == 0)
				rp = "003";
			else
				rp = "023";
		} else {
			sector = 56;
			if(plane_id.station() == 0)
				rp = "103";
			else
				rp = "123";
		}
		// Create mask files
		gSystem->Exec("mkdir -p newMasks");
		TString maskFileName = Form("newMasks/ROC_Masks_module_CTPPS_SEC%i_RP%s_PLN%i.dat",sector,rp.Data(),plane_id.plane());
		std::ofstream maskFile(maskFileName.Data(),std::ofstream::out);
		for(auto roc = 0; roc < 6; roc++){
			if(rocMasks.find(roc) == rocMasks.end())
				continue;
			TString rocName = Form("CTPPS_SEC%i_RP%s_PLN%i_ROC%i",sector,rp.Data(),plane_id.plane(),roc);
			maskFile << "ROC:     " << rocName << std::endl;

			// Hard-coding maximum row and column - this really can't vary
			for(auto col = 0; col < 52; col++){
				TString colName = Form("col%02d:",col);
				maskFile << colName << "   ";
				for(auto row = 0; row < 80; row++){
					if(rocMasks[roc][col][row])
						maskFile << "0";
					else
						maskFile << "1";
				}
				maskFile << std::endl;
			}
		}
		maskFile.close();

  } // end of the loop over planes

	// Give the noise report
	TString noiseReport;
	int totalNoisy = 0;
	for(const auto &planeAndNoise : noisyPixels_){
		CTPPSPixelDetId plane_id(planeAndNoise.first);
		int noise = planeAndNoise.second;
		double noise_frac = double(noise*100) / (maxRows * maxCols);
		totalNoisy += noise;
		noiseReport += Form("Arm%i_St%i_Pln%i: %i noisy pixels found (%.3f %% of the detector plane)\n",plane_id.arm(),plane_id.station(),plane_id.plane(),noise,noise_frac);
	}
	noiseReport += Form("TOTAL: %i noisy pixels (%.3f %%)",totalNoisy,double(totalNoisy*100)/(maxRows*maxCols*noisyPixels_.size()));
	noiseReport += "\nNew mask files are available in the 'newMasks' directory";
	edm::LogInfo("CTPPSPixelNoiseFinder")
		<< "CTPPSPixelNoiseFinder report:\n" << "Events processed: " << events_total_ << "\n" << noiseReport;

}

//----------------------------------------------------------------------------------------------------

DEFINE_FWK_MODULE(CTPPSPixelNoiseFinder);