import logging

from datetime import datetime

from yaml import load, dump

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

log = logging.getLogger(__name__)


class YamlSchedule:
    def __init__(self, event_schedule):
        self.yamls = {}

        for event_date, schedule in event_schedule.get_events().items():
            time_lookup = {}
            yaml_struct = {
                'longdate': datetime.fromisoformat(event_date).strftime('%A, %B %-d, %Y'),
                'times': []
            }

            for event_start_time, venue in schedule.items():
                for venue_name, events in venue.items():
                    for event in events:
                        if event_start_time not in time_lookup.keys():
                            time_lookup[event_start_time] = len(yaml_struct['times'])
                            yaml_struct['times'].append({
                                'time': event_start_time,
                                'venues': {}
                            })

                        if venue_name not in yaml_struct['times'][time_lookup[event_start_time]]['venues'].keys():
                            yaml_struct['times'][time_lookup[event_start_time]]['venues'][venue_name] = []

                        event_dict = {
                            'event_name': event['event_name'].strip()
                        }

                        # Add some attributes to the event to add context on the webpage
                        if 'description' in event.keys():
                            event_dict['description'] = event['description'].strip().replace('\n', ' ')
                        if 'event_end_time' in event.keys():
                            event_dict['event_end_time'] = event['event_end_time'].strip().replace('\n', ' ')

                        yaml_struct['times'][time_lookup[event_start_time]]['venues'][venue_name].append(event_dict)

            self.yamls[event_date] = dump(yaml_struct, Dumper=Dumper, sort_keys=False)

    def get_yamls(self):
        return self.yamls
