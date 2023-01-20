import json
import os
import time

import requests
from bs4 import BeautifulSoup
from selenium import webdriver


def descargar_img(image_url):
    img_data = requests.get(image_url).content
    with open('./exports/minuta.jpg', 'wb') as handler:
        handler.write(img_data)
    pass


def obtener_minuta(filename):
    website = "https://dgaeapucv.cl/casino/#casacentral"

    browser = webdriver.Chrome()
    browser.get(website)
    # time.sleep(5)
    html = browser.find_element('id', 'casacentral')

    html_txt = html.get_attribute('innerHTML')

    with open(filename, 'w') as f:
        f.write(html_txt)

    browser.quit()

    pass


def buscar_en_minuta(filename):
    
    with open(filename) as fp:
        soup = BeautifulSoup(fp, 'html.parser')
    
    title = soup.find("p").text
    img_url = soup.find("a", class_="et_pb_lightbox_image")['href']
    
    minuta = {
        "title": title,
        "img_url": img_url,
        "request_time": time.strftime("%m/%d/%Y, %H:%M:%S", time.localtime())
    }
    
    minuta_json = json.dumps(minuta, indent=4)
    
    print(title)
    print(img_url)
    
    descargar_img(img_url)
    
    with open('./exports/minuta.json', 'w') as f:
        f.write(minuta_json)
    pass

if __name__ == "__main__":
    
    if not os.path.exists('./exports'):
        os.makedirs('./exports')
        
    filename = "./exports/minuta.html"
    
    obtener_minuta(filename)
    buscar_en_minuta(filename)
