##
# Jonathan Dyer (jbdyer)
# Brian Rhindress (brhindre)
##
# coding: utf-8


# Question 1
records = []

with open("expenses.txt", "r") as file:
    for line in file.readlines():
        records.append(line.rstrip())

import re

# 1a
# pat = r'D'

# 1b
# pat = r'\''

# 1c
# pat = r'\"'

# 1d
# pat = r'^7'

# 1e
# pat = r'[rt]$'

# 1f
# pat = r'\.'

# 1g
# pat = r'r.*g'

# 1h
# pat = r'[A-Z][A-Z]'

# 1i
# pat = r','

# 1j
# pat = r',.*,.*,.*'

# 1k
# pat = r'^[^vwxyz]*$'

# 1l
# pat = r'(?<![0-9])[1-9][0-9]\.[0-9][0-9]'

#1m
# pat = r'(^[^,]*[,][^,]*[,][^,]*[,][^,]*$)'

#1n
# pat = r'\('

#1o
# pat = r'[1-9]+[0-9]*[0-9][0-9]\.[0-9][0-9]'

#1p
# pat = r'[0-9]:....:'

#1q
# pat = r':20[01][0-9]03'

#1r
# pat = r'[a].*[b].*[c]'

#1s
# pat = r'(.)\1.*\1\1.*\1\1'

#1t
# pat = r'([a].*[0-9])|([0-9].*[a])'

#1u
# pat = r'^[^A-Z]*$'

# records.append('doily')
#1v
# pat = r'[d].?[i]'

for line in records:
    if re.search(pat, line) != None:
        print(line)
