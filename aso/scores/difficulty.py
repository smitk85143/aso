from datetime import datetime
import yake

from aso.utils.calc import *

# Weights to merge all stats into a single score
TITLE_W = 4
COMPETITOR_W = 3
INSTALLS_W = 5
RATING_W = 2
AGE_W = 1

def build(store):
    def get_match_type(keyword, title):
        keyword = keyword.lower()
        title = title.lower()

        if keyword in title:
            return 'exact'

        matches = [title_word in keyword.split(' ') for title_word in title.split(' ')]

        if all(matches):
            return 'broad'
        if any(matches):
            return 'partial'

        return 'none'

    def get_title_matches(keyword, apps, lang, country):
        matches = [get_match_type(keyword, store['app'](app, lang=lang, country=country)['trackCensoredName']) for app in apps]
        counts = {
            'exact': matches.count('exact'),
            'broad': matches.count('broad'),
            'partial': matches.count('partial'),
            'none': matches.count('none')
        }
        score = (10 * counts['exact'] + 5 * counts['broad'] + 2.5 * counts['partial']) / len(apps)
        return {'score': score, **counts}
    
    def get_keywords(store):
        def get_keywords(app, lang, country):
            data = store['app'](app, lang=lang, country=country)
            keywords = yake.KeywordExtractor(top=50).extract_keywords(f"{data['description']}")
            return [keyword[0] for keyword in keywords]
        return get_keywords

    def is_competitor(keyword, app, lang, country):
        return keyword in get_keywords(store)(app, lang=lang, country=country)

    def get_competitors(keyword, apps, lang, country):
        competitors = [is_competitor(keyword, app, lang, country) for app in apps]
        count = competitors.count(True)
        score = z_score(len(apps), count)
        return {'count': count, 'score': score}

    def get_rating(apps, lang, country):
        avg = sum([store['app'](app, lang=lang, country=country)['averageUserRating'] or 0 for app in apps]) / len(apps)
        return {
            'avg': avg,
            'score': avg * 2
        }

    def get_days_since(date):
        if isinstance(date, str):
            try:
                date = datetime.strptime(date, "%b %d, %Y")  # Assuming the date string is in ISO format (e.g., '2023-11-06T00:00:00')
            except Exception:
                date = datetime.fromisoformat(date)
        else:
            date = datetime.fromtimestamp(date)
        
        current_date = datetime.now(date.tzinfo)
        delta = current_date - date
        return delta.days

    def get_age(apps, lang, country):
        updated = [get_days_since(store['app'](app, lang=lang, country=country)['currentVersionReleaseDate']) for app in apps]
        avg = sum(updated) / len(apps)
        max = 500
        score = z_score(max, avg)
        return {
            'avgDaysSinceUpdated': avg,
            'score': score
        }

    def get_score(stats):
        return aggregate([TITLE_W, COMPETITOR_W, INSTALLS_W, RATING_W, AGE_W],
                             [stats['titleMatches']['score'], stats['competitors']['score'],
                              stats['installs']['score'], stats['rating']['score'], stats['age']['score']])

    def get_stats(keyword, apps, lang, country):
        competitors = get_competitors(keyword, apps, lang, country)
        top_apps = apps[:10]
        title_matches = get_title_matches(keyword, top_apps, lang, country)
        installs = store['getInstallsScore'](top_apps, lang, country)
        rating = get_rating(top_apps, lang, country)
        age = get_age(top_apps, lang, country)
        stats = {
            'titleMatches': title_matches,
            'competitors': competitors,
            'installs': installs,
            'rating': rating,
            'age': age
        }
        stats['score'] = get_score(stats)
        return stats

    return get_stats