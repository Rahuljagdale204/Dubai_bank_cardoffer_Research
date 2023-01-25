# import scrapy
import yaml
from yaml import SafeLoader

# class offerSpider(scrapy.Spider):

# name = "offer"
# start_urls = []
# path = "banker/data/xpath.yaml"

# with open(path, 'r') as f:
#     data = yaml.load(f, Loader=SafeLoader)
#     for obj in data:
#         start_urls.append(data[obj]['baseurl'])


# bankname = []

# with open(path, 'r') as f:
#     data = yaml.load(f, Loader=SafeLoader)

#     for obj in data:
#         bankname.append(obj)
# i =0
# for url in start_urls:
#     print("[===================]")
#     print("url->",url)
#     print("Bankname: -",bankname[i])
#     i+=1
#     print("[===================]")

def crawl_url(data):
    xpath_list = data[obj]['xpaths']
    print("x_paths for the ",obj," : - ")
    for i in xpath_list:
        if(data[obj]['xpaths'][i]):
            print("entityname: ->",i,"entity_xpath->",data[obj]['xpaths'][i])



path = '/home/rahul/Downloads/Intership/Dubai_bank_cardoffer_Research/banker/data/testy.yaml'

    # def start_requests(self):

with open(path, 'r') as f:
    data = yaml.load(f, Loader=SafeLoader)

    for obj in data:
        
        if(data[obj]['baseUrl']):
            print(obj)
            crawl_url(data)
        

        else:
            print("url not present for ",obj)

        






