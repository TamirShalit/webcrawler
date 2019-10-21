from newscollector.news_downloader import BenGurionAirportScheduleDownloader
from conf import SCHEDULE_DIRECTORY, CHROME_DRIVER_LOCATION

if __name__ == '__main__':
    print 'Downloading flight schedule perpetually. Type Ctrl + C to stop.'
    BenGurionAirportScheduleDownloader(SCHEDULE_DIRECTORY,
                                       CHROME_DRIVER_LOCATION).download_news_perpetually()
