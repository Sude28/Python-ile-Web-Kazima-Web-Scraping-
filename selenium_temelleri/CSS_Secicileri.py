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
list_items = driver.find_elements(By.CSS_SELECTOR, 'li') #li etiketlerini bulur
print(len(list_items))

#İlk Element
list_item = driver.find_element(By.CSS_SELECTOR,'li').text
print(list_item)


##SINIF İSMİ (CLASS NAME) İLE ELEMENT SEÇME

#Tüm Elementler
prices = driver.find_elements(By.CSS_SELECTOR,'p.price_color') #price_color ismine sahip olan p elementlerini bana ver
for price in prices :
    print(price.text)

#İlk element
price = driver.find_element(By.CSS_SELECTOR,'p.price_color')
print(price.text)


##ID İLE ELEMENT SEÇME  #id'ler en iyi yöntem çünkü sadece bir element için kullanılıyor
body = driver.find_element(By.CSS_SELECTOR, 'body#default') #sonrasında id ismi
#print(body.text)

body_ = driver.find_element(By.ID,'default') #Yukarıdaki ile aynı
print(body.text)


##ÖZELLİKLERİ(ATTRİBUTE) KULLANARAK ELEMENT SEÇME
alert = driver.find_element(By.CSS_SELECTOR,'div[role="alert"]') #div etiketinde role özelliği değeri alert'le birlikte
print(alert.text)


##İÇ İÇE (NESTED) OLAN ELEMENTLERİ SEÇME  #Bundan kastımız parent element seçicez ve içe içe giderek çocuklarına doğru ilerliycez
img_src = driver.find_element(By.CSS_SELECTOR,'article.product_pod div a img').get_attribute('src') # sınıfı product_pod olan article içinden div'e ordan a'ya ordan img'ye gittik
print(img_src)


##ELEMENTİ SEÇTİKTEN SONRA:
 #İçindeki metni çıkarma
the_first_book = driver.find_element(By.CSS_SELECTOR,'article.product_pod')
print(the_first_book.text)


 #ÖZELLİKLERİ(ATTRİBUTE) ÇIKARMA
warning_div = driver.find_element(By.CSS_SELECTOR,'div.alert-warning').get_attribute('role')
print(warning_div)

name_of_element= driver.find_element(By.CSS_SELECTOR,'article.product_pod img').get_attribute('alt')
print(name_of_element)






#<p class="highlight">Bu paragraf vurgulanmış bir paragraftır.</p> p etiket highlight sınıftır