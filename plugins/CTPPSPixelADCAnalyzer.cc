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
#include "TH1D.h"
#include "TH2D.h"
#include "TProfile2D.h"
#include "TSystem.h"


#include <map>
#include <string>
#include <memory>
#include <algorithm>
#include <fstream>

//----------------------------------------------------------------------------------------------------

class CTPPSPixelADCAnalyzer : public edm::one::EDAnalyzer<> {
public:
  explicit CTPPSPixelADCAnalyzer(const edm::ParameterSet&);

  ~CTPPSPixelADCAnalyzer() override {}

private:
  void analyze(const edm::Event&, const edm::EventSetup&) override;
  void endJob() override;

  CTPPSPixelIndices thePixIndices;

  edm::EDGetTokenT<edm::DetSetVector<CTPPSPixelDigi>> digiToken_;

  std::string outputFile_;
  bool verbose_;
  unsigned int events_total_;
  std::vector<unsigned> enabled_RPs_;
  
  // Histograms to initialize
  std::map<unsigned,std::unique_ptr<TH2D>> h2HitMaps_;
  std::map<unsigned,std::unique_ptr<TProfile2D>> p2AvgADCMaps_;
  std::map<unsigned,std::map<unsigned,std::unique_ptr<TH1D>>> h1RocADC_;

	// Histograms not to initialize
  const int maxRows = 160;
  const int maxCols = 104;

  const std::vector<int> rocsInPlane_ = {0,1,4,5};

};

//----------------------------------------------------------------------------------------------------

CTPPSPixelADCAnalyzer::CTPPSPixelADCAnalyzer(const edm::ParameterSet& iConfig)
    : digiToken_(consumes<edm::DetSetVector<CTPPSPixelDigi>>(iConfig.getParameter<edm::InputTag>("tagDigis"))),
      outputFile_(iConfig.getParameter<std::string>("outputFile")),
      verbose_(iConfig.getParameter<bool>("verbose")),
      events_total_(0) {
  enabled_RPs_ = iConfig.getParameter<std::vector<unsigned>>("enabledRPs");
}

//----------------------------------------------------------------------------------------------------

void CTPPSPixelADCAnalyzer::analyze(const edm::Event& iEvent, const edm::EventSetup&) {
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
    if(h2HitMaps_.find(digi_id) == h2HitMaps_.end()){
        TString plot_tag = Form("Arm%i_St%i_Pln%i",digi_id.arm(),digi_id.station(),digi_id.plane());
        h2HitMaps_[digi_id] = std::make_unique<TH2D>("HitMap_"+plot_tag,"HitMap_"+plot_tag+";Column;Row",maxCols,0,maxCols,maxRows,0,maxRows);
        p2AvgADCMaps_[digi_id] = std::make_unique<TProfile2D>("AvgADCMap_"+plot_tag,"AvgADCMap_"+plot_tag+";Column;Row",maxCols,0,maxCols,maxRows,0,maxRows);
        for (const auto roc : rocsInPlane_){
          h1RocADC_[digi_id][roc] = std::make_unique<TH1D>("RocADC_"+plot_tag+"_Roc"+Form("%i",roc),"RocADC_"+plot_tag+"_Roc"+Form("%i",roc)+";ADC",255,0,255);
        }
    }

    for (const auto &digi : digi_ds.data){
        // Row/column in the module reference frame
        int mod_row = digi.row(); 
        int mod_col = digi.column();
        int adc = digi.adc();
        
        if(verbose_)
            edm::LogInfo("CTPPSPixelADCAnalyzer") << "Found digi in arm " << digi_id.arm() << 
          	  " station " << digi_id.station() << " plane " << digi_id.plane() << " col,row in the module RF: " << mod_col << "," << mod_row;

        h2HitMaps_[digi_id]->Fill(mod_col,mod_row);
        p2AvgADCMaps_[digi_id]->Fill(mod_col,mod_row,adc);
        
        // Get ROC number
        int roc_row,roc_col,roc = 0;
				if(thePixIndices.transformToROC(mod_col, mod_row, roc, roc_col, roc_row))
					edm::LogWarning("CTPPSPixelADCAnalyzer") << "Something went wrong when converting from module to roc coordinates";
        h1RocADC_[digi_id][roc]->Fill(adc);
    }
  }

  // update counters
  events_total_++;

}

//----------------------------------------------------------------------------------------------------

void CTPPSPixelADCAnalyzer::endJob() {
  auto f_out = std::make_unique<TFile>(outputFile_.c_str(), "recreate");

	// Create the necessary folders
  for(const auto &rp : enabled_RPs_){
    CTPPSPixelDetId rp_id(rp);
    TString folderName = Form("Arm%i_St%i",rp_id.arm(),rp_id.station());
    f_out->mkdir(folderName); 
  }

  for(const auto &idAndPlot : h2HitMaps_){
		CTPPSPixelDetId plane_id(idAndPlot.first);
		TString folderName = Form("Arm%i_St%i",plane_id.arm(),plane_id.station());
    TString plot_tag = Form("Arm%i_St%i_Pln%i",plane_id.arm(),plane_id.station(),plane_id.plane());

		f_out->cd(folderName);

		h2HitMaps_[plane_id]->Write();
    p2AvgADCMaps_[plane_id]->Write();

    for (const auto roc : rocsInPlane_)
      h1RocADC_[plane_id][roc]->Write();

  } // end of the loop over planes

	// Final report
	edm::LogInfo("CTPPSPixelADCAnalyzer")
		<< "CTPPSPixelADCAnalyzer report:\n" << "Events processed: " << events_total_ << std::endl;

}

//----------------------------------------------------------------------------------------------------

DEFINE_FWK_MODULE(CTPPSPixelADCAnalyzer);