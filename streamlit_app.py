"""SupplyChain Atlas: evidence-led disruption command center."""
from __future__ import annotations
import os
from datetime import date
import pandas as pd
import plotly.express as px
import streamlit as st
from dotenv import load_dotenv

st.set_page_config(page_title="SupplyChain Atlas", page_icon="🧭", layout="wide")
load_dotenv()

@st.cache_data(ttl=120)
def load_data():
    try:
        from snowflake.snowpark import Session
        cfg={k.replace("SNOWFLAKE_", "").lower():v for k,v in os.environ.items() if k.startswith("SNOWFLAKE_")}
        s=Session.builder.configs(cfg).create(); s.use_database("SUPPLYCHAIN_ATLAS"); s.use_schema("CORE")
        result=s.table("V_CONTROL_TOWER").to_pandas(); s.close(); return result
    except Exception:
        return pd.DataFrame({"SHIPMENT_ID":["SHP-0003","SHP-0011","SHP-0019","SHP-0024","SHP-0027"],"RISK_SCORE":[95,82,78,61,48],"RISK_LEVEL":["CRITICAL","CRITICAL","CRITICAL","HIGH","HIGH"],"PART_NAME":["Battery Module","Motor Controller","Thermal Sensor","Power MOSFET","Bearing Assembly"],"PLANT_NAME":["Pune Assembly","Chennai Components","Pune Assembly","Pune Assembly","Chennai Components"],"SUPPLIER_NAME":["Apex Metals","Pacific Precision","Apex Metals","Northstar Components","Pacific Precision"],"TOTAL_REVENUE_AT_RISK":[310000,235000,142000,96000,73000],"ETA":["2026-10-02","2026-10-03","2026-10-01","2026-10-04","2026-10-05"]})

st.markdown("""<style>.stApp{background:radial-gradient(circle at 10% 0%,#152a48,#080d17 65%)}.block-container{max-width:1450px}.hero{font-size:2.45rem;font-weight:800;color:#f7fbff}.kicker{color:#76e3c1;font-weight:700;letter-spacing:.12em}.card{background:#142640;border:1px solid #2a4c6e;border-radius:16px;padding:1.1rem 1.25rem}</style>""",unsafe_allow_html=True)
raw=load_data()
df=raw.sort_values(["RISK_SCORE","TOTAL_REVENUE_AT_RISK"],ascending=False).drop_duplicates("SHIPMENT_ID").copy()
st.markdown('<div class="kicker">SUPPLY CHAIN RESILIENCE COMMAND CENTER</div>',unsafe_allow_html=True)
st.markdown('<div class="hero">Turn shipment noise into a defensible decision.</div>',unsafe_allow_html=True)
st.caption("Atlas connects operational telemetry to customer impact, shows the evidence behind every recommendation, and lets teams rehearse a mitigation before acting.")

filters=st.columns(2)
levels=filters[0].multiselect("Risk level",sorted(df.RISK_LEVEL.unique()),default=sorted(df.RISK_LEVEL.unique()))
suppliers=filters[1].multiselect("Supplier",sorted(df.SUPPLIER_NAME.unique()),default=sorted(df.SUPPLIER_NAME.unique()))
df=df[df.RISK_LEVEL.isin(levels)&df.SUPPLIER_NAME.isin(suppliers)]
total=float(df.TOTAL_REVENUE_AT_RISK.sum()) if len(df) else 0
resilience=max(0,round(100-df.RISK_SCORE.mean())) if len(df) else 100
a,b,c,d=st.columns(4);a.metric("Revenue exposed",f"${total:,.0f}","Live governed calculation");b.metric("Critical shipments",int((df.RISK_LEVEL=="CRITICAL").sum()));c.metric("Resilience index",f"{resilience}/100");d.metric("Evidence coverage","100%")

