'''
Utilities related to interfacing with Canvas

(C) Mustafa Quraish, 2020
'''
import requests
import os


class Canvas():

    # -------------------------------------------------------------------------

    def __init__(self, config):
        self.base_url = config['base_url']
        self.course_id = config['course']
        self.assgn_id = config['assignment']
        self.cfg = config
        self.mapping = None
        self._get_token()
        self.header = {"Authorization": "Bearer " + self.token}

    # -------------------------------------------------------------------------
    #       Internal Utils
    # -------------------------------------------------------------------------

    def _get_token(self):
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
                self.token = tokens_dict[self.base_url]
                return

        token = input("Enter Canvas Token: ").strip()
        prompt = input(f"Save token in {token_path} ?: [Y]/n")
        if 'n' not in prompt.lower():
            with open(token_path, 'a') as token_file:
                token_file.write(f'{self.base_url},{token}\n')
    
        self.token = token

    # -------------------------------------------------------------------------

    def _get_mapping(self):
        if self.mapping is not None:
            return

        print("- Fetching course users...", end="", flush=True)

        url = f'{self.base_url}/api/v1/courses/{self.course_id}/users'
        page, res = 1, None

        self.mapping = {}

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
                    self.mapping[user['login_id']] = user['id']
                elif 'sis_user_id' in user:
                    self.mapping[user['sis_user_id']] = user['id']
                elif 'email' in user:
                    userid = user['email'].split('@')[0]
                    self.mapping[userid] = user['id']
                else:
                    raise Exception("No suitable column found in canvas data")
            page += 1
            print(".", end="", flush=True)

        print()
        return

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
                if sub["submitted_at"] > latest_date:
                    if "attachments" in sub:
                        file_url = sub["attachments"][0]["url"]
                        latest_date = sub["submitted_at"]

        return file_url

    # -------------------------------------------------------------------------
    #       Functions meant to be exposed
    # -------------------------------------------------------------------------

    def students(self):
        self._get_mapping()
        return self.mapping.keys()

    # -------------------------------------------------------------------------

    def get_mapping(self):
        self._get_mapping()
        return self.mapping

    # -------------------------------------------------------------------------

    def student_exists(self, student):
        self._get_mapping()
        return student in self.mapping

    # -------------------------------------------------------------------------

    def upload_report(self, student_id, report_path):
        '''
        Upload a file to the comments section of a given assignment for the 
        given student_id
        '''
        self._get_mapping()
        if student_id not in self.mapping:
            raise ValueError(f"{student_id} not in the course.")

        canvas_id = self.mapping[student_id]

        url = (f"{self.base_url}/api/v1/courses/{self.course_id}"
               f"/assignments/{self.assgn_id}/submissions/{canvas_id}"
               f"/comments/files")

        file_size = os.path.getsize(report_path)
        data = {
            "name": report_path,
            "size": file_size,
            "content_type": "text/html",
            "parent_folder_path": "My Files/reports"
        }

        res = requests.post(url, data=data, headers=self.header).json()

        if res.get('error') or res.get('errors'):
            return False

        url = res.get('upload_url')
        data = {"file": open(report_path, 'rb')}

        res = requests.post(url, files=data, headers=self.header).json()
        if (res.get('error')):
            return False

        url = res.get('location')
        res = requests.get(url, headers=self.header).json()
        if (res.get('upload_status') != "success"):
            return False

        file_id = res.get('id')
        url = (f"{self.base_url}/api/v1/courses/{self.course_id}/"
               f"assignments/{self.assgn_id}/submissions/{canvas_id}")

        data = {"comment[file_ids][]": file_id}
        res = requests.put(url, data=data, headers=self.header).json()

        return True

    # -------------------------------------------------------------------------

    def download_submission(self, student_id, student_dir):
        self._get_mapping()
        if student_id not in self.mapping:
            raise ValueError(f"{student_id} not in the course.")
        canvas_id = self.mapping[student_id]

        url = (f"{self.base_url}/api/v1/courses/{self.course_id}/"
               f"assignments/{self.assgn_id}/submissions/{canvas_id}")
        data = {"include[]": "submission_history"}
        res = requests.get(url, data=data, headers=self.header).json()

        if res.get('error') or res.get('errors'):
            return False

        file_url = self._get_file_url(res)

        # Found no submissions.
        if file_url is None:
            return False

        res = requests.get(file_url, data={}, headers=self.header)
        # Assuming no errors returned for now...
        file_name = self.cfg["file_name"]
        open(f'{student_dir}/{file_name}', 'wb').write(res.content)

        return True

    # -------------------------------------------------------------------------

    def upload_mark(self, student_id, mark_list):
        self._get_mapping()
        if student_id not in self.mapping:
            raise ValueError(f"{student_id} not in the course.")
        canvas_id = self.mapping[student_id]

        url = (f"{self.base_url}/api/v1/courses/{self.course_id}/"
               f"assignments/{self.assgn_id}/submissions/{canvas_id}")

        # For Canvas, we can only submit one numerical mark. Take the sum:
        mark = sum(mark_list)

        data = {"submission[posted_grade]": f"{mark}"}
        res = requests.put(url, data=data, headers=self.header).json()

        if res.get('error') or res.get('errors'):
            return False

        return True

# -----------------------------------------------------------------------------
