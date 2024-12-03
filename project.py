from ipumspy import readers
import pandas


ddi_path = "./cps_00001.xml"
csv_path = "./data.csv"

df = pandas.read_csv(csv_path)

avg_income = df.groupby("YEAR")["FTOTVAL"].mean()
std_income = df.groupby("YEAR")["FTOTVAL"].std()

def gini(series):
    total = series.iloc[series.shape[0] - 1]
    proportions = series/total

    equal_area = 0.5
    diff_area = 0
    
    delta = 1/proportions.shape[0]
    for i in range(proportions.shape[0]):
        percentile = (i + 1)/proportions.shape[0]
        diff_area += delta * (percentile - proportions.iloc[i])
    
    return diff_area / equal_area

gini_yearly = df.groupby("YEAR")["CUMULATIVE"].agg(gini)


print(f"AVERAGE INCOME: {avg_income}")
print(f"INCOME STDDEV: {std_income}")
print(f"INCOME STDDEV/AVG: {std_income/avg_income}")
print(f"GINI: {gini_yearly}")