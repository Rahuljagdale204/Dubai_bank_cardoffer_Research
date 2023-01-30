# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BankerItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()

    pass


class CardItem(scrapy.Item):
    bankname = scrapy.Field()
    cardlink = scrapy.Field()
    nameOfCard = scrapy.Field()
    typeOfCard = scrapy.Field()
    info = scrapy.Field()
    benefits = scrapy.Field()
    image = scrapy.Field()
    tnc = scrapy.Field()
    
    

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

# applylink:  //div[@class='product-card__offer']/a/@href
#       cardoffer:
#         coffname: //h1[@class='bold']/text()
#         information: //p[@class='h3 bold']/text()
#         validity: //div[@class='caption']/h2/text()
#         cardoffdetails:
#             offerdesciber: //div[@class='info-card offer-benefits-info main']/h2/text()
#             offerinfo:  //div[@class='info-card offer-benefits-info main']/div/p/text()
#             eligible

class CardItemfab(scrapy.Item):
    bankname = scrapy.Field()
    cardurl = scrapy.Field()
    nameOfCard = scrapy.Field()
    typeOfCard = scrapy.Field()
    info = scrapy.Field()
    benefits = scrapy.Field()
    image = scrapy.Field()
    tnc = scrapy.Field()
    offerlink = scrapy.Field()
    cardoffer = scrapy.Field()
    coffname = scrapy.Field()
    information = scrapy.Field()
    validity = scrapy.Field()
    cardoffdetails = scrapy.Field()
    eligible = scrapy.Field()
    all_links = scrapy.Field()
    Atype = scrapy.Field()