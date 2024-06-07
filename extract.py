
import os
import json
import pytz

from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from urllib.parse import urljoin
from dotenv import load_dotenv
from datetime import datetime

from calender import create_ical

MYPORTAL_BASE_URL = 'https://myportal.vtc.edu.hk'

# User defined parameters
CALENDER_START_DATE = '20240516'
CALENDER_END_DATE = '20240730'
CALENDER_EVENTS_FILE = 'calender_events.json'
CALENDER_EXPORT_FILE = 'calender_export.ics'

# attemps load envs
if os.path.exists('.config'):
    load_dotenv('.config')

# follow environ
CALENDER_EXPORT_FILE = os.environ.get(
    'CALENDER_EXPORT_FILE', CALENDER_EXPORT_FILE)
CALENDER_EVENTS_FILE = os.environ.get(
    'CALENDER_EVENTS_FILE', CALENDER_EVENTS_FILE)
CALENDER_START_DATE = os.environ.get(
    'CALENDER_START_DATE', CALENDER_START_DATE)
CALENDER_END_DATE = os.environ.get('CALENDER_END_DATE', CALENDER_END_DATE)
CALENDER_PASSWORD = os.environ.get('CALENDER_PASSWORD', None)
CALENDER_CNA = os.environ.get('CALENDER_CNA', None)


def get_calender_events(browser: Chrome) -> dict:
    # click on the calendar
    browser.find_element(By.LINK_TEXT, 'Calendar').click()

    # get url from calender
    calender_feed_url = browser.execute_script("return eventFeedUrl;")
    calender_feed_url = urljoin(MYPORTAL_BASE_URL, calender_feed_url)
    calender_feed_url = f'{calender_feed_url}&from={
        CALENDER_START_DATE}&to={CALENDER_END_DATE}'

    # print and open the url
    browser.get(calender_feed_url)

    # parse content into json
    calender_events = browser.find_element(By.TAG_NAME, 'pre').text
    calender_events = json.loads(calender_events)

    return calender_events


def main():
    # open myportal to get calender information
    if not os.path.exists(CALENDER_EVENTS_FILE):

        # open the browser in incognito mode
        options = Options()
        options.add_argument("--incognito")

        # open myportal
        browser = Chrome(options=options)
        browser.get(MYPORTAL_BASE_URL)

        # check if login is provided
        if CALENDER_CNA and CALENDER_PASSWORD:
            # get the login form
            login = browser.find_element(By.ID, value='loginform')
            # fill in the form
            login.find_element(By.NAME, 'userid').send_keys(CALENDER_CNA)
            login.find_element(By.NAME, 'password').send_keys(
                CALENDER_PASSWORD)
            # submit
            login.submit()
        else:
            # wait for login from the broswer for 600 seconds
            WebDriverWait(browser, 600).until(
                EC.url_changes(browser.current_url))

        # get events
        calender_events = get_calender_events(browser)

        # filter holiday
        calender_events = list(
            filter(lambda e: e['eventType'] != 'Holiday', calender_events))
        calender_events = list(
            filter(lambda e: e['eventType'] != 'InstitutionHoliday', calender_events))

        # save events to file
        with open(CALENDER_EVENTS_FILE, 'w') as f:
            json.dump(calender_events, f, indent=4)

        # close the browser
        print('Calender events saved to file {}. Closing broswer.'.format(
            CALENDER_EVENTS_FILE))
        browser.quit()

    # read events from file
    calender_events = json.load(open(CALENDER_EVENTS_FILE))

    # create ical file
    create_ical(calender_events, CALENDER_EXPORT_FILE)


if __name__ == '__main__':
    main()
