
# Helpful pymongo documentation
# http://api.mongodb.org/python/current/index.html

import pymongo, json, re

client = pymongo.MongoClient('localhost')

# Print the name of the databases
databases = client.database_names()
print 'Databases: ' + str(databases)

# Get the BitBucket database
db = client['bitbucket']

# Print the names of the BitBucket collections
collections = db.collection_names()
print 'Collections: ' + str(collections)

repos = db['repos']

# Print one repo from the repo collection
repo = repos.find_one( {} )
print 'Repo: ' + str(repo)


# Create a database
db = client['team-awesome']

# Create a collection in the new database
members = db['members']

# A member
spongebob = { 'name' : 'SpongeBob SquarePants', 'awesomenessLevel' : 9 }

# Add the member to the members collection
members.insert(spongebob)

# A list of members
awesomePeeps = [ { 'name' : 'Jerry Mouse', 'awesomenessLevel' : 10 } ,
  { 'name' : 'Arnold', 'awesomenessLevel' : 6 } ]

# Add members to the members collection
members.insert(awesomePeeps)

# Print the members of Team Awesome
for member in members.find():
  print str(member)

# for member in members.find( { 'awesomenessLevel' : { '$gt' : 9 } } )
#   print str(member)

# Remove all members
# members.remove()
