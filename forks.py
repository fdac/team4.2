import multiprocessing
import os
from sys import argv, exit
import argparse
import envoy, time

def clean(str):
  return str.replace('\n', '')
  
def diskCap():
  proc = subprocess.Popen(["df -k . | tail -1 | awk '{ print $4 }'"], stdout=subprocess.PIPE, shell=True)
  (out, err) = proc.communicate()
  return out

def clone(repos, forkid):

  f = open('errors' + str(forkid) + '.txt', 'w')
  start = time.time()
  now = start
  nmax = diskCap()
  nused = 0
  totalSize = 0
  totalCloned = 0
  totalTime = 0
  gitTime = 0
  hgTime = 0
  
  for repo in repos:
    splitRepo = repo.split(';')
    totalSize = totalSize + int(splitRepo[0])

  for repo in repos:

    splitRepo = repo.split(';')
    
    repoSize = int(splitRepo[0])
    versContType = splitRepo[1]
    target = splitRepo[5] # repo name
    dest = target.replace('/', '_', 1)

    if versContType == 'hg':
      command = 'hg clone -U https://bitbucket.org/' + target + ' hg/' + dest
    elif versContType == 'git':
      command = 'git clone --mirror https://bitbucket.org/' + target + ' git/' + dest

    print command

    if (nused + repoSize > nmax):
      now0 = time.time()
      print str (nused) + ' cloned in ' + str (now0 - now) 
      now = time.time()
	  envoy.run ('rsync -ae "ssh -p2200" hg/* cdaffron@da2.eecs.utk.edu:hg')
	  envoy.run ('rsync -ae "ssh -p2200" git/* cdaffron@da2.eecs.utk.edu:git')
      envoy.run ('ls | while read dir; do [[ -d $dir ]] && find $dir -delete; done')
      now = time.time()
      print str (nused) + ' synced in ' + str (now - now0) 
      nused = 0
    
	if( versContType == 'hg' ):
	  startHg = time.time()
	  r = envoy.run (command)
	  endHg = time.time()
	  hgTime += (endHg - startHg)
	else:
	  startGit = time.time()
	  r = envoy.run(command)
	  endGit = time.time()
	  gitTime += (endGit - startGit)
	
	if( r.status_code != 0):
	  f.write('Repo ' + target + ' failed to clone')
	else:
	  nused += repoSize
	  totalCloned += repoSize
	  totalTime = time.time() - start;
      print 'PID: ' + str(forkid)
      print '    ' + str(totalCloned) + ' bytes cloned'
      print '    ' + str((float(totalCloned) / float(totalSize)) * 100) + '% done'
      print '	 ' + str(totalTime) + ' seconds elapsed'
	  print '      Git:' + str(gitTime)
	  print '      Hg: ' + str(hgTime)

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

#clone(processRepos[0])

for i in range(numCores):
  forkId = i
  if(os.fork() == 0):
    #print 'Process: ' + str(forkId)
	clone(processRepos[0], forkid)
    break;


