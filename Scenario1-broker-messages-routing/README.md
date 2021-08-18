# Scenarios 1 - Route data published on a topic to the built-in-endpoint

This scenario showcases how to configure route to send filtered messages from a custom topic to the built-in Event Hubs endpoint. Consider a use case where one needs to identify location of vehicles. The vehicles publish their GPS data on topics with their device ID in the path, for example `vehicles/<VIN>/GPS`. This scenario also showcases routing query and message enrichments which are existing IoT Hub message routing capabilities. Also see [routing](https://github.com/Azure/IoTHubMQTTBrokerPreviewSamples#message-routing-for-mqtt-broker-enabled-iot-hubs)

For this scenario, please ensure you have deployed a IoT Hub with routing using the [ARM template](https://github.com/prashmo/azure-quickstart-templates/tree/master/quickstarts/microsoft.devices/iothub-mqtt-broker-route-messages).

| Device | Role| Topic | Topic Template | Topic Space Type|
| -------- | --------------- |---------- |---------- |---------- |
| vehicle1 | publisher | vehicles/vehicle1/GPS | vehicles/${principal.deviceid}/GPS/# | PublishOnly|

1. Configure TopicSpace using the Azure CLI command guidance below:

 ```azurecli
az iot hub topic-space create -n {iothub_name} --tsn publisher_ts --tst PublishOnly --template 'vehicles/${principal.deviceid}/GPS/#'
```

  For more details see [Topic Spaces](https://github.com/Azure/IoTHubMQTTBrokerPreviewSamples#topic-spaces)

2. Register devices using the [Azure CLI](https://docs.microsoft.com/cli/azure/iot/hub/device-identity?view=azure-cli-latest#az_iot_hub_device_identity_create)

```azure cli
az iot hub device-identity create -n {iothub_name} -d vehicle1 --am shared_private_key
az iot hub device-identity connection-string show -n {iothub_name} -d vehicle1
```
3. If using tags in routing query, set up device with relevant tags.
```azure cli
az iot hub device-twin update -n {iothub_name} -d vehicle1 --tags '{"model": "model1"}'
```
4. Store your device connection string in the environment variable named `CS_VEHICLE_1`.
5. You can turn on monitoring of messages delivered by routing capability via using CLI 
```azure cli
az iot hub monitor-events -n {iothub_name}
```
6. Use the device sample (instructions below) to publish to the topic.


## Running the python version of this sample:

1. If you haven't installed the required modules, follow the instructions in the [python README file](../python/README.md).
2. Make sure you have the `iothub-broker` virtual environment activated by running `source ~/env/iothub-broker/bin/activate` in Linux or `env/iothub-broker/bin/activate` in Windows 
3. Make sure you have the `CS_VEHICLE_1` environment variable set to the connection string for your `vehicle1` device identity.
4. Type `python python/publish_1.py` to run the sample

