"""
@author: Jonathan Dyer & Brian Rhindress
2/3/2019
"""
records =[]
with open('expenses.txt','r') as expense_file:
	for line in expense_file:
		records.append(line)

for line in records:
	print(line)

