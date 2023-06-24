import logging

from collections import OrderedDict
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
            yaml_struct = {
                'longdate': datetime.fromisoformat(event_date).strftime('%A, %B %-d, %Y'),
                'times': {}
            }

            for event_start_time, venue in schedule.items():
                for venue_name, events in venue.items():
                    for event in events:
                        if event_start_time not in yaml_struct['times']:
                            yaml_struct['times'][event_start_time] = {}

                        if venue_name not in yaml_struct['times'][event_start_time]:
                            yaml_struct['times'][event_start_time][venue_name] = []

                        yaml_struct['times'][event_start_time][venue_name].append(event['event_name'].strip())

            self.yamls[event_date] = dump(yaml_struct, Dumper=Dumper, sort_keys=False)

    def get_yamls(self):
        return self.yamls
