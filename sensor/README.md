### Sensor with local model file in docker container

If anomaly detected, the sensor will send the flow, including pcap-file to the specified server. The sensor will check for new model updates, every 6 hours, and before sending a flow. If a new model is available, it will be downloaded and the flow will be reevaluated. 

Get a configuartion file like the *example.env* for your sensor from the server and put it in this folder. It has to be renamed to *.env*! Build your Docker container with  `sudo docker-compose up --build` after the servercomponent is up and running.

The server is located [here](../dockerized-dash-elastic-server) and has to be started first.

After the build process you can restart the container with `sudo docker-compose up`. If there is a change in the *.env* file, you have to rebuild the container as written above. 