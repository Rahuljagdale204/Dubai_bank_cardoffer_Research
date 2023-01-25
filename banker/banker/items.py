# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BankerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


'''
  baseUrl:
  offerType: 
  shopname: 
  category:  
  validity: 
  offerlink:  
  image: 
'''

    
class offerItem(scrapy.Item):
    bankname = scrapy.Field()
    baseUrl = scrapy.Field()
    category = scrapy.Field()
    shopname = scrapy.Field()
    offertitle = scrapy.Field()
    validity = scrapy.Field()
    image = scrapy.Field()
    offerlink = scrapy.Field() 
    offerdetails = scrapy.Field()
    tnc = scrapy.Field()
    location = scrapy.Field()
    eligible = scrapy.Field()
    applylink = scrapy.Field()
