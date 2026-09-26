"""Create a small, deterministic, fully synthetic supply-chain demo dataset."""
from __future__ import annotations

from datetime import date, datetime, timedelta
from pathlib import Path
import csv
import random

OUT = Path(__file__).resolve().parents[1] / "data" / "generated"
random.seed(42)
TODAY = date.today()

def write(name: str, rows: list[dict]) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    with (OUT / f"{name}.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=rows[0].keys())
        writer.writeheader(); writer.writerows(rows)

suppliers = [
    {"SUPPLIER_ID":"SUP-001","SUPPLIER_NAME":"Northstar Components","COUNTRY":"India","RISK_TIER":"LOW","ON_TIME_RATE":96.2},
    {"SUPPLIER_ID":"SUP-002","SUPPLIER_NAME":"Pacific Precision","COUNTRY":"Vietnam","RISK_TIER":"MEDIUM","ON_TIME_RATE":88.4},
    {"SUPPLIER_ID":"SUP-003","SUPPLIER_NAME":"Apex Metals","COUNTRY":"Malaysia","RISK_TIER":"HIGH","ON_TIME_RATE":72.1},
]
plants = [
    {"PLANT_ID":"PLT-01","PLANT_NAME":"Pune Assembly","COUNTRY":"India","CRITICALITY":"HIGH"},
    {"PLANT_ID":"PLT-02","PLANT_NAME":"Chennai Components","COUNTRY":"India","CRITICALITY":"MEDIUM"},
]
parts = [{"PART_ID":f"PRT-{i:03}","PART_NAME":name,"CATEGORY":category,"LEAD_TIME_DAYS":lead,"UNIT_COST":cost}
         for i,(name,category,lead,cost) in enumerate([
             ("Motor Controller","Electronics",21,430.0),("Bearing Assembly","Mechanical",14,89.0),
             ("Battery Module","Energy",28,980.0),("Thermal Sensor","Electronics",10,35.0)], 1)]
pos=[]; shipments=[]; orders=[]; events=[]
for i in range(1, 101):
    supplier=suppliers[(i-1)%3]; part=parts[(i-1)%4]; plant=plants[(i-1)%2]
    po=f"PO-{i:04}"; delay=8 if i in {3, 11, 19, 47, 63, 88} else random.choice([0,0,1,2,3,4])
    pos.append({"PO_ID":po,"SUPPLIER_ID":supplier["SUPPLIER_ID"],"PART_ID":part["PART_ID"],"PLANT_ID":plant["PLANT_ID"],"QUANTITY":random.randint(30,180),"PROMISED_DATE":str(TODAY+timedelta(days=i%14+4)),"STATUS":"IN_TRANSIT"})
    shipment=f"SHP-{i:04}"; shipments.append({"SHIPMENT_ID":shipment,"PO_ID":po,"CARRIER":"Atlas Freight" if i%2 else "BlueRoute Logistics","ORIGIN":supplier["COUNTRY"],"DESTINATION":"India","ETA":str(TODAY+timedelta(days=i%14+4+delay)),"ACTUAL_OR_FORECAST_DELAY_DAYS":delay,"STATUS":"AT_RISK" if delay>=3 else "IN_TRANSIT","LAST_EVENT_AT":datetime.now().isoformat()})
    events.append({"EVENT_ID":f"EVT-{i:04}","SHIPMENT_ID":shipment,"EVENT_AT":datetime.now().isoformat(),"TEMPERATURE_C":38 if i in {3,11,19,47,63,88} else random.randint(18,33),"SHOCK_G":3.2 if i in {3,11,19,47,63,88} else round(random.uniform(.1,2.3),2),"GPS_STATUS":"DELAYED" if delay>=3 else "ON_TRACK"})
    for j in range(1, 3): orders.append({"ORDER_ID":f"ORD-{i:04}-{j}","PART_ID":part["PART_ID"],"PLANT_ID":plant["PLANT_ID"],"CUSTOMER_SEGMENT":"Enterprise" if j==1 else "Strategic","REVENUE_AT_RISK":round(random.uniform(30000,180000),2),"REQUIRED_DATE":str(TODAY+timedelta(days=i%10+5)),"STATUS":"OPEN"})

for name, rows in {"SUPPLIERS":suppliers,"PLANTS":plants,"PARTS":parts,"PURCHASE_ORDERS":pos,"SHIPMENTS":shipments,"CUSTOMER_ORDERS":orders,"SENSOR_EVENTS":events}.items(): write(name, rows)
print(f"Generated synthetic demo files in {OUT}")
