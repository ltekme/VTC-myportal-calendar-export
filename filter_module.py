import json
import os
from dotenv import load_dotenv

from calender import create_ical

# default
CALENDER_FILTER_MODULE = 'ITP4927'
CALENDER_EVENTS_FILE = 'calender_events.json'
CALENDER_FILTERED_EVENTS_FILE = f'{CALENDER_FILTER_MODULE}_events.json'
CALENDER_FILTERED_EXPORT_FILE = f'{CALENDER_FILTER_MODULE}_events.ics'

# attemps load envs
if os.path.exists('.config'):
    load_dotenv('.config')

# overide with env
CALENDER_FILTER_MODULE = os.environ.get(
    'CALENDER_FILTER_MODULE', CALENDER_FILTER_MODULE)
CALENDER_EVENTS_FILE = os.environ.get(
    'CALENDER_EVENTS_FILE', CALENDER_EVENTS_FILE)
CALENDER_FILTERED_EVENTS_FILE = os.environ.get(
    'CALENDER_FILTERED_EVENTS_FILE', CALENDER_FILTERED_EVENTS_FILE)
CALENDER_FILTERED_EXPORT_FILE = os.environ.get(
    'CALENDER_FILTERED_EXPORT_FILE', CALENDER_FILTERED_EXPORT_FILE)


def main(event_file: str, filtered_event_file: str):
    '''
    Filter 'summary' from event_file
    Export filtered events to filtered_event_file
    '''

    # get events from json
    events = json.load(open(event_file))

    # filter events
    filtered_events = list(
        filter(lambda x: CALENDER_FILTER_MODULE in x['summary'], events))

    # save filtered json
    with open(filtered_event_file, 'w') as f:
        json.dump(filtered_events, f, indent=4)

    # create ical
    create_ical(filtered_events, CALENDER_FILTERED_EXPORT_FILE)


# main executalbe
if __name__ == '__main__':
    main(CALENDER_EVENTS_FILE, CALENDER_FILTERED_EVENTS_FILE)
