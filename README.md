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
 
## Resources

(Any additional resources or related projects)

