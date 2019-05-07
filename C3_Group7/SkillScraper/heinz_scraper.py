"""
@author: Jonathan Dyer

 NOTE
------
Must run the following commands in the appropriate conda env in order for this to work:

> conda install spacy
> python -m spacy download en
(second one must be run as admin)

Alternatively run the top command and then include the following in the code:
    import spacy
    import en_core_web_sm
    nlp = en_core_web_sm.load()
------
"""
# file: heinz_scraper.py
################################################################################
##################################  IMPORTS  ###################################
################################################################################
from urllib.request import urlopen
from bs4 import BeautifulSoup
import csv
import re
import spacy


################################################################################
############################### PRIVATE METHODS ################################
################################################################################
def _get_course_description(link):
    # Retrieve the html
    html = urlopen(link)
    soup = BeautifulSoup(html.read(), "lxml")

    # Recover the description text (cleaned)
    text = soup.find_all('p')[2].get_text()
    clean = text.replace('\n', '').replace('\r', '')
    clean =  re.sub(r'[^\w\s]', '', clean)
    return clean;


def _get_course_links():
    """
    Get a list of urls to Heinz College course description
    pages, so we can scrape each of those iteratively.

    Params
    -------
    skill_list
        A list of all the skills searched for in these pages

    Return
    -------
    <dict> {course_name: course_link, ...}
        course_name: string containing course name
        course_link: string containing link to course description page
    """
    print("Getting course links... ".ljust(35), end='')
    html_base = 'https://api.heinz.cmu.edu'
    html = urlopen('https://api.heinz.cmu.edu/courses_api/course_list/')
    soup = BeautifulSoup(html.read(), "lxml")

    names = []
    links = []

    # Each course link is contained in a <tr> element with class="clickable-row"
    course_rows = soup.findAll('tr', {'class': 'clickable-row'})
    for row in course_rows:
        td = row.findAll('td')
        num = td[0].string
        name = td[1].string
        names.append(num + ": " + name)
        links.append(html_base + row.get('data-href'))

    print("done.")
    return dict(zip(names, links))



# Main function that does all the work
def _map_skills(skills_list):
    """
    Returns a dict mapping each skill in the skill_list
    to a list of course names associated with that skill.
    """
    # first get the links for all Heinz courses
    course_dict = _get_course_links()
    course_descriptions = {}

    # then scrape the description text for each link
    print("Getting course descriptions...".ljust(35), end='')
    for name, link in course_dict.items():
        course_descriptions[name] = _get_course_description(link)
    print("done.")
#####################################################
# IF YOU CANNOT GET SPACY/NLP TO WORK:
#   Replace the next block with the following code.
#
# # we'll store the results in a new dictionary
# parsed_descriptions = course_descriptions.copy()
# for name, text in course_descriptions.items():
#     parsed_tokens = []
#
#     # remove all stopwords, punctuation, and spaces
#     for token in text.split(' '):
#         token = re.sub(r'[^\w\s]', '', token)
#         token = token.strip().lower()
#
#         if token not in ['the', 'a','as', 'and', 'an', '&', '-', 'for']:
#             parsed_tokens.append(token)
#
#     # finally add list to dictionary
#     parsed_descriptions[name] = ' '.join(parsed_tokens)
#####################################################

    # time for a little nlp (to lemmatize the descriptions)
    # can replace both of the following lines with  nlp = spacy.load('en')
    # import en_core_web_sm
    # nlp = en_core_web_sm.load()
    print("Loading NLP model...".ljust(35), end='')
    nlp = spacy.load('en')
    print("done.")

    print("Parsing course descriptions...".ljust(35), end='')
    # we'll store the results in a new dictionary
    parsed_descriptions = {}
    for name, text in course_descriptions.items():
        parsed_text = nlp(text)
        parsed_tokens = []

        # remove all stopwords, punctuation, and spaces
        for token in parsed_text:
            lemma = token.lemma_.lower()
            if not (nlp.vocab[lemma].is_stop or token.pos_ == 'PUNCT' or token.pos_ == 'SPACE'):
                parsed_tokens.append(lemma)

        # finally add parsed text to dictionary
        parsed_descriptions[name] = parsed_tokens
    print("done.")
