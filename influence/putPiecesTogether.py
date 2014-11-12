import sys, pickle, json

userContrib = open('userContrib.json', 'r')
quality = open('qualityProjects.r', 'r')
outfile = open('userMetrics.r', 'w')

quality_list = []
for line in quality:
  quality_list.append(line)

count = 0
contribCount = 0
qualityCount = 0
contributions = json.load(userContrib)
# print contributions['ariel.calzada@gmail.com']
for user in contributions:
  repos = contributions[user]
  contribCount = len(repos)
  for repo in repos:
    if repo in quality_list:
      qualityCount += 1
  outfile.write(user + ';' + str(contribCount) + ';' + str(qualityCount) + '\n')
  contribCount = 0
  qualityCount = 0
  if(count % 1000 == 0):
    print str(count)
  count += 1
  # print user
  # sys.exit()
# for line in userContrib:

  # splitline = line.split(';')
  # forks.append(int(splitline[2]))
  # if(int(splitline[2]) >= 4):
    # outfile.write(splitline[0] + '\n')
  # if(count % 1000 == 0):
    # print str(count)
  # if(int(splitline[2]) != 0):
    # break
  # count += 1
  # print splitline
  # sys.exit()

print 'Done collecting data'
# print forks
# forks.sort()
# forks.reverse()
# length = len(forks)

# pickle.dump(forks, open('forks.pickle', 'w'))

# top_percent = int(length / 200)
# print 'Threshold is: ', forks[top_percent]

# for i in range(len(forks)):
  # if(forks[i] == 0):
    # print str(i)
    # break
# print forks