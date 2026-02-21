import pandas as pd

df = pd.read_csv("orders_level2.csv")

print("=== SELECT COLUMNS ===")
print(df[["order_id", "amount", "status"]].head())

print("\n=== BOOLEAN FILTER (exact match) ===")
print(df[df["status"] == "PAID"])

print("\n=== BOOLEAN FILTER (contains) ===")
print(df[df["status"].str.contains("PAID", case=False, na=False)])

print("\n=== COMPOUND FILTER ===")
print(df[df["amount"] == "20000"])

print("\n=== SELECT USING .loc ===")
print(df.loc[df["status"].str.contains("PAID", case=False, na=False), ["order_id", "amount", "country"]])