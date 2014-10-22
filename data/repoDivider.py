divfile = open('awesomeRepoSizes.csv', 'r')
outfile = open('hg_remaining.csv', 'w')

delim = ';'

todo = []

for line in divfile:
	split_line = line.split(delim)
	repo_type = split_line[1]
	if( repo_type == 'hg' ):
		repo_name = split_line[5]
		#repo_name = repo_name.replace('\n', '')
		dir_name = repo_name.replace('/', '_', 1)
		if( dir_name > 'esuwartadi_adjointperm' ):
			todo.append(dir_name)
			
sorted_list = sorted(todo)
for entry in sorted_list:
	outfile.write(entry)