# Scenario 6 – x509 authentication

This scenario shows how to authenticate with IoTHub using an x509 certificate. A modified publish/subscribe example from the quickstart is used to show successful communication.

| Device | Role| Topic | Topic Template |
| -------- | --------------- |---------- |---------- |
| x509_pub_device | publisher | sample/topic | sample/# |
| x509_sub_device | subscriber | sample/topic | sample/# |

1. Configure TopicSpace using the Azure CLI command guidance below:

Run this command to check the topic spaces in your hub. If you see a `LowFanout` topic space for the topicTemplate `sample/#`, then you can skip to the next step.

 ```azurecli
az iot hub topic-space list -n {iothub_name}"
```

If you do not have a topic space for `sample/#`, you can add it as follows:

 ```azurecli
az iot hub topic-space create -n {iothub_name} --tsn SampleZero --tst LowFanout --template sample/#
```

  For more details see [Topic Spaces](https://github.com/Azure/IoTHubMQTTBrokerPreviewSamples#topic-spaces)

2. Register devices using the [Azure CLI](https://docs.microsoft.com/cli/azure/iot/hub/device-identity?view=azure-cli-latest#az_iot_hub_device_identity_create)

```azure cli
mkdir ./certs
az iot hub device-identity create -n {iothub_name} -d x509_pub_device --am x509_thumbprint --output-dir ./certs
az iot hub device-identity create -n {iothub_name} -d x509_sub_device --am x509_thumbprint --output-dir ./certs
```

3. Use the subscribe device sample (instructions below) to subscribe to the topic, receive messages, and return responses.
4. Use the publish device sample code (instructions below) to publish to the topic.


## Running the python version of this sample:

1. If you haven't installed the required modules, follow the instructions in the [python README file](../python/README.md).
2. Open 2 command windows.  Activate the `iothub-broker` virtual environment in both.
3. Store the following connection strings in both windows:
```bash
export IOTHUB_HOST_NAME={iothub_name}.azure-devices.net

export PUB_DEVICE_ID=x509_pub_device
export PUB_CERT_PATH=./certs/x509_pub_device-cert.pem
export PUB_KEY_PATH=./certs/x509_pub_device-key.pem

export SUB_DEVICE_ID=x509_sub_device
export SUB_CERT_PATH=./certs/x509_sub_device-cert.pem
export SUB_KEY_PATH=./certs/x509_sub_device-key.pem
```

4. In the first (subscribe device) command window, type `python python/subscribe_x509.py` to run the subscribe app.
5. In the second (publish device) command window, type `python python/publish_x509.py` to run the publish app.

