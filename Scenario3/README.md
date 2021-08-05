
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
3. Download the SDK samples (**TODO** SDK team to add git link for these)
4. Use the solution code (**TODO** LINK) to publish to the topic.
5. Use the device sample (**TODO** LINK) to subscribe to the topic and receive messages.

 
