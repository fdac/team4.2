
import pymongo
from bson import json_util

client = pymongo.MongoClient('localhost')
# client = pymongo.MongoClient('da0.eecs.utk.edu')

bitbucket = client['bitbucket']
contribByUser = bitbucket['ContribByUser']
forks = bitbucket['forks']

for user in contribByUser.find():
  
  repos = user['repos']
  for repo in repos:

    repoUrl = 'https://api.bitbucket.org/2.0/repositories/' + repo + '/forks'
    forkDoc = forks.find_one( { 'url' : repoUrl } )
    forkJson = json_util.dump( forkDoc, sort_keys=False, indent=2, separators=( ',', ':' ) )
    print forkJson

  break
