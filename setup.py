from setuptools import setup

setup(
   name='aso',
   version='0.1',
   description='App Store Optimization (ASO)',
   author='Smit Kukadiya',
   author_email='smitk85143@gmail.com',
   packages=['aso'],
   url="https://github.com/smit-kukadiya/aso.git",
   install_requires=[
       'wheel', 
       'bar', 
       'greek',
       'lxml',
       'yake',
       'google_play_scraper @ git+https://github.com/smit-kukadiya/google-play-scraper.git@test-aso',
       'itunes_app_scraper @ git+https://github.com/smit-kukadiya/itunes-app-scraper.git'
    ], 
)