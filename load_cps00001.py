import pandas
from ipumspy import readers, ddi

"""
CPS_0001 ranges from [1962 - 1989] and contains data on [EDUCATION] and [FAMILY INCOME].
1962 and 1963 incomes are not available in the data.
"""

data_path = "./cps_00001.dat"
ddi_path = "./cps_00001.xml"
csv_path = "./data.csv"

print("Reading DDI")
ddi = readers.read_ipums_ddi(ddi_path)
print("Finished reading DDI.\nReading Data")
df = readers.read_microdata(ddi, data_path)
print("Finished reading Data.")

# filter out people with invalid income
df = df[df["FTOTVAL"] != 9999999999]

df["CUMULATIVE"] = 0

def compute_cumulatives(df, year_title, income_title, cumulative_title):
    # Calculates "cumulative incomes" for each year and adds them onto the DataFrame
    # Cumulative income is the total income of everyone who makes less than you
    # Used for calculating Gini Coefficient
    # Assumes DataFrame already has a column cumulative_title

    print("Beginning sorting")
    df = df.sort_values(by=[year_title, income_title], ascending=[True, True]).reset_index(drop=True)
    print("Sorting done")
    last_year = 0
    last_cumulative = 0
    for i in range(df.shape[0]):
        row = df.iloc[i, :]
        year = row[year_title]
        income = row[income_title]
        if (year != last_year):
            last_year = year
            last_cumulative = 0
        else:
            df.loc[i, cumulative_title] = last_cumulative
        last_cumulative += income
        print(f"{round(i/df.shape[0] * 10000) / 100}% done with computing cumulatives")
    return df

df = compute_cumulatives(df, "YEAR", "FTOTVAL", "CUMULATIVE")

df.to_csv(csv_path, index=False)