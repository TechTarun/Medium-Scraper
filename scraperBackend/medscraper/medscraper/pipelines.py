# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import mysql.connector

class MedscraperPipeline:
    def __init__(self):
        self.create_connection()
        self.create_table()

    def create_connection(self):
        self.conn = mysql.connector.connect(
            host = "mediumdb.cqe2pu5mx78b.ap-south-1.rds.amazonaws.com",
            user = "admin",
            passwd = "medium_admin",
            database = "mediumdb"
        )
        self.cursor = self.conn.cursor()

    def create_table(self):
        self.cursor.execute("DROP TABLE IF EXISTS medium_blogs")
        self.cursor.execute("""
            CREATE TABLE medium_blogs(
                title TEXT,
                author TEXT,
                responses TEXT,
                link TEXT
            )
        """)
        print("New table created")

    def process_item(self, item, spider):
        self.cursor.execute("INSERT INTO medium_blogs VALUES (%s, %s, %s, %s)", (item["title"][0], item["author"][0], item["responses"][0], item["link"][0]))
        self.conn.commit()
        print("=======================Item=============================")
        # print(item["title"], item["author"], item["responses"], item["link"])
        return item
