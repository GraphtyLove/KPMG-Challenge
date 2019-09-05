import scrapy
import json
import re


class BlogSpider(scrapy.Spider):
    name = 'DE STAATSBLADMONITOR '

    start_urls = []
    year = 2019

    for month in range(1, 12):
        if month < 10:
            month = f'0{month}'
        for day in range(1, 31):
            if day < 10:
                day = f'0{day}'
            start_urls.append(f'https://www.staatsbladmonitor.be/oprichtingen-bedrijven.html?datum={year}-{month}-{day}')

    data_final = []
    data_final_clean = []

    def parse(self, response):
        for data in response.css('.data::text'):
            if re.match('^[0-9]+$', data.get()):
                self.data_final.append('https://www.staatsbladmonitor.be/bedrijfsfiche.html?ondernemingsnummer='+data.get())

        with open('link_each_entreprise.json', 'w', encoding='utf-8') as f:
            json.dump(self.data_final, f, ensure_ascii=False, indent=4)
