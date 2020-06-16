import sys
import time

from marker.lms import LMS_Factory
from marker.utils import config
try:
    from selenium import webdriver
    from selenium.common.exceptions import TimeoutException
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.chrome.options import Options
except ImportError:
    print("This script is not part of the official suite and expects you to "
          "have selenium installed with the Chrome driver. Please install "
          "these yourself before proceeding.")
    sys.exit(1)

import getpass

if len(sys.argv) != 2:
    print("Please enter to config. file as an argument.")
    sys.exit(1)

# -----------------------------------------------------------------------------

cfg = config.load(sys.argv[1])
assert(cfg['lms'].lower() == "canvas")
cv = LMS_Factory(cfg)

utorid = input("Enter UtorID: ")
password = getpass.getpass(prompt='Enter Password: ', stream=None) 

base = f'{cfg["base_url"]}/courses/{cfg["course"]}/gradebook/speed_grader' +\
       f'?assignment_id={cfg["assignment"]}&student_id='

chrome_options = Options()  
chrome_options.add_argument("--headless")  

driver = webdriver.Chrome(options=chrome_options)

# -----------------------------------------------------------------------------

max_timeout = 10

print("Attempting login... If this takes long your credentials may be wrong.")

# Let user log in first to avoid timing out the speedgrader.
driver.get(cfg["base_url"])
driver.find_element_by_id("username").send_keys(utorid)
driver.find_element_by_id("password").send_keys(password)
driver.find_element_by_xpath("/html/body/div/div/div[1]/div[2]/form/button").click()

try:
    # If we see the dashboard, successful login. Otherwise, exit for now.
    exist = EC.presence_of_element_located((By.ID, 'dashboard'))
    WebDriverWait(driver, max_timeout).until(exist)

except TimeoutException:
    print("Error logging in. Exiting")
    sys.exit(1)

# -----------------------------------------------------------------------------

config_report_name = cfg["report"]

for (student, student_id) in cv.get_mapping().items():
    url = base + str(student_id)

    print(f"Loading {student} ... ", end="", flush=True)
    driver.get(url)
    # Wait till the comments section has loaded.
    try:
        # This will take a while if the comment does not exist :(
        # - Checking for the container doesn't work, seems to load first...
        exist = EC.presence_of_element_located((By.CLASS_NAME, 'comment'))
        WebDriverWait(driver, max_timeout).until(exist)

    except TimeoutException:
        print("timed out. Skipping ... ")
        continue


    comments_list = driver.find_elements_by_class_name("comment")
    for comment in comments_list:
        display_names = comment.find_elements_by_class_name("display_name")

        # Assuming only one attachment per comment.
        if len(display_names) > 0:
            report_name = display_names[0].text

            if (report_name != config_report_name):
                print("Skipping...")
                continue
            
            print(f"found {report_name}. Deleting...")   
            found = True 
            
            del_link = comment.find_element_by_class_name("delete_comment_link")
            del_link.click()
            # Move to the alert and accept the deletion it.
            alert = driver.switch_to.alert
            alert.dismiss()
            # alert.accept()

    if not found:
        print("no matching report found.")

# -----------------------------------------------------------------------------

print("Done.")
# time.sleep(3)
driver.quit()
