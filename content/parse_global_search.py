import os,sys, json
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(PROJECT_ROOT)
import scrapers.global_search_scraper as scraper

dir_path = os.path.dirname(os.path.realpath(__file__))+"\\global_search\\pages\\"

urls=[]
i=0
for filename in os.listdir(dir_path):
    filepath=dir_path+filename

    if ".json" in filepath: 
        json_file = open(filepath,encoding='utf-8')
        file_text=json_file.read()
        #print(filepath)
        data = json.loads(file_text)
        for doc in data['docs']:
            try:
                if doc['url'].count('http://') ==0 and doc['url'].count('https://') ==0 :
                    url="https://www.citigroup.com"+ doc['url']
                else:
                    url=doc['url']

                if doc['url'].count('citigroup.com') !=0:
                    i=i+1
                    print(i)
                    scraper.get_article_content(doc)
            except:
                pass
            
        json_file.close()
# i=0;
# for url in urls:
#     i=i+1
#     print (i)
#     print("downloading url::::::::" + url)
#     #scraper.get_article_content(url)
