import pandas as pd
from pathlib import Path

OUT = Path("output")
OUT.mkdir(exist_ok=True)

# get data
df = pd.read_csv(OUT / "joined.csv")

assert len(df) == 100, f"Expected 100 rows, got {len(df)}"
assert df["user_name"].notna().all(), "Found null in user name"
assert df["post_id"].notna().all(), "Found null in post id"
assert df["body_length"].notna().all(), "Found null in body"
assert df["title_length"].notna().all(), "Found null in title"

# print(df)

top_users = (
    df.groupby("user_name")["post_id"]
        .count()
        .reset_index(name="post_count")
        .sort_values(["post_count", "user_name"], ascending=[False, True])
        .head(3)
)

print(top_users)

avg_title_length = df["title_length"].mean()

top_users2 = (
    df.groupby("user_name")["body_length"].mean()
        .reset_index(name="avg_body_length")
        .sort_values(["avg_body_length", "user_name"], ascending=[False, True])
        .head(3)
)

print(top_users2)

# Metrics
lines = []
lines.append("\n=== API Ingestion -> Join -> Analytics ===\n")

lines.append("\n1). Top 3 users by number of posts:")
for _, row in top_users.iterrows():
    lines.append(f"- name: {row['user_name']}, {int(row['post_count'])} posts")
    
lines.append("\n2). Average title length overall:")
lines.append(f"- {avg_title_length:.2f} characters")

lines.append("\n3). Top 3 users by average body length:")
for _, row in top_users2.iterrows():
    lines.append(f"- name: {row['user_name']}, {row['avg_body_length']:.2f} characters")

metrics_path = OUT / "metrics.txt"
metrics_path.write_text("\n".join(lines), encoding="utf-8")

print("saved:", metrics_path)
print("preview:\n".join(lines[:10]))

