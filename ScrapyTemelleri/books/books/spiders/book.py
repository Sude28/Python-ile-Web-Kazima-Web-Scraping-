import scrapy
from unicodedata import category

from ..items import BookItem

number_dict = {'One':'1', 'Two': '2', 'Three':'3', 'Four':'4', 'Five':'5'}

#Parse methodile sayfalar arasında gezinicez, linkleri topluycaz ve request yapıcaz, sonraki sayfa var mı yok mu kontrol edicez varsa request yapıp parse methodunu çağırıcaz yine. Verileri kazımak için yaptığımız requestte başka bşr methodu çağırıcaz
class BookSpider(scrapy.Spider):
    name = "book"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com"]

#Parse ile kitapların linklerine gidicez, parse_books ile de kazıycaz

    def parse(self, response):    #Bu response otomatik olarak start_urls'e yapılan requestin sonucu
        book_links = response.css('article.product_pod h3 a::attr(href)').getall() #Bir değer çıkaracaksak toplu bir şekilde alamıyorduk selenium ve beatiful soup ile döngü oluşturuyorduk. Burada attr ve getall kullanımı tek satırda içeriden çıkaracağımız değerlerin listesini veriyor
        for book_link in book_links:
            yield response.follow(book_link,callback=self.parse_books)   #request yapmanın bir yöntemi scrapy ile. Her kitabın linkine git (book_link) ve orada parse methodunu çalıştır

        next_page_link = response.css('li.next a::attr(href)').get()  #li'nin class= next'inden a etiketine gidip hrefi alıcaz
        if next_page_link is not None:
            yield response.follow(next_page_link,callback=self.parse) #içinde bulunduğumuz methodu çağrıyor diğer sayfa için. İlk sayfaya request yaptık ve parse_book methodu ilie heopsini kazıdık sonrasında ikinci sayfa var mı diye kontrol ediyoruz var mı var o zaman ikinci sayfa için aynılarını yapmak için yine bu fonksiyonu çağırıyuoruz. Yani bunu loop gibi kullandık

    def parse_books(self, response):
        book = BookItem()
        book['name'] = response.css('div.product_main h1::text').get() #divin product main sınıfının içinde h1 etiketinde
        book['price_exc_tax'] = response.xpath('//th[text()="Price (excl. tax)"]/following-sibling::td[1]/text()').get()
        book['price_inc_tax'] = response.xpath('//th[text()="Price (incl. tax)"]/following-sibling::td[1]/text()').get()
        book['upc'] = response.xpath('//th[text()="UPC"]/following-sibling::td[1]/text()').get()
        book['availability'] = response.xpath('//th[text()="Availability"]/following-sibling::td[1]/text()').get()
        book['tax'] = response.xpath('//th[text()="Tax"]/following-sibling::td[1]/text()').get()

        category_children =response.xpath('//ul[@class="breadcrumb"]/child::*') #lass'ı "breadcrumb" olan <ul> etiketini seçer.child::* ifadesi, bu <ul> içindeki tüm doğrudan çocukları alır.
        book['category'] = category_children[2].css('a::text').get() #3.li'yi seçtik ve texti çıkardık

        star_tag = response.css('p.star-rating') #response.css('p.star-rating') ifadesi, sayfadaki <p> etiketi içinde class="star-rating" olan HTML öğesini seçer.
        class_name_string = star_tag.attrib['class'] #star_tag.attrib['class'], yukarıda seçtiğimiz <p> etiketinin class niteliğini (class="star-rating Three") alır.
        #star-rating Three
        stars = class_name_string.split(' ')[-1] #star-rating Three ifadesinin son eleöanı olan Three'yi aldık
        book['stars'] = number_dict[stars] #Three 3'ye eşit olduğundan 3 dönücek # int değil string ama sayı halinde

        book['image_url'] ='https://books.toscrape.com' +  response.css('div.active img').attrib['src'][5:]
        #../../media/cache/fe/72/fe72f0532301ec28892ae79a629a293c.jpg baştakileri almadık o yüzden 5.den başladık. Başlangıca da sayfanın url'sini ekleyince tam bir bağlantı oldu

        yield book #Scrapy'nin bu veriyi dışarıya (pipeline veya dosya gibi) göndermesi anlamına gelir. crapy otomatik olarak yield edilen veriyi alıp kaydeder.