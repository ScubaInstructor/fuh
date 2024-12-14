### Erster Sensor Versuch im Docker Container

Sendet Flow und pcap.Daten an deinen Elastic/Kibana Server.

Docker Compose Projekt das einen Sensor erstellt. 
Anpassen von *.env* und dann starten mit `docker-compose up`.

~~Zum Senden von Dateien muss noch ein ssh-Keypair erstellt werden (z.B. mit `ssh-keygen`) und in *.env* 
eingetragen werden. Dabei muss nur der name des Schlüssels, alse etwa *idrsa* und nicht *idrsa.pub* verwendet werden. Der Schlüssel muss Zugang zu dem Server gewähren, der die .pcap Dateien erhalten soll. Das kann mit dem Kommando `ssh-copy-id -i SCHLÜSSELNAME user@remoteserver` gemacht werden.~~

~~Der zugehörige Flaskserver sollte gestartet werden um die Daten zu empfangen. ~~

Der Server in `server/Kibana` sollte mit `docker-compose up` gestartet werden, damit der Sensor erfolgreich eine Verbindung zu elastic aufbauen kann.

**Derzeit werden zu debugzwecken alle Flows gesendet, egal ob Anomalie oder nicht.**



Zum starten ohne Docker mit `sudo python sniffer` starten. 