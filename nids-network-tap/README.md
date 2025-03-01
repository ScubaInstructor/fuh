Enable additional repositories:

```console
echo "http://dl-cdn.alpinelinux.org/alpine/v3.21/community" >> /etc/apk/repositories
apk update
apk add lshw
```

Configure network interfaces

```console
odroid-alpine:~$ vi /etc/network/interfaces
auto lo
iface lo inet loopback

auto eth0
iface eth0 inet dhcp

auto eth1
iface eth1 inet dhcp

auto bridge0
iface bridge0 inet manual
	bridge-ports eth2 eth3
	up ip link set $IFACE up
	down ip link set $IFACE down

auto bridge1
iface bridge1 inet manual
	bridge-ports eth4 eth5
	up ip link set $IFACE up
	down ip link set $IFACE down
```

Install libpcap
```console
´# apk add libpcap
(1/1) Installing libpcap (1.10.5-r0)
OK: 219 MiB in 80 packages
```

