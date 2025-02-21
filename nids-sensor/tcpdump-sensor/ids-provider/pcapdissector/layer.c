#include "layers/ethernet-layer.h"
#include "layers/wifi-layer.h"
#include "layers/fddi-layer.h"
#include "layers/linux-cooked-layer.h"
#include "layers/loop-null-layer.h"
#include "layers/loopback-layer.h"
#include "layers/ppp-layer.h"
#include "layers/pppoe-layer.h"
#include "layers/radiotap-layer.h"
#include "layers/raw-ip-layer.h"
#include "layers/slip-layer.h"

#include "layer.h"
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <tcp-layer.h>
#include <udp-layer.h>
#include <pcap/dlt.h>

#include "arp-layer.h"
#include "dhcp-layer.h"
#include "dns-layer.h"
#include "icmpv6-layer.h"
#include "igmp-layer.h"
#include "ipv6-layer.h"
#include "llc-layer.h"
#include "mdns-layer.h"
#include "protocols/ntp-layer.h"
#include "sctp-layer.h"
#include "sna-path-control-layer.h"
#include "snap-layer.h"
#include "snmp-layer.h"
#include "ssdp-layer.h"
#include "stp-layer.h"
#include "udp-port-custom-layer.h"
#include "protocols/ipv4-layer.h"

handler_t handlers[] = {
    // DLT Handlers (is_dlt = 1)
    {0x01, "eth", dissect_ethernet, 1}, // DLT_EN10MB
    {0x0C, "Raw IP", dissect_raw_ip, 1}, // DLT_RAW
    {0x69, "Wi-Fi", dissect_wifi, 1}, // DLT_IEEE802_11
    {0x71, "Linux Cooked", dissect_linux_cooked, 1}, // DLT_LINUX_SLL
    {0x00, "BSD Loopback", dissect_loop_null, 1}, // DLT_NULL
    {0x6C, "Loopback", dissect_loop, 1}, // DLT_LOOP
    {0x09, "PPP", dissect_ppp, 1}, // DLT_PPP
    {0x33, "PPPoE", dissect_pppoe, 1}, // DLT_PPP_ETHER
    {0x08, "SLIP", dissect_slip, 1}, // DLT_SLIP
    {0x0A, "FDDI", dissect_fddi, 1}, // DLT_FDDI
    {0x7F, "Wi-Fi Radiotap", dissect_radiotap, 1}, // DLT_IEEE802_11_RADIO

    // Protocol Handlers (is_dlt = 0)
    {0x0800, "ip", dissect_ipv4, 0}, // IPv4 Ethertype
    {0x86DD, "ip", dissect_ipv6, 0}, // IPv6 Ethertype
    {0x0806, "arp", dissect_arp, 0}, // ARP Ethertype
    {0x8864, "PPPoE", dissect_pppoe, 0}, // PPPoE Ethertype
    {0x0002, "IGMP", dissect_igmp, 0}, // IGMP Protocol
    {0x0084, "SCTP", dissect_sctp, 0}, // SCTP Protocol
    {0x06, "tcp", dissect_tcp, 0}, // TCP Protocol
    {0x11, "udp", dissect_udp, 0}, // UDP Protocol
    {0x3A, "ICMPv6", dissect_icmpv6, 0}, // ICMPv6 Protocol
    {0x4000, "sna", dissect_sna_path_control, 0},
    {0x35, "dns", dissect_dns, 0}, // DNS (UDP Port 53)
    {0xA1, "SNMP", dissect_snmp, 0}, // SNMP (UDP Port 161)

    // LLC Protocol Handlers
    {0x05DC, "llc", dissect_llc, 2}, // LLC
    {0x4242, "stp", dissect_stp, 2}, // STP
    {0xAAAA, "snap", dissect_snap, 2}, // SNAP

    {0xFFFF, NULL, NULL, 0} // End marker
};

handler_t udp_port_handlers[] = {
    {0x35, "dns", dissect_dns, 3},
    {0x43, "dhcp", dissect_dhcp,3},
    {0x44, "dhcp", dissect_dhcp,3},
    //{ 0x45, "TFTP", dissect_tftp },
    {0x7B, "ntp", dissect_ntp,3},
    //{ 0x89, "NBNS", dissect_nbns },
    //{ 0x8A, "NBDGM", dissect_nbdgm },
    {0xA1, "snmp", dissect_snmp,3},
    {0xA2, "SNMP-TRAP", dissect_snmp,3},
    //{ 0x1F4, "ISAKMP", dissect_isakmp },
    //{ 0x202, "Syslog", dissect_syslog },
    //{ 0x208, "RIP", dissect_rip },
    // {0x76C, "ssdp", dissect_ssdp,3},
    {0x14E9, "mDNS", dissect_mdns,3},
    //{ 0x1194, "IPsec NAT-T", dissect_ipsec_nat_t },
    //{ 0x13C4, "SIP", dissect_sip },
    //{ 0x14E9, "mDNS", dissect_mdns },
    {0x3CF0, "udp-port", dissect_udp_port_custom,3}, // SAMSUNG TV remote control?
    {0x7E9C, "udp-plex", dissect_udp_port_custom,3}, // Plex Media Server!
    {0x7E9E, "udp-plex", dissect_udp_port_custom,3}, // Plex Media Server!
    {0x0, NULL, NULL} // End marker
};

/* Free a layer and all subsequent layers */
void layer_free(layer_t *layer) {
    if (!layer) return;

    // Free the parsed data
    if (layer->parsed_data) {
        free(layer->parsed_data);
    }
}
