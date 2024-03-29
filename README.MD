# SrbijaSportScraper

Python web scraper based on the BeautifulSoup package used for scraping the [SrbijaSport](https://srbijasport.net) website. Since the website is javascript heavy, alongside BeautifulSoup, Selenium will also be used in order to emulate user actions. Data of every football game played is stored in a .csv file after scraping, and can then be used for other purposes.

## Motivation

Reason for creating such a project is in order to make the data available for some possible future statistical analysis. The data can also be used as a base for some prediction systems.

## Usage

Before using the project make sure you have pipenv installed. You can do so by running:

```
pip install pipenv
```

After that, navigate into the root directory of the project and run:

```
pipenv install
```

this will install all the necessary package dependencies. Finally, run the project like so:

```
pipenv run python scraper.py
```

After some time, all the acquired data will appear in the in a .csv file.

## Future Improvements

Current project only covers the first four levels on the Serbia Football League system, as well as the three levels of Montenegrin football system. Future holds possibility of expanding it on lower levels of the Serbian league system.
