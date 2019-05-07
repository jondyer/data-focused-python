"""
filename: bls_data_frame.py
date: 2/22/19

Group members: 
Jonathan Dyer
Devraj Kori 
Muriel Pokol 
Brian Rhindress
Matthew Samach 

Code function: This file initializes a data frame containing employment data indexed by job titles,
mapped to total employment, 25%, median, and 75% Annual Salary Figures

Imported by: SkillScraper.py
Imports: pandas, csv

"""

### Gets list of all possible jobs from BLS csv ###
def get_job_list(df_bls):
    # all possible jobs
    job_list = df_bls.index.values.tolist()

    return(job_list)

### Gets df of all BLS data ###
def get_df_bls():

    import pandas as pd
    import csv

    # read in BLS csv and set index_col = 0 to use first col (OCC_TITLE) as index
    df_bls = pd.read_csv('./data/BLS_employment_data.csv', index_col = 0)

    	# Drop all non-detailed rows
    df_bls = df_bls.drop(df_bls[df_bls['OCC_GROUP']!='detailed'].index.values.tolist())

    # Drop all but desired Columns
    df_bls = df_bls[['TOT_EMP','A_PCT25','A_MEDIAN','A_PCT75']]

    return(df_bls)

### Gets BLS stats for chosen job ###
def get_job_stats(df_bls, sample_job):
    # test with job

    	# Retrieve key indicators
    total_employment = df_bls['TOT_EMP'][sample_job]
    annual_salary_25 = df_bls['A_PCT25'][sample_job]
    annual_salary_median = df_bls['A_MEDIAN'][sample_job]
    annual_salary_75 = df_bls['A_PCT75'][sample_job]

    return(str('For ' + sample_job +
    '\nTotal Employment: ' + total_employment +
    '\nAnnual Salary 25 Percentile: ' + annual_salary_25 +
    '\nAnnual Median Salary: ' + annual_salary_median +
    '\nAnnual Salary 75 Percentile: ' + annual_salary_75))
