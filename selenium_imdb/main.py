from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.ie.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
import pandas as pd
import openpyxl

movie_dict = {
    'name' : [] ,
    'year' : [],
    'duration' : [],
    'stars': [],
    'votes':[],
    'metascore': [],
    'description':[]
}

def accept_cookies(the_driver):
    try:
        accept_cookies = the_driver.find_element(By.XPATH, '//button[text()="Accept"]') #Metine göre arama yaptığımızdan XPATH kullandık
        accept_cookies.click()
    except:
        pass



options = webdriver.ChromeOptions()
options.add_argument('--start-maximized') #Tarayıcımızın tam ekran modunda çalışmasını sağlayacak
options.add_experimental_option('detach',True) #Tarayıcımız kendi kendine kapanmayacak

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)
driver.implicitly_wait(5)
actions = ActionChains(driver)


driver.get('https://www.imdb.com/')

#Sayfayı açınca ilk yapacağımız çerez tercihlerini kabul etmek yani accept butonuna tıklamak
sleep(2)
#Cookie tercihleri çıkmazsa o yüzden buton yoksa hata döner bu nedenle try except butonu oluştururuz

accept_cookies(driver)

sleep(1)

#once arama butonuna tıklıyoruz sonra filmler,tv ve daha fazlası butonuna sonra çıkan filtre kısımlarından filmi komediyi ve oskar adayı olanları filtreliyoruz

search_button = driver.find_element(By.ID,'suggestion-search-button') #Id'si vardı direkt ona göre yaptık
search_button.click()

sleep(1)

movies_tv = driver.find_element(By.CSS_SELECTOR,'a[data-testid = "advanced-search-chip-tt"]')  #a elementi içinde data-testid attribute'ını kullanarak erişicez direkt ıd yok
movies_tv.click()

sleep(1)


#Bu kısımda 7 adet tıklama yapıcaz once tittle type'a tıklayıp ve movie seçicez sonra genre'ye tıklayıp comedie seçicez sonra awars'a tıklayıp oscar nominated seçicez ve en son see results diyicez
title_type = driver.find_element(By.XPATH,'//div[text() = "Title type"]')
title_type.click()

sleep(1)

movie = driver.find_element(By.CSS_SELECTOR, 'button[data-testid = "test-chip-id-movie"]')
driver.execute_script('arguments[0].click()',movie)
#movie.click()


sleep(1)

genre = driver.find_element(By.XPATH,'//div[text() = "Genre"]')
driver.execute_script('arguments[0].click()',genre)
genre.click()

sleep(1)

comedy = driver.find_element(By.CSS_SELECTOR, 'button[data-testid = "test-chip-id-Comedy"]')
driver.execute_script('arguments[0].click()',comedy)
#comedy.click()
sleep(1)

awards = driver.find_element(By.XPATH,'//div[text() = "Awards & recognition"]')
driver.execute_script('arguments[0].click()',awards)
#awards.click()

sleep(1)

oscar_nom = driver.find_element(By.CSS_SELECTOR, 'button[data-testid = "test-chip-id-oscar-nominated"]')
driver.execute_script('arguments[0].click()',oscar_nom)
#oscar_nom.click()

sleep(1)

results_button = driver.find_element(By.CSS_SELECTOR, 'button[data-testid = "adv-search-get-results"]')
driver.execute_script('arguments[0].click()',results_button)
#results_button.click()



#Bir sayfada 50 tane film geliyor diğer sayfaları yüklemek için aşağı kaydırıp 50 more butonuna tıklıycaz
#Elemanı bulamazsa hata değil boş liste döndürücek. Listenin uzunluğunu kontrol edicez eğer 1 ise butonu bulmuş demektir eğer 0 ise butonumuz artık sayfada yok bütün elemanlar yüklendi demek.

while True:
    sleep(2)
    more_buttons = driver.find_elements(By.CSS_SELECTOR,'span.ipc-see-more__text')
    if len(more_buttons) != 0:
        more_button = more_buttons[0]
        actions.move_to_element(more_button).perform()
        more_button.click()
    else:
        break


movies = driver.find_elements(By.CLASS_NAME, 'ipc-metadata-list-summary-item')                         #Bütün filmler li etiketinin içinde

for movie in movies:
    #1. Anora
    raw_name = movie.find_element(By.CSS_SELECTOR,'h3.ipc-title__text').text
    name =' '.join(raw_name.split(' ')[1:])   #sayıyı attık [1:] ile sonra iki kelimesli ise birleştirdik
    print(name)
    movie_dict['name'].append(name)

#hepsi span altında sınıf etiketi de aynı bu yüzden elements diyip sırayla alıcaz. yılını süresini
    year = movie.find_elements(By.CSS_SELECTOR, 'span.sc-f30335b4-7 jhjEEd dli-title-metadata-item')[0].text
    print(year)
    movie_dict['year'].append(year)

    duration = movie.find_elements(By.CSS_SELECTOR, 'span.sc-f30335b4-7 jhjEEd dli-title-metadata-item')[1].text
    print(duration)
    movie_dict['duration'].append(duration)

#yıldız
    stars = movie.find_element(By.CSS_SELECTOR,'span.ipc-rating-star--rating').text
    print(stars)
    movie_dict['stars'].append(stars)

#oyların sayısı span içinde sınıf var ama (160K) bu formatta sadece sayıyıy alıcaz
    votes = movie.find_element(By.CLASS_NAME,'ipc-rating-star--voteCount').text.strip()[1:-1] #strip baştaki ve sondaki boşlukları siliyor [1:-1] bu da baştaki ve sondaki parantezleri siliyor
    print(votes)
    movie_dict['votes'].append(votes)

#Metascore puanı ama bütün filmlerde bulunmuyor try except uyguluycaz o yüzden
    try:
        metascore = movie.find_element(By.CSS_SELECTOR,'span.metacritic-score-box').text   #class_Selector yapıp da direkt classs izsmi yazabilirdik span yazmadan iki türlü de olur

    except:
        metascore = 'Bilgi Yok'

    print(metascore)
    movie_dict['metascore'].append(metascore)

#Açıklama
    description = movie.find_element(By.CSS_SELECTOR,'div.ipc-html-content-inner-div').text
    print(description)
    movie_dict['description'].append(description)
    print('\n')

df = pd.DataFrame(movie_dict)
df.to_excel('filmler.xlsx')

