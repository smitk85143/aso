from itunes_app_scraper.scraper import AppStoreScraper

appStoreScraper = AppStoreScraper()

from aso.utils.calc import *

MAX_KEYWORD_LENGTH = 25
MAX_SEARCH = 250
MAX_LIST = 50

def get_collection(app, lang, country):
    return 'topfreeapplications' if appStoreScraper.get_app_details(app, lang=lang, country=country)['price'] == 0.0 else 'toppaidapplications'

def get_genre(app, lang, country):
    return appStoreScraper.get_app_details(app, lang=lang, country=country)['primaryGenreId']

def build_store():

    def get_suggest_length(keyword, lang, country, length=None):
        length = length or 1
        if length > min(len(keyword), MAX_KEYWORD_LENGTH):
            return {'length': None, 'index': None}

        prefix = keyword[:length]
        suggestions = appStoreScraper.get_suggestion_from_query(prefix, country=country)
        index = suggestions.index(keyword) if keyword in suggestions else -1
        
        if index == -1:
            return get_suggest_length(keyword, lang=lang, country=country, length=length + 1)

        return {'length': length, 'index': index}

    def get_installs_score(apps, lang, country):
        min_installs = [appStoreScraper.get_app_details(app, lang=lang, country=country)['userRatingCount'] for app in apps]
        avg = sum(min_installs) / len(apps)
        max = 1000000
        score = z_score(max, avg)
        return {'avg': avg, 'score': score}

    def get_suggest_score(keyword, lang, country):
        length_stats = get_suggest_length(keyword, lang, country)

        if not length_stats['length']:
            score = 1
        else:
            length_score = i_score(1, MAX_KEYWORD_LENGTH, length_stats['length'])
            index_score = iz_score(4, length_stats['index'])
            score = aggregate([10, 1], [length_score, index_score])

        return {**length_stats, 'score': score}

    store = {
        'MAX_SEARCH': 250,
        'MAX_LIST': 50,
        'list': appStoreScraper.get_app_ids_for_collection,
        'search': appStoreScraper.get_app_ids_for_query,
        'app': appStoreScraper.get_app_details,
        'similar': appStoreScraper.get_similar_app_ids_for_app,
        'suggest': get_suggest_length,
        'getInstallsScore': get_installs_score,
        'getSuggestScore': get_suggest_score,
        'getCollection': get_collection,
        'getGenre': get_genre,
        'getCollectionQuery': lambda app, lang, country: {
            'collection': get_collection(app, lang=lang, country=country),
            'category': get_genre(app, lang, country),
            'num': store['MAX_LIST']
        }
    }

    return store