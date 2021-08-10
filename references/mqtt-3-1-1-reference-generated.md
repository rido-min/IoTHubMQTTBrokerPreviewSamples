# IoT Hub data plane MQTT 3.1.1 API reference

This document defines operations available in IoT Hub data plane API version `2020-06-30-preview`.

## Operations

### Send Telemetry

Post message to telemetry channel - Azure Event Hubs by default or other endpoint via routing configuration.

#### Message

**Topic name:** `$az/iot/telemetry`

**Properties**:

| Name | Type | Required | Description |
| :--- | :--- | :------- | :---------- |
| ct | string | no | Specifies Content Type of payload |
| ce | string | no | Specifies Content Encoding of the payload |
| mid | string | no | translates into `message-id` system property on posted message |
| uid | string | no | translates into `user-id` system property on posted message |
| cid | string | no | translates into `correlation-id` system property on posted message |
| crt | time | no | translates into `iothub-creation-time-utc` property on posted message |
| dts | string | no | Digital Twin subject |
| traceparent | string | no | defines `traceparent` header of [trace context](https://www.w3.org/TR/trace-context-1/#traceparent-header) for the operation |
| tracestate | string | no | defines `tracestate` header of [trace context](https://www.w3.org/TR/trace-context-1/#tracestate-header) for the operation |

**Payload**: any byte sequence

#### Success Acknowledgment

Message has been successfully posted to telemetry channel

#### Sample

```
-> PUBLISH
  QoS: 1
  Packet Id: 21
  Topic: $az/iot/telemetry/?ct=plain%2Ftext&mid=11324&@my property 1=test
  Payload: t1=10;t2=13.1
<- PUBACK
  Packet Id: 21
```

### Receive Commands

Receive and handle commands

#### Message

**Topic name:** `$az/iot/commands`

**Properties**:

| Name | Type | Required | Description |
| :--- | :--- | :------- | :---------- |
| sn | u64 | yes | Sequence number of the message |
| et | time | yes | Timestamp of when the message will expire |
| ent | time | yes | Timestamp of when the message entered the system |
| dc | u32 | yes | Number of times the message delivery was attempted |
| ct | string | no | Specifies Content Type of payload |
| ce | string | no | Specifies Content Encoding of the payload |
| crt | time | no | Timestamp of when the message was created (provided by sender) |
| mid | string | no | Message identity (provided by sender) |
| uid | string | no | User identity (provided by sender) |
| cid | string | no | Correlation identity (provided by sender) |

**Payload**: any byte sequence

#### Success Acknowledgment

Indicates command was accepted for handling by the client

#### Sample

```
-> SUBSCRIBE
  Packet Id: 28
  Payload:
    - Topic Filter: $az/iot/commands/+
      QoS: 1
<- SUBACK
  Packet Id: 28
  Payload:
    - Reason Code: 1

<- PUBLISH
  QoS: 1
  Packet Id: 35
  Topic: $az/iot/commands/?ct=application%2Fyaml&sn=118&et=1600987195320&ent=1600987175320&dc=1&@my-prop-3=test
  Payload:
    rotate:
      angle: -110
      speed: 6
-> PUBACK
  Packet Id: 35
  Reason Code: 0
```

### Receive Direct Methods

Receive and handle Direct Method calls

#### Request

**Topic name:** `$az/iot/methods/{name}`

**Properties**:

| Name | Type | Required | Description |
| :--- | :--- | :------- | :---------- |
| ct | string | no | Specifies Content Type of payload |
| ce | string | no | Specifies Content Encoding of the payload |

**Payload**: any byte sequence

#### Response

**Topic name:** `$az/iot/methods/{name}/response`

**Properties**:

| Name | Type | Required | Description |
| :--- | :--- | :------- | :---------- |
| rc | u32 | yes |  |
| ct | string | no | Specifies Content Type of payload |
| ce | string | no | Specifies Content Encoding of the payload |

**Payload**: any byte sequence

#### Alternative Responses

| Status | Name | Description |
| :----- | :--- | :---------- |
| 06A0 |  Unavailable | Indicates that client is not reachable through this connection. |

#### Sample

```
-> SUBSCRIBE
  Packet Id: 24
  Payload:
    - Topic Filter: $az/iot/methods/+/+
      QoS: 0
<- SUBACK
  Packet Id: 24
  Payload:
    - Reason Code: 0

<- PUBLISH
  QoS: 0
  Topic: $az/iot/methods/rotate/?rid=0A
  Payload: {"angle":-110,"speed":6}
-> PUBLISH
  QoS: 0
  Topic: $az/iot/methods/rotate/response/?rid=0A&rc=200
  Payload: {"angle":142}
```

### Get Twin

Retrieves Twin state

#### Request

**Topic name:** `$az/iot/twin/get`

**Properties**:
 none

**Payload**: empty

#### Response

**Topic name:** `$az/iot/twin/get/response`

**Properties**:
 none

**Payload**: Twin

#### Alternative Responses

| Status | Name | Description |
| :----- | :--- | :---------- |
| 0100 |  Bad Request | Operation message is malformed and cannot be processed. |
| 0101 |  Not Authorized | Client is not authorized to perform the operation. |
| 0102 |  Not Allowed | Operation is not allowed. |
| 0501 |  Throttled | request rate is too high per SKU |
| 0502 |  Quota Exceeded | daily quota per current SKU is exceeded |
| 0601 |  Server Error | internal server error |
| 0602 |  Timeout | operation timed out before it could be completed |
| 0603 |  Server Busy | server busy |

#### Sample

```
-> SUBSCRIBE
  Packet Id: 22
  Payload:
    - Topic Filter: $az/iot/twin/get/response/+
      QoS: 0
<- SUBACK
  Packet Id: 22
  Payload:
    - Reason Code: 0

-> PUBLISH
  QoS: 0
  Topic: $az/iot/twin/get/?rid=3
<- PUBLISH
  QoS: 0
  Topic: $az/iot/twin/get/response/?rid=3
  Payload: {"desired":{"$version":1},"reported":{"$version":1}}
```

### Get Twin Reported

Retrieves Twin's reported state

#### Request

**Topic name:** `$az/iot/twin/get/reported`

**Properties**:

| Name | Type | Required | Description |
| :--- | :--- | :------- | :---------- |

**Payload**: empty

#### Response

**Topic name:** `$az/iot/twin/get/response`

**Properties**:

| Name | Type | Required | Description |
| :--- | :--- | :------- | :---------- |
| v | u64 | no |  |

**Payload**: TwinData

#### Alternative Responses

| Status | Name | Description |
| :----- | :--- | :---------- |
| 0001 |  Not Modified | Resource was not modified based on provided precondition. |
| 0100 |  Bad Request | Operation message is malformed and cannot be processed. |
| 0504 |  Not Found | requested resource does not exist |
| 0601 |  Server Error | internal server error |
| 0501 |  Throttled | request rate is too high per SKU |
| 0502 |  Quota Exceeded | daily quota per current SKU is exceeded |

#### Sample

```
-> SUBSCRIBE
  Packet Id: 26
  Payload:
    - Topic Filter: $az/iot/twin/get/response/+
      QoS: 0
<- SUBACK
  Packet Id: 26
  Payload:
    - Reason Code: 0

-> PUBLISH
  QoS: 0
  Topic: $az/iot/twin/get/reported/?rid=3
<- PUBLISH
  QoS: 0
  Topic: $az/iot/twin/get/response/?rid=3&v=2
  Payload: {"temp":28}
```

### Get Twin Desired

Retrieves Twin's desired state

#### Request

**Topic name:** `$az/iot/twin/get/desired`

**Properties**:

| Name | Type | Required | Description |
| :--- | :--- | :------- | :---------- |

**Payload**: empty

#### Response

**Topic name:** `$az/iot/twin/get/response`

**Properties**:

| Name | Type | Required | Description |
| :--- | :--- | :------- | :---------- |
| v | u64 | no |  |

**Payload**: TwinData

#### Alternative Responses

| Status | Name | Description |
| :----- | :--- | :---------- |
| 0001 |  Not Modified | Resource was not modified based on provided precondition. |
| 0100 |  Bad Request | Operation message is malformed and cannot be processed. |
| 0504 |  Not Found | requested resource does not exist |
| 0601 |  Server Error | internal server error |
| 0501 |  Throttled | request rate is too high per SKU |
| 0502 |  Quota Exceeded | daily quota per current SKU is exceeded |

#### Sample

```
-> SUBSCRIBE
  Packet Id: 26
  Payload:
    - Topic Filter: $az/iot/twin/get/response/+
      QoS: 0
<- SUBACK
  Packet Id: 26
  Payload:
    - Reason Code: 0

-> PUBLISH
  QoS: 0
  Topic: $az/iot/twin/get/desired/?rid=3
<- PUBLISH
  QoS: 0
  Topic: $az/iot/twin/get/response/?rid=3&v=5
  Payload: {"firmware":"1.3.1"}
```

### Patch Twin Reported

Patch Twin's reported state

#### Request

**Topic name:** `$az/iot/twin/patch/reported`

**Properties**:

| Name | Type | Required | Description |
| :--- | :--- | :------- | :---------- |
| iv | u64 | no |  |

**Payload**: TwinState

#### Response

**Topic name:** `$az/iot/twin/patch/response`

**Properties**:

| Name | Type | Required | Description |
| :--- | :--- | :------- | :---------- |
| v | u64 | yes | Version of reported state after patch was applied |

**Payload**: empty

#### Alternative Responses

| Status | Name | Description |
| :----- | :--- | :---------- |
| 0104 |  Precondition Failed | precondition was not met resulting in request being canceled |
| 0100 |  Bad Request | Operation message is malformed and cannot be processed. |
| 0101 |  Not Authorized | Client is not authorized to perform the operation. |
| 0102 |  Not Allowed | Operation is not allowed. |
| 0501 |  Throttled | request rate is too high per SKU |
| 0502 |  Quota Exceeded | daily quota per current SKU is exceeded |
| 0601 |  Server Error | internal server error |
| 0602 |  Timeout | operation timed out before it could be completed |
| 0603 |  Server Busy | server busy |

#### Sample

```
-> SUBSCRIBE
  Packet Id: 12
  Payload:
    - Topic Filter: $az/iot/twin/patch/response/+
      QoS: 0
<- SUBACK
  Packet Id: 12
  Payload:
    - Reason Code: 0

-> PUBLISH
  QoS: 0
  Topic: $az/iot/twin/patch/reported/?rid=d1&iv=3
  Payload: {"temp":29}
<- PUBLISH
  QoS: 0
  Topic: $az/iot/twin/get/response/?rid=d1&v=4
  Payload: <empty>
```

### Receive Twin Desired State Changes

Receive updates to Twin's desired state

#### Message

**Topic name:** `$az/iot/twin/events/desired/changed`

**Properties**:

| Name | Type | Required | Description |
| :--- | :--- | :------- | :---------- |
| v | u64 | yes | Version of desired state matching this change |

**Payload**: TwinState

#### Sample

```
-> SUBSCRIBE
  Packet Id: 17
  Payload:
    - Topic Filter: $az/iot/twin/events/desired-changed/+
      QoS: 0
<- SUBACK
  Packet Id: 17
  Payload:
    - Reason Code: 0

<- PUBLISH
  QoS: 0
  Topic: $az/iot/twin/events/desired-changed/?v=2
  Payload: {"firmware":"1.2.4"}
```

## Responses

### Bad Request

Operation message is malformed and cannot be processed.

**Reason Code:** `131`

**Status:** `0100`

**Properties**:

| Name | Type | Required | Description |
| :--- | :--- | :------- | :---------- |
| r | string | no | contains information on what specifically is not valid about the message |

**Payload**: empty

### Conflict

Operation is in conflict with another ongoing operation.

**Reason Code:** `131`

**Status:** `0103`

**Properties**:

| Name | Type | Required | Description |
| :--- | :--- | :------- | :---------- |
| tid | string | no | trace ID for correlation with additional diagnostics for the error |
| r | string | no | contains information on what specifically is not valid about the message |

**Payload**: empty

### Not Allowed

Operation is not allowed.

**Reason Code:** `131`

**Status:** `0102`

**Properties**:

| Name | Type | Required | Description |
| :--- | :--- | :------- | :---------- |
| r | string | no | contains information on what specifically is not valid about the message |

**Payload**: empty

### Not Authorized

Client is not authorized to perform the operation.

**Reason Code:** `135`

**Status:** `0101`

**Properties**:

| Name | Type | Required | Description |
| :--- | :--- | :------- | :---------- |
| tid | string | no | trace ID for correlation with additional diagnostics for the error |

**Payload**: empty

### Not Found

requested resource does not exist

**Reason Code:** `131`

**Status:** `0504`

**Properties**:

| Name | Type | Required | Description |
| :--- | :--- | :------- | :---------- |
| r | string | no | contains information on what specifically is not valid about the message |

**Payload**: empty

### Not Modified

Resource was not modified based on provided precondition.

**Reason Code:** `0`

**Status:** `0001`

**Properties**:
 none

**Payload**: empty

### Precondition Failed

precondition was not met resulting in request being canceled

**Reason Code:** `131`

**Status:** `0104`

**Properties**:
 none

**Payload**: empty

### Quota Exceeded

daily quota per current SKU is exceeded

**Reason Code:** `151`

**Status:** `0502`

**Properties**:
 none

**Payload**: empty

### Resource Exhausted

resource has no capacity to complete the operation

**Reason Code:** `131`

**Status:** `0503`

**Properties**:

| Name | Type | Required | Description |
| :--- | :--- | :------- | :---------- |
| r | string | no | contains information on what specifically is not valid about the message |

**Payload**: empty

### Server Busy

server busy

**Reason Code:** `131`

**Status:** `0603`

**Properties**:

| Name | Type | Required | Description |
| :--- | :--- | :------- | :---------- |
| tid | string | no | trace ID for correlation with additional diagnostics for the error |

**Payload**: empty

### Server Error

internal server error

**Reason Code:** `131`

**Status:** `0601`

**Properties**:

| Name | Type | Required | Description |
| :--- | :--- | :------- | :---------- |
| tid | string | no | trace ID for correlation with additional diagnostics for the error |

**Payload**: empty

### Target Failed

Target responded but the response was invalid or malformed

**Reason Code:** `131`

**Status:** `06A2`

**Properties**:

| Name | Type | Required | Description |
| :--- | :--- | :------- | :---------- |
| r | string | no | contains information on what specifically is not valid about the message |

**Payload**: empty

### Target Timeout

timed out waiting for target to complete the request

**Reason Code:** `131`

**Status:** `06A1`

**Properties**:

| Name | Type | Required | Description |
| :--- | :--- | :------- | :---------- |
| tid | string | no | trace ID for correlation with additional diagnostics for the error |
| r | string | no | contains information on what specifically is not valid about the message |

**Payload**: empty

### Target Unavailable

Target is unreachable to complete the request

**Reason Code:** `131`

**Status:** `06A0`

**Properties**:
 none

**Payload**: empty

### Throttled

request rate is too high per SKU

**Reason Code:** `151`

**Status:** `0501`

**Properties**:
 none

**Payload**: empty

### Timeout

operation timed out before it could be completed

**Reason Code:** `131`

**Status:** `0602`

**Properties**:

| Name | Type | Required | Description |
| :--- | :--- | :------- | :---------- |
| tid | string | no | trace ID for correlation with additional diagnostics for the error |

**Payload**: empty
