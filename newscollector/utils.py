import os
from datetime import datetime

from newscollector.raw_material import FlightLandingUpdate

LANDING_UPDATE_FILENAME_FORMAT = 'landing_update_flight_{{flight_number}}_{date_format}.json' \
    .format(date_format=FlightLandingUpdate.SCHEDULE_TIME_FORMAT)


def save_landing_updates_to_directory(landing_updates, directory_path):
    """
    Dump landing updates to directory, using file-names which contain data from the landing update.
    """
    for landing_update in landing_updates:
        landing_update_filename = \
            datetime.strftime(landing_update.schedule_update_time,
                              LANDING_UPDATE_FILENAME_FORMAT.format(
                                  flight_number=landing_update.flight_number))
        landing_update_file_path = os.path.join(directory_path, landing_update_filename)
        landing_update.dump(landing_update_file_path)


def load_raw_material_from_files(material_type, file_paths):
    return [material_type.load(file_path) for file_path in file_paths]


def get_most_recent_landing_updates(landing_updates):
    """
    :type landing_updates: list[FlightLandingUpdate]
    :return: Most recent landing update for each flight in given updates.
    :rtype list[FlightLandingUpdate]
    """
    most_recent_landing_updates = {}
    for landing_update in landing_updates:
        saved_landing_update = most_recent_landing_updates.get(landing_update.flight_number)
        if saved_landing_update is None or \
                landing_update.schedule_update_time > saved_landing_update.schedule_update_time:
            most_recent_landing_updates[landing_update.flight_number] = landing_update
    return most_recent_landing_updates.values()
