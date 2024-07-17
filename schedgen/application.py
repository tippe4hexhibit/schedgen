import logging
import os

from pathlib import Path

from pyairtable import Api
from schedgen.models.schedule import FullSchedule
from schedgen.models.yaml import YamlSchedule

from schedgen.widgets import SchedulePane

log = logging.getLogger(__name__)


class SchedGenApp:

    @staticmethod
    def run():

        required_env_vars = [
            'AIRTABLE_API_KEY',
            'AIRTABLE_BASE',
            'AIRTABLE_TABLE',
            'OUTPUT_DIR'
        ]

        check_env_vars = [x in os.environ for x in required_env_vars]

        if not all(check_env_vars):
            log.error(f'{required_env_vars}: {check_env_vars}')
            log.error('Ensure all environment variables are set properly')
            exit(255)
        else:
            for env_var in required_env_vars:
                if 'KEY' in env_var:
                    log.info(f'{env_var} is set')
                else:
                    log.info(f'{env_var} is {os.environ[env_var]}')

        output_path = Path(os.environ['OUTPUT_DIR'])

        if not output_path.exists():
            log.error(f"OUTPUT_DIR ({os.environ['OUTPUT_DIR']}) does not exist.")
            exit(254)

        api = Api(os.environ['AIRTABLE_API_KEY'])

        table = api.get_table(os.environ['AIRTABLE_BASE'], os.environ['AIRTABLE_TABLE'])
        raw_schedule = table.all(sort=['Event Start'])

        # Build the object structure from the Airtable data
        full_schedule = FullSchedule(raw_schedule)

        # Dump out all the YAMLs for each schedule type, by date
        schedule_prefix = None
        for schedule_type, schedule in full_schedule.get_schedules().items():
            schedule_yamls = YamlSchedule(schedule)
            schedule_prefix = schedule.schedule_abbreviation + '_'

            if schedule_type in ('Pre-Fair', 'Fair'):
                for event_date, daily_schedule in schedule.get_events().items():
                    for event_time, venue in daily_schedule.items():
                        print(f'{event_time}')
                        for venue_name, events in venue.items():
                            for event in events:
                                print(f'{event["event_name"]} - {venue_name} (until {event["event_end_time"]})')

            for yaml_date, yaml in schedule_yamls.get_yamls().items():
                schedule_filename = schedule_prefix + ''.join(yaml_date.split('-')) + '.yaml'

                with open(output_path / schedule_filename, 'w') as yaml_out:
                    log.info(f'Writing {schedule_type} schedule file for {yaml_date} called {schedule_filename}')
                    yaml_out.write(yaml)

