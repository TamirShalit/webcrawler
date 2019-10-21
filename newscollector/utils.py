import os
from datetime import datetime

from newscollector.raw_news import FlightLandingUpdate

LANDING_UPDATE_FILENAME_FORMAT = 'landing_update_flight_{{flight_number}}_{date_format}.json' \
    .format(date_format=FlightLandingUpdate.SCHEDULE_TIME_FORMAT)


def save_landing_updates_to_directory(landing_updates, directory_path):
    """
    :param landing_updates:
    :type landing_updates: list[FlightLandingUpdate]
    :param directory_path:
    """
    for landing_update in landing_updates:
        landing_update_filename = \
            datetime.strftime(landing_update.schedule_update_time,
                              LANDING_UPDATE_FILENAME_FORMAT.format(
                                  flight_number=landing_update.flight_number))
        landing_update_file_path = os.path.join(directory_path, landing_update_filename)
        landing_update.dump(landing_update_file_path)
