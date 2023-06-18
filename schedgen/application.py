import logging
import os

from pyairtable import Api
from pprint import pprint

from schedgen.models.schedule import FullSchedule

log = logging.getLogger(__name__)


class SchedGenApp:

    @staticmethod
    def run():
        api = Api(os.environ['AIRTABLE_API_KEY'])

        table = api.get_table('appywWGDJU508OseV', 'tblJHQ4V4VfCdVlFg')
        raw_schedule = table.all(sort=['Event Start'])

        full_schedule = FullSchedule(raw_schedule)

        for schedule in full_schedule.schedules:
            log.info(full_schedule.schedules[schedule])



