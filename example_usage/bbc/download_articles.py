import os

from newscollector.news_downloader import BBCNewsDownloader
from conf import DOWNLOAD_MATERIAL_DIR

if __name__ == '__main__':
    if not os.path.exists(DOWNLOAD_MATERIAL_DIR):
        os.mkdir(DOWNLOAD_MATERIAL_DIR)
    BBCNewsDownloader(DOWNLOAD_MATERIAL_DIR).download_news()
