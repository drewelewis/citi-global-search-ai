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

def get_private_banking_page_content(url):
    
    id=str(uuid.uuid4())
    #dictionary for article content
    articlecontent={}
    articlecontent['id']=id
    articlecontent['url']=url

    options = Options()
    options.add_argument('-headless')
    options.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'
    #options.add_argument("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36")
    options.set_preference("general.useragent.override", "Mozilla/5.0 (iPhone; CPU iPhone OS 15_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/101.0.4951.44 Mobile/15E148 Safari/604.1")
        
    driver = webdriver.Firefox(options=options)
    driver.get(url)
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "main"))
            )
       
        try:
            bodytag=driver.find_element_by_tag_name('body')
            for n in range(20):
                bodytag.send_keys(Keys.PAGE_DOWN)
        except:
            pass

        time.sleep(5)

        try:
            element = driver.find_element(By.CLASS_NAME,'citi-cmp-container--default')  
            driver.execute_script("""
            var element = arguments[0];
            element.parentNode.removeChild(element);
            """, element)
        except:
            pass
     
        # try:
        #     element = driver.find_element(By.CLASS_NAME,'cmp-container')  
        #     driver.execute_script("""
        #     var element = arguments[0];
        #     element.parentNode.removeChild(element);
        #     """, element)
        # except:
        #     pass

        # try:
        #     element = driver.find_element(By.CLASS_NAME,'experiencefragment')  
        #     driver.execute_script("""
        #     var element = arguments[0];
        #     element.parentNode.removeChild(element);
        #     """, element)
        # except:
        #     pass

        

        content=driver.page_source
        soup=BeautifulSoup(content,'html.parser')
        
        try:
            articlecontent['title']=soup.title.string
        except:
            print ("title  missing")

        try:
            articlecontent['main']=soup.find((By.TAG_NAME, "main")).get_text().replace('\n', ' ').strip()
        except:
            print ("main tag missing")


        output=json.dumps(articlecontent)

        try:
            f= open("./content/private_banking_search/output/"+id+".json","w+",encoding="utf-8")
            f.write(output)
            f.close()
        except:
            print ('issue writing file')

    finally:
        driver.quit()

