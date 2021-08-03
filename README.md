# MQTT Broker Private Preview

The Microsoft Azure IoT team invites you and your organization to preview the MQTT Broker feature in IoT Hub. During this preview, we will provide full support with a high level of engagement from the Azure IoT product group. We look forward to your feedback as you leverage this capability for your IoT solutions. Please note that this preview is available by invitation only and requires an NDA. By participating the private preview, you are agreeing to the [Terms of Use](https://www.microsoft.com/legal/terms-of-use). 

## Overview of IoT Hub MQTT Broker  

IoT Hub MQTT broker is a pub/sub messaging broker, to enable secure transfer of messages to and from IoT devices and applications. You can now use MQTT’s flexible topic structure to send and receive messages from millions of devices and support flexible messaging patterns such as command and control and as well as broadcast messages to devices at scale.   

## Private preview program information 

* Timeline: The private preview will run till 10/15/2021(TBD:date to be updated based on deployment timelines). The private preview is only for testing. Please do NOT use it for your production.   
* Engagement: We will actively engage with you during the preview. At any point, feel free to connect with us for questions/concerns by creating issues in the Samples repo, confidential questions can be asked to  asrastog@microsoft.com  
* Feedback: At the end of the preview, will capture additional feedback using this form 
* Cost to use: For this release, MQTT Broker is available for no additional charge. Currently, you are charged when you send a message to an IoT Hub. You will only be charged once for that message, even if the message goes to multiple TopicSpaces or routing endpoints. Charges for IoT Hub remain unchanged and will be based on the tier purchased. Free, Basic and Standard tiers are supported. See IoT Hub pricing. 
* Cleanup: When the preview program ends, or when your tests are complete, we will delete the IoT Hubs that were created in this preview with MQTT Broker capabilities. All the data stored within the IoT Hub will also be deleted.   

## IoT Hub MQTT Broker Concepts 

* MQTT](https://mqtt.org/) standard protocol 
* [IoT Hub overview](https://docs.microsoft.com/azure/iot-hub/about-iot-hub)
* Topic Space and Topic Template (TODO: ADD LINK TO DOC HEADING) 
* Device authentication (TODO ADD LINK TO DOC HEADING)

## Capabilities available in this release 

This private preview provides the following capabilities - 

* MQTT features 
* Ability for registered devices to publish or subscribe to any custom topics 
* QoS 0 and QoS 1 
* Wildcards support for topics 
* Persistent session 
* For one-to-many messages, only low fan-out is supported. 
* MQTT v3.1.1 
* Topic Spaces and Topic Templates are new concepts introduced to simplify management of topics and topic filters used for pub/sub 
* Routing messages from MQTT Broker to custom endpoints 
* Code samples based on existing MQTT libraries 
* See throttle limits 

## Capabilities coming up in future releases 

The following features are not in scope for this release, but they will be supported in future -  

* Granular access control on pub/sub per topic/topic filter 
* Ability to publish messages to topics using HTTP 
* Last Will and Testament (LWT) 
* Retain flag 
* Metrics and diagnostic logs 
* Azure Portal support 
* Official IoT Hub libraries (aka SDKs) using existing MQTT libraries 
* Enhanced performance and scale limits 
* MQTT v5 (partial)
* Edge broker synchronization 

### Prerequisites 

1. To create an IoT Hub without routing use [ARM template](https://github.com/prashmo/azure-quickstart-templates/tree/master/quickstarts/microsoft.devices/iothub-mqtt-broker). 
2. To create an IoT Hub with routing use [ARM template](https://github.com/prashmo/azure-quickstart-templates/tree/master/quickstarts/microsoft.devices/iothub-mqtt-broker-route-messages).
*The new IoT Hub will be created in your subscription. This feature is not available for existing IoT Hubs in this release. 
*Central EUAP is the only region where MQTT Broker is currently supported.  
*You can customize the SKU and number of units for this IoT Hub in the template. 
*The template will also create an Event Hubs as a custom endpoint for your IoT Hub. 
*You can customize the routing query. See Routing limitations. 
*The routing source “MQTT Broker” is only supported in REST/ARM template. Azure Portal experience is not enabled for routing MQTT Broker topic messages in this release.  

3. Instructions for CLI  (TBD LINK) 

### Quickstart

Follow these steps to configure the IoT Hub MQTT Broker with one client enabled to publish and subscribe (many to many) –  
1. We will enable the feature for the subscription ID you shared in the sign up form emailed to you. 
2. Configure TopicSpace using the Azure CLI command guidance below: 
  az iot hub topic-space create --topic-name "SampleZero" --topic-template "sample/#" --type "LowFanout" 
  For more details see Topic Spaces and Topic Templates (TODO : LINK TO SECTION)
3. Register devices using [Azure CLI](https://docs.microsoft.com/cli/azure/iot/hub/device-identity?view=azure-cli-latest#az_iot_hub_device_identity_create) 
4. Clone the samples from this GitHub Repo and follow the [README instructions](https://github.com/Azure-Samples/IoTHub-MqttBroker-Samples)
* Update connection strings 
* Execute the publish and subscribe programs 
5. Observe messages published from the client to the devices. 

## Scenarios 

Here are a few additional scenarios you can try out. Please refer the details below about the limitations.  

### Scenario 1 – Route data published on a topic to the built-in-endpoint 

This scenario showcases how to configure route to send filtered messages from a custom topic to the built-in Event Hubs endpoint. Consider a use case where one needs to identify location of vehicles. The vehicles publish their GPS data on topics with their device ID in the path, for example “vehicles/<VIN>/GPS”. A message routing configuration is set up to route all MQTT Broker message to built-in Event Hubs. For instructions see [README](https://github.com/Azure/IoTHubMQTTBrokerPreviewSamples/tree/main/Scenario1).
  
### Scenario 2 – Fan-out (one-to-many) messages over custom topics 

This scenario simulates cloud to device commands to several devices and can be leveraged for use cases such as sending alerts to devices. Consider the use case where a fleet management service needs to send a weather alert to all the vehicles in the fleet. For instructions see [README](https://github.com/Azure/IoTHubMQTTBrokerPreviewSamples/tree/main/Scenario2).

### Scenario 3– Fan-in (many to one) messaging over custom topics  

This scenario simulates publishing messages from multiple clients to a single device. For instructions see [README](https://github.com/Azure/IoTHubMQTTBrokerPreviewSamples/tree/main/Scenario3)

### Scenario 4– One to one messaging over custom topics  

This scenario simulates publishing messages from one client to another. Consider a use case where a user can unlock their car from a mobile app. For instructions see [README](https://github.com/Azure/IoTHubMQTTBrokerPreviewSamples/tree/main/Scenario4)
 
## Topic Spaces and Topic Templates
  TODO : this section describes CRUD and limitations around TopicSpaces and topic templates

## Message routing for MQTT Broker enabled IoT Hubs 
  TODO : this section decribes new/limited routing for broker messages

** System properties added
** What query conditions for broker topics 
** What is going to continue to work (twin) 
** What will not work (body query) 
* What kinds of Message Routing capabilities are supported? 
* MQTT Broker messages support routing capabilities mostly same as existing one: 
** Same types of custom endpoints 
** same filtering/query capabilities in routing, with exception of query based on message body 
* Some behaviors are different and worth to point out: 
** Query based on message body is not available and will be later. 
** Unlike existing Hub Telemetry, MQTT messages WON'T flow to built-in endpoint automatically. Customers need explicitly set routing for MQTT custom topics as source to the choice of endpoint (built-in Event Hubs, or other custom endpoints).   

  
To learn more about IoT Hub routing, please visit [Understand Azure IoT Hub message routing](https://docs.microsoft.com/en-us/azure/iot-hub/iot-hub-devguide-messages-d2c)
  
## Throttle limits 

For this release, the following limits are imposed to protect the services and ensure performance. The limits might be revised for future releases. 
  
## Reference of Updated Hub APIs  

If you do not want to use the  samples, then you can use these APIs to connect device to IoT Hub. 
[TODO- Max] – also where in the doc or instructions should customer leverage this? 
PR Created to update doc - https://github.com/MicrosoftDocs/azure-docs-pr/pull/167226 . Need comments in PR for guidance around updates. 

*What would happen to existing Hub MQTT?  
IoT Hub will be backward compatible. So the MQTT as-is will continue be supported.   

*How is Broker related with existing D2C, direct method, etc?  

IoT Hub currently supports seven ways of communicating or transferring data from devices (see illustration below). By adding an MQTT broker, we are adding an additional way to communicate with devices that allows us to connect millions of existing devices that reply on the MQTT broker functionality.  

*Is Hub Broker compatible with MQTT protocol? 

IoT Hub MQTT Broker is intended to be fully compliant with MQTT protocols, with a few caveats: 
The broker supports MQTT v3.1.1 for this release and will support v5 in future releases.  
The broker supports Qos 0 and 1. Right now we don’t have plan to support QoS 2 though.  
Not all MQTT features are available at this release (see the Capabilities section above). We will bring more features along our roadmap.  

We intend to provide consistent experience across IoT Edge Broker and IoT Hub Broker. So devices can connect either IoT Hub or IoT Edge without awareness of the target. However, some MQTT features might be available to IoT Edge sooner.  

 

### Frequently asked questionsFrequently asked questions 
* What happens if your device disconnects (session cleanup) 
  
## Other Resources

(Any additional resources or related projects)

