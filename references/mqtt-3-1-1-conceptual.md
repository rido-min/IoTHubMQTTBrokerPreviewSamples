---
 title: Azure IoT Hub MQTT 3.1.1 support (preview)
 description: Learn about MQTT 3.1.1 support in IoT Hub
 services: iot-hub
 ms.service: iot-fundamentals
 ms.topic: conceptual
 ms.date: 08/30/2021
---

# IoT Hub MQTT 3.1.1 support overview (preview)

**api-version:** 2021-06-30-preview

This document defines IoT Hub data plane API over MQTT 3.1.1 protocol. See [API Reference](iot-hub-mqtt-3-1-1-reference.md) for complete definitions in this API.

## Prerequisites

- [Enable preview mode](iot-hub-preview-mode.md) on a brand new IoT hub.
- Prior knowledge of [MQTT 3.1.1 specification](https://docs.oasis-open.org/mqtt/mqtt/v3.1.1/os/mqtt-v3.1.1-os.html) is required.

## Level of support and limitations

IoT Hub support for MQTT 3.1.1 is limited in following ways:

- No official [Azure IoT Hub device SDK](iot-hub-devguide-sdks.md) support yet.
- `RETAIN` isn't supported.
- `Maximum QoS` is `1`.
- `Maximum Packet Size` is `256 KiB` (subject to further restrictions per operation).
- Assigned Client IDs aren't supported.
- `Keep Alive` is limited to `19 min` (maximum delay for liveness check is `28.5 min` per MQTT specification).
- Maximum number of outstanding unacknowledged PUBLISH packets (in client-server direction) with `QoS: 1` is `16`.
- Single client can have no more than `50` subscriptions.
  When the limit's reached, SUBACK will return `0x80` (Failure) reason code for subscriptions.

## Connection lifecycle

### Connection

Client connects to IoT Hub's MQTT endpoint as follows:

- Resolve IoT hub's hostname to IP address using DNS.
- Establish TCP connection to resolved IP address and port 8883.
- Establish TLS-encrypted channel over the TCP connection.
- Send CONNECT packet according to MQTT specification within 30 seconds after successfully completing TLS handshake.

Here's an example of CONNECT packet:

```text
-> CONNECT
    Protocol Level: 4
    Clean Session: 0
    Client Identifier: MyDevice15
    Username: av=2021-06-30-preview&h=abc.azure-devices.net&did=MyDevice15&am=SAS&se=1600987195320&ca=artisan-0.2;Linux
    Password: {SAS signature bytes}
```

> [!NOTE]
> All the samples in this specification are shown from client's perspective. Sign `->` means client sending packet, `<-` - receiving.

Username field if present, must follow encoding rules described in [Message Properties](#message-properties) section.

Supported properties are:

| Name | Type   | Required  | Description                                                                                                                                        |
| :--- | :----- | :-------- | :------------------------------------------------------------------------------------------------------------------------------------------------- |
| h    | string | no        | Defines host name of the IoT hub. Optional if SNI extension is provided during TLS handshake.                                                      |
| did  | string | no        | Defines identity of the device for which connection is being established. If missing, client identifier will be used to determine device identity. |
| mid  | string | no        | Defines identity of the module for which connection is being established.                                                                          |
| av   | string | yes       | Must be set to API version value provided in this specification's header for this specification to apply.                                          |
| am   | string | yes       | Authentication method used. For more information about authentication method, see [Authentication](#authentication).                               |
| ca   | string | no        | Communicates information about the client creating the connection.                                                                                 |
| se   | time   | yes (SAS) | Expiration time for the provided SAS.                                                                                                              |
| sa   | time   | no        | Defines time of connection for SAS authentication.                                                                                                 |
| sp   | string | no        | Defines IoT Hub access policy used for SAS authentication.                                                                                         |
| dct  | string | no        | Content Type to be used by default on this connection. Only `application/json` and `application/cbor` are supported.                               |
| dtmi | string | no        | Defines Digital Twin model identity.                                                                                                                 |

IoT Hub responds with CONNACK packet once it completes authentication. If connection is established successfully, CONNACK looks like:

```text
<- CONNACK
    Session Present: 0
    Reason Code: 0x00
```

`Session Present` flag indicates whether IoT Hub has restored previously created MQTT session.

### Authentication

The `am` (Authentication Method) property on CONNECT determines what kind of authentication client uses for the connection:

- `SAS` - Shared Access Signature authentication,
- `SASb64` - Shared Access Signature authentication with base64 encoding,
- `X509` - client certificate authentication.

If client does not provide `am` property, connection fails with `0x04` "Connection Refused, bad user name or password" return code.

If connection's authentication method doesn't match the device's configured method in IoT Hub, connection fails with `0x05` "Connection Refused, not authorized" return code.

#### SAS

When using SAS-based authentication, client must provide the signature of connection context. This proves authenticity of the MQTT connection. The signature must be based on one of two authentication keys in the client's configuration in IoT Hub or one of two shared access keys of a [Shared access policy](https://docs.microsoft.com/en-us/cli/azure/iot/hub/device-identity/connection-string?view=azure-cli-latest).

String to sign must be formed as follows:

```text
{host-name}\n
{identity}\n
{sas-policy}\n
{sas-at}\n
{sas-expiry}\n
```

- `host-name` is provided in Username field of CONNECT packet.
- `identity` is identity of device or module used to authenticate.
- `sas-policy` is provided via `sp` property in CONNECT packet. If present, defines IoT Hub access policy used for authentication. If omitted, authentication settings in device registry will be used instead.
- `sas-at` is provided via `sa` property in CONNECT packet. If present, specifies time of connection - current time.
- `sas-expiry` defines expiration time for the authentication. It's a `time`-typed user property on CONNECT packet. This property is required.

For optional parameters, if omitted, empty string MUST be used instead in string to sign.

HMAC-SHA256 is used to hash the string based on one of device's or access policy symmetric keys. Hash value is then set as value of `Authentication Data` property.

Here's an example of string to sign for `sensor_1` module of `MyDevice15` device in `abc.azure-devices.net` IoT hub connecting at 2021-06-30T14:05:38.334, setting SAS token expiration at 40 minutes, using device's symmetric keys:

```text
abc.azure-devices.net
MyDevice15/sensor_1

1625061938334
1625064338334
```

> [!NOTE]
> Once SAS token expires, connection is considered unauthenticated and is closed by IoT Hub.

#### X509

If `am` (Authentication Method) property in CONNECT packet is set to `X509`, IoT Hub authenticates the connection based on the provided client certificate.
For more details see [certificate based authentication](https://docs.microsoft.com/en-us/azure/iot-hub/iot-hub-dev-guide-sas?tabs=node#supported-x509-certificates)

### Disconnection

Server can disconnect client for a few reasons:

- client is misbehaving in a way that is impossible to respond to with negative acknowledgment (or response) directly,
- server is failing to keep state of the connection up to date,
- client with the same identity has connected.

## Operations

This API defines operations that enable devices to interact with IoT Hub over MQTT. Here's an example of Send Telemetry operation:

```text
-> PUBLISH
    QoS: 1
    Packet Id: 31
    Topic: $az/iot/telemetry
    Payload: Hello

<- PUBACK
    Packet Id: 31
```

For complete specification of operations, see [API Reference](iot-hub-mqtt-3-1-1-reference.md).

### Message topics and subscriptions

Topics used in operations' messages in this API start with `$az/iot/`.
MQTT broker semantics don't apply to these messages (see "[Topics beginning with \$](https://docs.oasis-open.org/mqtt/mqtt/v3.1.1/csprd02/mqtt-v3.1.1-csprd02.html#_Toc385349844)" for details).

Topics starting with `$az/iot/` that aren't defined in this API aren't supported:

- Sending messages to undefined system topic results in `Not Found` error (see [Response](#response) for details),
- Subscribing to undefined topic results in `SUBACK` with `Reason Code: 0x80` (Failure).

Topic names are case-sensitive and must be exact match. For example, `$az/iot/Telemetry` isn't supported while `$az/iot/telemetry` is.

Wildcards in subscription topic filters starting with `$az/iot/..` aren't fully supported. For example, a client can't subscribe to `$az/iot/+` or `$az/iot/#`. Attempting to do so results in `SUBACK` with `Reason Code: 0x80` (Failure). Single-segment wildcard (`+`) is supported instead of topic segment where properties are encoded. Single-segment wildcard can also be used in place of path parameters. Here is an example of subscription to receive Twin Get and Twin Patch responses, and all Direct Method calls:

```text
-> SUBSCRIBE
  Packet Id: 22
  Payload:
    - Topic Filter: $az/iot/twin/get/response/+
      QoS: 0
    - Topic Filter: $az/iot/twin/patch/response/+
      QoS: 0
    - Topic Filter: $az/iot/methods/+/+
      QoS: 0
<- SUBACK
  Packet Id: 22
  Payload:
    - Reason Code: 0
    - Reason Code: 0
    - Reason Code: 0
```

### Interaction types

All the operations in this API are based on one of two interaction types:

- Message with optional acknowledgment (Message-Ack)
- Request-Response (Request-Response)

Operations also vary by direction (determined by direction of initial message in exchange):

- Client-to-Server
- Server-to-Client

For example, Send Telemetry is Client-to-Server operation of "Message with acknowledgment" type, while Handle Direct Method is Server-to-Client operation of Request-Response type.

#### Message-Acknowledgement interactions

Message with optional Acknowledgment (Message-Ack) interaction is expressed as an exchange of PUBLISH and PUBACK packets in MQTT. Acknowledgment is optional and sender may choose to not request it by sending PUBLISH packet with `QoS: 0`.

Here's an example of a simple Message-Ack interaction:

```text
-> PUBLISH
    QoS: 1
    Packet Id: 34
    Topic: $az/iot/telemetry
    Payload: {"temperature":47}

<- PUBACK
    Packet Id: 34
```

#### Request-Response Interactions

In Request-Response interactions, both Request and Response messages are sent as PUBLISH packets with `QoS: 0`.

Both request and response messages have predefined per this specification.
For client-to-server interactions, client needs to subscribe to response topic for the operation before sending request in order to be able to receive the response.
For server-to-client operations, it needs to subscribe to request topic to start receiving requests.

`rid` property must be set in both Request and Response messages and is used to correlate them. Omitting `rid` property results in `Bad Request` error.
Maximum supported length for `rid` property is 32 bytes. Setting `rid` property to a value longer than 32 bytes results in `Bad Request` error.

IoT Hub will not be able to respond to request that has an issue with topic name or `rid` property.

Here's an example of Request-Response interaction:

```text
// assumes that client is subscribed for `$az/iot/twin/get/response/+` already

-> PUBLISH
    QoS: 0
    Topic: $az/iot/twin/get/desired/?rid=1fa
    Payload: <empty>

<- PUBLISH
    QoS: 0
    Topic: $az/iot/twin/get/response/?rid=1fa
    Payload: ...
```

Request-Response interactions don't support PUBLISH packets with `QoS: 1` as request or response messages. Sending Request or Response PUBLISH packet with `QoS: 1` results in `Bad Request` error.

### Message Properties

Message properties, when present, always appear in the last segment in message topic name. Properties are encoded as `name=value` pairs separated by `&`. Following characters are reserved and must be [percent-encoded](https://en.wikipedia.org/wiki/Percent-encoding) if they occur in either name or value: `%/#+&=`.

All property names are case sensitive.

Each operation has its own set of supported properties. Property is defined by name, data type, and whether it is required. Consult with operation's specification for details.
Sending messages with properties not defined in this specification will result in `Bad Request` error.

Where user-defined properties are allowed, their names must follow the format `@{property name}`. User-defined properties only support valid UTF-8 string values.

All system properties have one of the following data types:

- `string`: UTF-8 string
- `time`: number of milliseconds since `1970-01-01T00:00:00.000Z`. for example, `1600987195320` for `2020-09-24T22:39:55.320Z`,
- `u32`: unsigned 32-bit integer number,
- `u64`: unsigned 64-bit integer number,
- `i32`: signed 32-bit integer number,
- `binary`: base64-encoded byte sequence.

For example, telemetry message with a topic name `$az/iot/telemetry/?ct=application%2Fjson&crt=1600987195320&@my prop%231=&@my prop%232=%25needs encoding%25` has following properties:

- Content Type: application/json,
- Creation Time: 2020-09-24T22:39:55.320Z,
- user-defined `my prop#1` property with an empty value,
- user-defined `my prop#2` property with value of `%needs encoding%`.

### Response

Interactions can complete with different outcomes: `Success`, `Bad Request`, `Not Found`, and others.

For Message-Ack interactions, MQTT 3.1.1 provides a way to communicate only `Success` outcome. For any other outcome IoT Hub is going to close the connection and specify the outcome as a reason.

For Request-Response interactions, outcomes are distinguished from each other by `s` property.
Every operation has a default (success) outcome with `s` property not set.

Here's an example of `Not Authorized` response:

```text
-> PUBLISH
    QoS: 0
    Topic: $az/iot/twin/patch/reported/?rid=1fa
    Payload: ...

<- PUBLISH
    QoS: 0
    Topic: $az/iot/twin/get/response/?rid=1fa&s=0101
    Payload: <empty>
```

When appropriate, IoT Hub sets the following properties:

- `s` - IoT Hub's code for operation's status. This code can be used to differentiate outcomes as described above.
- `tid` – trace Id for the operation; IoT Hub may keep additional diagnostics concerning the operation that could be used for internal investigation.
- `r` - human-readable message providing further information on why operation ended up in a state indicated by `s` property.

> [!NOTE] > `r` property (Reason) is meant only for people and should not be used in client logic. This API allows for messages to be changed at any point without warning or change of version.

#### Status code

`s` property in Response messages carries status code for operation. It's optimized for machine reading efficiency.
It consists of two-byte unsigned integer encoded as hex in string like `06A1`.
Code structure (bit map):

```text
7 6 5 4 3 2 1 0 | 7 6 5 4 3 2 1 0
0 0 0 0 0 R T T | C C C C C C C C
```

First byte is used for flags:

- bits 0 and 1 indicate type of outcomes:
  - `00` - success
  - `01` - client error
  - `10` - server error
- bit 2: `1` indicates error is retryable
- bits 3 through 7 are reserved and must be set to `0`

Second byte contains actual distinct response code. Error codes with different flags can have the same second byte value. For example, there can be `0001`, `0101`, `0201`, `0301` error codes having distinct meaning.

For example, `Too Many Requests` is a client, retryable error with own code of `1`. Its binary value is
`0000 0101 0000 0001`. Its hex-encoded string representation is `0501`.

Clients may use type bits to identify whether operation concluded successfully. Clients may also use retryable bit to decide whether it's sensible to retry operation.

## Recommendations

### Session management

CONNACK packet has `Session Present` flag to indicate whether server restored previously created session. Client can use this property to identify whether previously made subscriptions are still in effect or client needs to re-subscribe.
To rely on `Session Present`, client must keep track of subscriptions it has made. Subscription can be considered established only when SUBACK packet is received and it shows success reason code.

### Batching

This API does not define any special way to send a batch of messages. To reduce overhead of resource-intensive operations in TLS and networking, client may bundle packets (PUBLISH, PUBACK, SUBSCRIBE, and others) together before handing them over to underlying TLS/TCP stack.
