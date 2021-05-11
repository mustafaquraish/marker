'''
Utilities related to interfacing with Canvas

(C) Mustafa Quraish, 2020
'''
import requests
import aiofiles
from functools import cached_property
import os

from .lms_base import LMS

class Canvas(LMS):

    # -------------------------------------------------------------------------

    def __init__(self, config):
        self.base_url = config['base_url']
        self.course_id = config['course']
        self.assgn_id = config['assignment']
        self.cfg = config

    # -------------------------------------------------------------------------
    #       Internal Utils
    # -------------------------------------------------------------------------

    @cached_property
    def header(self):
        return {"Authorization": "Bearer " + self.token}

    @cached_property
    def token(self):
        '''
        Try to load Canvas token from file. If it doesn't exist, prompt
        the user and give them an option to save it locally.
        '''
        from pathlib import Path

        token_path = f"{Path.home()}/.canvas.tokens"
        if os.path.exists(token_path):
            lst = [line.split(",") for line in open(token_path).readlines()]
            tokens_dict = { url.strip(): token.strip() for url, token in lst }
            if self.base_url in tokens_dict:
                return tokens_dict[self.base_url]

        token = self.console.get("Enter Canvas Token").strip()
        save = self.console.ask(f"Save token in [red]{token_path}[/red]?", default=True)
        if save:
            with open(token_path, 'a') as token_file:
                token_file.write(f'{self.base_url},{token}\n')
            self.console.log("Access token saved")
    
        return token

    # -------------------------------------------------------------------------

    @cached_property
    def mapping(self):

        self.console.log("Fetching course users")

        url = f'{self.base_url}/api/v1/courses/{self.course_id}/users'
        page, res = 1, None

        mapping = {}

        while (res != []):
            data = {
                'enrollment_type': 'student',
                'per_page': 100,
                'page': page,
            }
            res = requests.get(url, data=data, headers=self.header).json()

            # Pick the field as the identifier. For archived courses, login_id
            # is not always available. This makes it easier to test
            for user in res:
                if 'login_id' in user:
                    mapping[user['login_id']] = user['id']
                elif 'sis_user_id' in user:
                    mapping[user['sis_user_id']] = user['id']
                elif 'email' in user:
                    userid = user['email'].split('@')[0]
                    mapping[userid] = user['id']
                else:
                    raise Exception("No suitable column found in canvas data")
            page += 1

        return mapping

    # -------------------------------------------------------------------------

    def _get_file_url(self, submission):
        file_url = None

        if not submission["late"] or self.cfg["allow_late"]:
            if "attachments" in submission:
                # Assuming only one attachment for now
                file_url = submission["attachments"][0]["url"]

        if file_url is not None:
            return file_url

        # If we're here need to look at submission history
        if "submission_history" not in submission:
            return None

        # Initial default that is earlier than all dates
        latest_date = "0000-00-00T00:00:00Z"

        for sub in submission['submission_history']:
            # Want newest submission that is either not late or allowed to be
            if (not sub["late"]) or self.cfg["allow_late"]:
                if sub["submitted_at"] is not None: 
                    if sub["submitted_at"] > latest_date:
                        if "attachments" in sub:
                            file_url = sub["attachments"][0]["url"]
                            latest_date = sub["submitted_at"]
        return file_url

    # -------------------------------------------------------------------------
    #       Functions meant to be exposed
    # -------------------------------------------------------------------------

    @cached_property
    def students(self):
        return self.mapping.keys()

    # -------------------------------------------------------------------------

    async def upload_report(self, session, student):
        '''
        Upload a file to the comments section of a given assignment for the 
        given student
        '''
        if student not in self.mapping:
            self.console.error(student, "not found in course list")
            return False

        canvas_id = self.mapping[student]
        url = f"{self.base_url}/api/v1/courses/{self.course_id}/assignments/{self.assgn_id}/submissions/{canvas_id}/comments/files"

        report_path = f'{student}/{self.cfg["report"]}'

        if not os.path.isfile(report_path):
            self.console.error(report_path, "doesn't exist.")
            return False

        file_size = os.path.getsize(report_path)
        data = {
            "name": self.cfg["report"],
            "size": file_size,
            "content_type": "text/html",
        }

        async with session.post(url, data=data, headers=self.header) as resp:
            res = await resp.json()

        if res.get('error') or res.get('errors'):
            self.console.error(student, "error adding submission comment file data")
            return False

        url = res.get('upload_url')
        data = {"file": open(report_path, 'rb')}

        async with session.post(url, data=data, headers=self.header) as resp:
            try:
                res = await resp.json()
            except Exception as e:
                self.console.error(student, "error uploading file")
                # self.console.log(url, str(data), self.header)
                return False

        if res.get('error') or res.get('errors'):
            self.console.error(student, "error uploading report file")
            return False

        url = res.get('location')

        # Verify file upload success
        async with session.get(url, headers=self.header) as resp:
            res = await resp.json()

        if (res.get('upload_status') != "success"):
            self.console.error(student, "error uploading report file")
            return False

        file_id = res.get('id')
        url = f"{self.base_url}/api/v1/courses/{self.course_id}/assignments/{self.assgn_id}/submissions/{canvas_id}"
        data = {"comment[file_ids][]": file_id}
        async with session.put(url, data=data, headers=self.header) as resp:
            res = await resp.json()
        
        if res.get('error') or res.get('errors'):
            self.console.error(student, "error attaching file to comment")
            return False

        return True

    # -------------------------------------------------------------------------

    async def download_submission(self, session, student, late=False):
        if student not in self.mapping:
            self.console.error(student, "not found in course list")
            return False

        canvas_id = self.mapping[student]

        url = (f"{self.base_url}/api/v1/courses/{self.course_id}/assignments/{self.assgn_id}/submissions/{canvas_id}")
        data = {"include[]": "submission_history"}

        async with session.get(url, data=data, headers=self.header) as resp:
            res = await resp.json()

        if res.get('error') or res.get('errors'):
            self.console.error(student, "error getting submission details")
            return False

        file_url = self._get_file_url(res)

        # Found no submissions.
        if file_url is None:
            self.console.error(student, "submmission late / not found")
            return False


        async with session.get(file_url, data={}, headers=self.header) as resp:
            content = await resp.content.read()
            file_path = f'{student}/{self.cfg["file_name"]}'
            os.makedirs(student, exist_ok=True)
            f = await aiofiles.open(file_path, mode='wb')
            await f.write(content)
            await f.close()
        
        return True

    # -------------------------------------------------------------------------

    async def upload_mark(self, session, student, mark_list):
        if student not in self.mapping:
            self.console.error(student, "not found in course list")
            return False

        canvas_id = self.mapping[student]
        url = f"{self.base_url}/api/v1/courses/{self.course_id}/assignments/{self.assgn_id}/submissions/{canvas_id}"

        # For Canvas, we can only submit one numerical mark. Take the sum:
        mark = sum(mark_list)

        data = {"submission[posted_grade]": mark}
        async with session.put(url, data=data, headers=self.header) as resp:
            res = await resp.json()

        if res.get('error') or res.get('errors'):
            self.console.error(student, "error uploading marks")
            return False

        return True

# -----------------------------------------------------------------------------

    async def delete_report(self, session, student):
        if student not in self.mapping:
            self.console.error(student, "not found in course list")
            return False

        canvas_id = self.mapping[student]
        url = (f"{self.base_url}/api/v1/courses/{self.course_id}/assignments/{self.assgn_id}/submissions/{canvas_id}")
        data = {"include[]": "submission_comments"}

        async with session.get(url, data=data, headers=self.header) as resp:
            res = await resp.json()

        if res.get('error') or res.get('errors'):
            self.console.error(student, "error getting submission details")
            return False

        for sub_comment in res['submission_comments']:
            if 'attachments' not in sub_comment:
                continue

            comment_id = sub_comment['id']
            comment_url = f"{url}/comments/{comment_id}"

            async with session.delete(comment_url, headers=self.header) as resp:
                res = await resp.json()

            if res.get("error") or res.get("errors"):
                self.console.error(student, "error deleting comment id", comment_id)

        return True

# -----------------------------------------------------------------------------
