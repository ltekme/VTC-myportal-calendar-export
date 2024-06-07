import pytz

from icalendar import Calendar, Event, vCalAddress, vText
from datetime import datetime


def create_ical_event(calender_events: dict) -> Event:
    # adjust time to UTC
    local = pytz.timezone("Asia/Hong_Kong")
    start = datetime.strptime(
        calender_events['startDateTime'], "%Y%m%dT%H%M%S")
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


def create_ical(events: list, export_file: str):
    # init calender
    cal = Calendar()

    # add event to calender
    for event in events:
        print('Creating event: {} - {}'.format(
            event["details"].replace("\n", " -> "), event["startDateTime"]))
        cal.add_component(create_ical_event(event))

    # save the calender
    print('using file: ', export_file)
    with open(export_file, 'wb') as f:
        f.write(cal.to_ical())
