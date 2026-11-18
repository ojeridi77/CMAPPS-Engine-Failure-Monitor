# simulator/config.py
import os
from dataclasses import dataclass


@dataclass
class Config:
    mqtt_host: str
    mqtt_port: int
    tick_seconds: float
    fault_duplicate: float
    fault_missing_sensor: float
    fault_out_of_range: float
    fault_late: float
    fault_corrupted: float

def load_config() -> Config:
    return Config(
        mqtt_host=os.getenv("MQTT_HOST", "localhost"),
        mqtt_port=int(os.getenv("MQTT_PORT", "1883")),
        tick_seconds=float(os.getenv("TICK_SECONDS", "1.0")),
        fault_duplicate=float(os.getenv("FAULT_DUPLICATE", "0.02")),
        fault_missing_sensor=float(os.getenv("FAULT_MISSING_SENSOR", "0.01")),
        fault_out_of_range=float(os.getenv("FAULT_OUT_OF_RANGE", "0.01")),
        fault_late=float(os.getenv("FAULT_LATE", "0.02")),
        fault_corrupted=float(os.getenv("FAULT_CORRUPTED", "0.005")),
    )

cfg = load_config()   # l'objet que les autres fichiers importent