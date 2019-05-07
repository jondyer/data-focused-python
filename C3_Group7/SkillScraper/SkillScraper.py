# -*- coding: utf-8 -*-
"""
Created on Sat Feb 23 14:34:54 2019

filename: SkillScraper.py

Group members: 
Jonathan Dyer
Devraj Kori 
Muriel Pokol 
Brian Rhindress
Matthew Samach 

Code function: The Main Controller. This script creates the Heinz SkillScraper GUI, allows for user input, 
and draws on data from each of the other modules to aggregate job-skill-course information. 

Imported by: 
Imports: Tkinter, bls_data_frame, match_indeed_to_skill,
heinz_scraper, pandas, sys

"""

import sys
if "Tkinter" not in sys.modules:
    from tkinter import *

# read in bls_data_frame module
import bls_data_frame as b
# read in the match_indeed_to_skill module
import match_indeed_to_skill as mi
# read in the heinz_scraper module
import heinz_scraper as hs
import pandas as pd

# Get DF of BLS with Data
df_bls = b.get_df_bls()

# Get full list of BLS-tracked jobs
job_list = b.get_job_list(df_bls)

# Get full list of possible skills
print("Scraping skills from Payscale...".ljust(35), end='')
skill_list = mi.get_skill_list()
#remove some skills that are returning erroneous matches.
to_remove=[' Training ', ' Tools ', ' Design ']
for x in to_remove:
    skill_list.remove(x)
print("done.")

# Run initial Heinz Course scraping

### Builds GUI ###
def skill_builder_interface():
    # Create command for submit button
    def click():

        # Get Drop-down selection
        entered_text = variable.get()

        # Set Job to drop-down text
        job = entered_text

        # Get Job_stats
        job_stats = b.get_job_stats(df_bls, job)

        #Get Indeed scrape
        job_df = mi.scrape_pages(job,'Pittsburgh','PA',skill_list)
        #limit indeed scrape to just first two columns, for job output
        job_df_for_output=job_df[['Job Title', 'Employer']]
        #concatenate the job and employer
        job_postings=pd.DataFrame([i+', '+j for i, j in zip(job_df_for_output["Job Title"],job_df_for_output["Employer"])])

        # Match skills - jobs
        job_skill_count = mi.return_job_count(skill_list,job_df)


        #strip the skills returned from job_skill_count to match with the skill map
        job_skill_count=job_skill_count.applymap(lambda x: x.strip() if type(x)==str else x)

        #to avoid matching too many courses, only return course matches for top 10 skills
        top_10=job_skill_count.head(10)

        # Match skills to Heinz course listings
        skill_map = hs.get_skill_map(top_10['Skill'].values)

        # turn courses into a printable format
        course_set = set()
        for i in skill_map.values():
            course_set.update(i)
        course_pd = pd.DataFrame(list(course_set))

        output_job.delete(0.0, END)
        output_job.insert(END, job_stats)

        output_skills.delete(0.0, END)
        output_skills.insert(END, job_skill_count.to_string(index=False,justify="center"))

        output_courses.delete(0.0, END)
        output_courses.insert(END, course_pd.values)

        output_postings.delete(0.0,END)
        output_postings.insert(END,job_postings)

    window = Tk()
    window.title("SkillScraper")
    window.configure(bg="white")

    # add Heinz image
    photo1 = PhotoImage(file="./img/Skill_Scraper.gif")
    Label(window, image=photo1, bg="white").grid(row=0, column=0, sticky=W, columnspan=2)

    # Create job selection pull-down menu
    lbl_input = Label(window, text="Dream job?", bg="white", fg="red4", font="times 14 bold")
    lbl_input.grid(row=1, column=0, sticky=W)

    variable = StringVar(window)
    jobs = job_list
    variable.set("No Job Selected")

    textentry_menu = OptionMenu(window, variable, *jobs)
    textentry_menu.config(bg="red4", activebackground="red4", fg="white", activeforeground="white", font="times 10")
    textentry_menu.grid(row=2, column=0, columnspan=1, sticky = N+S+W+E, padx = 5, pady = 5)
    textentry = str(textentry_menu)

    # Create a "Submit" button
    submit_button = Button(window, text="Submit", width=8, command=click, activebackground="gray70", font="times 10")
    submit_button.grid(row=2, column=1, sticky=W)

    # Create text output sections
    lbl_output_skills = Label(window, text="\nSkills Needed:", bg="white", fg="red4", font="times 14 bold")
    lbl_output_skills.grid(row=4, column=0, sticky=W)
    output_skills = Text(window, width=35, height=6, wrap=WORD, bg="MistyRose2", bd=2)
    output_skills.grid(row=5, column=0, columnspan=1, sticky = N+S+W+E)

    lbl_output_courses = Label(window, text="\nCourses:", bg="white", fg="red4", font="times 14 bold")
    lbl_output_courses.grid(row=4, column=1, sticky=W)
    output_courses = Text(window, width=35, height=6, wrap=WORD, bg="MistyRose2", bd=2)
    output_courses.grid(row=5, column=1, columnspan=1, sticky = N+S+W+E)

    lbl_output_job = Label(window, text="\nJob Information:", bg="white", fg="red4", font="times 14 bold")
    lbl_output_job.grid(row=6, column=0, sticky=W)
    output_job = Text(window, width=35, height=6, wrap=WORD, bg="MistyRose2", bd=2)
    output_job.grid(row=7, column=0, columnspan=1, sticky = N+S+W+E)

    lbl_output_postings = Label(window, text="\nCurrent Postings in Pittsburgh,PA", bg="white", fg="red4", font="times 14 bold")
    lbl_output_postings.grid(row=6, column=1,sticky=W)
    output_postings = Text(window, width=35, height=6, wrap=NONE, bg="MistyRose2", bd=2)
    output_postings.grid(row=7, column=1, columnspan=1, sticky = N+S+W+E)

    # Create an exit button
    def close_window():
        window.destroy()
        exit()

    Button(window, text="Exit", width=12, command=close_window, activebackground="gray70", font="times 10").grid(row=9, column=1, sticky=SE)

    window.mainloop()

###########################
# Do that thing
skill_builder_interface()
###########################
