from ipumspy import readers
import pandas

# Paths
ddi_path = "./source/cps_00005.xml"
csv_path = "./source/cps_00005.csv"
cpi_path = "./source/cpi.csv"

avg_income_path = "./aggregate/avg_income.csv"
median_income_path = "./aggregate/median_income.csv"
std_income_path = "./aggregate/std_income.csv"
avg_income_ed_path = "./aggregate/avg_income_ed.csv"
median_income_ed_path = "./aggregate/median_income_ed.csv"
std_income_ed_path = "./aggregate/std_income_ed.csv"

avg_real_income_path = "./aggregate/avg_real_income.csv"
median_real_income_path = "./aggregate/median_real_income.csv"
std_real_income_path = "./aggregate/std_real_income.csv"
avg_real_income_ed_path = "./aggregate/avg_real_income_ed.csv"
median_real_income_ed_path = "./aggregate/median_real_income_ed.csv"
std_real_income_ed_path = "./aggregate/std_real_income_ed.csv"

gini_path = "./aggregate/gini.csv"
gini_ed_path = "./aggregate/gini_ed.csv"

total_survey_size_path = "./aggregate/total_survey_size.csv"
counts_ed_path = "./aggregate/counts_ed.csv"
proportions_ed_path = "./aggregate/proportions_ed.csv"

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

groupby_year = df.groupby("YEAR")
groupby_year_ed = df.groupby(["YEAR", "EDGROUP"])

# Calculations
avg_income = groupby_year["FTOTVAL"].mean()
median_income = groupby_year["FTOTVAL"].median()
std_income = groupby_year["FTOTVAL"].std()
avg_income_ed = groupby_year_ed["FTOTVAL"].mean()
median_income_ed = groupby_year_ed["FTOTVAL"].median()
std_income_ed = groupby_year_ed["FTOTVAL"].std()

avg_real_income = avg_income * cpi
median_real_income = median_income * cpi
std_real_income = std_income * cpi
avg_real_income_ed = avg_income_ed * cpi
median_real_income_ed = median_income_ed * cpi
std_real_income_ed = std_income_ed * cpi

total_survey_size = groupby_year.size()
counts_ed = groupby_year_ed.size()
proportions_ed = counts_ed / total_survey_size

gini_yearly = groupby_year["CUMULATIVE"].agg(gini)
gini_yearly_ed = groupby_year_ed["CUMULATIVE_ED"].agg(gini)

# Copying
avg_income.to_csv(avg_income_path)
median_income.to_csv(median_income_path)
std_income.to_csv(std_income_path)
avg_income_ed.to_csv(avg_income_ed_path)
median_income_ed.to_csv(median_income_ed_path)
std_income_ed.to_csv(std_income_ed_path)

avg_real_income.to_csv(avg_real_income_path)
median_real_income.to_csv(median_real_income_path)
std_real_income.to_csv(std_real_income_path)
avg_real_income_ed.to_csv(avg_real_income_ed_path)
median_real_income_ed.to_csv(median_real_income_ed_path)
std_real_income_ed.to_csv(std_real_income_ed_path)

total_survey_size.to_csv(total_survey_size_path)
counts_ed.to_csv(counts_ed_path)
proportions_ed.to_csv(proportions_ed_path)

gini_yearly.to_csv(gini_path)    
gini_yearly_ed.to_csv(gini_ed_path)