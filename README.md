# main/eapp-identity



## Getting Started

Download links:

SSH clone URL: ssh://git@git.jetbrains.space/50gramx/main/eapp-identity.git

HTTPS clone URL: https://git.jetbrains.space/50gramx/main/eapp-identity.git



These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

## Prerequisites

What things you need to install the software and how to install them.

```
Examples
```

## Deployment

Add additional notes about how to deploy this on a production system.

## Resources

Add links to external resources for this project, such as CI server, bug tracker, etc.


docker run -d --name jaeger \
  -e COLLECTOR_ZIPKIN_HTTP_PORT=9411 \
  -p 5775:5775/udp \
  -p 6831:6831/udp \
  -p 6832:6832/udp \
  -p 5778:5778 \
  -p 16686:16686 \
  -p 14268:14268 \
  -p 9411:9411 \
  jaegertracing/all-in-one:latest


ghz --insecure \
    --proto /path/to/your/service.proto \
    --call your.package.ValidateAccount \
    --data '{"account_mobile_number": "1234567890", "requested_at": "your_timestamp"}' \
    -c 50 \
    -n 2000 \
    -q 10 \
    your.server.address:your_port


ghz --insecure \
    --proto /opt/ethos/apps/service/eapp-service-core/src/main/proto/ethos/elint/services/product/identity/account/access_account.proto \
    --import-paths /opt/ethos/apps/service/eapp-service-core/src/main/proto \
    --call elint.services.product.identity.account.AccessAccountService.ValidateAccount \
    --data '{"account_mobile_number": "1234567890"}' \
    -c 50 \
    -n 2000 \
    localhost:50501
