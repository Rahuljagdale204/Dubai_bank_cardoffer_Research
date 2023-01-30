import scrapy
import yaml
from yaml.loader import SafeLoader
from scrapy.loader import ItemLoader
from banker.items import offerItem

import re
'''
  baseUrl: 
  image:  
  category:  
  validity: 
  offerlink:  
  shopname: 
  offertitle:  
  xpaths:
    offerdetails:
    tnc:
'''

class Bankoffer(scrapy.Spider):

    name="offer"

    path = 'data/offerxpath.yaml.yaml'
    def start_requests(self):
        with open(self.path, 'r') as f:
            data = yaml.load(f, Loader=SafeLoader)
            for key, obj in data.items():
                if obj['baseUrl']:
                    
                    yield scrapy.Request(url=obj['baseUrl'],method='GET',callback=self.parse, meta={"data":obj,"xp": obj['xpaths'],"bank": key, "items": obj['shopname']})


    def parse(self, response):
        
        valdata = ['category','location','validity', 'shopname','offertitle', 'offerdetails','tnc']
        
        num = response.xpath(response.meta['items']).getall()
        for i in range(len(num)):
            card = offerItem()
            for key, val in response.meta["data"].items():
                if val:
                    
                    card['bankname'] = response.meta["bank"]
                    card['baseUrl'] = response.url

                    if (key in valdata):
                        
                        value1 = response.xpath(val).getall()
                        card[key] = self.extract_desc(value1[i])

                    elif(key=='image'):
                        links = response.xpath(val).getall()
                        card[key] = response.urljoin(links[i])

                    elif(key=='offerlink'):
                        value4 = value1 = response.xpath(val).getall()
                        cUrl = response.urljoin(value4[i])
                        card[key] = cUrl
                        yield scrapy.Request(url=cUrl,method='GET',callback=self.parse_items,meta = {"xp":response.meta["xp"], "card":card})
            yield card
                 
            
           
    def parse_items(self,response):
        
        for key, val in response.meta['xp'].items():
            if val:
                if(key=='image'):
                    links = response.xpath(val).getall()
                    response.meta['card'][key]  = response.urljoin(links)
                elif(key == 'applylink'):
                    links = response.xpath(val).getall()
                    response.meta['card'][key]  = response.urljoin(links)
                
                else:
                    value = response.xpath(val).getall()
                    response.meta['card'][key] = self.removehtmllist(value)
       
        yield response.meta['card']
        

    
    def extract_desc(self, string):
        string = string.replace('\r', '').replace('\n','')
        string = re.sub(' +', ' ', string)
        regex = re.compile(r'<[^>]+>')
        return regex.sub('', re.sub(' +', ' ', string)).strip()

    def removehtmllist(self,value1):
        value1= list(map(lambda x:x.strip(),set(value1)))
        regex = re.compile(r'<[^>]+>')
        value2 = ""
        for val in value1:
            string1 = regex.sub('', val).strip()
            string1 = re.sub(' +', ' ', string1)
            value2 = value2+string1
        return value2


                    
        
    

    