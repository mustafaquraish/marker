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
from marker import Marker

from cmd2 import ansi

all_students_list = []


class MarkerCLI(cmd2.Cmd):
    """ Marker CLI """

    def __init__(self, args):
        # Set use_ipython to True to enable the "ipy" command which embeds and interactive IPython shell
        super().__init__(use_ipython=False)

        self.marker = Marker(args)
        self.prompt = ansi.style('marker > ', fg="white", bg="black")


    def _complete_list_value(self, text, line, begidx, endidx):
        type_ = line.split()[1]
        if type_ == 'student':
            return [e for e in all_students_list if e.startswith(text)]
        else:
            return []
        
    student_parser = argparse.ArgumentParser()
    student_parser.add_argument("student", nargs='?', default=None, help="(Optional) individual student", choices=all_students_list)

    @cmd2.with_argparser(student_parser)
    def do_download(self, args):
        """ Download submissions for student(s) """
        self.marker.download_submissions(args.student)

    @cmd2.with_argparser(student_parser)
    def do_prepare(self, args):
        """ Download submissions for student(s) """
        self.marker.prepare(args.student)

    @cmd2.with_argparser(student_parser)
    def do_upload_marks(self, args):
        """ Download submissions for student(s) """
        self.marker.upload_marks(args.student)

    @cmd2.with_argparser(student_parser)
    def do_upload_reports(self, args):
        """ Download submissions for student(s) """
        self.marker.upload_reports(args.student)

    @cmd2.with_argparser(student_parser)
    def do_delete_reports(self, args):
        """ Download submissions for student(s) """
        self.marker.delete_reports(args.student)


    run_parser = argparse.ArgumentParser()
    run_parser.add_argument("student", nargs='?', default=None, help="(Optional) individual student", choices=all_students_list)
    run_parser.add_argument("--recompile", "-r", action='store_true', help="Force recompile submissions")
    run_parser.add_argument("--all", "-a", action='store_true', default=False, help="Force re-mark all submissions")
    @cmd2.with_argparser(run_parser)
    def do_run(self, args):
        """ Download submissions for student(s) """
        self.marker.run(args.student, args.recompile, args.all)


def main():
    top_parser = argparse.ArgumentParser()
    top_parser.add_argument("assgn_dir", nargs='?', default=os.getcwd(), help="Marking directory (Default: current)")
    top_parser.add_argument("--config", default=None, help="Location of configuration file, if not config.yml in assgn_dir")
    top_parser.add_argument("--src_dir", default=None, help="Location of source files, if not config.yml parent dir")
    
    args = vars(top_parser.parse_args())

    if args["config"] is None:
        args["config"] = f'{args["assgn_dir"]}/config.yml'
    if args["src_dir"] is None:
        args["src_dir"] = os.path.dirname(args["config"])

    candidates_dir = f'{args["assgn_dir"]}/candidates/'
    if os.path.isdir(candidates_dir):
        for student in os.listdir(candidates_dir):
            all_students_list.append(student)

    app = MarkerCLI(args)
    sys.exit(app.cmdloop())

if __name__ == '__main__':
    main()