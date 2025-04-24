from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.ie.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep


url = 'https://quotes.toscrape.com/scroll'

options = webdriver.ChromeOptions()
options.add_argument('--start-maximized') #Tarayıcımızın tam ekran modunda çalışmasını sağlayacak
options.add_experimental_option('detach',True) #Tarayıcımız kendi kendine kapanmayacak

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

driver.get(url)

sleep(2)

def scroll_to_bottom():
    driver.execute_script('window.scrollTo(0,document.body.scrollHeight);')
    sleep(1)

old_height = driver.execute_script('return document.body.scrollHeight')  #sayfanın uzunluğunu buluyor. İlk basta ilk uzunluk

while True:
    scroll_to_bottom() #asagı kaydırıyoe
    new_height = driver.execute_script('return document.body.scrollHeight') #aşağı kaydırdık sayfanın uzunlugu degisti o yüzden yeni uzunlugunu degiskenin icinde sakladık
    if new_height == old_height: #Birbirlerine esitse son yaptıgımız kaydırma olmadı yani esitler yani sonuna geldik demek
        break
    old_height = new_height #eski deger simdiki degeri aldı