import os

from newscollector.downloader import FlightLandingScheduleDownloader
from conf import SCHEDULE_DIRECTORY, CHROME_DRIVER_LOCATION


def main():
    if not os.path.exists(SCHEDULE_DIRECTORY):
        os.mkdir(SCHEDULE_DIRECTORY)
    print 'Downloading flight schedule perpetually. Type Ctrl+C to stop.'
    FlightLandingScheduleDownloader(SCHEDULE_DIRECTORY,
                                    CHROME_DRIVER_LOCATION).download_data_perpetually()


if __name__ == '__main__':
    main()
