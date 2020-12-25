from .utils import config
from .utils.marksheet import Marksheet
from .utils import pushd

from .lms import LMS_Factory

from .commands.download import download_handler
from .commands.prepare import prepare_handler
from .commands.run import run_handler
from .commands.upload_marks import upload_mark_handler
from .commands.upload_reports import upload_report_handler
from .commands.delete_reports import delete_report_handler

from functools import cached_property

import asyncio

class Marker():
    def __init__(self, args):
        print("Loading config...")
        config_path = args["config"]
        self.cfg = config.load(config_path)
        self.cfg.update(args)
    
    @cached_property
    def lms(self):
        return LMS_Factory(self.cfg)

    def download_submissions(self, student=None):
        return download_handler(self.cfg, self.lms, student)

    def prepare(self, student=None):
        return prepare_handler(self.cfg, student)

    def run(self, student=None, recompile=False, all=False):
        """
        Run takes in some additional arguments to augment behaviour such as
        forcing recompilation and running for all students.
        """
        new_cfg = self.cfg.copy()
        new_cfg['all'] = all
        new_cfg['recompile'] = recompile
        return run_handler(new_cfg, student)
    
    def upload_reports(self, student=None):
        return upload_report_handler(self.cfg, self.lms, student)

    def upload_marks(self, student=None):
        return upload_mark_handler(self.cfg, self.lms, student)

    def delete_reports(self, student=None):
        return delete_report_handler(self.cfg, self.lms, student)
