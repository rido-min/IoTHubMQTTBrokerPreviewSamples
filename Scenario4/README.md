## Scenario 4– One to one messaging over custom topics  

This scenario simulates publishing messages from one client to another. Consider a use case where a user can unlock their car from a mobile app. 

 
1. Configure TopicSpace using the Azure CLI command guidance below: 
 ```azurecli
az iot hub topic-space create --topic-space-name mytopicspace --topic-template "vehicles/+/GPS” --type LowFanout --hub-name myhub 

az iot hub topic-space create --topic-space-name servicetopicspace --topic-template "vehicles/${principal.deviceid }/GPS”--type PublishOnly --hub-name myhub 
```
  For more details see Topic Spaces and Topic Templates (**TODO** Add link to section)

2. Register devices using the [Azure CLI](https://docs.microsoft.com/cli/azure/iot/hub/device-identity?view=azure-cli-latest#az_iot_hub_device_identity_create) 
3. Download the SDK samples (**TODO** SDK team to add git link for these)
4. Use the solution code (**TODO** LINK) to publish to the topic.
5. Use the device sample (**TODO** LINK) to subscribe to the topic and receive messages.
