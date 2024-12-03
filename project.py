from ipumspy import readers
import pandas


ddi_path = "./cps_00001.xml"

csv_path = "./data.csv"
df = pandas.read_csv(csv_path)

avg_income = df.groupby("YEAR")["FTOTVAL"].mean()
std_income = df.groupby("YEAR")["FTOTVAL"].std()

# calculate gini income coefficient...?

print(f"AVERAGE INCOME: {avg_income}")
print(f"INCOME STDDEV: {std_income}")
print(f"INCOME STDDEV/AVG: {std_income/avg_income}")


#print(f"DataFrame shape: {df.shape}")
#print(f"First elements: {df.iloc[0:20, :]}") 