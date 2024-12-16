### Erster Sensor Versuch im Docker Container

Sendet Flow und pcap.Daten an deinen Elastic/Kibana Server.

Docker Compose Projekt das einen Sensor erstellt. 
Anpassen von *.env* und dann starten mit `docker-compose up`.

~~Zum Senden von Dateien muss noch ein ssh-Keypair erstellt werden (z.B. mit `ssh-keygen`) und in *.env* ~~
~~eingetragen werden. Dabei muss nur der name des Schlüssels, alse etwa *idrsa* und nicht *idrsa.pub* verwendet werden. Der Schlüssel muss Zugang zu dem Server gewähren, der die .pcap Dateien erhalten soll. Das kann mit dem Kommando `ssh-copy-id -i SCHLÜSSELNAME user@remoteserver` gemacht werden.~~

~~Der zugehörige Flaskserver sollte gestartet werden um die Daten zu empfangen. ~~

Der Server in `server/Kibana` sollte mit `docker-compose up` gestartet werden und dessen ip und Portnummer in der *.env* Datei, damit der Sensor erfolgreich eine Verbindung zu elastic aufbauen kann.

Um einen API Key zu erstellen kann entweder die Weboberfläche genutzt werden, oder es kann mit 
'curl -X POST "https://ES_HOST:ES_PORT/_security/api_key" -H 'Content-Type: application/json' -u elastic_superuser:elastic_superuser_password -d '{"name": "test-api-key","role_descriptors": {"role-name": {"cluster": ["all"],"index": [{"names": ["ES_INDEX"],"privileges": ["all"]}]}}}' --insecure' 
ein API Key der Form XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX== erstellt und in  der *.env* Datei eingetragen werden. 

**Derzeit werden zu debugzwecken alle Flows gesendet, egal ob Anomalie oder nicht.**



Zum starten ohne Docker mit `sudo python sniffer` starten. 