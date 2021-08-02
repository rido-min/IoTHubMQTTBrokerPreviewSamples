This scenario simulates cloud to device commands to several devices and can be leveraged for use cases such as sending alerts to devices. Consider the use case where a fleet management service needs to send a weather alert to all the vehicles in the fleet.  

 

Configure TopicSpace using the Azure CLI command guidance below: 

az iot hub topic-space create --topic-space-name mytopicspace --topic-template "commands/request/${principal.deviceid}/#" --type LowFanout --hub-name myhub 

az iot hub topic-space create --topic-space-name servicetopicspace --topic-template "commands/request/+/#" --type PublishOnly --hub-name myhub 

For more details see Topic Spaces and Topic Templates 

Register devices using the CLI  

Download the SDK samples (SDK team to add git link for these)

Use the solution code to publish to the topic  

Use the device sample to subscribe to the topic.  