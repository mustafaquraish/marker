#! /usr/bin/env python3

import os
import aiohttp
import asyncio

from ..utils.marksheet import Marksheet
from ..utils import config
from ..lms import LMS_Factory
from ..utils.console import console


async def upload_mark_dispatch(lms, marksheet, student=None):
    '''
    Given a student's identifier, upload their report file to LMS. Assumes
    the working directory is the root of the assignment directory
    '''
    students = lms.students if student is None else [ student ]
    connector = aiohttp.TCPConnector(limit=10)
    async with aiohttp.ClientSession(connector=connector) as session:  
        tasks = [lms.upload_mark(session, student, marksheet[student]) for student in students]
        await console.track_async(tasks, "Uploading marks")


def upload_mark_handler(cfg, lms, student):
    marksheet_path = f'{cfg["assgn_dir"]}/{cfg["marksheet"]}'
    if not os.path.exists(marksheet_path):
        console.error(marksheet_path, "file not found. Stopping.")
        return

    console.log("Loading marksheet")
    marksheet = Marksheet(marksheet_path)
    asyncio.run(upload_mark_dispatch(lms, marksheet, student))