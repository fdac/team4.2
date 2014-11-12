import sys, pickle

infile = open('prepR.r', 'r')
outfile = open('qualityProjects.r', 'w')

count = 0
first = True
for line in infile:
  if first == True:
    first = False
    continue
  splitline = line.split(';')
  # forks.append(int(splitline[2]))
  if(int(splitline[2]) >= 4):
    outfile.write(splitline[0] + '\n')
  if(count % 1000 == 0):
    print str(count)
  # if(int(splitline[2]) != 0):
    # break
  count += 1
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