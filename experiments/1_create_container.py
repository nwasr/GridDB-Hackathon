import griddb_python as griddb

factory = griddb.StoreFactory.get_instance()

store = factory.get_store(
    notification_member="127.0.0.1:10001",
    cluster_name="myCluster",
    username="admin",
    password="admin"
)

cols = [
    ["datetime", griddb.Type.TIMESTAMP],
    ["machineID", griddb.Type.INTEGER],
    ["volt", griddb.Type.FLOAT],
    ["rotate", griddb.Type.FLOAT],
    ["pressure", griddb.Type.FLOAT],
    ["vibration", griddb.Type.FLOAT],
]

container_info = griddb.ContainerInfo(
    "machine_telemetry",
    cols,
    griddb.ContainerType.TIME_SERIES,
    True
)

ts = store.put_container(container_info)
ts.create_index("machineID")

print("✅ TimeSeries container 'machine_telemetry' created")
