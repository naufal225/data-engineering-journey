import os
from dataclasses import dataclass

def _required_env(key: str) -> str:
    val = os.getenv(key=key)
    if not val:
        raise RuntimeError(f"Missing required environtment variable: {key}")
    return val

def _env(key: str, default: str) -> str:
    return os.getenv(key=key, default=default)
   
def mask_secret(s: str, keep: int = 3) -> str:
    if s is None:
        return "<none>"
    if len(s) <= keep:
        return "*" * keep
    return s[:keep] + (len(s) - keep) * "*"

@dataclass(frozen=True)
class PgConfig:
    host: str
    port: str
    dbname: str
    user: str
    password: str
    
    @staticmethod
    def from_env() -> "PgConfig":
        host = _env("PGHOST", "localhost")
        port = _env("PGPORT", 5432)
        dbname = _required_env("PGDATABASE")
        user = _env("PGUSER", "postgres")
        password = _required_env("PGPASSWORD")
        return PgConfig(
            host=host,
            port=port,
            dbname=dbname,
            user=user,
            password=password
        )
        
    def safe_str(self) -> str:
        return (
            f"PgConfig(host={self.host}, port={self.port}, dbname={self.dbname}, "
            f"user={self.user}, password={mask_secret(self.password)})"
        )