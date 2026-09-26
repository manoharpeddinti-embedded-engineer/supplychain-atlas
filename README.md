# SupplyChain Atlas

**A governed supply-chain intelligence copilot built for the Snowflake CoCo CLI Hackathon.**

SupplyChain Atlas joins supplier, part, plant, purchase order, shipment, and sensor signals into a business ontology. It gives operations teams a trusted answer to questions such as *"Which shipments threaten customer orders this week, why, and what should we do first?"* Every answer is grounded in governed metrics and linked evidence.

## Why this can win

| Judging focus | What Atlas proves |
| --- | --- |
| Technical execution (40%) | Snowpark pipelines, Streams/Tasks, Cortex AI, a semantic model, RBAC, and Streamlit in one coherent architecture. |
| Real-world relevance (30%) | A realistic delay-to-customer-impact workflow with clear decisions for a supply-chain control tower. |
| Completeness (30%) | Reproducible synthetic data, deployable SQL, an interactive application, an evaluation plan, and a demo script. |

## The demo story

1. A sensor and carrier update makes a shipment high-risk.
2. Snowpark derives a risk score and joins the event to the affected parts, plants, and customer orders.
3. The Streamlit control tower prioritizes the largest business impact.
4. A governed copilot explains the risk with source records and recommends a next action.

## Architecture

```text
Synthetic operational feeds ──> Snowflake tables ──> Snowpark risk pipeline
                                                    │
Carrier / sensor updates ──> Stream + Task ────────┤
                                                    v
                                    Governed semantic model + Cortex
                                                    │
                                                    v
                                      Streamlit command center
```

## Repository map

| Path | Purpose |
| --- | --- |
| `sql/01_setup.sql` | Isolated role, warehouse, database, and schema setup. |
| `sql/02_tables.sql` | Core ontology tables and views. |
| `sql/03_governance.sql` | Risk view, row access pattern, and quality checks. |
| `src/generate_demo_data.py` | Deterministic synthetic operational dataset generator. |
| `src/load_data.py` | Snowpark loader for generated CSVs. |
| `src/risk_pipeline.py` | Snowpark risk scoring and impacted-order derivation. |
| `streamlit_app.py` | Interactive control tower and evidence-led copilot interface. |
| `semantic/atlas_semantic_model.yaml` | Governed metric and relationship contract. |

## Quick start

1. Create a virtual environment and install dependencies: `python -m venv .venv; .\.venv\Scripts\Activate.ps1; pip install -r requirements.txt`.
2. Copy `.env.example` to `.env` and populate your Snowflake account and user. The default `externalbrowser` authenticator keeps passwords out of the project and opens your existing Snowflake sign-in flow.
3. In Snowsight, execute the SQL files in order: `01_setup.sql`, `02_tables.sql`, then `03_governance.sql`.
4. Generate and load the synthetic data:

   ```powershell
   python src/generate_demo_data.py
   python src/load_data.py
   python src/risk_pipeline.py
   streamlit run streamlit_app.py
   ```

5. Run CoCo CLI against this repository and your Snowflake connection:

   ```powershell
   cortex -w . -c <your_connection>
   ```

   Prompt it: `Review this supply-chain repository. Validate the data model, then suggest a Snowflake-native improvement that preserves the demo story.`

## Data and responsible AI

All supplied data is synthetic. The app labels risk as a decision-support signal, shows the contributing factors, and keeps an evidence trail. Do not load customer, employee, or proprietary operational data without the necessary rights and governance approval.

## Submission checklist

- [ ] Run the app from a clean clone and capture screenshots.
- [ ] Add a 6-slide deck: problem, users, architecture, live workflow, governance, impact.
- [ ] Add a 90-second backup demo video, while keeping the live demo primary.
- [ ] Make the GitHub repository accessible to judges.
- [ ] List every dataset and license in the final submission.
- [ ] Submit the prototype and GitHub/deployed links before **4 October 2026, 11:59 PM IST**.
