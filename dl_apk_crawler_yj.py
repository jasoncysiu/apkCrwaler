"""
Written by Yujin Huang(Jinx)
Started 28/03/2021 9:28 pm
Last Editted 

Description of the purpose of the code
"""
import csv
from telnetlib import EC

import requests
from bs4 import BeautifulSoup as bs
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
import random
from fp.fp import FreeProxy
import re


for i in range(100):
    filename = 'apkmonk_list.csv'
    url = "https://www.apkmonk.com/app/"
    domain = "https://www.apkmonk.com"

    ua = UserAgent()
    headers = requests.utils.default_headers()
    headers.update({
        'User-Agent': ua.random,
    })

    options = Options()
    options.headless = True
    # PROXY = FreeProxy(anonym=True).get().split("//")[1]
    # options.add_argument('--proxy-server=%s' % PROXY)
    options.add_argument("--window-size=1920,1200")
    driver = webdriver.Chrome(executable_path= r"C:\Users\sjsa3\Desktop\Share_with_mac\year2_sem2\AI_Android\Apk_crawler\chromedriver.exe",options=options)

    try:
        with open(filename, 'r') as file:
            apks = csv.reader(file)
            header = next(apks)
            for apk in apks:
                count = 0
                apk_name = apk[0].split('_')[0]

                # apk_name = 'com.google.android.apps.meetings'
                apk_url = url + apk_name

                print(apk_url)

                # request the target apk url
                soup = bs(requests.get(apk_url, headers=headers).text, 'html.parser')
                links = soup.findAll("a")

                for link in links:
                    onclick_value = link.get('onclick', "")
                    if ".apk" in onclick_value:
                        download_url = domain + link['href']

                        driver.implicitly_wait(60)
                        driver.get(download_url)

                        soup2 = bs(driver.page_source, 'lxml')
                        final_link = soup2.find('a', id='dlink')['download-link'][3:]
                        # print(driver.page_source)
                        print(final_link)

                        # response = requests.get(final_link, headers=headers, stream=True, proxies=PROXY)
                        response = requests.get(final_link, headers=headers, stream=True)

                        apk_version = ("_").join(download_url.split("_", 2)[1:3])[:-1]

                        path = "dl_apks_big_comp/" + apk_name + "/"
                        if not os.path.exists(path):
                            os.makedirs(path)

                        with open(path + apk_version, 'wb') as download_apk:
                            for chunk in response.iter_content(chunk_size=1024):
                                download_apk.write(chunk)

                        count += 1

                print("Download", apk_name, ":", count)
                break
    except Exception as e:
        print(e)
        print("Skipping. Connnection error")
