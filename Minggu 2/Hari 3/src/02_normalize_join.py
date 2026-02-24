import pandas as pd
from pathlib import Path

OUT = Path("output")
OUT.mkdir(exist_ok=True)

def load_raw():
    return pd.read_csv(OUT / "users.csv"), pd.read_csv(OUT / "posts.csv")

def normalize_users(df: pd.DataFrame):
    return df.rename(columns={
    "id":"user_id",
    "name":"user_name",
    "email":"user_email"
})
    
def normalize_posts(df: pd.DataFrame):
    return df.rename(columns={
    "id":"post_id",
    "userId":"user_id"
})
    
def join_data(df1: pd.DataFrame, df2: pd.DataFrame, on: str, how="inner"):
    return df1.merge(df2, on=on, how=how)
    
def validate_join(df: pd.DataFrame):
    assert len(df) == 100, f"Join rows expected 100, got {len(df)}"
    assert df["user_name"].notna().all(), "Found null user_name after join"
    assert df["user_email"].notna().all(), "Found null user_email after join"

df_users, df_posts = load_raw()
    
df_users = normalize_users(df_users)

df_posts = normalize_posts(df_posts)

df = join_data(df_posts, (df_users[["user_id","user_name","user_email"]]), on="user_id", how="left")

df["title_length"] = df["title"].astype(str).str.len()
df["body_length"] = df["body"].astype(str).str.len()

validate_join(df)

df.to_csv(OUT / "joined.csv", index=False)

print("joined shape:", df.shape)
print("joined:", OUT / "joined.csv")
print(df.head())
