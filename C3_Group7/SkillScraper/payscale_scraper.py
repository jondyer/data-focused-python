# -*- coding: utf-8 -*-
"""
Created on Sat Feb  9 19:29:13 2019

filename: payscale_scraper.py

Group members: 
Jonathan Dyer
Devraj Kori 
Muriel Pokol 
Brian Rhindress
Matthew Samach 

Code function: This scrapes payscale.com for an up-to-date list of payscale.com skill listings. Not used in production version.

Imported by: 
Imports: urllib.request.urlopen, bs4.BeautifulSoup, csv

"""
from urllib.request import urlopen  # b_soup_1.py
from bs4 import BeautifulSoup
import csv

### Main scraper function ###
def main():
    html = urlopen('https://www.payscale.com/index/US/Skill')
    bsyc = BeautifulSoup(html.read(), "lxml")
    table = bsyc.findAll('table')
    # Initialize list of lists 
    entries = []
    # For all rows in the table, collect the data 
    for rows in table[0].children:
        try:
            # Initialize the [job skill, # entries] pair
            pair = []
            # For each td in row, collect the job title and entry
            for data in rows.children:				
                try:
                    # If length is 3, it is an <a href= ...> data </a> tag with \n on each side.  We want the data, not the tag 
                    if( len(data) == 3 ):
                        pair.append(data.contents[1].contents[0]) 
                    # Else, it is the # of entries, but needs to be cleaned of spaces and \n 
                    elif( len(data) == 1 ):
                        data = data.contents[0]
                        data_clean = data.replace(' ', '')
                        data_clean = data_clean.replace('\n', '')
                        pair.append(data_clean)
                    else:
                        pass
                except:
                    pass
            # Add the pair to the final list 
            entries.append(pair)
        except:
            pass
        # creates .csv file
        myFile = open('payscale_clean_data.csv', 'w', newline='')
        with myFile:
            writer = csv.writer(myFile)
            writer.writerows(entries)


if __name__ == "__main__":
	main()