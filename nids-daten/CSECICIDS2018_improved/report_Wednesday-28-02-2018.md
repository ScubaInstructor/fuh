# Data Assessment Report on dataset: Wednesday-28-02-2018.csv
## Command line executed  
 ```dataset_assessment_prepare.py --drop-columns id,Protocol,Attempted Category,Src Port --drop-highly-correlated --correlation-threshold 0.95 --drop-categorical-columns --impute-strategy mean --assess-only --zero-variance --low-variance-threshold=0.01 --low-variance-sample-percentage=100 --missing-threshold=0.05 --descriptive-statistics --distribution-analysis --distribution-column Label -output . -input CSECICIDS2018_improved/Wednesday-28-02-2018.csv```  
# Report  
 ### Options used to generate this report  

| # | Option | Value |
|---|---|---|
| 1 | -input | CSECICIDS2018_improved/Wednesday-28-02-2018.csv |
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
 
✅ Dataset Loaded Successfully: `.../DATASET_engelen_improved/CSECICIDS2018_improved/Wednesday-28-02-2018.csv
- File Size: 3635.62 MB
- Number of Records: 6,568,726
- File loaded in 04:05 minutes

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
 Found 13112560 negative values:

### Columns with Negative Values

| # | Column | Negative Count |
|---|---|---|
| 1 | Fwd Header Length | 834 |
| 2 | Bwd Header Length | 1534 |
| 3 | ICMP Code | 6555096 |
| 4 | ICMP Type | 6555096 |

💡 To replace with zero, use:
```python
df_numeric.loc[:, df_numeric.columns] = np.where(df_numeric < 0, 0, df_numeric)
```
## Infinite Values ⚠️ 
 Found 8 infinite values:

### Columns with Infinite Values

| # | Column | Infinite Count |
|---|---|---|
| 1 | Flow Bytes/s | 4 |
| 2 | Flow Packets/s | 4 |

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
| 1 | Total Length of Bwd Packet | Total Bwd packets | 0.9958 |
| 2 | Fwd Packet Length Std | Fwd Packet Length Max | 0.9649 |
| 3 | Bwd Packet Length Std | Bwd Packet Length Max | 0.9726 |
| 4 | Bwd IAT Total | Flow Duration | 0.9951 |
| 5 | Bwd IAT Max | Flow IAT Max | 0.9946 |
| 6 | Bwd IAT Max | Bwd IAT Std | 0.9545 |
| 7 | Fwd Packets/s | Flow Packets/s | 0.9913 |
| 8 | Bwd Packets/s | Flow Packets/s | 0.9909 |
| 9 | Bwd Packets/s | Fwd Packets/s | 0.9646 |
| 10 | Packet Length Min | Fwd Packet Length Min | 0.9947 |
| 11 | ACK Flag Count | Total Bwd packets | 0.9637 |
| 12 | ACK Flag Count | Total Length of Bwd Packet | 0.9676 |
| 13 | URG Flag Count | Fwd URG Flags | 1.0000 |
| 14 | Average Packet Size | Packet Length Mean | 1.0000 |
| 15 | Fwd Segment Size Avg | Fwd Packet Length Mean | 1.0000 |
| 16 | Bwd Segment Size Avg | Bwd Packet Length Mean | 1.0000 |
| 17 | Fwd Packet/Bulk Avg | Fwd Bytes/Bulk Avg | 0.9831 |
| 18 | Bwd Packet/Bulk Avg | Bwd Bytes/Bulk Avg | 1.0000 |
| 19 | Subflow Fwd Bytes | Fwd Packet Length Mean | 0.9762 |
| 20 | Subflow Fwd Bytes | Fwd Segment Size Avg | 0.9762 |
| 21 | Subflow Bwd Bytes | Bwd Packet Length Mean | 0.9754 |
| 22 | Subflow Bwd Bytes | Bwd Segment Size Avg | 0.9754 |
| 23 | Active Min | Active Mean | 0.9708 |
| 24 | Idle Mean | Flow IAT Max | 0.9920 |
| 25 | Idle Mean | Bwd IAT Max | 0.9872 |
| 26 | Idle Max | Flow IAT Max | 0.9996 |
| 27 | Idle Max | Bwd IAT Max | 0.9942 |
| 28 | Idle Max | Idle Mean | 0.9923 |
| 29 | Idle Min | Flow IAT Max | 0.9696 |
| 30 | Idle Min | Bwd IAT Max | 0.9653 |
| 31 | Idle Min | Idle Mean | 0.9923 |
| 32 | Idle Min | Idle Max | 0.9698 |

💡 To drop these features, use:
```python
df_numeric.drop(columns=['Total Length of Bwd Packet', 'Fwd Packet Length Std', 'Bwd Packet Length Std', 'Bwd IAT Total', 'Bwd IAT Max', 'Fwd Packets/s', 'Bwd Packets/s', 'Packet Length Min', 'ACK Flag Count', 'URG Flag Count', 'Average Packet Size', 'Fwd Segment Size Avg', 'Bwd Segment Size Avg', 'Fwd Packet/Bulk Avg', 'Bwd Packet/Bulk Avg', 'Subflow Fwd Bytes', 'Subflow Bwd Bytes', 'Active Min', 'Idle Mean', 'Idle Max', 'Idle Min'], inplace=True)
```
## Descriptive Statistics Analysis
 Descriptive Statistics for Features

| # | Column | Count | Mean | Std | Min | 25% | 50% | 75% | Max |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Dst Port | 6568726.0 | 1085.7113594021123 | 2189.6326461454323 | 0.0 | 53.0 | 443.0 | 3389.0 | 65389.0 |
| 2 | Flow Duration | 6568726.0 | 20760816.826553125 | 38716754.789046675 | 0.0 | 1336.0 | 241737.5 | 8095811.25 | 119999998.0 |
| 3 | Total Fwd Packet | 6568726.0 | 7.6610740043046395 | 73.96134064411109 | 0.0 | 1.0 | 5.0 | 9.0 | 53218.0 |
| 4 | Total Bwd packets | 6568726.0 | 10.072119159788366 | 218.88997401005295 | 0.0 | 1.0 | 4.0 | 8.0 | 142798.0 |
| 5 | Total Length of Fwd Packet | 6568726.0 | 1163.8889848655583 | 48940.63601493504 | 0.0 | 41.0 | 97.0 | 1128.0 | 41765677.0 |
| 6 | Total Length of Bwd Packet | 6568726.0 | 7217.674550894649 | 311195.6280362454 | 0.0 | 77.0 | 223.0 | 1581.0 | 208410910.0 |
| 7 | Fwd Packet Length Max | 6568726.0 | 317.6706340011747 | 881.9543649546989 | 0.0 | 39.0 | 74.0 | 628.0 | 64800.0 |
| 8 | Fwd Packet Length Min | 6568726.0 | 16.438657511365218 | 23.84781308630582 | 0.0 | 0.0 | 0.0 | 37.0 | 1484.0 |
| 9 | Fwd Packet Length Mean | 6568726.0 | 71.40598101044372 | 158.8354535059943 | 0.0 | 34.0 | 45.0 | 98.92857142857142 | 10491.46 |
| 10 | Fwd Packet Length Std | 6568726.0 | 95.1898385952148 | 251.07638361611305 | 0.0 | 0.0 | 23.11493023999856 | 188.78178964763552 | 10612.99711514188 |
| 11 | Bwd Packet Length Max | 6568726.0 | 558.8813037718426 | 601.0892246018075 | 0.0 | 70.0 | 152.0 | 1173.0 | 64240.0 |
| 12 | Bwd Packet Length Min | 6568726.0 | 40.28731827145781 | 57.83630741099048 | 0.0 | 0.0 | 0.0 | 72.0 | 1460.0 |
| 13 | Bwd Packet Length Mean | 6568726.0 | 154.62785331901577 | 167.44196143911537 | 0.0 | 58.0 | 113.0 | 206.9090909090909 | 7095.428571428572 |
| 14 | Bwd Packet Length Std | 6568726.0 | 188.07232422242305 | 229.35122885931912 | 0.0 | 0.0 | 15.500000000000002 | 420.4990798925441 | 13789.657765358585 |
| 15 | Flow Bytes/s | 6568722.0 | 84728.73261004074 | 249637.48435970795 | 0.0 | 88.88514063001455 | 1620.6595008998383 | 95604.83933883604 | 83000000.0 |
| 16 | Flow Packets/s | 6568722.0 | 4674.731927326675 | 60814.69896694638 | 0.0166670213964387 | 1.9620352715087055 | 25.314853490285422 | 1539.6458814472671 | 5000000.0 |
| 17 | Flow IAT Mean | 6568726.0 | 1032384.3954409832 | 2709151.565797905 | 0.0 | 1294.0 | 49745.35416666667 | 596148.4906015038 | 119997446.0 |
| 18 | Flow IAT Std | 6568726.0 | 3039209.059209674 | 6367479.679036268 | 0.0 | 0.0 | 65301.8024238228 | 1558351.5537008047 | 84827093.44032682 |
| 19 | Flow IAT Max | 6568726.0 | 12219095.99982158 | 26233918.396178667 | 0.0 | 1311.0 | 160441.0 | 5559577.5 | 119997446.0 |
| 20 | Flow IAT Min | 6568726.0 | 45880.690772457245 | 1433977.5507904491 | 0.0 | 4.0 | 41.0 | 462.0 | 119997446.0 |
| 21 | Fwd IAT Total | 6568726.0 | 13655915.976642502 | 32844035.573441524 | 0.0 | 0.0 | 201918.5 | 4011692.0 | 119999997.0 |
| 22 | Fwd IAT Mean | 6568726.0 | 1364607.4020385712 | 4508114.174023401 | 0.0 | 0.0 | 79917.0 | 349614.9583333333 | 119997446.0 |
| 23 | Fwd IAT Std | 6568726.0 | 1993417.4211063902 | 5641151.013604682 | 0.0 | 0.0 | 44451.36293254562 | 400800.74290192034 | 84786284.1866642 |
| 24 | Fwd IAT Max | 6568726.0 | 5346955.47974554 | 14538282.005428452 | 0.0 | 0.0 | 136762.0 | 1274016.75 | 119997446.0 |
| 25 | Fwd IAT Min | 6568726.0 | 201753.05137190985 | 3310226.2690727003 | 0.0 | 0.0 | 17.0 | 293.0 | 119997446.0 |
| 26 | Bwd IAT Total | 6568726.0 | 20417058.581838243 | 38555979.561323605 | 0.0 | 0.0 | 156455.0 | 5975151.5 | 119999998.0 |
| 27 | Bwd IAT Mean | 6568726.0 | 2438692.0444077575 | 6747602.094716753 | 0.0 | 0.0 | 52288.0 | 917140.712121212 | 119999800.0 |
| 28 | Bwd IAT Std | 6568726.0 | 3970997.2948336704 | 8837908.47417382 | 0.0 | 0.0 | 431.33436372811303 | 1444556.622971327 | 84820442.39394298 |
| 29 | Bwd IAT Max | 6568726.0 | 12061974.521850355 | 26174830.53077914 | 0.0 | 0.0 | 95981.0 | 5197692.75 | 119999800.0 |
| 30 | Bwd IAT Min | 6568726.0 | 625980.6790166008 | 5688823.2262615 | 0.0 | 0.0 | 1.0 | 44429.75 | 119999800.0 |
| 31 | Fwd PSH Flags | 6568726.0 | 2.562572711968805 | 7.123302126237615 | 0.0 | 0.0 | 1.0 | 5.0 | 2384.0 |
| 32 | Bwd PSH Flags | 6568726.0 | 2.472987760488107 | 8.985604616646713 | 0.0 | 0.0 | 1.0 | 5.0 | 15679.0 |
| 33 | Fwd URG Flags | 6568726.0 | 0.0004082983519178605 | 0.05836593783757271 | 0.0 | 0.0 | 0.0 | 0.0 | 20.0 |
| 34 | Bwd URG Flags | 6568726.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| 35 | Fwd RST Flags | 6568726.0 | 0.2177198440001912 | 0.41554751499521203 | 0.0 | 0.0 | 0.0 | 0.0 | 14.0 |
| 36 | Bwd RST Flags | 6568726.0 | 0.19662290678588207 | 0.4159469428512885 | 0.0 | 0.0 | 0.0 | 0.0 | 16.0 |
| 37 | Fwd Header Length | 6568726.0 | 138.85240273380256 | 463.7963725502698 | -32732.0 | 8.0 | 92.0 | 204.0 | 32764.0 |
| 38 | Bwd Header Length | 6568726.0 | 145.66309266058593 | 615.3333621655659 | -32764.0 | 8.0 | 80.0 | 172.0 | 32760.0 |
| 39 | Fwd Packets/s | 6568726.0 | 2348.3789160058927 | 31065.48310702035 | 0.0 | 0.9441509236856243 | 13.480086542767978 | 768.6395080707148 | 5000000.0 |
| 40 | Bwd Packets/s | 6568726.0 | 2326.350164661063 | 30294.980093090544 | 0.0 | 0.8232267064643384 | 11.607352290399325 | 770.4160246533129 | 2000000.0 |
| 41 | Packet Length Min | 6568726.0 | 16.39375443579166 | 23.613532197048674 | 0.0 | 0.0 | 0.0 | 37.0 | 1426.0 |
| 42 | Packet Length Max | 6568726.0 | 610.6561120071076 | 1006.0966737635421 | 0.0 | 71.0 | 158.0 | 1173.0 | 64800.0 |
| 43 | Packet Length Mean | 6568726.0 | 113.96469148714534 | 127.18086306994368 | 0.0 | 51.0 | 78.0 | 152.91666666666666 | 4899.284403669727 |
| 44 | Packet Length Std | 6568726.0 | 173.85931482288004 | 232.3435194693801 | 0.0 | 22.62741699796952 | 72.12489168102785 | 310.5929352521905 | 8738.959890322296 |
| 45 | Packet Length Variance | 6568726.0 | 84210.56417183763 | 855498.8286000697 | 0.0 | 512.0 | 5202.0 | 96467.9714285714 | 76369419.96466188 |
| 46 | FIN Flag Count | 6568726.0 | 0.5004279368632517 | 0.8275206780442841 | 0.0 | 0.0 | 0.0 | 1.0 | 20.0 |
| 47 | SYN Flag Count | 6568726.0 | 1.0914713142244021 | 1.0626139566490158 | 0.0 | 0.0 | 2.0 | 2.0 | 265.0 |
| 48 | RST Flag Count | 6568726.0 | 0.4143497536660838 | 0.53732888025796 | 0.0 | 0.0 | 0.0 | 1.0 | 16.0 |
| 49 | PSH Flag Count | 6568726.0 | 5.035560472456912 | 12.8617881669206 | 0.0 | 0.0 | 2.0 | 10.0 | 15811.0 |
| 50 | ACK Flag Count | 6568726.0 | 16.079641775284887 | 271.9067967458814 | 0.0 | 0.0 | 8.0 | 17.0 | 178710.0 |
| 51 | URG Flag Count | 6568726.0 | 0.0004082983519178605 | 0.05836593783757271 | 0.0 | 0.0 | 0.0 | 0.0 | 20.0 |
| 52 | CWR Flag Count | 6568726.0 | 0.3242316698854542 | 0.49697790874597436 | 0.0 | 0.0 | 0.0 | 1.0 | 47.0 |
| 53 | ECE Flag Count | 6568726.0 | 0.4625764569872453 | 0.7433889711523146 | 0.0 | 0.0 | 0.0 | 1.0 | 13.0 |
| 54 | Down/Up Ratio | 6568726.0 | 0.9381543220041503 | 0.3634126947707235 | 0.0 | 0.8461538461538461 | 1.0 | 1.0 | 24.08436213991769 |
| 55 | Average Packet Size | 6568726.0 | 113.96469148714534 | 127.18086306994365 | 0.0 | 51.0 | 78.0 | 152.91666666666666 | 4899.284403669725 |
| 56 | Fwd Segment Size Avg | 6568726.0 | 71.40598101044372 | 158.83545350599428 | 0.0 | 34.0 | 45.0 | 98.92857142857144 | 10491.46 |
| 57 | Bwd Segment Size Avg | 6568726.0 | 154.62785331901577 | 167.44196143911537 | 0.0 | 58.0 | 113.0 | 206.9090909090909 | 7095.428571428572 |
| 58 | Fwd Bytes/Bulk Avg | 6568726.0 | 361.41380687822874 | 43775.686134653384 | 0.0 | 0.0 | 0.0 | 0.0 | 8418304.0 |
| 59 | Fwd Packet/Bulk Avg | 6568726.0 | 0.07419794949583831 | 5.431905050646474 | 0.0 | 0.0 | 0.0 | 0.0 | 1438.0 |
| 60 | Fwd Bulk Rate Avg | 6568726.0 | 21878.06241636506 | 4220074.724105622 | 0.0 | 0.0 | 0.0 | 0.0 | 2643000000.0 |
| 61 | Bwd Bytes/Bulk Avg | 6568726.0 | 2714.02839637397 | 207655.51938448817 | 0.0 | 0.0 | 0.0 | 0.0 | 69470303.0 |
| 62 | Bwd Packet/Bulk Avg | 6568726.0 | 1.9894795429128875 | 144.25060974890167 | 0.0 | 0.0 | 0.0 | 0.0 | 47593.0 |
| 63 | Bwd Bulk Rate Avg | 6568726.0 | 20201041.081999462 | 191483680.42908722 | 0.0 | 0.0 | 0.0 | 0.0 | 5645000000.0 |
| 64 | Subflow Fwd Packets | 6568726.0 | 0.012399969187327954 | 0.11066260351086075 | 0.0 | 0.0 | 0.0 | 0.0 | 1.0 |
| 65 | Subflow Fwd Bytes | 6568726.0 | 36.29886404152038 | 65.96645168817585 | 0.0 | 17.0 | 22.0 | 56.0 | 4812.0 |
| 66 | Subflow Bwd Packets | 6568726.0 | 0.001172373455674662 | 0.03421986520172064 | 0.0 | 0.0 | 0.0 | 0.0 | 1.0 |
| 67 | Subflow Bwd Bytes | 6568726.0 | 76.99077416229571 | 101.79720162495667 | 0.0 | 29.0 | 54.0 | 94.0 | 2442.0 |
| 68 | FWD Init Win Bytes | 6568726.0 | 5355.886259679579 | 8429.375930706674 | 0.0 | 0.0 | 8192.0 | 8192.0 | 65535.0 |
| 69 | Bwd Init Win Bytes | 6568726.0 | 11271.463149475256 | 23691.424224945058 | 0.0 | 0.0 | 0.0 | 286.0 | 65535.0 |
| 70 | Fwd Act Data Pkts | 6568726.0 | 3.17070463892085 | 26.986756570131845 | 0.0 | 0.0 | 1.0 | 5.0 | 53217.0 |
| 71 | Fwd Seg Size Min | 6568726.0 | 15.356250816368348 | 6.406791409128087 | 0.0 | 8.0 | 20.0 | 20.0 | 48.0 |
| 72 | Active Mean | 6568726.0 | 466968.0574639844 | 1840205.1842065884 | 0.0 | 0.0 | 0.0 | 17087.97916666667 | 114303859.0 |
| 73 | Active Std | 6568726.0 | 57249.00015219808 | 635921.6259609308 | 0.0 | 0.0 | 0.0 | 0.0 | 76565382.96684347 |
| 74 | Active Max | 6568726.0 | 548590.719386225 | 2124604.672695641 | 0.0 | 0.0 | 0.0 | 22586.75 | 114303859.0 |
| 75 | Active Min | 6568726.0 | 431816.1954554049 | 1772773.2857112933 | 0.0 | 0.0 | 0.0 | 74.0 | 114303859.0 |
| 76 | Idle Mean | 6568726.0 | 11440509.199342808 | 25784992.079459827 | 0.0 | 0.0 | 0.0 | 5544251.625 | 119997446.0 |
| 77 | Idle Std | 6568726.0 | 663895.1884569954 | 4357215.678081035 | 0.0 | 0.0 | 0.0 | 0.0 | 75063556.75296102 |
| 78 | Idle Max | 6568726.0 | 11940291.562412102 | 26350844.48762705 | 0.0 | 0.0 | 0.0 | 5559577.5 | 119997446.0 |
| 79 | Idle Min | 6568726.0 | 10891502.31134226 | 25630280.506605018 | 0.0 | 0.0 | 0.0 | 5186413.25 | 119997446.0 |
| 80 | ICMP Code | 6568726.0 | -0.9961718604185956 | 0.14358744848446525 | -1.0 | -1.0 | -1.0 | -1.0 | 13.0 |
| 81 | ICMP Type | 6568726.0 | -0.9821170802374768 | 0.4046698713237926 | -1.0 | -1.0 | -1.0 | -1.0 | 11.0 |
| 82 | Total TCP Flow Time | 6568726.0 | 143588681.3530304 | 1487073149.522539 | 0.0 | 0.0 | 350135.5 | 19318854.25 | 45748333154.0 |

## Distribution Analysis
 Distribution of target variable 'Label':

Distribution Analysis

| # | Class | Percentage |
|---|---|---|
| 1 | BENIGN | 0.9924 |
| 2 | Infiltration - Communication Victim Attacker | 0.0000 |
| 3 | Infiltration - Dropbox Download | 0.0000 |
| 4 | Infiltration - Dropbox Download - Attempted | 0.0000 |
| 5 | Infiltration - NMAP Portscan | 0.0076 |

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
| 18 | Fwd IAT Total | fwd_iat_total |
| 19 | Fwd IAT Mean | fwd_iat_mean |
| 20 | Fwd IAT Std | fwd_iat_std |
| 21 | Fwd IAT Max | fwd_iat_max |
| 22 | Fwd IAT Min | fwd_iat_min |
| 23 | Bwd IAT Mean | bwd_iat_mean |
| 24 | Bwd IAT Std | bwd_iat_std |
| 25 | Bwd IAT Min | bwd_iat_min |
| 26 | Fwd PSH Flags | fwd_psh_flags |
| 27 | Bwd PSH Flags | bwd_psh_flags |
| 28 | Fwd URG Flags | fwd_urg_flags |
| 29 | Fwd RST Flags | fwd_rst_flags |
| 30 | Bwd RST Flags | bwd_rst_flags |
| 31 | Fwd Header Length | fwd_header_length |
| 32 | Bwd Header Length | bwd_header_length |
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
| 44 | Fwd Bytes/Bulk Avg | fwd_bytes/bulk_avg |
| 45 | Fwd Bulk Rate Avg | fwd_bulk_rate_avg |
| 46 | Bwd Bytes/Bulk Avg | bwd_bytes/bulk_avg |
| 47 | Bwd Bulk Rate Avg | bwd_bulk_rate_avg |
| 48 | Subflow Fwd Packets | subflow_fwd_packets |
| 49 | Subflow Bwd Packets | subflow_bwd_packets |
| 50 | FWD Init Win Bytes | fwd_init_win_bytes |
| 51 | Bwd Init Win Bytes | bwd_init_win_bytes |
| 52 | Fwd Act Data Pkts | fwd_act_data_pkts |
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
- Performing further analysis using the available columns: `['Dst Port', 'Flow Duration', 'Total Fwd Packet', 'Total Bwd packets', 'Total Length of Fwd Packet', 'Fwd Packet Length Max', 'Fwd Packet Length Min', 'Fwd Packet Length Mean', 'Bwd Packet Length Max', 'Bwd Packet Length Min', 'Bwd Packet Length Mean', 'Flow Bytes/s', 'Flow Packets/s', 'Flow IAT Mean', 'Flow IAT Std', 'Flow IAT Max', 'Flow IAT Min', 'Fwd IAT Total', 'Fwd IAT Mean', 'Fwd IAT Std', 'Fwd IAT Max', 'Fwd IAT Min', 'Bwd IAT Mean', 'Bwd IAT Std', 'Bwd IAT Min', 'Fwd PSH Flags', 'Bwd PSH Flags', 'Fwd URG Flags', 'Fwd RST Flags', 'Bwd RST Flags', 'Fwd Header Length', 'Bwd Header Length', 'Packet Length Max', 'Packet Length Mean', 'Packet Length Std', 'Packet Length Variance', 'FIN Flag Count', 'SYN Flag Count', 'RST Flag Count', 'PSH Flag Count', 'CWR Flag Count', 'ECE Flag Count', 'Down/Up Ratio', 'Fwd Bytes/Bulk Avg', 'Fwd Bulk Rate Avg', 'Bwd Bytes/Bulk Avg', 'Bwd Bulk Rate Avg', 'Subflow Fwd Packets', 'Subflow Bwd Packets', 'FWD Init Win Bytes', 'Bwd Init Win Bytes', 'Fwd Act Data Pkts', 'Fwd Seg Size Min', 'Active Mean', 'Active Std', 'Active Max', 'Idle Std', 'ICMP Code', 'ICMP Type', 'Total TCP Flow Time']`
- Train machine learning models with the reduced feature set.
## End of Report ✅  
 
✅ Report Successfully Generated in  07:07 minutes

