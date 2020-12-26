#! /usr/bin/env python3

import os

import aiohttp
import asyncio

from ..utils import config
from ..utils import pushd
from ..utils.marksheet import Marksheet
from ..lms import LMS_Factory
from ..utils.log import progress_futures, console


# Handler to download submission for each process
async def download_dispatch(lms, student=None):
    '''
    Given a student's identifier, make their directory and download file(s).
    '''
    students = lms.students if student is None else [ student ]
    connector = aiohttp.TCPConnector(limit=10)
    async with aiohttp.ClientSession(connector=connector) as session: 
        tasks = [lms.download_submission(session, student) for student in students]
        await progress_futures(tasks, "Downloading submissions")

# -----------------------------------------------------------------------------

def download_handler(cfg, lms, student=None, allow_late=False):
    console.log("Making directory structure")
    candidates_dir = f'{cfg["assgn_dir"]}/candidates'
    os.makedirs(candidates_dir, exist_ok=True)

    lms.cfg["allow_late"] = allow_late

    with pushd(candidates_dir):
        asyncio.run(download_dispatch(lms, student))
    
    # Create a blank marksheet.
    marksheet_path = f'{cfg["assgn_dir"]}/{cfg["marksheet"]}' 
    if not os.path.exists(marksheet_path):
        console.log("Creating marksheet")
        marksheet = Marksheet()
        students_list = sorted(os.listdir(candidates_dir))
        marksheet.add_students(students_list)
        marksheet.save(marksheet_path)
