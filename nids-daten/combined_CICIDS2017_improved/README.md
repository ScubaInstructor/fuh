Es gibt in den Daten die Kategorie Attempted, d.h. es wurde ein Angriff erkannt aber da die Nutzdaten im Netzwerkverkehr fehlen war der Angriff nicht erfolgreich.

Die Empfehlung ist Attempted nicht als eigene Kategorie zu verwenden, sonder als normalen Datenverkehr zu betrachten.

Da die Anzahl der Versuche sehr gering ist haben wir und entschieden alle Attempted zu ignorieren.

Quelle: https://intrusion-detection.distrinet-research.be/CNS2022/Dataset_Download.html


Erstellung der "combined" Dateien:

```
% ./dataset_combine.sh -input=split_CICIDS2017_improved -output=combined_CICIDS2017_improved -exclude=Attempted 
Skipping file: friday_Botnet_-_Attempted_4067.csv
```
