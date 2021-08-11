# Copyright (c) Microsoft Corporation. All rights reserved.S
# Licensed under the MIT License. See License.txt in the project root for
# license information.
import os
import sys
import logging
import json
import time
from paho_client import PahoClient

logger = logging.getLogger(__name__)

"""
Uncomment the following lines to enable debug logging
"""

logging.basicConfig(level=logging.INFO)
logging.getLogger("paho").setLevel(level=logging.DEBUG)

topic_filter = "sample/topic"


client = PahoClient.create_from_connection_string(
    os.environ["CS"], clean_session=True
)

print("Connecting")
client.start_connect()
if not client.connection_status.wait_for_connected(timeout=20):
    sys.exit(1)

qos = 1
print("Subscribing to {} at qos {}".format(topic_filter, qos))
(rc, mid) = client.subscribe(topic_filter, qos)

ack_result = client.incoming_subacks.wait_for_ack(mid, timeout=20)
if not ack_result:
    print("SUBACK not received within 20 seconds")
    client.disconnect()
    client.connection_status.wait_for_disconnected()
    sys.exit(1)
elif ack_result[0] == -1:
    print("Subscription was rejected")
    client.disconnect()
    client.connection_status.wait_for_disconnected()
    sys.exit(1)
else:
    print("Subscription was granted with qos {}".format(ack_result[0]))

time_to_listen_in_seconds = 600
end_time = time.time() + time_to_listen_in_seconds

while time.time() <= end_time:
    remaining_time = end_time - time.time()
    print("Waiting for messages for {} more seconds".format(remaining_time))

    message = client.incoming_messages.pop_next_message(timeout=remaining_time)
    if message:
        print("Message received on topic {}".format(message.topic))
        payload_object = json.loads(message.payload)
        print("Payload: {}".format(payload_object))

print("Disconnecting")
client.disconnect()
client.connection_status.wait_for_disconnected()
