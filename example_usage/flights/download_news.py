from newscollector.news_downloader import BenGurionAirportScheduleDownloader

# Configure it to your Selenium chrome driver location.
CHROME_DRIVER_LOCATION = '/Users/tamir/Downloads/chromedriver'

if __name__ == '__main__':
    print 'Downloading flight schedule perpetually. Type Ctrl + C to stop.'
    BenGurionAirportScheduleDownloader('./schedule_pages',
                                       CHROME_DRIVER_LOCATION).download_news_perpetually()
