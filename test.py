import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.chrome.service import Service  # <-- bunu ekle


def test_url():
    URL = 'https://www.skyscanner.net/transport/flights/ista/esb/250915/?adultsv2=1&cabinclass=economy'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9'
    }
    try:
        response = requests.get(URL, headers = headers)
        if response.status_code == 200: 
            print("url is working...")
            print(f"Status Code: {response.status_code}")

            with open('skyscanner_page.html', 'w', encoding= 'utf-8') as f:
                f.write(response.text)
            print("HTML is saved to the 'skyscanner_page' file.")

            soup = BeautifulSoup(response.text, 'html.parser')
            flight_cards = soup.find_all('div', class_ = 'FlightsTicket_container__NjliO')
            
            if flight_cards:
                print(f"{len(flight_cards)} flight cards have been found!")
                for i, card in enumerate(flight_cards[:2]):
                    print(f"flight card {i+1}: {card.text[:100]}")
            
            else:
                print("flight card cannot be found. file can need to download javascipt.")

        else:
            print(f"error code: {response.status_code}")
    except Exception as e:
        print(f"error detected: {e}")


def test_url_selenium():
    URL = 'https://www.skyscanner.net/transport/flights/ista/esb/250915/?adultsv2=1&cabinclass=economy'
    options = Options()
    options.headless = True

    # Service objesi ile chromedriver yolunu belirt
    service = Service('/Users/kaancakir/Library/CloudStorage/OneDrive-Kişisel/data/projects/flight-elt-pipeline/chromedriver')
    driver = None  # driver'ı başta tanımla
    try:
        driver = webdriver.Chrome(service=service, options=options)
        print("Sayfa yükleniyor...")
        driver.get(URL)
        time.sleep(5)
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # HTML kaydet
        with open('skyscanner_page_selenium.html', 'w', encoding='utf-8') as f:
            f.write(soup.prettify())
        print("HTML 'skyscanner_page_selenium.html' dosyasına kaydedildi.")

        # Uçuş kartlarını kontrol et
        flight_cards = soup.find_all('div', class_='FlightsTicket_container__NjliO')
        if flight_cards:
            print(f"{len(flight_cards)} uçuş kartı bulundu!")
            for i, card in enumerate(flight_cards[:2]):
                print(f"Uçuş Kartı {i+1}: {card.text[:100]}...")
        else:
            print("Uçuş kartı bulunamadı. Class ismi yanlış olabilir.")
    except Exception as e:
        print(f"Hata oluştu: {e}")
    finally:
        if driver:  # driver tanımlıysa kapat
            driver.quit()

test_url_selenium()