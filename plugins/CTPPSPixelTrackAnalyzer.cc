// Original Author:  Andrea Bellora
//         Created:  Wed, 21 Dec 2022 10:33:05 GMT
//
//

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/one/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "DataFormats/Common/interface/DetSetVector.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "DataFormats/CTPPSDetId/interface/CTPPSPixelDetId.h"
#include "DataFormats/CTPPSDigi/interface/CTPPSPixelDigi.h"
#include "DataFormats/CTPPSReco/interface/CTPPSPixelLocalTrack.h"

#include "TH1D.h"
#include "TH2D.h"
#include "TString.h"

#include <string>
#include <vector>
#include <map>
#include <memory>


using namespace std;
using namespace edm;

class CTPPSPixelTrackAnalyzer : public edm::one::EDAnalyzer<edm::one::SharedResources> {
public:
  explicit CTPPSPixelTrackAnalyzer(const edm::ParameterSet &);
  inline ~CTPPSPixelTrackAnalyzer() {};
  static void fillDescriptions(edm::ConfigurationDescriptions &descriptions);

private:
  virtual void beginJob() override;
  virtual void analyze(const edm::Event &, const edm::EventSetup &) override;
  virtual void endJob() override;


  // Data to get
  edm::EDGetTokenT<edm::DetSetVector<CTPPSPixelDigi>> ppsPixelDigiToken_;
  edm::EDGetTokenT<edm::DetSetVector<CTPPSPixelLocalTrack>> ppsPixelLocalTrackToken_;

  // Hard-coded configs
  vector<uint32_t> arms_ = {0, 1};
  vector<uint32_t> stations_ = {0, 2};
  vector<uint32_t> planes_ = {0, 1, 2, 3, 4, 5};

  // Declare hists
  map<CTPPSPixelDetId,TH2D*> h2PlContVsNPlInTrack_; // x-axis: fill if plane contributes to track or not (even/odd), y-axis: number of planes in track
  map<CTPPSPixelDetId,TH2D*> h2PlContVsHitsMult_; // x-axis: fill if plane contributes to track or not (even/odd), y-axis: plane multiplicity
 
  // int digiPerPlaneBins = 50;
  // int digiPerPlaneMax = 100;
  // int digiPerStationBins = 300;
  // int digiPerStationMax = 600;
  int trackPerStationBins = 10;
  int trackPerStationMax = 10;
  int colMax = 104; // max cols per plane
  int rowMax = 160; // max rows per plane

};

CTPPSPixelTrackAnalyzer::CTPPSPixelTrackAnalyzer(const edm::ParameterSet &iConfig) {
  ppsPixelDigiToken_ = consumes<DetSetVector<CTPPSPixelDigi>>(
      iConfig.getUntrackedParameter<edm::InputTag>("tagPPSPixelDigi"));
  ppsPixelLocalTrackToken_ = consumes<DetSetVector<CTPPSPixelLocalTrack>>(
      iConfig.getUntrackedParameter<edm::InputTag>("tagPPSPixelLocalTrack"));
  Service<TFileService> fs;

  // Book histograms here
  for (auto const & arm : arms_)
    for (auto const & station : stations_){
      CTPPSPixelDetId stationId = CTPPSPixelDetId(arm,station,3); // Pixels have always rp=3
      h2PlContVsNPlInTrack_[stationId] = fs->make<TH2D>("h2PlContVsNPlInTrack", "h2PlContVsNPlInTrack",12,-0.5,11.5,4,2.5,6.5);
      h2PlContVsHitsMult_[stationId] = fs->make<TH2D>("h2PlContVsHitsMult", "h2PlContVsHitsMult",12,-0.5,11.5,20,0,20);
      for (int i=1;i<=h2PlContVsHitsMult_[stationId]->GetNbinsX();i++){
        if (i%2 == 1){
          h2PlContVsNPlInTrack_[stationId]->GetXaxis()->SetBinLabel(i,Form("Plane %i",(i-1)/2));
          h2PlContVsHitsMult_[stationId]->GetXaxis()->SetBinLabel(i,Form("Plane %i",(i-1)/2));
        }
        else{
          h2PlContVsNPlInTrack_[stationId]->GetXaxis()->SetBinLabel(i,Form("No plane %i",(i-1)/2));
          h2PlContVsHitsMult_[stationId]->GetXaxis()->SetBinLabel(i,Form("No plane %i",(i-1)/2));
        }
      }
    }
}

void CTPPSPixelTrackAnalyzer::beginJob() {}

void CTPPSPixelTrackAnalyzer::endJob() {}

void CTPPSPixelTrackAnalyzer::analyze(const edm::Event &iEvent,const edm::EventSetup &iSetup) {
  Handle<edm::DetSetVector<CTPPSPixelDigi>> ppsPixelDigis;
  iEvent.getByToken(ppsPixelDigiToken_,ppsPixelDigis);

  Handle<edm::DetSetVector<CTPPSPixelLocalTrack>> ppsPixelLocalTracks;
  iEvent.getByToken(ppsPixelLocalTrackToken_,ppsPixelLocalTracks);

  // Process tracks 
  for (const auto & ds_track : *ppsPixelLocalTracks){
    CTPPSPixelDetId stationId(ds_track.id);
      std::string stName;
      stationId.rpName(stName,CTPPSDetId::nFull);

    // Process station tracks
    for (const auto & track : ds_track.data){
      auto trackHits = track.hits();

      for (const auto & plane : planes_){
        CTPPSPixelDetId planeId(stationId);
        planeId.setPlane(plane);
        h2PlContVsNPlInTrack_[stationId]->SetNameTitle("h2PlContVsNPlInTrack_"+TString(stName),"h2PlContVsNPlInTrack_"+TString(stName)+";;# Points in track");
        h2PlContVsHitsMult_[stationId]->SetNameTitle("h2PlContVsHitsMult_"+TString(stName),"h2PlContVsHitsMult_"+TString(stName)+";;Plane multiplicity");

        // Check if plane contributed to track
        if (trackHits[planeId].data[0].isRealHit()){
          // Plane contributed
          h2PlContVsNPlInTrack_[stationId]->Fill(2*plane,track.numberOfPointsUsedForFit());
          h2PlContVsHitsMult_[stationId]->Fill(2*plane,(*ppsPixelDigis)[planeId].data.size());
        } else {
          // Plane did not contribute
          h2PlContVsNPlInTrack_[stationId]->Fill(2*plane+1,track.numberOfPointsUsedForFit());
          if ((*ppsPixelDigis).find(planeId) != (*ppsPixelDigis).end()){
            h2PlContVsHitsMult_[stationId]->Fill(2*plane+1,(*ppsPixelDigis)[planeId].data.size());
          }
        }

      }
    } 
  }
}

void CTPPSPixelTrackAnalyzer::fillDescriptions(edm::ConfigurationDescriptions &descriptions) {
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  desc.add<InputTag>("tagPPSPixelDigi", InputTag("ctppsPixelDigis"))
      ->setComment("inputTag of the PPS pixel digi input");
  desc.add<InputTag>("tagPPSPixelLocalTrack", InputTag("ctppsPixelLocalTrack"))
      ->setComment("inputTag of the PPS pixel local track input");
  descriptions.addDefault(desc);
}

DEFINE_FWK_MODULE(CTPPSPixelTrackAnalyzer);