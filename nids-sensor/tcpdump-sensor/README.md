# tcpdump-sensor

Dieses Verzeichnis enhält den source code für die Komponenten des Sensors. Der tcpdump-sensor ist Teil einer Seminarbeit zum Thema *Intelligente Anomalieerkennung in Datenströmen mittels KI*. Er dient zur Erfassung der Netzwerkpakete aus dem Datenstrom (Interface) und bereitet diese für das nachfolgende, auf KI basierende IDS-System auf.

## tcpdump-sensor
Sensor, basierend auf tcpdump 4.99.5 zu Auzeichung der Pakete, Verarbeitung und Weiterleitung an kafka

## cicflowmeter
Angepasste CICFlowmeter Version von Gints Engelen zur Erzeugung von Flows basierend auf JSON Paketen vom tcpdump-sensor

## flink-cicflowmeter
Flink CICFlowmeter Processor zur Erzeugung der Flows (verwendet cicflowmeter).

## flink-http-send
Flink HTTP Sender Processor zur Weiterleitung der flink-flowmeter Flows an den Server.

## sensor-middleware-docker
Docker compose script zum starten des kafka und flink servers für den tcpdump-sensor.