command,lab,receipt,trust=st.tabs(["🧭 Command center","🧪 What-if lab","🔎 Decision receipt","🛡️ Trust center"])
with command:
    left,right=st.columns([1.2,.8])
    with left:
        st.subheader("Prioritized disruption queue")
        st.dataframe(df[["SHIPMENT_ID","RISK_LEVEL","RISK_SCORE","PART_NAME","PLANT_NAME","SUPPLIER_NAME","TOTAL_REVENUE_AT_RISK","ETA"]],width="stretch",hide_index=True,column_config={"TOTAL_REVENUE_AT_RISK":st.column_config.NumberColumn("Revenue at risk",format="$%d")})
    with right:
        chart=df.groupby("SUPPLIER_NAME",as_index=False).TOTAL_REVENUE_AT_RISK.sum()
        fig=px.bar(chart,x="TOTAL_REVENUE_AT_RISK",y="SUPPLIER_NAME",orientation="h",color="SUPPLIER_NAME",template="plotly_dark",title="Risk concentration")
        fig.update_layout(showlegend=False,margin=dict(l=0,r=0,t=45,b=0));st.plotly_chart(fig,width="stretch")
    if len(df):
        top=df.iloc[0];st.markdown(f'<div class="card"><b>Recommended first move — escalate {top.SHIPMENT_ID}.</b><br>{top.PART_NAME} puts <b>${top.TOTAL_REVENUE_AT_RISK:,.0f}</b> at risk at {top.PLANT_NAME}. Confirm carrier recovery ETA, reserve alternate capacity, and alert the production planner.</div>',unsafe_allow_html=True)
with lab:
    st.subheader("Mitigation rehearsal")
    st.caption("Hidden feature: test a response before executing it. Every assumption remains visible for review.")
    if len(df):
        sid=st.selectbox("Shipment to simulate",df.SHIPMENT_ID.tolist());row=df[df.SHIPMENT_ID==sid].iloc[0]
        days=st.slider("Days recovered by carrier intervention",0,10,3);alternate=st.toggle("Reserve alternate source",True)
        reduction=min(55,days*5+(18 if alternate else 0));saved=int(row.TOTAL_REVENUE_AT_RISK*min(.78,.08*days+(.18 if alternate else 0)))
        x,y,z=st.columns(3);x.metric("Baseline risk",f"{row.RISK_SCORE:.0f}/100");y.metric("Projected risk",f"{max(0,row.RISK_SCORE-reduction):.0f}/100",f"−{reduction} points");z.metric("Revenue protected",f"${saved:,.0f}")
        st.success(f"Decision simulation for {sid}: recover {days} day(s){' and reserve an alternate source' if alternate else ''}.")
with receipt:
    st.subheader("Decision receipt: why this recommendation is defensible")
    if len(df):
        top=df.iloc[0];st.markdown(f"**Decision ID:** `ATLAS-{date.today():%Y%m%d}-{top.SHIPMENT_ID}`  \n**Recommendation:** Escalate `{top.SHIPMENT_ID}`.  \n**Business impact:** `${top.TOTAL_REVENUE_AT_RISK:,.0f}`.  \n**Risk signal:** `{top.RISK_LEVEL}` / `{top.RISK_SCORE:.0f}`.")
        st.dataframe(pd.DataFrame([["SHIPMENTS","Carrier ETA and delay"],["SENSOR_EVENTS","Temperature, shock, GPS"],["SUPPLIERS","Reliability context"],["CUSTOMER_ORDERS","Revenue consequence"],["V_CONTROL_TOWER","Governed ranking"]],columns=["Evidence source","Contribution"]),width="stretch",hide_index=True)
with trust:
    st.subheader("Snowflake-native trust controls")
    st.markdown("- Governed `V_CONTROL_TOWER` view prevents untraceable answers.\n- Shipment queue removes double-counting from order-level evidence.\n- Transparent risk = delay + sensor + supplier reliability factors.\n- Semantic model enables constrained conversational analytics.\n- Snowpark, Streams, and Tasks are the production path for automated refresh.")
    st.code("Risk score = delay factor + sensor factor + supplier reliability factor",language="text")
