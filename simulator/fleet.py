import json
import uuid
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
SPLIT_PATH = ROOT / "data" / "split.json"
CMAPSS_PATH = ROOT / "data" / "cmapss" / "train_FD001.txt"
COLS = (["unit_id", "cycle", "op_setting_1", "op_setting_2", "op_setting_3"]
        + [f"s{i}" for i in range(1, 22)])
# Capteurs retenus au lab 1 (corrélation avec la RUL > 0.56), voir notebook 01_exploration
KEPT_SENSORS = ["s2", "s3", "s4", "s7", "s8", "s11", "s12", "s13", "s15", "s17", "s20", "s21"]


def engine_id(unit_id: int) -> str:
    return f"ENG-{unit_id:03d}"


def row_to_message(row: pd.Series) -> dict:
    return {
        "message_id": str(uuid.uuid4()),
        "engine_id": engine_id(int(row["unit_id"])),
        "cycle": int(row["cycle"]),
        "event_time": datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z"),
        "op_settings": [float(row["op_setting_1"]), float(row["op_setting_2"]), float(row["op_setting_3"])],
        "sensors": {s: float(row[s]) for s in KEPT_SENSORS},
    }


def load_demo_fleet() -> pd.DataFrame:
    with open(SPLIT_PATH) as file:
        demo_units = json.load(file)["demo_units"]

    df = pd.read_csv(CMAPSS_PATH, sep=r"\s+", header=None).iloc[:, :26]
    df.columns = COLS

    return df[df["unit_id"].isin(demo_units)]


def iter_ticks(df: pd.DataFrame):
    engines = {}
    for unit_id, group in df.groupby("unit_id"):
        engines[unit_id] = group.sort_values("cycle")

    t = 0
    while True:
        rows = []
        for group in engines.values():
            if len(group) > t:
                rows.append(group.iloc[t])
        if not rows:
            break
        yield rows
        t += 1


