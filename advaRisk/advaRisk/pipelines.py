# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
import pymongo


class MongoAdvariskPipeline:
    def __init__(self):
        """
            we initiate dbname, collection name and 
            a set for tracking duplicates
        """
        self.dbname = 'companiesincorp'
        self.collectionName = 'companiesinfo'
        self.companies_seen = set()

    def open_spider(self, spider):
        """
            This method start executing even before the scrapy main method
            and here we initiate the dbname,collection and connection with MongoDB
        """
        self.client = pymongo.MongoClient('mongodb://localhost:27017')
        self.db = self.client[self.dbname]
        self.collection = self.db[self.collectionName]

    def process_item(self, item, spider):
        """
            This method will push data into DB and returns output to scrapy console and
            Duplicates will be checked here.
            NOTE: in order to work with Pipeline we need to 
            go into pipelines.py and change ITEM_PIPELINES to this format
            projectname:pipelines:classname : Integer
            lower interger get high preference
        """
        if item['cin'] in self.companies_seen:
            raise DropItem(f"Duplicates Detected: {item}")
        else:
            self.companies_seen.add(item["cname"])
            self.collection.insert_one(item)
        return item

    def close_spider(self, spider):
        """
            This method will close connection after complete insertion of data
        """
        self.client.close()


class MongoOps:
    """
            This Class perform accessing data from MongoDB after data got inserted
    """

    def __init__(self):
        self.url = 'mongodb://localhost:27017'
        self.dbname = 'companiesincorp'
        self.collectionName = 'companiesinfo'

    def fetch(self):
        with open('input.json', 'r') as f:
            query = (f.read())
        if not query:
            query='{}'
        self.client = pymongo.MongoClient(self.url)
        db = self.client[self.dbname]
        collection = db[self.collectionName]
        result = list(collection.find(eval(query), {'_id': 0}))
        return result


if __name__ == "__main__":
    mongoInsta = MongoOps()
    """
        if we want to access inserted data from mongodb
        we need to execute this script using python filename.py
    """
    result = mongoInsta.fetch()
    print(result)
