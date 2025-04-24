import requests
from bs4 import BeautifulSoup

response = requests.get('https://quotes.toscrape.com/')
soup = BeautifulSoup(response.text,'html.parser')

#Başlık Elementini Bulma (ilgili satırı verir)
title = soup.find('title')
print(title)

#Başlık İçindeki Metni Bulma
title = soup.find('title').text
print(title)


###SEÇME###
##Class ismine göre ilk kodu seç
  #1. soup.find ile -> İlk bulduğu elementi return eder
first_quote = soup.find('div', class_='quote') #div etiketini arıyoruz, quote sınıfına ait -> div class="quote"
print(first_quote)


  #2. soup.find_all ile -> Bu class ismi ile bulduğu tüm elementleri return eder
quotes = soup.find_all('div',class_='quote') #birden fazla "quote" sınıfına sahip <div> etiketi varsa, hepsini alır
first_quote = quotes[0]
print(first_quote)

##"itemprop" özelliğini (attribute) kullanarak ilk quote'u seç ve textini bul
quote_text = first_quote.find('span',attrs={'itemprop':'text'}).text
#itemprop attribute(özelliği) text'e eşit olan span elemanını bul first_quote'nin içinde ve text'i istediğimiziçinde . text diyoruz
# div sınıfıın bir alt sınıfı olduğundan onu bulmuştuk ondan bir bulma yapıyoruz
print(quote_text)

##İçeriğindeki text'i kullanarak etiket başlığını (Top Ten tags başlığını seç sayfadaki )
tags_tittle = soup.find('h2',string='Top Ten tags')
print(tags_tittle)
#Sayfanın tamamında arama yapıyoruz.


###NAVİGASYON###
#Bir elementi kullanarak başka bir elemente erişmeye deniyor. Elementler arasında hiyerarşi olmasından kaynaklanıyor

##tags_tittle elementinin ebeveynini (parents) bul
tag_box = tags_tittle.parent
print(tag_box)

##tags_tittle elementinin sonraki kardeşini (next sibling) bul yani Top Ten tags başlığıyla aynı hizadaki ilk
first_tag_span = tags_tittle.find_next_sibling()
print(first_tag_span) #love yazan başlık

#first_tag_span elementinin önceki kardeşini (previous sibling) bul
h2 = first_tag_span.find_previous_sibling()
print(h2)

#tag_box elementinin çocuklarını (children) bul [tag_box tags_tittle'ın ebeveyni]
tag_children = tag_box.children
list_of_children = list(tag_children)
for child in list_of_children:
    print(child)
# Direkt liste döndürmüyor list_iterator döndürüyor bu nedenle listeye çeviriyoruz



###DEGERLERİ ELDE ETME###
#Bir elementi elde ettikten sonra içerisindeki değerleri çıkarma

##top_tag(başlıktan sonraki ilk)  elementinin href değerini çıkart
top_tag_a = first_tag_span.a #a elementine ulaştık
top_tag_href = top_tag_a['href']
print(top_tag_href)

#Bu yöntemle tüm attribute(özellikleri) elde ederiz
top_tag_class = top_tag_a['class']
print(top_tag_class)

top_tag_style = top_tag_a['style']
print(top_tag_style)
#Böylece style özelliğine de erişmiş olduk ve değerini ekrana yazdı