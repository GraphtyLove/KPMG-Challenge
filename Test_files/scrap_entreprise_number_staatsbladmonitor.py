import scrapy
import json
import re


# Scrap the number of all society
class BlogSpider(scrapy.Spider):
    name = 'DE STAATSBLADMONITOR'
    start_urls = []
    data_final = []
    year = 2018

    for month in range(1, 13):
        if month < 10:
            month = f'0{month}'
        for day in range(1, 32):
            if day < 10:
                day = f'0{day}'
            start_urls.append(f'https://www.staatsbladmonitor.be/oprichtingen-bedrijven.html?datum={year}-{month}-{day}')

    def parse(self, response):

        for data in response.css('.data::text'):
            if re.match('^[0-9]+$', data.get()):
                self.data_final.append('https://www.staatsbladmonitor.be/bedrijfsfiche.html?ondernemingsnummer=' + data.get())

        with open('../assets/link_each_entreprise_2018.json', 'w', encoding='utf-8') as f:
            json.dump(self.data_final, f, ensure_ascii=False, indent=4)
