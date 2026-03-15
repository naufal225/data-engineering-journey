import time
from pathlib import Path
import pandas as pd
import psycopg2
from psycopg2.extensions import cursor
from psycopg2.extras import execute_values
from dotenv import load_dotenv

from logger import build_logger
from config import PgConfig
from db_validate import validate_db

BASE_DIR = Path(__file__).parent.parent
INPUT_PATH = BASE_DIR / "input" / "joined.csv"
LOG_PATH = BASE_DIR / "output" / "etl_run.log"

REQUIRED_COLS = {
    "post_id", "user_id", "user_name", "user_email",
    "title_length", "body_length"
}

def load_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"Input file not found: ${path}")
    return pd.read_csv(path)

def validate_df(df: pd.DataFrame):
    missing = REQUIRED_COLS - set(df.columns)
    if missing:
        raise RuntimeError(f"Missing required columns: ${sorted(missing)}")
    
    if df["post_id"].isna().any():
        raise RuntimeError("Found null post_id")
    if df["user_id"].isna().any():
        raise RuntimeError("Found null user_id")
    if df["user_name"].isna().any():
        raise RuntimeError("Found null user_name")
    if df["user_email"].isna().any():
        raise RuntimeError("Found null user_email")
    
    if df["post_id"].duplicated().any():
        dup_count = int(df["post_id"].duplicated().sum())
        raise RuntimeError(f"Found duplicate post id: ${dup_count}")
    
def upsert_joined(cur: cursor, df: pd.DataFrame):
    cols = ["post_id", "user_id", "user_name", "user_email", "title_length", "body_length"]
    rows = list(df[cols].itertuples(index=False, name=None))
    
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
    return len(rows)
    
def main():
    logger = build_logger(LOG_PATH)
    start = time.time()
    
    logger.info("ETL Start")
    try:    
        load_dotenv()
        cfg = PgConfig.from_env()
    except Exception as e:
        logger.exception("Exception while load config: %s", e)
        raise
        
    logger.info("Config loaded: %s", cfg.safe_str())

    df = load_csv(INPUT_PATH)
    logger.info("Loaded CSV: %s | rows = %d cols= %s", INPUT_PATH, len(df), len(df.columns)) 
    
    validate_df(df=df)
    logger.info("Dataframe validation: OK")
    
    conn = psycopg2.connect(
        host=cfg.host,port=cfg.port,dbname=cfg.dbname,user=cfg.user,password=cfg.password
    )   
    
    conn.autocommit = False
    
    try:
        with conn.cursor() as cur:
            logger.info("DB connected")
            
            inserted = upsert_joined(cur, df)
            logger.info("Upsert completed | rows=%d", inserted)
            
            results = validate_db(cur, expected_rows=len(df))
            logger.info("DB validation OK | total_rows=%s | avg_title_length=%.2f | top3=%s", 
                        results["total_rows"], float(results["avg_title_length"]), results["top3"])
        
        conn.commit()
        logger.info("Commit success.")
    
    except Exception:
        conn.rollback()
        logger.exception("ETL failed -> rollback executed")
        raise
    finally:
        conn.close()
        logger.info("DB connection closed")
        
    elapsed = time.time() - start
    logger.info("ETL end | duration=%.2fs", elapsed)
    
if __name__ == "__main__":
    main()