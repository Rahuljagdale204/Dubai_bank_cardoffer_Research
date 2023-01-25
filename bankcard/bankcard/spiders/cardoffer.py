
import scrapy
import yaml 
from yaml import SafeLoader
from bankcard.items import CardItem
import re

class Card(scrapy.Spider):
    name="card"
    path='/home/rahul/Downloads/Intership/Dubai_bank_cardoffer_Research/bankcard/bankcard/Data/testfile.yaml'

    def start_requests(self):
        with open(self.path,'r') as f:
            data=yaml.load(f,Loader=SafeLoader)
            for key,val in data.items():
                if(val['baseUrl']):
                    yield scrapy.Request(url=val['baseUrl'],meta={"BankName":key,"xp":val['xpath'],"Newlink":val['nexturl']})


    
    def parse(self, response):
        lisNew=response.xpath(response.meta['Newlink']).getall()
    
        for link in lisNew:
            curl = response.urljoin(link)
            
            yield scrapy.Request(
                url= curl,
                meta=response.meta,
                callback=self.parse_items
            )
        
    def parse_items(self, response):
        info=CardItem()
        info['bankname']=response.meta['BankName']
        for key,val in response.meta['xp'].items():
            if val:
                if key=='benefits':
                    lisBen={}
                    lishead=response.xpath(val['title']).getall()
                    lisDesc=response.xpath(val['desc']).getall()

                    for h,i in zip(lishead,lisDesc):
                        lisBen.update({h:self.extract_desc(i)})
                    if len(lisBen)!=0:
                        info[key]=lisBen 

                elif key == 'image':
                        
                    info[key]=response.urljoin(response.xpath(val).get())
            
                    
                else:
                    info[key]=response.xpath(val).getall()
        yield info
           
           
    def extract_desc(self, string):
            string = string.replace('\r', '').replace('\n','')
            regex = re.compile(r'<[^>]+>')
            return regex.sub('', re.sub(' +', ' ', string)).strip()

    def removehtmllist(self,value1):
        value1= list(map(lambda x:x.strip(),value1))
        regex = re.compile(r'<[^>]+>')
        value2 = []
        for val in value1:
            string1 = regex.sub('', val).strip()
            string1 = re.sub(' +', ' ', string1)
            value2.append(string1)
        return list(set(value2))


