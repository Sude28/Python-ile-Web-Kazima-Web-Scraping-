from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.ie.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains

url = 'https://quotes.toscrape.com/js'

options = webdriver.ChromeOptions()
options.add_argument('--start-maximized') #Tarayıcımızın tam ekran modunda çalışmasını sağlayacak
options.add_experimental_option('detach',True) #Tarayıcımız kendi kendine kapanmayacak

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

actions = ActionChains(driver)

driver.get(url)

#Elemanı seçtikten sonra tıklama kısmında bir hatayla karşılaşabiliriz işte o zaman kullanıcaz
next_button = driver.find_element(By.CSS_SELECTOR,'li.next a')
actions.move_to_element(next_button).perform()  #araya bunu ekliyoruz problem yaşarsak
next_button.click()