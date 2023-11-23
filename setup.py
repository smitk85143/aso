import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
   name='aso',
   version='0.1.0',
   description='App Store Optimization (ASO)',
   long_description=long_description,
   long_description_content_type="text/markdown",
   author='smit-kukadiya',
   author_email='smitk85143@gmail.com',
   packages=setuptools.find_packages(),
   url="https://github.com/smit-kukadiya/aso.git",
   classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
   python_requires='>=3.9',
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
       'google-play-scraper @ git+https://github.com/smit-kukadiya/google-play-scraper.git',
       'itunes-app-scraper-dmi @ git+https://github.com/smit-kukadiya/itunes-app-scraper.git'
    ],
    license='MIT',
)
