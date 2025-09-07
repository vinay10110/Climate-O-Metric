import pandas as pd

# Read file, letting pandas recognize 'NaN' or blanks as missing
df = pd.read_csv("./global-data-on-sustainable-energy (1).csv", na_values=["NaN", "NULL", "NA"])

# Fill missing values with column means
df_filled = df.fillna(df.mean(numeric_only=True))

df_filled.to_csv("./global-data-on-sustainable-energy-preprocessed.csv", index=False)
