import scrapy

class BankerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

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

class CardItem(scrapy.Item):
    bankName=scrapy.Field()
    type=scrapy.Field()
    cardUrl = scrapy.Field()
    image=scrapy.Field()
    typeOfCard=scrapy.Field()
    nameOfCard=scrapy.Field()
    information=scrapy.Field()
    benefits=scrapy.Field()

class CardItememi(scrapy.Item):
    bankname = scrapy.Field()
    cardurl = scrapy.Field()
    nameOfCard = scrapy.Field()
    typeOfCard = scrapy.Field()
    info = scrapy.Field()
    benefits = scrapy.Field()
    image = scrapy.Field()
    tnc = scrapy.Field()
    
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

