
# Network Traffic Analysis Summary

Die CNS2022 Daten wurden von hier heruntergeladen:
https://intrusion-detection.distrinet-research.be/CNS2022/Datasets/

Die unzipped-Datensets wurden im ersten Schritt separat verarbeitet:

Verifizierung der Gesamtzahl der network flows im Datenset CIC-IDS-2017:
```console
DATASET_engelen_improved/CICIDS2017_improved# ../count_data_records.sh
Total number of records (excluding headers): 2099976
```

| Dataset | Size (MB) | Number of Records |
|---------|----------:|-------------------|
| CICIDS2017 | 327.55 | 2,099,976 |
| CSECICIDS2018 | 9,939.50 | 10,426,851,729 |
| **Total** | **10,267.05** | **** |

Verifizierung der Gesamtzahl der network flows im Datenset CSE-CIC-IDS 2018:
```console
DATASET_engelen_improved/CICIDS2017_improved# ../count_data_records.sh
Total number of records (excluding headers): 2099976
```

## CIC-IDS-2017 data files

| Filename | Records | % of Total | Size (MB) |
|----------|--------:|------------|----------:|
| monday_BENIGN_371624.csv | 371,624 | 17.70% | 198.25 |
| tuesday_BENIGN_315106.csv | 315,106 | 15.01% | 165.56 |
| tuesday_FTP-Patator - Attempted_12.csv | 12 | 0.00% | 0.01 |
| tuesday_FTP-Patator_3972.csv | 3,972 | 0.19% | 2.59 |
| tuesday_SSH-Patator - Attempted_27.csv | 27 | 0.00% | 0.01 |
| tuesday_SSH-Patator_2961.csv | 2,961 | 0.14% | 1.96 |
| wednesday_BENIGN_319120.csv | 319,120 | 15.20% | 167.91 |
| wednesday_DoS GoldenEye - Attempted_80.csv | 80 | 0.00% | 0.03 |
| wednesday_DoS GoldenEye_7567.csv | 7,567 | 0.36% | 5.16 |
| wednesday_DoS Hulk - Attempted_581.csv | 581 | 0.03% | 0.28 |
| wednesday_DoS Hulk_158468.csv | 158,468 | 7.55% | 98.40 |
| wednesday_DoS Slowhttptest - Attempted_3368.csv | 3,368 | 0.16% | 1.74 |
| wednesday_DoS Slowhttptest_1740.csv | 1,740 | 0.08% | 1.12 |
| wednesday_DoS Slowloris - Attempted_1847.csv | 1,847 | 0.09% | 0.84 |
| wednesday_DoS Slowloris_3859.csv | 3,859 | 0.18% | 2.32 |
| wednesday_Heartbleed_11.csv | 11 | 0.00% | 0.01 |
| thursday_BENIGN_288172.csv | 288,172 | 13.72% | 151.55 |
| thursday_Infiltration - Attempted_45.csv | 45 | 0.00% | 0.02 |
| thursday_Infiltration - Portscan_71767.csv | 71,767 | 3.42% | 28.06 |
| thursday_Infiltration_36.csv | 36 | 0.00% | 0.03 |
| thursday_Web Attack - Brute Force - Attempted_1292.csv | 1,292 | 0.06% | 0.68 |
| thursday_Web Attack - Brute Force_73.csv | 73 | 0.00% | 0.05 |
| thursday_Web Attack - SQL Injection - Attempted_5.csv | 5 | 0.00% | 0.00 |
| thursday_Web Attack - SQL Injection_13.csv | 13 | 0.00% | 0.01 |
| thursday_Web Attack - XSS - Attempted_655.csv | 655 | 0.03% | 0.34 |
| thursday_Web Attack - XSS_18.csv | 18 | 0.00% | 0.01 |
| friday_BENIGN_288544.csv | 288,544 | 13.74% | 150.90 |
| friday_Botnet - Attempted_4067.csv | 4,067 | 0.19% | 1.60 |
| friday_Botnet_736.csv | 736 | 0.04% | 0.42 |
| friday_DDoS_95144.csv | 95,144 | 4.53% | 60.04 |
| friday_Portscan_159066.csv | 159,066 | 7.57% | 59.02 |
| **Total** | **2,099,926** | **100.00%** | **1,098.91** |

