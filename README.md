# Holo Zato API Documentation

The base address for all Holo Zato services is:

`http://proxy.holohost.net/zato/`

* Holo Zato API services communicate with other API services upstream.  This means that responses and errors vary because they can be:

  * **generated internally** by the Zato service
  * **generated upstream** by the target API and returned via the Zato service

* Authentication

  * Holo Zato API services require authentication.  You must **pass in a correct `Holo-Init` authentication header**.
  * Authentication for upstream APIs is already **handled by Zato internally**.
  * Authentication can be obtained from the HoloCentral team.


### About this document
The services listed in this document (below) are listed in the order in which the following entries should be made when setting up new routes for new nodes, as follows:

1. holo-cloudflare-dns-create
1. holo-proxy-service-create
1. holo-proxy-route-create
1. holo-cloudflare-dns2hash-create
1. holo-cloudflare-hash2tranche-create

...

# DNS Routing

## holo-cloudflare-dns-create

### Description
This service accepts a public key which is used to securely create a DNS entry on Cloudflare via their API.  Currently, `.holohost.net` is appended to the public key to create the fully qualified domain name for the DNS entry.

### HTTP Request
**Method** `POST http://proxy.holohost.net/zato/holo-cloudflare-dns-create`

### Parameters

| Parameter | Required | Description |
| -------- | -------- | -------- |
| pubkey | required | A public key to be used as the basis for the DNS entry. |

### Example

```
curl -X POST "http://proxy.holohost.net/zato/holo-cloudflare-dns-create" \
 -H "Holo-Init: [a_valid_key]" \
 -H "Content-Type: application/json" \
 --data '{"pubkey":"something"}'
```

...

# Proxy Routing

## holo-proxy-service-create

### Description
This service accepts four values which are used to securely create a "service" entry on the Holo proxy server via the proxy API.

### HTTP Request
**Method** `POST http://proxy.holohost.net/zato/holo-proxy-service-create`

### Parameters

| Parameter | Required | Description |
| -------- | -------- | -------- |
| name | required | The name to be used.  The name should be the **case-sensitive** version of `[pubkey].holohost.net`. (Ex. `HcSCjblAhbLah.holohost.net`). |
| protocol | required | The protocol to be used.  Currently `http`. |
| host | required | The host to be used.  The host is an IP address, ex. `172.26.166.34`.  Currently the ZeroTier-assigned IP address of the node. |
| port | required | The port to be used.  Currently `48080`. |

### Example

```
curl -X POST "http://proxy.holohost.net/zato/holo-proxy-service-create" \
 -H "Holo-Init: [a_valid_key]" \
 -H "Content-Type: application/json" \
 --data '{"name":"[pubkey].holohost.net", "protocol":"http", "host":"10.10.10.1", "port":48080}'
```

...


## holo-proxy-route-create

### Description
This service accepts four values which are used to securely create a "route" entry on the Holo proxy server via the proxy API.


### HTTP Request
**Method** `POST http://proxy.holohost.net/zato/holo-proxy-route-create`

### Parameters

| Parameter | Required | Description |
| -------- | -------- | -------- |
| name | required | The name to be used.  The name should be the **case-sensitive** version of `[pubkey].holohost.net`. (Ex. `HcSCjblAhbLah.holohost.net`). The name **should** match the `name` of the service to which the route is forwarded. |
| protocols | required | The protocols to be used.  Protocols is an array. Currently `["http","https"]`. |
| hosts | required | The hosts to be used. Hosts is an array. Each host should be the **lower-case** version of the tranche entry. (Ex. `["*.hcscjblahblah.holohost.net"]`). |
| service | required | The service id of the service to which the route is forwarded. (Ex. `53b36017-781d-4381-a299-b0f0a546b4be`).|

### Example

```
curl -X POST "http://proxy.holohost.net/zato/holo-proxy-route-create" \
 -H "Holo-Init: [a_valid_key]" \
 -H "Content-Type: application/json" \
 --data '{"name":"[pubkey].holohost.net", "protocols":["http","https"], "hosts":"10.10.10.1", "service":"53b36017-781d-4381-a299-b0f0a546b4be" }'
```

...

# Cloudflare KV Stores

## holo-cloudflare-dns2hash-create

### Description
This service accepts a key/value pair which is used to securely create a KV Store entry on Cloudflare via their API.

### HTTP Request
**Method** `POST http://proxy.holohost.net/zato/holo-cloudflare-dns2hash-create`

### Parameters

| Parameter | Required | Description |
| -------- | -------- | -------- |
| kv_key | required | The key to be used.  The key is the domain name which will be used to retrieve the value. |
| kv_value | required | The value to be paired with the key.  The value is the hApp "bundlehash" from the Holo Hosting hApp. |

### Example

```
curl -X POST "http://proxy.holohost.net/zato/holo-cloudflare-dns2hash-create" \
 -H "Holo-Init: [a_valid_key]" \
 -H "Content-Type: application/json" \
 --data '{"kv_key":"some_key", "kv_value":"some_value"}'
```

...

## holo-cloudflare-hash2tranche-create

### Description
This service accepts a key/value pair which is used to securely create a KV Store entry on Cloudflare via their API.

### HTTP Request
**Method** `POST http://proxy.holohost.net/zato/holo-cloudflare-hash2tranche-create`

### Parameters

| Parameter | Required | Description |
| -------- | -------- | -------- |
| kv_key | required | The key to be used. The key is the hApp "bundlehash" from the Holo Hosting hApp.  The key must match the value used in the "dns2hash" Cloudflare KV Store. |
| kv_value | required | The value to be paired with the key.  The value is an **array** of hosts, each in the form of `*.[pubkey].holohost.net`. |

### Example

```
curl -X POST "http://proxy.holohost.net/zato/holo-cloudflare-hash2tranche-create" \
 -H "Holo-Init: [a_valid_key]" \
 -H "Content-Type: application/json" \
 --data '{"kv_key":"some_key", "kv_value":"some_value"}'
```

...

