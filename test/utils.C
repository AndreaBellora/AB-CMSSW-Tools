
#ifndef GETFIRSTPLOTFROMDIR
#define GETFIRSTPLOTFROMDIR
// 
// Store in *plot_ptr the first plot matching the regular 
// expression *plot_re, in the TDirectory *dir
// 
template <class T>
void getFirstPlotFromDir(TString plot_re, T &plot_ptr, TDirectory* &dir){
    bool found = false;
    for (const auto&& k : *(dir->GetListOfKeys())){
        TString key = k->GetName();
        if (key.Contains(TRegexp(plot_re,kTRUE))){
            plot_ptr = (T)dir->Get(key.Data());
            found = true;
            break;
        }
    }
    if (!found)
        plot_ptr = nullptr;
}
#endif

#ifndef GETFIRSTPLOTFROMFILE
#define GETFIRSTPLOTFROMFILE
// 
// Store in *plot_ptr the first plot matching the regular 
// expression *plot_re, in the TFile *file
// 
template <class T>
void getFirstPlotFromFile(TString plot_re, T &plot_ptr, TFile* &file){
    bool found = false;
    for (const auto&& k : *(file->GetListOfKeys())){
        TString key = k->GetName();
        if (key.Contains(TRegexp(plot_re,kTRUE))){
            plot_ptr = (T)file->Get(key.Data());
            found = true;
            break;
        }
    }
    if (!found)
        plot_ptr = nullptr;
}
#endif

#ifndef GETNTHPLOTFROMDIR
#define GETNTHPLOTFROMDIR
// 
// Store in *plot_ptr the n-th (starting from 1) plot matching  
// the regular expression *plot_re, in the TDirectory *dir
// 
template <class T>
void getNthPlotFromDir(TString plot_re, T &plot_ptr, TDirectory* dir, int n){
    bool found = false;
    int found_idx = 0;
    int desired_idx = n - 1;
    for (const auto&& k : *(dir->GetListOfKeys())){
        TString key = k->GetName();
        if (key.Contains(TRegexp(plot_re,kTRUE))){
            found_idx ++;
            if (found_idx == desired_idx){
                plot_ptr = (T)dir->Get(key.Data());
                found = true;
                break;
            }
        }
    }
    if (!found)
        plot_ptr = nullptr;
}
#endif

#ifndef MAKECANVASWITHASPECTRATIO
#define MAKECANVASWITHASPECTRATIO
// 
// Create a canvas with the w:h aspect ratio
// 
TCanvas* makeCanvasWithAspectRatio(TString name, TString title, int w, int h){
    int displayH = gClient->GetDisplayHeight(); 
    int displayW = gClient->GetDisplayWidth();
    // cout << displayW << " " << displayH << "\n";
    float finalW = displayW - 150;
    float finalH = finalW*h/w;

    bool h_limited = finalH > (displayH - 15)  ? true : false;

    if (h_limited){
        // cout << "it's h limited\n"; 
        finalH = displayH - 150;
        finalW = finalH*w/h;
    }
    // cout << "making it " << finalW << " " << finalH << "\n";
    return new TCanvas(name,title,100,100,int(finalW),int(finalH));
}
#endif