if __name__ == '__main__':
    # BBCNewsDownloader('/Users/tamir/temp').download_news()
    BenGurionAirportScheduleDownloader(
        '/Users/tamir/PycharmProjects/newscollector/newscollector/output',
        '/Users/tamir/Downloads/chromedriver').download_news_perpetually()