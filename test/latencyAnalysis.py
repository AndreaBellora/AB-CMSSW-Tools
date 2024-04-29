import logging
import argparse
import os
import sys
import itertools
import subprocess
import ROOT
from array import array

#  User-defined run numbers and latency shift in ns
LATENCY_RUNS = {
    378861: {
        'lat_shift_45_210': 0,
        'lat_shift_45_220': 0,
        'lat_shift_56_210': 0,
        'lat_shift_56_220': 0,
    },
    378863: {
        'lat_shift_45_210': 1,
        'lat_shift_45_220': 1,
        'lat_shift_56_210': 1,
        'lat_shift_56_220': 1,
    },
    378864: {
        'lat_shift_45_210': -1,
        'lat_shift_45_220': -1,
        'lat_shift_56_210': -1,
        'lat_shift_56_220': -1,
    },
    378865: {
        'lat_shift_45_210': 2,
        'lat_shift_45_220': 2,
        'lat_shift_56_210': 2,
        'lat_shift_56_220': 2,
    },
    378866: {
        'lat_shift_45_210': -2,
        'lat_shift_45_220': -2,
        'lat_shift_56_210': -2,
        'lat_shift_56_220': -2,
    },
}

# User-defined filled bunch crossings
# INTERESTING_BXS = [1, 1786]
INTERESTING_BXS = [1786]

# Maximum bunch crossing number
MAX_BX = 3564

# General variables
SECTORS = ['45', '56']
STATIONS = ['210', '220']
PLANES = ['0', '1', '2', '3', '4', '5']


def parseArguments():
    parser = argparse.ArgumentParser(description='Analyze latency of PPS data')
    parser.add_argument('--dataset', type=str,
                        help='Dataset(s) to be processed, wildcards accepted', default='')
    parser.add_argument('--debug', action='store_true',
                        help='Enable debug output')
    parser.add_argument('--skipDQM', action='store_true',
                        help='Skip DQM analysis step')
    parser.add_argument('--inputDir', type=str, default='',
                        help='Directory in which DQM files are produced or from which they are taken when \'--skipDQM\' is defined.')
    parser.add_argument('--drawPlots', action='store_true',
                        help='Draw plots after processing the data.')
    parser.add_argument('--notScaled', action='store_true',
                        help='Do not scale the histograms.')
    return parser.parse_args()


def dqmStep(args):
    """Run PPSRandom DQM analysis

    :param args: command line arguments
    :type args: argparse.Namespace
    """
    runs = LATENCY_RUNS.keys()
    command = f'cmsRun ppsRandomFromRaw_cfg.py dataset={args.dataset} runs={",".join(map(str, runs))} outputDir={args.inputDir}'
    logging.info(f'Running command: {command}')
    subprocess.run(command, env=os.environ, shell=True, check=True)


