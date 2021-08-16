
# Scenario 3 – Fan-in (many to one) messaging

This scenario simulates many-to-one communication pattern. Consider a use case where one needs to identify location of vehicles on a map.

| Device | Role| Topic | Topic Template | Topic Space Type|
| -------- | --------------- |---------- |---------- |---------- |
| map_device | subscriber | vehicles/+/GPS | vehicles/+/GPS/# | LowFanout|
| vehicle1 | publisher | vehicles/vehicle1/GPS | vehicles/${principal.deviceid}/GPS/# | PublishOnly|
| vehicle2 | publisher | vehicles/vehicle2/GPS | vehicles/${principal.deviceid}/GPS/# | PublishOnly|

1. Configure TopicSpace using the Azure CLI command guidance below:

 ```azurecli
az iot hub topic-space create -n myhub --tsn publisher_ts --tst PublishOnly --template 'vehicles/${principal.deviceid}/GPS/#'

az iot hub topic-space create -n myhub --tsn subcriber_ts --tst LowFanout --template 'vehicles/+/GPS/#'
```

  For more details see [Topic Spaces](https://github.com/Azure/IoTHubMQTTBrokerPreviewSamples#topic-spaces)

2. Register devices using the [Azure CLI](https://docs.microsoft.com/cli/azure/iot/hub/device-identity?view=azure-cli-latest#az_iot_hub_device_identity_create)

```azure cli
az iot hub device-identity create -n myhub -d vehicle1 --am shared_private_key
az iot hub device-identity connection-string show -n myhub -d vehicle1

az iot hub device-identity create -n myhub -d vehicle2 --am shared_private_key
az iot hub device-identity connection-string show -n myhub -d vehicle2

az iot hub device-identity create -n myhub -d map_device --am shared_private_key
az iot hub device-identity connection-string show -n myhub -d map_device
```

3. Store the device connection string for `map_device` in the environment variable `CS_MAP_DEVICE` and store the connection strings for `vehicle1` and `vehicle2` in `CS_VEHICLE_1` and `CS_VEHICLE_2`
4. Use the solution sample (instructions below) to subscribe to the topic and receive messages.
5. Use the device code (instructions below) to publish to the topic.

## Running the python version of this sample:

1. If you haven't installed the required modules, follow the instructions in the [python README file](../python/README.md).
2. Open 2 command windows.  Activate the `iothub-broker` virtual environment in both.
3. In the first command window (the publisher window), set the `CS_VEHICLE_1` and `CS_VEHICLE_2`  environment variable to the correct connection strings.
3. In the second command window (the subscriber window), set the `CS_MAP_DEVICE` environment variable to the correct connection string.
4. In the second (subscriber) command window, type `python python/subscribe_3.py` to run the subscriber app.
5. In the first (publisher) command window, type `python python/publish_3.py` to run the publisher app.
  * The publisher app will create two threads and connect using both vehicle identities in a single app.

