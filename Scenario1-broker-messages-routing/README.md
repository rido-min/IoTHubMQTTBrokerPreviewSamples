# Scenarios 1 - Route data published on a topic to the built-in-endpoint

This scenario showcases how to configure route to send filtered messages from a custom topic to the built-in Event Hubs endpoint. Consider a use case where one needs to identify location of vehicles. The vehicles publish their GPS data on topics with their device ID in the path, for example `vehicles/<VIN>/GPS`. This scenario also showcases routing query and message enrichments which are existing IoT Hub message routing capabilities. Also see [routing](https://github.com/Azure/IoTHubMQTTBrokerPreviewSamples#message-routing-for-mqtt-broker-enabled-iot-hubs)

| Device | Role| Topic | Topic Template | Topic Space Type|
| -------- | --------------- |---------- |---------- |---------- |
| vehicle1 | publisher | vehicles/vehicle1/GPS | vehicles/${principal.deviceid}/GPS/# | PublishOnly|

1. Configure TopicSpace using the Azure CLI command guidance below:

 ```azurecli
az iot hub topic-space create -n myhub --tsn publisher_ts --tst PublishOnly --template 'vehicles/${principal.deviceid}/GPS/#'
```

  For more details see [Topic Spaces](https://github.com/Azure/IoTHubMQTTBrokerPreviewSamples#topic-spaces)

2. Register devices using the [Azure CLI](https://docs.microsoft.com/cli/azure/iot/hub/device-identity?view=azure-cli-latest#az_iot_hub_device_identity_create)

```azure cli
az iot hub device-identity create -n myhub -d vehicle1 --am shared_private_key
az iot hub device-identity connection-string show -n myhub -d vehicle1
```

3. Download the SDK samples (**TODO** SDK team to add git link for these)
4. Use the device sample (**TODO** LINK) to publish to the topic
5. You can monitor volume of messages delivered and troubleshoot routing via using CLI command - **az iot hub monitor-events**
