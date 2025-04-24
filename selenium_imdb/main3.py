
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.ie.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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
actions = ActionChains(driver)
driver.implicitly_wait(5)

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

try:
    # Öğenin görünür olmasını bekle
    title_type = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//input[@id='title_type-1']"))
    )

    # Önce kaydır, sonra JavaScript ile tıkla
    driver.execute_script("arguments[0].scrollIntoView(true);", title_type)
    driver.execute_script("arguments[0].click();", title_type)

except Exception as e:
    print("Title Type kutusuna tıklanamadı:", e)



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

