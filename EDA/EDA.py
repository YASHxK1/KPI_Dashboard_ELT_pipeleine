import pandas as pd 
import numpy as np

# Read StoreSales.json\StoreSales.json
df = pd.read_json('StoreSales.json\\StoreSales.json')

# Display basic information about the dataset
print("Dataset Shape:", df.shape)
print("\nFirst few rows:")
print(df.head())
print("\nColumn names:")
print(df.columns.tolist())
print("\nData types:")
print(df.dtypes)
print("\nBasic statistics:")
print(df.describe())