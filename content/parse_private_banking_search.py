import os,sys, json
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(PROJECT_ROOT)
import scrapers.private_banking_scaper as scraper

file = os.path.dirname(os.path.realpath(__file__))+"\\private_banking_search\\private_bank_urls.txt"

urls=[]
i=0;
with open(file) as urls:
    for line in urls:
        url=line.rstrip('\n')
        i=i+1
        print (i)
        print (url)  # The comma to suppress the extra new line char
        scraper.get_private_banking_page_content(url)
