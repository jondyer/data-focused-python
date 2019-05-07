# read in bls_data_frame module
import bls_data_frame as b
# read in the match_indeed_to_skill module
import match_indeed_to_skill as mi
# read in the heinz_scraper module
import heinz_scraper as hs

# Get DF of BLS with Data
df_bls = b.get_df_bls()

# Get full list of BLS-tracked jobs
job_list = b.get_job_list(df_bls)

# Get full list of Payscale.com tracked skills
skill_list = mi.get_skill_list()

# Get DF of number of jobs returned for a given job search from the BLS job_list
job_df = mi.scrape_pages('Financial Analysts','Pittsburgh','PA',skill_list)

# Get count of job skills for the searched job
job_skill_count = mi.return_job_count(skill_list,job_df)

# Get skill_map
skill_map = hs.get_skill_map(job_skill_count["Skill"].values)

for i in skill_map.items():
    print(i)
