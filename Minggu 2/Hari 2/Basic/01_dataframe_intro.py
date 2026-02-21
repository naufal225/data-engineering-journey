import pandas as pd

orders = [
    {"id":"1","amount":"15000","status":"PAID"},
    {"id":"2","amount":"20000","status":"FAILED"},
]

df = pd.DataFrame(orders)

print(df)

print("Columns:", df.columns)
print("Values:", df.values)

print(type(df["amount"]))

df["amount"] = df["amount"].str.replace(",","").astype(int)

print(type(df["amount"]))
print(type(df["amount"].str.replace(",","").astype(int)))

print(df[df["status"]=="PAID"])
print(df[df["status"]=="FAILED"])
print(df[df["amount"].str.replace(",","").astype(int)>15000])