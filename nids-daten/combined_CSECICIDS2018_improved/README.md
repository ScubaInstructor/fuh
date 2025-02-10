Es gibt in den Daten die Kategorie Attempted, d.h. es wurde ein Angriff erkannt aber da die Nutzdaten im Netzwerkverkehr fehlen war der Angriff nicht erfolgreich.

Die Empfehlung ist Attempted nicht als eigene Kategorie zu verwenden, sonder als normalen Datenverkehr zu betrachten.

Da die Anzahl der Versuche sehr gering ist haben wir und entschieden alle Attempted zu ignorieren.

Quelle: https://intrusion-detection.distrinet-research.be/CNS2022/Dataset_Download.html

Erstellung der "combined" Dateien:
```
# ./dataset_combine.sh -input=split_CSECICIDS2018_improved -output=combined_CSECICIDS2018_improved -exclude=Attempted
Skipping file: Friday-02-03-2018_Botnet_Ares_-_Attempted_262.csv
Skipping file: Friday-16-02-2018_DoS_Hulk_-_Attempted_86.csv
Skipping file: Friday-16-02-2018_FTP-BruteForce_-_Attempted_105520.csv
Skipping file: Friday-23-02-2018_Web_Attack_-_Brute_Force_-_Attempted_61.csv
Skipping file: Friday-23-02-2018_Web_Attack_-_SQL_-_Attempted_10.csv
Skipping file: Friday-23-02-2018_Web_Attack_-_XSS_-_Attempted_1.csv
Skipping file: Thursday-01-03-2018_Infiltration_-_Dropbox_Download_-_Attempted_13.csv
Skipping file: Thursday-15-02-2018_DoS_GoldenEye_-_Attempted_4301.csv
Skipping file: Thursday-15-02-2018_DoS_Slowloris_-_Attempted_2280.csv
Skipping file: Thursday-22-02-2018_Web_Attack_-_Brute_Force_-_Attempted_76.csv
Skipping file: Thursday-22-02-2018_Web_Attack_-_SQL_-_Attempted_4.csv
Skipping file: Thursday-22-02-2018_Web_Attack_-_XSS_-_Attempted_3.csv
Skipping file: Tuesday-20-02-2018_DDoS-LOIC-UDP_-_Attempted_80.csv
Skipping file: Wednesday-14-02-2018_FTP-BruteForce_-_Attempted_193354.csv
Skipping file: Wednesday-21-02-2018_DDoS-LOIC-UDP_-_Attempted_171.csv
Skipping file: Wednesday-28-02-2018_Infiltration_-_Dropbox_Download_-_Attempted_15.csv
Combined CSV files have been created in combined_CSECICIDS2018_improved.
```

| File Name                                      | Size (MB) | Record Count |
|-----------------------------------------------|----------:|------------:|
| BENIGN_59353486.csv                           |     32251 |     59353486 |
| Botnet_Ares_142921.csv                        |        79 |       142921 |
| DDoS-HOIC_1082293.csv                         |       597 |      1082293 |
| DDoS-LOIC-HTTP_289328.csv                     |       175 |       289328 |
| DDoS-LOIC-UDP_2527.csv                        |         1 |         2527 |
| DoS_GoldenEye_22560.csv                       |        14 |        22560 |
| DoS_Hulk_1803160.csv                          |      1039 |      1803160 |
| DoS_Slowloris_8490.csv                        |         5 |         8490 |
| Infiltration_-_Communication_Victim_Attacker_204.csv |         0 |          204 |
| Infiltration_-_Dropbox_Download_85.csv        |         0 |           85 |
| Infiltration_-_NMAP_Portscan_89374.csv        |        36 |        89374 |
| SSH-BruteForce_94197.csv                      |        61 |        94197 |
| Web_Attack_-_Brute_Force_131.csv              |         0 |          131 |
| Web_Attack_-_SQL_39.csv                       |         0 |           39 |
| Web_Attack_-_XSS_113.csv                      |         0 |          113 |
| **Total**                                      | **34258 MB** | **62888908** |
