from ipumspy import readers
import pandas


ddi_path = "./source/cps_00001.xml"
csv_path = "./source/cps_00001.csv"
cpi_path = "./source/cpi.csv"

avg_income_path = "./aggregate/avg_income.csv"
std_income_path = "./aggregate/std_income.csv"
avg_income_ed_path = "./aggregate/avg_income_ed.csv"
std_income_ed_path = "./aggregate/std_income_ed.csv"
gini_path = "./aggregate/gini.csv"

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

df = pandas.read_csv(csv_path)
cpi = pandas.read_csv(cpi_path)

df["EDGROUP"] = df["HIGRADE"].apply(get_education_group)
groupby_year = df.groupby("YEAR")
groupby_year_ed = df.groupby("YEAR", "EDGROUP")

avg_income = groupby_year["FTOTVAL"].mean()
std_income = groupby_year["FTOTVAL"].std()
avg_income_education = groupby_year_ed["FTOTVAL"].mean()
std_income_education = groupby_year_ed["FTOTVAL"].std()
gini_yearly = groupby_year["CUMULATIVE"].agg(gini)

avg_income.to_csv(avg_income_path)
std_income.to_csv(std_income_path)
avg_income_education.to_csv(avg_income_ed_path)
std_income_education.to_csv(std_income_ed_path)
gini_yearly.to_csv(gini_path)

#print(f"AVERAGE INCOME: {avg_income}")
#print(f"INCOME STDDEV: {std_income}")
#print(f"INCOME STDDEV/AVG: {std_income/avg_income}")
#print(f"GINI: {gini_yearly}")