import time
import paho.mqtt.client as mqtt
from simulator.config import cfg
from simulator.fleet import load_demo_fleet, iter_ticks, row_to_message
from simulator.faults import apply_faults, FAULT_COUNTS

def main():
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="factory-simulator")
    client.connect(cfg.mqtt_host, cfg.mqtt_port)
    client.loop_start()                       # thread réseau en arrière-plan

    df = load_demo_fleet()                    # uniquement les moteurs de démo (split du lab 1)
    try:
        for rows in iter_ticks(df):
            for row in rows:
                msg = row_to_message(row)
                for payload in apply_faults(msg, cfg):
                    topic = f"factory/engine/{msg['engine_id']}/telemetry"
                    client.publish(topic, payload, qos=1)
            time.sleep(cfg.tick_seconds)
    except KeyboardInterrupt:
        print("Simulator stopped by user")
    finally:
        print(FAULT_COUNTS)
        client.loop_stop()
        client.disconnect()

if __name__ == "__main__":
    main()