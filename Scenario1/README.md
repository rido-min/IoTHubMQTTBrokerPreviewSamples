## Scenarios 1 - Route data published on a topic to the built-in-endpoint

This scenario showcases how to configure route to send filtered messages from a custom topic to the built-in Event Hubs endpoint. Consider a use case where one needs to identify location of vehicles. The vehicles publish their GPS data on topics with their device ID in the path, for example “vehicles/<VIN>/GPS”. A message routing configuration is set up to route all MQTT Broker message to built-in Event Hubs.


1. Configure TopicSpace using one of the two Azure CLI command guidance below:
* If you know the IoT Hub name and resource group:
  ```azurecli
  az iot hub topic-space create -n {IoT_Hub_name} -g {IoT_Hub_resource_group}  --topic-space-name mytopicspace --topic-template "vehicles/${principal.deviceid}/GPS" --type PublishOnly
  ```
  ```azurecli
  az iot hub topic-space create -l {IoT_Hub_connection_string}  --topic-space-name mytopicspace --topic-template "vehicles/${principal.deviceid}/GPS" --type PublishOnly
  ```
  For more details see Topic Spaces and Topic Templates (**TODO** Add link to section)

2. Register devices using the [Azure CLI](https://docs.microsoft.com/cli/azure/iot/hub/device-identity?view=azure-cli-latest#az_iot_hub_device_identity_create)
3. Download the SDK samples (**TODO** SDK team to add git link for these)
4. Use the device sample (**TODO** LINK) to publish to the topic
5. You can monitor volume of messages delivered and troubleshoot routing via using CLI command - **az iot hub monitor-events**


