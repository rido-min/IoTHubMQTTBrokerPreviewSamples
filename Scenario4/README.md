## Scenario 4 – One to one messaging over custom topics  

This scenario simulates the request-response messaging pattern. Request-response uses two topics: one for the request and one for the response. Consider a use case where a user can unlock their car from a mobile app. The request to unlock are use published on `vehicles/unlock/req/#` and the response of unlock operation are published on `vehicles/unlock/res/#`

| Device | Role| Topic | Topic Template | Topic Space Type|
| -------- | --------------- |---------- |---------- |---------- |
| mobile_device | publisher | vehicles/unlock/req/car1  | vehicles/unlock/req/#  | PublishOnly|
| car_device | subscriber | vehicles/unlock/req/car1 | vehicles/unlock/req/${principal.deviceid}/# | LowFanout|
| car_device | publisher | vehicles/unlock/res/car1 | vehicles/unlock/res/${principal.deviceid}/# | PublishOnly|
| mobile_device | subscriber | vehicles/unlock/res/car1  | vehicles/unlock/res/#  | LowFanout |

 
1. Configure TopicSpace using the Azure CLI command guidance below: 
 ```azurecli
az iot hub topic-space create -n myhub --tsn publisher_ts --tst PublishOnly --template 'vehicles/unlock/req/#' 'vehicles/unlock/res/${principal.deviceid}/#'

az iot hub topic-space create -n myhub --tsn subscriber_ts --tst LowFanout --template 'vehicles/unlock/req/${principal.deviceid}/#' 'vehicles/unlock/res/#'
```
  For more details see [Topic Spaces](https://github.com/Azure/IoTHubMQTTBrokerPreviewSamples#topic-spaces)

2. Register devices using the [Azure CLI](https://docs.microsoft.com/cli/azure/iot/hub/device-identity?view=azure-cli-latest#az_iot_hub_device_identity_create) 
```azure cli
az iot hub device-identity create -n myhub -d car_device --am shared_private_key
az iot hub device-identity connection-string show -n myhub -d car_device

az iot hub device-identity create -n myhub -d mobile_device --am shared_private_key
az iot hub device-identity connection-string show -n myhub -d mobile_device
```
3. Download the SDK samples (**TODO** SDK team to add git link for these)
4. Use the solution code (**TODO** LINK) to publish to the topic.
5. Use the device sample (**TODO** LINK) to subscribe to the topic and receive messages.
