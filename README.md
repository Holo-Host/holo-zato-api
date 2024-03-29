# Holo Zato API Documentation For Developers

The base address for all Holo Zato services is:

`http://proxy.holohost.net/zato/`

* Holo Zato API services communicate with other API services upstream.  This means that responses and errors vary because they can be:

  * **generated internally** by the Zato service
  * **generated upstream** by the target API and returned via the Zato service

* Authentication

  * Holo Zato API services require authentication.  You must **pass in a correct authentication header**.
  * Authentication for upstream APIs is already **handled by Zato internally**.
  * Authentication can be obtained from the HoloCentral team.


### Services for Creating New Full Routes

The following services are listed in the order in which the following entries should be made when setting up new routes for new hosts, as follows:

1. holo-cloudflare-dns-create
1. holo-proxy-service-create
1. holo-proxy-route-create
1. holo-cloudflare-dns2hash-create
1. holo-cloudflare-hash2tranche-create

...

# DNS Routing

## holo-cloudflare-dns-create

### Description
This service accepts a public key which is used to securely create a DNS entry on Cloudflare via their API.  Currently, `*.` is prepended & `.holohost.net` is appended to the public key to create the fully qualified domain name for the DNS entry.

### HTTP Request
**Method** `POST http://proxy.holohost.net/zato/holo-cloudflare-dns-create`

### Parameters

| Parameter | Required | Description |
| -------- | -------- | -------- |
| pubkey | required | A public key to be used as the basis for the DNS entry. |

### Example

```
curl -X POST "http://proxy.holohost.net/zato/holo-cloudflare-dns-create" \
 -H "[a_header]: [a_valid_key]" \
 -H "Content-Type: application/json" \
 --data '{"pubkey":"something"}'
```

...

## holo-cloudflare-dns-delete

### Description
This service accepts a public key which is used to securely delete a DNS entry on Cloudflare via their API.  Currently, `*.` is prepended & `.holohost.net` is appended to the public key to create the fully qualified domain name for the DNS entry.

### HTTP Request
**Method** `POST http://proxy.holohost.net/zato/holo-cloudflare-dns-delete`

### Parameters

| Parameter | Required | Description |
| -------- | -------- | -------- |
| pubkey | required | A public key to be used as the basis for the DNS deletion. |

### Example

```
curl -X POST "http://proxy.holohost.net/zato/holo-cloudflare-dns-delete" \
 -H "[a_header]: [a_valid_key]" \
 -H "Content-Type: application/json" \
 --data '{"pubkey":"something"}'
```

...


## holo-cloudflare-dns-list

### Description
This service retrieves the DNS entries from Cloudflare via their API.

**NOTE:  This service is hard-coded to retrieve the DNS entries only for the `holohost.net` zone.**


### HTTP Request
**Method** `GET http://proxy.holohost.net/zato/holo-cloudflare-dns-list`

### Parameters

None

### Example

```
curl -X GET "http://proxy.holohost.net/zato/holo-cloudflare-dns-list" \
 -H "[a_header]: [a_valid_key]"
```

...


## holo-cloudflare-dns-read

### Description
This service accepts one value which is used to retrieve a DNS entry from Cloudflare via their API.


**NOTE:  This service is hard-coded to retrieve the DNS entries only for the `holohost.net` zone.**


### HTTP Request
**Method** `POST http://proxy.holohost.net/zato/holo-cloudflare-dns-read`

### Parameters

| Parameter | Required | Description |
| -------- | -------- | -------- |
| record_id | required | The dns record to be retrieved.|

### Example

```
curl -X POST "http://proxy.holohost.net/zato/holo-cloudflare-dns-read" \
 -H "[a_header]: [a_valid_key]" \
 -H "Content-Type: application/json" \
 --data '{"record_id":"[a_valid_dns_record_id]}'
```

...


## holo-cloudflare-dns-customer-create

### Description
This service accepts a domain name which is used to securely create a DNS entry on Cloudflare via their API.  Currently, the incoming "name" is prepended to `.holohost.net` to create the fully qualified domain name for the DNS entry.

The **purpose** for this service is for developers to create domain entries that are **CNAME**d to `loader.holohost.net` !

### HTTP Request
**Method** `POST http://proxy.holohost.net/zato/holo-cloudflare-dns-customer-create`

### Parameters

| Parameter | Required | Description |
| -------- | -------- | -------- |
| type | required | record type: usually CNAME |
| name | required | subdomain to be used.  It will be prepended to `holohost.net` |
| content | required | where the dns points to.  For Holo `holohost.net` CNAMEs it will be `loader.holohost.net` |

### Example

