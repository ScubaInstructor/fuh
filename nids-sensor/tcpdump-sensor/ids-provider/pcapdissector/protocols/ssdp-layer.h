#ifndef SSDP_LAYER_H
#define SSDP_LAYER_H

#include "layer.h"
#include "packet.h"

typedef struct {
    int is_request;                // 1 = Request, 0 = Response

    // For Requests (M-SEARCH, NOTIFY, etc.)
    char method[16];               // Request method (e.g., "M-SEARCH", "NOTIFY")
    char uri[256];                 // Target URI (e.g., "*")

    // For Responses (HTTP/1.1 200 OK)
    int status_code;               // HTTP response status code

    // Common SSDP Headers
    char host[64];                 // "HOST: 239.255.255.250:1900"
    char st[128];                  // "ST: upnp:rootdevice" (Search Target)
    char usn[128];                 // "USN: uuid:device-UUID"
    char location[256];             // "LOCATION: http://192.168.1.1:8080/desc.xml"
    char nts[64];                   // "NTS: ssdp:alive"
    char nt[128];                   // "NT: upnp:rootdevice"
    char server[128];               // "SERVER: OS/version UPnP/1.0 product/version"
    char cache_control[32];         // "CACHE-CONTROL: max-age=1800"
    int max_age;                    // Parsed max-age from CACHE-CONTROL
    char ext[8];                    // "EXT:" (empty, just must be present)

} ssdp_header_t;


int dissect_ssdp(layer_t *layer, packet_t *packet, const uint8_t *data, size_t len);
char *ssdp_to_json(layer_t *layer);
void ssdp_layer_free(layer_t *layer);

#endif // SSDP_LAYER_H
