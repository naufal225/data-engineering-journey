import pandas as pd
import requests

def fetch_request(url:str):
    r = requests.get(url=url, timeout=10)
    r.raise_for_status()
    return r.json()

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
    
def join(df1: pd.DataFrame, df2: pd.DataFrame, on: str, how="left"):
    return df1.merge(df2, on=on, how=how)

def validate(df: pd.DataFrame):
    assert len(df) == 100, f"Expected 100 rows, got {len(df)}"
    assert df["post_id"].notna().all(), "post id cannot be null"
    assert df["user_id"].notna().all(), "user id cannot be null"
    assert df["body_length"].notna().all(), "body length cannot be null"
    assert df["title_length"].notna().all(), "title length cannot be null"

users = fetch_request("https://jsonplaceholder.typicode.com/users")
posts = fetch_request("https://jsonplaceholder.typicode.com/posts")

df_users = pd.DataFrame(users)
df_posts = pd.DataFrame(posts)

# normalize

df_users = normalize_users(df_users)
df_posts = normalize_posts(df_posts)

# join

df_joined = join(df_users[["user_id", "user_name", "user_email"]], df_posts, on="user_id", how="left")

df_joined["body_length"] = df_joined["body"].astype(str).str.len()
df_joined["title_length"] = df_joined["title"].astype(str).str.len()

# validation

validate(df_joined)

# to list of tuples

data = list(df_joined.itertuples(name=None, index=False))

for i,v in enumerate(data):
    print(v)
    # mau lakuin query disini