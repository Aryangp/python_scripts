import pymongo
import requests


class connectMongo:
    def __init__(self,password,database,collection_to_use):
        self.__password=password
        self.__database=database
        self.__collection_to_use=collection_to_use

    def connect(self):
        client=pymongo.MongoClient(f'mongodb+srv://kiyotaka:{self.__password}@user.nzzo7.mongodb.net/?retryWrites=true&w=majority')
        db_name=self.__database
        collection_name=self.__collection_to_use
        db=client[collection_name]
        collection=db[db_name]
        return collection    


class generateEmbeding:
    def __init__(self,token):
        self.__token=token
        self.embeding_url="https://api-inference.huggingface.co/pipeline/feature-extraction/sentence-transformers/all-MiniLM-L6-v2"

    def get_embeding(self,text:str)->list[float]:
        response=requests.post(
            self.embeding_url,
            headers={
                "Authorization":f"Bearer {self.__token}"
            },
            json={
                "inputs":text
            }
        )

        if response.status_code!=200:
            raise Exception("Request failed with status code"+str(response.status_code))
        
        return response.json()
          

mongo=connectMongo('pikapika05','movies','sample_mflix')
collection=mongo.connect()

embed=generateEmbeding("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")

for doc in collection.find({'plot':{"$exists":True}}).limit(50):
    doc['plot_embeding_hf']=embed.get_embeding(doc['plot'])
    collection.replace_one({'_id':doc['_id']},doc)

#PlotSemanticSearch

query=input("Enter the query: ")
results=collection.aggregate([
    {"$vectorSearch":{
        "queryVector":embed.get_embeding(query),
        "path":"plot_embeding_hf",
        "numCandidates":100,
        "limit":4,
        "index":"PlotSemanticSearch"

    }}
])    

for doc in results:
    print(f"Movie: {doc['title']} ,\n Movie Plot: {doc['plot']}\n")

