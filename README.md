[![Build Status](https://travis-ci.org/sesam-community/delayed-rest-proxy.svg?branch=master)](https://travis-ci.org/sesam-community/delayed-rest-proxy)


# delayed-rest-proxy
Can be used to send rest requests with a delay between each request.

 ### Environment Parameters

 | CONFIG_NAME        | DESCRIPTION           | IS_REQUIRED  |DEFAULT_VALUE|
 | -------------------|---------------------|:------------:|:-----------:|
 | OPERATIONS | similar to 'operations' property in [Sesam's built-in REST system](https://docs.sesam.io/configuration.html#the-rest-system) with only 'url', 'method', 'headers' properties | yes | n/a |
 | URL_PATTERN |  same as 'url_pattern' in  in [Sesam's built-in REST system](https://docs.sesam.io/configuration.html#the-rest-system)  Azure Storage account key. | no, basic auth alternatively | n/a |
 | DELAY_DURATION_IN_SECONDS | number of seconds to wait between each rest request  | no | 60 |
 | LOG_LEVEL | log level. One of DEBUG,INFO,WARNING,ERROR,CRITICAL | no | INFO |


 ### Query Parameters

 None for the microservice. Any query string that is sent to the microservice will be forwarded to the target system

 ### How-to-configure
   1. collect entities according to [Sesam's rest-entity-shape](https://docs.sesam.io/configuration.html#rest-expected-rest-entity-shape)
   2. create the microservice system
   3. create an endpoint pipe with sink of type json


 ### Example configurations:

 ##### system:
 ```json
 {
   "_id": "my-delayed-rest-system",
   "type": "system:microservice",
   "docker": {
     "environment": {
       "DELAY_DURATION_IN_SECONDS": "3",
       "LOG_LEVEL": "DEBUG",
       "OPERATIONS": {
         "put-entity": {
           "headers": {
             "Content-type": "application/json; charset=utf-8"
           },
           "method": "PUT",
           "url": "myendpoint"
         },
         "post-entity": {
           "headers": {
             "Content-type": "application/json; charset=utf-8"
           },
           "method": "POST",
           "url": "myendpoint"
         },
         "delete-entity": {
           "headers": {
             "Content-type": "application/json; charset=utf-8"
           },
           "method": "DELETE",
           "url": "myendpoint"
         }
       },
       "URL_PATTERN": "http://my-rest-receiver-system/%s"
     },
     "image": "sesamcommunity/delayed-rest-proxy:1.0.0",
     "memory": 512,
     "port": 5000
   }
 }

 ```

##### entity to be prosessed
```json
{
  "_id": "1",
  "operation": "put-entity",
  "payload": {
    "key1": "value1",
    "key2": "value2",
    "key3": "value3",
    "key4": "value4"
  }
}
```

 ##### pipe:
 ```json
 {
  "_id": "my-endpoint",
  "type": "pipe",
  "source": {
    "type": "dataset",
    "dataset": "my-dataset"
  },
  "sink": {
    "type": "json",
    "system": "my-delayed-rest-system",
    "url": ""
  },
  "transform": {
    "type": "dtl",
    "rules": {
      "default": [
        ["copy", "*"]
      ]
    }
  }
}

 ```
