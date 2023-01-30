import scrapy
import yaml 
from yaml import SafeLoader
from bankcard.items import CardItem
import re

class Card(scrapy.Spider):
    name="card"
    path='bankcard/Data/data.yaml'

    def start_requests(self):
        with open(self.path,'r') as f:
            data=yaml.load(f,Loader=SafeLoader)
            for key,val in data.items():
                if(val['baseUrl']):
                    yield scrapy.Request(url=val['baseUrl'],meta={"BankName":key,"xp":val['xpaths'],"Newlink":val['cardUrl']})

    def parse(self, response):
        lisNew=response.xpath(response.meta['Newlink']).getall()
        name = response.meta['BankName']
        for link in lisNew:
            curl = response.urljoin(link)
            yield scrapy.Request(
                url=curl,method='GET',
                    callback=self.parse_items, meta={'bname':name, 'burl':curl, 'xp':response.meta['xp']})
    def parse_items(self, response):
        info=CardItem()
        info['bankName']=response.meta['bname']
        info['type']="Card"
        info['cardUrl'] = response.meta['burl']
        for key,val in response.meta['xp'].items():
            if val:
                if key=='benefits':
                    lisBen=[]
                    lishead=[]
                    lisDesc=[]
                    if val['title']:
                        lishead=response.xpath(val['title']).getall()
                
                    if val['description']:
                        lisDesc=response.xpath(val['description']).getall()
                 

                    if len(lishead)>=len(lisDesc):
                        for i in range(len(lisDesc)):
                            lisBen.append({"title":self.extract_desc(lishead[i]),"description":self.extract_desc(lisDesc[i])})
                        for i in range(len(lisDesc),len(lishead)):
                            lisBen.append({"title":self.extract_desc(lishead[i]),"description":'NA'})
                    else:
                        for i in range(len(lishead)):
                            lisBen.append({"title":self.extract_desc(lishead[i]),"description":self.extract_desc(lisDesc[i])})
                        for i in range(len(lishead),len(lisDesc)):
                            lisBen.append({"title":'NA',"description":self.extract_desc(lisDesc[i])})

                            
                  
                    info[key]=lisBen 

                elif key == 'image':
                        
                        info[key]=response.urljoin(response.xpath(val).get())
            
                    
                else:
                    
                    info[key]=self.removehtmllist(response.xpath(val).getall())
            elif key =='container':
                pass
            else:
                str1 = "NA"
                info[key] = str1
        yield info
           
           
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