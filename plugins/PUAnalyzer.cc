// Original Author:  Andrea Bellora
//         Created:  Wed, 21 Dec 2022 10:33:05 GMT
//
//

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/one/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "DataFormats/Common/interface/DetSetVector.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "DataFormats/CTPPSDetId/interface/CTPPSPixelDetId.h"
#include "DataFormats/CTPPSDigi/interface/CTPPSPixelDigi.h"

#include "DataFormats/VertexReco/interface/Vertex.h"
#include "TH1D.h"
#include "TH2D.h"
#include "TFile.h"
#include "TString.h"

#include <string>
#include <vector>
#include <map>
#include <memory>


using namespace std;
using namespace edm;

class PUAnalyzer : public edm::one::EDAnalyzer<edm::one::SharedResources> {
public:
  explicit PUAnalyzer(const edm::ParameterSet &);
  inline ~PUAnalyzer() {};
  static void fillDescriptions(edm::ConfigurationDescriptions &descriptions);

private:
  virtual void beginJob() override;
  virtual void analyze(const edm::Event &, const edm::EventSetup &) override;
  virtual void endJob() override;


  // Data to get
  edm::EDGetTokenT<edm::DetSetVector<CTPPSPixelDigi>> ppsPixelDigiToken_;
  edm::EDGetTokenT<edm::View<reco::Vertex>> recoVertexToken_;

  string outputFileName_;

  // Hard-coded configs
  vector<uint32_t> arms_ = {0, 1};
  vector<uint32_t> stations_ = {0, 2};
  vector<uint32_t> planes_ = {0, 1, 2, 3, 4, 5};

  int digiPerPlaneBins = 50;
  int digiPerPlaneMax = 100;
  int digiPerStationBins = 300;
  int digiPerStationMax = 600;
  int PUBins = 16;
  int PUMax = 80;
  int colMax = 104; // max cols per plane
  int rowMax = 160; // max rows per plane

  // output histograms
  unique_ptr<TH1D> h1PU_;
  map<CTPPSPixelDetId, unique_ptr<TH1D>> h1DigiMultPerPlane_;
  map<CTPPSPixelDetId, unique_ptr<TH1D>> h1DigiMultPerStation_;
  map<CTPPSPixelDetId, unique_ptr<TH2D>> h2PUvsDigiMultPerPlane_;
  map<CTPPSPixelDetId, unique_ptr<TH2D>> h2PUvsDigiMultPerStation_;
  map<CTPPSPixelDetId, unique_ptr<TH2D>> h2DigiXY_;

  
};

PUAnalyzer::PUAnalyzer(const edm::ParameterSet &iConfig) {
  ppsPixelDigiToken_ = consumes<DetSetVector<CTPPSPixelDigi>>(
      iConfig.getUntrackedParameter<edm::InputTag>("tagPPSPixeldigi"));
  recoVertexToken_ = consumes<edm::View<reco::Vertex>>(
      iConfig.getUntrackedParameter<edm::InputTag>("tagRecoVertex"));
  outputFileName_ = iConfig.getUntrackedParameter<string>("outputFileName");
}

void PUAnalyzer::beginJob() {
  // Book histograms
  h1PU_ = make_unique<TH1D>(TString("h1PU"),TString("h1PU"),PUBins,0,PUMax);
  for (auto const & arm : arms_)
    for (auto const & station : stations_){
      CTPPSPixelDetId stationId = CTPPSPixelDetId(arm,station,3); // Pixels have always rp=3
      std::string stName;
      stationId.rpName(stName,CTPPSDetId::nFull);

      // Book per-station histograms
      h1DigiMultPerStation_[stationId] = make_unique<TH1D>(TString("h1DigiMult_"+stName),TString("Digi Multiplicity "+stName),digiPerStationBins,0,digiPerStationMax);
      h2PUvsDigiMultPerStation_[stationId] = 
        make_unique<TH2D>(TString("h2PUvsDigiMult_"+stName),TString("PU vs Digi Multiplicity "+stName),PUBins,0,PUMax,digiPerStationBins,0,digiPerStationMax);
      
      for (auto const & plane : planes_){
        CTPPSPixelDetId planeId = CTPPSPixelDetId(arm,station,3,plane); // Pixels have always rp=3
        std::string pName = stName + to_string(plane);

        // Book per-plane histograms
        h1DigiMultPerPlane_[planeId] = make_unique<TH1D>(TString("h1DigiMult_"+pName),TString("Digi Multiplicity "+pName),digiPerPlaneBins,0,digiPerPlaneMax);
        h2PUvsDigiMultPerPlane_[planeId] = 
          make_unique<TH2D>(TString("h2PUvsDigiMult_"+pName),TString("PU vs Digi Multiplicity "+pName),PUBins,0,PUMax,digiPerPlaneBins,0,digiPerPlaneMax);
        h2DigiXY_[planeId] = make_unique<TH2D>(TString("h2DigiXY_"+pName),TString("Hitmap "+pName),colMax,0,colMax,rowMax,0,rowMax);
      }
    }
}

