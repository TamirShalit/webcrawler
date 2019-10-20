import os

from newscollector.raw_news import JsonRawNews


def has_text(raw_news, text):
    if hasattr(raw_news, 'to_text'):
        return text in raw_news.to_text()
    if isinstance(raw_news, JsonRawNews):
        news_dict = raw_news.to_dict()
        return text in news_dict.values() or text in news_dict.values()


def search_for_text_in_news_files(news_type, file_paths, text):
    """

    :param news_type:
    :type news_type: newscollector.raw_news.RawNews
    :param file_paths:
    :type file_paths: list[str]
    :param text:
    :type text: str
    :return:
    """
    files_with_text = []
    for file_path in file_paths:
        raw_news = news_type.load(file_path)
        if has_text(raw_news, text):
            files_with_text.append(file_path)
    return files_with_text


def search_for_text_in_news_directory(news_type, directory_path, text):
    file_paths = [os.path.join(directory_path, file_name) for file_name in
                  os.listdir(directory_path)]
    return search_for_text_in_news_files(news_type, file_paths, text)
