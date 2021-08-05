# Scenario 2 – Fan-out (one-to-many) messages over custom topics

This scenario simulates cloud to device commands to several devices and can be leveraged for use cases such as sending alerts to devices. Consider the use case where a fleet management service needs to send a weather alert to all the vehicles in the fleet.  

| Device | Role| Topic |
| -------- | --------------- |---------- |
| fleet_mgt_device | publisher | vehicles/alerts/weather/alert1  |
| vehicle1 | subscriber | vehicles/alerts/# |
| vehicle2 | subscriber | vehicles/alerts/# |

1. Configure TopicSpace using the Azure CLI command guidance below:

```azurecli
az iot hub topic-space create -n myhub --tsn alerts_ts --tst LowFanout --template 'vehicles/alerts/#'
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

3. Download the SDK samples (**TODO** SDK team to add git link for these)
4. Use the solution code (**TODO** LINK) to publish to the topic.
5. Use the device sample (**TODO** LINK) to subscribe to the topic.
