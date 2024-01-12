import os
import uuid
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup

def get_article_content(doc):
    
    id=str(uuid.uuid4())
    #dictionary for article content
    articlecontent={}
    articlecontent['id']=id
    articlecontent['url']=doc['url']
    print(doc['url'])
    
    try:
        articlecontent['title']=doc['title']
    except:
        print ("title  missing")
    
    try:
        articlecontent['summary']=doc['summary']
    except:
        print ("summary  missing")

    options = Options()
    options.add_argument('-headless')
    options.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'
    #options.add_argument("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36")
    options.set_preference("general.useragent.override", "Mozilla/5.0 (iPhone; CPU iPhone OS 15_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/101.0.4951.44 Mobile/15E148 Safari/604.1")
        
    driver = webdriver.Firefox(options=options)
    driver.get(doc['url'])
    
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "__next"))
            )
        
        try:
            element = driver.find_element(By.ID,'disclaimer')  
            driver.execute_script("""
            var element = arguments[0];
            element.parentNode.removeChild(element);
            """, element)
        except:
            pass

        try:
            element = driver.find_element(By.ID,'GpaSubscribe')  
            driver.execute_script("""
            var element = arguments[0];
            element.parentNode.removeChild(element);
            """, element)
        except:
            pass
        

        try:
            element = driver.find_element('nav')  
            driver.execute_script("""
            var element = arguments[0];
            element.parentNode.removeChild(element);
            """, element)
        except:
            pass
    
        
        content=driver.page_source
        soup=BeautifulSoup(content,'html.parser')

        try:
            tags=soup.find_all(['p', 'h1', 'h2', 'h3'])
            index = 0
            for tag in tags:
                text=tag.get_text().strip()

                if text !="":
                    index += 1
                    text=tag.get_text().strip()
                    articlecontent["tag-" +str(index)]=text
                    print ("tag found")
        except Exception as err:
            print(f"Unexpected {err=}, {type(err)=}")
        
        # try:
        #     articlecontent['h1-1']=soup.find(attrs={'class':'citigroup-h1'}).get_text()
        # except:
        #     print ("header 1 missing")

        # try:
        #     articlecontent['h1-2']=soup.find(attrs={'class':'detail-header'}).get_text()
        # except:
        #     print ("header 2 missing")

        # try:
        #     articlecontent['h1-3']=soup.find(attrs={'class':'detail-header'}).get_text()
        # except:
        #     print ("header 3 missing")

        # #body content

        # try:
        #     articlecontent['body-1']=soup.find(attrs={'class':'description___1Z5N5'}).get_text()
        # except:
        #     print ("body 1 missing")
        
        # try:
        #     articlecontent['body-2']=soup.find(attrs={'class':'summary___iwTwc'}).get_text()
        # except:
        #     print ("body 2 missing")

        # try:
        #     gridrows=soup.find_all(attrs={'class':'GridRow'})
        #     index = 0
        #     for gridrow in gridrows:
        #         if gridrow.get_text()!="":
        #             index += 1
        #             articlecontent['gridrow-'+str(index)]=gridrow.get_text()
        #             print ("grid row found")
        # except Exception as err:
        #     print(f"Unexpected {err=}, {type(err)=}")


        output=json.dumps(articlecontent)

        try:
            f= open("./content/global_search/output/"+id+".json","w+",encoding="utf-8")
            f.write(output)
            f.close()
        except:
            print ('issue writing file')

    finally:
        driver.quit()




#get_article_content('https://www.citigroup.com/global/about-us/heritage/1812/new-bank-born-in-new-york')