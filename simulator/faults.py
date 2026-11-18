import json
import random as rd
from simulator.config import Config
import copy
from collections import Counter

FAULT_COUNTS = Counter()
LATE_BUFFER = {}

def apply_faults(msg,cfg: Config):

    engine = msg["engine_id"]
    cp_msg = copy.deepcopy(msg)

    if rd.random() < cfg.fault_missing_sensor:
        cp_msg["sensors"].pop(rd.choice(list(cp_msg["sensors"])))
        FAULT_COUNTS["MISSING_SENSOR"] += 1

    if rd.random() < cfg.fault_out_of_range:
        rd_sensor = rd.choice(list(cp_msg["sensors"]))
        cp_msg["sensors"][rd_sensor] *= 10
        FAULT_COUNTS["OUT_OF_RANGE"] += 1

    payload = []
    msg_json = json.dumps(cp_msg).encode('utf-8')

    still_waiting = []
    for remaining, late_payload in LATE_BUFFER.get(engine, []):
        if remaining <= 1:
            payload.append(late_payload)
        else:
            still_waiting.append((remaining - 1, late_payload))
    LATE_BUFFER[engine] = still_waiting


    if rd.random() < cfg.fault_corrupted:
        cut = len(msg_json) // 2
        payload.append(msg_json[:cut])
        FAULT_COUNTS["CORRUPTED"] += 1

    elif rd.random() < cfg.fault_duplicate:
        payload.append(msg_json)
        payload.append(msg_json)
        FAULT_COUNTS["DUPLICATE"] += 1

    elif rd.random() < cfg.fault_late:
        LATE_BUFFER[engine].append((rd.randint(2, 5), msg_json))
        FAULT_COUNTS["LATE"] += 1

    else:
        payload.append(msg_json)

    return payload