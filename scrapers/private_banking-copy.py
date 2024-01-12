import os
import uuid
import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup

def get_article_content(url):
    page=1
    urls=[]


    options = Options()
    options.add_argument('-headless')
    options.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'
    #options.add_argument("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36")
    options.set_preference("general.useragent.override", "Mozilla/5.0 (iPhone; CPU iPhone OS 15_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/101.0.4951.44 Mobile/15E148 Safari/604.1")
        
    driver = webdriver.Firefox(options=options)
    driver.get(url)
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "next"))
            )
        for i in range(220):
            print(page)
            page+=1
            titles=driver.find_elements(By.CLASS_NAME, "title");
            for title in titles:
               href=title.get_attribute('href')
               if href !=None:
                    urls.append(href);
                    print(href)
            try:
            #remove an obsuring banners and overlays
                accept_cookies_button=driver.find_element(By.ID, "ensAcceptAll");
                accept_cookies_button.click()
            except:
                pass

            #click the next button 
            try:
                next_button=driver.find_element(By.CLASS_NAME, "next");
                next_button.click()
                time.sleep(5)
            except:
                pass 


    except Exception as err:
        print (err);

        output=json.dumps(urls)

        try:
            filename=url.rsplit('/', 1)[-1]
            f= open("./content/output/privatebankingurls.json","w+",encoding="utf-8")
            f.write(output)
            f.close()
        except:
            print ('issue writing file')

    finally:
        driver.quit()




get_article_content('https://www.privatebank.citibank.com/search-results?search=*')