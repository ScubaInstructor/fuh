Konfiguriert und startet das Docker Netzwerk mit kafka und flink.

docker compose -f 63184-docker-compose.yml up -d

### start-docker.sh
Auf OSX Intel kann es vorkommen, dass das ARM image von kafka geladen und im emulator Modus ausgeführt wird.
Um das richtige Image in Docker zu laden, kann das start-docker.sh script verwendet werden.
