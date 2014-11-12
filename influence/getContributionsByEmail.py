import sys, pickle, json

contributions = {}

infile = open('/home/audris/measures.out', 'r')

count = 0
for line in infile:
  splitline = line.split(';')
  authors = splitline[4].split(':')
  repo = splitline[0]
  for author in authors:
    if author != '':
      if author in contributions:
        contributions[author].append(repo)
      else:
        contributions[author] = [repo]
  # forks.append(int(splitline[2]))
  if(count == 10):
    break
  if(count % 1000 == 0):
    print str(count)
  # if(int(splitline[2]) != 0):
    # break
  count += 1
  # print splitline
  # sys.exit()

print 'Done collecting data'
outfile = open('userContrib.json', 'w')
json.dump(contributions, outfile)
