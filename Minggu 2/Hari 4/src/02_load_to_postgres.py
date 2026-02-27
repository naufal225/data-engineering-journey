import pandas as pd
import requests
import psycopg2
from psycopg2.extras import execute_values
import os

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

# connect postgres

conn = psycopg2.connect(
    host=os.getenv("PGHOST", "localhost"),
    port=os.getenv("PGPORT", "5432"),
    database=os.getenv("PGDATABASE", "praktek_etl_simpel"),
    user=os.getenv("PGUSER", "postgres"),
    password=os.getenv("PGPASSWORD", "nma225")
)

conn.autocommit = False

try:
    with conn.cursor() as cur:
        cols = ["post_id", "user_id", "user_name", "user_email", "title_length", "body_length"]
        rows = list(df_joined[cols].itertuples(name=None, index=False))
        
        sql = f"""
        INSERT INTO joined_analytics ({",".join(cols)})
        VALUES %s
        ON CONFLICT (post_id) DO UPDATE SET
            user_id = EXCLUDED.user_id,
            user_name = EXCLUDED.user_name,
            user_email = EXCLUDED.user_email,
            title_length = EXCLUDED.title_length,
            body_length = EXCLUDED.body_length;
        """
        
        execute_values(cur, sql, rows, page_size=1000)
        
        cur.execute("SELECT COUNT(*) FROM joined_analytics;")
        total = cur.fetchone()[0]
        
        cur.execute("""
                    SELECT user_name, COUNT(*) as post_count
                    FROM joined_analytics
                    GROUP BY user_name
                    ORDER BY post_count DESC, user_name ASC
                    LIMIT 3;
                    """)
        
        top3 = cur.fetchall()
        
    conn.commit()
    
    print("Inserted/Upserted rows:", len(df_joined))
    print("Total:",total)
    print("Top 3:", top3)
except Exception as e:
    conn.rollback()
    raise
finally:
    conn.close()