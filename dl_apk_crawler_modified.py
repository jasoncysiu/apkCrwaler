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
# from bs4 import BeautifulSoup as bs
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import json
from fake_useragent import UserAgent
import random
from fp.fp import FreeProxy
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from collections import OrderedDict 
import pandas as pd

filename = 'apkmonk_list.csv'
apks= pd.read_csv(filename)
count = 0
flag_found = True
last_row_apk = len(apks[['Package_name']])
not_found = [] # list of apps found on apkmonk but does not have download button
for i in range(last_row_apk):
    url = "https://www.apkmonk.com/app/"
    domain = "https://www.apkmonk.com"
    ua = UserAgent()

    downloadPath = r"C:\Users\sjsa3\Downloads\Only_once\Yj_apkCrwaler\apk_tencent"
    exe_path = r"C:\Users\sjsa3\Desktop\Share_with_mac\year2_sem2\AI_Android\Apk_crawler\chromedriver.exe"
    options = Options()
    prefs = {}
    prefs["download.default_directory"]=downloadPath
    # options.headless = True
    options.add_argument("--window-size=800,1200")
    # options.add_argument("headless")
    options.add_argument(f'user-agent={ua.random}')
    options.add_experimental_option("prefs", prefs)
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("--disable-blink-features=AutomationControlled")


    
    driver = webdriver.Chrome(executable_path= exe_path, 
                              chrome_options=options)

    
    try:
        with open(filename, 'r') as file:
            apks= pd.read_csv(filename)
            for apk in apks:
                apk_name = apks[['Package_name']].values[count][0]
                # apk_name = "io.trade.tradeio.eu"
                apk_url = url + apk_name

                print(apk_url)
                # request the target apk url
                driver.get(apk_url)

                # get that source
                html_source = driver.page_source
                flag_found = True
                while flag_found: # check if apk package is found
                    if "Not Found"in html_source : # if it is not found
                        count += 1
                        print("Not found", apk_name, ":", count ,"    Did not download")
                        flag_found = False
                        driver.quit()
                        break
                    elif not "download-app" in html_source: #if it is not, but cannot see the download link
                        count += 1
                        print("Cannot download", apk_name, ":", count ,"    !!")
                        not_found.append(apk_name)
                        flag_found = False
                        driver.quit()
                        break
                    else:
                        flag_found = False

                
                apk_comp_2 = html_source.split('https://www.apkmonk.com/download-app/')[1].split('.apk')[0]
                final_link = "https://www.apkmonk.com/download-app/" + apk_comp_2 +".apk"
                print(final_link)
                driver.get(final_link)
                time.sleep(7)

                fileends = "crdownload"
                    
                while any(fileends in string for string in os.listdir(downloadPath)): # check if the download is completed
                    time.sleep

                driver.quit()

                print("Download", apk_name, ":", count)
                count += 1
                break

    except Exception as e:
        print(e)
        print("Skipping. Connnection error")


print(not_found)