This scenario simulates cloud to device commands to several devices and can be leveraged for use cases such as sending alerts to devices. Consider the use case where a fleet management service needs to send a weather alert to all the vehicles in the fleet.  

 

Configure TopicSpace using the Azure CLI command guidance below: 
```azurecli
az iot hub topic-space create --topic-space-name mytopicspace --topic-template "commands/request/${principal.deviceid}/#" --type LowFanout --hub-name myhub 

az iot hub topic-space create --topic-space-name servicetopicspace --topic-template "commands/request/+/#" --type PublishOnly --hub-name myhub 
  ```
  For more details see Topic Spaces and Topic Templates (**TODO** Add link to section)

2. Register devices using the [Azure CLI](https://docs.microsoft.com/cli/azure/iot/hub/device-identity?view=azure-cli-latest#az_iot_hub_device_identity_create) 
3. Download the SDK samples (**TODO** SDK team to add git link for these)
4. Use the solution code (**TODO** LINK) to publish to the topic.
5. Use the device sample (**TODO** LINK) to subscribe to the topic.
