Feature: holo zato api holo-cloudflare-dns-read

Scenario: *** Holo zato api POST {} ***

    Given address "http://proxy.holohost.net"
    Given URL path "/zato/holo-cloudflare-dns-read"
    Given header "$KEY_HEADER" "$KEY"
    Given HTTP method "POST"
    Given format "JSON"
    Given request is "{}"

    When the URL is invoked

    Then status is "400"
    And header "Connection" is "keep-alive"
    And header "Server" is "Zato"

    And JSON response exists