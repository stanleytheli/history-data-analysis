from ipumspy import readers
import pandas

# Paths
ddi_path = "./source/cps_00003.xml"
csv_path = "./source/cps_00003.csv"
cpi_path = "./source/cpi.csv"

avg_income_path = "./aggregate/avg_income.csv"
std_income_path = "./aggregate/std_income.csv"
avg_income_ed_path = "./aggregate/avg_income_ed.csv"
std_income_ed_path = "./aggregate/std_income_ed.csv"

avg_real_income_path = "./aggregate/avg_real_income.csv"
std_real_income_path = "./aggregate/std_real_income.csv"
avg_real_income_ed_path = "./aggregate/avg_real_income_ed.csv"
std_real_income_ed_path = "./aggregate/std_real_income_ed.csv"

gini_path = "./aggregate/gini.csv"

# Utility functions
def get_years_schooling(code):
    # Based on IPUMS USA's HIGRADE variable codes.
    # completed 1st grade = 1 year of schooling, 2nd grade = 2 years...
    # does not count anything before 1st grade
    # stops counting additiona years beyond 8th year of college (20 years of schooling)
    return max(0, code // 10 - 3)

def get_education_group(code):
    # Based on IPUMS USA's HIGRADE variable codes.
    # 0 = No school
    # 1 = Completed elementary school (1st-5th grade)
    # 2 = Completed middle school (6th-8th grade)
    # 3 = Completed high school (9th-12th grade)
    # 4 = Completed 4 years of college (13-16 yrs school)
    # 5 = Completed 5+ years of college (17+ yrs school)
    years = get_years_schooling(code)
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

def gini(series):
    # Calculates the Gini Coefficient given a series of cumulative incomes
    total = series.iloc[series.shape[0] - 1]
    proportions = series/total

    equal_area = 0.5
    diff_area = 0
    
    delta = 1/proportions.shape[0]
    for i in range(proportions.shape[0]):
        percentile = (i + 1)/proportions.shape[0]
        diff_area += delta * (percentile - proportions.iloc[i])
    
    return diff_area / equal_area

df = pandas.read_csv(csv_path).set_index("YEAR")
cpi = pandas.read_csv(cpi_path).set_index("YEAR").iloc[:, 0]

df["EDGROUP"] = df["HIGRADE"].apply(get_education_group)
groupby_year = df.groupby("YEAR")
groupby_year_ed = df.groupby(["YEAR", "EDGROUP"])

# Calculations
avg_income = groupby_year["FTOTVAL"].mean()
std_income = groupby_year["FTOTVAL"].std()
avg_income_ed = groupby_year_ed["FTOTVAL"].mean()
std_income_ed = groupby_year_ed["FTOTVAL"].std()

avg_real_income = avg_income * cpi
std_real_income = std_income * cpi
avg_real_income_ed = avg_income_ed * cpi
std_real_income_ed = std_income_ed * cpi

gini_yearly = groupby_year["CUMULATIVE"].agg(gini)

# Copying
avg_income.to_csv(avg_income_path)
std_income.to_csv(std_income_path)
avg_income_ed.to_csv(avg_income_ed_path)
std_income_ed.to_csv(std_income_ed_path)

avg_real_income.to_csv(avg_real_income_path)
std_real_income.to_csv(std_real_income_path)
avg_real_income_ed.to_csv(avg_real_income_ed_path)
std_real_income_ed.to_csv(std_real_income_ed_path)

gini_yearly.to_csv(gini_path)