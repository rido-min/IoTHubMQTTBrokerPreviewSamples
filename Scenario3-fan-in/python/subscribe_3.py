# Copyright (c) Microsoft Corporation. All rights reserved.S
# Licensed under the MIT License. See License.txt in the project root for
# license information.
import os
import sys
import logging  # noqa: F401
import json
import time
from paho_client import PahoClient

"""
Uncomment the following lines to enable debug logging
"""
# logging.basicConfig(level=logging.INFO)
# logging.getLogger("paho").setLevel(level=logging.DEBUG)


##################################
# CREATE CLIENTS
##################################

client = PahoClient.create_from_connection_string(os.environ["CS_MAP_DEVICE"])

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
# SUBSCRIBE
##################################

topic_filter = "vehicles/+/GPS/#"

qos = 1
print(
    "{}: Subscribing to {} at qos {}".format(client.auth.device_id, topic_filter, qos)
)
(rc, mid) = client.subscribe(topic_filter, qos)

ack_result = client.incoming_subacks.wait_for_ack(mid, timeout=20)
if not ack_result:
    print("{}: SUBACK not received within 20 seconds".format(client.auth.device_id))
    client.disconnect()
    client.connection_status.wait_for_disconnected()
    sys.exit(1)
elif ack_result[0] == -1:
    print("{}: Subscription was rejected".format(client.auth.device_id))
    client.disconnect()
    client.connection_status.wait_for_disconnected()
    sys.exit(1)
else:
    print(
        "{}: Subscription was granted with qos {}".format(
            client.auth.device_id, ack_result[0]
        )
    )

##################################
# LISTEN
##################################

time_to_listen_in_seconds = 600
end_time = time.time() + time_to_listen_in_seconds

while time.time() <= end_time:
    remaining_time = end_time - time.time()

    message = client.incoming_messages.pop_next_message(timeout=remaining_time)
    if message:
        payload_object = json.loads(message.payload)
        print(
            "{}: Message for received on topic {}: {}".format(
                client.auth.device_id, message.topic, payload_object
            )
        )


##################################
# DISCONNECT
##################################

print("{}: Disconnecting".format(client.auth.device_id))
client.disconnect()
client.connection_status.wait_for_disconnected()
