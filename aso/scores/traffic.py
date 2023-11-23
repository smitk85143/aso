'''
Need change in ranked
'''

import math
from aso.utils.calc import *

def build(store):
    MAX_KEYWORD_LENGTH = 25

    SUGGEST_W = 8
    RANKED_W = 3
    INSTALLS_W = 2
    LENGTH_W = 1

    def get_keyword_length(keyword):
        length = len(keyword)
        return {
            "length": length,
            "score": math.ceil(10 * length / MAX_KEYWORD_LENGTH)
        }

    def get_ranked_apps(apps, lang, country):
        def find_rank(app, app_list):
            index = app_list.index(app) if app in app_list else -1
            return index + 1 if index >= 0 else None

        queries = set((store["getCollection"](app, lang, country) for app in apps))
        query_index = {tuple(q): store["list"](q, lang=lang, country=country) for q in queries}
        
        app_rank_lists = [query_index[tuple(store["getCollection"](app, lang, country))] for app in apps]
        ranks = [find_rank(app, app_rank_list) for app, app_rank_list in zip(apps, app_rank_lists) if find_rank(app, app_rank_list) is not None]
        if not ranks:
            return {
                "count": 0,
                "avgRank": None,
                "score": 1
            }

        avg_rank = sum(ranks) / len(ranks)
        count_score = (10 * len(ranks) / len(apps))
        avg_rank_score = math.ceil(100 - avg_rank)  # Adjust as needed
        score = (count_score + avg_rank_score) / 2
        return {
            "count": len(ranks),
            "avgRank": avg_rank,
            "score": score
        }

    def get_score(stats):
        weights = [SUGGEST_W, LENGTH_W, INSTALLS_W, RANKED_W]
        values = [stats["suggest"]["score"], stats["length"]["score"], stats["installs"]["score"], stats["ranked"]["score"]]
        return aggregate(weights, values)

    def get_top_apps(apps, lang, country):
        top = apps[:10]
        if apps and "description" not in apps[0]:
            return [store['app'](single_app, lang=lang, country=country)["trackId"] for single_app in top]
        else:
            return top

    def get_stats(keyword, apps, lang, country):
        top_apps = get_top_apps(apps, lang, country)
        ranked = get_ranked_apps(top_apps, lang, country)
        suggest = store["getSuggestScore"](keyword, lang, country)
        length = get_keyword_length(keyword)
        installs = store["getInstallsScore"](top_apps, lang, country)
        stats = {
            "suggest": suggest,
            "ranked": ranked,
            "installs": installs,
            "length": length
        }
        stats["score"] = get_score(stats)
        return stats

    return get_stats