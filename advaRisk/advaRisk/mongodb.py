import pymongo


class MongoDB():
    """
        This class will perform different operations on the 
        MongoDB database
    """

    def __init__(self):
        """
            we initiate dbname, collection name and 
            a connection url
        """
        self.url = 'mongodb://localhost:27017'
        self.dbname = 'companiesincorp'
        self.collectionName = 'companiesinfo'
        # self.url = 'mongodb+srv://venunallapu:venunallapu@cluster0.33ocfmv.mongodb.net/?retryWrites=true&w=majority'

    def find_many_from_mongo(self):
        """
            This method will pick all details of company and return list to fastAPI UI
        """
        client = pymongo.MongoClient(self.url)
        db = client[self.dbname]
        collection = db[self.collectionName]
        result = list(collection.find({}, {'_id': 0}))
        client.close()
        return result

    def delete_many_from_mongo(self):
        """
            This method will delete all the data from MongoDB
        """
        client = pymongo.MongoClient(self.url)
        db = client[self.dbname]
        collection = db[self.collectionName]
        collection.delete_many({})
        client.close()
        return True

    def find_one_from_Mongo(self, cin: int):
        """
            This method will filter MongoDB and retrieves
            matched data
        """
        client = pymongo.MongoClient(self.url)
        db = client[self.dbname]
        collection = db[self.collectionName]
        result = list(collection.find({'cin': cin}, {'_id': 0}))
        client.close()
        return result

    def find_from_mongo_by_name(self, name: str):
        """
            This method will filter MongoDB based on company name and retrieves
            matched data
        """
        client = pymongo.MongoClient(self.url)
        db = client[self.dbname]
        collection = db[self.collectionName]
        result = list(collection.find({'cname': name}, {'_id': 0}))
        client.close()
        return result

    def find_from_mongo_by_status(self, status: str):
        """
            This method will filter MongoDB based on company working status and retrieves
            matched data
        """
        client = pymongo.MongoClient(self.url)
        db = client[self.dbname]
        collection = db[self.collectionName]
        result = list(collection.find({'status': status}, {'_id': 0}))
        client.close()
        return result

    def find_from_mongo_by_city(self, city_name: str):
        """
            This method will filter MongoDB based on company located city and retrieves
            matched data
        """
        client = pymongo.MongoClient(self.url)
        db = client[self.dbname]
        collection = db[self.collectionName]
        result = list(collection.find(
            {'company_address.city': city_name}, {'_id': 0}))
        client.close()
        return result

    def find_from_mongo_by_query(self, query):
        """
            This method will filter MongoDB based on company name and retrieves
            matched data
            Here we need to provide input as in python-mongodb stndard form
        """
        client = pymongo.MongoClient(self.url)
        db = client[self.dbname]
        collection = db[self.collectionName]
        result = list(collection.find(query, {'_id': 0}))
        client.close()
        return result


if __name__ == "__main__":
    instnc = MongoDB()
    instnc.delete_many_from_mongo()
