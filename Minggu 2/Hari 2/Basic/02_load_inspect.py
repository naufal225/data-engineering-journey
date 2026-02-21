import pandas as pd

df = pd.read_csv("orders.csv")

print("\nDATA:")
print(df)

print("\nHEAD(n), default 5:")
print(df.head())

print("\nINFO()")
df.info()

# Kalau mau lebih cepat pakai:

print("\nDTYPES:")
print(df.dtypes)

print("\nSHAPE:")
print(df.shape)

print("\nCOLUMNS()")
print(df.columns)

print("\nSimple Values Per Column")

for col in df.columns:
    print(col,":",df[col].unique()[:5])
    
print("\nNull Count Per Column")
print(df.isna().sum())

print("Total:", df.isna().sum().sum())

print("\nMemory Usage (bytes)")
print(df.memory_usage())
print("Total:", df.memory_usage().sum(), "bytes")

# Sortir Kolom

print("\nSortir Kolom")
categorical = df.select_dtypes(include="object").columns
numerical = df.select_dtypes(exclude="object").columns

print("Categorical:",categorical)
print("Numerical:",numerical)