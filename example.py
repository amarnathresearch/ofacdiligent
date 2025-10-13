import pandas as pd

url = "https://www.treasury.gov/ofac/downloads/sdn.csv"
sdn = pd.read_csv(url, encoding="latin1")

# Inspect columns
print(sdn.columns)

# Example search
name_to_search = "Tesla"
# After inspecting columns, adjust the column you search in, e.g., 'LASTNAME' or 'NAME'
matches = sdn[sdn['LASTNAME'].str.contains(name_to_search, case=False, na=False)]
print(matches)
