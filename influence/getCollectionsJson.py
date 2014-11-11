
# ssh -L27017:da0.eecs.utk.edu:27017 -p 2200 -fN jwill221@da2.eecs.utk.edu

import pymongo
# import json
from bson import json_util


def getJson( database , collectionName ):
  collection = database[ collectionName ]
  fileName = 'json/' + collectionName + '.json'
  with open(fileName, 'w') as fileObj:
    documentBson = collection.find_one( {} )
    # https://stackoverflow.com/questions/4404742/how-do-i-turn-mongodb-query-into-a-json
    documentJson = json_util.dumps( documentBson , sort_keys=True , indent=4 , default=json_util.default )
    fileObj.write( documentJson )


# Local computer connection using the following ssh command
# ssh -L27017:da0.eecs.utk.edu:27017 -p 2200 -fN jwill221@da2.eecs.utk.edu
client = pymongo.MongoClient('localhost')

# UTK computer connection via da2.eecs.utk.edu 
# client = pymongo.MongoClient('da0.eecs.utk.edu')

bitbucketDb = client['bitbucket'] # BitBucket database

collectionNames = bitbucketDb.collection_names()
print 'Collections: ' + str(collectionNames)

for collectionName in collectionNames:
  print 'Collection name: ' + collectionName
  getJson( bitbucketDb, collectionName )



