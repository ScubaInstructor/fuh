Vorbereitung der Date für 10000 pro Kategorie

```
./dataset_sample_rnd_records.sh -i combined_CSECICIDS2018_improved -o sampled_CSECICIDS2018_improved -t 10000
Randomly selected 10000 from BENIGN_59353486.csv (total: 59353486)
Randomly selected 10000 from Botnet_Ares_142921.csv (total: 142921)
Randomly selected 10000 from DDoS-HOIC_1082293.csv (total: 1082293)
Randomly selected 10000 from DDoS-LOIC-HTTP_289328.csv (total: 289328)
Copied all 2527 records from DDoS-LOIC-UDP_2527.csv
Randomly selected 10000 from DoS_GoldenEye_22560.csv (total: 22560)
Randomly selected 10000 from DoS_Hulk_1803160.csv (total: 1803160)
Copied all 8490 records from DoS_Slowloris_8490.csv
Copied all 204 records from Infiltration_-_Communication_Victim_Attacker_204.csv
Copied all 85 records from Infiltration_-_Dropbox_Download_85.csv
Randomly selected 10000 from Infiltration_-_NMAP_Portscan_89374.csv (total: 89374)
Randomly selected 10000 from SSH-BruteForce_94197.csv (total: 94197)
Copied all 131 records from Web_Attack_-_Brute_Force_131.csv
Copied all 39 records from Web_Attack_-_SQL_39.csv
Copied all 113 records from Web_Attack_-_XSS_113.csv
```

Markdown Table for All Files:

| Filename | Records in File | Target Records | Missing Records | Fraction Available | Missing (%) | Ratio |
|----------|-----------------|----------------|-----------------|------------------|-------------|-------|
| BENIGN_10000.csv | 59353486 | 10000 | 0 | 100% | 0% | 1:1 |
| Botnet_Ares_10000.csv | 142921 | 10000 | 0 | 100% | 0% | 1:1 |
| DDoS-HOIC_10000.csv | 1082293 | 10000 | 0 | 100% | 0% | 1:1 |
| DDoS-LOIC-HTTP_10000.csv | 289328 | 10000 | 0 | 100% | 0% | 1:1 |
| DDoS-LOIC-UDP_2527.csv | 2527 | 10000 | 7473 | 25% | 75% | 1:4 |
| DoS_GoldenEye_10000.csv | 22560 | 10000 | 0 | 100% | 0% | 1:1 |
| DoS_Hulk_10000.csv | 1803160 | 10000 | 0 | 100% | 0% | 1:1 |
| DoS_Slowloris_8490.csv | 8490 | 10000 | 1510 | 85% | 15% | 1:1 |
| Infiltration_-_Communication_Victim_Attacker_204.csv | 204 | 10000 | 9796 | 2% | 98% | 1:49 |
| Infiltration_-_Dropbox_Download_85.csv | 85 | 10000 | 9915 | 1% | 99% | 1:118 |
| Infiltration_-_NMAP_Portscan_10000.csv | 89374 | 10000 | 0 | 100% | 0% | 1:1 |
| SSH-BruteForce_10000.csv | 94197 | 10000 | 0 | 100% | 0% | 1:1 |
| Web_Attack_-_Brute_Force_131.csv | 131 | 10000 | 9869 | 1% | 99% | 1:76 |
| Web_Attack_-_SQL_39.csv | 39 | 10000 | 9961 | 0% | 100% | 1:256 |
| Web_Attack_-_XSS_113.csv | 113 | 10000 | 9887 | 1% | 99% | 1:88 |

