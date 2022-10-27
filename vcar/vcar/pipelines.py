# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import sqlite3
import pyodbc
import uuid

class VcarPipeline:
    def __init__(self):
        self.conn = pyodbc.connect('Driver={SQL Server};'
                                   'Server=10.10.10.50,1469;'
                                   'Database=TD_DATAAPP_Application;'
                                   'UID=tdcongdan;'
                                   'PWD=Tandan@123;'
                                   'Trusted_Connection=no;')
        self.cursor = self.conn.cursor()
    def process_item(self, item, spider):
        self.cur.execute("select * from Catalog.Car where car_id = ?", (item['car_id'],))
        result = self.cur.fetchone()

        if result:
            spider.logger.warn("Item already in database: %s" % item['url'])
        else:
            ## Define insert statement
            self.cur.execute("""
                INSERT INTO Catalog.Car (Id, car_id, company_id, company_name, company_url, full_name, car_name, segment_name, segment_company,version_id,price,tskt_version,list_version,thumbnail_url,arrImages) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            """,
                             (
                                 str(uuid.uuid4()),
                                 item['car_id'],
                                 item['company_id'],
                                 item['company_name'],
                                 item['company_url'],
                                 item['full_name'],
                                 item['car_name'],
                                 item['segment_name'],
                                 item['segment_company'],
                                 item['version_id'],
                                 item['price'],
                                 item['tskt_version'],
                                 item['list_version'],
                                 item['thumbnail_url'],
                                 item['arrImages']
                             ))

            ## Execute insert of data into database
            self.con.commit()
        return item
