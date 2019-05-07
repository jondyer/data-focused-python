#!/usr/bin/env python
"""
Created on Sat Feb  9 19:29:13 2019

filename: match_indeed_to_skill.py

Group members: 
Jonathan Dyer
Devraj Kori 
Muriel Pokol 
Brian Rhindress
Matthew Samach 

Code function: Scrapes the top 5-pages from a selected indeed.com job search. 
Cross-compares and counts the number of job skill occurrences, based on payscale.com skill lists.
Also generates a df of job listings on indeed.come for the given job search. 

Imported by: 
Imports: urllib.request.urlopen, bs4.BeautifulSoup, csv

"""


### Gets list of skills from payscale.com csv ###
def get_skill_list():
    #read in list of skills as
    import pandas as pd
    df_skills= pd.read_csv('./data/payscale_clean_data.csv')
    #store the list of skills from payscale
    raw_skill_list=list(df_skills["PopularSkills"])
    #replace special characters with escapes, and split multiple skills separated by '/'
    skill_list=list()
    for i in range(0,len(raw_skill_list)):
        skill=raw_skill_list[i]
        skill=skill.replace(r'+',r'\+')
        skill=skill.replace(r'.',r'\.')
        skill=skill.replace(' / ','/')
        skill=skill.replace(r')','')
        skill=skill.split('/')
        #break out parenthetical items into their own searches
        skill_temp=list()
        for a in skill:
            b=a.split(r'(')
            for c in b:
                skill_temp.append(c)
        skill=skill_temp
        for x in skill:
            skill_list.append(x)
    #pad everything with spaces at the start and end
    for i in range(0,len(skill_list)):
        skill=skill_list[i]
        skill=skill.center(len(skill)+2)
        skill_list[i]=skill
    #remove OR since its a common word
    skill_list.remove(" OR ")
    return(skill_list)


#define function that scrapes one page at a time and returns a panda dataframe
def scrape_page(page_num,job,city,state,skill_list):
    import requests  # b_soup_1.py
    import re
    from bs4 import BeautifulSoup
    #spoof the user agent to make page scrapable
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    #define position search term (one word) and location
    #replace spaces in the user input job with plus
    position=job.replace(" ","+")
    location=city+"+"+state
    page_str=str(page_num)
    #url for search query
    url='https://www.indeed.com/jobs?q='+position+'&l='+location+'&start='+page_str
    search_page=requests.get(url,headers=headers)
    soup=BeautifulSoup(search_page.content,'html.parser')
    all_cards=soup.find_all(class_='jobsearch-SerpJobCard row result')
    #empty list to store job posting urls
    job_urls=[]
    #it seems to be easier to pull posting dates and locations from search page, so do that here
    posting_dates=[]
    locations=[]
    #iterate through all_cards, extract job posting urls, posting dates, and locations
    for card in all_cards:
    #urls
        job_id=card['data-jk']
        job_url='https://www.indeed.com/viewjob?jk='+job_id
        job_urls.append(job_url)
    #posting dates
    #some jobs don't have posting dates so try them
        try:
            job_post_date=card.find(class_='date').get_text()
        except:
            job_post_date=' '
        posting_dates.append(job_post_date)
    #locations
        job_location=card.find(class_='location').get_text()
        locations.append(job_location)


    #locations
    #lets make this dataframe
    #declare the empty lists that will become columns
    position_name=[]
    employer=[]
    full_description=[]
    #in the future, we can develop a list of keywords that we'll
    #search postings for, but for now, just return all capitalized
    #words besides common words
    for job_url in job_urls:
        #retrieve job page
        job_page=requests.get(job_url,headers=headers)
        #make job page into BeautifulSoup object
        job_soup=BeautifulSoup(job_page.content,'html.parser')
        #retrieve the job title
        try:
            job_position=job_soup.find(class_='icl-u-xs-mb--xs').get_text()
        except:
            job_position=""
        #retrieve company name from job rating line on page

        job_rating_line=job_soup.find(class_='jobsearch-InlineCompanyRating')

        #some jobs seem to not have a job rating line, so wrap this step in try
        try:
            job_employer=job_rating_line.find(class_='icl-u-lg-mr--sm').get_text()
        except:
            job_employer=""
            #retrieve full job description
        job_descrip=job_soup.find(class_='jobsearch-JobComponent-description').get_text().upper()
        #replace line breaks and common punctuation with spaces
        to_replace=['\n','\t','\.','\,','\(','\)','\;','\:']
        for x in to_replace:
            job_descrip.replace(x,' ')

        #append all of the items created to the empty lists from last step
        position_name.append(job_position)
        employer.append(job_employer)
        full_description.append(job_descrip)

    #for each skill in skill_list, search the job description to see if contains that skill
    #if it contains the skill, assign the value 1 to it and if not, assign 0
    #create blank dictionary that will store the 1-0 values
    skill_dict=dict()
    for skill in skill_list:
        #create a blank list to show 0-1 values
        match_values=list()
        for descrip in full_description:
            if re.search(skill.upper(),descrip)==None:
                match_values.append(0)
            else:
                match_values.append(1)
        skill_dict[skill]=match_values
    #store results in dictionary, then data frame
    import pandas as pd
    result_dict={'Job Title':position_name,
                'Employer':employer,
                'Location':locations,
                'Posting Date':posting_dates,
                'Posting Url':job_urls,
                'Full Job Description':full_description,
                }
    result_dict={**result_dict,**skill_dict}
    result_frame=pd.DataFrame(result_dict)
    return(result_frame)


#function that scrapes 5 pages
def scrape_pages(user_input_job,user_input_city,user_input_state,skill_list):
    import pandas as pd
    df=scrape_page(0,user_input_job,user_input_city,user_input_state,skill_list)
    for x in range(1,5):
        temp=scrape_page(x,user_input_job,user_input_city,user_input_state,skill_list)
        df=pd.concat([df,temp])
    return(df)





#function to return frame of skills listing the number of jobs that matched each skill
def return_job_count(skill_list,df):
    import pandas as pd
    skill_sums=list()
    for skill in skill_list:
        skill_sums.append(sum(df[skill]))

    job_counts_dict={"Skill":skill_list,"Job_Matches":skill_sums}
    job_counts=pd.DataFrame(job_counts_dict).sort_values(by="Job_Matches",ascending=False)
    job_counts=job_counts[job_counts["Job_Matches"]>0]
    return(job_counts)

skill_list=get_skill_list()

df=scrape_pages("Financial Analyst","Pittsburgh","PA",skill_list)
return_job_count(skill_list,df)
#df2 = return_job_count("Financial Analysts","Pittsburgh","PA")
#df2
