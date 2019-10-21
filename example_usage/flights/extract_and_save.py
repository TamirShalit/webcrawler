import os

from newscollector.news_extractor import BenGurionAirportScheduleExtractor
from conf import SCHEDULE_DIRECTORY, RAW_MATERIAL_DIR


# TODO
def main():
    for schedule_file_name in os.listdir(SCHEDULE_DIRECTORY):
        schedule_file_path = os.path.join(SCHEDULE_DIRECTORY, schedule_file_name)
        flight_updates = BenGurionAirportScheduleExtractor(schedule_file_path).extract_raw_news()
        for flight_update in flight_updates:
            flight_update_filename = flight_update

        raw_news_filename = os.path.splitext(schedule_file_name)[0] + '.txt'
        raw_news_file_path = os.path.join(RAW_MATERIAL_DIR, raw_news_filename)
        flight_updates.dump(raw_news_file_path)


if __name__ == '__main__':
    main()
