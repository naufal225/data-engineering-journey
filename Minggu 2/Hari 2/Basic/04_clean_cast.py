import pandas as pd

df = pd.read_csv("orders_level2.csv")

df["status_clean"] = df["status"].astype(str).str.strip().str.upper()

country_map = {
    "ID":"INDONESIA", 
    "TH":"THAILAND"
}

df["country_clean"] = df["country"].astype(str).str.strip().str.upper()
df["country_clean"] = df["country_clean"].replace(country_map)

df["amount_clean"] = (
    df["amount"]
        .astype(str)
        .str.replace(",", "", regex=False)
        .str.replace(".", "", regex=False)
)

df["amount_clean"] = pd.to_numeric(df["amount_clean"], errors="coerce").astype("Int64")

dt1 = pd.to_datetime(df["created_at"], errors="coerce", dayfirst=True, format="mixed")
dt2 = pd.to_datetime(df["created_at"], errors="coerce", dayfirst=False, format="mixed")
# df["created_at_clean"] = dt1.fillna(dt2)
df["created_at_clean"] = pd.to_datetime(df["created_at"], errors="coerce", dayfirst=False, format="mixed")

print(df[["order_id", "amount", "amount_clean", "country", "country_clean", "status", "status_clean", "created_at", "created_at_clean"]])
print("\nDTYPES After Clean:")
print(df.dtypes)

# print("\n\n\n")

# df2 = pd.DataFrame({
#     "col1":["a","b","c","d"],
#     "col2":["a.",".","b.","cc"]
# })

# df2["col2lain"] = (
#     df2["col2"].astype(str)
#         .str.replace(".", "-")
# )

# df2["col3lain"] = (
#     df2["col2"].astype(str)
#         .replace(".", "-")
# )

# print(df2)