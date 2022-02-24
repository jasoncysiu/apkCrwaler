"""
Written by Yujin Huang(Jinx)
Started 28/ /2021 9:28 pm
Last Editted 

Description of the purpose of the code
"""
import csv
from telnetlib import EC
import time
import requests
from bs4 import BeautifulSoup as bs
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
import random
from fp.fp import FreeProxy

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
    prefs = {}
    downloadPath = r"C:\Users\sjsa3\Downloads\Only_once\Yj_apkCrwaler\apk_google"
    prefs["download.default_directory"]=downloadPath
    # options.headless = True
    # PROXY = FreeProxy(anonym=True).get().split("//")[1]
    # PROXY = '212.41.9.192:3128'
    # options.add_argument('--proxy-server=%s' % PROXY)
    options.add_argument("--window-size=800,1200")
    # options.add_argument("headless")
    options.add_experimental_option("prefs", prefs)
    exe_path = r"C:\Users\sjsa3\Desktop\Share_with_mac\year2_sem2\AI_Android\Apk_crawler\chromedriver.exe"
    driver = webdriver.Chrome(executable_path= exe_path,options=options)
    
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
                s = requests.get(apk_url, headers=headers)
                # request the target apk url
                soup = bs(requests.get(apk_url, headers=headers).text, 'html.parser')
                links = soup.findAll("a")

                for link in links:
                    try:
                        if link["id"] == "download_button":
                            final_link = link["href"]
                            break
                        else:
                            continue
                    except:
                        continue
                print(final_link)

                # response = requests.get(final_link, headers=headers, stream=True, proxies=PROXY)
                response = requests.get(final_link, headers=headers, stream=True)
                driver.get(final_link)
                time.sleep(10)
                # driver.get("https://www.google.com")
                # apk_version = ("_").join(download_url.split("_", 2)[1:3])[:-1]

                count += 1

                print("Download", apk_name, ":", count)
                break
    except Exception as e:
        print(e)
        print("Skipping. Connnection error")
