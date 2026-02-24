import pandas as pd
from pathlib import Path

OUT = Path("output")
OUT.mkdir(exist_ok=True)

# get data
df = pd.read_csv(OUT / "joined.csv")

top_users = (
    df.groupby("user_name")["post_id"]
        .count()
        .sort_values(ascending=False)
        .head(3)
)

avg_title_length = df["title_length"].mean()

top_users2 = (
    df.groupby("user_name")["body_length"].mean()
        .sort_values(ascending=False)
        .head(3)
)

# Metrics
lines = []
lines.append("=== API Ingestion -> Join -> Analytics ===\n")

lines.append("1). Top 3 users by number of posts:")
for name, cnt in top_users.items():
    lines.append(f"- name: {name}, {int(cnt)} posts")
    
lines.append("\n2). Average title lenght overall:")
lines.append(f"- {avg_title_length:.2f} characters")

lines.append("\n3). Top 3 users by average body length:")
for name, cnt in top_users2.items():
    lines.append(f"- name: {name}, {int(cnt)} characters")

metrics_path = OUT / "metrics.txt"
metrics_path.write_text("\n".join(lines), encoding="utf-8")

print("saved:", metrics_path)
print("preview:\n".join(lines[::10]))

