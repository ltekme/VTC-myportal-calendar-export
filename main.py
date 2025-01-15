from icalendar import Calendar, Event, vCalAddress, vText
from datetime import datetime
import pytz
import json
from urllib.parse import urljoin
from selenium.webdriver.common.by import By
from selenium.webdriver import Chrome
import os
from selenium.webdriver.chrome.options import Options


DATA_DIR = "data"

if not os.path.exists(DATA_DIR):
    os.mkdir(DATA_DIR)

MYPORTAL_BASE_URL = 'https://myportal.vtc.edu.hk'
CALENDAR_START_DATE = '20250101'
CALENDAR_END_DATE = '20250500'
CALENDAR_EVENTS_FILE = 'calendar_events.json'
CALENDAR_EXPORT_FILE = 'calendar_export.ics'

CALENDAR_EVENTS_FILE = os.path.join(DATA_DIR, CALENDAR_EVENTS_FILE)
CALENDAR_EXPORT_FILE = os.path.join(DATA_DIR, CALENDAR_EXPORT_FILE)


chrome_broswer = Chrome(options=Options())
chrome_broswer.get(MYPORTAL_BASE_URL)

input("Press Enter after login")

chrome_broswer.find_element(By.LINK_TEXT, 'Calendar').click()

# Get Feed URL
calender_feed_url = chrome_broswer.execute_script("return eventFeedUrl;")
calender_feed_url = urljoin(MYPORTAL_BASE_URL, calender_feed_url)
calender_feed_url = f'{calender_feed_url}&from={
    CALENDAR_START_DATE}&to={CALENDAR_END_DATE}'

chrome_broswer.get(calender_feed_url)


calendar_events = chrome_broswer.find_element(By.TAG_NAME, 'pre').text
calendar_events = json.loads(calendar_events)

calendar_events = list(filter(
    lambda e: e['eventType'] != 'Holiday',
    calendar_events
))
calendar_events = list(filter(
    lambda e: e['eventType'] != 'InstitutionHoliday',
    calendar_events
))


with open(CALENDAR_EVENTS_FILE, 'w') as f:
    json.dump(calendar_events, f, indent=4)

calendar_events = json.load(open(CALENDAR_EVENTS_FILE))


cal = Calendar()

for event in calendar_events:

    # adjust time to UTC
    local = pytz.timezone("Asia/Hong_Kong")
    start = datetime.strptime(
        event['startDateTime'], "%Y%m%dT%H%M%S")
    start = local.localize(start, is_dst=None).astimezone(pytz.utc)
    end = datetime.strptime(event['endDateTime'], "%Y%m%dT%H%M%S")
    end = local.localize(end, is_dst=None).astimezone(pytz.utc)

    ical_event = Event()
    # add event details
    ical_event.add('summary', f'{event["summary"]} <BOT>')
    ical_event.add('description',
                   f"{event['details']}\n\nLast updated by MYPORTAL_iCALENDER_BOT@{datetime.now()}")
    ical_event.add('categories', event['eventType'])
    ical_event.add('dtstart', start)
    ical_event.add('dtend', end)

    # add bot as the organizer
    organizer = vCalAddress('MAILTO:VTC_MYPORTAL_iCAL_BOT@example.com')
    organizer.params['cn'] = vText('MYPORTAL_iCAL_BOT')
    organizer.params['role'] = vText('BOT')
    ical_event['organizer'] = organizer

    # add location of the event
    ical_event['location'] = vText(event['location'])

    cal.add_component(ical_event)


with open(CALENDAR_EXPORT_FILE, 'wb') as f:
    f.write(cal.to_ical())
