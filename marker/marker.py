import asyncio
import os
import sys
from functools import cached_property
from sys import exit

from .lms import LMSFactory
from .repl.console import REPLConsole
from .utils.config import load_config
from .utils.marksheet import Marksheet
import shutil


class Marker():
    def __init__(self, args, console=REPLConsole()):
        """
        Initializing the marker requires passing in a dictionary with the 
        following fields:

        ```
        args = {
            'assgn_dir': '...',
               'config': '...',
              'src_dir': '...'
        }
        ```
        Optionally, also pass in a `Console` object to handle errors/progress.
        """
        config_path = args["config"]
        try:
            self.cfg = load_config(config_path)
            console.log(f"Config Loaded")
        except FileNotFoundError:
            console.error(f"Could not find {config_path}.")
            exit(1)
        self.cfg.update(args)
        self.console = console
    
    @cached_property
    def lms(self):
        lms_instance = LMSFactory.create(self.cfg)
        lms_instance.console = self.console
        return lms_instance    

    def getLMSSubmissionURL(self, user):
        """
        Returns the URL to the submission page on the LMS if the students
        have already been fetched, otherwise `None`.
        """

        # These are cached properties, so we want to make sure that they
        # have already been accessed. We don't want to force-access them
        # since it's not necessary that an LMS is provided, and we don't
        # want to have to require it.
        if "lms" not in self.__dict__ or "mapping" not in self.lms.__dict__:
            return None
        
        return self.lms.submissionURL(user)

    @property
    def candidates_dir(self):
        return os.path.join(self.cfg["assgn_dir"], "candidates")

    @property
    def marksheet_path(self):
        return os.path.join(self.cfg["assgn_dir"], self.cfg["marksheet"])

    def getMarksheet(self):
        marksheet_path = os.path.join(self.cfg["assgn_dir"], self.cfg["marksheet"])
        if not os.path.exists(marksheet_path):
            self.console.error(marksheet_path, "file not found.")
            return Marksheet()
        return Marksheet(marksheet_path)
    
    def getStudentDir(self, student):
        student_dir = os.path.join(self.cfg["assgn_dir"], "candidates", student)
        if not os.path.exists(student_dir):
            self.console.error(student_dir, "dir not found. Stopping.")
            return None
        return student_dir

    def clean(self):
        """
        Delete all submissions / marking data. Be careful when using this!
        """
        if os.path.isdir(self.candidates_dir):
            shutil.rmtree(self.candidates_dir)
        if os.path.isfile(self.marksheet_path):
            os.remove(self.marksheet_path)


    # Import in the specific command handlers...

    from .commands.delete_reports import delete_reports
    from .commands.download import download
    from .commands.prepare import prepare
    from .commands.run import run
    from .commands.set_status import set_status
    from .commands.stats import stats
    from .commands.upload_marks import upload_marks
    from .commands.upload_reports import upload_reports
