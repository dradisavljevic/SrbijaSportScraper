from link import Link
from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException
from soup_getter import get_soup
import time
import config as cfg

def scrape_match(link, driver, league_level, football_clubs, identifier, writer, scraped_leagues, offset, links_to_scrape):
    league_season = link.text.strip().replace('"', '')
    scrape_link = cfg.ROOT_LINK + link['href']
    league_link = link['href']
    while league_level != cfg.LEVEL_CUTOFF:
        driver.get(scrape_link)
        more_matchdays = True
        game_buttons = driver.find_elements_by_class_name('page-link')
        if not game_buttons:
            more_matchdays = False
        if more_matchdays:
            driver.execute_script('arguments[0].click();', game_buttons[0])
        soup = get_soup(driver)
        league_name = soup.find('h1', {'class': 'page-name'}).text.strip().replace('"', '')
        matchday = 1

        matchday_selector = soup.find('select', {'id': 'kolo'})
        if not more_matchdays:
            matchday_count = 1
        else:
            matchday_count = len(matchday_selector.find_all('option'))
        old_table = {}
        for i in range(0,matchday_count):
            game_buttons = driver.find_elements_by_class_name('page-link')
            if more_matchdays:
                game_buttons = driver.find_elements_by_class_name('page-link')
                try:
                    driver.execute_script('arguments[0].click();', game_buttons[2])
                except StaleElementReferenceException as e:
                    time.sleep(1)
                    game_buttons = driver.find_elements_by_class_name('page-link')
                    driver.execute_script('arguments[0].click();', game_buttons[2])
                time.sleep(1)
                soup = get_soup(driver)
            tables = soup.find_all('table', {'class': 'ssnet-results'})
            if not more_matchdays:
                for table in tables:
                    matches = table.find_all('tr', {'class': 'result-row'})
                    for match in matches:
                        match_selector.append(match)
            else:
                match_selector = tables[0].find_all('tr', {'class': 'result-row'})
                while old_table == match_selector:
                    time.sleep(1)
                    soup = get_soup(driver)
                    tables = soup.find_all('table', {'class': 'ssnet-results'})
                    match_selector = tables[0].find_all('tr', {'class': 'result-row'})
            for match in match_selector:
                match_date = match.find('a', {'class': 'game-date'}).text.strip().replace('"', '')
                match_time = match.find('span', {'class': 'game-time'}).text.strip().replace('"', '')
                host = match.find('td', {'class': 'team-host'})
                host_link = host.find('a')
                host_name = host_link.text
                host_url = cfg.ROOT_LINK + host_link['href']
                host_city = host_link['data-original-title']
                host_site_id = host_url.split('/club/')[1].split('-')[0]
                if host_site_id not in football_clubs:
                    football_clubs[host_site_id] = identifier
                    identifier = identifier + 1
                host_id = football_clubs[host_site_id]
                guest = match.find('td', {'class': 'team-guest'})
                guest_link = guest.find('a')
                guest_name = guest_link.text
                guest_url = cfg.ROOT_LINK + guest_link['href']
                guest_city = guest_link['data-original-title']
                guest_site_id = guest_url.split('/club/')[1].split('-')[0]
                if guest_site_id not in football_clubs:
                    football_clubs[guest_site_id] = identifier
                    identifier = identifier + 1
                guest_id = football_clubs[guest_site_id]
                goals_host = match.find('span', {'class': 'res-1'}).text.strip().replace('"', '')
                goals_guest = match.find('span', {'class': 'res-2'}).text.strip().replace('"', '')
                if league_level == 0:
                    level = 1
                else:
                    level = league_level
                row = [
                league_name,
                level,
                league_season,
                matchday,
                match_date,
                match_time,
                host_id,
                host_name,
                host_city,
                host_url,
                guest_id,
                guest_name,
                guest_city,
                guest_url,
                goals_host,
                goals_guest
                ]
                writer.writerow(row)
                print('Writing: ' + league_name + ' Season ' + league_season + ' Matchday ' + str(matchday))
            old_table = match_selector
            matchday = matchday + 1
        scraped_leagues.append(league_link.split('/')[2])
        if all(scrape_link.id != league_link.split('/')[2] for scrape_link in links_to_scrape):
            links_to_scrape.append(Link(cfg.ROOT_LINK + league_link, league_link.split('/')[2], league_link, league_level, False))
        for i in range(0,len(links_to_scrape)):
            if league_link.split('/')[2] == links_to_scrape[i].id:
                links_to_scrape[i].scraped = True
                break

        soup = get_soup(driver)
        league_list = soup.find('div', {'class': 'league-nav'})
        league_tabs = league_list.find_all('li', {'role': 'presentation'})
        selenium_tabs = driver.find_elements_by_xpath('//*/a[@role="tab"]')
        for j in range(0,len(league_tabs)):
            next_league = league_tabs[j].find('a')
            if j != 0:
                webdriver.ActionChains(driver).move_to_element(selenium_tabs[j]).click(selenium_tabs[j]).perform()
            soup = get_soup(driver)
            league_container = soup.find('div', {'class': 'tab-content'})
            crawl_league_container = league_container.find('div', {'class': 'active'})
            leagues = crawl_league_container.find_all('a')
            for league in leagues:
                if next_league.text.strip().replace('"', '') == 'Niži rang':
                    next_league_level = league_level + 1
                elif next_league.text.strip().replace('"', '') == 'Liga višeg ranga':
                    next_league_level = league_level - 1
                else:
                    next_league_level = league_level
                if all(scrape_link.id != league['href'].split('/')[2] for scrape_link in links_to_scrape):
                    if next_league_level != cfg.LEVEL_CUTOFF:
                        links_to_scrape.append(\
                        Link(cfg.ROOT_LINK + league['href'], league['href'].split('/')[2], league['href'], next_league_level, False))
        next_link = None
        for link in links_to_scrape:
            if link.scraped == False:
                if next_link != None and next_link.level > link.level:
                    next_link = link
                elif next_link == None:
                    next_link = link
        if next_link is not None:
            league_link = next_link.href
            scrape_link = next_link.url
            league_level = next_link.level
        else:
            league_level = cfg.LEVEL_CUTOFF

    return football_clubs, identifier, scraped_leagues, links_to_scrape