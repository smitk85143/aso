from difficulty import build as build_difficulty
from traffic import build as build_traffic

from aso.main import ASO

class Score:

    def __init__(self, store: str) -> None:
        self.aso_instance = ASO(store)

    def score(self, keyword: str, lang: str = "en", country: str = "us"):
        appsId = [ single_app['appId'] for single_app in self.aso_instance.search(keyword, lang=lang, country=country)]
        difficulty = build_difficulty(self.aso_instance.build_store())(keyword, appsId, lang, country)
        traffic = build_traffic(self.aso_instance.build_store())(keyword, appsId, lang, country)
        return {
            'difficulty': difficulty,
            'traffic': traffic
        }