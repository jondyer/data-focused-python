"""
@author: Jonathan Dyer & Brian Rhindress
2/3/2019
"""

# 1a 
records =[]

with open('expenses.txt','r') as expense_file:
	for line in expense_file:
		records.append(line.split('\n')[0])

for line in records:
	print(line)

# 1b 
with open('expenses.txt','r') as expense_file:
	records2 = [line.split('\n')[0] for line in expense_file]

print("\nrecords == records2:",
records == records2, '\n')

#1c
with open('expenses.txt','r') as expense_file:
		records3 = tuple([tuple(line.split('\n')[0].split(':')) 
			for line in expense_file])
	
	# This also works and may be more what he's looking for? 
	#records3 = tuple((tuple(i for i in line.split('\n')[0].split(':'))) 
		#for line in expense_file)

for tup in records3:
	print(tup)

# 1d
cat_set = set(line[1] for line in records3 if line[1] != 'Category')
date_set = set(line[2] for line in records3 if line[1] != 'Date')

print()
print('Categories:', cat_set, '\n')
print('Dates:     ', date_set, '\n')

# 1e
rec_num_to_record = {line_num : records[line_num] for line_num in range(0,len(records3),1) }

for rn in range(len(rec_num_to_record)):
		    print('{:3d}: {}'.format(rn,
		    	rec_num_to_record[rn]))

print()
for i in rec_num_to_record.items():
		    print('{:3d}: {}'.format(i[0], i[1]))
