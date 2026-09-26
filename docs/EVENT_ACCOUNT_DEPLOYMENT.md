# Event Account Deployment

SupplyChain Atlas is live in the event Snowflake account as:

- Database/schema: `SUPPLYCHAIN_ATLAS.CORE`
- Warehouse: `SUPPLYCHAIN_HACK_WH` (X-Small, 60-second auto-suspend)
- Streamlit app: `SUPPLYCHAIN_ATLAS.CORE.SUPPLYCHAIN_ATLAS`

The demo uses only synthetic records. The deployed scenario contains 120 shipments, 10 critical disruptions, 32 high-risk disruptions, and a governed `V_CONTROL_TOWER` view joining shipment, sensor, supplier, plant, part, purchase-order, and customer-order evidence.

## Reproduce

Run the SQL scripts in order:

1. `sql/01_setup.sql`
2. `sql/02_tables.sql`
3. `sql/03_governance.sql`
4. Generate and load synthetic data with `src/generate_demo_data.py`, `src/load_data.py`, and `src/risk_pipeline.py`.

The deployed Streamlit experience adds a command-center queue, supplier risk concentration chart, mitigation rehearsal, decision receipt, and trust controls.

## CoCo evidence prompt

Use the governed view as the source of truth:

```text
Using SUPPLYCHAIN_ATLAS.CORE.V_CONTROL_TOWER, identify the highest-risk shipment, explain its delay, sensor, and supplier factors, quantify customer revenue exposure, and recommend the first operator action. Cite the evidence entities used.
```