#! /usr/bin/env python3

import os

import aiohttp
import asyncio

from ..utils import config
from ..utils import pushd
from ..lms import LMS_Factory

from tqdm import tqdm

# Handler to download submission for each process
async def download_dispatch(lms, student=None):
    '''
    Given a student's identifier, make their directory and download file(s).
    '''
    students = lms.students if student is None else [ student ]
    async with aiohttp.ClientSession() as session:
        tasks = [lms.download_submission(session, student) for student in students]
        await asyncio.gather(*tasks, return_exceptions=True)

# -----------------------------------------------------------------------------

def download_handler(cfg, lms, student=None):
    print("Making directory structure...")
    candidates_dir = f'{cfg["assgn_dir"]}/candidates'
    os.makedirs(candidates_dir, exist_ok=True)

    with pushd(candidates_dir):
        asyncio.run(download_dispatch(lms, student))
