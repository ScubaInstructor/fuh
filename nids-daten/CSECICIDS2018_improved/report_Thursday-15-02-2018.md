# Data Assessment Report on dataset: Thursday-15-02-2018.csv
## Command line executed  
 ```dataset_assessment_prepare.py --drop-columns id,Protocol,Attempted Category,Src Port --drop-highly-correlated --correlation-threshold 0.95 --drop-categorical-columns --impute-strategy mean --assess-only --zero-variance --low-variance-threshold=0.01 --low-variance-sample-percentage=100 --missing-threshold=0.05 --descriptive-statistics --distribution-analysis --distribution-column Label -output . -input CSECICIDS2018_improved/Thursday-15-02-2018.csv```  
# Report  
 ### Options used to generate this report  

| # | Option | Value |
|---|---|---|
| 1 | -input | CSECICIDS2018_improved/Thursday-15-02-2018.csv |
| 2 | -output | . |
| 3 | --drop-columns | id,Protocol,Attempted Category,Src Port |
| 4 | --drop-categorical-columns | True |
| 5 | --drop-highly-correlated | True |
| 6 | --impute-strategy | mean |
| 7 | --assess-only | True |
| 8 | --missing-threshold | 0.05 |
| 9 | --correlation-threshold | 0.95 |
| 10 | --zero-variance | True |
| 11 | --low-variance-threshold | 0.01 |
| 12 | --low-variance-sample-percentage | 100.0 |
| 13 | --distribution-analysis | True |
| 14 | --distribution-column | Label |
| 15 | --descriptive-statistics | True |
  
## Dataset Loaded  ✅  
 
✅ Dataset Loaded Successfully: `.../DATASET_engelen_improved/CSECICIDS2018_improved/Thursday-15-02-2018.csv
- File Size: 2853.90 MB
- Number of Records: 5,410,102
- File loaded in 10:56 minutes

## Assessment Mode  
 # 🔍 Running in assessment-only mode. No changes applied to the dataset.  
## Explicitly Defined Columns 🗑  
 ### Explicitly Defined Columns  

| # | Column |
|---|---|
| 1 | id |
| 2 | Protocol |
| 3 | Attempted Category |
| 4 | Src Port |

Python Command to drop columns these columns manually 💡  
 ```python