Aufteilung der Datein:
```console
DATASET_engelen_improved\CICIDS2017_improved>..\split_dataset.sh . processed-dataset-split
```

## CIC-IDS-2017 Attack Summary

| Attack Type | Number of Attacks | % of Total |
|-------------|------------------:|------------|
| Botnet | 4,803 | 1.26% |
| DDoS | 95,144 | 24.93% |
| DoS GoldenEye | 7,647 | 2.00% |
| DoS Hulk | 159,049 | 41.68% |
| DoS Slowhttptest | 5,108 | 1.34% |
| DoS Slowloris | 5,706 | 1.50% |
| FTP-Patator | 3,984 | 1.04% |
| Heartbleed | 11 | 0.00% |
| Infiltration | 71,848 | 18.83% |
| Portscan | 159,066 | 41.69% |
| SSH-Patator | 2,988 | 0.78% |
| Web Attack - Brute Force | 1,365 | 0.36% |
| Web Attack - SQL Injection | 18 | 0.00% |
| Web Attack - XSS | 673 | 0.18% |
| **Total** | **381,410** | **100.00%** |

# Network Traffic Analysis Summary (2018 Dataset)

## CSE-CIC-IDS 2018 File data files

Here's the markdown table sorted by weekday and date, with the number of records, percentage of total records, and file size in MB:

