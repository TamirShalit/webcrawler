import os

from conf import SCHEDULE_DIRECTORY, RAW_MATERIAL_DIR
from newscollector import utils
from newscollector.news_extractor import FlightLandingScheduleExtractor


def main():
    if not os.path.exists(RAW_MATERIAL_DIR):
        os.mkdir(RAW_MATERIAL_DIR)
    for schedule_file_name in os.listdir(SCHEDULE_DIRECTORY):
        schedule_file_path = os.path.join(SCHEDULE_DIRECTORY, schedule_file_name)
        landing_updates = FlightLandingScheduleExtractor(schedule_file_path).extract_raw_news()
        utils.save_landing_updates_to_directory(landing_updates, RAW_MATERIAL_DIR)


if __name__ == '__main__':
    main()
