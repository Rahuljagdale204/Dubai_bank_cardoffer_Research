import scrapy
import yaml
from yaml.loader import SafeLoader
from bankcard.items import CardItem
import re
'''
baseUrl:
nexturl:
xpath:
    image:
    typeOfCard:
    nameOfCard:
    info:
    benifits:
        title:
        desc:
'''


class cardsSpider(scrapy.Spider):
    filePath = '/home/rahul/Downloads/Intership/Dubai_bank_cardoffer_Research/bankcard/bankcard/Data/testfile.yaml'
    # filePath = '/home/unfixedbug/Desktop/Internship/dubai_banks_crawler/banker/data/CardData.yaml'
    name = "cards"

    # initial requests
    def start_requests(self):
        with open(self.filePath, 'r') as f:
            data = yaml.load(f, Loader=SafeLoader)
            for key, obj in data.items():
                if obj['baseUrl']:
                    self.logger.info(f"Sending requets for {key}")
                    yield scrapy.Request(url=obj['baseUrl'], meta={"xp": obj['xpath'], "bankName": key, "itemPath": obj['nexturl']})

    def parse(self, response):
        card = CardItem()

        if len(response.meta["itemPath"]) is 0:
            '''
            cards = response.xpath(
                response.meta["xp"]['container']).getall() #cards has all single cards
            for card in cards:
                # traverse xpaths len(cards) times
            '''
            for key, val in response.meta["xp"].items():
                # add containerisation

                if val:
                    if key == 'benefits':
                        AllBenifits = {}
                        titleList = response.xpath(val['title']).getall()
                        DescList = response.xpath(val['desc']).getall()
                        for title, Desc in zip(titleList, DescList):
                            AllBenifits.update({
                                title: self.extract_desc(Desc)
                            })
                        card['benefits'] = AllBenifits
                    elif key == 'image':
                        card[key] = response.urljoin(self.extract_desc(
                            response.xpath(val).get()))
                    else:
                        card[key] = self.removehtmllist(
                            response.xpath(val).get())
            if not card['info'] and not card['typeOfCard']:
                return
            card['nameOfBank'] = response.meta['bankName']
            card['cardUrl'] = response.url
            yield card
        # if it has next links then pass the link as url
        # extract links
        nextPath = response.meta["itemPath"]
        links = response.xpath(nextPath).getall()

        for link in links:
            # if link has https tag, then parse else get it from completeUrl
            cUrl = response.urljoin(link)

            yield scrapy.Request(
                url=cUrl,
                callback=self.parse_items, meta=response.meta)

    def parse_items(self, response):
        Card = CardItem()
        for key, val in response.meta["xp"].items():
            if val:
                if key == 'benefits':
                    AllBenifits = {}
                    titleList = []
                    DescList = []
                    if val['title']:
                        titleList = response.xpath(val['title']).getall()
                    if val['desc']:
                        DescList = response.xpath(val['desc']).getall()
                    for title, Desc in zip(titleList, DescList):
                        AllBenifits.update({
                            title: self.extract_desc(Desc)
                        })
                    Card[key] = AllBenifits
                elif key == 'image':
                    Card[key] = response.urljoin(self.extract_desc(
                        response.xpath(val).get()))
                else:
                    Card[key] = self.extract_desc(
                        response.xpath(val).get())
        Card['nameOfBank'] = response.meta['bankName']
        Card['cardUrl'] = response.url
        yield Card

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