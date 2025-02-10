Es gibt in den Daten die Kategorie Attempted, d.h. es wurde ein Angriff erkannt aber da die Nutzdaten im Netzwerkverkehr fehlen war der Angriff nicht erfolgreich.

Die Empfehlung ist Attempted nicht als eigene Kategorie zu verwenden, sonder als normalen Datenverkehr zu betrachten.

Da die Anzahl der Versuche sehr gering ist haben wir und entschieden alle Attempted zu ignorieren.

Quelle: https://intrusion-detection.distrinet-research.be/CNS2022/Dataset_Download.html


Erstellung der "combined" Dateien:

```
./dataset_combine.sh -input=split_CICIDS2017_improved -output=combined_CICIDS2017_improved -exclude=Attempted
Skipping file: friday_Botnet_-_Attempted_4067.csv
Skipping file: thursday_Infiltration_-_Attempted_45.csv
Skipping file: thursday_Web_Attack_-_Brute_Force_-_Attempted_1292.csv
Skipping file: thursday_Web_Attack_-_SQL_Injection_-_Attempted_5.csv
Skipping file: thursday_Web_Attack_-_XSS_-_Attempted_655.csv
Skipping file: tuesday_FTP-Patator_-_Attempted_12.csv
Skipping file: tuesday_SSH-Patator_-_Attempted_27.csv
Skipping file: wednesday_DoS_GoldenEye_-_Attempted_80.csv
Skipping file: wednesday_DoS_Hulk_-_Attempted_581.csv
Skipping file: wednesday_DoS_Slowhttptest_-_Attempted_3368.csv
Skipping file: wednesday_DoS_Slowloris_-_Attempted_1847.csv
Combined CSV files have been created in combined_CICIDS2017_improved.
```
