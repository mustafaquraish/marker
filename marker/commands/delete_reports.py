#! /usr/bin/env python3

import os
import aiohttp
import asyncio

from ..utils import pushd
from ..utils import config
from ..lms import LMS_Factory

async def delete_report_dispatch(lms, student=None):
    '''
    Given a student's identifier, delete their report file to LMS. Assumes
    the working directory is the root of the assignment directory
    '''
    students = lms.students if student is None else [ student ]
    async with aiohttp.ClientSession() as session:
        tasks = [lms.delete_report(session, student) for student in students]
        await asyncio.gather(*tasks, return_exceptions=True)


def delete_report_handler(cfg, lms, student):
    asyncio.run(delete_report_dispatch(lms, student))
    print("Done.")