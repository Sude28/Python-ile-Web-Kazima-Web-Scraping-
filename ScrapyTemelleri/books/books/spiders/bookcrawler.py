import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..items import BookItem

number_dict = {'One':'1', 'Two': '2', 'Three':'3', 'Four':'4', 'Five':'5'}


class BookcrawlerSpider(CrawlSpider):
    name = "bookcrawler"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com"]

    #Kuralları tanımlıycaz çünkü bu haliyle her sayfaya girebilir. allow yani izin ver kısmında ayarlıycaz hangi url'lere gitmesi gerektiğini. callback ile de bu sayfaya git ve veri al ayarını yapıyoruz.
    #Bizim  linkimiz için kitaplara girsin, next butonuna bassın ama kategorilerin butonlarına basmasın onu istemiyoruz mesela onu ayarlıycaz url'den
    rules = (Rule(LinkExtractor(allow='catalogue/page'),), #sayfaları gezicez veri kazımıycaz o yüzden callback olmuycak. Kategori yazan sayfalara girerse catalogue/page olur url'de oraya girsin istemiyorum. Herhangi bir döngü vs yazmadan sayfalar arasında gezinmeyi bu satırla yaptık
             Rule(LinkExtractor(allow='catalogue' , deny=('category', 'page')), callback="parse_item", follow=False)) #verileri kazıycaz yani kıtapların içine giricez ve veri çekicez bir şeye tıklamıycaz o yüzden follow false. Kategoriden ve kitaptan kitaba geçişi engelledik deny ile


    def parse_item(self, response):
        book = BookItem()
        book['name'] = response.css('div.product_main h1::text').get()  # divin product main sınıfının içinde h1 etiketinde
        book['price_exc_tax'] = response.xpath('//th[text()="Price (excl. tax)"]/following-sibling::td[1]/text()').get()
        book['price_inc_tax'] = response.xpath('//th[text()="Price (incl. tax)"]/following-sibling::td[1]/text()').get()
        book['upc'] = response.xpath('//th[text()="UPC"]/following-sibling::td[1]/text()').get()
        book['availability'] = response.xpath('//th[text()="Availability"]/following-sibling::td[1]/text()').get()
        book['tax'] = response.xpath('//th[text()="Tax"]/following-sibling::td[1]/text()').get()

        category_children = response.xpath('//ul[@class="breadcrumb"]/child::*')  # lass'ı "breadcrumb" olan <ul> etiketini seçer.child::* ifadesi, bu <ul> içindeki tüm doğrudan çocukları alır.
        book['category'] = category_children[2].css('a::text').get()  # 3.li'yi seçtik ve texti çıkardık

        star_tag = response.css('p.star-rating')  # response.css('p.star-rating') ifadesi, sayfadaki <p> etiketi içinde class="star-rating" olan HTML öğesini seçer.
        class_name_string = star_tag.attrib['class']  # star_tag.attrib['class'], yukarıda seçtiğimiz <p> etiketinin class niteliğini (class="star-rating Three") alır.
        # star-rating Three
        stars = class_name_string.split(' ')[-1]  # star-rating Three ifadesinin son eleöanı olan Three'yi aldık
        book['stars'] = number_dict[stars]  # Three 3'ye eşit olduğundan 3 dönücek # int değil string ama sayı halinde

        book['image_url'] = 'https://books.toscrape.com' + response.css('div.active img').attrib['src'][5:]
        # ../../media/cache/fe/72/fe72f0532301ec28892ae79a629a293c.jpg baştakileri almadık o yüzden 5.den başladık. Başlangıca da sayfanın url'sini ekleyince tam bir bağlantı oldu

        yield book  # Scrapy'nin bu veriyi dışarıya (pipeline veya dosya gibi) göndermesi anlamına gelir. crapy otomatik olarak yield edilen veriyi alıp kaydeder.
