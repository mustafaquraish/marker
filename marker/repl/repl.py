#!/usr/bin/env python
# coding=utf-8
"""
A sample application for cmd2.
"""
import argparse
import random
import sys
import cmd2
import os
import textwrap
from .. import Marker, CONFIG_DIR
from .console import REPLConsole
from ..utils import listdir
from cmd2 import ansi
from cmd2.utils import basic_complete
from .show_stats import show_stats


class MarkerCLI(cmd2.Cmd):

    def __init__(self, args):
        shortcuts = dict(cmd2.DEFAULT_SHORTCUTS)
        # Run a quick script to get students with timed-out tests
        timed_out_cmd = (f"grep 'Timed out' {args['assgn_dir']}/candidates/*/report.txt | " +
                         f"sed -n 's/.*candidates\/\([a-zA-Z0-9\.]*\).*/\\1/p' | uniq")
        shortcuts.update({'timed-out': timed_out_cmd})

        # cmd2 doesn't allow dashes by default, so just alias them
        shortcuts.update({'upload-reports'  : 'upload_reports'})
        shortcuts.update({'upload-marks'    : 'upload_marks'})
        shortcuts.update({'delete-reports'  : 'delete_reports'})
        shortcuts.update({'set-status'      : 'set_status'})

        hist_file = os.path.join(CONFIG_DIR, "cli_history.dat")
        super().__init__(
            use_ipython=False, 
            shortcuts=shortcuts, 
            persistent_history_file=hist_file,
        )

    # Hide all built-in commands (still accessible)...
        to_hide = ['edit', 'macro', 'py', 'shortcuts', 'set', 'q',
                   'run_pyscript', 'run_script', 'alias', 'help',
                   'shell', 'history', 'quit']
        for cmd in to_hide:
            self.hidden_commands.append(cmd)

        self.args = args
        self.console = REPLConsole()
        self.marker = Marker(self.args, self.console)
        self.prompt = ansi.style('marker > ', fg="blue")
        self.default_to_shell = True
        self.students_list = []
        self.debug = True
        self.update_students_list()

    # --------------- Update student list for autocompletion ------------------

    def update_students_list(self, students=None):
        if students is not None:
            self.students_list = students
        else:
            candidates_dir = os.path.join(self.args["assgn_dir"], "candidates")
            if os.path.isdir(candidates_dir):
                students_list = sorted(listdir(candidates_dir))
                self.students_list = students_list

    # --------------- Reload config file --------------------------------------

    def do_reload(self, args):
        """ Reload the configuration file """
        self.marker = Marker(self.args)

    # --------------- Completion helper ---------------------------------------

    def student_completer(self, text, line, begidx, endidx):
        return basic_complete(text, line, begidx, endidx, self.students_list)

    # ---------------- Download submissions -----------------------------------

    download_parser = argparse.ArgumentParser()
    download_parser.add_argument("students", nargs='*', help="(Optional) specific students", completer_method=student_completer)
    download_parser.add_argument("-l", "--allow_late", action='store_true', default=False, help="Get newest submission (after deadline / not collected)")

    @cmd2.with_argparser(download_parser)
    def do_download(self, args):
        """ Download submissions for student(s) """
        self.marker.download(args.students, allow_late=args.allow_late)
        self.update_students_list(self.marker.lms.students)


    # ----------------- Prepare submissions -----------------------------------

    prepare_parser = argparse.ArgumentParser()
    prepare_parser.add_argument("students", nargs='*', help="(Optional) specific students", completer_method=student_completer)

    @cmd2.with_argparser(prepare_parser)
    def do_prepare(self, args):
        """ Prepare submissions for student(s) """
        self.marker.prepare(args.students)

    # ---------------------- Upload marks -------------------------------------


    upload_mark_parser = argparse.ArgumentParser()
    upload_mark_parser.add_argument("students", nargs='*', help="(Optional) specific students", completer_method=student_completer)

    @cmd2.with_argparser(upload_mark_parser)
    def do_upload_marks(self, args):
        """ Upload marks for student(s) """
        self.marker.upload_marks(args.students)

    # ---------------------- Upload reports -----------------------------------

    upload_report_parser = argparse.ArgumentParser()
    upload_report_parser.add_argument("students", nargs='*', help="(Optional) specific students", completer_method=student_completer)

    @cmd2.with_argparser(upload_report_parser)
    def do_upload_reports(self, args):
        """ Upload reports for student(s) """
        self.marker.upload_reports(args.students)

    # ---------------------- Delete reports -----------------------------------

    delete_report_parser = argparse.ArgumentParser()
    delete_report_parser.add_argument("students", nargs='*', help="(Optional) specific students", completer_method=student_completer)

    @cmd2.with_argparser(delete_report_parser)
    def do_delete_reports(self, args):
        """ Delete reports from LMS for student(s) """
        self.marker.delete_reports(args.students)


    # ---------------------- Run automarker -----------------------------------

    run_parser = argparse.ArgumentParser()
    run_parser.add_argument("students", nargs='*', help="(Optional) specific students", completer_method=student_completer)
    run_parser.add_argument("-r", "--recompile", action='store_true', help="Force recompile submissions")
    run_parser.add_argument("-a", "--all", action='store_true', default=False, help="Force re-mark all submissions")
    run_parser.add_argument("-q", "--quiet", action='store_true', default=False, help="Don't display marks as submissions finish")
    @cmd2.with_argparser(run_parser)
    def do_run(self, args):
        """ Run test cases for student(s) """
        self.marker.run(args.students, args.recompile, args.all, args.quiet)


    # ---------------------- Display Statistics -------------------------------

    stats_parser = argparse.ArgumentParser()
    stats_parser.add_argument("students", nargs='*', help="(Optional) specific students", completer_method=student_completer)
    stats_parser.add_argument("-m", "--minimal", action='store_true', default=False, help="Only display mean / median")
    @cmd2.with_argparser(stats_parser)
    def do_stats(self, args):
        """ Display mark statistics for student(s) """
        stats = self.marker.stats(args.students)
        if args.students != []:
            for user, markList in stats.items():
                self.console.log(f"{user}: {markList}")
        else:
            show_stats(self.console, stats, args.minimal)
    

    # ---------------------- Set status (Markus) -----------------------------------

    status_parser = argparse.ArgumentParser()
    status_parser.add_argument("status", help="Status", choices=["complete", "incomplete"])
    status_parser.add_argument("students", nargs='*', help="(Optional) specific students", completer_method=student_completer)

    @cmd2.with_argparser(status_parser)
    def do_set_status(self, args):
        """ Set the status on MarkUs for student(s) """
        self.marker.set_status(args.status, args.students)

    # ---------------------- Clean everything --------------------------------------

    clean_parser = argparse.ArgumentParser()
    clean_parser.add_argument("-f", "--force", action='store_true', default=False, help="Don't ask to confirm")

    @cmd2.with_argparser(clean_parser)
    def do_clean(self, args):
        """ Remove candidates directory and marksheet """
        if not args.force:
            if not self.console.ask("Delete all submissions and marksheet? ", default=True):
                self.console.error("Cancelled")
                return
        self.marker.clean()

    # -------------------------- Aliases --------------------------------------

    do_q = cmd2.Cmd.do_quit


