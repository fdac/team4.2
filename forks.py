import multiprocessing
import os
from sys import argv, exit
import argparse
import envoy, time

def clean(str):
  return str.replace('\n', '')

def clone(repos):

  start = time.time()
  now = start
  nmax = DiskCapacity
  nused = 0

  for repo in repos:

    splitRepo = repo.split(';')
    
    repoSize = int(splitRepo[0])
    versContType = splitRepo[1]
    target = splitRepo[5] # repo name
    dest = target.replace('/', '_', 1)

    if versContType == 'hg':
      command = 'hg clone -U https://bitbucket.org/' + target + ' ' + dest
    elif versContType == 'git':
      command = 'git clone --mirror https://bitbucket.org/' + target + ' ' + dest

    print command

    if (nused + repoSize > DiskCapacity):
      now0 = time.time()
      print str (nused) + ' cloned in ' + str (now0 - now) 
      now = time.time()
      # envoy.run ('rsync -ae "ssh -p2200" * drose17@da2.eecs.utk.edu:hg')
      # envoy.run ('ls | while read dir; do [[ -d $dir ]] && find $dir -delete; done')
      now = time.time()
      print str (nused) + ' synced in ' + str (now - now0) 
      nused = 0
    
    nused += repoSize
    # envoy.run (command)

numCores = multiprocessing.cpu_count()
forkId = 0

parser = argparse.ArgumentParser(description='Creates a clone process for every core.');
parser.add_argument('repoFile',
                    type=str,
                    help='file of repositiories to clone')

if len(argv) == 1:
  parser.print_usage()
  exit()

options = parser.parse_args(argv[1:])
repoFile = options.repoFile
print options
print repoFile

processRepos = []
for i in range(numCores):
  processRepos.append([])

numRepos = 0

f = open(repoFile, 'r')
for line in f:
  processRepos[numRepos % numCores].append(clean(line))
  numRepos += 1
f.close()

clone(processRepos[0])

# for i in range(numCores):
# 	forkId = i
# 	if(os.fork() == 0):
# 		print 'Process: ' + str(forkId)
# 		break;


