import random

import hazelcast

# Connect to the Hazelcast cluster
hz_client = hazelcast.HazelcastClient(
    cluster_name="dev",
    cluster_members=[
        "127.0.0.1:5701",
        "127.0.0.1:5702",
        "127.0.0.1:5703"
    ]
)

# Create a Distributed Map
distributed_map = hz_client.get_map("3_distributed_map").blocking()

for key in range(1000):
    distributed_map.set(key, random.randint(1, 500))

# Shutdown the Hazelcast client
hz_client.shutdown()
