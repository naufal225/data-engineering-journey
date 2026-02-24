import requests
import pandas as pd
from pathlib import Path

OUT = Path("output")
OUT.mkdir(exist_ok=True)

def fecth_json(url:str):
    r = requests.get(url=url, timeout=10)
    r.raise_for_status()
    return r.json()

users = fecth_json("https://jsonplaceholder.typicode.com/users")
posts = fecth_json("https://jsonplaceholder.typicode.com/posts")

df_users = pd.DataFrame(users)
df_posts = pd.DataFrame(posts)

df_users.to_csv(OUT / "users.csv", index=False)
df_posts.to_csv(OUT / "posts.csv", index=False)

print("users shaved:", df_users.shape)
print("posts shaved:", df_posts.shape)

print("saved:", OUT / "users.csv", "and", OUT / "posts.csv")