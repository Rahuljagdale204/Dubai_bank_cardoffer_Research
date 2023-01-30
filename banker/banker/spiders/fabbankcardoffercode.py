# python scraper code for the pagination bank information code 
# example: - fab bank

import scrapy
import yaml
from yaml.loader import SafeLoader
from banker.items import CardItemfab
from scrapy_splash import SplashRequest
import re

class Bankcard(scrapy.Spider):
    name="fabbankcard"
    path = 'banker/data/fabbank.yaml'

    def start_requests(self):
        with open(self.path, 'r') as f:
            data = yaml.load(f, Loader=SafeLoader)
            for key, obj in data.items():
                if obj['baseUrl']:
                   
                    yield SplashRequest(url=obj['baseUrl'],callback=self.parse, meta ={'xp':obj['xpath'],"itemPath":obj['xpath']['nameOfCard'],"bankName":key})

    def parse(self, response):
        nextPath = response.meta["itemPath"]
        cardnumber = response.xpath(nextPath).getall()
        name = response.meta["bankName"]
        for i in range(len(cardnumber)):
            card = CardItemfab()       
            
            for key, val in response.meta["xp"].items():
                if val:
                    card['bankname'] = name
                    if key == 'image':
                        links = response.xpath(val).getall()
                        card[key] = response.urljoin(links[i])
                        
                    elif key=='benefits' or key=='cardoffer':
                        pass                   
                    elif key=='cardurl':
                        links = response.xpath(val).getall()
                        cUrl= response.urljoin(links[i])
                        card[key] = cUrl
                        yield SplashRequest(
                            url=cUrl,method='GET',
                            callback=self.parse_items, meta={'maincard':card,'cardoffer':response.meta['xp']['cardoffer'], 'xp':response.meta['xp']})
                    
                    else:
                        value2 = response.xpath(val).getall()
                        card[key] = self.extract_desc(value2[i])    
        yield card                

    def parse_items(self, response):
        
        card2 = response.meta['maincard']
             
        for key, val in response.meta["cardoffer"].items():
            if val:
                if(key=='offerlink'):
                    links = response.xpath(val).getall()
                    
                    for curl in links:
                        curl = response.urljoin(curl)
                        card2[key] = curl
                        
                        yield SplashRequest(
                            url=curl,method='GET',
                            callback=self.parse_items_offer, meta={'maincard':card2,'cardoffer':response.meta['cardoffer']})

        card2['Atype'] = 'Card'
        links1 = response.xpath(response.meta["cardoffer"]['offerlink']).getall()
        links2 = []
        for i in links1:
            links2.append(response.urljoin(i))
        card2['all_links'] = links2 
        yield card2
       

                
    def parse_items_offer(self, response):
       
        card3 = response.meta['maincard']
        card3['Atype'] = 'Offer'
        for key, val in response.meta['cardoffer'].items():
            if val:               
                if key=='cardoffdetails':
                   
                    offerdetails = []
                    titleList = response.xpath(val['offerdesciber']).getall()
                    DescList = response.xpath(val['offerinfo']).getall()  
                    for title, Desc in zip(titleList, DescList):
                        offerdetails.append({
                            "offerdesciber":(title),
                            "offerinfo":self.extract_desc(Desc)
                            
                        })
                    card3[key] = (offerdetails)
                elif key=='offerlink':
                    pass
                
                elif key=='coffname' or key == 'information' or key =='validity' or key=='eligible':
                    value3 = response.xpath(val).getall()
                    card3[key] = self.removehtmllist(value3)
        yield card3

    def extract_desc(self, string):
        string = string.replace('\r', '').replace('\n','')
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


    





'''
    code for test
    import scrapy
import yaml
import scrapy_splash
from yaml.loader import SafeLoader
from bankcard.items import CardItem
from scrapy.linkextractors import LinkExtractor

from scrapy_splash import SplashRequest
import re



lua_script = """
function main(splash,args)
    assert(splash:go(args.url)) 

    local element = splash.select('body>div[@class='col-lg-12 view-more-btn-container']>button')
    element:mouse_click()

    splash:wait(splash.args.wait)
    return splash:html()
"""

class Bankcard(scrapy.Spider):

    name="fabbank"
    # start_urls = ["https://www.cbd.ae/personal/bank/cards"]

    path = '/home/rahul/Downloads/Intership/Dubai_bank_cardoffer_Research/bankcard/bankcard/Data/testfile.yaml'

    def start_requests(self):
        with open(self.path, 'r') as f:
            data = yaml.load(f, Loader=SafeLoader)
            for key, obj in data.items():
                if obj['baseUrl']:
                    self.logger.info(f"Sending requets for {key}")
                    yield SplashRequest(url=obj['baseUrl'],method='GET',callback=self.parse, 
                    meta={"xp": obj['xpath'],"bankName": key, "itemPath": obj['xpath']['nameOfCard']}
                    )

                   

    def parse(self, response):

        nextPath = response.meta["itemPath"]
        cardnumber = response.xpath(nextPath).getall()
        name = response.meta["bankName"]
        
        for i in range(len(cardnumber)):
            card = CardItem()
            
            # card['cardlink'] = response.meta['burl']
            for key, val in response.meta["xp"].items():
                if val:
                    card['bankname'] = name
                    if key == 'image':
                        links = response.xpath(val).getall()
                        card[key] = response.urljoin(links[i])
                        
                    elif key=='benefits':
                        pass
                    
                        
                    elif key=='cardurl':
                        links = response.xpath(val).getall()
                        cUrl= response.urljoin(links[i])
                        card['cardlink'] = cUrl
                        # yield scrapy.Request(
                        #     url=cUrl,method='GET',
                        #     callback=self.parse_items, meta={'maincard':card, 'xp':response.meta['xp']})

                    else:
                        value2 = response.xpath(val).getall()
                        card[key] = self.extract_desc(value2[i])

            yield card



    def extract_desc(self, string):
        string = string.replace('\r', '').replace('\n','')
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

'''