# Scenario 2 – Fan-out (one-to-many) messages

This scenario simulates cloud to device commands to several devices and can be leveraged for use cases such as sending alerts to devices. Consider the use case where a fleet management service needs to send a weather alert to all the vehicles in the fleet.  

| Device | Role| Topic |
| -------- | --------------- |---------- |
| fleet_mgt_device | publisher | vehicles/alerts/weather/alert1  |
| vehicle1 | subscriber | vehicles/alerts/# |
| vehicle2 | subscriber | vehicles/alerts/# |

1. Configure TopicSpace using the Azure CLI command guidance below:

```azurecli
az iot hub topic-space create -n myhub --tsn alerts_ts --tst LowFanout --template 'vehicles/alerts/*'
  ```

  For more details see [Topic Spaces](https://github.com/Azure/IoTHubMQTTBrokerPreviewSamples#topic-spaces)

2. Register devices using the [Azure CLI](https://docs.microsoft.com/cli/azure/iot/hub/device-identity?view=azure-cli-latest#az_iot_hub_device_identity_create)

```azure cli
az iot hub device-identity create -n myhub -d fleet_mgt_device --am shared_private_key
az iot hub device-identity connection-string show -n myhub -d fleet_mgt_device

az iot hub device-identity create -n myhub -d vehicle1 --am shared_private_key
az iot hub device-identity connection-string show -n myhub -d vehicle1

az iot hub device-identity create -n myhub -d vehicle2 --am shared_private_key
az iot hub device-identity connection-string show -n myhub -d vehicle2
```

3. Store the device connection string for `fleet_mgt_device` in the environment variable `CS_FLEET_MGT_DEVICE` and store the connection strings for `vehicle1` and `vehicle2` in `CS_VEHICLE_1` and `CS_VEHICLE_2`
4. Use the device sample (instructoins below) to subscribe to the topic.
5. Use the solution code (instructions below) to publish to the topic.

## Running the python version of this sample:

1. If you haven't installed the required modules, follow the instructions in the [python README file](../python/README.md).
2. Open 2 command windows.  Activate the `iothub-broker` virtual environment in both.
3. In the first command window (the publisher window), set the `CS_FLEET_MGT_DEVICE` environment variable to the correct connection string.
3. In the second command window (the subscriber window), set the `CS_VEHICLE_1` and `CS_VEHICLE_2`  environment variable to the correct connection strings.
4. In the second (subscriber) command window, type `python python/subscribe_2.py` to run the subscriber app.
  * The subscriber app will create two threads and connect using both vehicle identities in a single app.
5. In the first (publisher) command window, type `python python/publish_2.py` to run the publisher app.

