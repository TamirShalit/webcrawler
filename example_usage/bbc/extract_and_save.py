import os

from webcrawler.data_extractor import BBCNewsExtractor
from conf import DOWNLOAD_MATERIAL_DIR, RAW_MATERIAL_DIR


def main():
    if not os.path.exists(RAW_MATERIAL_DIR):
        os.mkdir(RAW_MATERIAL_DIR)
    for download_news_file_name in os.listdir(DOWNLOAD_MATERIAL_DIR):
        download_news_file_path = os.path.join(DOWNLOAD_MATERIAL_DIR, download_news_file_name)
        raw_news = BBCNewsExtractor(download_news_file_path).extract_raw_material()[0]

        raw_news_filename = os.path.splitext(download_news_file_name)[0] + '.txt'
        raw_news_file_path = os.path.join(RAW_MATERIAL_DIR, raw_news_filename)
        raw_news.dump(raw_news_file_path)


if __name__ == '__main__':
    main()
