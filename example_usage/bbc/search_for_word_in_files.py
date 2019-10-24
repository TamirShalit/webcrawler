from conf import RAW_MATERIAL_DIR, SEARCHED_WORD
from webcrawler import analyzers
from webcrawler.raw_material import BBCRawArticle


def main():
    article_paths_about_bibi = analyzers.search_for_text_in_material_directory(BBCRawArticle,
                                                                               RAW_MATERIAL_DIR,
                                                                               SEARCHED_WORD)
    print 'Articles talking about {searched_word}:'.format(searched_word=SEARCHED_WORD)
    for article_path in article_paths_about_bibi:
        print article_path


if __name__ == '__main__':
    main()
