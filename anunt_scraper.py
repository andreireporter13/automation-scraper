#
#   Author: Andrei C. Cojocaru
#   LinkedIn profile: https://www.linkedin.com/in/andrei-cojocaru-985932204/
#   site: https://webautomation.ro
#
# Try to make a new scraper; 
#
# import needed libraries; 
import requests 
from bs4 import BeautifulSoup 
#
#
# too important library is Selenium;
#
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
#
# wait and expected_conditions;
#
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
#
# import another needed libraries; 
# 
from time import sleep
import csv 
import pandas as pd 
from fake_useragent import UserAgent
# 
# 
# import library for beautiful introduction screen;
from termcolor import colored 
from pyfiglet import Figlet 
from pyfiglet import figlet_format
#
#
# Firefox important options; 
options = webdriver.FirefoxOptions()
user_agent = UserAgent()
options.set_preference("general.useragent.override", user_agent.random) # random UserAgent 
options.add_argument('--disable-blink-features=AutomationControlled')
firefox_service = Service(executable_path='/home/andy/Documents/web-scraping-projects/geckodriver') # get your driver path;
#
# option for headless webdriver;
options.headless = True

# function for gather data from publi24.ro; 
def gather_data(link, user_input_keyword, input_integer):

    try: 
        driver = webdriver.Firefox(service=firefox_service, options=options)
        driver.get(link)
        sleep(2)

        input_label = driver.find_element(By.ID, 'keyword').send_keys(user_input_keyword)
        sleep(1)
        click_icon = driver.find_element(By.ID, 'btn-search').click()
        
        sleep(1)

        # logic for scraper data; 
        list_with_data = []
        for i in range(1, input_integer + 1):
            
            print(f'Se face scraping pe pagina {i}')

            soup = BeautifulSoup(driver.page_source, 'lxml')
            list_div_information = soup.findAll('div', class_ = 'listing-data')

            # gather information from pages; 
            for elem in list_div_information: 
            
                try:
                    link = elem.find('a', class_ = 'maincolor').get('href')
                except: 
                    print('-')

                try: 
                    text = elem.find('a', class_ = 'maincolor').text.strip()
                except: 
                    print('-')

                try: 
                    price = elem.find('div', class_ = 'large-4 medium-5 large-text-right medium-text-right columns prices').find('strong', class_ = 'price maincolor').text.strip()
                except: 
                    print('-')

                try:
                    locatie = elem.find('label', class_ = 'article-location').findAll('span')[0].text.strip()
                except:
                    print('-')

                try: 
                    data_post = elem.find('div', class_ = 'small-12 columns bottom').find('label', class_ = 'article-date').text.strip()
                except: 
                    print('-')

                try:
                    alte_date = elem.find('div', class_ = 'small-12 columns bottom').find('label', class_ = 'article-details').text.strip()
                except: 
                    print('-')
                    
                
                list_with_data.append([link, text, price, locatie, data_post, alte_date])


            # clik on next page;
            sleep(3)
            next_button_link = soup.find('ul', class_ = 'pagination radius').findAll('li')[-1].find('a').get('href')
            driver.get(next_button_link)
            sleep(10)
            

        header = ['link', 'text', 'price', 'locatie', 'data_post', 'alte_date']
        df = pd.DataFrame(list_with_data, columns = header)
        df.to_csv('publi24_scraper_data_webautomation_ro.csv', encoding='utf8')
        print('Done!')

    except Exception as ex: 
        print(ex)

    finally: 
        # set time for sleep, driver working; 
        sleep(15)
        driver.quit()


# define main() function: 
def main():

    introduction = Figlet(font = 'big')
    print(colored(introduction.renderText('Powered by:'), 'green'))
    print(figlet_format("webautomation.ro", font = "banner3", width = 600))
    reclama = Figlet(font = 'digital')
    print(colored(reclama.renderText('Site-ul de anunturi Publi24.ro'), 'blue'))

    user_input = input('Scrie un cuvant cheie pentru a cauta un anunt pe publi24.ro: ')
    user_input_2 = input('De la 1 la 3, cate pagini de informatie vrei sa ti se returneze?: ')         

    # try 
    try:
        if 1 <= int(user_input_2) <= 3:
            if user_input_2.isdigit(): 
                gather_data('https://www.publi24.ro/', user_input, int(user_input_2))
   
        else: 
            if int(user_input_2) < 1: 
                print('Ai pus o valoare mai mica decat 0!')
            else: 
                print('Ai pus o valoare mai mare decat 3!')
    except: 
        print('Ai introdus semne gresite!')


# condition if __name__ == '__main__'
if __name__ == '__main__':
    main()
