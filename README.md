[![Build Status](https://travis-ci.org/sesam-community/delayed-rest-proxy.svg?branch=master)](https://travis-ci.org/sesam-community/delayed-rest-proxy)


# delayed-rest-proxy
Microservice for breaking down the rest-sink batch into single items and sending each with a delay in between

 ### Environment Parameters

 | CONFIG_NAME        | DESCRIPTION           | IS_REQUIRED  |DEFAULT_VALUE|
 | -------------------|---------------------|:------------:|:-----------:|
 | OPERATIONS | similar to 'operations' property in [Sesam's built-in REST system](https://docs.sesam.io/configuration.html#the-rest-system) with only 'url', 'method', 'headers' properties | yes | n/a |
 | URL_PATTERN |  same as 'url_pattern' in  in [Sesam's built-in REST system](https://docs.sesam.io/configuration.html#the-rest-system)  Azure Storage account key. | no, basic auth alternatively | n/a |
 | DELAY_DURATION_IN_SECONDS | number of seconds to wait between each rest request  | no | 60 |
 | LOG_LEVEL | log level. One of DEBUG,INFO,WARNING,ERROR,CRITICAL | no | INFO |


 ### Query Parameters

 None for the microservice. Any query string that is sent to the microservice will be forwarded to the target system



 ### An example of system config:

 ```json
 {
   "_id": "my-delayed-rest-system",
   "type": "system:microservice",
   "docker": {
     "environment": {
       "DELAY_DURATION_IN_SECONDS": "3",
       "LOG_LEVEL": "DEBUG",
       "OPERATIONS": {
         "put-customer": {
           "headers": {
             "Content-type": "application/json; charset=utf-8"
           },
           "method": "PUT",
           "url": "customer"
         },
         "post-customer": {
           "headers": {
             "Content-type": "application/json; charset=utf-8"
           },
           "method": "POST",
           "url": "customer"
         },
         "delete-customer": {
           "headers": {
             "Content-type": "application/json; charset=utf-8"
           },
           "method": "DELETE",
           "url": "customer"
         }
       },
       "URL_PATTERN": "http://my-customer-system/%s"
     },
     "image": "sesamcommunity/delayed-rest-proxy:9.9.9",
     "memory": 512,
     "port": 5000
   }
 }

 ```
