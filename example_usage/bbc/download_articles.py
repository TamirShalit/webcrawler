from newscollector.news_downloader import BBCNewsDownloader
from conf import DOWNLOAD_MATERIAL_DIR

if __name__ == '__main__':
    BBCNewsDownloader(DOWNLOAD_MATERIAL_DIR).download_news()
