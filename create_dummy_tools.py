"""Populate the database with tools from a literal in this file.

This is file is not currently used. To restore it, see the FIXMEs and TODOs in this file.
"""

import os

from pymongo import MongoClient

# TODO DRY w/ other references to os.environ.get('mongo_uri')
MONGO_URI = os.environ.get('mongo_uri', 'mongodb://localhost:27017/')

client = MongoClient(MONGO_URI)
# FIXME the database name below disagrees with the database in create_tools_from_tind
# TODO if the database is aligned, this code might should verify that it's not run against production
print("The database that this script creates isn't the one that the code uses.")
db = client.olinloanbot
tools = db.tools


# TODO DRY w/ class in create_tools_from_tind
class Tool(object):
    def __init__(self, name, collection, resource_link):
        self.name = name
        self.current_user = None
        self.current_due_date = None
        self.collection = collection
        self.resource_link = resource_link


tools_list = [
    Tool('screwdriver', 'tool wall', None),
    Tool('drill', 'tool wall', None),
    Tool('arduino', 'tool wall', 'https://www.arduino.cc/en/Main/Docs'),
    Tool('camera', 'media', 'https://vimeo.com/201067762'),
    Tool('tripod', 'media', 'https://vimeo.com/201067762'),
    Tool('lens', 'media', 'https://vimeo.com/201067762')]


def create_tools(tools_list):
    for tool in tools_list:
        tools.insert_one(tool.__dict__)


create_tools(tools_list)
