#! /usr/bin/env python3

import os
import aiohttp
import asyncio

from ..utils.marksheet import Marksheet
from ..utils import config
from ..lms import LMS_Factory


async def upload_mark_dispatch(lms, marksheet, student=None):
    '''
    Given a student's identifier, upload their report file to LMS. Assumes
    the working directory is the root of the assignment directory
    '''
    students = lms.students if student is None else [ student ]
    async with aiohttp.ClientSession() as session:
        tasks = [lms.upload_mark(session, student, marksheet[student]) for student in students]
        await asyncio.gather(*tasks, return_exceptions=True)


def upload_mark_handler(cfg, lms, student):
    marksheet_path = f'{cfg["assgn_dir"]}/{cfg["marksheet"]}'
    if not os.path.exists(marksheet_path):
        print(marksheet_path, "file not found. Stopping.")
        return

    marksheet = Marksheet(marksheet_path)
    asyncio.run(upload_mark_dispatch(lms, marksheet, student))
    print("Done.")