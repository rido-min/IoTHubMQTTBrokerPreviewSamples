# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
import os
import sys
import logging  # noqa: F401
import json
from paho_client import PahoClient

"""
Uncomment the following lines to enable debug logging
"""
# logging.basicConfig(level=logging.INFO)
# logging.getLogger("paho").setLevel(level=logging.DEBUG)


##################################
# CREATE CLIENT
##################################

client = PahoClient.create_from_connection_string(os.environ["CS_FLEET_MGT_DEVICE"])

##################################
# CONNECT
##################################

print("{}: Starting connection".format(client.auth.device_id))
client.start_connect()
if not client.connection_status.wait_for_connected(timeout=20):
    print("{}: failed to connect.  exiting".format(client.auth.device_id))
    sys.exit(1)

##################################
# PUBLISH
##################################

topic = "fleet/alerts/weather/alert1"
payload = {
    "message": "The national weather service has issued a tornado watch for Milwaukee County until 8 PM tonight"
}

print("{}: Publishing to {} at QOS=1: {}".format(client.auth.device_id, topic, payload))
(rc, mid) = client.publish(topic, json.dumps(payload), qos=1)
print(
    "{}: Publish returned rc={}: {}".format(
        client.auth.device_id, rc, PahoClient.error_string(rc)
    )
)

print("{}: Waiting for PUBACK for mid={}".format(client.auth.device_id, mid))
if client.incoming_pubacks.wait_for_ack(mid, timeout=20):
    print("{}: PUBACK received".format(client.auth.device_id))
else:
    print("{}: PUBACK not received within 20 seconds".format(client.auth.device_id))


##################################
# DISCONNECT
##################################

print("{}: Disconnecting".format(client.auth.device_id))
client.disconnect()
client.connection_status.wait_for_disconnected()