```
curl -X POST "http://proxy.holohost.net/zato/holo-cloudflare-dns-customer-create" \
 -H "[a_header]: [a_valid_key]" \
 -H "Content-Type: application/json" \
 --data '{"type":"CNAME", "name":"asdf","content":"loader.holohost.net"}'
```

...


## holo-cloudflare-dns-customer-delete

### Description
This service accepts a domain name which is used to securely delete a DNS entry on Cloudflare via their API.  Currently, the incoming "name" is prepended to `.holohost.net` to create the fully qualified domain name for the DNS entry.

### HTTP Request
**Method** `POST http://proxy.holohost.net/zato/holo-cloudflare-dns-customer-delete`

### Parameters

| Parameter | Required | Description |
| -------- | -------- | -------- |
| domain | required | subdomain to be used.  It will be prepended to `holohost.net` |

### Example

```
curl -X POST "http://proxy.holohost.net/zato/holo-cloudflare-dns-customer-delete" \
 -H "[a_header]: [a_valid_key]" \
 -H "Content-Type: application/json" \
 --data '{"domain":"asdf"}'
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
 -H "[a_header]: [a_valid_key]" \
 -H "Content-Type: application/json" \
 --data '{"name":"[pubkey].holohost.net", "protocol":"http", "host":"10.10.10.1", "port":48080}'
```

...


## holo-proxy-service-delete

### Description
This service accepts one value which is used to securely delete a "service" entry on the Holo proxy server via the proxy API.


### HTTP Request
**Method** `POST http://proxy.holohost.net/zato/holo-proxy-service-delete`

### Parameters

| Parameter | Required | Description |
| -------- | -------- | -------- |
| name | required | The name to be used.  If the service was created correctly (see above), then the name should be the **case-sensitive** version of `[pubkey].holohost.net`. (Ex. `HcSCjblAhbLah.holohost.net`).|

### Example

```
curl -X POST "http://proxy.holohost.net/zato/holo-proxy-service-delete" \
 -H "[a_header]: [a_valid_key]" \
 -H "Content-Type: application/json" \
 --data '{"name":"[pubkey].holohost.net"}'
```

...


## holo-proxy-service-list

### Description
This service retrieves the "service" entries from the Holo proxy server via the proxy API.


### HTTP Request
**Method** `GET http://proxy.holohost.net/zato/holo-proxy-service-list`

### Parameters

None

### Example

```
curl -X GET "http://proxy.holohost.net/zato/holo-proxy-service-list" \
 -H "[a_header]: [a_valid_key]"
```

...


## holo-proxy-service-read

### Description
This service accepts one value which is used to retrieve a "service" entry from the Holo proxy server via the proxy API.


### HTTP Request
**Method** `POST http://proxy.holohost.net/zato/holo-proxy-service-read`

### Parameters

| Parameter | Required | Description |
| -------- | -------- | -------- |
| service_id | required | The service to be retrieved.|

### Example

```
curl -X POST "http://proxy.holohost.net/zato/holo-proxy-service-read" \
 -H "[a_header]: [a_valid_key]" \
 -H "Content-Type: application/json" \
 --data '{"route_id":"[a_valid_service_id]}'
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
 -H "[a_header]: [a_valid_key]" \
 -H "Content-Type: application/json" \
 --data '{"name":"[pubkey].holohost.net", "protocols":["http","https"], "hosts":["*.[pubkey].holohost.net"], "service":"53b36017-781d-4381-a299-b0f0a546b4be" }'
```

...

## holo-proxy-route-delete

### Description
This service accepts one value which is used to securely delete a "route" entry on the Holo proxy server via the proxy API.


### HTTP Request
**Method** `POST http://proxy.holohost.net/zato/holo-proxy-route-delete`

### Parameters

| Parameter | Required | Description |
| -------- | -------- | -------- |
| name | required | The name to be used.  If the route was created correctly (see above), then the name should be the **case-sensitive** version of `[pubkey].holohost.net`. (Ex. `HcSCjblAhbLah.holohost.net`). The name **should** match the `name` of the service to which the route is forwarded. |

### Example

```
curl -X POST "http://proxy.holohost.net/zato/holo-proxy-route-delete" \
 -H "[a_header]: [a_valid_key]" \
 -H "Content-Type: application/json" \
 --data '{"name":"[pubkey].holohost.net"}'
```

...

## holo-proxy-route-list

### Description
This service retrieves the "route" entries from the Holo proxy server via the proxy API.


### HTTP Request
**Method** `GET http://proxy.holohost.net/zato/holo-proxy-route-list`

### Parameters

None

### Example

```
curl -X GET "http://proxy.holohost.net/zato/holo-proxy-route-list" \
 -H "[a_header]: [a_valid_key]"
```