df.drop(columns=['id', 'Protocol', 'Attempted Category', 'Src Port'], inplace=True)
```
## Leading Spaces in Feature Names ✅  
 ### No issues found!  
## Identified Categorical Columns ⚠️  
 ## Categorical Columns

| # | Column |
|---|---|
| 1 | Flow ID |
| 2 | Src IP |
| 3 | Dst IP |
| 4 | Timestamp |
| 5 | Label |

💡 To drop them manually, use:
```python
df.drop(columns=['Flow ID', 'Src IP', 'Dst IP', 'Timestamp', 'Label'], inplace=True)
```  
## Zero Variance Columns ⚠️
 ### Identified Zero Variance Columns

| # | Column | Unique Value |
|---|---|---|
| 1 | Fwd URG Flags | 0 |
| 2 | Bwd URG Flags | 0 |
| 3 | URG Flag Count | 0 |

To drop these columns, use:
```python
df_numeric.drop(columns=['Fwd URG Flags', 'Bwd URG Flags', 'URG Flag Count'], inplace=True)
```
## Negative Values ⚠️  
 Found 10805714 negative values:

### Columns with Negative Values

| # | Column | Negative Count |
|---|---|---|
| 1 | Fwd Header Length | 740 |
| 2 | Bwd Header Length | 1536 |
| 3 | ICMP Code | 5401719 |
| 4 | ICMP Type | 5401719 |

💡 To replace with zero, use:
```python
df_numeric.loc[:, df_numeric.columns] = np.where(df_numeric < 0, 0, df_numeric)
```
## Infinite Values ⚠️ 
 Found 28 infinite values:

### Columns with Infinite Values

| # | Column | Infinite Count |
|---|---|---|
| 1 | Flow Bytes/s | 14 |
| 2 | Flow Packets/s | 14 |

💡 To replace with NaN, use:
```python
df_numeric.replace([np.inf, -np.inf], np.nan, inplace=True)
```
## Missing Values ✅  
 No columns to drop, max missing =  0.0% and that's below threshold 0.05%
## Impute Missing Values ✅  
 No issues found
## Highly Correlated Features ⚠️  
 ️Found 20 highly correlated features (threshold: 0.95):

### Highly Correlated Features

| # | Feature 1 | Feature 2 | Correlation |
|---|---|---|---|
| 1 | Total Length of Bwd Packet | Total Bwd packets | 0.9967 |
| 2 | Fwd Packet Length Std | Fwd Packet Length Max | 0.9603 |
| 3 | Bwd Packet Length Std | Bwd Packet Length Max | 0.9734 |
| 4 | Fwd IAT Total | Flow Duration | 0.9548 |
| 5 | Bwd IAT Total | Flow Duration | 0.9949 |
| 6 | Bwd IAT Max | Flow IAT Max | 0.9883 |
| 7 | Packet Length Min | Fwd Packet Length Min | 0.9969 |
| 8 | ACK Flag Count | Total Bwd packets | 0.9891 |
| 9 | ACK Flag Count | Total Length of Bwd Packet | 0.9845 |
| 10 | Average Packet Size | Packet Length Mean | 1.0000 |
| 11 | Fwd Segment Size Avg | Fwd Packet Length Mean | 1.0000 |
| 12 | Bwd Segment Size Avg | Bwd Packet Length Mean | 1.0000 |
| 13 | Fwd Bytes/Bulk Avg | Total Length of Fwd Packet | 0.9805 |
| 14 | Fwd Packet/Bulk Avg | Total Length of Fwd Packet | 0.9760 |
| 15 | Fwd Packet/Bulk Avg | Fwd Bytes/Bulk Avg | 0.9914 |
| 16 | Bwd Packet/Bulk Avg | Bwd Bytes/Bulk Avg | 0.9999 |
| 17 | Subflow Fwd Bytes | Fwd Packet Length Mean | 0.9705 |
| 18 | Subflow Fwd Bytes | Fwd Segment Size Avg | 0.9705 |
| 19 | Subflow Bwd Bytes | Bwd Packet Length Mean | 0.9782 |
| 20 | Subflow Bwd Bytes | Bwd Segment Size Avg | 0.9782 |
| 21 | Active Min | Active Mean | 0.9681 |
| 22 | Idle Mean | Flow IAT Max | 0.9813 |
| 23 | Idle Mean | Bwd IAT Max | 0.9687 |
| 24 | Idle Max | Flow IAT Max | 0.9993 |
| 25 | Idle Max | Bwd IAT Max | 0.9876 |
| 26 | Idle Max | Idle Mean | 0.9819 |
| 27 | Idle Min | Idle Mean | 0.9807 |

💡 To drop these features, use:
```python
df_numeric.drop(columns=['Total Length of Bwd Packet', 'Fwd Packet Length Std', 'Bwd Packet Length Std', 'Fwd IAT Total', 'Bwd IAT Total', 'Bwd IAT Max', 'Packet Length Min', 'ACK Flag Count', 'Average Packet Size', 'Fwd Segment Size Avg', 'Bwd Segment Size Avg', 'Fwd Bytes/Bulk Avg', 'Fwd Packet/Bulk Avg', 'Bwd Packet/Bulk Avg', 'Subflow Fwd Bytes', 'Subflow Bwd Bytes', 'Active Min', 'Idle Mean', 'Idle Max', 'Idle Min'], inplace=True)
```
## Descriptive Statistics Analysis
 Descriptive Statistics for Features

| # | Column | Count | Mean | Std | Min | 25% | 50% | 75% | Max |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Dst Port | 5410102.0 | 646.911044745552 | 1700.5375788897052 | 0.0 | 53.0 | 80.0 | 443.0 | 65533.0 |
| 2 | Flow Duration | 5410102.0 | 16794910.236348964 | 36463826.4001397 | 0.0 | 1123.0 | 69451.5 | 3388757.5 | 120000000.0 |
| 3 | Total Fwd Packet | 5410102.0 | 6.729341517036093 | 61.238313593720996 | 0.0 | 1.0 | 3.0 | 8.0 | 11160.0 |
| 4 | Total Bwd packets | 5410102.0 | 9.325575377321906 | 170.2475977156104 | 0.0 | 1.0 | 2.0 | 7.0 | 22715.0 |
| 5 | Total Length of Fwd Packet | 5410102.0 | 946.7530787774426 | 38408.64327097875 | 0.0 | 40.0 | 74.0 | 553.0 | 8737314.0 |
| 6 | Total Length of Bwd Packet | 5410102.0 | 6958.313529578555 | 244742.92717970363 | 0.0 | 69.0 | 163.0 | 1429.0 | 33078298.0 |
| 7 | Fwd Packet Length Max | 5410102.0 | 244.03880610753734 | 786.6941139890961 | 0.0 | 37.0 | 46.0 | 288.0 | 64440.0 |
| 8 | Fwd Packet Length Min | 5410102.0 | 19.864862252134987 | 24.386887176149006 | 0.0 | 0.0 | 0.0 | 40.0 | 3475.0 |
| 9 | Fwd Packet Length Mean | 5410102.0 | 62.09123078117443 | 139.85345627462252 | 0.0 | 32.2 | 42.0 | 61.07142857142856 | 16497.155642023346 |
| 10 | Fwd Packet Length Std | 5410102.0 | 73.17953730032605 | 223.36813916639022 | 0.0 | 0.0 | 0.0 | 89.83540504723068 | 18398.090305675927 |
| 11 | Bwd Packet Length Max | 5410102.0 | 441.823040674649 | 541.886571373699 | 0.0 | 66.0 | 131.0 | 1149.0 | 65160.0 |
| 12 | Bwd Packet Length Min | 5410102.0 | 49.08477363273373 | 60.16031732039144 | 0.0 | 0.0 | 0.0 | 94.0 | 1460.0 |
| 13 | Bwd Packet Length Mean | 5410102.0 | 148.07299359628317 | 170.97319451857538 | 0.0 | 56.66666666666666 | 99.0 | 182.0 | 31799.237499999985 |
| 14 | Bwd Packet Length Std | 5410102.0 | 149.44716392878755 | 220.5919358882539 | 0.0 | 0.0 | 0.0 | 352.61544853488 | 23907.88518631709 |
| 15 | Flow Bytes/s | 5410088.0 | 102336.74271308558 | 835037.216434082 | 0.0 | 302.7345947339283 | 4087.060622266489 | 132103.32103321032 | 716000000.0 |
| 16 | Flow Packets/s | 5410088.0 | 1854.5758975246058 | 16625.639345330193 | 0.0166667073612104 | 4.748177441770106 | 62.16585851050603 | 1895.7345971563984 | 4000000.0 |
| 17 | Flow IAT Mean | 5410102.0 | 876649.8890286558 | 2731902.7173365806 | 0.0 | 1052.0 | 23365.0 | 241793.55882352946 | 119999707.0 |
| 18 | Flow IAT Std | 5410102.0 | 2143125.2483870666 | 5474588.770449284 | 0.0 | 0.0 | 14867.962414984699 | 317524.393483349 | 84796566.22636944 |
| 19 | Flow IAT Max | 5410102.0 | 7441927.654843107 | 18733117.948547 | 0.0 | 1059.0 | 44552.0 | 1110334.25 | 119999707.0 |
| 20 | Flow IAT Min | 5410102.0 | 48585.17319710423 | 1462377.139842608 | 0.0 | 3.0 | 59.0 | 916.0 | 119999707.0 |
| 21 | Fwd IAT Total | 5410102.0 | 15346048.176428651 | 35296149.08778013 | 0.0 | 0.0 | 32433.5 | 2857047.75 | 119999994.0 |
| 22 | Fwd IAT Mean | 5410102.0 | 1536190.777146597 | 4932078.846055759 | 0.0 | 0.0 | 24185.0 | 393423.71978021984 | 119999707.0 |
| 23 | Fwd IAT Std | 5410102.0 | 2311750.228172736 | 6202059.7159324 | 0.0 | 0.0 | 32.526911934581186 | 406570.7967391206 | 84769556.16154167 |
| 24 | Fwd IAT Max | 5410102.0 | 6129927.481116622 | 15976157.562811261 | 0.0 | 0.0 | 28793.0 | 1253623.0 | 119999707.0 |
| 25 | Fwd IAT Min | 5410102.0 | 213146.14556028703 | 3674842.872781288 | 0.0 | 0.0 | 5.0 | 152.0 | 119999707.0 |
| 26 | Bwd IAT Total | 5410102.0 | 16426994.539209612 | 36251620.77475316 | 0.0 | 0.0 | 630.0 | 2765045.0 | 120000000.0 |
| 27 | Bwd IAT Mean | 5410102.0 | 2109467.368153551 | 7264175.639522403 | 0.0 | 0.0 | 164.25 | 406762.5773809524 | 119999915.0 |
| 28 | Bwd IAT Std | 5410102.0 | 2466448.0565580055 | 6719598.38628747 | 0.0 | 0.0 | 0.0 | 321940.4743955933 | 84825066.16518515 |
| 29 | Bwd IAT Max | 5410102.0 | 7287606.38613431 | 18667690.48168463 | 0.0 | 0.0 | 282.0 | 969032.0 | 119999915.0 |
| 30 | Bwd IAT Min | 5410102.0 | 729104.7649475001 | 6307895.574287945 | 0.0 | 0.0 | 0.0 | 233.0 | 119999915.0 |
| 31 | Fwd PSH Flags | 5410102.0 | 1.9589861706858762 | 5.512641817662246 | 0.0 | 0.0 | 0.0 | 3.0 | 779.0 |
| 32 | Bwd PSH Flags | 5410102.0 | 2.0082968860845876 | 6.151123623504853 | 0.0 | 0.0 | 0.0 | 3.0 | 2492.0 |
| 33 | Fwd URG Flags | 5410102.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| 34 | Bwd URG Flags | 5410102.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| 35 | Fwd RST Flags | 5410102.0 | 0.1720657022732658 | 0.38030380755578963 | 0.0 | 0.0 | 0.0 | 0.0 | 40.0 |
| 36 | Bwd RST Flags | 5410102.0 | 0.1270549058039941 | 0.35637582487175706 | 0.0 | 0.0 | 0.0 | 0.0 | 12.0 |
| 37 | Fwd Header Length | 5410102.0 | 117.62350950129961 | 455.1070112536602 | -32744.0 | 8.0 | 48.0 | 172.0 | 32680.0 |
| 38 | Bwd Header Length | 5410102.0 | 129.95799635570643 | 633.6001613852783 | -32744.0 | 8.0 | 20.0 | 152.0 | 32764.0 |
| 39 | Fwd Packets/s | 5410102.0 | 947.786284106835 | 11990.80046692264 | 0.0 | 2.3819151807486643 | 36.128472849452656 | 947.8672985781992 | 4000000.0 |
| 40 | Bwd Packets/s | 5410102.0 | 906.7848142360593 | 7693.120020163594 | 0.0 | 2.0868619283297942 | 28.15394577550044 | 947.8672985781992 | 3000000.0 |
| 41 | Packet Length Min | 5410102.0 | 19.841616294849892 | 24.152556798526827 | 0.0 | 0.0 | 0.0 | 40.0 | 1460.0 |
| 42 | Packet Length Max | 5410102.0 | 484.5977593398424 | 901.5249252948107 | 0.0 | 66.0 | 131.0 | 1149.0 | 65160.0 |
| 43 | Packet Length Mean | 5410102.0 | 106.729718488935 | 122.47640447721047 | 0.0 | 50.0 | 70.0 | 141.8571428571429 | 17805.636363636364 |
| 44 | Packet Length Std | 5410102.0 | 148.27606021009058 | 216.41672361843698 | 0.0 | 20.439341150503523 | 60.10407640085654 | 288.9071192085992 | 23841.38419170952 |
| 45 | Packet Length Variance | 5410102.0 | 68821.97963599066 | 757335.160068597 | 0.0 | 417.7666666666667 | 3612.5 | 83467.32352941175 | 568411600.1766965 |
| 46 | FIN Flag Count | 5410102.0 | 0.48965398434262425 | 0.8494586209924138 | 0.0 | 0.0 | 0.0 | 1.0 | 11.0 |
| 47 | SYN Flag Count | 5410102.0 | 0.9169730995829654 | 1.0549971949254318 | 0.0 | 0.0 | 0.0 | 2.0 | 33.0 |
| 48 | RST Flag Count | 5410102.0 | 0.29912837133200076 | 0.5082089502590826 | 0.0 | 0.0 | 0.0 | 1.0 | 41.0 |
| 49 | PSH Flag Count | 5410102.0 | 3.967283056770464 | 9.8058113167682 | 0.0 | 0.0 | 0.0 | 7.0 | 2492.0 |
| 50 | ACK Flag Count | 5410102.0 | 14.425200855732479 | 224.33796228408346 | 0.0 | 0.0 | 1.0 | 14.0 | 33875.0 |
| 51 | URG Flag Count | 5410102.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| 52 | CWR Flag Count | 5410102.0 | 0.23606394112347603 | 0.4938305194218171 | 0.0 | 0.0 | 0.0 | 0.0 | 14.0 |
| 53 | ECE Flag Count | 5410102.0 | 0.30272756410137924 | 0.6357888988048412 | 0.0 | 0.0 | 0.0 | 0.0 | 8.0 |
| 54 | Down/Up Ratio | 5410102.0 | 0.9605786754551314 | 0.34822122001307526 | 0.0 | 0.9 | 1.0 | 1.0 | 23.320388349514563 |
| 55 | Average Packet Size | 5410102.0 | 106.729718488935 | 122.47640447721044 | 0.0 | 50.0 | 70.0 | 141.85714285714286 | 17805.636363636364 |
| 56 | Fwd Segment Size Avg | 5410102.0 | 62.09123078117443 | 139.85345627462252 | 0.0 | 32.2 | 42.0 | 61.07142857142857 | 16497.155642023346 |
| 57 | Bwd Segment Size Avg | 5410102.0 | 148.07299359628317 | 170.97319451857538 | 0.0 | 56.66666666666666 | 99.0 | 182.0 | 31799.2375 |
| 58 | Fwd Bytes/Bulk Avg | 5410102.0 | 345.5095465852585 | 36452.61074939829 | 0.0 | 0.0 | 0.0 | 0.0 | 6383621.0 |
| 59 | Fwd Packet/Bulk Avg | 5410102.0 | 0.08043452785178543 | 4.466063132412687 | 0.0 | 0.0 | 0.0 | 0.0 | 789.0 |
| 60 | Fwd Bulk Rate Avg | 5410102.0 | 17303.027807793642 | 3599085.2881862377 | 0.0 | 0.0 | 0.0 | 0.0 | 2754500000.0 |
| 61 | Bwd Bytes/Bulk Avg | 5410102.0 | 2048.2368642957194 | 141032.1238934575 | 0.0 | 0.0 | 0.0 | 0.0 | 27659119.0 |
| 62 | Bwd Packet/Bulk Avg | 5410102.0 | 1.5433185917751644 | 98.64128698921532 | 0.0 | 0.0 | 0.0 | 0.0 | 19680.0 |
| 63 | Bwd Bulk Rate Avg | 5410102.0 | 23372625.378568094 | 205055214.03936654 | 0.0 | 0.0 | 0.0 | 0.0 | 5840000000.0 |
| 64 | Subflow Fwd Packets | 5410102.0 | 0.013911382816811957 | 0.117123263191122 | 0.0 | 0.0 | 0.0 | 0.0 | 1.0 |
| 65 | Subflow Fwd Bytes | 5410102.0 | 30.864723068067846 | 55.00952779361032 | 0.0 | 16.0 | 21.0 | 31.0 | 4043.0 |
| 66 | Subflow Bwd Packets | 5410102.0 | 0.000879096179702342 | 0.029636523614586893 | 0.0 | 0.0 | 0.0 | 0.0 | 1.0 |
| 67 | Subflow Bwd Bytes | 5410102.0 | 75.23017680627832 | 102.70426841456107 | 0.0 | 28.0 | 48.0 | 89.0 | 17789.0 |
| 68 | FWD Init Win Bytes | 5410102.0 | 4703.852018871363 | 8571.820422765224 | 0.0 | 0.0 | 254.0 | 8192.0 | 65535.0 |
| 69 | Bwd Init Win Bytes | 5410102.0 | 7429.09537805387 | 19692.311586909313 | 0.0 | 0.0 | 0.0 | 180.0 | 65535.0 |
| 70 | Fwd Act Data Pkts | 5410102.0 | 2.589827511570022 | 6.3882841826326455 | 0.0 | 0.0 | 1.0 | 4.0 | 1468.0 |
| 71 | Fwd Seg Size Min | 5410102.0 | 14.434274991488145 | 6.703343947855254 | 0.0 | 8.0 | 20.0 | 20.0 | 56.0 |
| 72 | Active Mean | 5410102.0 | 174554.11349479886 | 1313302.0943719596 | 0.0 | 0.0 | 0.0 | 0.0 | 113501625.0 |
| 73 | Active Std | 5410102.0 | 55308.65923880293 | 484259.3345328088 | 0.0 | 0.0 | 0.0 | 0.0 | 75968370.59016733 |
| 74 | Active Max | 5410102.0 | 255546.9273405566 | 1577944.240926443 | 0.0 | 0.0 | 0.0 | 0.0 | 113501625.0 |
| 75 | Active Min | 5410102.0 | 141088.79922615137 | 1259940.441672918 | 0.0 | 0.0 | 0.0 | 0.0 | 113501625.0 |
| 76 | Idle Mean | 5410102.0 | 6611818.361176543 | 17678361.119782194 | 0.0 | 0.0 | 0.0 | 0.0 | 119999707.0 |
| 77 | Idle Std | 5410102.0 | 793287.5936886369 | 4763013.313088951 | 0.0 | 0.0 | 0.0 | 0.0 | 75385356.09933154 |
| 78 | Idle Max | 5410102.0 | 7213641.374913634 | 18808243.504583072 | 0.0 | 0.0 | 0.0 | 0.0 | 119999707.0 |
| 79 | Idle Min | 5410102.0 | 5970411.660876819 | 17238352.22071047 | 0.0 | 0.0 | 0.0 | 0.0 | 119999707.0 |
| 80 | ICMP Code | 5410102.0 | -0.9970854523630054 | 0.13308389260619838 | -1.0 | -1.0 | -1.0 | -1.0 | 13.0 |
| 81 | ICMP Type | 5410102.0 | -0.9860128330297654 | 0.3634940874402924 | -1.0 | -1.0 | -1.0 | -1.0 | 11.0 |
| 82 | Total TCP Flow Time | 5410102.0 | 178365710.87142146 | 1709688338.5304942 | 0.0 | 0.0 | 1095.0 | 5858048.5 | 44281049305.0 |

## Distribution Analysis
 Distribution of target variable 'Label':

Distribution Analysis

| # | Class | Percentage |
|---|---|---|
| 1 | BENIGN | 0.9930 |
| 2 | DoS GoldenEye | 0.0042 |
| 3 | DoS GoldenEye - Attempted | 0.0008 |
| 4 | DoS Slowloris | 0.0016 |
| 5 | DoS Slowloris - Attempted | 0.0004 |

## Recommended Columns and Mapping  
 The following columns are available after cleaning.
Recommended mapping:
| # | Column Name | Mapping |
|---|---|---|
| 1 | Dst Port | dst_port |
| 2 | Flow Duration | flow_duration |
| 3 | Total Fwd Packet | total_fwd_packet |
| 4 | Total Bwd packets | total_bwd_packets |
| 5 | Total Length of Fwd Packet | total_length_of_fwd_packet |
| 6 | Fwd Packet Length Max | fwd_packet_length_max |
| 7 | Fwd Packet Length Min | fwd_packet_length_min |
| 8 | Fwd Packet Length Mean | fwd_packet_length_mean |
| 9 | Bwd Packet Length Max | bwd_packet_length_max |
| 10 | Bwd Packet Length Min | bwd_packet_length_min |
| 11 | Bwd Packet Length Mean | bwd_packet_length_mean |
| 12 | Flow Bytes/s | flow_bytes/s |
| 13 | Flow Packets/s | flow_packets/s |
| 14 | Flow IAT Mean | flow_iat_mean |
| 15 | Flow IAT Std | flow_iat_std |
| 16 | Flow IAT Max | flow_iat_max |
| 17 | Flow IAT Min | flow_iat_min |
| 18 | Fwd IAT Mean | fwd_iat_mean |
| 19 | Fwd IAT Std | fwd_iat_std |
| 20 | Fwd IAT Max | fwd_iat_max |
| 21 | Fwd IAT Min | fwd_iat_min |
| 22 | Bwd IAT Mean | bwd_iat_mean |
| 23 | Bwd IAT Std | bwd_iat_std |
| 24 | Bwd IAT Min | bwd_iat_min |
| 25 | Fwd PSH Flags | fwd_psh_flags |
| 26 | Bwd PSH Flags | bwd_psh_flags |
| 27 | Fwd RST Flags | fwd_rst_flags |
| 28 | Bwd RST Flags | bwd_rst_flags |
| 29 | Fwd Header Length | fwd_header_length |
| 30 | Bwd Header Length | bwd_header_length |
| 31 | Fwd Packets/s | fwd_packets/s |
| 32 | Bwd Packets/s | bwd_packets/s |
| 33 | Packet Length Max | packet_length_max |
| 34 | Packet Length Mean | packet_length_mean |
| 35 | Packet Length Std | packet_length_std |
| 36 | Packet Length Variance | packet_length_variance |
| 37 | FIN Flag Count | fin_flag_count |
| 38 | SYN Flag Count | syn_flag_count |
| 39 | RST Flag Count | rst_flag_count |
| 40 | PSH Flag Count | psh_flag_count |
| 41 | CWR Flag Count | cwr_flag_count |
| 42 | ECE Flag Count | ece_flag_count |
| 43 | Down/Up Ratio | down/up_ratio |
| 44 | Fwd Bulk Rate Avg | fwd_bulk_rate_avg |
| 45 | Bwd Bytes/Bulk Avg | bwd_bytes/bulk_avg |
| 46 | Bwd Bulk Rate Avg | bwd_bulk_rate_avg |
| 47 | Subflow Fwd Packets | subflow_fwd_packets |
| 48 | Subflow Bwd Packets | subflow_bwd_packets |
| 49 | FWD Init Win Bytes | fwd_init_win_bytes |
| 50 | Bwd Init Win Bytes | bwd_init_win_bytes |
| 51 | Fwd Act Data Pkts | fwd_act_data_pkts |
| 52 | Fwd Seg Size Min | fwd_seg_size_min |
| 53 | Active Mean | active_mean |
| 54 | Active Std | active_std |
| 55 | Active Max | active_max |
| 56 | Idle Std | idle_std |
| 57 | ICMP Code | icmp_code |
| 58 | ICMP Type | icmp_type |
| 59 | Total TCP Flow Time | total_tcp_flow_time |

## Recommendation
 Based on the assessment, it is recommended to continue working with the available columns. You may consider the following:
- Performing further analysis using the available columns: `['Dst Port', 'Flow Duration', 'Total Fwd Packet', 'Total Bwd packets', 'Total Length of Fwd Packet', 'Fwd Packet Length Max', 'Fwd Packet Length Min', 'Fwd Packet Length Mean', 'Bwd Packet Length Max', 'Bwd Packet Length Min', 'Bwd Packet Length Mean', 'Flow Bytes/s', 'Flow Packets/s', 'Flow IAT Mean', 'Flow IAT Std', 'Flow IAT Max', 'Flow IAT Min', 'Fwd IAT Mean', 'Fwd IAT Std', 'Fwd IAT Max', 'Fwd IAT Min', 'Bwd IAT Mean', 'Bwd IAT Std', 'Bwd IAT Min', 'Fwd PSH Flags', 'Bwd PSH Flags', 'Fwd RST Flags', 'Bwd RST Flags', 'Fwd Header Length', 'Bwd Header Length', 'Fwd Packets/s', 'Bwd Packets/s', 'Packet Length Max', 'Packet Length Mean', 'Packet Length Std', 'Packet Length Variance', 'FIN Flag Count', 'SYN Flag Count', 'RST Flag Count', 'PSH Flag Count', 'CWR Flag Count', 'ECE Flag Count', 'Down/Up Ratio', 'Fwd Bulk Rate Avg', 'Bwd Bytes/Bulk Avg', 'Bwd Bulk Rate Avg', 'Subflow Fwd Packets', 'Subflow Bwd Packets', 'FWD Init Win Bytes', 'Bwd Init Win Bytes', 'Fwd Act Data Pkts', 'Fwd Seg Size Min', 'Active Mean', 'Active Std', 'Active Max', 'Idle Std', 'ICMP Code', 'ICMP Type', 'Total TCP Flow Time']`
- Train machine learning models with the reduced feature set.
## End of Report ✅  
 
✅ Report Successfully Generated in  13:15 minutes

