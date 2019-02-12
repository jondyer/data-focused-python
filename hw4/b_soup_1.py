from urllib.request import urlopen  # b_soup_1.py
from bs4 import BeautifulSoup

html = urlopen('https://www.treasury.gov/resource-center/'
               'data-chart-center/interest-rates/Pages/'
               'TextView.aspx?data=yieldYear&year=2018')

bsyc = BeautifulSoup(html.read(), "lxml")

# fout = open('bsyc_temp.txt', 'wt',
# 		encoding='utf-8')

# fout.write(str(bsyc))

# fout.close()

# # print the first table
# print(str(bsyc.table))
# # ... not the one we want

# so get a list of all table tags
# table_list = bsyc.findAll('table')

# how many are there?
# print('there are', len(table_list), 'table tags')

# # look at the first 50 chars of each table
# for t in table_list:
#     print(str(t)[:50])

# only one class="t-chart" table, so add that
# to findAll as a dictionary attribute
# tc_table_list = bsyc.findAll('table',
#                       { "class" : "t-chart" } )

# # how many are there?
# print(len(tc_table_list), 't-chart tables')

# # only 1 t-chart table, so grab it
# tc_table = tc_table_list[0]

# # what are this table's components/children?
# for c in tc_table.children:
#     print(str(c)[:50])

# # tag tr means table row, containing table data
# # what are the children of those rows?
# # for c in tc_table.children:
# #     for r in c.children:
# #         print(str(r)[:50])

# # # we have found the table data!
# # # just get the contents of each cell
# # for c in tc_table.children:
# #     for r in c.children:
# #         print(r.contents)


# only one class="t-chart" table, so add that
# to findAll as a dictionary attribute
t_chart_tables = bsyc.findAll('table', { "class" : "t-chart" } )

# since len t_chart_table = 1
t_chart_table = t_chart_tables[0]

# initialize our final list of lists 
daily_yield_curves = []

# for each row in the t-chart 
for r in t_chart_table.children:

	# initialize a new data list for the table row (date)
	data_list = []

	# for each data point in the row, place into a list 
	for d in r.children:

		data = d.contents[0]

		try: # convert to floats 
			data = float(data)
		except:
			pass # string, no transformation

		data_list.append(data)

	# add this row list to the list of lists 
	daily_yield_curves.append(data_list)

# remove the '2 mo' interest rates 
for c in daily_yield_curves:
	c.pop(2)

for i in daily_yield_curves:
	print(i)


##### Now write output #####
with open('daily_yield_curves.txt','w') as output:
    
    ### Table 1 output (B-records) ###
    column_width = 11
    column_label_1 = daily_yield_curves[0]
    #column_label_2 = ['Code', 'Month', 'Type', 'Exp Date', 'Code', 'Exp Date']
    column_label_3 = '-------'

    # print header
    for column_label in column_label_1:
        output.write(column_label.ljust(column_width))
    output.write('\n')

    # for column_label in column_label_2:
    #     output.write(column_label.ljust(column_width))
    # output.write('\n')

    for i in range(0,len(daily_yield_curves[0]),1):
        output.write(column_label_3.ljust(column_width))
    output.write('\n')

    # print data excluding header
    for row in daily_yield_curves[1:]:
        for value in row:
            output.write(str(value).ljust(column_width))
        output.write('\n')


### Part B 
### Source: https://matplotlib.org/gallery/mplot3d/surface3d.html
# This import registers the 3D projection, but is otherwise unused.
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import

import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import numpy as np


fig = plt.figure()
ax = fig.gca(projection='3d')

# Make data.
#X = days since 1/02/18 
import datetime 
start_date = datetime.datetime(2018, 1, 2)

X = np.append([[]], [[]], axis = 0)

for row in daily_yield_curves[1:]:
	row_date_list = row[0].split('/')
	print(row_date_list)
	row_date = datetime.datetime(int('20'+row_date_list[2]),
		int(row_date_list[0]), int(row_date_list[1]))	
	days_diff = row_date - start_date
	#print(np.repeat(days_diff.days,len(row[1:])))
	if len(X) < 1:
		X = np.repeat(days_diff.days,len(row[1:]))
	else:
		X = np.append(X,np.repeat(days_diff.days,len(row[1:])), axis = 0)
#np.append([[1,1],[2,2]],[[3,3]], axis = 0)

print(X)



# X = np.arange()
# X = np.arange(-5, 5, 0.25)
# Y = np.arange(-5, 5, 0.25)
# X, Y = np.meshgrid(X, Y)
# R = np.sqrt(X**2 + Y**2)
# Z = np.sin(R)

# # Plot the surface.
# surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm,
#                        linewidth=0, antialiased=False)

# # Customize the z axis.
# ax.set_zlim(-1.01, 1.01)
# ax.zaxis.set_major_locator(LinearLocator(10))
# ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

# # Add a color bar which maps values to colors.
# fig.colorbar(surf, shrink=0.5, aspect=5)

# plt.show()