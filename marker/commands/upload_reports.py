#! /usr/bin/env python3

import os
import aiohttp
import asyncio

from ..utils import pushd
from ..utils import config
from ..lms import LMS_Factory

async def upload_report_dispatch(lms, student=None):
    '''
    Given a student's identifier, upload their report file to LMS. Assumes
    the working directory is the root of the assignment directory
    '''
    students = sorted(os.listdir()) if student is None else [ student ]
    async with aiohttp.ClientSession() as session:
        tasks = [lms.upload_report(session, student) for student in students]
        await asyncio.gather(*tasks, return_exceptions=True)


def upload_report_handler(cfg, lms, student):
    candidates_dir = f'{cfg["assgn_dir"]}/candidates'
    with pushd(candidates_dir):
        asyncio.run(upload_report_dispatch(lms, student))
    print("Done.")