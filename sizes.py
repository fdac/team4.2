def clean(str):
  return str.replace('\n', '')

repos = []
numRepos = 0

f = open('awesomeRepo2.csv', 'r')
for line in f:
  repos.append(clean(line))
  numRepos += 1
f.close()

gitSize = 0
hgSize = 0
for repo in repos:
  splitRepo = repo.split(';')
  if( splitRepo[1] == 'git' ):
    gitSize += int(splitRepo[0])
  elif( splitRepo[1] == 'hg' ):
    hgSize += int(splitRepo[0])
  else:
    print 'Unknown type: ' + splitRepo[1]

print 'Sizes:'
print '  Git: ' + str(gitSize)
print '  Hg:  ' + str(hgSize)
