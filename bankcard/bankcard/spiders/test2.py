# python scraper code for the pagination bank information code 
# example: - Emirates Islamic
'''
    yaml file: - 
    Emirates Islamic:
    baseUrl: https://www.emiratesislamic.ae/eng/personal-banking/cards/credit-cards/
    xpath:
        container:
        image:  //div[@class='card-deck']/div/a/img/@src
        typeOfCard:
        nameOfCard: //div[@class='card-deck']/div/a/../div[1]/h3/a/text()
        info: //div[@class='card-deck']/div/a/../div[1]/div/ul
        cardurl: //div[@class='card-deck']/div/a/@href
        benefits:
        title: //div[@class="benefit-text"]/h3/text() | //div[@class='card']/h3/text()
        desc: //div[@class="benefit-text"]/p/text() | //div[@class='card']/h3/..
'''

import scrapy
import yaml
from yaml.loader import SafeLoader
from bankcard.items import CardItem

import re


class Bankcard(scrapy.Spider):

    name="cardtest2"
    # start_urls = ["https://www.cbd.ae/personal/bank/cards"]

    path = '/home/rahul/Downloads/Intership/Dubai_bank_cardoffer_Research/bankcard/bankcard/Data/testfile.yaml'

    def start_requests(self):
        with open(self.path, 'r') as f:
            data = yaml.load(f, Loader=SafeLoader)
            for key, obj in data.items():
                if obj['baseUrl']:
                    self.logger.info(f"Sending requets for {key}")
                    yield scrapy.Request(url=obj['baseUrl'],method='GET',callback=self.parse, meta={"xp": obj['xpath'],"bankName": key, "itemPath": obj['xpath']['nameOfCard']})

    

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
                        yield scrapy.Request(
                            url=cUrl,method='GET',
                            callback=self.parse_items, meta={'maincard':card, 'xp':response.meta['xp']})

                    else:
                        value2 = response.xpath(val).getall()
                        card[key] = self.extract_desc(value2[i])

            yield card

  # baseUrl:  
  # cardurl: 
  # xpath:
  #   container:
  #   image: 
  #   typeOfCard: 
  #   nameOfCard:
  #   info:
  #   benefits: 
  #     title:  
  #     desc

    def parse_items(self, response):
        
        
        card2 = response.meta['maincard']
        
        for key, val in response.meta["xp"].items():
            if val:
                    
                if key=='benefits':
                    AllBenifits = []
                    titleList = response.xpath(val['title']).getall()
                    DescList = response.xpath(val['desc']).getall()
                     
                    for title, Desc in zip(titleList, DescList):
                        AllBenifits.append({
                            "title":(title),
                            "Desc":self.extract_desc(Desc)
                        })
                        
                    card2[key]=(
                        AllBenifits
                    )
                    
                else:
                    card2[key] = self.extract_desc(response.xpath(val).getall())
                
        yield card2

    

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

    
