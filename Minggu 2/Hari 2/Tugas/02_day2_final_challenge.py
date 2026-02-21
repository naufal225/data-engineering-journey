import pandas as pd

# Ambil data
df = pd.read_csv("../Basic/orders_level2.csv")

# Cleaning amount
df["amount_clean"] = (
    df["amount"].astype(str)
        .str.replace(",", "", regex=False)
        .str.replace(".", "", regex=False)
)

df["amount_clean"] = pd.to_numeric(df["amount_clean"], errors="coerce").astype("Int64")

# Cleaning status (PAID, FAILED, REFUNDED)
df["status_clean"] = df["status"].astype(str).str.strip().str.upper()

# Cleaning country
country_map = {
    "INDONESIA":"INDONESIA",
    "ID":"INDONESIA",
    "TH":"THAILAND",
    "THAILAND":"THAILAND",
    "MALAYSIA":"MALAYSIA",
    "SINGAPORE":"SINGAPORE",
}

df["country_clean"] = df["country"].astype(str).str.strip().str.upper()

df["country_clean"] = df["country_clean"].map(country_map).fillna("UNKNOWN")

# Cleaning created_at
df["is_ambigouos"] = df["created_at"].astype(str).str.match(r"^\d{2}/\d{2}/\d{4}$")

ambigouos = df[df["is_ambigouos"]].copy()
non_ambigouos = df[~df["is_ambigouos"]].copy()

ambigouos["created_at_clean"] = pd.to_datetime(ambigouos["created_at"], format="%m/%d/%Y", errors="coerce")
non_ambigouos["created_at_clean"] = pd.to_datetime(non_ambigouos["created_at"], format="mixed", errors="coerce")

df = pd.concat([ambigouos, non_ambigouos]).sort_index()

print(df[["created_at", "created_at_clean", "is_ambigouos"]])
print(ambigouos)
print(non_ambigouos)

# Valid
valid = df[(df["amount_clean"].notna()) & (df["amount_clean"] > 0)]

# Revenue
revenue = valid[(valid["status_clean"] == "PAID")]["amount_clean"].sum()

# Paid
paid = valid[valid["status_clean"] == "PAID"].copy()

# Order month
assert paid["created_at_clean"].notna().all()
paid["order_month"] = paid["created_at_clean"].dt.to_period("M").astype(str)

# Country
top_countries = (
    paid.groupby("country_clean")["amount_clean"]
        .sum()
        .sort_values(ascending=False)
)

# Monthly
monthly = (
    paid.groupby("order_month")["amount_clean"]
        .sum()
        .sort_values(ascending=False)
)

# Clean data summary
print("\n=== Clean Data Summary ===")
print("Total rows:", len(df))
print("Total paid transactions:", len(paid))

# Metrics
print("\n=== Metrics ===")
print("Total paid revenue:", revenue)
print("Top country:", top_countries.index[0], int(top_countries.iloc[0]))
print("Monthly revenue:")
print(monthly)
