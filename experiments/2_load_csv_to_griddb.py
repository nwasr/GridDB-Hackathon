import griddb_python as griddb
import pandas as pd

factory = griddb.StoreFactory.get_instance()

store = factory.get_store(
    notification_member="127.0.0.1:10001",
    cluster_name="myCluster",
    username="admin",
    password="admin"
)

ts = store.get_container("machine_telemetry")

df = pd.read_csv("../data/PdM_telemetry.csv")
df["datetime"] = pd.to_datetime(df["datetime"])

df = df[["datetime", "machineID", "volt", "rotate", "pressure", "vibration"]]

rows = []
BATCH = 5000

print("📥 Loading historical CSV into GridDB...")

for _, r in df.iterrows():
    rows.append([
        r["datetime"].to_pydatetime(),
        int(r["machineID"]),
        float(r["volt"]),
        float(r["rotate"]),
        float(r["pressure"]),
        float(r["vibration"]),
    ])

    if len(rows) == BATCH:
        ts.multi_put(rows)
        rows.clear()

if rows:
    ts.multi_put(rows)

print("✅ Historical data loaded")
