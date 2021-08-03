# Copyright (c) Microsoft Corporation. All rights reserved.S
# Licensed under the MIT License. See License.txt in the project root for
# license information.
import os
import sys
import logging
import json
from paho_client import PahoClient

logger = logging.getLogger(__name__)

logging.basicConfig(level=logging.INFO)
logging.getLogger("paho").setLevel(level=logging.DEBUG)

# az iot hub topic-space create --topic-name "SampleZero" --topic-template "sample/#" --type "LowFanout"
topic = "sample/topic"
payload = {
    "latitude": 47.63962283908785,
    "longitude": -122.12718926895407,
}

client = PahoClient.create_from_connection_string(os.environ["CS"])

print("Starting connection")
client.start_connect()

print("Waiting for CONNACK")
if not client.connection_status.wait_for_connected(timeout=20):
    print("failed to connect.  exiting")
    sys.exit(1)

print("Publishing to {} at QOS=1".format(topic))
(rc, mid) = client.publish(topic, json.dumps(payload), qos=1)
print("Publish returned rc={}: {}".format(rc, PahoClient.error_string(rc)))

print("Waiting for PUBACK for mid={}".format(mid))
if client.incoming_pubacks.wait_for_ack(mid, timeout=20):
    print("PUBACK received")
else:
    print("PUBACK not received within 20 seconds")

print("Disconnecting")
client.disconnect()
client.connection_status.wait_for_disconnected()
