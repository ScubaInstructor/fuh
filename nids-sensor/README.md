# tcpdump-sensor

Dieses Verzeichnis enhält den source code für den *tcpdump-sensor*. Der tcpdump-sensor ist Teil einer Seminarbeit zum Thema *Intelligente Anomalieerkennung in Datenströmen mittels KI*. Er dient zur Erfassung der Netzwerkpakete aus dem Datenstrom und bereitet diese für das nachfolgende, auf KI basierende IDS-System auf.
Dieser Sensor basiert auf tcpdump 4.99.5, dazu wurde tcpdump wurde durch eine Option erweitert:
 ```console
[ --ids-packet-provider <config.yml>] send dissected packets to ids tool using config
```
Wenn diese Option aktiviert ist wird der tcpdump dissection Mechanismus umgangen und die dissection für das IDS wird ausgeführt.


# tcpdump-sensor

 ```console
./tcpdump-sensor -h
tcpdump-sensor version 0.6
Extension of tcpdump version 4.99.5
libpcap version 1.10.1
OpenSSL 3.4.0 22 Oct 2024
SMI-library: 0.5.0
64-bit build, 64-bit time_t
Usage: tcpdump-sensor [-AbdDefhHIJKlLnNOpqStuUvxX#] [ -B size ] [ -c count ] [--count]
		[ -C file_size ] [ -E algo:secret ] [ -F file ] [ -G seconds ]
		[ -i interface ] [ --immediate-mode ] [ -j tstamptype ]
		[ -m module ] ...
		[ -M secret ] [ --number ] [ --print ] [ -Q in|out|inout ]
		[ -r file ] [ -s snaplen ] [ -T type ] [ --version ]
		[ -V file ] [ -w file ] [ -W filecount ] [ -y datalinktype ]
		[ --time-stamp-precision precision ] [ --micro ] [ --nano ]
		[ -z postrotate-command ] [ -Z user ] [ expression ]
		[ --ids-packet-provider <config.yml>]  send dissected packets to ids tool using config
```

### tcpdump-sensor compiles and works on at least the following platforms:
* {Mac} OS X / macOS (13.7 Ventura)
* alpine Linux

### Supported platforms
* MacBookPro11,3
* odroid H4 Ultra - N305


### Dependency on libpcap
tcpdump-sensor uses libpcap, a system-independent interface for user-level packet capture. If your operating system does not provide libpcap, or if it provides a libpcap that does not support the APIs from libpcap 1.0 or later, you must first retrieve and build libpcap before building tcpdump.

### Other dependencies
* liblz4
* librdkafka
