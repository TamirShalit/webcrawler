from newscollector.news_downloader import FlightLandingScheduleDownloader
from conf import SCHEDULE_DIRECTORY, CHROME_DRIVER_LOCATION

if __name__ == '__main__':
    print 'Downloading flight schedule perpetually. Type Ctrl+C to stop.'
    FlightLandingScheduleDownloader(SCHEDULE_DIRECTORY,
                                    CHROME_DRIVER_LOCATION).download_news_perpetually()
