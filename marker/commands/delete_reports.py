#! /usr/bin/env python3

import os
import aiohttp
import asyncio

from ..utils import pushd
from ..utils import config
from ..lms import LMS_Factory
from ..utils.console import console


async def delete_report_dispatch(lms, student=None):
    '''
    Given a student's identifier, delete their report file to LMS. Assumes
    the working directory is the root of the assignment directory
    '''
    students = lms.students if student is None else [ student ]
    connector = aiohttp.TCPConnector(limit=10)
    async with aiohttp.ClientSession(connector=connector) as session: 
        tasks = [lms.delete_report(session, student) for student in students]
        await console.track_async(tasks, "Deleting reports")


def delete_report_handler(cfg, lms, student):
    asyncio.run(delete_report_dispatch(lms, student))
