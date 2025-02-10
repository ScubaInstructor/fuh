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


# Dataset File Details

| Filename                               | Size (MB) | Records  |
|----------------------------------------|----------:|---------:|
| BENIGN_1582566.csv                     |   833.95  | 1582566  |
| Botnet_736.csv                          |     0.42  |     736  |
| DDoS_95144.csv                          |    60.04  |   95144  |
| DoS_GoldenEye_7567.csv                  |     5.16  |    7567  |
| DoS_Hulk_158468.csv                     |    98.42  |  158468  |
| DoS_Slowhttptest_1740.csv               |     1.12  |    1740  |
| DoS_Slowloris_3859.csv                   |     2.32  |    3859  |
| FTP-Patator_3972.csv                     |     2.59  |    3972  |
| Heartbleed_11.csv                        |     0.01  |      11  |
| Infiltration_-_Portscan_71767.csv        |    28.06  |   71767  |
| Infiltration_36.csv                      |     0.03  |      36  |
| Portscan_159066.csv                      |    58.99  |  159066  |
| SSH-Patator_2961.csv                     |     1.96  |    2961  |
| Web_Attack_-_Brute_Force_73.csv          |     0.05  |      73  |
| Web_Attack_-_SQL_Injection_13.csv        |     0.01  |      13  |
| Web_Attack_-_XSS_18.csv                  |     0.01  |      18  |

