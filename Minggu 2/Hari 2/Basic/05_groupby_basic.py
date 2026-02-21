import pandas as pd

df = pd.read_csv("orders_level2.csv")

df["status_clean"] = df["status"].astype(str).str.strip().str.upper()

country_map = {
    "ID":"INDONESIA",
    "TH":"THAILAND",
    "MALAYSIA":"MALAYSIA",
    "THAILAND":"THAILAND",
    "SINGAPORE":"SINGAPORE",
    "INDONESIA":"INDONESIA"
}

df["country_clean"] = df["country"].astype(str).str.strip().str.upper()
df["country_clean"] = df["country_clean"].map(country_map).fillna("UNKNOWN")

df["amount_clean"] = (
    df["amount"].astype(str)
    .str.replace(",","")
    .str.replace(".","")
)

df["amount_clean"] = pd.to_numeric(df["amount_clean"], errors="coerce").astype("Int64").fillna(0)

s = df["created_at"].astype(str)
dt1 = pd.to_datetime(s, errors="coerce", dayfirst=False, format="mixed")
dt2 = pd.to_datetime(s, errors="coerce", dayfirst=True, format="mixed")

df["created_at_clean"] = dt1.fillna(dt2)

valid = df[(df["amount_clean"].notna()) & (df["amount_clean"] > 0)]

print("\n=== Revenue By Status (PAID Only vs All Statusses) ===")

req_by_status = (
    valid.groupby("status_clean")["amount_clean"]
        .sum()
        .sort_values(ascending=False)
)

print(req_by_status)

print("\n=== Revenue By Country ===")

rev_by_country = (
    valid.groupby("country_clean")["amount_clean"]
        .sum()
        .sort_values(ascending=False)
)

print(rev_by_country)

print("\n=== Monthly Revenue Trend (PAID Only) ===")
 
paid = valid[valid["status_clean"] == "PAID"].copy()
paid["order_month"] = paid["created_at_clean"].dt.to_period('M').astype(str)

monthly = (
    paid.groupby("order_month")["amount_clean"]
        .sum()
        .sort_values(ascending=False)
)

print(monthly)

print("\n=== Sanity Check ===")
print("Total valid rows:", len(valid))
print("Total paid rows:", len(paid))
print("Total paid revenue:", int(paid["amount_clean"].sum()))
