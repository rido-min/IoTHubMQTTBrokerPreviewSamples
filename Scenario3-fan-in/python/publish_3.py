# Copyright (c) Microsoft Corporation. All rights reserved.S
# Licensed under the MIT License. See License.txt in the project root for
# license information.
import os
import sys
import logging  # noqa: F401
import json
import time
import random
import copy
from typing import Dict, Any
from concurrent.futures import ThreadPoolExecutor
from paho_client import PahoClient

"""
Uncomment the following lines to enable debug logging
"""

# logging.basicConfig(level=logging.INFO)
# logging.getLogger("paho").setLevel(level=logging.DEBUG)

##################################
# CREATE CLIENTS
##################################

client_1 = PahoClient.create_from_connection_string(
    os.environ["CS_VEHICLE_1"], clean_session=True
)
client_2 = PahoClient.create_from_connection_string(
    os.environ["CS_VEHICLE_2"], clean_session=True
)
all_clients = (
    (client_1, {"latitude": 47.63962283908785, "longitude": -122.12718926895407}),
    (client_2, {"latitude": 35.04774061011439, "longitude": -90.02605170007172}),
)


def listen(client: PahoClient, initial_location: Dict[str, Any]) -> None:
    ##################################
    # CONNECT
    ##################################

    print("{}: Connecting".format(client.auth.device_id))
    client.start_connect()
    if not client.connection_status.wait_for_connected(timeout=20):
        print("{}: Connection failed.  Exiting.".format(client.auth.device_id))
        sys.exit(1)
    print("{}: Connected".format(client.auth.device_id))

    ##################################
    # PUBLISH
    ##################################
    topic = "vehicles/{}/GPS/position".format(client.auth.device_id)
    for i in range(1, 20):
        payload = copy.copy(initial_location)
        payload["index"] = i
        payload["latitude"] += i

        print(
            "{}: Publishing to {} at QOS=1: {}".format(
                client.auth.device_id, topic, payload
            )
        )
        (rc, mid) = client.publish(topic, json.dumps(payload), qos=1)
        print(
            "{}: Publish for {} returned rc={}: {}".format(
                client.auth.device_id, str(payload), rc, PahoClient.error_string(rc)
            )
        )

        print("{}: Waiting for PUBACK for mid={}".format(client.auth.device_id, mid))
        if client.incoming_pubacks.wait_for_ack(mid, timeout=20):
            print("{}: PUBACK received".format(client.auth.device_id))
        else:
            print(
                "{}: PUBACK not received within 20 seconds".format(
                    client.auth.device_id
                )
            )

        # sleep between .5 and 2.5 seconds
        sleep_time = random.uniform(0.5, 2.5)
        print("{}: sleeping for {} seconds".format(client.auth.device_id, sleep_time))
        time.sleep(sleep_time)

    ##################################
    # DISCONNECT
    ##################################

    print("{}: Disconnecting".format(client.auth.device_id))
    client.disconnect()
    client.connection_status.wait_for_disconnected()


##################################
# CREATE THREADS
##################################
with ThreadPoolExecutor() as tp:
    for (client, initial_position) in all_clients:
        tp.submit(listen, client, initial_position)
