# Data Assessment Report on dataset: Tuesday-20-02-2018.csv
## Command line executed  
 ```dataset_assessment_prepare.py --drop-columns id,Protocol,Attempted Category,Src Port --drop-highly-correlated --correlation-threshold 0.95 --drop-categorical-columns --impute-strategy mean --assess-only --zero-variance --low-variance-threshold=0.01 --low-variance-sample-percentage=100 --missing-threshold=0.05 --descriptive-statistics --distribution-analysis --distribution-column Label -output . -input CSECICIDS2018_improved/Tuesday-20-02-2018.csv```  
# Report  
 ### Options used to generate this report  

| # | Option | Value |
|---|---|---|
| 1 | -input | CSECICIDS2018_improved/Tuesday-20-02-2018.csv |
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
 
✅ Dataset Loaded Successfully: `.../DATASET_engelen_improved/CSECICIDS2018_improved/Tuesday-20-02-2018.csv
- File Size: 3272.29 MB
- Number of Records: 6,054,702
- File loaded in 05:44 minutes

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
 Found 12093887 negative values:

### Columns with Negative Values

| # | Column | Negative Count |
|---|---|---|
| 1 | Fwd Header Length | 1325 |
| 2 | Bwd Header Length | 1570 |
| 3 | ICMP Code | 6045496 |
| 4 | ICMP Type | 6045496 |

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
| 1 | Total Length of Bwd Packet | Total Bwd packets | 0.9965 |
| 2 | Fwd Packet Length Std | Fwd Packet Length Max | 0.9521 |
| 3 | Bwd Packet Length Std | Bwd Packet Length Max | 0.9702 |
| 4 | Fwd IAT Total | Flow Duration | 0.9590 |
| 5 | Bwd IAT Total | Flow Duration | 0.9795 |
| 6 | Packet Length Min | Fwd Packet Length Min | 0.9926 |
| 7 | ACK Flag Count | Total Bwd packets | 0.9885 |
| 8 | ACK Flag Count | Total Length of Bwd Packet | 0.9842 |
| 9 | URG Flag Count | Fwd URG Flags | 1.0000 |
| 10 | Average Packet Size | Packet Length Mean | 1.0000 |
| 11 | Fwd Segment Size Avg | Fwd Packet Length Mean | 1.0000 |
| 12 | Bwd Segment Size Avg | Bwd Packet Length Mean | 1.0000 |
| 13 | Fwd Bytes/Bulk Avg | Total Length of Fwd Packet | 0.9966 |
| 14 | Fwd Packet/Bulk Avg | Total Fwd Packet | 0.9988 |
| 15 | Bwd Packet/Bulk Avg | Bwd Bytes/Bulk Avg | 0.9998 |
| 16 | Subflow Fwd Bytes | Fwd Packet Length Mean | 0.9671 |
| 17 | Subflow Fwd Bytes | Fwd Segment Size Avg | 0.9671 |
| 18 | Subflow Bwd Bytes | Bwd Packet Length Mean | 0.9767 |
| 19 | Subflow Bwd Bytes | Bwd Segment Size Avg | 0.9767 |
| 20 | Fwd Act Data Pkts | Total Fwd Packet | 0.9989 |
| 21 | Fwd Act Data Pkts | Fwd Packet/Bulk Avg | 0.9999 |
| 22 | Active Min | Active Mean | 0.9734 |
| 23 | Idle Mean | Flow IAT Max | 0.9834 |
| 24 | Idle Max | Flow IAT Max | 0.9991 |
| 25 | Idle Max | Idle Mean | 0.9843 |
| 26 | Idle Min | Idle Mean | 0.9823 |

💡 To drop these features, use:
```python
df_numeric.drop(columns=['Total Length of Bwd Packet', 'Fwd Packet Length Std', 'Bwd Packet Length Std', 'Fwd IAT Total', 'Bwd IAT Total', 'Packet Length Min', 'ACK Flag Count', 'URG Flag Count', 'Average Packet Size', 'Fwd Segment Size Avg', 'Bwd Segment Size Avg', 'Fwd Bytes/Bulk Avg', 'Fwd Packet/Bulk Avg', 'Bwd Packet/Bulk Avg', 'Subflow Fwd Bytes', 'Subflow Bwd Bytes', 'Fwd Act Data Pkts', 'Active Min', 'Idle Mean', 'Idle Max', 'Idle Min'], inplace=True)
```
## Descriptive Statistics Analysis
 Descriptive Statistics for Features

| # | Column | Count | Mean | Std | Min | 25% | 50% | 75% | Max |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Dst Port | 6054702.0 | 840.2549945480389 | 1929.9795510392655 | 0.0 | 53.0 | 80.0 | 445.0 | 65535.0 |
| 2 | Flow Duration | 6054702.0 | 15848397.321712777 | 34290419.851983264 | 0.0 | 1257.0 | 168340.5 | 5125021.0 | 120000000.0 |
| 3 | Total Fwd Packet | 6054702.0 | 21.75889994255704 | 1425.7442965346302 | 0.0 | 1.0 | 4.0 | 9.0 | 280043.0 |
| 4 | Total Bwd packets | 6054702.0 | 9.23816613930793 | 181.4966802379373 | 0.0 | 1.0 | 3.0 | 7.0 | 25808.0 |
| 5 | Total Length of Fwd Packet | 6054702.0 | 1414.6064628779418 | 62376.474108012735 | 0.0 | 38.0 | 77.0 | 907.0 | 8961376.0 |
| 6 | Total Length of Bwd Packet | 6054702.0 | 6670.053383304414 | 262018.03465737906 | 0.0 | 78.0 | 204.0 | 1581.0 | 37583377.0 |
| 7 | Fwd Packet Length Max | 6054702.0 | 260.6749831783629 | 675.7604172032135 | 0.0 | 36.0 | 47.0 | 436.0 | 52560.0 |
| 8 | Fwd Packet Length Min | 6054702.0 | 17.30823069409527 | 23.86191911069365 | 0.0 | 0.0 | 0.0 | 38.0 | 3480.0 |
| 9 | Fwd Packet Length Mean | 6054702.0 | 62.616653025695236 | 122.40601925213664 | 0.0 | 32.124999999999986 | 42.0 | 75.83333333333333 | 9800.644144144148 |
| 10 | Fwd Packet Length Std | 6054702.0 | 79.03376328936902 | 193.20604725122655 | 0.0 | 0.0 | 8.94427190999916 | 136.63773763140708 | 12909.655137326708 |
| 11 | Bwd Packet Length Max | 6054702.0 | 517.8407863838715 | 554.7927975595346 | 0.0 | 71.0 | 146.0 | 1173.0 | 65160.0 |
| 12 | Bwd Packet Length Min | 6054702.0 | 42.866561558273226 | 58.73202013704647 | 0.0 | 0.0 | 0.0 | 79.0 | 1460.0 |
| 13 | Bwd Packet Length Mean | 6054702.0 | 157.45824936310066 | 163.94028248771954 | 0.0 | 59.0 | 113.0 | 225.8571428571429 | 30017.729411764707 |
| 14 | Bwd Packet Length Std | 6054702.0 | 184.76351420302652 | 229.40001245381305 | 0.0 | 0.0 | 0.0 | 430.0986044197418 | 22556.301629999754 |
| 15 | Flow Bytes/s | 6054694.0 | 91227.1874979946 | 332107.56669208634 | 0.0 | 195.52656556618365 | 1683.203994244785 | 111642.7432216906 | 276000000.0 |
| 16 | Flow Packets/s | 6054694.0 | 1585.838516077159 | 13567.940540129264 | 0.016666673333336 | 3.2511495410041342 | 34.608762362105175 | 1658.374792703151 | 5000000.0 |
| 17 | Flow IAT Mean | 6054702.0 | 891684.5875462135 | 2584084.4883147785 | 0.0 | 1201.0 | 38633.0 | 338830.87500000006 | 119999952.0 |
| 18 | Flow IAT Std | 6054702.0 | 2197833.634455894 | 5191641.191282385 | 0.0 | 0.0 | 46960.749527644366 | 755628.8070768313 | 84808080.04608749 |
| 19 | Flow IAT Max | 6054702.0 | 7456295.356803357 | 17752222.77283287 | 0.0 | 1215.0 | 115296.0 | 3010266.5 | 119999952.0 |
| 20 | Flow IAT Min | 6054702.0 | 46518.227499883564 | 1480341.8685139397 | 0.0 | 3.0 | 46.0 | 573.0 | 119999952.0 |
| 21 | Fwd IAT Total | 6054702.0 | 14674667.858240752 | 33254083.932964172 | 0.0 | 0.0 | 130471.0 | 4343443.75 | 119999998.0 |
| 22 | Fwd IAT Mean | 6054702.0 | 1581951.9962681734 | 4255420.245373715 | 0.0 | 0.0 | 56565.25 | 542283.675 | 119999952.0 |
| 23 | Fwd IAT Std | 6054702.0 | 2546051.179644331 | 6260672.07618496 | 0.0 | 0.0 | 20000.405371631372 | 660231.4521538427 | 84799007.86608487 |
| 24 | Fwd IAT Max | 6054702.0 | 6406345.23262879 | 15458651.154192472 | 0.0 | 0.0 | 96198.0 | 2005923.0 | 119999952.0 |
| 25 | Fwd IAT Min | 6054702.0 | 143194.29866820862 | 2667445.021263248 | 0.0 | 0.0 | 14.0 | 163.0 | 119999952.0 |
| 26 | Bwd IAT Total | 6054702.0 | 14445706.762489384 | 33973352.49735177 | 0.0 | 0.0 | 69957.0 | 2742310.0 | 120000000.0 |
| 27 | Bwd IAT Mean | 6054702.0 | 1790229.6719323308 | 6333908.114059404 | 0.0 | 0.0 | 28072.0 | 479738.3333333334 | 119996954.0 |
| 28 | Bwd IAT Std | 6054702.0 | 2141987.497406572 | 6059461.013031946 | 0.0 | 0.0 | 147.6672780272621 | 585862.9964724449 | 84837189.5109486 |
| 29 | Bwd IAT Max | 6054702.0 | 6314085.303511222 | 17019461.042136583 | 0.0 | 0.0 | 50069.0 | 1368825.5 | 119996954.0 |
| 30 | Bwd IAT Min | 6054702.0 | 590230.8175117454 | 5527732.284053793 | 0.0 | 0.0 | 1.0 | 15069.0 | 119996954.0 |
| 31 | Fwd PSH Flags | 6054702.0 | 2.1259850608667445 | 6.0618572947194505 | 0.0 | 0.0 | 1.0 | 4.0 | 1037.0 |
| 32 | Bwd PSH Flags | 6054702.0 | 2.1801773233430812 | 5.912763339557797 | 0.0 | 0.0 | 0.0 | 4.0 | 2805.0 |
| 33 | Fwd URG Flags | 6054702.0 | 3.3032178957775295e-07 | 0.0008127998395395401 | 0.0 | 0.0 | 0.0 | 0.0 | 2.0 |
| 34 | Bwd URG Flags | 6054702.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| 35 | Fwd RST Flags | 6054702.0 | 0.2691153090606276 | 0.44628988408250153 | 0.0 | 0.0 | 0.0 | 1.0 | 39.0 |
| 36 | Bwd RST Flags | 6054702.0 | 0.11868940866123552 | 0.34629743963294013 | 0.0 | 0.0 | 0.0 | 0.0 | 22.0 |
| 37 | Fwd Header Length | 6054702.0 | 123.99493418503504 | 505.01207997647214 | -32764.0 | 8.0 | 80.0 | 188.0 | 32752.0 |
| 38 | Bwd Header Length | 6054702.0 | 130.35701377210637 | 609.9228668646087 | -32752.0 | 8.0 | 72.0 | 152.0 | 32752.0 |
| 39 | Fwd Packets/s | 6054702.0 | 808.5052027172347 | 10589.3853079894 | 0.0 | 1.7778033781465918 | 17.91283257418526 | 829.1873963515754 | 5000000.0 |
| 40 | Bwd Packets/s | 6054702.0 | 777.3312180118563 | 6265.149955728755 | 0.0 | 1.4046829029760728 | 15.103097519466015 | 828.5004142502072 | 2000000.0 |
| 41 | Packet Length Min | 6054702.0 | 17.290794988754193 | 23.599316706747203 | 0.0 | 0.0 | 0.0 | 38.0 | 1460.0 |
| 42 | Packet Length Max | 6054702.0 | 553.8078159750885 | 810.9826338501268 | 0.0 | 71.0 | 147.0 | 1173.0 | 65160.0 |
| 43 | Packet Length Mean | 6054702.0 | 110.29300675117143 | 113.70692263223513 | 0.0 | 51.72972972972973 | 76.5 | 151.61111111111114 | 16582.948051948046 |
| 44 | Packet Length Std | 6054702.0 | 167.67921973074806 | 202.18662395721614 | 0.0 | 22.62741699796952 | 70.0035713374682 | 313.29443020902875 | 22430.72203716133 |
| 45 | Packet Length Variance | 6054702.0 | 68995.74488504577 | 582862.8862045128 | 0.0 | 512.0 | 4900.5 | 98153.4 | 503137291.10839486 |
| 46 | FIN Flag Count | 6054702.0 | 0.4835093452989098 | 0.8170746584530716 | 0.0 | 0.0 | 0.0 | 1.0 | 16.0 |
| 47 | SYN Flag Count | 6054702.0 | 1.0580922066849863 | 1.0600813406938712 | 0.0 | 0.0 | 2.0 | 2.0 | 202.0 |
| 48 | RST Flag Count | 6054702.0 | 0.38781627898449833 | 0.5309362945844798 | 0.0 | 0.0 | 0.0 | 1.0 | 40.0 |
| 49 | PSH Flag Count | 6054702.0 | 4.306162384209825 | 9.850213971450094 | 0.0 | 0.0 | 2.0 | 8.0 | 2805.0 |
| 50 | ACK Flag Count | 6054702.0 | 14.620284367422212 | 240.61678710901356 | 0.0 | 0.0 | 6.0 | 15.0 | 37683.0 |
| 51 | URG Flag Count | 6054702.0 | 3.3032178957775295e-07 | 0.0008127998395395401 | 0.0 | 0.0 | 0.0 | 0.0 | 2.0 |
| 52 | CWR Flag Count | 6054702.0 | 0.29618072037236515 | 0.5092603735054302 | 0.0 | 0.0 | 0.0 | 1.0 | 9.0 |
| 53 | ECE Flag Count | 6054702.0 | 0.37986295609594 | 0.6704449555344381 | 0.0 | 0.0 | 0.0 | 1.0 | 8.0 |
| 54 | Down/Up Ratio | 6054702.0 | 0.9380127760590581 | 0.3244123243014645 | 0.0 | 0.875 | 1.0 | 1.0 | 22.67765567765568 |
| 55 | Average Packet Size | 6054702.0 | 110.29300675117143 | 113.70692263223512 | 0.0 | 51.729729729729726 | 76.5 | 151.61111111111111 | 16582.948051948053 |
| 56 | Fwd Segment Size Avg | 6054702.0 | 62.616653025695236 | 122.40601925213664 | 0.0 | 32.125 | 42.0 | 75.83333333333333 | 9800.644144144144 |
| 57 | Bwd Segment Size Avg | 6054702.0 | 157.45824936310066 | 163.94028248771954 | 0.0 | 59.0 | 113.0 | 225.8571428571429 | 30017.729411764707 |
| 58 | Fwd Bytes/Bulk Avg | 6054702.0 | 818.9008778631879 | 62027.648483004894 | 0.0 | 0.0 | 0.0 | 0.0 | 8961376.0 |
| 59 | Fwd Packet/Bulk Avg | 6054702.0 | 14.773606198950832 | 1423.965485403737 | 0.0 | 0.0 | 0.0 | 0.0 | 280043.0 |
| 60 | Fwd Bulk Rate Avg | 6054702.0 | 17328.062560469534 | 3670921.3805819997 | 0.0 | 0.0 | 0.0 | 0.0 | 2742000000.0 |
| 61 | Bwd Bytes/Bulk Avg | 6054702.0 | 1813.0229983242775 | 132444.39973840961 | 0.0 | 0.0 | 0.0 | 0.0 | 31151926.0 |
| 62 | Bwd Packet/Bulk Avg | 6054702.0 | 1.361767598141081 | 91.93769761029354 | 0.0 | 0.0 | 0.0 | 0.0 | 21700.0 |
| 63 | Bwd Bulk Rate Avg | 6054702.0 | 18971467.719965737 | 184996014.74500954 | 0.0 | 0.0 | 0.0 | 0.0 | 5840000000.0 |
| 64 | Subflow Fwd Packets | 6054702.0 | 0.013362507353788841 | 0.11482139577832269 | 0.0 | 0.0 | 0.0 | 0.0 | 1.0 |
| 65 | Subflow Fwd Bytes | 6054702.0 | 31.64548643351894 | 48.12758790536204 | 0.0 | 16.0 | 21.0 | 40.0 | 4416.0 |
| 66 | Subflow Bwd Packets | 6054702.0 | 0.0007090357213286468 | 0.026618285194514046 | 0.0 | 0.0 | 0.0 | 0.0 | 1.0 |
| 67 | Subflow Bwd Bytes | 6054702.0 | 77.9998829009256 | 96.70432131508218 | 0.0 | 29.0 | 54.0 | 98.0 | 16568.0 |
| 68 | FWD Init Win Bytes | 6054702.0 | 4847.18979150419 | 7035.006036343733 | 0.0 | 0.0 | 8192.0 | 8192.0 | 65535.0 |
| 69 | Bwd Init Win Bytes | 6054702.0 | 11138.39417084441 | 23554.964180184437 | 0.0 | 0.0 | 0.0 | 253.0 | 65535.0 |
| 70 | Fwd Act Data Pkts | 6054702.0 | 17.45061111182681 | 1424.2198387478386 | 0.0 | 0.0 | 1.0 | 5.0 | 280042.0 |
| 71 | Fwd Seg Size Min | 6054702.0 | 15.089223548904636 | 6.459891151699439 | 0.0 | 8.0 | 20.0 | 20.0 | 48.0 |
| 72 | Active Mean | 6054702.0 | 207226.67697582906 | 1255018.4339932022 | 0.0 | 0.0 | 0.0 | 0.0 | 114868917.0 |
| 73 | Active Std | 6054702.0 | 45074.82379852147 | 422898.1484435032 | 0.0 | 0.0 | 0.0 | 0.0 | 74978322.80866358 |
| 74 | Active Max | 6054702.0 | 275196.0446887394 | 1469157.5575087527 | 0.0 | 0.0 | 0.0 | 0.0 | 114868917.0 |
| 75 | Active Min | 6054702.0 | 180516.83497486747 | 1216946.4935573426 | 0.0 | 0.0 | 0.0 | 0.0 | 114868917.0 |
| 76 | Idle Mean | 6054702.0 | 6666616.831112147 | 16907805.141406707 | 0.0 | 0.0 | 0.0 | 0.0 | 119999952.0 |
| 77 | Idle Std | 6054702.0 | 659456.9119912122 | 4359687.61764134 | 0.0 | 0.0 | 0.0 | 0.0 | 76393949.17038548 |
| 78 | Idle Max | 6054702.0 | 7151728.811567275 | 17859006.55720195 | 0.0 | 0.0 | 0.0 | 0.0 | 119999952.0 |
| 79 | Idle Min | 6054702.0 | 6126813.025632806 | 16528361.545476293 | 0.0 | 0.0 | 0.0 | 0.0 | 119999952.0 |
| 80 | ICMP Code | 6054702.0 | -0.9972845897287761 | 0.12449932128922707 | -1.0 | -1.0 | -1.0 | -1.0 | 13.0 |
| 81 | ICMP Type | 6054702.0 | -0.9862016330448633 | 0.36166495553888006 | -1.0 | -1.0 | -1.0 | -1.0 | 11.0 |
| 82 | Total TCP Flow Time | 6054702.0 | 171070973.53604603 | 1741590273.7111614 | 0.0 | 0.0 | 237381.0 | 7613220.0 | 43598225394.0 |

## Distribution Analysis
 Distribution of target variable 'Label':

Distribution Analysis

| # | Class | Percentage |
|---|---|---|
| 1 | BENIGN | 0.9521 |
| 2 | DDoS-LOIC-HTTP | 0.0478 |
| 3 | DDoS-LOIC-UDP | 0.0001 |
| 4 | DDoS-LOIC-UDP - Attempted | 0.0000 |

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
| 24 | Bwd IAT Max | bwd_iat_max |
| 25 | Bwd IAT Min | bwd_iat_min |
| 26 | Fwd PSH Flags | fwd_psh_flags |
| 27 | Bwd PSH Flags | bwd_psh_flags |
| 28 | Fwd URG Flags | fwd_urg_flags |
| 29 | Fwd RST Flags | fwd_rst_flags |
| 30 | Bwd RST Flags | bwd_rst_flags |
| 31 | Fwd Header Length | fwd_header_length |
| 32 | Bwd Header Length | bwd_header_length |
| 33 | Fwd Packets/s | fwd_packets/s |
| 34 | Bwd Packets/s | bwd_packets/s |
| 35 | Packet Length Max | packet_length_max |
| 36 | Packet Length Mean | packet_length_mean |
| 37 | Packet Length Std | packet_length_std |
| 38 | Packet Length Variance | packet_length_variance |
| 39 | FIN Flag Count | fin_flag_count |
| 40 | SYN Flag Count | syn_flag_count |
| 41 | RST Flag Count | rst_flag_count |
| 42 | PSH Flag Count | psh_flag_count |
| 43 | CWR Flag Count | cwr_flag_count |
| 44 | ECE Flag Count | ece_flag_count |
| 45 | Down/Up Ratio | down/up_ratio |
| 46 | Fwd Bulk Rate Avg | fwd_bulk_rate_avg |
| 47 | Bwd Bytes/Bulk Avg | bwd_bytes/bulk_avg |
| 48 | Bwd Bulk Rate Avg | bwd_bulk_rate_avg |
| 49 | Subflow Fwd Packets | subflow_fwd_packets |
| 50 | Subflow Bwd Packets | subflow_bwd_packets |
| 51 | FWD Init Win Bytes | fwd_init_win_bytes |
| 52 | Bwd Init Win Bytes | bwd_init_win_bytes |
| 53 | Fwd Seg Size Min | fwd_seg_size_min |
| 54 | Active Mean | active_mean |
| 55 | Active Std | active_std |
| 56 | Active Max | active_max |
| 57 | Idle Std | idle_std |
| 58 | ICMP Code | icmp_code |
| 59 | ICMP Type | icmp_type |
| 60 | Total TCP Flow Time | total_tcp_flow_time |

## Recommendation
 Based on the assessment, it is recommended to continue working with the available columns. You may consider the following:
- Performing further analysis using the available columns: `['Dst Port', 'Flow Duration', 'Total Fwd Packet', 'Total Bwd packets', 'Total Length of Fwd Packet', 'Fwd Packet Length Max', 'Fwd Packet Length Min', 'Fwd Packet Length Mean', 'Bwd Packet Length Max', 'Bwd Packet Length Min', 'Bwd Packet Length Mean', 'Flow Bytes/s', 'Flow Packets/s', 'Flow IAT Mean', 'Flow IAT Std', 'Flow IAT Max', 'Flow IAT Min', 'Fwd IAT Mean', 'Fwd IAT Std', 'Fwd IAT Max', 'Fwd IAT Min', 'Bwd IAT Mean', 'Bwd IAT Std', 'Bwd IAT Max', 'Bwd IAT Min', 'Fwd PSH Flags', 'Bwd PSH Flags', 'Fwd URG Flags', 'Fwd RST Flags', 'Bwd RST Flags', 'Fwd Header Length', 'Bwd Header Length', 'Fwd Packets/s', 'Bwd Packets/s', 'Packet Length Max', 'Packet Length Mean', 'Packet Length Std', 'Packet Length Variance', 'FIN Flag Count', 'SYN Flag Count', 'RST Flag Count', 'PSH Flag Count', 'CWR Flag Count', 'ECE Flag Count', 'Down/Up Ratio', 'Fwd Bulk Rate Avg', 'Bwd Bytes/Bulk Avg', 'Bwd Bulk Rate Avg', 'Subflow Fwd Packets', 'Subflow Bwd Packets', 'FWD Init Win Bytes', 'Bwd Init Win Bytes', 'Fwd Seg Size Min', 'Active Mean', 'Active Std', 'Active Max', 'Idle Std', 'ICMP Code', 'ICMP Type', 'Total TCP Flow Time']`
- Train machine learning models with the reduced feature set.
## End of Report ✅  
 
✅ Report Successfully Generated in  09:00 minutes

