# Scenarios 1 - Route data published on a topic to the built-in-endpoint

This scenario showcases how to configure route to send filtered messages from a custom topic to the built-in Event Hubs endpoint. For more details, see [routing support for broker hubs](https://github.com/Azure/IoTHubMQTTBrokerPreviewSamples#message-routing-for-mqtt-broker-enabled-iot-hubs)

Consider a use case where one needs to identify location of vehicles. The vehicles publish their GPS data on topics with their device ID in the path, for example `vehicles/<VIN>/GPS`.
| Device | Role| Topic | Topic Template | Topic Space Type|
| -------- | --------------- |---------- |---------- |---------- |
| vehicle1 | publisher | vehicles/vehicle1/GPS | vehicles/${principal.deviceid}/GPS/# | PublishOnly|

1. Setup

For this scenario, please ensure you have deployed a IoT Hub with routing using the [ARM template](https://github.com/prashmo/azure-quickstart-templates/tree/master/quickstarts/microsoft.devices/iothub-mqtt-broker-route-messages). 

Validate routing setup.

```azurecli
az rest --method get --url 'https://management.azure.com/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Devices/IotHubs/{iothubName}?api-version=2021-07-01-preview' --query "properties.routing.routes"
```

Expected:

```
[
  {
    "condition": "STARTS_WITH($mqtt-topic, \"vehicles/\")",
    "endpointNames": [
      "events"
    ],
    "isEnabled": true,
    "name": "MqttBrokerRoute",
    "source": "MqttBrokerMessages"
  }
]
```

2. Configure TopicSpace using the Azure CLI command guidance below:

 ```azurecli
az iot hub topic-space create -n {iothub_name} --tsn publisher_ts --tst PublishOnly --template 'vehicles/${principal.deviceid}/GPS/#'
```

  For more details see [Topic Spaces](https://github.com/Azure/IoTHubMQTTBrokerPreviewSamples#topic-spaces)

3. Register devices using the [Azure CLI](https://docs.microsoft.com/cli/azure/iot/hub/device-identity?view=azure-cli-latest#az_iot_hub_device_identity_create)

```azure cli
az iot hub device-identity create -n {iothub_name} -d vehicle1 --am shared_private_key
az iot hub device-identity connection-string show -n {iothub_name} -d vehicle1
```

4. Store your device connection string in the environment variable named `CS_VEHICLE_1`.
5. You can turn on monitoring of messages delivered by routing capability via using CLI

```azure cli
az iot hub monitor-events -n {iothub_name} -p all
```

6. Use the device sample using the instructions below to publish to the topic.

  * If you haven't installed the required modules, follow the instructions in the [python README file](../python/README.md).
  * Make sure you have the `iothub-broker` virtual environment activated by running `source ~/env/iothub-broker/bin/activate` in Linux or `env/iothub-broker/bin/activate` in Windows
  * Make sure you have the `CS_VEHICLE_1` environment variable set to the connection string for your `vehicle1` device identity.
  * Run the sample within `Scenario1-broker-messages-routing` using the below command
    ```
    python python/publish_1.py
    ```
7. Below is the sample output of events.
  ```
  {
    "event": {
        "origin": "vehicle1",
        "module": "",
        "interface": "",
        "component": "",
        "properties": {
            "application": {}
        },
        "annotations": {
            "iothub-connection-device-id": "vehicle1",
            "iothub-connection-auth-generation-id": "637661152537314785",
            "iothub-enqueuedtime": 1630520083289,
            "iothub-message-source": "broker",
            "mqtt-qos": "1",
            "mqtt-topic": "vehicles/vehicle1/GPS/position",
            "x-opt-sequence-number": 19,
            "x-opt-offset": "6536",
            "x-opt-enqueued-time": 1630520083476
        },
        "payload": "{\"latitude\": 46.63962283908785, \"longitude\": -122.12718926895407, \"index\": 1}"
    }
}
```
