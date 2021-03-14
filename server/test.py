from PIL import Image
from datauri import DataURI
import os
from pymongo import MongoClient

client = MongoClient("mongodb://127.0.0.1", 27017)
db = client.cartoon

def run():
    result = list(db.gallery.find({"id": "cho1234"}).sort([("date", -1)]))
    result_arr = []
    for image in result:
        private = {
            "id": image["id"],
            "imageId": image["imageId"],
            "filter": image["filter"],
            "date": str(image["date"]),
            "isPublic": image["isPublic"],
            "like": image["like"],
        }
        result_arr.append(private)

    print(result_arr)


if __name__ == "__main__":
    run()