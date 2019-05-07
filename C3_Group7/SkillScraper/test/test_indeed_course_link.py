# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
#read in the heinz_scraper module
import heinz_scraper as hs
#read in the match_indeed_to_skill module
import match_indeed_to_skill as mi

#scrape first 10 jobs
skills=mi.return_job_count('analyst','pittsburgh','pa')[0:5]

skills

skills_to_match=skills['Skill']
#every skill in skills is padded with a space so remove the first and last digit
skills_to_match=[x[1:(len(x)-1)] for x in skills_to_match]

hs.get_skill_map(skills_to_match)
