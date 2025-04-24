from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.ie.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

url = 'https://quotes.toscrape.com/js-delayed' #gecikmeli versiyonu

options = webdriver.ChromeOptions()
options.add_argument('--start-maximized') #Tarayıcımızın tam ekran modunda çalışmasını sağlayacak
options.add_experimental_option('detach',True) #Tarayıcımız kendi kendine kapanmayacak

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)
#driver.implicitly_wait(3) #WebDriverWait bir tanesi içindi bu genel herhangi bir elemanı bulurken . 3 saniye gibi yüklenmesinden az süre girince ise hata vermiyor 0 sonucu çıkıyor

driver.get(url)

#Ucuncu yontem;
sleep(15)


#WebDriverWait(driver, 15).until(  #şuna kadar bekle anlamında
#    EC.presence_of_element_located((By.CSS_SELECTOR, 'div.quote')) #elemanı sayfada bulmaya çalış eğer bulamazsan 15 saniye bekle sonra devam et
#
#)

#Genel durumlar için implicitly_wait kullanıyoruz ve saniyeyi düşük tutuyoruz çünkü her elemanı beklersek çalışma süresi uzar diye ama spesifik bir eleman için WebDriverWait kullanıyoruz ve bekliyoruz yüklenmesini. İkisini beraber kullanınca WebDriverWait baskın geliyor ve bekliyor o süreyi
quotes = driver.find_elements(By.CSS_SELECTOR, 'div.quote')
print(len(quotes))

