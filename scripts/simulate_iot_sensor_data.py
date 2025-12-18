import griddb_python as griddb
import pandas as pd
import time
from datetime import datetime

factory = griddb.StoreFactory.get_instance()

store = factory.get_store(
    notification_member="127.0.0.1:10001",
    cluster_name="myCluster",
    username="admin",
    password="admin"
)

ts = store.get_container("machine_telemetry")

df = pd.read_csv("../data/PdM_telemetry.csv")

print("🚀 Starting real-time IoT data stream...")

for _, r in df.iterrows():
    ts.put([
        datetime.utcnow(),              # ✅ LIVE timestamp
        int(r["machineID"]),
        float(r["volt"]),
        float(r["rotate"]),
        float(r["pressure"]),
        float(r["vibration"]),
    ])

    print(
        f"Machine {r['machineID']} | "
        f"Vibration={r['vibration']:.2f}"
    )

    time.sleep(0.5)  # simulate sensor interval
