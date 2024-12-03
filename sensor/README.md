### Erster Sensor Versuch im Docker Container

Docker Compose Projekt das einen Sensor erstellt. 
Anpassen von *.env* und dann starten mit `docker-compose up`.

Zum Senden von Dateien muss noch ein ssh-Keypair erstellt werden (z.B. mit `ssh-keygen`) und in *.env* 
konfiguriert werden. Dabei muss nur der name des Schlüssels, alse etwa *idrsa* und nicht *idrsa.pub* verwendet werden. Der Schlüssel muss Zugang zu dem Server gewähren, der die .pcap Dateien erhalten soll. Das kann mit dem Kommando `ssh-copy-id -i SCHLÜSSELNAME user@remoteserver` gemacht werden.

