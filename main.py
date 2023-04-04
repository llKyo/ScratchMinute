import json
import os
import time
import requests

from datetime import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from PIL import Image

def abrir_img(r_img):
    
    image = Image.open(r_img)
    image.show()
    pass

def descargar_img(r_html, r_img):
    img_data = requests.get(r_html).content
    with open(r_img, 'wb') as handler:
        handler.write(img_data)
    pass


def obtener_minuta(r_html):
    website = "https://dgaeapucv.cl/casino/#casacentral"

    browser = webdriver.Chrome()
    browser.get(website)
    # time.sleep(5)
    html = browser.find_element('id', 'casacentral')

    html_txt = html.get_attribute('innerHTML')

    with open(r_html, 'w') as f:
        f.write(html_txt)

    browser.quit()

    pass


def buscar_en_minuta(r_html, r_img, r_json):
    
    with open(r_html) as fp:
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
    
    descargar_img(img_url, r_img)
    
    with open(r_json, 'w') as f:
        f.write(minuta_json)
    pass

if __name__ == "__main__":
    
    r_root = "./exports/"
    
    if not os.path.exists(r_root):
        os.makedirs(r_root)
        
    now = datetime.now()
    now_format = now.strftime("%Y%d%m_%H%M%S/")

    r_main = r_root + now_format
    
    if not os.path.exists(r_main):
        os.makedirs(r_main)
    
    r_html = r_main + "minuta.html"
    r_img  = r_main + "minuta.jpg"
    r_json = r_main + "minuta.json"
    
    obtener_minuta(r_html)
    buscar_en_minuta(r_html, r_img, r_json)
    abrir_img(r_img)
