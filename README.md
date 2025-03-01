# Abschlussarbeit Fachpraktikum Softwareentwicklung mit
Methoden der Künstlichen Intelligenz

This is the Repository of Group 2 of the Fachpraktikum "Intelligente Anomalieerkennung in Datenströmen mittels KI" from the Fernuniversität in Hagen, Germany.

We introduce an intrusion detection system around the improved-CIC-IDS-2017 Dataset from The Canadian Institue for Cybersecurity of the University New Brunswick and Lisa Liu/Gints Engelen. The IDS is divided in Server and sensor Components. The Server is build around an ElasticSearch backend and a dash frontend. The sensors can be placed onto machines to monitor for attacks on. 
The incoming networktraffic will be grouped into flows and evaluated by machine learning techniques for known attacks. Flows  will be sent to the server to be classified by a machine learning algorithm. Anomalous flows will  afterwards be inspected and categorized by the users. A new model, adapted to the manually categorized flows, can be trained. 

The server component can be found in [this](dockerized-dash-elastic-server) folder. Follow instructions in the local README to start the server. 

The sensor is located in [this](nids-sensor) folder. There is a local README with instructions how to start the sensor. 