#####################################################

    # now we can iterate through the skills list and build our final dictionary
    # give each skill its own list
    skills_to_courses = { k : [] for k in skills_list }

    print("Matching skills to courses...".ljust(35), end='')
    for skill in skills_list:
        # now check every course for that skill
        for course_name in parsed_descriptions.keys():
            # if that skill appears in the description, add to the map
            if len(skill.split(' ')) > 1:   # handle multi-word skills
                skillwords = skill.strip().lower().split(' ')
                if set(skillwords).issubset(parsed_descriptions[course_name]):
                    # print("Match:", skill, course_name)
                    skills_to_courses[skill].append(course_name)

            else:
                if skill.strip().lower() in parsed_descriptions[course_name]:
                    # print("Match:", skill, course_name)
                    skills_to_courses[skill].append(course_name)

    # return the final mapping, but only the nonempty elements
    print("done.")
    return { key : val for key, val in skills_to_courses.items() if val }



################################################################################
################################ PUBLIC METHODS ################################
################################################################################
def get_full_skill_map():
    import csv
    try:        # check to see if we've already done the scraping work
        skill_map = read_from_csv()
        return skill_map

    except:     # if not then start the process anew
        print("Scraping skills from Payscale...".ljust(35), end='')
        # read in the skills scraped from payscale, cleaned by the match_indeed_to_skill module
        import match_indeed_to_skill as mi
        all_skills = mi.get_skill_list()
        # remove leading and trailing spaces for every skill in all skills
        all_skills = [x.strip() for x in all_skills]
        print("done.")

        print("\nScraping course website:")
        print("------------------------")
        results = _map_skills(all_skills)
        print("------------------------")

        write_to_csv(results)
        return results


def get_full_skill_map_from_list(all_skills):
    import csv
    try:        # check to see if we've already done the scraping work
        skill_map = read_from_csv()
        return skill_map

    except:     # if not then start the process anew
        # remove leading and trailing spaces for every skill in all skills
        print("\nScraping course website:")
        print("------------------------")
        results = _map_skills(all_skills)
        print("------------------------")

        write_to_csv(results)
        return results


def get_skill_map(sub_list):
# Tests if an output file called heinz_skills_courses.csv is present in the directory,
# if not, it writes the file - a full mapping of skills and heinz courses.
#
# Either way returns a dictionary {str: list} with the required info.
    import csv
    try:        # check to see if we've already done the scraping work
        full_skill_map = read_from_csv()
        sub_skill_map = {}
        for k in sub_list:
            v = full_skill_map.get(k)
            if v:
                sub_skill_map[k] = v

        return sub_skill_map

    except:     # if not then start the process anew
        print("\nScraping course website:")
        print("------------------------")
        results = _map_skills(sub_list)
        print("------------------------")
        return results


### DEPRECATED ###
def get_skill_map_pandas(skill_list):
# Tests if an output file called heinz_skills_courses.csv is present in the directory,
# if not, it writes the file - a full mapping of skills and heinz courses.
#
# Either way returns a pandas dataframe with the required info.
    import pandas as pd

    try:
        pd.read_csv('./data/heinz_skills_courses.csv', header=None)
    except:
        results = pd.DataFrame(get_skill_map(all_skills))
        write_to_csv(results)


# Helper function to read a dictionary of form {str: list} from csv
def read_from_csv():
    with open('./data/heinz_skills_courses.csv', mode='r', newline='') as csvfile:
        print("Reading csv...".ljust(20), end='')
        csvreader = csv.reader(csvfile, delimiter=',')
        skill_map = {}
        for row in csvreader:
            skill_map[row[0]] = row[1:]

    print("done.")
    return skill_map


# Helper function to write a dictionary of form {str: list} to csv
def write_to_csv(skill_map):
    with open('./data/heinz_skills_courses.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        for name, li in skill_map.items():
            entry = [name] + li
            writer.writerow(entry)


################################################################################
################################# MAIN METHOD ##################################
################################################################################
# little test function
if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        test_list = sys.argv[1:]
    else:
        # results = get_skill_map(['management', 'accounting', 'soft skills'])
        results = get_full_skill_map()

        for i in results.items():
            print(i)

        write_to_csv(results)
