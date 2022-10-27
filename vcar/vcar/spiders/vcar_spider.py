import scrapy
from scrapy import Spider
from scrapy.selector import Selector
import json
from vcar.items import VcarItem
import requests


BASE_URL = "https://vnexpress.net/oto-xe-may/v-car/load-suggest-car/company_id/"

CARS = [
    {"value": 1, "name": "Aston Martin", "id": "1"},
    {"value": 2, "name": "Audi", "id": "2"},
    {"value": 3, "name": "Bentley", "id": "3"},
    {"value": 4, "name": "BMW", "id": "4"},
    {"value": 7, "name": "Ford", "id": "7"},
    {"value": 8, "name": "Honda", "id": "8"},
    {"value": 9, "name": "Hyundai", "id": "9"},
    {"value": 11, "name": "Isuzu", "id": "11"},
    {"value": 12, "name": "Jaguar", "id": "12"},
    {"value": 13, "name": "Jeep", "id": "13"},
    {"value": 14, "name": "Kia", "id": "14"},
    {"value": 16, "name": "Land Rover", "id": "16"},
    {"value": 17, "name": "Lexus", "id": "17"},
    {"value": 18, "name": "Maserati", "id": "18"},
    {"value": 19, "name": "Mazda", "id": "19"},
    {"value": 20, "name": "Mercedes", "id": "20"},
    {"value": 21, "name": "MG", "id": "21"},
    {"value": 22, "name": "Mini", "id": "22"},
    {"value": 23, "name": "Mitsubishi", "id": "23"},
    {"value": 24, "name": "Nissan", "id": "24"},
    {"value": 25, "name": "Peugeot", "id": "25"},
    {"value": 26, "name": "Porsche", "id": "26"},
    {"value": 27, "name": "Ram", "id": "27"},
    {"value": 30, "name": "Subaru", "id": "30"},
    {"value": 31, "name": "Suzuki", "id": "31"},
    {"value": 32, "name": "Toyota", "id": "32"},
    {"value": 33, "name": "VinFast", "id": "33"},
    {"value": 34, "name": "Volkswagen", "id": "34"},
    {"value": 35, "name": "Volvo", "id": "35"},
]


class VCarsSpider(scrapy.Spider):
    name = "vcar"
    allowed_domains = ['vnexpress.net']

    def start_requests(self):
        urls = [

        ]
        for i in CARS:
            urls.append(BASE_URL + str(i['value']))

        print(urls)

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        json_res = json.loads(response.body)
        tmp = json_res['data']
        keys = json_res['data'].keys()
        for i in keys:
            url_2 = 'https://vnexpress.net/microservice/get-data-car/car_id/' + str(tmp[i]['car_id'])
            yield scrapy.Request(
                str(url_2),
                meta={'car_id': tmp[i]['car_id']},
                callback=self.parse_chitiet_url)

    def parse_chitiet_url(self, response):
        json_res = json.loads(response.body)
        tmp = json_res['data']
        for i in tmp:
            datapost = 'version_ids='+str(i['version_id'])+'&new_version_id='+str(i['version_id'])+'&new_life_id=0&new_car_id='+str(response.meta['car_id'])
            # print(datapost)
            url_2 = 'https://vnexpress.net/oto-xe-may/v-car/add-new-car'
            yield scrapy.Request(
                str(url_2),
                method='POST',
                body=datapost,
                headers={'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                         'x-requested-with': 'XMLHttpRequest'
                         },
                meta={'version_id': i['version_id']},
                callback=self.parse_final)

    def parse_final(self, response):
        item = VcarItem()



        json_res = json.loads(response.body)

        url = "https://vnexpress.net/oto-xe-may/v-car/load-gallery/object_id/" + str(
            json_res['arrCompareData'][response.meta['version_id']]['car_id'])

        headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Cookie': 'device_env=4; device_env_real=4'
        }

        responseImage = requests.request("GET", url, headers=headers)

        json_res_image = json.loads(responseImage.text)


        # print(json_res)
        item['car_id'] = json_res['arrCompareData'][response.meta['version_id']]['car_id']
        item['company_id'] = json_res['arrCompareData'][response.meta['version_id']]['company_id']
        item['company_name']= json_res['arrCompareData'][response.meta['version_id']]['company_name']
        item['company_url'] = json_res['arrCompareData'][response.meta['version_id']]['company_url']
        item['full_name'] = json_res['arrCompareData'][response.meta['version_id']]['company_url']
        item['car_name'] = json_res['arrCompareData'][response.meta['version_id']]['car_name']
        item['segment_name'] = json_res['arrCompareData'][response.meta['version_id']]['segment_name']
        item['segment_company'] = json_res['arrCompareData'][response.meta['version_id']]['segment_company']
        item['version_id'] = str(json_res['arrCompareData'][response.meta['version_id']]['version_id'])
        item['price'] = json_res['arrCompareData'][response.meta['version_id']]['price']
        item['tskt_version'] = str(json_res['arrCompareData'][response.meta['version_id']]['tskt_version'])
        item['list_version'] = str(json_res['newCarDisplay']['list_version'])
        item['thumbnail_url'] = json_res['newCarDisplay']['thumbnail_url']
        item['arrImages'] = str(json_res_image['arrImages'])

        yield item




