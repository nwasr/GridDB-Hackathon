import griddb_python as griddb
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import time
from datetime import datetime, timedelta

st.set_page_config(layout="wide")
st.title("Predictive Maintenance Dashboard (GridDB)")

# GridDB connection
factory = griddb.StoreFactory.get_instance()
store = factory.get_store(
    notification_member="127.0.0.1:10001",
    cluster_name="myCluster",
    username="admin",
    password="admin"
)

ts = store.get_container("machine_telemetry")

# Sidebar controls
st.sidebar.header("Controls")
machine_id = st.sidebar.selectbox("Select Machine ID", list(range(1, 101)))
limit = st.sidebar.slider("Recent records", 100, 2000, 500)

# Query (GridDB-safe)
query = ts.query(
    f"SELECT * WHERE machineID = {machine_id} "
    f"ORDER BY datetime DESC LIMIT {limit}"
)

rs = query.fetch(False)
df = rs.fetch_rows()

if df.empty:
    st.warning("No data found for selected machine.")
    time.sleep(2)
    st.rerun()

# Convert + filter recent data
df["datetime"] = pd.to_datetime(df["datetime"])
df = df.sort_values("datetime")

cutoff = datetime.utcnow() - timedelta(hours=1)
df = df[df["datetime"] > cutoff]

if df.empty:
    st.warning("No recent data in the last hour.")
    time.sleep(2)
    st.rerun()

# Stats
mean_v = df["vibration"].mean()
std_v = df["vibration"].std()
warn = mean_v + 2 * std_v
crit = mean_v + 3 * std_v
latest = df["vibration"].iloc[-1]

# Metrics
c1, c2, c3 = st.columns(3)
c1.metric("Mean Vibration", f"{mean_v:.2f}")
c2.metric("Std Deviation", f"{std_v:.2f}")
c3.metric("Latest Vibration", f"{latest:.2f}")

# Plot
fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(df["datetime"], df["vibration"], label="Vibration")
ax.axhline(warn, linestyle="--", color="orange", label="Warning")
ax.axhline(crit, linestyle="--", color="red", label="Critical")
ax.set_title(f"Machine {machine_id} Vibration (Live)")
ax.legend()

st.pyplot(fig)

# Alerts
if latest > crit:
    st.error("🚨 CRITICAL: Immediate maintenance required")
elif latest > warn:
    st.warning("⚠️ WARNING: Abnormal vibration detected")
else:
    st.success("✅ Machine operating normally")

# Auto-refresh (LIVE)
time.sleep(2)
st.rerun()
