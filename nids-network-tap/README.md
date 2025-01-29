

echo "http://dl-cdn.alpinelinux.org/alpine/v3.21/community" >> /etc/apk/repositories
apk update
apk add lshw


vi /etc/network/interfaces

```console
# cat /etc/network/interfaces
auto lo
iface lo inet loopback

auto eth0
iface eth0 inet dhcp

auto eth1
iface eth1 inet dhcp

auto eth2
iface eth2 inet dhcp

auto eth3
iface eth2 inet dhcp

auto eth4
iface eth2 inet dhcp

auto eth5
iface eth2 inet dhcp

auto eth6
iface eth2 inet dhcp
```

Install libpcap
```console
´# apk add libpcap
(1/1) Installing libpcap (1.10.5-r0)
OK: 219 MiB in 80 packages
```