...


## holo-proxy-route-read

### Description
This service accepts one value which is used to retrieve a "route" entry from the Holo proxy server via the proxy API.

### HTTP Request
**Method** `POST http://proxy.holohost.net/zato/holo-proxy-route-read`

### Parameters

| Parameter | Required | Description |
| -------- | -------- | -------- |
| route_id | required | The route to be retrieved.|

### Example

```
curl -X POST "http://proxy.holohost.net/zato/holo-proxy-route-read" \
 -H "[a_header]: [a_valid_key]" \
 -H "Content-Type: application/json" \
 --data '{"route_id":"[a_valid_route_id]}'
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
| kv_value | required | The value to be paired with the key.  The value is the hApp "holoHostingId" from the Holo Hosting hApp. |

### Example

```
curl -X POST "http://proxy.holohost.net/zato/holo-cloudflare-dns2hash-create" \
 -H "[a_header]: [a_valid_key]" \
 -H "Content-Type: application/json" \
 --data '{"kv_key":"some_key", "kv_value":"some_value"}'
```

...


## holo-cloudflare-dns2hash-delete

### Description
This service accepts a key which is used to securely delete a KV Store entry on Cloudflare via their API.

### HTTP Request
**Method** `POST http://proxy.holohost.net/zato/holo-cloudflare-dns2hash-delete`

### Parameters

| Parameter | Required | Description |
| -------- | -------- | -------- |
| kv_key | required | The key to be used.  The key (in dns2hash) is the domain name. |

### Example

```
curl -X POST "http://proxy.holohost.net/zato/holo-cloudflare-dns2hash-delete" \
 -H "[a_header]: [a_valid_key]" \
 -H "Content-Type: application/json" \
 --data '{"kv_key":"some_key"}'
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
| kv_key | required | The key to be used. The key is the hApp "holoHostingId" from the Holo Hosting hApp.  The key must match the value used in the "dns2hash" Cloudflare KV Store. |
| kv_value | required | The value to be paired with the key.  The value is an **array** of hosts, each in the form of `[pubkey].holohost.net`. |

### Example

```
curl -X POST "http://proxy.holohost.net/zato/holo-cloudflare-hash2tranche-create" \
 -H "[a_header]: [a_valid_key]" \
 -H "Content-Type: application/json" \
 --data '{"kv_key":"some_key", "kv_value":["[pubkey].holohost.net", "etc."]}'
```

...


## holo-cloudflare-hash2tranche-delete

### Description
This service accepts a key which is used to securely delete a KV Store entry on Cloudflare via their API.

### HTTP Request
**Method** `POST http://proxy.holohost.net/zato/holo-cloudflare-hash2tranche-delete`

### Parameters

| Parameter | Required | Description |
| -------- | -------- | -------- |
| kv_key | required | The key to be used. The key (in hash2tranche) is the hApp "holoHostingId" from the Holo Hosting hApp. |

### Example

```
curl -X POST "http://proxy.holohost.net/zato/holo-cloudflare-hash2tranche-delete" \
 -H "[a_header]: [a_valid_key]" \
 -H "Content-Type: application/json" \
 --data '{"kv_key":"some_key"}'
```

...


## holo-cloudflare-kvstore-list-keys

### Description
This service accepts a KV Store namespace name which is used to securely retrieve and list a KV Store's keys from Cloudflare via their API.

### HTTP Request
**Method** `POST http://proxy.holohost.net/zato/holo-cloudflare-list-keys`

### Parameters

| Parameter | Required | Description |
| -------- | -------- | -------- |
| kv_store | required | The kv store to be retrieved. |

### Example

```
curl -X POST "http://proxy.holohost.net/zato/holo-cloudflare-kvstore-list-keys" \
 -H "[a_header]: [a_valid_key]" \
 -H "Content-Type: application/json" \
 --data '{"kv_store":"kv_store_name"}'
```

...

## holo-cloudflare-kvstore-get-value

### Description
This service accepts a KV Store namespace name and a key which are used to securely retrieve a KV Store value from Cloudflare via their API.

### HTTP Request
**Method** `POST http://proxy.holohost.net/zato/holo-cloudflare-get-value`

### Parameters

| Parameter | Required | Description |
| -------- | -------- | -------- |
| kv_store | required | The kv store to be used. |
| kv_key | required | The key to be used. |

### Example

```
curl -X POST "http://proxy.holohost.net/zato/holo-cloudflare-kvstore-get-value" \
 -H "[a_header]: [a_valid_key]" \
 -H "Content-Type: application/json" \
 --data '{"kv_store":"kv_store_name","kv_key":"some_key"}'
```

...

