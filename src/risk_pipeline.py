"""Derive transparent shipment risk scores with Snowpark."""
from __future__ import annotations
import os
from dotenv import load_dotenv
from snowflake.snowpark import Session
from snowflake.snowpark.functions import col, current_timestamp, lit, when

load_dotenv()
cfg={k.replace("SNOWFLAKE_", "").lower():v for k,v in os.environ.items() if k.startswith("SNOWFLAKE_")}
s=Session.builder.configs(cfg).create(); s.use_database(os.getenv("SNOWFLAKE_DATABASE","SUPPLYCHAIN_ATLAS")); s.use_schema(os.getenv("SNOWFLAKE_SCHEMA","CORE"))

ship=s.table("SHIPMENTS").join(s.table("PURCHASE_ORDERS"), "PO_ID").join(s.table("SUPPLIERS"), "SUPPLIER_ID")
events=s.table("SENSOR_EVENTS").select("SHIPMENT_ID", "TEMPERATURE_C", "SHOCK_G", "GPS_STATUS")
scored=(ship.join(events, "SHIPMENT_ID")
    .with_column("DELAY_FACTOR", when(col("ACTUAL_OR_FORECAST_DELAY_DAYS") >= 7, lit(45)).when(col("ACTUAL_OR_FORECAST_DELAY_DAYS") >= 3, lit(25)).otherwise(lit(5)))
    .with_column("SENSOR_FACTOR", when((col("TEMPERATURE_C") > 35) | (col("SHOCK_G") > 2), lit(25)).otherwise(lit(0)))
    .with_column("SUPPLIER_FACTOR", when(col("RISK_TIER") == "HIGH", lit(25)).when(col("RISK_TIER") == "MEDIUM", lit(12)).otherwise(lit(3)))
    .with_column("RISK_SCORE", col("DELAY_FACTOR") + col("SENSOR_FACTOR") + col("SUPPLIER_FACTOR"))
    .with_column("RISK_LEVEL", when(col("RISK_SCORE") >= 70, lit("CRITICAL")).when(col("RISK_SCORE") >= 40, lit("HIGH")).otherwise(lit("WATCH")))
    .with_column("CALCULATED_AT", current_timestamp())
    .select("SHIPMENT_ID","RISK_SCORE","RISK_LEVEL","DELAY_FACTOR","SENSOR_FACTOR","SUPPLIER_FACTOR","CALCULATED_AT"))
scored.write.mode("overwrite").save_as_table("SHIPMENT_RISK")
print("Risk model refreshed")
s.close()

