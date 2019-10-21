import os

from newscollector.raw_news import JsonRawNews, RawNews


def _get_lowered_list(iterable):
    lowered_list = []
    for element in iterable:
        if isinstance(element, basestring):
            lowered_list.append(element.lower())
        else:
            lowered_list.append(element)
    return lowered_list


def has_text(raw_news, text, case_sensitive=False):
    if not case_sensitive:
        text = text.lower()
    if hasattr(raw_news, 'to_text'):
        return _has_text_in_text_news(raw_news, text, case_sensitive)
    if isinstance(raw_news, JsonRawNews):
        return _has_text_in_json_news(text, raw_news, case_sensitive)
    raise NotImplementedError('No analyzer for this type of news.')


def _has_text_in_text_news(raw_news, text, case_sensitive):
    searched_text = raw_news.to_text()
    if not case_sensitive:
        searched_text = searched_text.lower()
    return text in searched_text


def _has_text_in_json_news(text, raw_news, case_sensitive):
    news_dict = raw_news.to_dict()
    searched_keys = news_dict.keys()
    searched_values = news_dict.values()
    if not case_sensitive:
        searched_keys = _get_lowered_list(searched_keys)
        searched_values = _get_lowered_list(searched_values)
    return text in searched_keys or text in searched_values


def search_for_text_in_news_files(news_type, file_paths, text):
    """

    :param news_type:
    :type news_type: RawNews
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
