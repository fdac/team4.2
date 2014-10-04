import envoy, re, time

start = time .time()
now = start
nmax = DiskCapacity
nused = 0
f = open ('awesomeRepo1.csv')
for l in f: 
  ar = l .split(';')
  t = int (ar [0])
  n = ar[2]
  p = re. sub('/', '_', n)
  vcs = ar [1]
  if vcs == 'hg':
    cmd = 'hg clone -U https://bitbucket.org/' + n + ' ' + p
  elif vcs == 'git':
    cmd = 'git clone --mirror https://bitbucket.org/' + n + ' ' + p
  if (nused + t > DiskCapacity):
    now0 = time .time()
    print str (nused) + ' cloned in ' + str (now0 - now) 
    now = time .time()
    envoy .run ('rsync -ae "ssh -p2200" * drose17@da2.eecs.utk.edu:hg')
    envoy .run ('ls | while read dir; do [[ -d $dir ]] && find $dir -delete; done')
    now = time .time()
    print str (nused) + ' synced in ' + str (now - now0) 
    nused = 0
  nused += t
  envoy .run (cmd)
f .close()