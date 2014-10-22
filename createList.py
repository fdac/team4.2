
repos = []
numRepos = 0

f = open('awesomeRepos', 'r')
outfile = open('fullList', 'w')
for line in f:
    splitRepo = line.split(';')
    name = splitRepo[2]
    outfile.write(name)

f.close()