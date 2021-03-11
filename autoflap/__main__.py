"""
AutoFLAP CLI
============

A Command Line Interface (CLI) for quick use of AutoFLAP features.

Through this resource it is possible to export JFLAP design files by
importing automaton representation spreadsheets.

This CLI also has several configuration options to change the behavior
with which both processes are executed.
"""
import errno
import os
from argparse import ArgumentParser

import autoflap as app
import autoflap.constants as c
from autoflap.automaton.automaton import Automaton

parser = ArgumentParser(prog=app.__name__,
                        description='JFLAP design generator from an ' \
                                    'automaton representation spreadsheet')

parser.add_argument('input_files',
                    nargs='+',
                    metavar='<csv_file>',
                    help='paths for the input CSV files')

parser.add_argument('-v',
                    '--version',
                    action='version',
                    version=f'AutoFLAP {app.__version__}')

parser.add_argument('-i',
                    '--initial-state-symbol',
                    default=c.DEFAULT_INITIAL_STATE_SYMBOL,
                    metavar='<symbol>',
                    help='initial state symbol in spreadsheet; default is ' \
                         '%(default)s')

parser.add_argument('-f',
                    '--final-state-symbol',
                    default=c.DEFAULT_FINAL_STATE_SYMBOL,
                    metavar='<symbol>',
                    help='final states symbol in spreadsheet; default is ' \
                         '%(default)s')

parser.add_argument('-n',
                    '--no-transition-symbol',
                    default=c.DEFAULT_NO_TRANSITION_SYMBOL,
                    metavar='<symbol>',
                    help='no transition symbol in spreadsheet; default is ' \
                         '%(default)s')

parser.add_argument('-e',
                    '--empty-string-symbol',
                    default=c.DEFAULT_EMPTY_STRING_SYMBOL,
                    metavar='<symbol>',
                    help='empty string representation symbol in ' \
                         'spreadsheet, usually represented by the ' \
                         'characters epsilon or lambda in JFLAP; default is ' \
                         '%(default)s')

parser.add_argument('-s',
                    '--states-col-index',
                    default=c.DEFAULT_STATES_COL,
                    metavar='<index>',
                    type=int,
                    help='states column index (i.e. its position) in ' \
                         'spreadsheet, starting at 0; default is %(default)s')

parser.add_argument('-y',
                    '--state-symbols-col-index',
                    default=c.DEFAULT_STATE_SYMBOLS_COL,
                    metavar='<index>',
                    type=int,
                    help='state symbols column index (i.e. its position) in ' \
                         'spreadsheet, starting at 0; default is %(default)s')

parser.add_argument('-r',
                    '--drawing-radius-factor',
                    default=c.DEFAULT_DRAWING_RADIUS_FACTOR,
                    metavar='<factor>',
                    type=float,
                    help='circle radius factor when designating the states ' \
                         'positions; the radius is equal to this factor ' \
                         'times the number of states; default is %(default)s')

parser.add_argument('-m',
                    '--drawing-margin',
                    default=c.DEFAULT_DRAWING_MARGIN,
                    metavar='<margin>',
                    type=float,
                    help='distance from the left and top margins from which ' \
                         'the states are positioned, in pixels; default is ' \
                         '%(default)s')

parser.add_argument('-q',
                    '--quiet',
                    action='store_true',
                    help='supress output messages')

parser.add_argument('-o',
                    '--output-dir',
                    nargs='?',
                    default=c.DEFAULT_OUTPUT_DIR,
                    metavar='<path>',
                    help='output path for JFLAP files, either relative or ' \
                         'absolute; default is the current directory; if it ' \
                         'is not followed by an argument, the paths of the ' \
                         'input files will be used, respectively')

args = vars(parser.parse_args())

output_dir = args.pop('output_dir')

if output_dir is not None:
    if not os.path.exists(output_dir):
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT),
                                output_dir)

    if not os.path.isdir(output_dir):
        raise NotADirectoryError(errno.ENOTDIR, os.strerror(errno.ENOTDIR),
                                 output_dir)

input_files = set(args.pop('input_files'))
input_files_number = len(input_files)

is_quiet = args.pop('quiet')

build_jff_keys = ['drawing_radius_factor', 'drawing_margin']
build_jff_args = {k: args.pop(k) for k in build_jff_keys}

for i, input_file in enumerate(input_files):
    try:
        automaton = Automaton()

        if not is_quiet:
            print(f"Parsing '{input_file}'...")

        automaton.parse_csv(input_file, **args)

        if not is_quiet:
            print('Building the JFLAP design file...')

        output_file = automaton.build_jff(
            os.path.splitext(input_file)[0], output_dir, **build_jff_args)

        if not is_quiet:
            print(f"File '{output_file}' was created successfully!")

            s = len(automaton.states)
            t = len(automaton.transitions)

            print(f'{s} state{"s" if s > 1 else ""} and ' \
                  f'{t} transition{"s" if t > 1 else ""} were computed.')
    except Exception as e:
        if not is_quiet:
            print(f'ERROR: {str(e)[:1].upper() + str(e)[1:]}!')

    if not is_quiet and i != input_files_number - 1:
        print()
