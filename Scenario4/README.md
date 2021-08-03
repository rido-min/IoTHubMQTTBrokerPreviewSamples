## Scenario 4– One to one messaging over custom topics  

This scenario simulates publishing messages from one client to another. Consider a use case where a user can unlock their car from a mobile app. 

 
Configure TopicSpace using the Azure CLI command guidance below: 

az iot hub topic-space create --topic-space-name mytopicspace --topic-template "vehicles/+/GPS” --type LowFanout --hub-name myhub 

az iot hub topic-space create --topic-space-name servicetopicspace --topic-template "vehicles/${principal.deviceid }/GPS”--type PublishOnly --hub-name myhub 

For more details see Topic Spaces and Topic Templates 

Register devices to your IoT Hub using Azure Portal. See instructions.Register device identities using the CLI  

Download the SDK samples (SDK team to add git link for these). (Microsoft internal: For bug bash Device sample use the end to end tests) 

Use the solution code to publish to the topic.  

Use the device sample to subscribe to the topic and receive messages. 
