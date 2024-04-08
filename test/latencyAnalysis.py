import logging
import argparse
import os
import sys
import itertools
import ROOT

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
INTERESTING_BXS = [1, 1786]

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
                        help='Input directory for DQM files')
    return parser.parse_args()


def dqmStep(args):
    """Run PPSRandom DQM analysis

    :param args: command line arguments
    :type args: argparse.Namespace
    """
    pass


def plottingStep(args):
    """Run latency plotting step

    :param args: command line arguments
    :type args: argparse.Namespace
    """

    # Collect data from histograms
    data = {}
    for run in LATENCY_RUNS.keys():
        dqm_file_path = args.inputDir + '/' + f'DQM_V0001_PPSRANDOM_R000{run}.root' if args.inputDir != '' else f'DQM_V0001_PPSRANDOM_R000{run}.root'
        logging.debug(f'Opening DQM file for run {run}: {dqm_file_path}')
        events_per_bx_hist_path = f'DQMData/Run {run}/PPSRANDOM/Run summary/RandomPixel/events per BX'
        logging.debug(f'Getting histogram {events_per_bx_hist_path}')
        if not os.path.exists(dqm_file_path):
            logging.warning(f'DQM file for run {run} not found. Skipping it.')
            continue
        dqm_file = ROOT.TFile(dqm_file_path, 'READ')
        if not dqm_file.IsOpen():
            logging.warning(f'Failed to open DQM file for run {run}. Skipping it.')
            continue
        events_per_bx_hist = dqm_file.Get(events_per_bx_hist_path)
        if not events_per_bx_hist:
            logging.warning(f'Failed to get histogram {events_per_bx_hist_path} for run {run}. Skipping it.')
            continue
        for sector, station, plane in itertools.product(SECTORS, STATIONS, PLANES):
            data[f'{sector}_{station}_{plane}'] = {}
            lat_shifts = LATENCY_RUNS[
                int(run)][f'lat_shift_{sector}_{station}']
            latency_hist_path = f'DQMData/Run {run}/PPSRANDOM/Run summary/RandomPixel/sector {sector}/station {station}/fr-hr/Digi per plane per BX - random triggers'
            latency_hist = dqm_file.Get(latency_hist_path)
            if not latency_hist:
                logging.warning(f'Failed to get histogram {latency_hist_path} for run {run}. Skipping it.')
                continue
            
            sys.exit(1)

def main(args):
    """Main function to run the latency analysis

    :param args: command line arguments
    :type args: argparse.Namespace
    """
    if not args.skipDQM:
        logging.info('Running DQM analysis')
        dqmStep(args)

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
