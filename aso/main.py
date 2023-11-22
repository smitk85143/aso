from typing import Any, Dict, List
import yake
import google_play_scraper as PlayStoreScraper
from itunes_app_scraper.scraper import AppStoreScraper
from aso.utils.gplay import build_store as build_google_store
from aso.utils.apple import build_store as build_apple_store

class ASO:

    def __init__(self, store: str) -> None:
        self.store = store
        if self.store == "google":
            self.app = PlayStoreScraper.app
            self.search = PlayStoreScraper.search_ids
            self.suggest = PlayStoreScraper.suggest_keyword
            self.build_store = build_google_store
        elif self.store == "apple":
            self.app = AppStoreScraper().get_app_details
            self.search = AppStoreScraper().get_app_ids_for_query
            self.suggest = AppStoreScraper().get_suggestion_from_query
            self.build_store = build_apple_store