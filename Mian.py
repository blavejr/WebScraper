from bs4 import BeautifulSoup
import requests
from urllib import urlretrieve
import os

class Cars:
    def __init__(self, keywords, year):
        self.max_pages = 5
        self.search_words = keywords
        self.year = year
        full__url = "https://www.namcars.net/search.html?change_currency_select=NAD&year="+str(self.year)+"&start_price=&transmission=&keywords="+self.search_words


    def carSpider(self):
        page = 0
        while page <= self.max_pages:
            full_url = "https://www.namcars.net/search.html?&action=search&keywords="+self.search_words+"&page=" + str(page)
            source_code = requests.get(full_url)
            plain_text = source_code.text
            soupOB = BeautifulSoup(plain_text, "html.parser")

            for hidenlink in soupOB.findAll('span', {'class':"hidelink"}):
                link_extention = hidenlink['class'][1]
                self.get_info(link_extention)

    def get_info(self, link_ext):
            ext_full_url = "https://www.namcars.net" + link_ext
            new_source = requests.get(ext_full_url)
            new_source_txt = new_source.text
            new_source_OB = BeautifulSoup(new_source_txt, "html.parser")

            for short_desc in new_source_OB.findAll('div', {'class':'pathBar'}):
                desc = short_desc.strong.text

                for piclink in new_source_OB.findAll('div', {'id':'main-img'}):
                    image_ext = piclink.a.get('href')
                    full_image_link = "https://www.namcars.net" + image_ext

                    for price_code in new_source_OB.findAll('span', {'id':'price_chng'}):
                        price = price_code.text
                        break


            print desc + " " + price + "\n" + full_image_link
            try:
                    os.makedirs("pics\\"+desc+"\\"+price)
                    urlretrieve(full_image_link, "pics\\"+desc+"\\"+price+"\\"+image_ext[7::])
            except OSError as e:
                print e
                urlretrieve(full_image_link, "pics\\"+desc+"\\"+price+"\\"+image_ext[7::])




d = Cars("polo", 2006)
d.carSpider()