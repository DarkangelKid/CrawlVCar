# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import sqlite3


class VcarPipeline:
    def __init__(self):
        ## Create/Connect to database
        self.con = sqlite3.connect('demo.db')

        ## Create cursor, used to execute commands
        self.cur = self.con.cursor()

        ## Create quotes table if none exists
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS Car(
            id INTEGER NOT NULL UNIQUE,
            car_id	TEXT,
	        company_id TEXT,
	        company_name	TEXT,
	        company_url	TEXT,
	        full_name	TEXT,
	        car_name	TEXT,
	        segment_name	TEXT,
	        segment_company	TEXT,
	        version_id	TEXT,
	        price	TEXT,
	        tskt_version	TEXT,
	        list_version	TEXT,
	        thumbnail_url	TEXT,
	        arrImages TEXT,
            PRIMARY KEY("id" AUTOINCREMENT)
        )
        """)
    def process_item(self, item, spider):
        self.cur.execute("select * from Car where car_id = ?", (item['car_id'],))
        result = self.cur.fetchone()

        if result:
            spider.logger.warn("Item already in database: %s" % item['url'])
        else:
            ## Define insert statement
            self.cur.execute("""
                INSERT INTO Car (car_id, company_id, company_name, company_url, full_name, car_name, segment_name, segment_company,version_id,price,tskt_version,list_version,thumbnail_url,arrImages) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            """,
                             (
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
