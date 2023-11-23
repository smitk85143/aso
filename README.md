# iTunes App Store Scraper
This defines a lightweight Python class that can be used for app 
information from Google Play Store and iTunes App Store.

Much of this has been adapted from 
[aso](https://github.com/facundoolano/aso), a 
nodeJS-based repo that does similar things. But this repo uses Python.

## Getting started
The following repo app details about all apps similar to the first result 
for the 'fortnite' search query:

```
from aso import PositionKeywordApp

results = PositionKeywordApp("google").PositionKeywordApp(app_id="com.openai.chatgpt", country="en", lang="us")
print(results)
```

Documentation is not available separately yet, but the code is relatively
simple.

## Resources
[google-play-scracper](https://github.com/JoMingyu/google-play-scraper)
[itunes-app-scraper](https://github.com/smit-kukadiya/itunes-app-scraper)