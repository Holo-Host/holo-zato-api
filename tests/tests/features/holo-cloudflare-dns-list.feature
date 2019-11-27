Feature: holo zato api holo-cloudflare-dns-list

Scenario: *** Holo zato api GET dns list ***

    Given address "http://proxy.holohost.net"
    Given URL path "/zato/holo-cloudflare-dns-list"
    Given header "$KEY_HEADER" "$KEY"
    Given HTTP method "GET"

    When the URL is invoked

    Then status is "200"
    And header "Connection" is "keep-alive"
    And header "Server" is "Zato"

    And JSON response exists