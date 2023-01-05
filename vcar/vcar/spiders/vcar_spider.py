import scrapy
from scrapy import Spider
from scrapy.selector import Selector
import json
from vcar.items import VcarItem
import requests

BASE_URL = "https://vnexpress.net/oto-xe-may/v-car/load-suggest-car/company_id/0"


class VCarsSpider(scrapy.Spider):
    name = "vcar"
    allowed_domains = ['vnexpress.net']

    def start_requests(self):
        urls = [
            "https://vnexpress.net/oto-xe-may/v-car/load-suggest-car/company_id/0"
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        json_res = json.loads(response.body)
        tmp = json_res['data']
        keys = json_res['data'].keys()
        for i in keys:
            url_2 = 'https://vnexpress.net/oto-xe-may/v-car/get-data-car?life_id=' + str(tmp[i]['life_id'])
            yield scrapy.Request(
                str(url_2),
                meta={'life_id': tmp[i]['life_id']},
                callback=self.parse_chitiet_url)

    def parse_chitiet_url(self, response):
        json_res = json.loads(response.body)
        tmp = json_res['data']
        for i in tmp:
            datapost = 'version_ids=' + str(i['version_id']) + '&new_life_id=0'
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
        item['company_name'] = json_res['arrCompareData'][response.meta['version_id']]['company_name']
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

        # yield item
