#include <memory>
#include "TROOT.h"
#include "TSystem.h"

#include "utils.C"

using namespace std;
using namespace TMath;

TString trackLabel = "CTPPSPixelLocalTrackedmDetSetVector_ctppsPixelLocalTracks__TEST.obj._sets.data";
TString trackId = "CTPPSPixelLocalTrackedmDetSetVector_ctppsPixelLocalTracks__TEST.obj._sets.id";
double bin_size_x = 0.15 * Cos(20.*Pi()/180.);
double bin_size_y = 0.1; 
double min_x = 0;
double max_x = 20;
double min_y = -12;
double max_y = 12;
int bins_x = ceil((max_x-min_x)/bin_size_x);
int bins_y = ceil((max_y-min_y)/bin_size_y);
int maxEvents = 10000;

void analysisMacro(
    TString inFileName="/eos/cms/store/group/dpg_ctpps/comm_ctpps/Commissioning_2022/ZeroBias0/ZeroBias_Run354332/220625_074448/0000/PPS_AOD_118.root",
    TString outFileName="out.root"
){
    // Enable FWLite
    gSystem->Load("libFWCoreFWLite.so");
    FWLiteEnabler::enable();
    gSystem->Load("libDataFormatsFWLite.so");
    gSystem->Load("libDataFormatsPatCandidates.so");

    auto f_in = make_unique<TFile>(inFileName);
    TTree *events = (TTree*)f_in->Get("Events");
    CTPPSPixelDetId detId(1,0,3);
    auto c = makeCanvasWithAspectRatio("Canvas","Canvas",16,9);

    // Create the string to produce a 2D histogram with the wanted binning
    TString hist_str = Form("hnew(%i,%f,%f,%i,%f,%f)",bins_x,min_x,max_x,bins_y,min_y,max_y);

    // Use TTree::Draw to create the plot and put it into the histogram
    events->Draw(trackLabel+".y0():"+trackLabel+".x0()>>"+hist_str,trackId+"=="+detId.rawId(),"colz",maxEvents);
    // Retrieve the histogram
    TH2F *hitmap = (TH2F*)gDirectory->Get("hnew");
    c->cd();
    hitmap->DrawCopy("colz");
    
    // Create output file
    auto f_out = make_unique<TFile>(outFileName,"RECREATE");

    // Save canvas in the output
    c->Write();

}
