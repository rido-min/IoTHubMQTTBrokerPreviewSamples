# MQTT Broker Private Preview

The Microsoft Azure IoT team invites you and your organization to preview the MQTT Broker feature in IoT Hub. During this preview, we will provide full support with a high level of engagement from the Azure IoT product group. We look forward to your feedback as you leverage this capability for your IoT solutions. Please note that this preview is available by invitation only and requires an NDA. By participating the private preview, you are agreeing to the [Terms of Use](https://www.microsoft.com/legal/terms-of-use).

## Overview of IoT Hub MQTT Broker

IoT Hub MQTT broker is a pub/sub messaging broker, to enable secure transfer of messages to and from IoT devices and applications. You can now use MQTT’s flexible topic structure to send and receive messages from your devices/services and support flexible messaging patterns such as command and control and as well as broadcast messages to devices/services.

## Private preview program information

* **Timeline**: The private preview will run till 11/11/2021. The private preview is only for testing. Please do NOT use it for your production.
* **Engagement**: We will actively engage with you during the preview. At any point, feel free to connect with us for questions/concerns by creating issues in the Samples repo, confidential questions can be asked to iothubmqttbroker@microsoft.com.
* **Feedback**: At the end of the preview, will capture additional feedback using [this form](https://forms.office.com/Pages/ResponsePage.aspx?id=v4j5cvGGr0GRqy180BHbR_mpSbs5LlNPijuErBTOYwFUOUxYUFM3MkJZM1dZWlBKVUFJTVIzQTJDTC4u).
* **Cost to use**: For this release, MQTT Broker is available for no additional charge. Currently, you are charged when you send a message to an IoT Hub. You will only be charged once for that message, even if the message goes to multiple clients or routing endpoints. Charges for IoT Hub remain unchanged and will be based on the tier purchased. Free, Basic and Standard tiers are supported. See [IoT Hub pricing](https://azure.microsoft.com/en-us/pricing/details/iot-hub/).
* **Cleanup**: When the preview program ends, or when your tests are complete, we will delete the IoT Hubs that were created in this preview with MQTT Broker capabilities. All the data stored within the IoT Hub will also be deleted.

## IoT Hub MQTT Broker Concepts

* [MQTT standard protocol](https://mqtt.org/)
* [IoT Hub overview](https://docs.microsoft.com/azure/iot-hub/about-iot-hub)
* [Topic spaces](#topic-spaces)
* [Device authentication](#device-authentication)

## Capabilities available in this release

This private preview provides the following capabilities -

* MQTT v3.1.1
* Ability for registered devices to publish or subscribe to any topic
* QoS 0 and QoS 1
* Wildcards support for topics
* Persistent session
* For one-to-many messages, only low fan-out is supported.
* Topic Spaces is a new concept introduced to simplify management of topics used for pub/sub
* Routing messages from MQTT Broker to custom endpoints
* Code samples based on existing MQTT libraries
* See [throttle limits](#throttle-limits)

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
* IoT Edge broker

## Prerequisites

1. We will enable the feature for the subscription ID you shared in the sign up form emailed to you. If you haven't responded, please fill out [this form](https://aka.ms/IoTHubMQTTBrokerPreviewSignup)
2. To create an IoT Hub, use [ARM template](https://github.com/prashmo/azure-quickstart-templates/tree/master/quickstarts/microsoft.devices/iothub-mqtt-broker). 
   * The new IoT Hub will be created in your subscription.
   * If you don't have an Azure subscription, [create one for free](https://azure.microsoft.com/free/?WT.mc_id=A261C142F) before you begin. This feature is not available for existing IoT Hubs in this release.
   * Central EUAP is the only region where MQTT Broker is currently supported.
   * You can customize the SKU and number of units for this IoT Hub in the template.
3. Azure CLI.
   * This quickstart requires Azure CLI version 2.17.1 or later. Run the below command to find the version.
      ```azure cli
      az --version
      ```  
     To install or upgrade, see [Install Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli).
   * In this release, topic space management commands can be enabled as follows.

      Remove the current Azure IoT extension using:

        ``` azure cli
        az extension remove -n azure-iot
        ```
      Run the following command to re-add Azure IoT extension:

        ``` azure cli
        az extension add --source 'https://topicspaceapp.blob.core.windows.net/files/azure_iot-255.255.3-py3-none-any.whl'
        ```
For more details on the Azure IoT extension for Azure CLI see [here](https://github.com/Azure/azure-iot-cli-extension). For Windows, please use `PowerShell`.
  
4. Clone the [repo](https://github.com/Azure/IoTHubMQTTBrokerPreviewSamples)

 For all the scenarios below we have provided python sample code. Microsoft SDK to interact with the broker will be provided in the next release. Current samples use existing MQTT libraries and include helper functions that can be used in your own applications. We are providing sample code in Python using the Paho MQTT client. To connect to hub, the clients must follow the [new authentication guidelines](#device-authentication), once the client is connected regular pub/sub operations will work. The samples use authentication based on SharedAccessKeys.

## Quickstart

Let us get started with a hello world scenario, with a publisher and subscriber communicating on a topic.
Below table enumerate the devices, topics and topic space used in this example.
| Device | Role| Topic | Topic Template |
| -------- | --------------- |---------- |---------- |
| pub_device | publisher | sample/topic | sample/# |
| sub_device | subscriber | sample/topic | sample/# |

1. To enable pub/sub on `sample/#`, configure TopicSpace using the below Azure CLI command:

  ```azurecli
  az iot hub topic-space create -n {iothub_name} --tsn SampleZero --tst LowFanout --template sample/#
  ```

  For more details see [topic spaces](#topic-spaces).
  
2. Register publisher and subscriber devices using [Azure CLI](https://docs.microsoft.com/cli/azure/iot/hub/device-identity?view=azure-cli-latest#az_iot_hub_device_identity_create)
Additionally use `connection-string` command to fetch the connection strings for these devices.

```azurecli
az iot hub device-identity create -n {iothub_name} -d pub_device --am shared_private_key
az iot hub device-identity connection-string show -n {iothub_name} -d pub_device

az iot hub device-identity create -n {iothub_name} -d sub_device --am shared_private_key
az iot hub device-identity connection-string show -n {iothub_name} -d sub_device
```

3. To run the sample,

* Clone the [repo](https://github.com/Azure/IoTHubMQTTBrokerPreviewSamples)
* Follow the instructions in the [Python README](https://github.com/Azure/IoTHubMQTTBrokerPreviewSamples/tree/main/python/README.md) to configure your environment.
* Python quickstart sample code is in [python](https://github.com/Azure/IoTHubMQTTBrokerPreviewSamples/tree/main/python) directory.
* Set your `pub_device` connection string into the `CS_PUB` environment variable.
* Set your `sub_device` connection string into the `CS_SUB` environment variable.
* Run `python subscribe.py` to subscribe and run `python publish.py` to publish.

4. Observe messages delivered to subscriber.

Publisher sample output:
```
(iothub-broker) contoso@fabrikam:~/code/IoTHubMQTTBrokerPreviewSamples/python$ python publish.py
Starting connection
Waiting for CONNACK
Publishing to sample/topic at QOS=1
Publish returned rc=0: No error.
Waiting for PUBACK for mid=1
PUBACK received
Disconnecting
```

Subscriber sample output:
```
(iothub-broker) prashmo@prashmo7:~/code/IoTHubMQTTBrokerPreviewSamples/python$ python subscribe.py
Connecting
Subscribing to sample/# at qos 1
Subscription was granted with qos 1
Message received on topic sample/topic
Payload: {'latitude': 47.63962283908785, 'longitude': -122.12718926895407}
```

## Scenarios

Here are a few additional scenarios you can try out. Please refer the details below about the limitations.

### Scenario 1 – Route data published on a topic to the built-in-endpoint

This scenario showcases how to configure route to send filtered messages from broker to the built-in Event Hubs endpoint. Consider a use case where one needs to identify location of vehicles. For instructions see [README](https://github.com/Azure/IoTHubMQTTBrokerPreviewSamples/tree/main/Scenario1-broker-messages-routing).

### Scenario 2 – Fan-out (one-to-many) messages

This scenario simulates cloud to device commands to several devices and can be leveraged for use cases such as sending alerts to devices. Consider the use case where a fleet management service needs to send a weather alert to all the vehicles in the fleet. For instructions see [README](https://github.com/Azure/IoTHubMQTTBrokerPreviewSamples/tree/main/Scenario2-fan-out).

### Scenario 3 – Fan-in (many to one) messaging

This scenario simulates publishing messages from multiple clients to a single client. Consider a use case where one needs to identify location of vehicles on a map. For instructions see [README](https://github.com/Azure/IoTHubMQTTBrokerPreviewSamples/tree/main/Scenario3-fan-in)

### Scenario 4 – One to one messaging

This scenario simulates publishing messages from one client to another. Consider a use case where a user can unlock their car from a mobile app. For instructions see [README](https://github.com/Azure/IoTHubMQTTBrokerPreviewSamples/tree/main/Scenario4-request-response)

### Scenario 5 – Route and enrich messages published on a topic to the built-in-endpoint

This scenario showcases how to configure route to send filtered messages from broker to the built-in Event Hubs endpoint. This scenario also uses routing query and message enrichments which are existing IoT Hub message routing capabilities. Consider a use case where one needs to identify location of vehicles. For instructions see [README](https://github.com/Azure/IoTHubMQTTBrokerPreviewSamples/tree/main/Scenario5-message-routing-enrichments).

### Scenario 6 – X509 Authentication

This scenario shows how to connection to IoT Hub using X509 authentication.  For instructions see [README](https://github.com/Azure/IoTHubMQTTBrokerPreviewSamples/tree/main/Scenario6-x509-authentication).

## Topic Spaces
  
Topic space is a new concept introduced to simplify management of topics used for pub/sub.
  
### Terminology

**Topic space** – A topic space is a set of topics within a hub. Topic space is defined using MQTT topic filters with support for MQTT wildcards and variable substitutions. It can be used to limit the set of topics based on the properties of the MQTT device.

**Topic filter** – An [MQTT topic filter](http://docs.oasis-open.org/mqtt/mqtt/v3.1.1/os/mqtt-v3.1.1-os.html#_Toc398718106) is an MQTT topic, possibly with wildcards for one or more segments allowing it to match multiple MQTT topics. Supported wildcards are `+`, which matches a single segment and `#`, which matches zero or more segments at the end of the topic. See [Topic Wilcards](https://docs.oasis-open.org/mqtt/mqtt/v3.1.1/os/mqtt-v3.1.1-os.html#_Toc398718107) from the MQTT spec for more details.
  
**Topic template** – Topic templates are an extension of the topic filter that includes support for variables. This simplifies management for high scale applications. A topic space can consist of multiple topic templates.
For example, `vehicles/${principal.deviceid}/GPS/#`. Here, `${principal.deviceid}` part is the variable that substitutes into the device Id during an MQTT session.  

 **Variable** - A value in a topic template that will be filled in based on the properties of the authenticated device. A variable can represent a portion of a segment or an entire segment but cannot cover more than one segment.
For example, if we want the device to publish on its own topic, you can use the topic `vehicles/${principal.deviceId}/GPS/location`. For this topic template, `vehicle1` can only publish to `vehicles/vehicle1/GPS/location`. If `vehicle1` attempts to publish on topic `vehicles/vehicle2/GPS/location`, it will fail.

**Topic space type** - The type of the topic space. Must be one of `LowFanout` or `PublishOnly`. The low fanout type is needed to adjust for the expected number of devices receiving each message, while the publish only option makes a topic space useable only for publishing.

**Fanout** - The number of devices that will receive a given message. A low fanout message would be received by only a small number of devices. See [throttle limit](#throttle-limits)

### Topic space management operations

We support topic space CRUD using Azure CLI. See [prerequisites](#prerequisites).

#### Create topic space

  ```azurecli
  az iot hub topic-space create -n {iothub_name} --tsn samplezero --template sample/# --tst LowFanout
  ```

  Topic space CLI can also use be configured using IoT hub connection string
  
  ```azurecli
  az iot hub topic-space create -n {iothub_name} --tsn samplezero --template sample/# --tst LowFanout -l "##connectionString##"
  ```

#### Get topic space

  ```azurecli
  az iot hub topic-space show -n {iothub_name} --tsn samplezero
  ```

#### Update topic space

This can take up to 5 minutes to propagate. Type cannot be updated.

  ```azurecli
  az iot hub topic-space create -n {iothub_name} --tsn samplezero --template sample/# sampleupdate/#
  ```  

#### Delete topic space

This can take up to 5 minutes to propagate.

  ```azurecli
  az iot hub topic-space delete -n {iothub_name} --tsn samplezero
  ```

#### List topic spaces within a hub

  ```azurecli
  az iot hub topic-space list -n {iothub_name}
  ```

### Topic space considerations

* To publish or subscribe to any topic, a matching topic space must be configured.
Pub/sub on system topics do not require topic spaces.
* The only topic space types that are supported in this release are `LowFanout` and `PublishOnly`.  
* Low Fanout topic spaces cannot overlap each other. Trying to create a new topic space that overlaps with an existing result in a conflict error. A conflict exists if a topic could exist in more than one topic space.
For example, `vehicles/vehicle1/telemetry/#` and `vehicles/+/telemetry/#` conflict because the second template covers the first one via wildcard.
Similarly, `vehicles/vehicle1/telemetry/#` and `vehicles/${principal.deviceId}/telemetry/#` conflict because in the second template the segment with variable is treated as single level wildcard `+` and hence, covers the first topic template.
`PublishOnly` topic spaces can overlap with `LowFanout` topic spaces.
* The only two variables available in this release are `${principal.deviceid}` and `${dollar}`.
  Example 1: `vehicles/${principal.deviceId}/GPS/location` substitutes the device ID in the topic template.
  Example 2: For topic filter `vehicles\$telemetry\#`, `$` can be escaped with `vehicles\${dollar}telemetry\#`.
* Topic space updates take up-to 5 minutes to propagate.  
* Topic space `type` is immutable. To change the topic space `type` delete the topic space and create a new topic space with the desired `type`.
* Topic templates use special characters `$` and `|` and these need to be escaped differently based on the shell being used. For Powershell, please see examples below.
'"vehicles/${principal.deviceId|dollar}/#"'
'vehicles/${principal.deviceId"|"dollar}/#'
  
## Existing IoT Hub features

IoT Hub delivers messaging via telemetry, device twin, direct method and C2D commands. These features will continue to work with existing SDKs. With introduction of MQTT broker, we are in process of updating the SDKs. Meanwhile, to utilize these capabilities, please see [MQTT 3.1.1 support for IoT Hub](https://github.com/Azure/IoTHubMQTTBrokerPreviewSamples/blob/main/references/mqtt-3-1-1-reference-generated.md)

### Device authentication

With the introduction of MQTT broker, we have revamped the [device authentication](https://github.com/Azure/IoTHubMQTTBrokerPreviewSamples/blob/main/references/mqtt-3-1-1-conceptual.md#authentication) format.

### IoT Hub API reference

System topics supported by IoT Hub have been updated. Please see [details](https://github.com/Azure/IoTHubMQTTBrokerPreviewSamples/blob/main/references/mqtt-3-1-1-conceptual.md#message-topics-and-subscriptions). The device SDK will be updated in future release.

## Message routing for MQTT Broker enabled IoT Hubs

Routing source `MQTTBrokerMessages` is only supported in REST/ARM template. Azure Portal experience is not enabled for routing MQTT Broker topic messages in this release.
Use [ARM template](https://github.com/prashmo/azure-quickstart-templates/tree/master/quickstarts/microsoft.devices/iothub-mqtt-broker-route-messages) to deploy routing enabled hub. 

New system properties `mqtt-topic` and `mqtt-qos` have been added that can be utilized for [routing query](https://docs.microsoft.com/azure/iot-hub/iot-hub-devguide-routing-query-syntax). The table below lists all the system properties that are supported when the routing broker messages.

| Properties | Keyword for routing query| Description |
| -------- | --------------- |---------- |
|  iothub-connection-device-id | connectionDeviceId | An ID set by IoT Hub on broker messages. It contains the deviceId of the device that sent the message. |
|  iothub-connection-module-id | connectionModuleId | An ID set by IoT Hub on broker messages. It contains the moduleId of the device that sent the message. |
|  iothub-connection-auth-generation-id | connectionDeviceGenerationId | An ID set by IoT Hub on broker messages. It contains the connectionDeviceGenerationId (as per [device identity properties](https://docs.microsoft.com/en-us/azure/iot-hub/iot-hub-devguide-identity-registry#device-identity-properties)) of the device that sent the message.|
|  iothub-enqueuedtime | enqueuedTime | Date and time the [Device-to-Cloud](https://docs.microsoft.com/azure/iot-hub/iot-hub-devguide-d2c-guidance) message was received by IoT Hub. |
|  mqtt-topic | mqtt-topic | Topic on which message was published, this is set by IoT Hub on messages sent to broker topics. |
|  mqtt-qos | mqtt-qos | QoS level of the message published, this is set by IoT Hub on messages sent to broker topics. |
|  iothub-message-source | iothub-message-source | The routing message source |

* Querying on body and application properties is not supported for `broker` messages.
* Unlike existing Hub Telemetry, broker messages will not flow to the built-in endpoint by default. Customers need to explicitly configure routing for broker as source to send data to the desired endpoint (built-in Event Hubs, or other custom endpoints).  
* When routing messages for broker the dropped messages will not go to the fallback route if the query condition is not met.
  
To learn more about IoT Hub routing, please visit [Understand Azure IoT Hub message routing](https://docs.microsoft.com/en-us/azure/iot-hub/iot-hub-devguide-messages-d2c)

## Limits

For this release, the following limits are supported. The limits might be revised for future releases.

### Broker

| Category | Description | Limit |
| -------- | ---- | ----------- |
| connect | Connect requests per second per client ID | Not enforced. Recommend using 1 request/second |
| connect | Keep alive limit | 19 mins |
| disconnect | Maximum time before disconnected persisted session is cleaned up | 1 hour|
| pub inbound | Inbound publish requests per second per IoT Hub per unit (counted together with D2C) | Varies per SKU, details in [Device-to-cloud sends](https://docs.microsoft.com/azure/iot-hub/iot-hub-devguide-quotas-throttling#operation-throttles) |
| pub inbound | Maximum inbound unacknowledged QoS 1 publish requests | 16 |
| sub | Maximum subscriptions per client ID (topics starting with `$az/iot` are also counted) | 50 |
| sub | Maximum topic filters per subscribe request | 8 |

### Topic Spaces Limits

| Category | Description | Limit |
| -------- | ---- | ----------- |
| topic space | LowFanout: Total subscriptions per substituted topic template (e.g. for `devices/${principal.deviceid}/#` you can have 10 subscriptions for topics for device d1, and independently 10 subscriptions for topics for device d2 | 10 |
| topic | Maximum number of slashes in topic and topic filter | 10 |
| topic | Topic size | 256 bytes |
| topic space | Maximum number of topic templates within a topic space | 5 |
| topic space | Maximum number of topic spaces per IoT Hub | 10 |
| topic space management APIs | Maximum requests per second | 1/s; with burst 10/s |

### Frequently asked questions
  
* Is monitoring metrics and logging is available?

    None in this release. We will add monitoring metrics and diagnostic logs in the next release.

* What happens if device attempts to pub/sub on a topic when a matching topic space is not found?

    Device connection will be closed. We will add monitoring metrics and diagnostic logs in the next release.

* How long does it take for topic space updates to propagate?

   It takes up-to 5 minutes to propagate a topic space update.

* Can I use my existing SDK?

    You can use any standard MQTT client SDK. See SDK samples [here](https://github.com/Azure/IoTHubMQTTBrokerPreviewSamples).
* How can I fix `Subscription was rejected` error when running the samples?

  Topic space updates take up-tp 5 minutes to propagate, please retry the samples post that.
