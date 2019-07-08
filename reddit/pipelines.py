# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem
from firebase import Firebase
from scrapy.utils.serialize import ScrapyJSONEncoder

config = {
    "apiKey": "AIzaSyBWNuamrgBXS90Kg3aZyu8hcutv4047j7g",
    "authDomain": "insult-generator-cf9af.firebaseapp.com",
    "databaseURL": "https://insult-generator-cf9af.firebaseio.com",
    "storageBucket": "insult-generator-cf9af.appspot.com",
}
firebase = Firebase(config)
db = firebase.database()

_encoder = ScrapyJSONEncoder()

class RedditPipeline(object):

    def process_item(self, item, spider):
        print(item)
        #db.child("insults").push(_encoder.encode(item))
