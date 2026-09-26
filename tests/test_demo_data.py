"""Regression checks for the synthetic hackathon demo data."""
from __future__ import annotations

import csv
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "generated"


def rows(name: str) -> list[dict[str, str]]:
    with (DATA / f"{name}.csv").open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


class DemoDataTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        subprocess.run([sys.executable, "src/generate_demo_data.py"], cwd=ROOT, check=True)

    def test_foreign_keys_and_risk_scenario_exist(self) -> None:
        suppliers = {row["SUPPLIER_ID"] for row in rows("SUPPLIERS")}
        parts = {row["PART_ID"] for row in rows("PARTS")}
        plants = {row["PLANT_ID"] for row in rows("PLANTS")}
        purchase_orders = {row["PO_ID"] for row in rows("PURCHASE_ORDERS")}
        self.assertTrue(all(row["SUPPLIER_ID"] in suppliers and row["PART_ID"] in parts and row["PLANT_ID"] in plants for row in rows("PURCHASE_ORDERS")))
        self.assertTrue(all(row["PO_ID"] in purchase_orders for row in rows("SHIPMENTS")))
        self.assertGreaterEqual(sum(int(row["ACTUAL_OR_FORECAST_DELAY_DAYS"]) >= 7 for row in rows("SHIPMENTS")), 3)

    def test_sensor_events_cover_every_shipment(self) -> None:
        shipment_ids = {row["SHIPMENT_ID"] for row in rows("SHIPMENTS")}
        event_shipments = {row["SHIPMENT_ID"] for row in rows("SENSOR_EVENTS")}
        self.assertEqual(shipment_ids, event_shipments)


if __name__ == "__main__":
    unittest.main()
