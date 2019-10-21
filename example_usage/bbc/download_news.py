from newscollector.news_downloader import BBCNewsDownloader

if __name__ == '__main__':
    BBCNewsDownloader('./articles').download_news()
