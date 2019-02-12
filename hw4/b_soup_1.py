from urllib.request import urlopen  # b_soup_1.py
from bs4 import BeautifulSoup

html = urlopen('https://www.treasury.gov/resource-center/'
               'data-chart-center/interest-rates/Pages/'
               'TextView.aspx?data=yieldYear&year=2018')

bsyc = BeautifulSoup(html.read(), "lxml")

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

# for i in daily_yield_curves:
# 	print(i)


##### Now write output #####
with open('daily_yield_curves.txt','w') as output:

    ### Table 1 output (B-records) ###
    column_width = 11
    column_label_1 = daily_yield_curves[0]
    column_label_3 = '-------'

    # print header
    for column_label in column_label_1:
        output.write(column_label.ljust(column_width))
    output.write('\n')

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

import datetime
start_date = datetime.datetime(2018, 1, 2)

first = True
for row in daily_yield_curves[1:]:

	# Finding dist from first /1/02/18
	row_date_list = row[0].split('/')
	row_date = datetime.datetime(int('20'+row_date_list[2]),
		int(row_date_list[0]), int(row_date_list[1]))
	days_diff = row_date - start_date

	if first:
		X = np.repeat(days_diff.days,len(row[1:]))
		Y = np.array([1, 3, 6, 12, 24, 36, 60, 84, 120, 240, 360])
		Z = np.array(row[1:])
		first = False
	else:
		X = np.vstack((X, np.repeat(days_diff.days,len(row[1:]))))
		Y = np.vstack((Y,[1, 3, 6, 12, 24, 36, 60, 84, 120, 240, 360]))
		Z = np.vstack((Z,np.array(row[1:])))

# print(X)
# print(Y)
# print(Z)

# Plot the surface.
surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm,
                       linewidth=0, antialiased=False)
# Customize the z axis.
ax.set_xlim(0, 400)
ax.set_ylim(0, 400)
ax.set_zlim(0, 4)

ax.zaxis.set_major_locator(LinearLocator(10))
ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

# add labels
ax.set_xlabel("Days since 01/02/18")
ax.set_ylabel("Months to maturity")
ax.set_zlabel("Rate")


# Add a color bar which maps values to colors.
fig.colorbar(surf, shrink=0.5, aspect=5)

plt.show()


# now for the wireframe
fig = plt.figure()
ax = fig.gca(projection='3d')

ax.plot_wireframe(X, Y, Z)

# Set the labels
ax.set_xlabel("Days since 01/02/18")
ax.set_ylabel("Months to maturity")
ax.set_zlabel("Rate")


plt.show()


### Part C
import pandas as pd

# Make DF out of daily_yield_curves list of lists
yield_curve_df = pd.DataFrame(data = [row[1:] for row in daily_yield_curves[1:]],
	columns = daily_yield_curves[0:1][0][1:], index = [row[0] for row in daily_yield_curves[1:]])

# print(yield_curve_df)

# Plot DF
yield_curve_df.plot(title='Interest Rate Time Series, 2018')
plt.show()


#Transpose DF and slice out one of every 20 columns
t_yield_curve_df = yield_curve_df.T[yield_curve_df.T.columns[[i for i in range(0,len(yield_curve_df),20)]]]

# convert column names to numbers
col_names_to_ints = { '1 mo' : 1, '3 mo' : 3, '6 mo' : 6, '1 yr' : 12, '2 yr' : 24,
                        '3 yr' : 36, '5 yr' : 60, '7 yr' : 84, '10 yr' : 120, '20 yr' : 240, '30 yr' : 360 }

t_yield_curve_df_renamed = t_yield_curve_df.rename(index=col_names_to_ints)

# print(t_yield_curve_df_renamed)
# Plot it
t_yield_curve_df_renamed.plot(title='2018 Yield Curves, 20 Day Intervals')
plt.show()
