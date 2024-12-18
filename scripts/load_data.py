import pandas
from ipumspy import readers, ddi

"""
CPS_00001 ranges from [1962 - 1989] and contains data on [EDUCATION] and [FAMILY INCOME].
1962 and 1963 incomes are not available in the data.
CPS_00003 ranges from [1962 - 1999] and contains data on [EDUCATION] and [FAMILY INCOME].
1962 and 1963 incomes are not available in the data.
1992 - 1999 educations are not available in the data.
CPS_00005 ranges from [1962 - 1999] and contains data on [EDUCATION] and [FAMILY INCOME].
1962 and 1963 incomes are not available in the data.
"""

data_path = "./source/cps_00005.dat"
ddi_path = "./source/cps_00005.xml"
csv_path = "./source/cps_00005.csv"

# Utility functions
def get_years_schooling_higrade(code):
    # Based on IPUMS USA's HIGRADE variable codes.
    # completed 1st grade = 1 year of schooling, 2nd grade = 2 years...
    # does not count anything before 1st grade
    # stops counting additiona years beyond 8th year of college (20 years of schooling)
    return max(0, code // 10 - 3)

def get_education_group_higrade(code):
    # Based on IPUMS USA's HIGRADE variable codes.
    # 0 = No school
    # 1 = Completed elementary school (1st-5th grade)
    # 2 = Completed middle school (6th-8th grade)
    # 3 = Completed high school (9th-12th grade)
    # 4 = Completed 4 years of college (13-16 yrs school)
    # 5 = Completed 5+ years of college (17+ yrs school)
    years = get_years_schooling_higrade(code)
    if years == 0:
        return 0
    if 1 <= years <= 5:
        return 1
    if 6 <= years <= 8:
        return 2
    if 9 <= years <= 12:
        return 3
    if 13 <= years <= 16:
        return 4
    return 5

def get_education_group_educ(code):
    # Based on IPUMS USA's EDUC code. 
    # 0 = No school
    # 1 = Completed 1-4 years of school (1st-4th grade)
    # 2 = Completed 5-8 years of school (5th-8th grade)
    # 3 = Completed 9-12 years of school (9th-12th grade)
    #     OR high school diploma/equivalent
    # 4 = Completed 13-16 years of school (1-4 years college)
    # 5 = Completed 17+ years of school (5+ years college)
    if 0 <= code <= 2:
        return 0
    if 10 <= code <= 14:
        return 1
    if 20 <= code <= 32:
        return 2
    if 40 <= code <= 73:
        return 3
    if 80 <= code <= 111:
        return 4
    if 120 <= code <= 125:
        return 5
    if code == 999:
        return None

print("Reading DDI")
ddi = readers.read_ipums_ddi(ddi_path)
print("Finished reading DDI.\nReading Data")
df = readers.read_microdata(ddi, data_path)
print("Finished reading Data.")

# filter out people with invalid income/unknown education
df = df[df["FTOTVAL"] != 9999999999]
df = df[df["EDUC"] != 999]

df = df.sort_values(by=["YEAR", "FTOTVAL"], ascending=[True, True]).reset_index(drop=True)
df["CUMULATIVE"] = df.groupby("YEAR")["FTOTVAL"].cumsum()
df["EDGROUP"] = df["EDUC"].apply(get_education_group_educ)

df["CUMULATIVE_ED"] = df.groupby(["YEAR", "EDGROUP"])["FTOTVAL"].cumsum()

df.to_csv(csv_path, index=False)