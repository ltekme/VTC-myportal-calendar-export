
import os
import json
import pytz

from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


from icalendar import Calendar, Event, vCalAddress, vText
from datetime import datetime
from urllib.parse import urljoin
from dotenv import load_dotenv


MYPORTAL_BASE_URL = 'https://myportal.vtc.edu.hk'

# User defined parameters
CALENDER_START_DATE = '20240601'
CALENDER_END_DATE = '20240731'
CALENDER_EVENTS_FILE = 'calender_events.json'
CALENDER_EXPORT_FILE = f'myportal_bot-{datetime.now(pytz.timezone("Asia/Hong_Kong")).strftime("%d%m%Y%H%M%S")}-{CALENDER_START_DATE}_{CALENDER_END_DATE}.ics'

# load envs
if os.path.exists('.config'):
    load_dotenv('.config')

# follow environ
CALENDER_CNA = os.environ.get('CALENDER_CNA', None)
CALENDER_PASSWORD = os.environ.get('CALENDER_PASSWORD', None)


def create_ical_event(calender_events: dict) -> Event:
    # adjust time to UTC
    local = pytz.timezone("Asia/Hong_Kong")
    start = datetime.strptime(calender_events['startDateTime'], "%Y%m%dT%H%M%S")
    start = local.localize(start, is_dst=None).astimezone(pytz.utc)
    end = datetime.strptime(calender_events['endDateTime'], "%Y%m%dT%H%M%S")
    end = local.localize(end, is_dst=None).astimezone(pytz.utc)

    event = Event()
    # add event details
    event.add('summary', f'{calender_events["summary"]} <BOT>')
    event.add('description',
              f"{calender_events['details']}\n\nLast updated by MYPORTAL_iCALENDER_BOT@{datetime.now()}")
    event.add('categories', calender_events['eventType'])
    event.add('dtstart', start)
    event.add('dtend', end)

    # add bot as the organizer
    organizer = vCalAddress('MAILTO:VTC_MYPORTAL_iCAL_BOT@example.com')
    organizer.params['cn'] = vText('MYPORTAL_iCAL_BOT')
    organizer.params['role'] = vText('BOT')
    event['organizer'] = organizer

    # add location of the event
    event['location'] = vText(calender_events['location'])

    return event


def get_calender_events(browser: Chrome) -> dict:
    # click on the calendar
    browser.find_element(By.LINK_TEXT, 'Calendar').click()

    # get url from calender
    calender_feed_url = browser.execute_script("return eventFeedUrl;")
    calender_feed_url = urljoin(MYPORTAL_BASE_URL, calender_feed_url)
    calender_feed_url = f'{calender_feed_url}&from={CALENDER_START_DATE}&to={CALENDER_END_DATE}'

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
            login.find_element(By.NAME, 'password').send_keys(CALENDER_PASSWORD)
            # submit
            login.submit()
        else:
            # wait for login from the broswer for 600 seconds
            WebDriverWait(browser, 600).until(EC.url_changes(browser.current_url))

        # save events to file
        calender_events = get_calender_events(browser)
        with open(CALENDER_EVENTS_FILE, 'w') as f:
            json.dump(calender_events, f, indent=4)

        # close the browser
        print('Calender events saved to file. Closing broswer.')
        browser.quit()

    # read events from file
    calender_events = json.load(open(CALENDER_EVENTS_FILE))

    # filter holiday
    calender_events = [x for x in calender_events if x['eventType'] != 'Holiday']
    calender_events = [x for x in calender_events if x['eventType'] != 'InstitutionHoliday']

    # save events to file
    json.dump(calender_events, open(CALENDER_EVENTS_FILE, 'w'), indent=4)

    cal = Calendar()

    # put events into ics file
    for event in calender_events:
        print('Creating event: {} - {}'.format(event["details"].replace("\n", " -> "), event["startDateTime"]))
        cal.add_component(create_ical_event(event))

    with open(CALENDER_EXPORT_FILE, 'wb') as f:
        f.write(cal.to_ical())


if __name__ == '__main__':
    main()
