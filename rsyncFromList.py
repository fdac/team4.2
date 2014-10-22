import multiprocessing
import requests
import shutil
import subprocess
import os
import io
from sys import argv, exit
import argparse
import envoy, time

parser = argparse.ArgumentParser(description='rsyncs selected folders')
parser.add_argument('list_file', type=str)
args = parser.parse_args()

listFile = args.list_file

infile = open(listFile, 'r')

startTimeOverall = time.time()

for dir in infile:
	dir_noNew = dir.replace('\n', '')
	rsyncStart = time.time()
	r = envoy.run('rsync -vae "ssh -i /home/ec2-user/.ssh/id_rsa_rsync -p 2202" /home/ec2-user/hg/' + dir + ' cdaffron@da2.eecs.utk.edu:hg')
	rsyncEnd = time.time()
	print '|||||||| RSYNC ||||||||'
	print '|| Std Out ||'
	print r.std_out
	print '|| Std Err ||'
	print r.std_err
	print '|| Time ||'
	print str(rsyncEnd - rsyncStart) + ' seconds'
	#print 'rsync -vae "ssh -i /home/ec2-user/.ssh/id_rsa_rsync -p 2202" /home/ec2-user/hg/' + dir_noNew + ' cdaffron@da2.eecs.utk.edu:hg'
	#exit()
	
endTimeOverall = time.time()

print 'Total Time: ' + str(endTimeOverall - startTimeOverall) + ' seconds'