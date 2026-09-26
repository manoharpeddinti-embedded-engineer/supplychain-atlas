"""Load generated CSVs into the Snowflake demo schema using Snowpark."""
from __future__ import annotations
import os
from pathlib import Path
from dotenv import load_dotenv
from snowflake.snowpark import Session

load_dotenv()
ROOT = Path(__file__).resolve().parents[1] / "data" / "generated"

def session() -> Session:
    return Session.builder.configs({k.replace("SNOWFLAKE_", "").lower(): v for k,v in os.environ.items() if k.startswith("SNOWFLAKE_")}).create()

if __name__ == "__main__":
    s=session(); s.use_database(os.getenv("SNOWFLAKE_DATABASE", "SUPPLYCHAIN_ATLAS")); s.use_schema(os.getenv("SNOWFLAKE_SCHEMA", "CORE"))
    for path in ROOT.glob("*.csv"):
        table=path.stem
        s.file.put(str(path), "@~/atlas_uploads", auto_compress=False, overwrite=True)
        s.sql(f"COPY INTO {table} FROM @~/atlas_uploads/{path.name} FILE_FORMAT=(TYPE=CSV SKIP_HEADER=1 FIELD_OPTIONALLY_ENCLOSED_BY='\"')").collect()
        print(f"Loaded {table}")
    s.close()

