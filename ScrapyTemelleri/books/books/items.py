# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

#Kazıdığımız verileri daha kolay bir şekilde yönetmemizi sağlayan dosya. Kullanım mantığı beatiful soup ve seleniumda kullandığımız dictionary ile aynı. Burada book ıtem tanımlıyoruz ve almak istediğimiz alanların isimlerini tanımlıyoruz, sonrasında parse book methodunun yani verileri kazıdığımız methodun içinde çağırıp instance oluşturucaz.
class BooksItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class BookItem(scrapy.Item):
    name = scrapy.Field()
    price_exc_tax = scrapy.Field()
    price_inc_tax = scrapy.Field()
    category = scrapy.Field()
    stars = scrapy.Field()
    upc = scrapy.Field()
    tax = scrapy.Field()
    availability = scrapy.Field()
    image_url = scrapy.Field()