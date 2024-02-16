from typing import Any, Dict, List
import yake

from aso.main import ASO

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

class PositionKeywordApp:

    def __init__(self, store: str) -> None:
        self.aso_instance = ASO(store)

    def conteins_keywords(self, keywords:List[tuple], key:str) -> bool:
        for k in keywords:
            if(k[0] == key):
                return True
        return False
        
    def position_validator(self, keywords, app_id, lang, country):
        relevant_keys = []
        for key in keywords:
            try:
                search_result = [ x for x in self.aso_instance.search(key[0], lang=lang, country=country, timeout=5,
                                                                    headers={
                                                                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
                                                                    }) ]
            except Exception:
                continue
            for j, search_app in enumerate(search_result):
                if search_app == app_id:
                    relevant_keys.append([key[0], key[1], j+1])
        return relevant_keys

    def position_keyword_app(self, app_id: str, lang: str = "en", country: str = "us", num: int = 25, keywords: list = None) -> Dict[str, Any]:
        """
        Get the position of the keywords in the search of the app
        :param app_id: the app id
        :param lang: the language of the app
        :param country: the country of the app
        :param num: the number of keywords to search
        :param keywords: the keywords to search

        :return: the position of the keywords in the search of the app
        """
        if keywords is None:
            data = self.aso_instance.app(app_id, lang=lang, country=country)
            full_content = [ f"{data['trackCensoredName']} {data['description']} {data['sellerName']}" ]
            keywords = []
            for txt in full_content:
                extractor = yake.KeywordExtractor(lan=lang, n=3, dedupLim=0.9, features=None, top=num)
                keys = extractor.extract_keywords(txt)
                for k in keys:
                    if not self.conteins_keywords(keywords, k[0]):
                        keywords.append(k)
        else:
            keywords = [(keyword, None) for keyword in keywords]
        position_keywords = self.position_validator(keywords, app_id, lang, country)
        data = []
        for item in position_keywords:
            data.append({'keyword': item[0], "number": item[2]})
        data = sorted(data, key=lambda k: k['number'])

        return data