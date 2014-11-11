
import pymongo
from bson import json_util

# client = pymongo.MongoClient('localhost')
client = pymongo.MongoClient('da0.eecs.utk.edu')

bitbucket = client['bitbucket']
forks = bitbucket['forks']
repoForkCount = bitbucket['repoForkCount']

for fork in forks.find():

  forkUrl = fork['url']
  repoName = forkUrl.replace('https://api.bitbucket.org/2.0/repositories/', '').replace('/forks', '')
  forkCount = len( fork['values'] )

  result = repoForkCount.find_one( { 'repoName' : repoName } )
  if result == None:
    repoDoc = { 'repoName' : repoName, 'count' : forkCount }
    repoForkCount.insert( repoDoc )
    # print 'Inserting ' + repoName + ' with ' + forkCount + ' forks'
  else:
    repoDoc = result
    repoDoc['count'] += forkCount
    repoForkCount.update( {'_id' : result['_id'] }, { '$set' : repoDoc } )
    # print 'Updating ' + repoName + ' with ' + forkCount + ' forks'