def plottingStep(args):
    """Run latency plotting step

    :param args: command line arguments
    :type args: argparse.Namespace
    """

    # Collect data from histograms
    data = {}
    for run in LATENCY_RUNS.keys():
        dqm_file_name = f'DQM_V0001_PPSRANDOM_R000{run}.root'
        dqm_file_path = args.inputDir + '/' + \
            dqm_file_name if args.inputDir != '' else dqm_file_name
        logging.debug(f'Opening DQM file for run {run}: {dqm_file_path}')
        events_per_bx_hist_path = f'DQMData/Run {run}/PPSRANDOM/Run summary/RandomPixel/events per BX'
        logging.debug(f'Getting histogram {events_per_bx_hist_path}')
        if not os.path.exists(dqm_file_path):
            logging.warning(f'DQM file for run {run} not found. Skipping it.')
            continue
        dqm_file = ROOT.TFile(dqm_file_path, 'READ')
        if not dqm_file.IsOpen():
            logging.warning(
                f'Failed to open DQM file for run {run}. Skipping it.')
            continue
        events_per_bx_hist = dqm_file.Get(events_per_bx_hist_path)
        if not events_per_bx_hist:
            logging.warning(
                f'Failed to get histogram {events_per_bx_hist_path} for run {run}. Skipping it.')
            continue
        for sector, station, plane in itertools.product(SECTORS, STATIONS, PLANES):
            if f'{sector}_{station}_{plane}' not in data:
                data[f'{sector}_{station}_{plane}'] = {}
            lat_shift = LATENCY_RUNS[
                int(run)][f'lat_shift_{sector}_{station}']
            latency_hist_path = f'DQMData/Run {run}/PPSRANDOM/Run summary/RandomPixel/sector {sector}/station {station}/fr_hr/Digi per plane per BX - random triggers'
            latency_hist = dqm_file.Get(latency_hist_path)
            if not latency_hist:
                logging.warning(
                    f'Failed to get histogram {latency_hist_path} for run {run}. Skipping it.')
                continue

            hits_in_bxs = 0
            hits_in_bxs_m1 = 0
            hits_in_bxs_p1 = 0
            triggers_in_bxs = 0
            triggers_in_bxs_m1 = 0
            triggers_in_bxs_p1 = 0

            for bx in INTERESTING_BXS:
                bx_after = bx + 1 if bx + 1 <= MAX_BX else 1
                bx_before = bx - 1 if bx - 1 > 0 else MAX_BX
                bx_bin = latency_hist.GetXaxis().FindBin(bx)
                bx_after_bin = latency_hist.GetXaxis().FindBin(bx_after)
                bx_before_bin = latency_hist.GetXaxis().FindBin(bx_before)
                plane_bin = latency_hist.GetYaxis().FindBin(int(plane))
                hits_in_bxs += latency_hist.GetBinContent(bx_bin, plane_bin)
                hits_in_bxs_m1 += latency_hist.GetBinContent(
                    bx_before_bin, plane_bin)
                hits_in_bxs_p1 += latency_hist.GetBinContent(
                    bx_after_bin, plane_bin)
                triggers_in_bxs += events_per_bx_hist.GetBinContent(bx_bin)
                triggers_in_bxs_m1 += events_per_bx_hist.GetBinContent(
                    bx_before_bin)
                triggers_in_bxs_p1 += events_per_bx_hist.GetBinContent(
                    bx_after_bin)
                logging.debug(
                    f'Run {run}, sector {sector}, station {station}, plane {plane}, BX {bx}: {latency_hist.GetBinContent(bx_bin, plane_bin)} hits, {events_per_bx_hist.GetBinContent(bx_bin)} triggers')
                logging.debug(
                    f'Run {run}, sector {sector}, station {station}, plane {plane}, BX {bx_before}: {latency_hist.GetBinContent(bx_before_bin,plane_bin)} hits, {events_per_bx_hist.GetBinContent(bx_before_bin)} triggers')
                logging.debug(
                    f'Run {run}, sector {sector}, station {station}, plane {plane}, BX {bx_after}: {latency_hist.GetBinContent(bx_after_bin,plane_bin)} hits, {events_per_bx_hist.GetBinContent(bx_after_bin)} triggers')

            data[f'{sector}_{station}_{plane}'][lat_shift] = {
                'BX': hits_in_bxs/triggers_in_bxs,
                'BX-1': hits_in_bxs_m1/triggers_in_bxs_m1,
                'BX+1': hits_in_bxs_p1/triggers_in_bxs_p1,
                'total_hits': (hits_in_bxs+hits_in_bxs_m1+hits_in_bxs_p1)/(triggers_in_bxs+triggers_in_bxs_m1+triggers_in_bxs_p1),
            }

    if args.debug:
        logging.debug('Data:')
        from pprint import pprint
        pprint(data)
    canvases = []
    canvases_control = []
    graphs = []
    graphs_control = []
    ROOT.gStyle.SetOptStat(0)
    ROOT.gStyle.SetOptTitle(0)
    ROOT.gStyle.SetLegendBorderSize(0)
    for sector in SECTORS:
        for station in STATIONS:
            canvases.append(ROOT.TCanvas(f'{sector}-{station}',f'{sector}-{station}',1400,900))
            canvases_control.append(ROOT.TCanvas(f'{sector}-{station}_control',f'{sector}-{station}_control',1400,900))
            canvases[-1].Divide(2, 3)
            canvases_control[-1].Divide(2, 3)
            for plane in PLANES:
                lat_shifts = sorted(data[f'{sector}_{station}_{plane}'].keys())

                # Create and fill the control plot
                canvases_control[-1].cd(int(plane)+1)
                hits_control = [
                    data[f'{sector}_{station}_{plane}'][lat_shift]['total_hits'] for lat_shift in lat_shifts]
                y_max = max(hits_control)
                graphs_control.append(ROOT.TGraph(len(data[f'{sector}_{station}_{plane}']),
                                          array('d',lat_shifts),
                                          array('d',hits_control)))
                graphs_control[-1].GetXaxis().SetTitle('Latency shift [ns]')
                graphs_control[-1].GetYaxis().SetTitle('Total hits per trigger')
                graphs_control[-1].GetYaxis().SetRangeUser(0, y_max*1.65)
                graphs_control[-1].SetTitle(f'{sector}-{station}-fr-hr-{plane}')
                graphs_control[-1].SetName(f'{sector}-{station}-fr-hr-{plane}')
                graphs_control[-1].GetXaxis().SetLabelSize(0.05)
                graphs_control[-1].GetYaxis().SetLabelSize(0.05)
                graphs_control[-1].GetXaxis().SetTitleSize(0.06)
                graphs_control[-1].GetYaxis().SetTitleSize(0.06)
                graphs_control[-1].GetXaxis().SetTitleOffset(0.8)
                graphs_control[-1].GetYaxis().SetTitleOffset(0.8)
                graphs_control[-1].SetMarkerStyle(20)
                graphs_control[-1].Draw('ALP')

                # Create and fill the BX plot, 
                canvases[-1].cd(int(plane)+1)
                hits_lat_shifts_bx = [
                    data[f'{sector}_{station}_{plane}'][lat_shift]['BX'] for lat_shift in lat_shifts]
                hits_lat_shifts_bx_m1 = [
                    data[f'{sector}_{station}_{plane}'][lat_shift]['BX-1'] for lat_shift in lat_shifts]
                hits_lat_shifts_bx_p1 = [
                    data[f'{sector}_{station}_{plane}'][lat_shift]['BX+1'] for lat_shift in lat_shifts]
                
                max_hits_lat_shifts_bx = max(hits_lat_shifts_bx)
                max_hits_lat_shifts_bx_m1 = max(hits_lat_shifts_bx_m1)
                max_hits_lat_shifts_bx_p1 = max(hits_lat_shifts_bx_p1)
                if not args.notScaled:
                    # 'Normalize' the histograms -> divide each bin by the maximum value of the corresponding histogram
                    # 'Normalize all points over the number of hits in the relevant triggers
                    for i in range(len(hits_lat_shifts_bx)):
                        if hits_control[i] == 0:
                            continue
                        if max_hits_lat_shifts_bx != 0:
                            hits_lat_shifts_bx[i] = hits_lat_shifts_bx[i]/(max_hits_lat_shifts_bx*hits_control[i])
                        if max_hits_lat_shifts_bx_m1 != 0:
                            hits_lat_shifts_bx_m1[i] = hits_lat_shifts_bx_m1[i]/(max_hits_lat_shifts_bx_m1*hits_control[i])
                        if max_hits_lat_shifts_bx_p1 != 0:
                            hits_lat_shifts_bx_p1[i] = hits_lat_shifts_bx_p1[i]/(max_hits_lat_shifts_bx_p1*hits_control[i])
                
                y_max = max(max(hits_lat_shifts_bx), max(hits_lat_shifts_bx_m1), max(hits_lat_shifts_bx_p1))
                graphs.append(ROOT.TGraph(len(data[f'{sector}_{station}_{plane}']),
                                          array('d',lat_shifts),
                                          array('d',hits_lat_shifts_bx)))
                graphs[-1].GetXaxis().SetTitle('Latency shift [ns]')
                graphs[-1].GetYaxis().SetTitle('Hits per trigger')
                graphs[-1].GetYaxis().SetRangeUser(0, y_max*1.65)
                graphs[-1].SetTitle(f'{sector}-{station}-fr-hr-{plane} BX')
                graphs[-1].SetName(f'{sector}-{station}-fr-hr-{plane}_BX')
                graphs[-1].GetXaxis().SetLabelSize(0.05)
                graphs[-1].GetYaxis().SetLabelSize(0.05)
                graphs[-1].GetXaxis().SetTitleSize(0.06)
                graphs[-1].GetYaxis().SetTitleSize(0.06)
                graphs[-1].GetXaxis().SetTitleOffset(0.8)
                graphs[-1].GetYaxis().SetTitleOffset(0.8)
                graphs[-1].SetMarkerStyle(20)
                graphs[-1].Draw('ALP')

                color_m1 = ROOT.kRed
                graphs.append(ROOT.TGraph(len(data[f'{sector}_{station}_{plane}']),
                                          array('d',lat_shifts),
                                          array('d',hits_lat_shifts_bx_m1)))
                graphs[-1].SetTitle(f'{sector}-{station}-fr-hr-{plane} BX-1')
                graphs[-1].SetName(f'{sector}-{station}-fr-hr-{plane}_BX-1')
                graphs[-1].SetMarkerStyle(20)
                graphs[-1].SetMarkerColor(color_m1)
                graphs[-1].SetLineColor(color_m1)
                graphs[-1].Draw('LPsame')

                color_p1 = ROOT.kGreen+3
                graphs.append(ROOT.TGraph(len(data[f'{sector}_{station}_{plane}']),
                                          array('d',lat_shifts),
                                          array('d',hits_lat_shifts_bx_p1)))
                graphs[-1].SetTitle(f'{sector}-{station}-fr-hr-{plane} BX+1')
                graphs[-1].SetName(f'{sector}-{station}-fr-hr-{plane}_BX+1')
                graphs[-1].SetMarkerStyle(20)
                graphs[-1].SetMarkerColor(color_p1)
                graphs[-1].SetLineColor(color_p1)
                graphs[-1].Draw('LPsame')

                ROOT.gPad.BuildLegend(0.6, 0.6, 0.89, 0.89)


    for canvas in canvases:
        canvas.Update()
        if args.notScaled:
            canvas.SaveAs(f'{canvas.GetName()}.png')
        else:
            canvas.SaveAs(f'{canvas.GetName()}_scaled.png')
        if args.drawPlots:
            canvas.Draw()
    for canvas in canvases_control:
        canvas.Update()
        canvas.SaveAs(f'{canvas.GetName()}.png')
        if args.drawPlots:
            canvas.Draw()
    if args.drawPlots:
        input('Press Enter to continue...')
    return

def main(args):
    """Main function to run the latency analysis

    :param args: command line arguments
    :type args: argparse.Namespace
    """
    if not args.skipDQM:
        logging.info('Running DQM analysis')
        try:
            dqmStep(args)
        except subprocess.CalledProcessError as e:
            logging.fatal(
                f'Failed to run DQM analysis with return code {e.returncode}')
            sys.exit(1)
    plottingStep(args)


if __name__ == '__main__':
    args = parseArguments()
    if args.debug:
        logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s - '+os.path.basename(
            __file__)+' - %(levelname)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    else:
        logging.basicConfig(level=logging.INFO, format='[%(asctime)s - '+os.path.basename(
            __file__)+' - %(levelname)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    main(args)
