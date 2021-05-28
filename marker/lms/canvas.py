'''
Utilities related to interfacing with Canvas

(C) Mustafa Quraish, 2020
'''
import requests
import aiofiles
from functools import cached_property
import os

from .base import LMS
from ..utils.token import get_or_prompt_token

class Canvas(LMS):

    def __init__(self, config):
        self.base_url = config['base_url']
        self.course_id = config['course']
        self.assgn_id = config['assignment']
        self.cfg = config
        super().__init__("canvas", self.base_url)


    # -------------------------------------------------------------------------
    #       Internal Utils
    # -------------------------------------------------------------------------

    @cached_property
    def header(self):
        return {"Authorization": "Bearer " + self.token}

    # -------------------------------------------------------------------------

    def submissionURL(self, student):
        if "mapping" not in self.__dict__:
            return None
        if student not in self.mapping:
            return None
        userid = self.mapping[student]
        url = f"{self.base_url}/courses/{self.course_id}/gradebook/" + \
              f"speed_grader?assignment_id={self.assgn_id}&" + \
              f"student_id={userid}"
        return url


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
                if 'email' in user:
                    userid = user['email'].split('@')[0]
                    mapping[userid] = user['id']
                elif 'login_id' in user:
                    mapping[user['login_id']] = user['id']
                elif 'sis_user_id' in user:
                    mapping[user['sis_user_id']] = user['id']
                else:
                    self.console.error(f"User entry: {user}")
                    raise Exception("No suitable column found in canvas data")

            page += 1

        return mapping

    # -------------------------------------------------------------------------

    def get_newest_submission(self, submission):
        result = None

        if not submission["late"] or self.cfg["allow_late"]:
            if "attachments" in submission:
                result = submission

        if result is not None:
            return result

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
                            result = sub
                            latest_date = sub["submitted_at"]
        return result


    async def download_attachment(self, session, file_url, student, filename):
        async with session.get(file_url, data={}, headers=self.header) as resp:
            content = await resp.content.read()
            file_path = os.path.join(student, filename)
            os.makedirs(student, exist_ok=True)
            f = await aiofiles.open(file_path, mode='wb')
            await f.write(content)
            await f.close()

    async def handle_download_files(self, session, student, submission):
        """
        Does one of the following based on `config['file_name']`:
            - If it exists, then download first attachment and rename it
            - Otherwise, download all attachments with original filenames
        """

        # If a single filename is specified, we downlod first attachment and rename
        if self.cfg["file_name"] is not None: 
            await self.download_attachment(
                session=session,
                file_url=submission["attachments"][0]["url"],
                student=student,
                filename=self.cfg["file_name"]
            )

        # Otherwise, download all attachments...
        else:
            for attachment in submission["attachments"]:
                await self.download_attachment(
                    session=session,
                    file_url=attachment["url"],
                    student=student,
                    filename=attachment["filename"]
                )
        
        return True

    # -------------------------------------------------------------------------
    #       Functions meant to be exposed
    # -------------------------------------------------------------------------

    @cached_property
    def students(self):
        return self.mapping.keys()

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

        submission = self.get_newest_submission(res)
        # Found no submissions.
        if submission is None:
            self.console.error(student, "submmission late / not found")
            return False
        
        return await self.handle_download_files(session, student, submission)

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

        report_path = os.path.join(student, self.cfg["report"])

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
            self.console.error(student+":", res['errors'][0]['message'])
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
        data = { "comment[file_ids][]": file_id }
        if self.cfg["submission_comment"] is not None:
            data["comment[text_comment]"] = self.cfg["submission_comment"]

        async with session.put(url, data=data, headers=self.header) as resp:
            res = await resp.json()
        
        if res.get('error') or res.get('errors'):
            self.console.error(student, "error attaching file to comment")
            return False

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
            self.console.error(f'{student}:', res['errors'][0]['message'])
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


from difflib import SequenceMatcher

def findBestAttachment(self, filename, submission):
    s = SequenceMatcher()
    s.set_seq2(filename)
    result = []
    for attachment in submission["attachments"]:
        s.set_seq1(attachment["filename"])
        result.append((s.ratio(), attachment))
    return max(result)[1]



