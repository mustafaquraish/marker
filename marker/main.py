#! /usr/bin/env python3

import argparse
import os

# Subcommand imports
from marker.commands import upload_marks
from marker.commands import upload_reports
from marker.commands import download
from marker.commands import set_status
from marker.commands import prepare
from marker.commands import run


# Create the top-level parser
top_parser = argparse.ArgumentParser()
subparsers = top_parser.add_subparsers(dest="command", metavar='{command}')
subparsers.required = True

# -----------------------------------------------------------------------------
#                                download
# -----------------------------------------------------------------------------

# create the parser for the "a" command
parser_dl = subparsers.add_parser('download', help='Download submissions')
parser_dl.add_argument("config", help="Path to the marker conig file")
parser_dl.add_argument("assgn_dir", nargs='?', default=os.getcwd(), 
                    help="Location to create directories (Default: current)")
parser_dl.set_defaults(func=download.main)

# -----------------------------------------------------------------------------
#                                prepare
# -----------------------------------------------------------------------------

parser_prep = subparsers.add_parser('prepare', help='Prepare dir. for marking')
parser_prep.add_argument("config", help="Location of configuration file")
parser_prep.add_argument(dest="assgn_dir", nargs='?', default=os.getcwd(), 
                    help="Location of marking directory (Default: current)")
parser_prep.add_argument("--src", "-s", dest="src_dir", default=None,
                    help="Source directory (Default: config. directory)")
parser_prep.set_defaults(func=prepare.main)

# -----------------------------------------------------------------------------
#                                  run
# -----------------------------------------------------------------------------

parser_run = subparsers.add_parser('run', help='Run the automarker')
parser_run.add_argument("assgn_dir", nargs='?', default=os.getcwd(), 
                        help="Marking directory (Default: current)")
parser_run.add_argument("--recompile", "-r", action='store_true', 
                        help="Force recompile submissions")
parser_run.add_argument("--all", "-a", action='store_true', default=False,
                        help="Force re-mark all submissions")
parser_run.add_argument("--config", default=None, metavar="cfg",
                        help="Location of configuration file, if not "
                        "config.yml in assgn_dir")
parser_run.add_argument("--no-parallel", "-n", dest="no_parallel",
                        action='store_true', help="Don't mark students in "
                        "parallel. This might be needed if tests keep timing "
                        "out due to CPU load")
parser_run.set_defaults(func=run.main)

# -----------------------------------------------------------------------------
#                              upload-marks
# -----------------------------------------------------------------------------

parser_upm = subparsers.add_parser('upload-marks', help='Upload the marks')
parser_upm.add_argument("assgn_dir", nargs='?', default=os.getcwd(), 
                        help="Location of assignment dir (Default: current)")
parser_upm.add_argument("--config", default=None, metavar="cfg",
                        help="Location of configuration file, if not "
                        "config.yml in assgn_dir")
parser_upm.set_defaults(func=upload_marks.main)

# -----------------------------------------------------------------------------
#                              upload-reports
# -----------------------------------------------------------------------------

parser_upr = subparsers.add_parser('upload-reports', help='Upload the reports')
parser_upr.add_argument("assgn_dir", nargs='?', default=os.getcwd(), 
                        help="Location of assignment dir (Default: current)")
parser_upr.add_argument("--config", default=None, metavar="cfg",
                        help="Location of configuration file, if not "
                        "config.yml in assgn_dir")
parser_upr.set_defaults(func=upload_reports.main)


# -----------------------------------------------------------------------------
#                              set-status
# -----------------------------------------------------------------------------

parser_sst = subparsers.add_parser('set-status', help='Set marking status')
parser_sst.add_argument("status", choices=['complete', 'incomplete'], 
                        help="Status to set")
parser_sst.add_argument("assgn_dir", nargs='?', default=os.getcwd(), 
                        help="Location of assignment dir (Default: current)")
parser_sst.add_argument("--config", default=None, metavar="cfg",
                        help="Location of configuration file, if not "
                        "config.yml in assgn_dir")
parser_sst.set_defaults(func=set_status.main)

# -----------------------------------------------------------------------------

args = top_parser.parse_args()

# Set default configuration values that depend on others
if args.config is None:
    args.config = f'{args.assgn_dir}/config.yml'
if hasattr(args, 'src_dir') and args.src_dir is None:
    args.src_dir = os.path.dirname(os.path.abspath(args.config))

args.func(args)
