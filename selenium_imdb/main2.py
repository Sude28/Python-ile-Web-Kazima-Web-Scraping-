from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

def accept_cookies(the_driver):
    try:
        accept_cookies_btn = WebDriverWait(the_driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, '//button[text()="Accept"]'))
        )
        accept_cookies_btn.click()
    except:
        pass

options = webdriver.ChromeOptions()
options.add_argument('--start-maximized')
options.add_experimental_option('detach', True)

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)
driver.implicitly_wait(5)

driver.get('https://www.imdb.com')

sleep(2)
accept_cookies(driver)
sleep(1)

# Arama butonuna tıklıyoruz
search_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.ID, 'suggestion-search-button'))
)
search_button.click()
sleep(2)

# "Movies, TV & More" seçeneğine tıklıyoruz
movies_tv = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[data-testid="advanced-search-chip-tt"]'))
)
movies_tv.click()
sleep(2)

### **Burada sayfayı aşağı kaydırarak filtrelerin düzgün yüklenmesini sağlıyoruz**
driver.execute_script("window.scrollBy(0, 500);")  # 500 piksel aşağı kaydır
sleep(10)

# "Title type" menüsüne tıklıyoruz
title_type = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '//div[text()="Title type"]'))
)
driver.execute_script("arguments[0].click();", title_type)
sleep(2)

# "Movie" seçeneğini seçiyoruz
movie = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '//span[text()="Movie"]/ancestor::button'))
)
driver.execute_script("arguments[0].click();", movie)
sleep(2)

# Sayfayı tekrar kaydırıyoruz
driver.execute_script("window.scrollBy(0, 500);")

# "Genre" menüsüne tıklıyoruz
genre = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '//div[text()="Genre"]'))
)
driver.execute_script("arguments[0].click();", genre)
sleep(2)

# "Comedy" seçeneğini seçiyoruz
comedy = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-testid="test-chip-id-Comedy"]'))
)
driver.execute_script("arguments[0].click();", comedy)
sleep(2)

# Sayfayı tekrar kaydırıyoruz
driver.execute_script("window.scrollBy(0, 500);")

# "Awards & recognition" menüsüne tıklıyoruz
awards = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '//div[text()="Awards & recognition"]'))
)
driver.execute_script("arguments[0].click();", awards)
sleep(2)

# "Oscar Nominated" seçeneğini seçiyoruz
oscar_nom = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-testid="test-chip-id-oscar-nominated"]'))
)
driver.execute_script("arguments[0].click();", oscar_nom)
sleep(2)

# Sayfayı tekrar kaydırıyoruz
driver.execute_script("window.scrollBy(0, 500);")

# "See Results" butonuna tıklıyoruz
results_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-testid="adv-search-get-results"]'))
)
driver.execute_script("arguments[0].click();", results_button)

print("Filtreleme başarıyla tamamlandı!")
