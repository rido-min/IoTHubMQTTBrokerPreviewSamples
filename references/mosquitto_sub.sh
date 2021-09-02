#!/bin/bash

hub=$1
dev=$2

az iot hub device-identity show -n $hub -d $dev --query properties.deviceId  2>/dev/null || \
    (echo "creating device $dev" && \
    az iot hub device-identity create -n $hub -d $dev)

mqttCreds=$(az iot hub device-identity generate-mqtt-credentials -n $hub -d $dev --du 3600 --only-show-errors)

host=$hub.azure-devices.net
clientid=$dev
pwd=$(echo $mqttCreds | jq -r '.password')
usr=$(echo $mqttCreds | jq -r '.username')

echo hostname: $host
echo clientid: $dev
echo username: $usr
echo password: $pwd

echo $'\n Connect with Mosquitto \n'

mosquitto_sub   -h $host \
                -p 8883 \
                -i "$dev" \
                -u "$usr" \
                -P "$pwd" \
                -t sample/topic \
                --cafile BaltimoreCA.pem \
                -V mqttv311 \
                -d -v