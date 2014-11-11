import pymongo
client = pymongo.MongoClient('da0.eecs.utk.edu')
db = client['bitbucket']
commits = db['commits']
cbu = db['ContribByUser']
unique_repos = {}
for doc in commits.find():
  print doc['url']
  for value in doc['values']:
    try:
      username = value['author']['user']['username']
      repo = value['repository']['full_name']
      # print username
      result = cbu.find_one({'username': username})
      if result is None:
        temp = {'username': username, 'repos': [repo]}
        cbu.insert(temp)
      else:
        if repo not in result['repos']:
          result['repos'].append(repo)
          cbu.update({'_id': result['_id']}, {'$set': result})
        else:
          print 'Repo already present'
    except:
      # print 'No username for commit'
