import scrapy
import yaml
from yaml.loader import SafeLoader
from bankcard.items import CardItem

import re


class Bankcard(scrapy.Spider):

    name="cardtest"
    # start_urls = ["https://www.cbd.ae/personal/bank/cards"]

    path = '/home/rahul/Downloads/Intership/Dubai_bank_cardoffer_Research/bankcard/bankcard/Data/testfile.yaml'

    def start_requests(self):
        with open(self.path, 'r') as f:
            data = yaml.load(f, Loader=SafeLoader)
            for key, obj in data.items():
                if obj['baseUrl']:
                    self.logger.info(f"Sending requets for {key}")
                    yield scrapy.Request(url=obj['baseUrl'],method='GET',callback=self.parse, meta={"xp": obj['xpath'],"bankName": key, "itemPath": obj['nexturl']})

    

    def parse(self, response):

        nextPath = response.meta["itemPath"]
        links = response.xpath(nextPath).getall()
        
        for link in links:
            cUrl= response.urljoin(link)
            
            yield scrapy.Request(
                url=cUrl,method='GET',
                callback=self.parse_items, meta=response.meta)

    def parse_items(self, response):
        pass
        
        card = CardItem()
        card['bankname'] = response.meta['bankName']
        card['baseurl'] = response.meta['itemPath']
        for key, val in response.meta["xp"].items():
            if val:
                if key == 'benefits':
                    # Allbenefits = {}
                    # titleList = response.xpath(val['title']).getall()
                    # DescList = response.xpath(val['desc']).getall()
                     
                    # for title, Desc in zip(titleList, DescList):
                    #     Allbenefits.update({
                    #         title: self.extract_desc(Desc)
                    #     })
                        
                    # card[key]=(
                    #     Allbenefits
                    # )
                    continue
                else:
                    card[key]=(
                        self.removehtmllist(response.xpath(val).getall())
                    )
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

    
