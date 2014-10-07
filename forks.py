import multiprocessing
import requests
import subprocess
import os
import io
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

  #repos.reverse()
  if((forkid % 2) == 0):
    os.chdir('/disk1')
  else:
    os.chdir('/disk2')
  
  if not os.path.isdir(str(forkid)):
    os.mkdir(str(forkid));
  os.chdir(str(forkid));
  
  f = open('errors' + str(forkid) + '.txt', 'w')
  s = open('stats' + str(forkid) + '.txt', 'w')
  s.write("TEST!!!!!!!!\n")
  f.write("TEST2\n")
  start = time.time()
  now = start
  nmax = diskCap()
  nused = 0
  totalSize = 0
  totalCloned = 0
  totalTime = 0
  gitTime = 0
  hgTime = 0
  prevSize = 0
  rsyncThresh = 10737418240  # 10 GB
  
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
    s.write(command + '\n')
    s.flush()
    os.fsync(s.fileno())

    nmax = diskCap()

    if ((repoSize > (float(nmax) * 0.25)) or (prevSize > rsyncThresh)):
      now0 = time.time()
      s.write('RSYNC!!!!!\n')
      s.write('    ' + str (nused) + ' cloned in ' + str (now0 - now) + '\n')
      now = time.time()
      s.write('    current dir: ' + os.getcwd() + '\n')
      envoy.run ('rsync -ae "ssh -p2200" hg/ cdaffron@da2.eecs.utk.edu:hg')
      envoy.run ('rsync -ae "ssh -p2200" git/ cdaffron@da2.eecs.utk.edu:git')
      envoy.run ('ls | while read dir; do [[ -d $dir ]] && find $dir -delete; done')
      now = time.time()
      s.write('    ' + str (nused) + ' synced in ' + str (now - now0) + '\n')
      s.flush()
      os.fsync(s.fileno())
      nused = 0
    
    api = requests.get('https://api.bitbucket.org/2.0/repositories/' + target)

    if((versContType == 'hg') and (api.status_code != 403) ):
      startHg = time.time()
      r = envoy.run (command)
      endHg = time.time()
      hgTime += (endHg - startHg)
    elif( api.status_code != 403 ):
      startGit = time.time()
      r = envoy.run(command)
      endGit = time.time()
      gitTime += (endGit - startGit)
	
    if((r.status_code != 0) or (api.status_code == 403)):
      f.write(versContType + ' repo ' + target + ' failed to clone')
      if(api.status_code == 403):
        f.write(' PRIVATE\n')
      else:
        f.write('\n')
      f.flush()
      os.fsync(f.fileno())
    else:
      prevSize = repoSize
      nused += repoSize
      totalCloned += repoSize
      totalTime = time.time() - start;
      s.write('Repo ' + target + 'cloned\n')
      s.write('\t' + str(totalCloned) + ' bytes cloned\n')
      s.write('\t' + str((float(totalCloned) / float(totalSize)) * 100) + '% done\n')
      s.write('\t' + str(totalTime) + ' seconds elapsed\n')
      s.write('\t  Git:' + str(gitTime) + '\n')
      s.write('\t  Hg: ' + str(hgTime) + '\n')
      print 'Repo Cloned!\n'
      s.flush()
      os.fsync(s.fileno())

  now0 = time.time()
  s.write('Final RSYNC\n')
  s.write('    ' + str(nused) + ' cloned in ' + str(now0 - now) + '\n')
  #now = time.time()
  envoy.run('rsync -ae "ssh -p2200" hg/* cdaffron@da2.eecs.utk.edu:hg')
  envoy.run('rsync -ae "ssh -p2200" git/* cdaffron@da2.eecs.utk.edu:git')
  envoy.run('ls | while read dir; do [[ -d $dir ]] && find $dir -delete; done')
  now = time.time()
  s.write('    ' + str(nused) + ' synced in ' + str(now - now0) + '\n')
  nused = 0

numCores = multiprocessing.cpu_count()
#numCores = 1
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
    clone(processRepos[forkId], forkId)
    break;


