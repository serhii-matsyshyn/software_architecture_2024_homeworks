from multiprocessing import Process

import hazelcast


def increment_value_without_locking():
    client = hazelcast.HazelcastClient(
        cluster_name="dev",
        cluster_members=[
            "127.0.0.1:5701",
            "127.0.0.1:5702",
            "127.0.0.1:5703"
        ]
    )
    distributed_map = client.get_map("map").blocking()

    key = "key"
    distributed_map.put_if_absent(key, 0)

    for _ in range(10000):
        value = distributed_map.get(key)
        value += 1
        distributed_map.put(key, value)

    client.shutdown()


def increment_value_with_pessimistic_locking():
    client = hazelcast.HazelcastClient(
        cluster_name="dev",
        cluster_members=[
            "127.0.0.1:5701",
            "127.0.0.1:5702",
            "127.0.0.1:5703"
        ]
    )
    distributed_map = client.get_map("map").blocking()

    key = "key"
    distributed_map.put_if_absent(key, 0)

    for _ in range(10000):
        distributed_map.lock(key)
        try:
            value = distributed_map.get(key)
            value += 1
            distributed_map.put(key, value)
        except Exception as err:
            print(err)
        finally:
            distributed_map.unlock(key)

    client.shutdown()


def increment_value_with_optimistic_locking():
    client = hazelcast.HazelcastClient(
        cluster_name="dev",
        cluster_members=[
            "127.0.0.1:5701",
            "127.0.0.1:5702",
            "127.0.0.1:5703"
        ]
    )
    distributed_map = client.get_map("map").blocking()

    key = "key"
    distributed_map.put_if_absent(key, 0)

    for _ in range(10000):
        while True:
            value = distributed_map.get(key)
            updated_value = value + 1
            if distributed_map.replace_if_same(key, value, updated_value):
                break

    client.shutdown()


if __name__ == "__main__":
    task = increment_value_with_optimistic_locking  # Selecting lock type here

    # Create three processes
    client1 = Process(target=task)
    client2 = Process(target=task)
    client3 = Process(target=task)

    # Start the processes
    client1.start()
    client2.start()
    client3.start()

    # Wait for the processes to finish
    client1.join()
    client2.join()
    client3.join()

    client = hazelcast.HazelcastClient()
    distributed_map = client.get_map("map")

    final_value = distributed_map.get("key").result()
    print(f"Final value: {final_value}")

    client.shutdown()
