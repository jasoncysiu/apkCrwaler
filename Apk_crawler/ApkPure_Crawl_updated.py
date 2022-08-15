import requests
from bs4 import BeautifulSoup as bs
import os
import urllib
from selenium import webdriver
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from webdriver_manager import driver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from requests.api import head
import time
DOMAIN = 'https://apkpure.com'
URL = 'https://apkpure.com/'
CATEGORY = 'health_and_fitness'
PROXY = {
                'https': '//23.23.23.23:3128'            }
dir_path = "C:/Users/sjsa3/Downloads/Only_once/temp_work_dir/"

#Chrome
chromeOptions = webdriver.ChromeOptions()
prefs = {"download.default_directory" : r"D:\Summer_Vocation\new_apk\health_and_fitness",  
         "download.prompt_for_download": False,
  "download.directory_upgrade": True,
  "safebrowsing.enabled": True}
chromeOptions.add_argument("start-maximized")
chromedriver = r"C:\Users\sjsa3\Desktop\Share_with_mac\year2_sem2\AI_Android\Apk_crawler\chromedriver.exe"

count = 0


def download_apks(url):
    #open a session
    requests.Session()
    chromeOptions.add_experimental_option("prefs",prefs)
    dr = webdriver.Chrome(executable_path=chromedriver, options=chromeOptions)
    dr.get(url)
    soup = bs(dr.page_source,'html.parser')
    dr.close()
    target_divs = soup.find_all('div', {'class': 'category-template-down'})
    print(target_divs)
    for div in target_divs:
        target_a = div.findAll("a")
        link = target_a[0].get('href')
        file_name = link.rsplit('/')[2]
        print('Downloading ' + file_name + '......')

        
        
        with open(dir_path  + CATEGORY + '/' + file_name + '.apk', 'wb') as file:

            requests.Session()
            dr = webdriver.Chrome(executable_path=chromedriver, options=chromeOptions)
            dr.get(DOMAIN + link)
            
            # target_page = bs(requests.get(DOMAIN + link).text, 'html.parser')
            # no_empty = target_page.findAll('a', {'id': 'download_link'})

            # if no_empty:
            #     download_link = target_page.findAll('a', {'id': 'download_link'})[0].get('href')
            #     print(download_link)

            #     response = requests.get(download_link, stream=True)
            #     for chunk in response.iter_content(chunk_size=1024):
            #         file.write(chunk)

            #     global count
            #     count += 1


def iterate_page(base_url):
    requests.Session()    # Open a session to get the max-page
    # chromeOptions.add_argument('--proxy-server=%s' % PROXY)
    dr = webdriver.Chrome(executable_path=chromedriver, options=chromeOptions)
    dr.get(base_url)
    soup = dr.find_elements_by_class_name("loadmore") # loacte the class - loadmore
    for my_href in soup:
        max_page = int(my_href.get_attribute("data-maxpage")) # fetch the maxpage

    dr.close()
    # soup = bs(requests.get(base_url).text, 'html.parser')
    # max_page = int(soup.find_all('a', {'class': 'loadmore'})[0].get('data-maxpage')) + 1

    for page in range(1, max_page + 2):
        target_url = base_url + '?page=' + str(page + 1)    
        download_apks(target_url)

    print(str(count) + ' apks have been downloaded.')


def main():
    iterate_page(URL + CATEGORY)


if __name__ == "__main__":
    main()