This scenario showcases how to configure route to send filtered messages from a custom topic to the built-in Event Hubs endpoint. Consider a use case where one needs to identify location of vehicles. The vehicles publish their GPS data on topics with their device ID in the path, for example “vehicles/<VIN>/GPS”. A message routing configuration is set up to route all MQTT Broker message to built-in Event Hubs.  


Configure TopicSpace using the Azure CLI command guidance below: 
 - az iot hub topic-space create --topic-space-name mytopicspace --topic-template "vehicles/${principal.deviceid}/GPS" --type PublishOnly --hub-name myhub 
 For more details see Topic Spaces and Topic Templates 

Register devices using the CLI  

Download the SDK samples (SDK team to add git link for these)

Use the device sample to publish to the topic 

You can monitor volume of messages delivered and troubleshoot routing via using CLI command- az iot hub monitor-events 

 