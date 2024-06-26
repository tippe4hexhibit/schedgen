import logging

from datetime import datetime
from datetime import timezone
from zoneinfo import ZoneInfo

log = logging.getLogger(__name__)


def _abbreviate_type(str_val):
    return ''.join([x for x in str_val.lower() if x not in [*' /-_&aeiou']])


class FullSchedule:
    def __init__(self, schedule_data):
        log.info(f'Initializing {self.__class__}')

        # Create our schedule attribute and add a holder
        # for the full schedule
        self.schedules = {
            'Full Schedule': Schedule('Full Schedule')
        }

        sorted_schedule_data = list(
            sorted(
                schedule_data,
                key=lambda item: item['fields']['Event Start']
            )
        )

        for event in sorted_schedule_data:
            if 'fields' in event:
                if 'Event Type' in event['fields'].keys():
                    for event_type in ['Full Schedule'] + event['fields']['Event Type']:
                        # Create a new schedule based on a new Event Type
                        if event_type not in self.schedules:
                            self.schedules[event_type] = Schedule(event_type)

                        # Decipher the date, so we can use it as a key name
                        event_start = datetime.fromisoformat(event['fields']['Event Start'][:-1])
                        event_start = event_start.replace(tzinfo=timezone.utc) \
                            .astimezone(tz=ZoneInfo('US/Eastern'))
                        event_end = None
                        if 'Event End' in event['fields']:
                            event_end = datetime.fromisoformat(event['fields']['Event End'][:-1])
                            event_end = event_end.replace(tzinfo=timezone.utc) \
                                .astimezone(ZoneInfo('US/Eastern'))

                        # Rewrite our column names so they are Python variable
                        # names
                        fields = {x.lower().replace(' ', '_'): y
                                  for x, y in event['fields'].items()}

                        # Reload timezone adjusted ISO dates
                        fields['event_start'] = event_start.isoformat(sep='T', timespec='auto')

                        # Inject in some human-readable time attributes
                        fields['event_start_date'] = event_start.date().isoformat()
                        fields['event_start_time'] = event_start.time().strftime("%-I:%M %p").lower()

                        # Only show ends if they exist, and if they are on the same day
                        # (works around for not wanting to broadcast a Carnival end time)
                        log.info(f'Event start date: {event_start.date()}')
                        if event_end:
                            log.info(f'Event end date: {event_end.date()}')
                        if event_end and event_end.date() == event_start.date():
                            fields['event_end_time'] = event_end.time().strftime("%-I:%M %p").lower()
                            # Reload timezone adjusted ISO dates
                            fields['event_end'] = event_end.isoformat(sep='T', timespec='auto')

                        # Fix up the venue and location attributes, so they're not in a list
                        if 'venue_name' in fields and type(fields['venue_name']) == list:
                            fields['venue_name'] = ', '.join(fields['venue_name'])
                        if 'location' in fields and type(fields['location']) == list:
                            fields['location'] = ','.join(fields['location'][0])

                        # Add the event to the relevant schedule objects
                        self.schedules[event_type].add_event(event_start.date().isoformat(), **fields)

    def get_schedules(self):
        return self.schedules


class Schedule:
    def __init__(self, schedule_type):
        log.info(f'Initializing {self.__class__}')
        self.schedule_type = schedule_type
        self.schedule_abbreviation = _abbreviate_type(schedule_type)
        self.event_dates = {}
        log.info(f"Class initialized for '{self.schedule_type}'")

    def add_event(self, event_date, **kwargs):

        if event_date not in self.event_dates:
            self.event_dates[event_date] = {}

        entry = {}

        if 'event_start_time' in kwargs.keys():
            event_start_time = kwargs['event_start_time']
        else:
            kwargs['event_start_time'] = "Start Time Not Set"
            event_start_time = kwargs['event_start_time']

        if event_start_time not in self.event_dates[event_date]:
            log.info(f'Creating a dict for "{event_start_time} in "{event_date}" type {self.schedule_type}')
            self.event_dates[event_date][event_start_time] = {}

        if 'venue_name' in kwargs.keys():
            venue_name = kwargs['venue_name']
        else:
            kwargs['venue_name'] = 'Venue Not Assigned'
            venue_name = kwargs['venue_name']

        if venue_name not in self.event_dates[event_date][event_start_time]:
            log.info(f'Creating a list for "{venue_name}" in "{event_start_time}" for "{event_date}" type "{self.schedule_type}"')
            self.event_dates[event_date][event_start_time][venue_name] = []

        for key, value in kwargs.items():
            entry[key] = value

        log.info(f'Inserting event {entry["event_name"]} on {event_date} at {event_start_time} in {venue_name} type {self.schedule_type}')
        self.event_dates[event_date][event_start_time][venue_name].insert(0, entry)

    def get_events(self):
        return self.event_dates

    def __str__(self):
        pretty_string = f"Schedule for {self.schedule_type}"
        for data in self.event_dates:
            pretty_string += f'\n{data}: {self.event_dates[data]}'

        return pretty_string

