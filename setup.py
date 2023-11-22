import setuptools

setuptools.setup(
   name='aso',
   version='0.1',
   description='App Store Optimization (ASO)',
   author='Smit Kukadiya',
   author_email='smitk85143@gmail.com',
   packages=setuptools.find_packages(),
   url="https://github.com/smit-kukadiya/aso.git",
   entry_points={
        'console_scripts': [
            'aso=aso.__main__:main'
        ]
    },
   install_requires=[
       'wheel', 
       'bar', 
       'greek',
       'lxml',
       'yake',
       'google-play-scraper @ git+https://github.com/smit-kukadiya/google-play-scraper.git@test-aso',
       'itunes-app-scraper-dmi @ git+https://github.com/smit-kukadiya/itunes-app-scraper.git'
    ], 
)