| Filename | Records | % of Total | Size (MB) |
|----------|--------:|------------|----------:|
| Tuesday-20-02-2018_BENIGN_5764497.csv | 5,764,497 | 14.99% | 3,096.43 |
| Tuesday-20-02-2018_DDoS-LOIC-HTTP_289328.csv | 289,328 | 0.75% | 175.21 |
| Tuesday-20-02-2018_DDoS-LOIC-UDP - Attempted_80.csv | 80 | 0.00% | 0.04 |
| Tuesday-20-02-2018_DDoS-LOIC-UDP_797.csv | 797 | 0.00% | 0.39 |
| Wednesday-14-02-2018_BENIGN_5610799.csv | 5,610,799 | 14.59% | 2,979.39 |
| Wednesday-14-02-2018_FTP-BruteForce - Attempted_193354.csv | 193,354 | 0.50% | 70.19 |
| Wednesday-14-02-2018_SSH-BruteForce_94197.csv | 94,197 | 0.24% | 61.74 |
| Wednesday-21-02-2018_BENIGN_5878399.csv | 5,878,399 | 15.29% | 3,171.18 |
| Wednesday-21-02-2018_DDoS-HOIC_1082293.csv | 1,082,293 | 2.81% | 597.27 |
| Wednesday-21-02-2018_DDoS-LOIC-UDP - Attempted_171.csv | 171 | 0.00% | 0.08 |
| Wednesday-21-02-2018_DDoS-LOIC-UDP_1730.csv | 1,730 | 0.00% | 0.85 |
| Wednesday-28-02-2018_BENIGN_6518882.csv | 6,518,882 | 16.95% | 3,614.98 |
| Wednesday-28-02-2018_Infiltration - Communication Victim Attacker_43.csv | 43 | 0.00% | 0.03 |
| Wednesday-28-02-2018_Infiltration - Dropbox Download - Attempted_15.csv | 15 | 0.00% | 0.01 |
| Wednesday-28-02-2018_Infiltration - Dropbox Download_46.csv | 46 | 0.00% | 0.03 |
| Wednesday-28-02-2018_Infiltration - NMAP Portscan_49740.csv | 49,740 | 0.13% | 20.32 |
| Thursday-15-02-2018_BENIGN_5372471.csv | 5,372,471 | 13.97% | 2,830.25 |
| Thursday-15-02-2018_DoS GoldenEye - Attempted_4301.csv | 4,301 | 0.01% | 2.53 |
| Thursday-15-02-2018_DoS GoldenEye_22560.csv | 22,560 | 0.06% | 14.60 |
| Thursday-15-02-2018_DoS Slowloris - Attempted_2280.csv | 2,280 | 0.01% | 1.03 |
| Thursday-15-02-2018_DoS Slowloris_8490.csv | 8,490 | 0.02% | 5.29 |
| Thursday-22-02-2018_BENIGN_6070945.csv | 6,070,945 | 15.79% | 3,312.49 |
| Thursday-22-02-2018_Web Attack - Brute Force - Attempted_76.csv | 76 | 0.00% | 0.05 |
| Thursday-22-02-2018_Web Attack - Brute Force_69.csv | 69 | 0.00% | 0.05 |
| Thursday-22-02-2018_Web Attack - SQL - Attempted_4.csv | 4 | 0.00% | 0.00 |
| Thursday-22-02-2018_Web Attack - SQL_16.csv | 16 | 0.00% | 0.01 |
| Thursday-22-02-2018_Web Attack - XSS - Attempted_3.csv | 3 | 0.00% | 0.00 |
| Thursday-22-02-2018_Web Attack - XSS_40.csv | 40 | 0.00% | 0.03 |
| Thursday-01-03-2018_BENIGN_6511554.csv | 6,511,554 | 16.93% | 3,615.65 |
| Thursday-01-03-2018_Infiltration - Communication Victim Attacker_161.csv | 161 | 0.00% | 0.11 |
| Thursday-01-03-2018_Infiltration - Dropbox Download - Attempted_13.csv | 13 | 0.00% | 0.01 |
| Thursday-01-03-2018_Infiltration - Dropbox Download_39.csv | 39 | 0.00% | 0.03 |
| Thursday-01-03-2018_Infiltration - NMAP Portscan_39634.csv | 39,634 | 0.10% | 15.96 |
| Friday-16-02-2018_BENIGN_5481500.csv | 5,481,500 | 14.25% | 2,938.22 |
| Friday-16-02-2018_DoS Hulk - Attempted_86.csv | 86 | 0.00% | 0.03 |
| Friday-16-02-2018_DoS Hulk_1803160.csv | 1,803,160 | 4.69% | 1,039.12 |
| Friday-16-02-2018_FTP-BruteForce - Attempted_105520.csv | 105,520 | 0.27% | 39.00 |
| Friday-23-02-2018_BENIGN_5976251.csv | 5,976,251 | 15.54% | 3,251.15 |
| Friday-23-02-2018_Web Attack - Brute Force - Attempted_61.csv | 61 | 0.00% | 0.04 |
| Friday-23-02-2018_Web Attack - Brute Force_62.csv | 62 | 0.00% | 0.05 |
| Friday-23-02-2018_Web Attack - SQL - Attempted_10.csv | 10 | 0.00% | 0.01 |
| Friday-23-02-2018_Web Attack - SQL_23.csv | 23 | 0.00% | 0.02 |
| Friday-23-02-2018_Web Attack - XSS - Attempted_1.csv | 1 | 0.00% | 0.00 |
| Friday-23-02-2018_Web Attack - XSS_73.csv | 73 | 0.00% | 0.05 |
| Friday-02-03-2018_BENIGN_6168188.csv | 6,168,188 | 16.04% | 3,439.36 |
| Friday-02-03-2018_Botnet Ares - Attempted_262.csv | 262 | 0.00% | 0.11 |
| Friday-02-03-2018_Botnet Ares_142921.csv | 142,921 | 0.37% | 79.16 |
| **Total** | **38,454,876** | **100.00%** | **28,372.55** |

## CSE-CIC-IDS 2018 Attack Summary

| Attack Type | Number of Attacks | % of Total |
|-------------|------------------:|------------|
| Botnet Ares | 143,183 | 3.81% |
| DDoS-HOIC | 1,082,293 | 28.80% |
| DDoS-LOIC-HTTP | 289,328 | 7.70% |
| DDoS-LOIC-UDP | 2,778 | 0.07% |
| DoS GoldenEye | 26,861 | 0.71% |
| DoS Hulk | 1,803,246 | 47.98% |
| DoS Slowloris | 10,770 | 0.29% |
| FTP-BruteForce | 298,874 | 7.95% |
| Infiltration | 89,691 | 2.39% |
| SSH-BruteForce | 94,197 | 2.51% |
| Web Attack - Brute Force | 268 | 0.01% |
| Web Attack - SQL | 53 | 0.00% |
| Web Attack - XSS | 117 | 0.00% |
| **Total** | **3,757,659** | **100.00%** |
