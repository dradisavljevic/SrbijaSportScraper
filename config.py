#!/usr/bin/env python

ROOT_LINK = 'https://www.srbijasport.net'
SERBIA_START_PAGE = 'https://www.srbijasport.net/league/4428/games'
MONTENEGRO_START_PAGE = 'https://www.srbijasport.net/league/4472/games'
SERBIA_EXPORT_FILE_NAME = 'serbiaData.csv'
MONTENEGRO_EXPORT_FILE_NAME = 'montenegroData.csv'

SEASON_CUTOFF = '2005-2006'
LEVEL_CUTOFF = 5

TITLE = [
    'League Name',
    'League Level',
    'League Season',
    'Matchday',
    'Match Date',
    'Match Time',
    'Host Team ID',
    'Host Team Name',
    'Host Team Hometown',
    'Host Team URL',
    'Guest Team ID',
    'Guest Team Name',
    'Guest Team Hometown',
    'Guest Team URL',
    'Goals Host',
    'Goals Guest',
    'Goals Host Half Time',
    'Goals Guest Half Time',
    'Game Outcome'
    ]

DRIVER_NAME = 'chromedriver'
