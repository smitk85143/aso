from typing import Dict, Any
from aso.main import ASO

class TopKeywords:

    def __init__(self, store: str) -> None:
        self.aso_instance = ASO(store)

    def top_keywords(self, country: str = "us") -> Dict[str, Any]:
        """
        Get top keywords for a country
        :param country: two letter country code

        Note: This function is only support english language
        """
        alphabet = "abcdefghijklmnopqrstuvwxyz"
        map_popularity = {}
        for char in alphabet:
            suggests = self.aso_instance.suggest_keyword(char, country=country)
            minus = 0
            for s in suggests:
                map_popularity[s] = 6 - minus
                minus += 1

        data = []

        for item in map_popularity.items():
            data.append({'Key': item[0], "Relative popularity": item[1]})

        data = sorted(data, key=lambda k: k['Relative popularity'], reverse=True)

        return data