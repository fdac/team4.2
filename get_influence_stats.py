import pymongo

client = pymongo.MongoClient('localhost')
db = client['bitbucket']

commits = db['commits']
ta = client['team-awesome']
cbu = ta['ContribByUser']

# count = 1;
unique_repos = {}

for doc in commits.find():
	# print str(doc)
	print doc['url']
	for value in doc['values']:
		try:
			username = value['author']['user']['username']
			repo = value['repository']['full_name']
			print username
			result = cbu.find_one({'username': username})
			if result is None:
				temp = {'username': username, 'repos': [repo]}
				cbu.insert(temp)
			else:
				result['repos'].append(repo)
			# if username in unique_repos:
			# 	if repo not in unique_repos[username]:
			# 		unique_repos[username].append(repo)
			# else:
				# unique_repos[username] = []
				# unique_repos[username].append(repo)
				
		# except:
			print 'No username for commit'
		# print value['author']
	# count += 1
	# if(count == 100):
		# break

# outfile.open('user_repo_contribution.csv', 'w')
# for user in unique_repos