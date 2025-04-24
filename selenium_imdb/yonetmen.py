# Drama kategorisinde 'Best Director'ödülünü alan yönetmenleri bulup boylarını kaydedicez.
# https://www.imdb.com/search/title/ linkinden başlıycaz

#1.Kütüphaneleri import etme
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.ie.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
import pandas as pd
import openpyxl



#2.Veriyi kaydetmek için dictionary oluşturmak. Key'ler: name,height
directors_dict = {'name': [], 'height': []}

#3.Option tanımlama, driver'ı oluşturma, ana sayfayı driver ile açma
options = webdriver.ChromeOptions()
options.add_argument('--start-maximized') #Tarayıcımızın tam ekran modunda çalışmasını sağlayacak
options.add_experimental_option('detach',True) #Tarayıcımız kendi kendine kapanmayacak

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)
driver.implicitly_wait(5)
actions = ActionChains(driver)
driver.get('https://www.imdb.com/search/title/')

#4.Cookie tercihini kontrol et, belirirse kontrol et (VAR)
try:
    accept_button = driver.find_element(By.XPATH,'//button[text()="Accept"]') #button elementi içinde accept yazan
    accept_button.click()
except:
    pass

#5.Genre'dan drama kategorisi seçme ve Awards'dan 'Best Director-Winning'i seçme
#5.1 Genre
sleep(1)
genre = driver.find_element(By.XPATH,'//div[text()="Genre"]')
actions.move_to_element(genre).perform()
genre.click()

sleep(1)

drama_button = driver.find_element(By.CSS_SELECTOR,'button[data-testid="test-chip-id-Drama"]') #data-testid özelliğine göre seçme yaptık o yüzden etiket[özellik=karşılığı]
actions.move_to_element(drama_button).perform()
drama_button.click()

sleep(1)

#5.2 Awards
awards_button = driver.find_element(By.XPATH,'//div[text()="Awards & recognition"]')
actions.move_to_element(awards_button).perform()
awards_button.click()

sleep(1)

director_winning_button = driver.find_element(By.CSS_SELECTOR,'button[data-testid="test-chip-id-best-director-winning"]') #data-testid özelliğine göre seçme yaptık o yüzden etiket[özellik=karşılığı]
actions.move_to_element(director_winning_button).perform()
director_winning_button.click()

sleep(1)

#See results
results_button = driver.find_element(By.CSS_SELECTOR,'button[aria-label="See results"]') #button etiketinde arial label özelliği see result'a eşit olan
actions.move_to_element(results_button).perform()
results_button.click()



#6 More butonu döngüsü
#Sayfada butonu arıycaz, bulabilirsek tıklıycaz bulamazsak döngüyü bitiricez
while True:
    sleep(2)
    more_buttons= driver.find_elements(By.CSS_SELECTOR, 'ipc-see-more__text') #find elements ile arama yapınca hata mesajı çıkmıyor eğer bulamıyorsa boş liste döndürüyor.
    if len(more_buttons) != 0: #0 degilse uzunluğu 1'dir butonu bulmuştur (1 buton var)
        more_button = more_buttons[0] #icindeki tek elemanı atadık.
        actions.move_to_element(more_button).perform()
        more_button.click()
    else:
        break

#7 Filmlerin sağ tarafındaki info butonlarının (svg etiketini kullanın) listesini alın
# svg.ipc-icon--info
i_buttons = driver.find_elements(By.CSS_SELECTOR,'svg.ipc-icon--info')

#Bu info butonlarına tek tek tıklamak için bir loop oluşturucaz ve bunlardan yönetmenlerin linklerini alıp bir listeye koyucaz
directors_list = [] #boş bir yönetmen listesi
for i_button in i_buttons:                               ##i buttons içinde döngü oluştururuz
    actions.move_to_element(i_button).perform()          #tıklıyoruz hepsine
    i_button.click()
    sleep(0.5)
    a_tag= driver.find_element(By.CSS_SELECTOR,'a.iCQxDv') # a etiketinde sınıf ismi yönetmen adında bu etikete gittik ondan da href yani linkini çıkarıcaz.
    link = a_tag.get_attribute('href')
    directors_list.append(link) #yönetmen linkini listeye ekledik
    close_button = driver.find_element(By.CSS_SELECTOR,'button[aria-label="Close Prompt"]') #bir filmin bilgi ekranını kapatmak için ki diğerine de geçebilelim
    actions.move_to_element(close_button).perform()          #tıklıyoruz hepsine
    close_button.click()
    sleep(0.5)

#Başka bir loop ile tüm yönetmen linklerini ziyaret edicez, isimlerini ve boylarını(eğer sayfada varsa) başta oluşturduğumuz dictionary'e ekliycez
for link in directors_list:
    driver.get(link) #yönetmenin sayfasını açtık
    #data-testid="hero__pageTitle"
#Yönetmenin ismi
    try:
        name = driver.find_element(By.CSS_SELECTOR,'h1[data-testid="hero__pageTitle"] span[data-testid="hero__primary-text"]').text #h1'içinde spanin içindeydi özellikleri ile birlikte ulaştık
    except:
        name = 'Bilgi Yok'

#Yönetmenin boyu
    try:
        height = driver.find_element(By.XPATH,'//span["Height"]/following-sibling::div[1]/ul/li/span').text #Height yazısına göre arama yaptık(XPATHin özelliği bir de // koyulmalı) sonraki kardeşinden dive gittik ilk dive[1]. Sonra oradan ul'ye li'ye ve boy bilgisinin olduğu spana geldik ve içindeki text'i çıkardık
    except:
        height = 'Bilgi Yok'

    directors_dict['name'].append(name)
    print(name)
    directors_dict['height'].append(height)
    print(height)

#8.Excele çeviriyoruz
df = pd.DataFrame(directors_dict)
df.to_excel('boylar.xlsx')
