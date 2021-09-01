# Scenario 4 – One to one messaging 

This scenario simulates the request-response messaging pattern. Request-response uses two topics, one for the request and one for the response. 

Consider a use case where a user can unlock their car from a mobile app. The request to unlock are use published on `vehicles/unlock/req/<carDeviceId>/<mobileDeviceId>` and the response of unlock operation are published on `vehicles/unlock/res/<mobileDeviceId>/<carDeviceId>`.

| Device | Role| Topic/Topic Filter | Topic Template | Topic Space Type
| -------- | --------------- |---------- |---------- |---------- |
| mobile_device | publisher | vehicles/unlock/req/car1/mobile1  | vehicles/unlock/req/+/${principal.deviceid}  | PublishOnly|
| car_device | subscriber | vehicles/unlock/req/car1/# | vehicles/unlock/req/${principal.deviceid}/# | LowFanout|
| car_device | publisher | vehicles/unlock/res/mobile1/car1 | vehicles/unlock/res/+/${principal.deviceid} | PublishOnly|
| mobile_device | subscriber | vehicles/unlock/res/mobile1/#  | vehicles/unlock/res/${principal.deviceid}/#  | LowFanout |

1. Configure TopicSpace using the Azure CLI command guidance below:

 ```azurecli
az iot hub topic-space create -n {iothub_name} --tsn publisher_ts --tst PublishOnly --template 'vehicles/unlock/req/+/${principal.deviceid}' 'vehicles/unlock/res/+/${principal.deviceid}'

az iot hub topic-space create -n {iothub_name} --tsn subscriber_ts --tst LowFanout --template 'vehicles/unlock/req/${principal.deviceid}/#' 'vehicles/unlock/res/${principal.deviceid}/#'
```

  For more details see [Topic Spaces](https://github.com/Azure/IoTHubMQTTBrokerPreviewSamples#topic-spaces)

2. Register devices using the [Azure CLI](https://docs.microsoft.com/cli/azure/iot/hub/device-identity?view=azure-cli-latest#az_iot_hub_device_identity_create)

```azure cli
az iot hub device-identity create -n {iothub_name} -d car_device --am shared_private_key
az iot hub device-identity connection-string show -n {iothub_name} -d car_device

az iot hub device-identity create -n {iothub_name} -d mobile_device --am shared_private_key
az iot hub device-identity connection-string show -n {iothub_name} -d mobile_device
```

3. Store the device connection string for `mobile_device` in the environment variable `CS_MOBILE_DEVICE` and store the connection strings for `car_device` in `CS_CAR_DEVICE`.
4. Use the car device sample (instructions below) to subscribe to the topic, receive messages, and return responses
5. Use the mobile device sample code (instructions below) to publish to the topic and receive responses.


## Running the python version of this sample:

1. If you haven't installed the required modules, follow the instructions in the [python README file](../python/README.md).
2. Open 2 command windows.  Activate the `iothub-broker` virtual environment in both.
3. In the first command window (the mobile device window), set the `CS_MOBILE_DEVICE` and `CS_CAR_DEVICE`  environment variable to the correct connection strings.
4. In the second command window (the car device window), set the `CS_CAR_DEVICE` environment variable to the correct connection string.
5. In the second (car device) command window, type `python python/car_device.py` to run the car device app.
6. In the first (mobile device) command window, type `python python/mobile_device.py` to run the mobile device app.

