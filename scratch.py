import config
from lms import LMS_Factory

# Load the configuration and get an instance of the LMS class
cfg = config.load("ex/markus.yaml")
lms = LMS_Factory(cfg)

print(lms.upload_mark('dosanj43', 0))
# print(lms.upload_report('dosanj43', 'automark.txt'))
# print(lms.delete_reports('dosanj43'))
# url=(f'{lms.base_url}/api/v1/courses/{lms.course_id}/assignments/'
#      f'{lms.assgn_id}/submissions/401133/comments')
# import requests
# print(url)
# print(requests.get(url, data={}, headers=lms.header))