void PUAnalyzer::endJob() {
  auto outputFile_ = make_unique<TFile>(outputFileName_.data(), "RECREATE");
  h1PU_->Write();
  for (auto const & arm : arms_){
    std::string armName;
    CTPPSPixelDetId(arm,0,0).armName(armName,CTPPSDetId::nShort);
    outputFile_->mkdir(TString("Sector "+armName));
    outputFile_->cd(TString("Sector "+armName));

    for (auto const & station : stations_) {
      std::string stationName;
      CTPPSPixelDetId stationId = CTPPSPixelDetId(arm,station,3);
      stationId.stationName(stationName,CTPPSDetId::nShort);
      outputFile_->mkdir(TString("Sector "+armName+"/Station "+stationName));
      outputFile_->cd(TString("Sector "+armName+"/Station "+stationName));

      h1DigiMultPerStation_[stationId]->Write();
      h2PUvsDigiMultPerStation_[stationId]->Write();

      for (auto const & plane : planes_) {
        CTPPSPixelDetId planeId = CTPPSPixelDetId(arm,station,3,plane);
        outputFile_->mkdir(TString("Sector "+armName+"/Station "+stationName+"/Plane "+to_string(plane)));
        outputFile_->cd(TString("Sector "+armName+"/Station "+stationName+"/Plane "+to_string(plane)));

        h1DigiMultPerPlane_[planeId]->Write();
        h2PUvsDigiMultPerPlane_[planeId]->Write();
        h2DigiXY_[planeId]->Write();
      }
    }
  }
}

void PUAnalyzer::analyze(const edm::Event &iEvent,const edm::EventSetup &iSetup) {
  Handle<edm::View<reco::Vertex>> recoVertices;
  iEvent.getByToken(recoVertexToken_, recoVertices);

  Handle<edm::DetSetVector<CTPPSPixelDigi>> ppsPixelDigis;
  iEvent.getByToken(ppsPixelDigiToken_,ppsPixelDigis);

  // Process vertices
  int vtxMux = 0;
  for (unsigned int i = 0; i < recoVertices->size() && recoVertices->size() < 150; ++i) {
    const edm::Ptr<reco::Vertex> vertex = recoVertices->ptrAt(i);
    if (fabs(vertex->z()) < 15 && vertex->isValid()) {
      vtxMux++;
    }
  }
  h1PU_->Fill(vtxMux);

  if (!ppsPixelDigis.isValid()) return;

  map<CTPPSPixelDetId,int> stationDigiMux; // store station digi multiplicity 
  for (const auto & arm : arms_)
    for (const auto & station : stations_)
      stationDigiMux[CTPPSPixelDetId(arm,station,3)] = 0;

  // Process pixel digis & fill per-plane histograms
  for (const auto & ds_digi : *ppsPixelDigis) {
    CTPPSPixelDetId planeId(ds_digi.id);
    CTPPSPixelDetId stationId = CTPPSPixelDetId(planeId.arm(),planeId.station(),3);

    int planeMux = ds_digi.data.size();
    stationDigiMux[stationId] += ds_digi.data.size();

    h1DigiMultPerPlane_[planeId]->Fill(planeMux);
    h2PUvsDigiMultPerPlane_[planeId]->Fill(vtxMux,planeMux);
    for (const auto & digi : ds_digi.data){
      h2DigiXY_[planeId]->Fill(digi.column(),digi.row());
    }
  }

  // Fill per-station histograms
  for (const auto & rpAndDigiMux : stationDigiMux) {
    h1DigiMultPerStation_[rpAndDigiMux.first]->Fill(rpAndDigiMux.second);
    h2PUvsDigiMultPerStation_[rpAndDigiMux.first]->Fill(vtxMux,rpAndDigiMux.second);
  }

}

void PUAnalyzer::fillDescriptions(edm::ConfigurationDescriptions &descriptions) {
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  desc.add<InputTag>("tagPPSPixeldigi", InputTag("ctppsPixelDigis"))
      ->setComment("inputTag of the PPS pixel digi input");
  desc.add<InputTag>("tagRecoVertex", InputTag("offlinePrimaryVertices"))
      ->setComment("inputTag of the tracker vertex input");
  desc.add<string>("outputFileName", "PUAnalysis.root")
      ->setComment("name of the output file");
  descriptions.addDefault(desc);
}

DEFINE_FWK_MODULE(PUAnalyzer);