def main():
    top_parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent('''\
         additional information:
             This program is an interactive REPL, which can also be used as a
             regular CLI. For instance, running:

                $ marker download student1

             is equivalent to first running `marker`, then running the
             command `download student1` on the REPL, followed by `quit`.
         ''')
    )
    top_parser.add_argument("-d", "--assgn_dir", default=os.getcwd(), help="Marking directory (Default: current)")
    top_parser.add_argument("-c", "--config", default=None, help="Location of config file (Default: assgn_dir/config.yml)")
    top_parser.add_argument("-s", "--src_dir", default=None, help="Location of source files (Default: assgn_dir)")

    args, unknown = top_parser.parse_known_args()
    args = vars(args)

    if args["config"] is None:
        args["config"] = os.path.join(args["assgn_dir"], "config.yml")
    if args["src_dir"] is None:
        args["src_dir"] = args["assgn_dir"]

    # Make everything an absolute path
    args["src_dir"] = os.path.abspath(args["src_dir"])
    args["assgn_dir"] = os.path.abspath(args["assgn_dir"])
    args["config"] = os.path.abspath(args["config"])

    # Remove command line args to not trip up cmd2
    sys.argv = sys.argv[:1]     # Keep argv[0] intact

    # Handle remaining command line args to make this behave like a regular CLI
    if unknown != []:
        # Dashed and underscores are both fine for CLI
        command = " ".join(unknown)
        sys.argv.append(command)
        sys.argv.append("quit")

    app = MarkerCLI(args)
    sys.exit(app.cmdloop())

if __name__ == '__main__':
    main()
