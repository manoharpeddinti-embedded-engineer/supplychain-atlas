# SupplyChain Atlas — 4:20 Hackathon Demo Plan

**Goal:** show a Snowflake-native, governed disruption workflow from input to operational decision.

**Recording rule:** record one Chrome tab: the deployed Snowflake Streamlit app. Turn off unrelated tabs and notifications. Use the narration at a measured 115–125 words per minute. Leave each metric visible for at least three seconds.

## Before recording — 20 seconds of preparation

- Open `SupplyChain Atlas` in Snowflake.
- Confirm **Command center** is selected and all three risk levels are selected.
- Keep the browser at normal zoom and scroll position so the four KPI cards and first critical rows are visible.
- Keep `SHP-0003` available in the What-if Lab.
- Do not show login, emails, browser history, or setup screens.

---

## 0:00–0:18 — Opening: business problem and project identity

**Screen:** Command center. Keep title, subtitle, and KPI cards in view.

**Show:** SupplyChain Atlas title; Revenue exposed; Critical shipments; Resilience index; Evidence coverage.

**Narration:**

> SupplyChain Atlas is a Snowflake-native supply-chain resilience command center. It brings supplier reliability, shipment status, IoT sensor events, plant demand, and customer commitments into one governed decision surface. The goal is to help an operations manager see which disruption must be escalated first, why it is risky, and how much customer revenue is exposed.

---

## 0:18–0:48 — Input: governed supply-chain ontology

**Screen:** Command center table. Slowly point to one row, then the columns: Shipment ID, Risk Level, Risk Score, Part, Plant, Supplier, Revenue at Risk, ETA.

**Show:** `SHP-0003`, its critical score, battery module, Pune Assembly, Apex Metals, and revenue at risk.

**Narration:**

> The input is a governed supply-chain ontology: suppliers, plants, parts, purchase orders, shipments, sensor events, customer orders, and shipment-risk records. Each row here is a joined operational story, not an isolated alert. For example, shipment SHP-0003 connects a delayed battery module to its supplier, destination plant, ETA, and the revenue that can be affected.

---

## 0:48–1:20 — Processing: explainable Snowpark risk model

**Screen:** Stay on the same critical row. Pause on Risk Score 95. Scroll slightly only if needed to keep the supplier exposure chart visible beneath the table.

**Show:** Risk score 95 and supplier exposure chart.

**Narration:**

> Processing happens in Snowflake. The risk pipeline combines three inspectable factors: delivery delay, sensor anomaly, and supplier reliability. The score is transparent: risk equals delay impact plus sensor impact plus supplier reliability impact. This is deliberately explainable. A planner can challenge a result, trace the evidence, and take action without relying on a black-box prediction.

---

## 1:20–1:55 — Capability 1: prioritized command center output

**Screen:** Command center. Point to the KPI cards, then the first five rows, then supplier chart.

**Show:** `33` shipments, `5` critical disruptions, `$40,242,000` revenue exposed, three supplier bars.

**Narration:**

> The first working capability is the command center. In this live scenario there are 33 shipments, five critical disruptions, and 40.2 million dollars of connected revenue exposure. The queue ranks the most urgent disruptions first. The supplier chart then reveals concentration of business risk across Apex Metals, Northstar Components, and Pacific Precision. This lets the team prioritize both a single shipment recovery and the supplier relationship behind it.

---

## 1:55–2:40 — Capability 2: recovery What-if Lab

**Navigation:** Click **What-if lab**. In **Shipment to simulate**, leave `SHP-0003` selected. Move **Days recovered by intervention** from `3` to `7`. Pause after each value change.

**Show:** Selected shipment, recovery-day slider, projected risk.

**Narration:**

> The second working capability is the What-if Lab. I select the highest-risk shipment, SHP-0003. A manager can test a realistic recovery intervention, such as expediting a carrier, changing routing, or using an alternate source. With three days recovered, the projected risk is 80. Increasing the recovery to seven days reduces it further. This converts a dashboard alert into a decision conversation: what intervention produces enough risk reduction to justify its cost?

---

## 2:40–3:15 — Capability 3: governed Decision Receipt

**Navigation:** Click **Decision receipt**. Keep the evidence text and formula visible.

**Show:** `SHIPMENTS + SENSOR_EVENTS + SUPPLIERS + CUSTOMER_ORDERS via governed V_CONTROL_TOWER` and `Risk = delay + sensor + supplier reliability`.

**Narration:**

> The third working capability is the Decision Receipt. Every recommendation has an evidence trail through the governed V_CONTROL_TOWER view. The receipt names the source domains: shipments, sensor events, suppliers, and customer orders. It also makes the risk formula visible. This is important for governance: the decision can be audited, reproduced, and explained to a planner, supplier manager, or executive.

---

## 3:15–3:48 — CoCo workflow connection

**Screen:** Keep Decision receipt visible. If the Snowflake CoCo panel is available, open it only after the main app demonstration and ask it to explain the governed view; otherwise retain the receipt screen.

**Show:** the evidence receipt; optionally the CoCo panel with a real prompt and real response.

**Narration:**

> CoCo accelerates the surrounding Snowflake workflow by helping teams discover catalog objects, validate the semantic contract, generate and verify SQL, and build the Streamlit experience. In this project, the governed view is the contract between raw operational signals and the business-facing command center. The application then exposes trusted metrics and evidence instead of allowing ungoverned interpretation of the source tables.

**Important:** only show CoCo if it produces a real response during recording. Do not present a mock response or claim a CoCo command was executed if it was not.

---

## 3:48–4:20 — Close: output and impact

**Navigation:** Click **Command center**. End on the KPI cards and critical shipment rows.

**Narration:**

> SupplyChain Atlas completes the workflow from governed input, through transparent Snowflake risk processing, to a prioritized and auditable action. Instead of asking planners to reconcile separate systems, it shows the disruption, the business impact, the recovery options, and the evidence in one place. That is the difference between detecting a delay and operating a resilient supply chain.

---

## Submission quality checklist

- [ ] Duration is between 3:50 and 4:30.
- [ ] The app title, four KPI cards, critical table rows, What-if Lab, and Decision Receipt are readable.
- [ ] Input → Processing → Output is spoken and visibly demonstrated.
- [ ] Three modular capabilities are named and demonstrated: Command Center, What-if Lab, Decision Receipt.
- [ ] No fabricated CoCo interaction is shown.
- [ ] Narration is added during editing; keep the narration script aligned to the on-screen action.
- [ ] Export as MP4 or WebM and verify playback before uploading.