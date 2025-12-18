import griddb_python as griddb

factory = griddb.StoreFactory.get_instance()

store = factory.get_store(
    notification_member="127.0.0.1:10001",
    cluster_name="myCluster",
    username="admin",
    password="admin"
)

ts = store.get_container("machine_telemetry")

query = ts.query("SELECT * ORDER BY datetime DESC LIMIT 5")
rs = query.fetch()

print("🔎 Latest records:")
while rs.has_next():
    print(rs.next())
