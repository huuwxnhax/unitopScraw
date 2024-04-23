# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
import pymongo
import json
from bson.objectid import ObjectId
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
import csv

class MongoDBUnitopPipeline:
    def __init__(self):  
        self.client = pymongo.MongoClient('mongodb+srv://huunha21032k2:ZaagIYgcBPBDbloZ@data.uqcywhk.mongodb.net/?retryWrites=true&w=majority&appName=data')
        self.db = self.client['lawnet']
        pass
    
    def process_item(self, item, spider):
        collection =self.db['dbunitop']
        try:
            collection.insert_one(dict(item))
            return item
        except Exception as e:
            raise DropItem(f"Error inserting item: {e}")
        pass

class JsonDBUnitopPipeline:
    def process_item(self, item, spider):
        self.file = open('jsondataunitop.json','a',encoding='utf-8')
        line = json.dumps(dict(item), ensure_ascii=False) + '\n'
        self.file.write(line)
        self.file.close
        return item


import mysql.connector
class MySQLUnitopPipeline:
    # Tham khảo: https://scrapeops.io/python-scrapy-playbook/scrapy-save-data-mysql/
    def __init__(self):
        self.conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='**********',
            database='unitop'
        )

        ## Create cursor, used to execute commands
        self.cur = self.conn.cursor()
        
        ## Create course table if none exists
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS course (
                id INT AUTO_INCREMENT PRIMARY KEY,
                coursename VARCHAR(255),
                lecturer VARCHAR(255),
                intro TEXT,
                describe TEXT,
                courseUrl VARCHAR(255),
                votenumber TEXT,
                rating FLOAT,
                oldfee FLOAT,
                newfee FLOAT,
                lessonnum TEXT
            )
        """)

    def process_item(self, item, spider):

        ## Define insert statement
        self.cur.execute(""" 
            INSERT INTO course 
            (coursename, lecturer, intro, describe, courseUrl, votenumber, rating, oldfee, newfee, lessonnum) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            item['coursename'],
            item['lecturer'],
            item['intro'],
            item['describe'],
            item['courseUrl'],
            item['votenumber'],
            item['rating'],
            item['oldfee'],
            item['newfee'],
            item['lessonnum']
        ))

        ## Execute insert of data into database
        self.conn.commit()

        return item

    def close_spider(self, spider):
        ## Close cursor & connection to database 
        self.cur.close()
        self.conn.close()



class CSVDBUnitopPipeline:
    '''
    Viết code để xuất ra file csv, thông tin item trên dòng
    mỗi thông tin cách nhau với dấu $
    Ví dụ: coursename$lecturer$intro$describe$courseUrl
    Sau đó, cài đặt cấu định để ưu tiên Pipline này đầu tiên
    '''
    def process_item(self, item, spider):
        with open('csvdataunitop.csv', 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file, delimiter='$')
            # Write header if the file is empty
            if file.tell() == 0:
                writer.writerow(item.keys())
            writer.writerow(item.values())
        return item