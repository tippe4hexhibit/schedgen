import logging
import os

from pyairtable import Api
from schedgen.models.schedule import FullSchedule
from schedgen.models.yaml import YamlSchedule

log = logging.getLogger(__name__)


class SchedGenApp:

    @staticmethod
    def run():
        api = Api(os.environ['AIRTABLE_API_KEY'])

        table = api.get_table('appywWGDJU508OseV', 'tblJHQ4V4VfCdVlFg')
        raw_schedule = table.all(sort=['Event Start'])

        full_schedule = FullSchedule(raw_schedule)

        # for schedule in full_schedule.schedules:
        #     log.info(full_schedule.schedules[schedule])

        fair_schedule_yamls = YamlSchedule(full_schedule.get_schedules()['Full Schedule'])

        for yaml_date, yaml in fair_schedule_yamls.get_yamls().items():
            print(yaml_date)
            print(yaml)
