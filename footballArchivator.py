import bs4
import csv
import os
from selenium import webdriver
import time

root_link = 'https://www.srbijasport.net'
identifier = 1
football_clubs = {}
title = ['League Name', 'League Level', 'League Season', 'Matchday', 'Match Date', 'Match Time', 'Host Team ID', 'Host Team Name', 'Host Team Hometown', 'Host Team URL', 'Guest Team ID', 'Guest Team Name', 'Guest Team Hometown', 'Guest Team URL', 'Goals Host', 'Goals Guest']

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
#options.add_argument('--headless')
driver = webdriver.Chrome(os.path.join(os.getcwd(), 'chromedriver'), options=options)
driver.get('https://www.srbijasport.net/league/3855/games')

page_source = driver.page_source

soup = bs4.BeautifulSoup(page_source, 'lxml')


team_data = soup.find('tbody', {'class': 'data'})
team_names = team_data.find_all('td', {'class': 'tim'})

with open('data.csv', 'w') as writeFile:
    writer = csv.writer(writeFile)
    writer.writerow(title)

writeFile.close()


league_name = soup.find('h1', {'class': 'page-name'}).text.strip().replace('"','')
league_level = 1



with open('data.csv', 'a') as csvFile:
    writer = csv.writer(csvFile)
    menu = soup.find('ul', {'class': 'page-menu-navs'})
    seasons_wrapper = menu.find('ul', {'class': 'dropdown-menu'})
    season_links = seasons_wrapper.find_all('a')
    for j in range(0,5):
        league_season = season_links[j].text.strip().replace('"','')
        if j!=0:
            driver.get(root_link+season_links[j]['href'])
        game_buttons = driver.find_elements_by_class_name('page-link')
        driver.execute_script('arguments[0].click();', game_buttons[0])
        page_source = driver.page_source
        soup = bs4.BeautifulSoup(page_source, 'lxml')
        matchday = 1

        matchday_selector = soup.find('select', {'id': 'kolo'})
        for i in range(0,len(matchday_selector.find_all('option'))):
            time.sleep(1)
            game_buttons = driver.find_elements_by_class_name('page-link')
            driver.execute_script('arguments[0].click();', game_buttons[2])
            page_source = driver.page_source
            soup = bs4.BeautifulSoup(page_source, 'lxml')

            match_selector = soup.find_all('tr', {'class': 'result-row'})

            for match in match_selector:
                match_date = match.find('a', {'class': 'game-date'}).text.strip().replace('"','')
                match_time = match.find('span', {'class': 'game-time'}).text.strip().replace('"','')
                host = match.find('td', {'class': 'team-host'})
                host_link = host.find('a')
                host_name = host_link.text
                host_url = root_link+host_link['href']
                host_city = host_link['data-original-title']
                if host_url not in football_clubs:
                    football_clubs[host_url] = identifier
                    identifier = identifier + 1
                host_id = football_clubs[host_url]
                guest = match.find('td', {'class': 'team-guest'})
                guest_link = guest.find('a')
                guest_name = guest_link.text
                guest_url = root_link+guest_link['href']
                guest_city = guest_link['data-original-title']
                if guest_url not in football_clubs:
                    football_clubs[guest_url] = identifier
                    identifier = identifier + 1
                guest_id = football_clubs[guest_url]
                goals_host = match.find('span', {'class': 'res-1'}).text.strip().replace('"','')
                goals_guest = match.find('span', {'class': 'res-2'}).text.strip().replace('"','')
                row = [league_name, league_level, league_season, matchday, match_date, match_time, host_id, host_name, host_city, host_url, guest_id, guest_name, guest_city, guest_url, goals_host, goals_guest]
                writer.writerow(row)
            matchday = matchday+1

csvFile.close()
driver.close()
