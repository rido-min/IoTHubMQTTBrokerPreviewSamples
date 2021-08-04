# MQTT Broker Private Preview

The Microsoft Azure IoT team invites you and your organization to preview the MQTT Broker feature in IoT Hub. During this preview, we will provide full support with a high level of engagement from the Azure IoT product group. We look forward to your feedback as you leverage this capability for your IoT solutions. Please note that this preview is available by invitation only and requires an NDA. By participating the private preview, you are agreeing to the [Terms of Use](https://www.microsoft.com/legal/terms-of-use).

## Overview of IoT Hub MQTT Broker

IoT Hub MQTT broker is a pub/sub messaging broker, to enable secure transfer of messages to and from IoT devices and applications. You can now use MQTT’s flexible topic structure to send and receive messages from your devices/services and support flexible messaging patterns such as command and control and as well as broadcast messages to devices/services. 

## Private preview program information

* **Timeline**: The private preview will run till 11/11/2021. The private preview is only for testing. Please do NOT use it for your production. 
* **Engagement**: We will actively engage with you during the preview. At any point, feel free to connect with us for questions/concerns by creating issues in the Samples repo, confidential questions can be asked to iothubmqttbroker@microsoft.com.
* **Feedback**: At the end of the preview, will capture additional feedback using [this form](https://forms.office.com/Pages/ResponsePage.aspx?id=v4j5cvGGr0GRqy180BHbR_mpSbs5LlNPijuErBTOYwFUOUxYUFM3MkJZM1dZWlBKVUFJTVIzQTJDTC4u)
* **Cost to use**: For this release, MQTT Broker is available for no additional charge. Currently, you are charged when you send a message to an IoT Hub. You will only be charged once for that message, even if the message goes to multiple TopicSpaces or routing endpoints. Charges for IoT Hub remain unchanged and will be based on the tier purchased. Free, Basic and Standard tiers are supported. See IoT Hub pricing.
* **Cleanup**: When the preview program ends, or when your tests are complete, we will delete the IoT Hubs that were created in this preview with MQTT Broker capabilities. All the data stored within the IoT Hub will also be deleted.

## IoT Hub MQTT Broker Concepts

* [MQTT standard protocol](https://mqtt.org/)
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

* The new IoT Hub will be created in your subscription. This feature is not available for existing IoT Hubs in this release.
* Central EUAP is the only region where MQTT Broker is currently supported.
* You can customize the SKU and number of units for this IoT Hub in the template.
* The template will also create an Event Hubs as a custom endpoint for your IoT Hub.
* You can customize the routing query. See Routing limitations.
* The routing source “MQTT Broker” is only supported in REST/ARM template. Azure Portal experience is not enabled for routing MQTT Broker topic messages in this release.
4. If you don't have an Azure subscription, [create one for free](https://azure.microsoft.com/free/?WT.mc_id=A261C142F) before you begin.
5. Azure CLI. You can run all commands in this quickstart using the Azure Cloud Shell, an interactive CLI shell that runs in your browser. If you use the Cloud Shell, you don't need to install anything. If you prefer to use the CLI locally, this quickstart requires Azure CLI version 2.17.1 or later. Run az --version to find the version. To install or upgrade, see [Install Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli).
6. To use the Azure IoT extension for Azure CLI with Topic Space, first remove the current Azure IoT extension using:
  ```
  az extension remove -n azure-iot
  ```
  Then, run the following command after you installed an Azure CLI version of 2.17.1 or later:
  ```
  az extension add --source 'https://topicspaceapp.blob.core.windows.net/files/azure_iot-255.255.3-py3-none-any.whl'
  ```
  For more details on the Azure IoT extension for Azure CLI see [here](https://github.com/Azure/azure-iot-cli-extension).

### Quickstart

Follow these steps to configure the IoT Hub MQTT Broker with one client enabled to publish and subscribe (many to many) –
1. We will enable the feature for the subscription ID you shared in the sign up form emailed to you. If you haven't responded, please fill out [this form](https://aka.ms/IoTHubMQTTBrokerPreviewSignup)
3. Configure TopicSpace using the Azure CLI command guidance below:
  ```azurecli
  az iot hub topic-space create --topic-name "SampleZero" --topic-template "sample/#" --type "LowFanout"
  ```
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

### Scenario 5: Routing Query on system property (TODO, can we make this part of scn 1)?

### Scenario 6: Apply message enrichment to broker message being routed (TODO, can we make this part of scn 1)?

### Scenario 7: Pub/sub to any non-system topic custom ($)


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


| Properties | Keyword for routing query|
| -------- | --------------- |
|  iothub-connection-device-id | connectionDeviceId |
|  iothub-connection-module-id | connectionModuleId |
|  iothub-connection-auth-generation-id | connectionDeviceGenerationId |
|  iothub-connection-auth-method | connectionAuthMethod |
|  iothub-enqueuedtime | enqueuedTime |
|  Mqtt-topic | Mqtt-topic |
|  Mqtt-qos | Mqtt-qos |
|  iothub-message-source | iothub-message-source |


To learn more about IoT Hub routing, please visit [Understand Azure IoT Hub message routing](https://docs.microsoft.com/en-us/azure/iot-hub/iot-hub-devguide-messages-d2c)

## Throttle limits

For this release, the following limits are imposed to protect the services and ensure performance. The limits might be revised for future releases.
 Table in section 9.3 in [instructions doc](https://microsoft.sharepoint.com/:w:/r/teams/Azure_IoT/_layouts/15/Doc.aspx?sourcedoc=%7B567cfc86-23b8-43db-8d8b-48aafc2c3b8b%7D&action=edit&wdPid=1054f99c&share=IQGG_HxWuCPbQ42LSKr8LDuLAVwreCP06LQbBlEbM_eeEs0&cid=27c9a266-2a79-44e0-a5f8-e040ebea8b9d)

  **TBD** Review TABLE - We should add a DESCRIPTION COLUMN

### Broker pub/sub

| Category | Feature | Limit |
| -------- | ---- | ----------- |
| connect | Connect requests per second per client ID | 1 |
| connect | Keep alive limit (max delay for liveness check - 28.5min) | 19 mins |
| pub inbound | Inbound publish requests per second per IoT Hub per unit (counted together with D2C) | Varies per SKU, details in [Device-to-cloud sends](https://docs.microsoft.com/azure/iot-hub/iot-hub-devguide-quotas-throttling#operation-throttles) |
| pub inbound | inbound Publish requests per second per connection (counted with D2C) | 100 |
| pub inbound | Maximum inbound unacknowledged QoS 1 publish requests (Receive Maximum (maximum number of allowed outstanding unacknowledged PUBLISH packets (in client-server direction) with QoS: 1)). If Hub failed to ack pub request for more than the limit, Hub will reject new pub request and disconnect the client. | 16 |
| sub | total Subscriptions (system topics are not counted here) per Hub | 1 million (**TBD** CONFIRM) |
| sub | maximum subscriptions (system topics are not counted here) per connection (Single client can have no more than X subscriptions (**TBD** CONFIRM TEXT).| 50 |
| sub | individual Subscriptions (system topics are not counted here)  per second per Hub per unit | same as existing (**TBD** confirm limit) |
| sub | Maximum subscriptions per subscribe request | 8 |
| throughput | Throughput per second per connection  | (maximum inbound and outbound publish rates * number of 4KB) (**TBD** CONFIRM) |

### Topics
| Category | Feature | Limit |
| -------- | ---- | ----------- |
| topic space | lowFanout: Total subscriptions per substituted values set (e.g. for devices/{deviceID}/# filter, devices/d1/#, devices/d2/# are counted toward this limit.  | 50 |
| topic space | lowFanout: Message rate per topic | 100 messages/second |
| topic space | lowFanout: Total subscriptions | Unbounded (up to the limit for the hub) (**TBD** Confirm text) |
| topic | Maximum number of slashes in topic and topic filter | 10 |
| topic | Topic size | 256 bytes |
| topic space | maximum of topic templates that can have within a topic space | 5 |
| topic space | maximum number of topic spaces per Hub | 10 |
| topic space management APIs | requests/s | 1/s with burst 10/s |

## Test using Code (**TODO** RIDO/SEJAL)
At this point there is not an official Microsoft SDK to interact with the broker, instead we are creating samples using existing MQTT libraries, these samples include helper functions that can be used in your own applications. In the next release, We will provide a modular SDK, that will still require a 3rd party MQTT client.

We are providing sample code in Python using the Paho MQTT client (TBD if we can include .NET with MQTTnet) To connect to hub, the clients must follow the new authentication guidelines, once the client is connected regular pub/sub operations should work.


The samples use authentication based on SharedAccessKeys


## Reference of Updated Hub APIs

If you do not want to use the  samples, then you can use these APIs to connect device to IoT Hub.
[TODO- Prashali/Max] – also where in the doc or instructions should customer leverage this?
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

