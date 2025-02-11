# Data Assessment Report on dataset: Friday-16-02-2018.csv
## Command line executed  
 ```dataset_assessment_prepare.py --drop-columns id,Protocol,Attempted Category,Src Port --drop-highly-correlated --correlation-threshold 0.95 --drop-categorical-columns --impute-strategy mean --assess-only --zero-variance --low-variance-threshold=0.01 --low-variance-sample-percentage=100 --missing-threshold=0.05 --descriptive-statistics --distribution-analysis --distribution-column Label -output . -input CSECICIDS2018_improved/Friday-16-02-2018.csv```  
# Report  
 ### Options used to generate this report  

| # | Option | Value |
|---|---|---|
| 1 | -input | CSECICIDS2018_improved/Friday-16-02-2018.csv |
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
 
✅ Dataset Loaded Successfully: `.../DATASET_engelen_improved/CSECICIDS2018_improved/Friday-16-02-2018.csv
- File Size: 4016.63 MB
- Number of Records: 7,390,266
- File loaded in 08:28 minutes

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
 Found 14761399 negative values:

### Columns with Negative Values

| # | Column | Negative Count |
|---|---|---|
| 1 | Fwd Header Length | 784 |
| 2 | Bwd Header Length | 1295 |
| 3 | ICMP Code | 7379660 |
| 4 | ICMP Type | 7379660 |

💡 To replace with zero, use:
```python
df_numeric.loc[:, df_numeric.columns] = np.where(df_numeric < 0, 0, df_numeric)
```
## Infinite Values ⚠️ 
 Found 16 infinite values:

### Columns with Infinite Values

| # | Column | Infinite Count |
|---|---|---|
| 1 | Flow Bytes/s | 8 |
| 2 | Flow Packets/s | 8 |

💡 To replace with NaN, use:
```python
df_numeric.replace([np.inf, -np.inf], np.nan, inplace=True)
```
## Missing Values ✅  
 No columns to drop, max missing =  0.0% and that's below threshold 0.05%
## Impute Missing Values ✅  
 No issues found
## Highly Correlated Features ⚠️  
 ️Found 21 highly correlated features (threshold: 0.95):

### Highly Correlated Features

| # | Feature 1 | Feature 2 | Correlation |
|---|---|---|---|
| 1 | Total Length of Bwd Packet | Total Bwd packets | 0.9968 |
| 2 | Bwd Packet Length Std | Bwd Packet Length Max | 0.9730 |
| 3 | Fwd IAT Total | Flow Duration | 0.9655 |
| 4 | Bwd IAT Total | Flow Duration | 0.9956 |
| 5 | Bwd IAT Total | Fwd IAT Total | 0.9604 |
| 6 | Bwd IAT Max | Flow IAT Max | 0.9901 |
| 7 | Fwd Packets/s | Flow Packets/s | 0.9921 |
| 8 | Bwd Packets/s | Flow Packets/s | 0.9917 |
| 9 | Bwd Packets/s | Fwd Packets/s | 0.9679 |
| 10 | Packet Length Min | Fwd Packet Length Min | 0.9992 |
| 11 | ACK Flag Count | Total Bwd packets | 0.9874 |
| 12 | ACK Flag Count | Total Length of Bwd Packet | 0.9827 |
| 13 | Average Packet Size | Packet Length Mean | 1.0000 |
| 14 | Fwd Segment Size Avg | Fwd Packet Length Mean | 1.0000 |
| 15 | Bwd Segment Size Avg | Bwd Packet Length Mean | 1.0000 |
| 16 | Fwd Bytes/Bulk Avg | Total Length of Fwd Packet | 0.9963 |
| 17 | Fwd Packet/Bulk Avg | Total Length of Fwd Packet | 0.9899 |
| 18 | Fwd Packet/Bulk Avg | Fwd Bytes/Bulk Avg | 0.9930 |
| 19 | Bwd Packet/Bulk Avg | Bwd Bytes/Bulk Avg | 0.9998 |
| 20 | Subflow Fwd Bytes | Fwd Packet Length Mean | 0.9690 |
| 21 | Subflow Fwd Bytes | Fwd Segment Size Avg | 0.9690 |
| 22 | Subflow Bwd Bytes | Bwd Packet Length Mean | 0.9765 |
| 23 | Subflow Bwd Bytes | Bwd Segment Size Avg | 0.9765 |
| 24 | Active Min | Active Mean | 0.9715 |
| 25 | Idle Mean | Flow IAT Max | 0.9816 |
| 26 | Idle Mean | Bwd IAT Max | 0.9712 |
| 27 | Idle Max | Flow IAT Max | 0.9991 |
| 28 | Idle Max | Bwd IAT Max | 0.9893 |
| 29 | Idle Max | Idle Mean | 0.9825 |
| 30 | Idle Min | Idle Mean | 0.9796 |

💡 To drop these features, use:
```python
df_numeric.drop(columns=['Total Length of Bwd Packet', 'Bwd Packet Length Std', 'Fwd IAT Total', 'Bwd IAT Total', 'Bwd IAT Max', 'Fwd Packets/s', 'Bwd Packets/s', 'Packet Length Min', 'ACK Flag Count', 'Average Packet Size', 'Fwd Segment Size Avg', 'Bwd Segment Size Avg', 'Fwd Bytes/Bulk Avg', 'Fwd Packet/Bulk Avg', 'Bwd Packet/Bulk Avg', 'Subflow Fwd Bytes', 'Subflow Bwd Bytes', 'Active Min', 'Idle Mean', 'Idle Max', 'Idle Min'], inplace=True)
```
## Descriptive Statistics Analysis
 Descriptive Statistics for Features

| # | Column | Count | Mean | Std | Min | 25% | 50% | 75% | Max |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Dst Port | 7390266.0 | 665.2393651324594 | 1539.3456035936035 | 0.0 | 53.0 | 80.0 | 443.0 | 65492.0 |
| 2 | Flow Duration | 7390266.0 | 11340676.61048168 | 30663110.431502134 | 0.0 | 2404.0 | 132918.0 | 1740074.0 | 119999997.0 |
| 3 | Total Fwd Packet | 7390266.0 | 6.362427685282235 | 48.86728677692414 | 0.0 | 1.0 | 5.0 | 8.0 | 11596.0 |
| 4 | Total Bwd packets | 7390266.0 | 7.901918144759607 | 142.05705486911302 | 0.0 | 1.0 | 5.0 | 7.0 | 23934.0 |
| 5 | Total Length of Fwd Packet | 7390266.0 | 808.6119450910156 | 31986.984984981747 | 0.0 | 43.0 | 310.0 | 594.0 | 7437184.0 |
| 6 | Total Length of Bwd Packet | 7390266.0 | 4870.277494341882 | 204808.16800916073 | 0.0 | 99.0 | 706.0 | 935.0 | 34872099.0 |
| 7 | Fwd Packet Length Max | 7390266.0 | 288.2216261227945 | 630.8742903411917 | 0.0 | 41.0 | 194.0 | 375.0 | 51956.0 |
| 8 | Fwd Packet Length Min | 7390266.0 | 13.53065410636099 | 22.18139958264502 | 0.0 | 0.0 | 0.0 | 34.0 | 648.0 |
| 9 | Fwd Packet Length Mean | 7390266.0 | 67.69753214194495 | 113.44044817146082 | 0.0 | 36.0 | 52.0 | 74.8 | 10448.777777777776 |
| 10 | Fwd Packet Length Std | 7390266.0 | 99.97209569098919 | 182.20742850428718 | 0.0 | 0.0 | 72.00138887549322 | 163.23296235748464 | 12128.510576584584 |
| 11 | Bwd Packet Length Max | 7390266.0 | 599.4546243667007 | 519.2050968639451 | 0.0 | 92.0 | 488.0 | 935.0 | 46489.0 |
| 12 | Bwd Packet Length Min | 7390266.0 | 33.43597524094532 | 54.66356705091152 | 0.0 | 0.0 | 0.0 | 62.0 | 1317.0 |
| 13 | Bwd Packet Length Mean | 7390266.0 | 159.33687335203288 | 144.00560880101787 | 0.0 | 67.0 | 160.0 | 187.0 | 6302.431111111117 |
| 14 | Bwd Packet Length Std | 7390266.0 | 229.0457368637984 | 222.16756337630912 | 0.0 | 0.0 | 218.24023460397947 | 418.1447117924607 | 9550.32384305613 |
| 15 | Flow Bytes/s | 7390258.0 | 74238.48811390412 | 1181293.1874547198 | 0.0 | 872.5920098920092 | 6587.948139082479 | 35651.959980274376 | 716000000.0 |
| 16 | Flow Packets/s | 7390258.0 | 11731.000412498279 | 95741.36233930955 | 0.0166667837508225 | 8.53137134542764 | 66.23262221574615 | 857.2653236176596 | 5000000.0 |
| 17 | Flow IAT Mean | 7390266.0 | 583464.3508031587 | 2148178.502773983 | 0.0 | 2224.0 | 18007.333333333336 | 126350.92857142858 | 119999157.0 |
| 18 | Flow IAT Std | 7390266.0 | 1409381.5080741371 | 4386483.714701236 | 0.0 | 0.0 | 22116.16161882315 | 245515.74475583227 | 84807888.4201498 |
| 19 | Flow IAT Max | 7390266.0 | 4885727.718411353 | 15106545.235894 | 0.0 | 2383.0 | 59769.0 | 953143.0 | 119999157.0 |
| 20 | Flow IAT Min | 7390266.0 | 31896.449717371474 | 1129880.6689276248 | 0.0 | 4.0 | 8.0 | 344.0 | 119999157.0 |
| 21 | Fwd IAT Total | 7390266.0 | 10542110.192834873 | 29767036.98833198 | 0.0 | 0.0 | 127092.0 | 1729945.0 | 119999997.0 |
| 22 | Fwd IAT Mean | 7390266.0 | 1033017.2027246731 | 3669733.451320839 | 0.0 | 0.0 | 32648.291666666664 | 248512.10714285713 | 119999157.0 |
| 23 | Fwd IAT Std | 7390266.0 | 1591075.7631599884 | 5166110.679537087 | 0.0 | 0.0 | 24083.62394172357 | 387448.06991584203 | 84743935.56153893 |
| 24 | Fwd IAT Max | 7390266.0 | 4194774.548205031 | 13212748.623851398 | 0.0 | 0.0 | 66457.0 | 1121506.0 | 119999157.0 |
| 25 | Fwd IAT Min | 7390266.0 | 116591.79142266327 | 2410839.617040113 | 0.0 | 0.0 | 46.0 | 948.0 | 119999157.0 |
| 26 | Bwd IAT Total | 7390266.0 | 11098099.772481397 | 30466223.05884194 | 0.0 | 0.0 | 118797.0 | 1610268.0 | 119999994.0 |
| 27 | Bwd IAT Mean | 7390266.0 | 1383013.1765436542 | 5668212.879423339 | 0.0 | 0.0 | 30678.25 | 269149.6666666667 | 119998336.0 |
| 28 | Bwd IAT Std | 7390266.0 | 1617072.8693938886 | 5392084.082381601 | 0.0 | 0.0 | 22082.67634611219 | 284094.84025833884 | 84810472.89543504 |
| 29 | Bwd IAT Max | 7390266.0 | 4782650.442780679 | 15007748.411760181 | 0.0 | 0.0 | 59260.0 | 951721.0 | 119998336.0 |
| 30 | Bwd IAT Min | 7390266.0 | 465794.9777091921 | 4895891.86551024 | 0.0 | 0.0 | 22.0 | 226.0 | 119998336.0 |
| 31 | Fwd PSH Flags | 7390266.0 | 1.9046346910923098 | 4.819006796437671 | 0.0 | 0.0 | 1.0 | 3.0 | 905.0 |
| 32 | Bwd PSH Flags | 7390266.0 | 1.9199517311014245 | 4.979073223852286 | 0.0 | 0.0 | 1.0 | 2.0 | 1694.0 |
| 33 | Fwd URG Flags | 7390266.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| 34 | Bwd URG Flags | 7390266.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| 35 | Fwd RST Flags | 7390266.0 | 0.17792404224692318 | 0.38407851825443134 | 0.0 | 0.0 | 0.0 | 0.0 | 6.0 |
| 36 | Bwd RST Flags | 7390266.0 | 0.10069515765738338 | 0.31899523474276886 | 0.0 | 0.0 | 0.0 | 0.0 | 11.0 |
| 37 | Fwd Header Length | 7390266.0 | 134.6312481851127 | 370.7837162796317 | -32764.0 | 8.0 | 168.0 | 172.0 | 32752.0 |
| 38 | Bwd Header Length | 7390266.0 | 139.73165296080006 | 513.47895753653 | -32760.0 | 8.0 | 152.0 | 168.0 | 32740.0 |
| 39 | Fwd Packets/s | 7390266.0 | 5889.6001294135995 | 48840.99501323802 | 0.0 | 4.570216811085518 | 34.72198109735349 | 428.2655246252677 | 5000000.0 |
| 40 | Bwd Packets/s | 7390266.0 | 5841.38758421791 | 47677.71192212758 | 0.0 | 3.9714441816357016 | 32.00573542778866 | 427.8990158322636 | 2000000.0 |
| 41 | Packet Length Min | 7390266.0 | 13.518908926958787 | 22.030857569799206 | 0.0 | 0.0 | 0.0 | 34.0 | 624.0 |
| 42 | Packet Length Max | 7390266.0 | 627.9125241229476 | 761.5828962410748 | 0.0 | 93.0 | 538.0 | 935.0 | 51956.0 |
| 43 | Packet Length Mean | 7390266.0 | 113.95216461190495 | 102.53394968965681 | 0.0 | 57.0 | 112.0 | 141.0 | 4151.153061224492 |
| 44 | Packet Length Std | 7390266.0 | 192.94992835685272 | 190.68867607102288 | 0.0 | 36.37306695894642 | 157.036761442805 | 305.1376556390393 | 7647.599637949987 |
| 45 | Packet Length Variance | 7390266.0 | 73591.84111435516 | 527147.1799425884 | 0.0 | 1323.0 | 24660.54444444444 | 93108.98888888893 | 58485780.22237277 |
| 46 | FIN Flag Count | 7390266.0 | 0.8240313677477915 | 0.9836102982910049 | 0.0 | 0.0 | 0.0 | 2.0 | 18.0 |
| 47 | SYN Flag Count | 7390266.0 | 1.2607534018396631 | 1.0213807082899997 | 0.0 | 0.0 | 2.0 | 2.0 | 179.0 |
| 48 | RST Flag Count | 7390266.0 | 0.27862623618689775 | 0.4838412703073625 | 0.0 | 0.0 | 0.0 | 1.0 | 11.0 |
| 49 | PSH Flag Count | 7390266.0 | 3.8245864221937342 | 8.28304757288569 | 0.0 | 0.0 | 2.0 | 6.0 | 1696.0 |
| 50 | ACK Flag Count | 7390266.0 | 12.819271322574858 | 183.6908332514881 | 0.0 | 0.0 | 9.0 | 14.0 | 34698.0 |
| 51 | URG Flag Count | 7390266.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| 52 | CWR Flag Count | 7390266.0 | 0.22056932727455278 | 0.4713626577774918 | 0.0 | 0.0 | 0.0 | 0.0 | 9.0 |
| 53 | ECE Flag Count | 7390266.0 | 0.2989080501297247 | 0.6433262527845408 | 0.0 | 0.0 | 0.0 | 0.0 | 7.0 |
| 54 | Down/Up Ratio | 7390266.0 | 0.952780112590055 | 0.29417807992904693 | 0.0 | 0.875 | 1.0 | 1.0 | 22.81069958847737 |
| 55 | Average Packet Size | 7390266.0 | 113.95216461190495 | 102.53394968965681 | 0.0 | 57.0 | 112.0 | 141.0 | 4151.15306122449 |
| 56 | Fwd Segment Size Avg | 7390266.0 | 67.69753214194495 | 113.4404481714608 | 0.0 | 36.0 | 52.0 | 74.8 | 10448.777777777776 |
| 57 | Bwd Segment Size Avg | 7390266.0 | 159.33687335203288 | 144.00560880101784 | 0.0 | 67.0 | 160.0 | 187.0 | 6302.431111111111 |
| 58 | Fwd Bytes/Bulk Avg | 7390266.0 | 245.06361516622 | 31837.47576776535 | 0.0 | 0.0 | 0.0 | 0.0 | 7435909.0 |
| 59 | Fwd Packet/Bulk Avg | 7390266.0 | 0.05712690179216824 | 3.877435065357438 | 0.0 | 0.0 | 0.0 | 0.0 | 914.0 |
| 60 | Fwd Bulk Rate Avg | 7390266.0 | 14474.832026343842 | 3772829.61453693 | 0.0 | 0.0 | 0.0 | 0.0 | 2611500000.0 |
| 61 | Bwd Bytes/Bulk Avg | 7390266.0 | 1196.9013874466764 | 87570.03838362648 | 0.0 | 0.0 | 0.0 | 0.0 | 28557313.0 |
| 62 | Bwd Packet/Bulk Avg | 7390266.0 | 0.9122392888158559 | 61.49861581383846 | 0.0 | 0.0 | 0.0 | 0.0 | 20283.0 |
| 63 | Bwd Bulk Rate Avg | 7390266.0 | 15376870.681735408 | 167245192.58021688 | 0.0 | 0.0 | 0.0 | 0.0 | 5840000000.0 |
| 64 | Subflow Fwd Packets | 7390266.0 | 0.009817237972219133 | 0.09859442746005566 | 0.0 | 0.0 | 0.0 | 0.0 | 1.0 |
| 65 | Subflow Fwd Bytes | 7390266.0 | 34.12153162010677 | 45.34913307350013 | 0.0 | 18.0 | 26.0 | 37.0 | 4056.0 |
| 66 | Subflow Bwd Packets | 7390266.0 | 0.0006286647868967098 | 0.025065307747872606 | 0.0 | 0.0 | 0.0 | 0.0 | 1.0 |
| 67 | Subflow Bwd Bytes | 7390266.0 | 79.14067802160301 | 85.33553676751852 | 0.0 | 33.0 | 77.0 | 93.0 | 2737.0 |
| 68 | FWD Init Win Bytes | 7390266.0 | 10608.577433342723 | 11964.881371027332 | 0.0 | 0.0 | 8192.0 | 26883.0 | 65535.0 |
| 69 | Bwd Init Win Bytes | 7390266.0 | 9060.306278556143 | 21632.304809567097 | 0.0 | 0.0 | 149.0 | 237.0 | 65535.0 |
| 70 | Fwd Act Data Pkts | 7390266.0 | 2.3427725064294034 | 5.385814760482837 | 0.0 | 0.0 | 1.0 | 4.0 | 1669.0 |
| 71 | Fwd Seg Size Min | 7390266.0 | 19.373732420456854 | 9.582295041661222 | 0.0 | 8.0 | 20.0 | 32.0 | 48.0 |
| 72 | Active Mean | 7390266.0 | 118267.84163659764 | 1099192.038607622 | 0.0 | 0.0 | 0.0 | 0.0 | 114400278.0 |
| 73 | Active Std | 7390266.0 | 36959.335845041576 | 384837.0654127981 | 0.0 | 0.0 | 0.0 | 0.0 | 77080235.89950676 |
| 74 | Active Max | 7390266.0 | 173593.64462943553 | 1309211.6741717462 | 0.0 | 0.0 | 0.0 | 0.0 | 114400278.0 |
| 75 | Active Min | 7390266.0 | 96106.91743707196 | 1061532.9972884222 | 0.0 | 0.0 | 0.0 | 0.0 | 114400278.0 |
| 76 | Idle Mean | 7390266.0 | 4243207.904951959 | 14184298.55478086 | 0.0 | 0.0 | 0.0 | 0.0 | 119999157.0 |
| 77 | Idle Std | 7390266.0 | 529210.042896658 | 3942941.309581763 | 0.0 | 0.0 | 0.0 | 0.0 | 69952499.84309022 |
| 78 | Idle Max | 7390266.0 | 4633025.559326552 | 15170635.383823391 | 0.0 | 0.0 | 0.0 | 0.0 | 119999157.0 |
| 79 | Idle Min | 7390266.0 | 3817457.565720503 | 13740384.057912854 | 0.0 | 0.0 | 0.0 | 0.0 | 119999157.0 |
| 80 | ICMP Code | 7390266.0 | -0.9976405450087994 | 0.11154503630903564 | -1.0 | -1.0 | -1.0 | -1.0 | 13.0 |
| 81 | ICMP Type | 7390266.0 | -0.9870445799921139 | 0.3475535192094405 | -1.0 | -1.0 | -1.0 | -1.0 | 11.0 |
| 82 | Total TCP Flow Time | 7390266.0 | 121885034.7690983 | 1419351089.9433062 | 0.0 | 0.0 | 134690.0 | 1908793.0 | 34553082568.0 |

## Distribution Analysis
 Distribution of target variable 'Label':

Distribution Analysis

| # | Class | Percentage |
|---|---|---|
| 1 | BENIGN | 0.7417 |
| 2 | DoS Hulk | 0.2440 |
| 3 | DoS Hulk - Attempted | 0.0000 |
| 4 | FTP-BruteForce - Attempted | 0.0143 |

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
| 9 | Fwd Packet Length Std | fwd_packet_length_std |
| 10 | Bwd Packet Length Max | bwd_packet_length_max |
| 11 | Bwd Packet Length Min | bwd_packet_length_min |
| 12 | Bwd Packet Length Mean | bwd_packet_length_mean |
| 13 | Flow Bytes/s | flow_bytes/s |
| 14 | Flow Packets/s | flow_packets/s |
| 15 | Flow IAT Mean | flow_iat_mean |
| 16 | Flow IAT Std | flow_iat_std |
| 17 | Flow IAT Max | flow_iat_max |
| 18 | Flow IAT Min | flow_iat_min |
| 19 | Fwd IAT Mean | fwd_iat_mean |
| 20 | Fwd IAT Std | fwd_iat_std |
| 21 | Fwd IAT Max | fwd_iat_max |
| 22 | Fwd IAT Min | fwd_iat_min |
| 23 | Bwd IAT Mean | bwd_iat_mean |
| 24 | Bwd IAT Std | bwd_iat_std |
| 25 | Bwd IAT Min | bwd_iat_min |
| 26 | Fwd PSH Flags | fwd_psh_flags |
| 27 | Bwd PSH Flags | bwd_psh_flags |
| 28 | Fwd RST Flags | fwd_rst_flags |
| 29 | Bwd RST Flags | bwd_rst_flags |
| 30 | Fwd Header Length | fwd_header_length |
| 31 | Bwd Header Length | bwd_header_length |
| 32 | Packet Length Max | packet_length_max |
| 33 | Packet Length Mean | packet_length_mean |
| 34 | Packet Length Std | packet_length_std |
| 35 | Packet Length Variance | packet_length_variance |
| 36 | FIN Flag Count | fin_flag_count |
| 37 | SYN Flag Count | syn_flag_count |
| 38 | RST Flag Count | rst_flag_count |
| 39 | PSH Flag Count | psh_flag_count |
| 40 | CWR Flag Count | cwr_flag_count |
| 41 | ECE Flag Count | ece_flag_count |
| 42 | Down/Up Ratio | down/up_ratio |
| 43 | Fwd Bulk Rate Avg | fwd_bulk_rate_avg |
| 44 | Bwd Bytes/Bulk Avg | bwd_bytes/bulk_avg |
| 45 | Bwd Bulk Rate Avg | bwd_bulk_rate_avg |
| 46 | Subflow Fwd Packets | subflow_fwd_packets |
| 47 | Subflow Bwd Packets | subflow_bwd_packets |
| 48 | FWD Init Win Bytes | fwd_init_win_bytes |
| 49 | Bwd Init Win Bytes | bwd_init_win_bytes |
| 50 | Fwd Act Data Pkts | fwd_act_data_pkts |
| 51 | Fwd Seg Size Min | fwd_seg_size_min |
| 52 | Active Mean | active_mean |
| 53 | Active Std | active_std |
| 54 | Active Max | active_max |
| 55 | Idle Std | idle_std |
| 56 | ICMP Code | icmp_code |
| 57 | ICMP Type | icmp_type |
| 58 | Total TCP Flow Time | total_tcp_flow_time |

## Recommendation
 Based on the assessment, it is recommended to continue working with the available columns. You may consider the following:
- Performing further analysis using the available columns: `['Dst Port', 'Flow Duration', 'Total Fwd Packet', 'Total Bwd packets', 'Total Length of Fwd Packet', 'Fwd Packet Length Max', 'Fwd Packet Length Min', 'Fwd Packet Length Mean', 'Fwd Packet Length Std', 'Bwd Packet Length Max', 'Bwd Packet Length Min', 'Bwd Packet Length Mean', 'Flow Bytes/s', 'Flow Packets/s', 'Flow IAT Mean', 'Flow IAT Std', 'Flow IAT Max', 'Flow IAT Min', 'Fwd IAT Mean', 'Fwd IAT Std', 'Fwd IAT Max', 'Fwd IAT Min', 'Bwd IAT Mean', 'Bwd IAT Std', 'Bwd IAT Min', 'Fwd PSH Flags', 'Bwd PSH Flags', 'Fwd RST Flags', 'Bwd RST Flags', 'Fwd Header Length', 'Bwd Header Length', 'Packet Length Max', 'Packet Length Mean', 'Packet Length Std', 'Packet Length Variance', 'FIN Flag Count', 'SYN Flag Count', 'RST Flag Count', 'PSH Flag Count', 'CWR Flag Count', 'ECE Flag Count', 'Down/Up Ratio', 'Fwd Bulk Rate Avg', 'Bwd Bytes/Bulk Avg', 'Bwd Bulk Rate Avg', 'Subflow Fwd Packets', 'Subflow Bwd Packets', 'FWD Init Win Bytes', 'Bwd Init Win Bytes', 'Fwd Act Data Pkts', 'Fwd Seg Size Min', 'Active Mean', 'Active Std', 'Active Max', 'Idle Std', 'ICMP Code', 'ICMP Type', 'Total TCP Flow Time']`
- Train machine learning models with the reduced feature set.
## End of Report ✅  
 
✅ Report Successfully Generated in  13:15 minutes

