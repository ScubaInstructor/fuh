### Arkime Container

Ein Docker-Compose Projekt das Elastic Search und Arkime Verbindet. 

https://arkime.com/

Es können Pcap Dateien in ein Verzeichnis hochgeladen werden und diese 
werden durch einen Cronjob autuomatisch in Arkime importiert. 

*.env* Datei anpassen, *update_consume_folder_cron* anpassen und mit `docker-compose up -d` starten.

Angepasster Code von https://github.com/mammo0/docker-arkime