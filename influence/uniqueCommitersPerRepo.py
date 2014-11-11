
# 
import pymongo

client = pymongo.MongoClient('localhost')
bitbucketDb = client['bitbucket']

repos = bitbucketDb['repos']
commits = bitbucketDb['commits']

# for commit in commits.find():

  # print 'Commit URL: ' + commit['url']
  # print '# values: ' + str( len( commit['values'] ) )
  # if len( commit['values'] ) > 1000:
  #   print commit
  #   break

# for repo in repos.find():

#   repoName = repo['full_name']
#   print 'Repo: ' + repoName

#   commitsUrl = repo['links']['commits']['href']
#   print 'Commits URL: ' + commitsUrl

#   print '# commits: ' + commits.find( { "url" : commitsUrl } ).count( )

#   for commit in commits.find( { "url" : commitsUrl } ):
#     print 'Found commit'


count = 0
for commit in commits.find( { "url": "https://api.bitbucket.org/2.0/repositories/vetler/fhtmlmps/commits" } ):

  print commit
  count += 1

print count


