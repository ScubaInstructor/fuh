# fuh 
This is the Repository of Group 2 of the Fachpraktikum "Intelligente Anomalieerkennung in Datenströmen mittels KI" from the Fernuniversität in Hagen, Germany.

We introduce an hostbased intrusion detection system around the CIC-IDS-2017 Dataset from The Canadian Institue for Cybersecurity of the University New Brunswick. The IDS is divided in a Server and sensor Components. The Server is build around an elastic backend and a dash frontend. The sensors can be placed onto machines to monitor for attacks on. 
The incoming networktraffic will be grouped into flows and evaluated by machine learning techniques for known attacks. Flows categorized as non-benign will be sent to the server to be categorized by the users. A new, adapted model, can be trained if new flows have been categorized. The new model will be sent to the sensors, for better attack detection.

The server component can be found in [this](dockerized-dash-elastic-server) folder. Follow instructions in the local README to start the server. 

The sensor is located in [this](sensor) folder. There is al local README with instructions to start the sensor. 
