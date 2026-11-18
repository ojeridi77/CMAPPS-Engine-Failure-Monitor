from simulator.fleet import engine_id
from simulator.fleet import row_to_message
import pandas as pd
import json
from pathlib import Path
from jsonschema import Draft202012Validator, FormatChecker
from simulator.config import Config
from simulator.faults import apply_faults
import pytest
SCHEMA_PATH = Path(__file__).resolve().parent.parent / "contracts" / "telemetry.schema.json"


def test_engine():
  assert engine_id(7) == 'ENG-007'
  assert engine_id(42) == 'ENG-042'

ser = {
    "unit_id": 1, "cycle": 1,
    "op_setting_1": -0.0007, "op_setting_2": -0.0004, "op_setting_3": 100.0,
    "s2": 641.82, "s3": 1589.70, "s4": 1400.60, "s7": 554.36,
    "s8": 2388.06, "s11": 47.47, "s12": 521.66, "s13": 2388.02,
    "s15": 8.4195, "s17": 392, "s20": 39.06, "s21": 23.4190,
}
ser_test = pd.Series(ser)

def test_message():
    with open(SCHEMA_PATH) as file:
        schema = json.load(file)

    validator = Draft202012Validator(schema, format_checker=FormatChecker())

    msg = row_to_message(ser_test)                                 # le message produit à partir de ser_test
    errors = list(validator.iter_errors(msg))

    assert len(errors) == 0

CFG_DUPLICATE = Config(     #Cas duplication
    mqtt_host="localhost",
    mqtt_port=1883,
    tick_seconds=0.0,
    fault_duplicate=1.0,
    fault_missing_sensor=0.0,
    fault_out_of_range=0.0,
    fault_late=0.0,
    fault_corrupted=0.0,
)

CFG_CORRUPTED = Config(      #Cas corrompu
    mqtt_host="localhost",
    mqtt_port=1883,
    tick_seconds=0.0,
    fault_duplicate=0.0,
    fault_missing_sensor=0.0,
    fault_out_of_range=0.0,
    fault_late=0.0,
    fault_corrupted=1.0,
)

def test_duplicate():
    payload_list = apply_faults(row_to_message(ser_test), CFG_DUPLICATE)

    assert len(payload_list) == 2
    assert  payload_list[0] == payload_list[1]

def test_corrupted():
    payload_list = apply_faults(row_to_message(ser_test), CFG_CORRUPTED)
    assert len(payload_list) == 1
    with pytest.raises(json.JSONDecodeError):
        json.loads(payload_list[0])

