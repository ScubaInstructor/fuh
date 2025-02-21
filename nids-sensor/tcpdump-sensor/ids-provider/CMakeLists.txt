cmake_minimum_required(VERSION 3.14)

#set(CMAKE_PREFIX_PATH ${CMAKE_PREFIX_PATH} "/usr/local")

project(ids-provider LANGUAGES C)

# Find required libraries using pkg-config
find_package(PkgConfig REQUIRED)
pkg_check_modules(rdkafka REQUIRED IMPORTED_TARGET rdkafka)
pkg_check_modules(lz4 REQUIRED IMPORTED_TARGET liblz4)

add_library(ids-provider STATIC
        common-util.c
        ring-buffer.c
        processor_threads.c
        dissection-processor.c
        kafka-processor.c
        pcapdissector/packet.c
        pcapdissector/layer.c
        pcapdissector/layers/wifi-layer.c
        pcapdissector/layers/ethernet-layer.c
        pcapdissector/layers/raw-ip-layer.c
        pcapdissector/layers/linux-cooked-layer.c
        pcapdissector/layers/loopback-layer.c
        pcapdissector/layers/ppp-layer.c
        pcapdissector/layers/loop-null-layer.c
        pcapdissector/layers/pppoe-layer.c
        pcapdissector/layers/slip-layer.c
        pcapdissector/layers/fddi-layer.c
        pcapdissector/layers/radiotap-layer.c
        pcapdissector/protocols/ipv4-layer.c
        pcapdissector/protocols/tcp-layer.c
        pcapdissector/protocols/udp-layer.c
        pcapdissector/protocols/icmp-layer.c
        pcapdissector/protocols/ipv6-layer.c
        pcapdissector/protocols/arp-layer.c
        pcapdissector/protocols/vlan-layer.c
        pcapdissector/protocols/igmp-layer.c
        pcapdissector/protocols/sctp-layer.c
        pcapdissector/protocols/llc-layer.c
        pcapdissector/protocols/stp-layer.c
        pcapdissector/protocols/snap-layer.c
        pcapdissector/protocols/icmpv6-layer.c
        pcapdissector/protocols/sna-path-control-layer.c
        pcapdissector/protocols/dns-layer.c
        pcapdissector/protocols/snmp-layer.c
        pcapdissector/protocols/dhcp-layer.c
        pcapdissector/protocols/ntp-layer.c
        pcapdissector/protocols/ssdp-layer.c
        pcapdissector/protocols/ssdp-layer.h
        pcapdissector/protocols/udp-port-custom-layer.c
        pcapdissector/protocols/udp-port-custom-layer.h
        pcapdissector/protocols/mdns-layer.c
        pcapdissector/protocols/mdns-layer.h
        yaml-processor.c
)

target_include_directories(ids-provider PRIVATE
        pcapdissector
        pcapdissector/layers
        pcapdissector/protocols
)

target_link_libraries(ids-provider PRIVATE
        PkgConfig::lz4
        PkgConfig::rdkafka
)