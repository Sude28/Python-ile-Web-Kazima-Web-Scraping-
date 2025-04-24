from selenium import webdriver
from selenium.webdriver.ie.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By


url = 'https://books.toscrape.com/'

options = webdriver.ChromeOptions()
options.add_argument('--headless') #Tarayıcımız arka planda çalışıcak ve biz onu görmiycez


service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)


##ETİKET İSMİ (TAG NAME) İLE ELEMENT SEÇME

#Tüm Elementler
driver.get(url)
list_items = driver.find_elements(By.XPATH,'//li')
print(len(list_items))

#İlk Element
list_items = driver.find_element(By.XPATH,'//li').text #Sadece seçim aşaması farklı sonrasında yapacağımız şeyler aynı
print(list_items)


##SINIF İSMİ (CLASS NAME) İLE ELEMENT SEÇME

#Tüm Elementler#
prices = driver.find_elements(By.XPATH, '//p[@class = "price_color"]')  #p etiketi içinde price_color sınıfı
for price in prices :
    print(price.text)

#İlk element
price = driver.find_element(By.XPATH, '//p[@class="price_color"]')
print(price.text)


##ID İLE ELEMENT SEÇME
body = driver.find_element(By.XPATH, '//body[@id="default"]')
print(body.text)


##ÖZELLİKLERİ(ATTRİBUTE) KULLANARAK ELEMENT SEÇME
alert = driver.find_element(By.XPATH, '//div[@role = "alert"]')
print(alert.text)


##İÇİNDEKİ METNİ(TEXT) KULLANARAK ELEMENT SEÇME    #XPATH'de en çok kullandığımız durum bu olucak çünkü bunu css selector ile yapamıyoruz
next_button = driver.find_element(By.XPATH,'//a[text()="next"]') #Özellikler sınıf ismi veya ıd'ye göre bakarken önüne @ yazıyorduk ama texte göre bakarken text() yazıyoruz  # İçinde next metni bulunan a elementini bana ver dedik
print(next_button.get_attribute('href'))


##İÇ İÇE (NESTED) OLAN ELEMENTLERİ SEÇME
img_src = driver.find_element(By.XPATH, '//article[@class = "product_pod"]/div/a/img').get_attribute('src')
print(img_src)


##ELEMENTİ SEÇTİKTEN SONRA:
 #İçindeki metni çıkarma --> element.text CSS Seçicileri ile aynı
 #ÖZELLİKLERİ(ATTRİBUTE) ÇIKARMA
# CSS Seçicileri ile aynı --> element.get_attribute('att_name')


##NAVİGASYON(SİBLİNG-PARENTS)
 #Elementin parent'ını (ebeveyni)bulma
first_book = driver.find_element(By.XPATH,'//article[@class = "product_pod"]')
#first_book_div = first_book.find_element(By.XPATH,'./div').get_attribute('class') #. first book anlamına geliyor
#print(first_book_div)
parent_of_first = first_book.find_element(By.XPATH,'./..') #first_bookile article seçmiştik bir üstü li'ye ulaştık iki nokta ile
print(parent_of_first.tag_name)

 #Elementin siblingini bulma (kardeş)
first_book = driver.find_element(By.XPATH,'//article[@class = "product_pod"]')
parent_of_first = first_book.find_element(By.XPATH,'./..') #first_bookile article seçmiştik bir üstü li'ye ulaştık iki nokta ile
following_sibling = parent_of_first.find_element(By.XPATH,'./following-sibling::li[1]') #Elementin üzerinde arama yaptığımız için ./ ile başlıyoruz. parent_of_first ile li'ye geldik zaten onun sonraki elementlerinden li elementini bul onun da ilkini ver bize  #following-siblingten sonra bulmak istediğimiz kardeş elementin tag ismini yazıyoruz
second_book_name = following_sibling.find_element(By.XPATH, './article/div/a/img') .get_attribute('alt') #alt alta giderek ismini çıkarıcaz
print(second_book_name)


book_name = driver.find_element(By.XPATH, '//article[@class = "product_pod"]/../following-sibling::li[1]/article/div/a/img').get_attribute('alt')
print(book_name)
#GENEL ORNEK --- BIR DAHA BAAK



#driver içinde arama yapıyorsak // , elementin üzerinde arama yapıyorsak ./
# iki nokta ..  ile parent'a gidilir
# :: kardeşe gidilir
