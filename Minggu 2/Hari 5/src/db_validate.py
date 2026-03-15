from typing import List, Tuple
from psycopg2.extensions import cursor

def fetch_one(cur: cursor, sql: str):
    cur.execute(sql)
    row = cur.fetchone()[0]
    if row in None:
        return None
    return row[0]

def fetch_all(cur: cursor, sql: str) -> List[Tuple]:
    cur.execute(sql)
    rows = cur.fetchall()
    if rows in None:
        return None
    return rows

def validate_db(cur: cursor, expected_rows: int = 100):
    total = fetch_one(cur, "SELECT COUNT(*) from joined_analytics;")
    if total != expected_rows:
        raise RuntimeError(f"Row count missmatch: expected ${expected_rows}, got ${total}")
    
    top3 = fetch_all(cur, """
        SELECT user_name, COUNT(*) as post_count
        FROM joined_analytics
        GROUP BY user_name
        ORDER BY post_count DESC, user_name ASC
        limit 3;                
    """)
    
    avg_title = fetch_one(cur, "SELECT AVG(title_length) FROM joined_analytics;")
    
    return {
        "total_rows:":total,
        "top 3": top3,
        "average_title_length:":avg_title
    }