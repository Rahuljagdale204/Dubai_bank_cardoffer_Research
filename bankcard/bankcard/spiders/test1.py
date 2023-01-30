import scrapy
import yaml
from yaml.loader import SafeLoader
from bankcard.items import CardItem
import re

class Bankcard(scrapy.Spider):
    name="cardtest"
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
        name = response.meta["bankName"]
        
        for link in links:
            cUrl= response.urljoin(link)
            
            yield scrapy.Request(
                url=cUrl,method='GET',
                callback=self.parse_items, meta={'bankName':name, 'burl':cUrl, 'xp':response.meta['xp']})
    def parse_items(self, response):    
        card = CardItem()
        card['bankname'] = response.meta['bankName']
        card['cardlink'] = response.meta['burl']
        for key, val in response.meta["xp"].items():
            if val:
                if key == 'image':
                    links = response.xpath(val).get()
                    card[key] = response.urljoin(links)
                    
                elif key=='benefits':
                    AllBenifits = []
                    titleList = response.xpath(val['title']).getall()
                    DescList = response.xpath(val['desc']).getall()
                     
                    for title, Desc in zip(titleList, DescList):
                        AllBenifits.append({
                            "title":(title),
                            "Desc":self.extract_desc(Desc)
                        })     
                    card[key]=(
                        AllBenifits
                    )
                else:
                    card[key] = self.removehtmllist(response.xpath(val).getall())   
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

    
