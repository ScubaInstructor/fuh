# Data Assessment Report on dataset: Thursday-22-02-2018.csv
## Command line executed  
 ```dataset_assessment_prepare.py --drop-columns id,Protocol,Attempted Category,Src Port --drop-highly-correlated --correlation-threshold 0.95 --drop-categorical-columns --impute-strategy mean --assess-only --zero-variance --low-variance-threshold=0.01 --low-variance-sample-percentage=100 --missing-threshold=0.05 --descriptive-statistics --distribution-analysis --distribution-column Label -output . -input CSECICIDS2018_improved/Thursday-22-02-2018.csv```  
# Report  
 ### Options used to generate this report  

| # | Option | Value |
|---|---|---|
| 1 | -input | CSECICIDS2018_improved/Thursday-22-02-2018.csv |
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
 
✅ Dataset Loaded Successfully: `.../DATASET_engelen_improved/CSECICIDS2018_improved/Thursday-22-02-2018.csv
- File Size: 3312.90 MB
- Number of Records: 6,071,153
- File loaded in 04:06 minutes

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
| 1 | Bwd URG Flags | 0 |

To drop these columns, use:
```python
df_numeric.drop(columns=['Bwd URG Flags'], inplace=True)
```
## Negative Values ⚠️  
 Found 12127223 negative values:

### Columns with Negative Values

| # | Column | Negative Count |
|---|---|---|
| 1 | Fwd Header Length | 912 |
| 2 | Bwd Header Length | 1941 |
| 3 | ICMP Code | 6062185 |
| 4 | ICMP Type | 6062185 |

💡 To replace with zero, use:
```python
df_numeric.loc[:, df_numeric.columns] = np.where(df_numeric < 0, 0, df_numeric)
```
## Infinite Values ⚠️ 
 Found 4 infinite values:

### Columns with Infinite Values

| # | Column | Infinite Count |
|---|---|---|
| 1 | Flow Bytes/s | 2 |
| 2 | Flow Packets/s | 2 |

💡 To replace with NaN, use:
```python
df_numeric.replace([np.inf, -np.inf], np.nan, inplace=True)
```
## Missing Values ✅  
 No columns to drop, max missing =  0.0% and that's below threshold 0.05%
## Impute Missing Values ✅  
 No issues found
## Highly Correlated Features ⚠️  
 ️Found 22 highly correlated features (threshold: 0.95):

### Highly Correlated Features

| # | Feature 1 | Feature 2 | Correlation |
|---|---|---|---|
| 1 | Total Length of Bwd Packet | Total Bwd packets | 0.9942 |
| 2 | Fwd Packet Length Std | Fwd Packet Length Max | 0.9704 |
| 3 | Bwd Packet Length Std | Bwd Packet Length Max | 0.9722 |
| 4 | Flow IAT Max | Flow IAT Std | 0.9556 |
| 5 | Bwd IAT Total | Flow Duration | 0.9957 |
| 6 | Bwd IAT Std | Flow IAT Max | 0.9575 |
| 7 | Bwd IAT Max | Flow IAT Max | 0.9956 |
| 8 | Bwd IAT Max | Bwd IAT Std | 0.9618 |
| 9 | Packet Length Min | Fwd Packet Length Min | 0.9969 |
| 10 | ACK Flag Count | Total Bwd packets | 0.9857 |
| 11 | ACK Flag Count | Total Length of Bwd Packet | 0.9782 |
| 12 | URG Flag Count | Fwd URG Flags | 1.0000 |
| 13 | Average Packet Size | Packet Length Mean | 1.0000 |
| 14 | Fwd Segment Size Avg | Fwd Packet Length Mean | 1.0000 |
| 15 | Bwd Segment Size Avg | Bwd Packet Length Mean | 1.0000 |
| 16 | Fwd Bytes/Bulk Avg | Total Length of Fwd Packet | 0.9909 |
| 17 | Fwd Packet/Bulk Avg | Total Length of Fwd Packet | 0.9854 |
| 18 | Fwd Packet/Bulk Avg | Fwd Bytes/Bulk Avg | 0.9901 |
| 19 | Bwd Packet/Bulk Avg | Bwd Bytes/Bulk Avg | 0.9984 |
| 20 | Subflow Fwd Bytes | Fwd Packet Length Mean | 0.9741 |
| 21 | Subflow Fwd Bytes | Fwd Segment Size Avg | 0.9741 |
| 22 | Subflow Bwd Bytes | Bwd Packet Length Mean | 0.9769 |
| 23 | Subflow Bwd Bytes | Bwd Segment Size Avg | 0.9769 |
| 24 | Active Min | Active Mean | 0.9838 |
| 25 | Idle Mean | Flow IAT Max | 0.9933 |
| 26 | Idle Mean | Bwd IAT Max | 0.9896 |
| 27 | Idle Max | Flow IAT Std | 0.9555 |
| 28 | Idle Max | Flow IAT Max | 0.9997 |
| 29 | Idle Max | Bwd IAT Std | 0.9573 |
| 30 | Idle Max | Bwd IAT Max | 0.9953 |
| 31 | Idle Max | Idle Mean | 0.9936 |
| 32 | Idle Min | Flow IAT Max | 0.9745 |
| 33 | Idle Min | Bwd IAT Max | 0.9711 |
| 34 | Idle Min | Idle Mean | 0.9935 |
| 35 | Idle Min | Idle Max | 0.9746 |

💡 To drop these features, use:
```python
df_numeric.drop(columns=['Total Length of Bwd Packet', 'Fwd Packet Length Std', 'Bwd Packet Length Std', 'Flow IAT Max', 'Bwd IAT Total', 'Bwd IAT Std', 'Bwd IAT Max', 'Packet Length Min', 'ACK Flag Count', 'URG Flag Count', 'Average Packet Size', 'Fwd Segment Size Avg', 'Bwd Segment Size Avg', 'Fwd Bytes/Bulk Avg', 'Fwd Packet/Bulk Avg', 'Bwd Packet/Bulk Avg', 'Subflow Fwd Bytes', 'Subflow Bwd Bytes', 'Active Min', 'Idle Mean', 'Idle Max', 'Idle Min'], inplace=True)
```
## Descriptive Statistics Analysis
 Descriptive Statistics for Features

| # | Column | Count | Mean | Std | Min | 25% | 50% | 75% | Max |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Dst Port | 6071153.0 | 969.2642305341341 | 1861.2418764844972 | 0.0 | 53.0 | 80.0 | 445.0 | 65535.0 |
| 2 | Flow Duration | 6071153.0 | 22447619.508007128 | 39904651.786690466 | 0.0 | 1255.0 | 161699.0 | 11471765.0 | 120000000.0 |
| 3 | Total Fwd Packet | 6071153.0 | 7.611370031359776 | 73.8581176058378 | 0.0 | 1.0 | 4.0 | 10.0 | 20162.0 |
| 4 | Total Bwd packets | 6071153.0 | 10.116852268424136 | 210.8518166423154 | 0.0 | 1.0 | 3.0 | 9.0 | 106894.0 |
| 5 | Total Length of Fwd Packet | 6071153.0 | 1067.2595854527137 | 46317.38240986871 | 0.0 | 40.0 | 88.0 | 1044.0 | 10640993.0 |
| 6 | Total Length of Bwd Packet | 6071153.0 | 7507.111089771581 | 305929.46788840194 | 0.0 | 76.0 | 191.0 | 1581.0 | 155969316.0 |
| 7 | Fwd Packet Length Max | 6071153.0 | 292.672839080155 | 928.368502184152 | 0.0 | 39.0 | 54.0 | 517.0 | 51956.0 |
| 8 | Fwd Packet Length Min | 6071153.0 | 17.355124965554317 | 24.24249651861313 | 0.0 | 0.0 | 0.0 | 38.0 | 1400.0 |
| 9 | Fwd Packet Length Mean | 6071153.0 | 66.67996969014963 | 157.16275712465463 | 0.0 | 33.0 | 44.0 | 84.0 | 10227.618181818178 |
| 10 | Fwd Packet Length Std | 6071153.0 | 86.22377785863064 | 258.8982270923854 | 0.0 | 0.0 | 23.05609102457165 | 162.84012024653126 | 13192.013639971456 |
| 11 | Bwd Packet Length Max | 6071153.0 | 523.7011903669699 | 604.0684707033888 | 0.0 | 69.0 | 139.0 | 1173.0 | 65160.0 |
| 12 | Bwd Packet Length Min | 6071153.0 | 42.76478948891586 | 58.584075331528574 | 0.0 | 0.0 | 0.0 | 79.0 | 1264.0 |
| 13 | Bwd Packet Length Mean | 6071153.0 | 149.145142075551 | 168.37954066837077 | 0.0 | 56.0 | 102.0 | 204.1428571428571 | 38848.0868421053 |
| 14 | Bwd Packet Length Std | 6071153.0 | 174.67964736857525 | 229.9880371274921 | 0.0 | 0.0 | 0.0 | 402.5401488405491 | 23566.87702399865 |
| 15 | Flow Bytes/s | 6071151.0 | 90132.19833721037 | 290516.915840631 | 0.0 | 61.20619841191891 | 1641.8997792617572 | 111349.0364025696 | 474000000.0 |
| 16 | Flow Packets/s | 6071151.0 | 1545.8075801408595 | 9356.68917200331 | 0.0166670465364356 | 1.2756765609743388 | 34.62603878116344 | 1657.0008285004144 | 3000000.0 |
| 17 | Flow IAT Mean | 6071153.0 | 1107268.4821437444 | 2692789.0538632805 | 0.0 | 1202.0 | 38733.0 | 885048.1666666667 | 119997265.0 |
| 18 | Flow IAT Std | 6071153.0 | 3431632.634998033 | 6760178.9315983085 | 0.0 | 0.0 | 46331.42235171863 | 2270104.78398888 | 84845974.60559806 |
| 19 | Flow IAT Max | 6071153.0 | 13942775.747589296 | 28269318.11382808 | 0.0 | 1215.0 | 119111.0 | 9266272.0 | 119997265.0 |
| 20 | Flow IAT Min | 6071153.0 | 48030.68356060208 | 1518316.1426381487 | 0.0 | 4.0 | 44.0 | 581.0 | 119997265.0 |
| 21 | Fwd IAT Total | 6071153.0 | 13705566.68922806 | 33046041.485875104 | 0.0 | 0.0 | 127141.0 | 3955307.0 | 119999998.0 |
| 22 | Fwd IAT Mean | 6071153.0 | 1313191.0100389686 | 4061990.0565537065 | 0.0 | 0.0 | 55495.0 | 343964.25 | 119997265.0 |
| 23 | Fwd IAT Std | 6071153.0 | 2046165.648673872 | 5769091.7948809145 | 0.0 | 0.0 | 13915.615772696994 | 403027.2118496881 | 84789484.55195585 |
| 24 | Fwd IAT Max | 6071153.0 | 5415571.354745466 | 14760748.074063746 | 0.0 | 0.0 | 95962.0 | 1278979.0 | 119997265.0 |
| 25 | Fwd IAT Min | 6071153.0 | 141295.073869494 | 2662667.332102217 | 0.0 | 0.0 | 17.0 | 249.0 | 119997265.0 |
| 26 | Bwd IAT Total | 6071153.0 | 22117339.821751487 | 39777033.44375337 | 0.0 | 0.0 | 64710.0 | 10200845.0 | 120000000.0 |
| 27 | Bwd IAT Mean | 6071153.0 | 2627344.530279416 | 6719861.924867064 | 0.0 | 0.0 | 25817.0 | 1344182.1379310344 | 119997334.0 |
| 28 | Bwd IAT Std | 6071153.0 | 4593615.239857574 | 9606485.74282421 | 0.0 | 0.0 | 142.0501671945514 | 2028480.27699139 | 84822076.5177143 |
| 29 | Bwd IAT Max | 6071153.0 | 13794381.869414426 | 28228761.719489332 | 0.0 | 0.0 | 44654.0 | 6569200.0 | 119997334.0 |
| 30 | Bwd IAT Min | 6071153.0 | 596027.7942936046 | 5523544.71949355 | 0.0 | 0.0 | 1.0 | 26787.0 | 119997334.0 |
| 31 | Fwd PSH Flags | 6071153.0 | 2.4567200003030725 | 7.674806429703178 | 0.0 | 0.0 | 1.0 | 5.0 | 4907.0 |
| 32 | Bwd PSH Flags | 6071153.0 | 2.2994338966585097 | 7.342670773996908 | 0.0 | 0.0 | 0.0 | 5.0 | 5168.0 |
| 33 | Fwd URG Flags | 6071153.0 | 1.647133584016084e-07 | 0.00040584893544471653 | 0.0 | 0.0 | 0.0 | 0.0 | 1.0 |
| 34 | Bwd URG Flags | 6071153.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| 35 | Fwd RST Flags | 6071153.0 | 0.1749866952784751 | 0.3829068791318805 | 0.0 | 0.0 | 0.0 | 0.0 | 5.0 |
| 36 | Bwd RST Flags | 6071153.0 | 0.2148659406211637 | 0.4309055090586629 | 0.0 | 0.0 | 0.0 | 0.0 | 18.0 |
| 37 | Fwd Header Length | 6071153.0 | 134.06442301816475 | 461.9071276355896 | -32744.0 | 8.0 | 80.0 | 212.0 | 32744.0 |
| 38 | Bwd Header Length | 6071153.0 | 135.12993199150145 | 608.5734917386837 | -32768.0 | 8.0 | 72.0 | 192.0 | 32752.0 |
| 39 | Fwd Packets/s | 6071153.0 | 775.1917258081758 | 6044.089786062483 | 0.0 | 0.6819893987995524 | 18.10118562765861 | 828.5004142502072 | 3000000.0 |
| 40 | Bwd Packets/s | 6071153.0 | 770.615345102368 | 5536.941534067598 | 0.0 | 0.5211283679875013 | 15.556051044588829 | 829.1873963515754 | 2000000.0 |
| 41 | Packet Length Min | 6071153.0 | 17.337507060026326 | 24.00902253108738 | 0.0 | 0.0 | 0.0 | 38.0 | 1400.0 |
| 42 | Packet Length Max | 6071153.0 | 573.4250220674722 | 1052.5616493052755 | 0.0 | 69.0 | 145.0 | 1173.0 | 65160.0 |
| 43 | Packet Length Mean | 6071153.0 | 108.58360255717565 | 124.68290860754047 | 0.0 | 50.66666666666666 | 72.0 | 146.47058823529412 | 23926.74230145868 |
| 44 | Packet Length Std | 6071153.0 | 163.5814169988544 | 235.57701026424286 | 0.0 | 21.74396467988301 | 67.88225099390856 | 302.89700532249134 | 25608.002899649367 |
| 45 | Packet Length Variance | 6071153.0 | 82255.39861137286 | 1099823.237805887 | 0.0 | 472.8 | 4608.0 | 91746.59583333335 | 655769812.5084504 |
| 46 | FIN Flag Count | 6071153.0 | 0.5272303300542747 | 0.8201630842475549 | 0.0 | 0.0 | 0.0 | 1.0 | 15.0 |
| 47 | SYN Flag Count | 6071153.0 | 1.0499995635096002 | 1.2519654214132108 | 0.0 | 0.0 | 2.0 | 2.0 | 277.0 |
| 48 | RST Flag Count | 6071153.0 | 0.3898616951343509 | 0.536262796348779 | 0.0 | 0.0 | 0.0 | 1.0 | 18.0 |
| 49 | PSH Flag Count | 6071153.0 | 4.756153896961582 | 13.372061688561022 | 0.0 | 0.0 | 2.0 | 10.0 | 10075.0 |
| 50 | ACK Flag Count | 6071153.0 | 16.175273296522093 | 272.65283499889773 | 0.0 | 0.0 | 6.0 | 17.0 | 112599.0 |
| 51 | URG Flag Count | 6071153.0 | 1.647133584016084e-07 | 0.00040584893544471653 | 0.0 | 0.0 | 0.0 | 0.0 | 1.0 |
| 52 | CWR Flag Count | 6071153.0 | 0.31786878044417594 | 0.5007273873616072 | 0.0 | 0.0 | 0.0 | 1.0 | 9.0 |
| 53 | ECE Flag Count | 6071153.0 | 0.4583132726188913 | 0.7465580367017564 | 0.0 | 0.0 | 0.0 | 1.0 | 7.0 |
| 54 | Down/Up Ratio | 6071153.0 | 0.9354721164369114 | 0.34408055914396374 | 0.0 | 0.8461538461538461 | 1.0 | 1.0 | 24.748 |
| 55 | Average Packet Size | 6071153.0 | 108.58360255717565 | 124.68290860754047 | 0.0 | 50.66666666666666 | 72.0 | 146.47058823529412 | 23926.74230145867 |
| 56 | Fwd Segment Size Avg | 6071153.0 | 66.67996969014963 | 157.16275712465466 | 0.0 | 33.0 | 44.0 | 84.0 | 10227.61818181818 |
| 57 | Bwd Segment Size Avg | 6071153.0 | 149.14514207555104 | 168.37954066837074 | 0.0 | 56.0 | 102.0 | 204.1428571428572 | 38848.08684210527 |
| 58 | Fwd Bytes/Bulk Avg | 6071153.0 | 386.6581995215736 | 45636.782187561286 | 0.0 | 0.0 | 0.0 | 0.0 | 8423661.0 |
| 59 | Fwd Packet/Bulk Avg | 6071153.0 | 0.07640262072130286 | 5.605611058946268 | 0.0 | 0.0 | 0.0 | 0.0 | 1377.0 |
| 60 | Fwd Bulk Rate Avg | 6071153.0 | 13846.626495000208 | 3243851.039738421 | 0.0 | 0.0 | 0.0 | 0.0 | 3632500000.0 |
| 61 | Bwd Bytes/Bulk Avg | 6071153.0 | 1860.4929200433592 | 136420.08389929117 | 0.0 | 0.0 | 0.0 | 0.0 | 56069142.0 |
| 62 | Bwd Packet/Bulk Avg | 6071153.0 | 1.3903599530435158 | 94.42945975110887 | 0.0 | 0.0 | 0.0 | 0.0 | 38415.0 |
| 63 | Bwd Bulk Rate Avg | 6071153.0 | 20455908.83248174 | 193532658.1904162 | 0.0 | 0.0 | 0.0 | 0.0 | 5840000000.0 |
| 64 | Subflow Fwd Packets | 6071153.0 | 0.01313704332603708 | 0.11386159824149332 | 0.0 | 0.0 | 0.0 | 0.0 | 1.0 |
| 65 | Subflow Fwd Bytes | 6071153.0 | 33.809343628796704 | 63.40442717413646 | 0.0 | 16.0 | 22.0 | 41.0 | 4150.0 |
| 66 | Subflow Bwd Packets | 6071153.0 | 0.0007193032361398239 | 0.02681018383726509 | 0.0 | 0.0 | 0.0 | 0.0 | 1.0 |
| 67 | Subflow Bwd Bytes | 6071153.0 | 74.0942822557758 | 100.42347576087482 | 0.0 | 28.0 | 50.0 | 91.0 | 23925.0 |
| 68 | FWD Init Win Bytes | 6071153.0 | 4631.305270679227 | 5956.950902024948 | 0.0 | 0.0 | 8192.0 | 8192.0 | 65535.0 |
| 69 | Bwd Init Win Bytes | 6071153.0 | 8222.335758957153 | 20696.696314360215 | 0.0 | 0.0 | 0.0 | 176.0 | 65535.0 |
| 70 | Fwd Act Data Pkts | 6071153.0 | 3.010810467138614 | 8.520659372689448 | 0.0 | 0.0 | 1.0 | 5.0 | 5596.0 |
| 71 | Fwd Seg Size Min | 6071153.0 | 15.100332342143247 | 6.462768509761559 | 0.0 | 8.0 | 20.0 | 20.0 | 48.0 |
| 72 | Active Mean | 6071153.0 | 472179.76775495865 | 1593982.1101067746 | 0.0 | 0.0 | 0.0 | 30716.58333333333 | 112532817.0 |
| 73 | Active Std | 6071153.0 | 44289.41537846445 | 418937.04715891235 | 0.0 | 0.0 | 0.0 | 0.0 | 76076282.86315098 |
| 74 | Active Max | 6071153.0 | 538955.5850689317 | 1758541.3337852526 | 0.0 | 0.0 | 0.0 | 62320.0 | 112532817.0 |
| 75 | Active Min | 6071153.0 | 445723.6657063329 | 1568222.4903565736 | 0.0 | 0.0 | 0.0 | 11281.0 | 112532817.0 |
| 76 | Idle Mean | 6071153.0 | 13219451.394583236 | 27900508.696572643 | 0.0 | 0.0 | 0.0 | 8022828.0 | 119997265.0 |
| 77 | Idle Std | 6071153.0 | 659598.160444912 | 4358161.009057122 | 0.0 | 0.0 | 0.0 | 0.0 | 76978921.63989836 |
| 78 | Idle Max | 6071153.0 | 13703614.530744983 | 28376718.522965103 | 0.0 | 0.0 | 0.0 | 9266272.0 | 119997265.0 |
| 79 | Idle Min | 6071153.0 | 12676222.315955635 | 27798754.74795624 | 0.0 | 0.0 | 0.0 | 5474418.0 | 119997265.0 |
| 80 | ICMP Code | 6071153.0 | -0.996966638791676 | 0.1338465887942898 | -1.0 | -1.0 | -1.0 | -1.0 | 13.0 |
| 81 | ICMP Type | 6071153.0 | -0.9870991556299108 | 0.347200072881567 | -1.0 | -1.0 | -1.0 | -1.0 | 11.0 |
| 82 | Total TCP Flow Time | 6071153.0 | 182944343.57601562 | 1789914415.988278 | 0.0 | 0.0 | 225922.0 | 60014628.0 | 43969950325.0 |

## Distribution Analysis
 Distribution of target variable 'Label':

Distribution Analysis

| # | Class | Percentage |
|---|---|---|
| 1 | BENIGN | 1.0000 |
| 2 | Web Attack - Brute Force | 0.0000 |
| 3 | Web Attack - Brute Force - Attempted | 0.0000 |
| 4 | Web Attack - SQL | 0.0000 |
| 5 | Web Attack - SQL - Attempted | 0.0000 |
| 6 | Web Attack - XSS | 0.0000 |
| 7 | Web Attack - XSS - Attempted | 0.0000 |

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
| 16 | Flow IAT Min | flow_iat_min |
| 17 | Fwd IAT Total | fwd_iat_total |
| 18 | Fwd IAT Mean | fwd_iat_mean |
| 19 | Fwd IAT Std | fwd_iat_std |
| 20 | Fwd IAT Max | fwd_iat_max |
| 21 | Fwd IAT Min | fwd_iat_min |
| 22 | Bwd IAT Mean | bwd_iat_mean |
| 23 | Bwd IAT Min | bwd_iat_min |
| 24 | Fwd PSH Flags | fwd_psh_flags |
| 25 | Bwd PSH Flags | bwd_psh_flags |
| 26 | Fwd URG Flags | fwd_urg_flags |
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
- Performing further analysis using the available columns: `['Dst Port', 'Flow Duration', 'Total Fwd Packet', 'Total Bwd packets', 'Total Length of Fwd Packet', 'Fwd Packet Length Max', 'Fwd Packet Length Min', 'Fwd Packet Length Mean', 'Bwd Packet Length Max', 'Bwd Packet Length Min', 'Bwd Packet Length Mean', 'Flow Bytes/s', 'Flow Packets/s', 'Flow IAT Mean', 'Flow IAT Std', 'Flow IAT Min', 'Fwd IAT Total', 'Fwd IAT Mean', 'Fwd IAT Std', 'Fwd IAT Max', 'Fwd IAT Min', 'Bwd IAT Mean', 'Bwd IAT Min', 'Fwd PSH Flags', 'Bwd PSH Flags', 'Fwd URG Flags', 'Fwd RST Flags', 'Bwd RST Flags', 'Fwd Header Length', 'Bwd Header Length', 'Fwd Packets/s', 'Bwd Packets/s', 'Packet Length Max', 'Packet Length Mean', 'Packet Length Std', 'Packet Length Variance', 'FIN Flag Count', 'SYN Flag Count', 'RST Flag Count', 'PSH Flag Count', 'CWR Flag Count', 'ECE Flag Count', 'Down/Up Ratio', 'Fwd Bulk Rate Avg', 'Bwd Bytes/Bulk Avg', 'Bwd Bulk Rate Avg', 'Subflow Fwd Packets', 'Subflow Bwd Packets', 'FWD Init Win Bytes', 'Bwd Init Win Bytes', 'Fwd Act Data Pkts', 'Fwd Seg Size Min', 'Active Mean', 'Active Std', 'Active Max', 'Idle Std', 'ICMP Code', 'ICMP Type', 'Total TCP Flow Time']`
- Train machine learning models with the reduced feature set.
## End of Report ✅  
 
✅ Report Successfully Generated in  06:47 minutes

