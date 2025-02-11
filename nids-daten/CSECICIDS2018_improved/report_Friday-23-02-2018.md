# Data Assessment Report on dataset: Friday-23-02-2018.csv
## Command line executed  
 ```dataset_assessment_prepare.py --drop-columns id,Protocol,Attempted Category,Src Port --drop-highly-correlated --correlation-threshold 0.95 --drop-categorical-columns --impute-strategy mean --assess-only --zero-variance --low-variance-threshold=0.01 --low-variance-sample-percentage=100 --missing-threshold=0.05 --descriptive-statistics --distribution-analysis --distribution-column Label -output . -input CSECICIDS2018_improved/Friday-23-02-2018.csv```  
# Report  
 ### Options used to generate this report  

| # | Option | Value |
|---|---|---|
| 1 | -input | CSECICIDS2018_improved/Friday-23-02-2018.csv |
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
 
✅ Dataset Loaded Successfully: `.../DATASET_engelen_improved/CSECICIDS2018_improved/Friday-23-02-2018.csv
- File Size: 3251.43 MB
- Number of Records: 5,976,481
- File loaded in 05:55 minutes

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
 Found 11937109 negative values:

### Columns with Negative Values

| # | Column | Negative Count |
|---|---|---|
| 1 | Fwd Header Length | 964 |
| 2 | Bwd Header Length | 2563 |
| 3 | ICMP Code | 5966791 |
| 4 | ICMP Type | 5966791 |

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
 ️Found 23 highly correlated features (threshold: 0.95):

### Highly Correlated Features

| # | Feature 1 | Feature 2 | Correlation |
|---|---|---|---|
| 1 | Total Length of Bwd Packet | Total Bwd packets | 0.9969 |
| 2 | Fwd Packet Length Std | Fwd Packet Length Max | 0.9805 |
| 3 | Bwd Packet Length Std | Bwd Packet Length Max | 0.9703 |
| 4 | Flow IAT Max | Flow IAT Std | 0.9513 |
| 5 | Bwd IAT Total | Flow Duration | 0.9956 |
| 6 | Bwd IAT Std | Flow IAT Max | 0.9542 |
| 7 | Bwd IAT Max | Flow IAT Max | 0.9950 |
| 8 | Bwd IAT Max | Bwd IAT Std | 0.9590 |
| 9 | Packet Length Min | Fwd Packet Length Min | 0.9855 |
| 10 | Packet Length Max | Fwd Packet Length Max | 0.9602 |
| 11 | Packet Length Std | Packet Length Max | 0.9560 |
| 12 | ACK Flag Count | Total Bwd packets | 0.9878 |
| 13 | ACK Flag Count | Total Length of Bwd Packet | 0.9833 |
| 14 | Average Packet Size | Packet Length Mean | 1.0000 |
| 15 | Fwd Segment Size Avg | Fwd Packet Length Mean | 1.0000 |
| 16 | Bwd Segment Size Avg | Bwd Packet Length Mean | 1.0000 |
| 17 | Fwd Bytes/Bulk Avg | Total Length of Fwd Packet | 0.9898 |
| 18 | Fwd Packet/Bulk Avg | Total Length of Fwd Packet | 0.9821 |
| 19 | Fwd Packet/Bulk Avg | Fwd Bytes/Bulk Avg | 0.9896 |
| 20 | Bwd Packet/Bulk Avg | Bwd Bytes/Bulk Avg | 1.0000 |
| 21 | Subflow Fwd Bytes | Fwd Packet Length Mean | 0.9806 |
| 22 | Subflow Fwd Bytes | Fwd Segment Size Avg | 0.9806 |
| 23 | Subflow Bwd Bytes | Bwd Packet Length Mean | 0.9753 |
| 24 | Subflow Bwd Bytes | Bwd Segment Size Avg | 0.9753 |
| 25 | Active Min | Active Mean | 0.9722 |
| 26 | Idle Mean | Flow IAT Max | 0.9932 |
| 27 | Idle Mean | Bwd IAT Max | 0.9888 |
| 28 | Idle Max | Flow IAT Std | 0.9512 |
| 29 | Idle Max | Flow IAT Max | 0.9997 |
| 30 | Idle Max | Bwd IAT Std | 0.9539 |
| 31 | Idle Max | Bwd IAT Max | 0.9947 |
| 32 | Idle Max | Idle Mean | 0.9935 |
| 33 | Idle Min | Flow IAT Max | 0.9740 |
| 34 | Idle Min | Bwd IAT Max | 0.9701 |
| 35 | Idle Min | Idle Mean | 0.9934 |
| 36 | Idle Min | Idle Max | 0.9742 |

💡 To drop these features, use:
```python
df_numeric.drop(columns=['Total Length of Bwd Packet', 'Fwd Packet Length Std', 'Bwd Packet Length Std', 'Flow IAT Max', 'Bwd IAT Total', 'Bwd IAT Std', 'Bwd IAT Max', 'Packet Length Min', 'Packet Length Max', 'Packet Length Std', 'ACK Flag Count', 'Average Packet Size', 'Fwd Segment Size Avg', 'Bwd Segment Size Avg', 'Fwd Bytes/Bulk Avg', 'Fwd Packet/Bulk Avg', 'Bwd Packet/Bulk Avg', 'Subflow Fwd Bytes', 'Subflow Bwd Bytes', 'Active Min', 'Idle Mean', 'Idle Max', 'Idle Min'], inplace=True)
```
## Descriptive Statistics Analysis
 Descriptive Statistics for Features

| # | Column | Count | Mean | Std | Min | 25% | 50% | 75% | Max |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Dst Port | 5976481.0 | 924.7950817546312 | 1863.335126964641 | 0.0 | 53.0 | 80.0 | 445.0 | 65522.0 |
| 2 | Flow Duration | 5976481.0 | 21926251.653457444 | 39713365.41759649 | 0.0 | 1249.0 | 141278.0 | 9407137.0 | 119999997.0 |
| 3 | Total Fwd Packet | 5976481.0 | 7.964286676390337 | 95.21139345289632 | 0.0 | 1.0 | 4.0 | 10.0 | 58109.0 |
| 4 | Total Bwd packets | 5976481.0 | 11.164562223154395 | 258.2194645498278 | 0.0 | 1.0 | 3.0 | 8.0 | 123118.0 |
| 5 | Total Length of Fwd Packet | 5976481.0 | 1204.6501447925627 | 47736.31367752158 | 0.0 | 40.0 | 84.0 | 1042.0 | 8500931.0 |
| 6 | Total Length of Bwd Packet | 5976481.0 | 8933.764197024972 | 366852.2631136249 | 0.0 | 73.0 | 184.0 | 1581.0 | 161602403.0 |
| 7 | Fwd Packet Length Max | 5976481.0 | 323.5326199480932 | 1302.0719117934052 | 0.0 | 38.0 | 52.0 | 517.0 | 51956.0 |
| 8 | Fwd Packet Length Min | 5976481.0 | 17.54246738172513 | 24.566896370859727 | 0.0 | 0.0 | 0.0 | 38.0 | 4981.0 |
| 9 | Fwd Packet Length Mean | 5976481.0 | 71.94512362504415 | 218.01204650193114 | 0.0 | 33.0 | 43.0 | 84.60000000000001 | 17261.666666666668 |
| 10 | Fwd Packet Length Std | 5976481.0 | 95.04893104340461 | 365.55803489474135 | 0.0 | 0.0 | 23.05609102457165 | 160.93697869386983 | 15904.505912895673 |
| 11 | Bwd Packet Length Max | 5976481.0 | 521.3825108788934 | 598.1045392253521 | 0.0 | 68.0 | 139.0 | 1173.0 | 65160.0 |
| 12 | Bwd Packet Length Min | 5976481.0 | 42.88302414079456 | 58.460093340705775 | 0.0 | 0.0 | 0.0 | 79.0 | 1460.0 |
| 13 | Bwd Packet Length Mean | 5976481.0 | 150.89854361063692 | 169.25243795395173 | 0.0 | 57.0 | 103.0 | 204.0 | 29661.84722222222 |
| 14 | Bwd Packet Length Std | 5976481.0 | 174.35714984660734 | 229.4866428836058 | 0.0 | 0.0 | 0.0 | 385.561279176216 | 19723.549086864765 |
| 15 | Flow Bytes/s | 5976477.0 | 91815.1232447386 | 1617033.22233998 | 0.0 | 69.16789872549896 | 1741.255477980735 | 111545.98825831704 | 2920000000.0 |
| 16 | Flow Packets/s | 5976477.0 | 1562.9083393289561 | 8983.404378854786 | 0.0166669340320667 | 1.6282314989015798 | 39.06631506983104 | 1666.6666666666667 | 3000000.0 |
| 17 | Flow IAT Mean | 5976481.0 | 1074509.2977275664 | 2692979.824603086 | 0.0 | 1195.0 | 35045.33333333333 | 747706.3157894737 | 119998075.0 |
| 18 | Flow IAT Std | 5976481.0 | 3274781.0287474957 | 6618420.859594672 | 0.0 | 0.0 | 40015.31557208231 | 1874470.683426914 | 84811125.55499406 |
| 19 | Flow IAT Max | 5976481.0 | 13243729.78472064 | 27494308.777351767 | 0.0 | 1209.0 | 96708.0 | 5943075.0 | 119998075.0 |
| 20 | Flow IAT Min | 5976481.0 | 46692.675626008015 | 1481404.1610205863 | 0.0 | 4.0 | 44.0 | 604.0 | 119998075.0 |
| 21 | Fwd IAT Total | 5976481.0 | 13912823.41867497 | 33389447.503685307 | 0.0 | 0.0 | 98479.0 | 3980187.0 | 119999997.0 |
| 22 | Fwd IAT Mean | 5976481.0 | 1330923.597838028 | 4182399.0620572385 | 0.0 | 0.0 | 43092.33333333334 | 342939.9 | 119998075.0 |
| 23 | Fwd IAT Std | 5976481.0 | 2049198.8165853661 | 5795922.504805812 | 0.0 | 0.0 | 11648.947634872433 | 403459.05230341706 | 84748117.39104287 |
| 24 | Fwd IAT Max | 5976481.0 | 5443847.212410614 | 14855532.688953293 | 0.0 | 0.0 | 87487.0 | 1277852.0 | 119998075.0 |
| 25 | Fwd IAT Min | 5976481.0 | 154823.91708197517 | 2817928.6230308637 | 0.0 | 0.0 | 17.0 | 268.0 | 119998075.0 |
| 26 | Bwd IAT Total | 5976481.0 | 21596924.302271686 | 39579165.83479276 | 0.0 | 0.0 | 50194.0 | 6834045.0 | 119999997.0 |
| 27 | Bwd IAT Mean | 5976481.0 | 2552769.8502612286 | 6758865.208564733 | 0.0 | 0.0 | 18101.75 | 1036643.8333333334 | 119999762.0 |
| 28 | Bwd IAT Std | 5976481.0 | 4329747.567539925 | 9300562.475112315 | 0.0 | 0.0 | 128.2273371789339 | 1771518.0032641843 | 84818332.38730793 |
| 29 | Bwd IAT Max | 5976481.0 | 13089890.443168145 | 27439974.86696148 | 0.0 | 0.0 | 32037.0 | 5586867.0 | 119999762.0 |
| 30 | Bwd IAT Min | 5976481.0 | 617604.2256811324 | 5629227.53557162 | 0.0 | 0.0 | 1.0 | 25238.0 | 119999762.0 |
| 31 | Fwd PSH Flags | 5976481.0 | 2.4503384182096455 | 7.6974974191891885 | 0.0 | 0.0 | 1.0 | 5.0 | 2102.0 |
| 32 | Bwd PSH Flags | 5976481.0 | 2.3246694835974546 | 16.37617311657065 | 0.0 | 0.0 | 0.0 | 5.0 | 17893.0 |
| 33 | Fwd URG Flags | 5976481.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| 34 | Bwd URG Flags | 5976481.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| 35 | Fwd RST Flags | 5976481.0 | 0.17350360521517597 | 0.3819851357250805 | 0.0 | 0.0 | 0.0 | 0.0 | 11.0 |
| 36 | Bwd RST Flags | 5976481.0 | 0.20852170365805564 | 0.42719298656786864 | 0.0 | 0.0 | 0.0 | 0.0 | 25.0 |
| 37 | Fwd Header Length | 5976481.0 | 136.1695425786512 | 509.71530597886976 | -32744.0 | 8.0 | 80.0 | 212.0 | 32748.0 |
| 38 | Bwd Header Length | 5976481.0 | 136.9785638070296 | 639.1700136285385 | -32764.0 | 8.0 | 72.0 | 184.0 | 32752.0 |
| 39 | Fwd Packets/s | 5976481.0 | 782.1427353288817 | 5594.024339681488 | 0.0 | 0.8115010253315454 | 20.33140185015757 | 832.6394671107411 | 3000000.0 |
| 40 | Bwd Packets/s | 5976481.0 | 780.7645579608815 | 5823.934927328279 | 0.0 | 0.6622250914438248 | 17.976881730095098 | 833.3333333333334 | 2000000.0 |
| 41 | Packet Length Min | 5976481.0 | 17.5010336350103 | 24.10995168410775 | 0.0 | 0.0 | 0.0 | 38.0 | 1460.0 |
| 42 | Packet Length Max | 5976481.0 | 600.6633276337698 | 1383.7752874051264 | 0.0 | 69.0 | 140.0 | 1173.0 | 65160.0 |
| 43 | Packet Length Mean | 5976481.0 | 111.8319907118055 | 141.23031454970632 | 0.0 | 50.66666666666666 | 72.0 | 146.24 | 15601.401459854014 |
| 44 | Packet Length Std | 5976481.0 | 169.58730306929567 | 292.08818089620996 | 0.0 | 21.213203435596427 | 65.24058041842771 | 300.19300140949 | 20583.731886835187 |
| 45 | Packet Length Variance | 5976481.0 | 114075.34450636679 | 1385502.9685529734 | 0.0 | 450.0 | 4256.333333333333 | 90115.83809523808 | 423690018.3891156 |
| 46 | FIN Flag Count | 5976481.0 | 0.5256720468114933 | 0.8241444596033632 | 0.0 | 0.0 | 0.0 | 1.0 | 16.0 |
| 47 | SYN Flag Count | 5976481.0 | 1.0344396644112146 | 1.0412866695925216 | 0.0 | 0.0 | 2.0 | 2.0 | 207.0 |
| 48 | RST Flag Count | 5976481.0 | 0.3820386946766835 | 0.5347929660476765 | 0.0 | 0.0 | 0.0 | 1.0 | 25.0 |
| 49 | PSH Flag Count | 5976481.0 | 4.7750079018071006 | 19.10526476723105 | 0.0 | 0.0 | 2.0 | 10.0 | 18018.0 |
| 50 | ACK Flag Count | 5976481.0 | 17.501930818486663 | 341.5882102004679 | 0.0 | 0.0 | 6.0 | 17.0 | 180279.0 |
| 51 | URG Flag Count | 5976481.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| 52 | CWR Flag Count | 5976481.0 | 0.30722426792622615 | 0.4964618909980226 | 0.0 | 0.0 | 0.0 | 1.0 | 9.0 |
| 53 | ECE Flag Count | 5976481.0 | 0.4334388413516248 | 0.7264113850493258 | 0.0 | 0.0 | 0.0 | 1.0 | 7.0 |
| 54 | Down/Up Ratio | 5976481.0 | 0.9373889380930176 | 0.35707744603979263 | 0.0 | 0.8571428571428571 | 1.0 | 1.0 | 28.666666666666668 |
| 55 | Average Packet Size | 5976481.0 | 111.83199071180547 | 141.23031454970635 | 0.0 | 50.66666666666666 | 72.0 | 146.24 | 15601.401459854014 |
| 56 | Fwd Segment Size Avg | 5976481.0 | 71.94512362504415 | 218.01204650193114 | 0.0 | 33.0 | 43.0 | 84.6 | 17261.666666666668 |
| 57 | Bwd Segment Size Avg | 5976481.0 | 150.89854361063692 | 169.25243795395173 | 0.0 | 57.0 | 103.0 | 204.0 | 29661.847222222223 |
| 58 | Fwd Bytes/Bulk Avg | 5976481.0 | 436.1103155853754 | 46952.8064143229 | 0.0 | 0.0 | 0.0 | 0.0 | 8498496.0 |
| 59 | Fwd Packet/Bulk Avg | 5976481.0 | 0.08511798163501232 | 5.776334698474198 | 0.0 | 0.0 | 0.0 | 0.0 | 1072.0 |
| 60 | Fwd Bulk Rate Avg | 5976481.0 | 26576.46128382237 | 5180624.975516453 | 0.0 | 0.0 | 0.0 | 0.0 | 2920000000.0 |
| 61 | Bwd Bytes/Bulk Avg | 5976481.0 | 2557.929276442107 | 181489.79533545848 | 0.0 | 0.0 | 0.0 | 0.0 | 56698402.0 |
| 62 | Bwd Packet/Bulk Avg | 5976481.0 | 1.8814812596241834 | 125.95941560453619 | 0.0 | 0.0 | 0.0 | 0.0 | 38845.0 |
| 63 | Bwd Bulk Rate Avg | 5976481.0 | 19507164.809454594 | 187799225.1392336 | 0.0 | 0.0 | 0.0 | 0.0 | 5500000000.0 |
| 64 | Subflow Fwd Packets | 5976481.0 | 0.013066217394483477 | 0.11355832648991596 | 0.0 | 0.0 | 0.0 | 0.0 | 1.0 |
| 65 | Subflow Fwd Bytes | 5976481.0 | 35.98378192786022 | 89.32761076277927 | 0.0 | 16.0 | 22.0 | 42.0 | 4116.0 |
| 66 | Subflow Bwd Packets | 5976481.0 | 0.0008734236752363138 | 0.029540835335780533 | 0.0 | 0.0 | 0.0 | 0.0 | 1.0 |
| 67 | Subflow Bwd Bytes | 5976481.0 | 75.1741221966572 | 100.95086921722925 | 0.0 | 28.0 | 51.0 | 91.0 | 15588.0 |
| 68 | FWD Init Win Bytes | 5976481.0 | 4578.523675386904 | 5687.371481765082 | 0.0 | 0.0 | 8192.0 | 8192.0 | 65535.0 |
| 69 | Bwd Init Win Bytes | 5976481.0 | 7892.098902514707 | 20301.701999817953 | 0.0 | 0.0 | 0.0 | 176.0 | 65535.0 |
| 70 | Fwd Act Data Pkts | 5976481.0 | 3.0443289286789335 | 9.796117566638326 | 0.0 | 0.0 | 1.0 | 5.0 | 4168.0 |
| 71 | Fwd Seg Size Min | 5976481.0 | 15.05944116613104 | 6.50654746577881 | 0.0 | 8.0 | 20.0 | 20.0 | 48.0 |
| 72 | Active Mean | 5976481.0 | 469820.4354690377 | 1827844.4288183837 | 0.0 | 0.0 | 0.0 | 20878.0 | 114259455.0 |
| 73 | Active Std | 5976481.0 | 51345.76962502462 | 605024.0437665369 | 0.0 | 0.0 | 0.0 | 0.0 | 76344327.24490893 |
| 74 | Active Max | 5976481.0 | 545425.9225266507 | 2102421.4028157853 | 0.0 | 0.0 | 0.0 | 50646.0 | 114259455.0 |
| 75 | Active Min | 5976481.0 | 438187.2119785874 | 1765629.9937849906 | 0.0 | 0.0 | 0.0 | 11102.0 | 114259455.0 |
| 76 | Idle Mean | 5976481.0 | 12529509.196690416 | 27114432.831466705 | 0.0 | 0.0 | 0.0 | 5923810.5 | 119998075.0 |
| 77 | Idle Std | 5976481.0 | 640368.9682952001 | 4255107.503392897 | 0.0 | 0.0 | 0.0 | 0.0 | 70452207.96271408 |
| 78 | Idle Max | 5976481.0 | 13002915.520362401 | 27599160.181517236 | 0.0 | 0.0 | 0.0 | 5943075.0 | 119998075.0 |
| 79 | Idle Min | 5976481.0 | 11999294.83021698 | 26998902.892116953 | 0.0 | 0.0 | 0.0 | 5303931.0 | 119998075.0 |
| 80 | ICMP Code | 5976481.0 | -0.9967925941703822 | 0.1355776810493859 | -1.0 | -1.0 | -1.0 | -1.0 | 13.0 |
| 81 | ICMP Type | 5976481.0 | -0.985829453820735 | 0.3630767628265983 | -1.0 | -1.0 | -1.0 | -1.0 | 11.0 |
| 82 | Total TCP Flow Time | 5976481.0 | 185874813.7476018 | 1815065480.0414565 | 0.0 | 0.0 | 180882.0 | 60012563.0 | 82762320857.0 |

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
| 26 | Fwd RST Flags | fwd_rst_flags |
| 27 | Bwd RST Flags | bwd_rst_flags |
| 28 | Fwd Header Length | fwd_header_length |
| 29 | Bwd Header Length | bwd_header_length |
| 30 | Fwd Packets/s | fwd_packets/s |
| 31 | Bwd Packets/s | bwd_packets/s |
| 32 | Packet Length Mean | packet_length_mean |
| 33 | Packet Length Variance | packet_length_variance |
| 34 | FIN Flag Count | fin_flag_count |
| 35 | SYN Flag Count | syn_flag_count |
| 36 | RST Flag Count | rst_flag_count |
| 37 | PSH Flag Count | psh_flag_count |
| 38 | CWR Flag Count | cwr_flag_count |
| 39 | ECE Flag Count | ece_flag_count |
| 40 | Down/Up Ratio | down/up_ratio |
| 41 | Fwd Bulk Rate Avg | fwd_bulk_rate_avg |
| 42 | Bwd Bytes/Bulk Avg | bwd_bytes/bulk_avg |
| 43 | Bwd Bulk Rate Avg | bwd_bulk_rate_avg |
| 44 | Subflow Fwd Packets | subflow_fwd_packets |
| 45 | Subflow Bwd Packets | subflow_bwd_packets |
| 46 | FWD Init Win Bytes | fwd_init_win_bytes |
| 47 | Bwd Init Win Bytes | bwd_init_win_bytes |
| 48 | Fwd Act Data Pkts | fwd_act_data_pkts |
| 49 | Fwd Seg Size Min | fwd_seg_size_min |
| 50 | Active Mean | active_mean |
| 51 | Active Std | active_std |
| 52 | Active Max | active_max |
| 53 | Idle Std | idle_std |
| 54 | ICMP Code | icmp_code |
| 55 | ICMP Type | icmp_type |
| 56 | Total TCP Flow Time | total_tcp_flow_time |

## Recommendation
 Based on the assessment, it is recommended to continue working with the available columns. You may consider the following:
- Performing further analysis using the available columns: `['Dst Port', 'Flow Duration', 'Total Fwd Packet', 'Total Bwd packets', 'Total Length of Fwd Packet', 'Fwd Packet Length Max', 'Fwd Packet Length Min', 'Fwd Packet Length Mean', 'Bwd Packet Length Max', 'Bwd Packet Length Min', 'Bwd Packet Length Mean', 'Flow Bytes/s', 'Flow Packets/s', 'Flow IAT Mean', 'Flow IAT Std', 'Flow IAT Min', 'Fwd IAT Total', 'Fwd IAT Mean', 'Fwd IAT Std', 'Fwd IAT Max', 'Fwd IAT Min', 'Bwd IAT Mean', 'Bwd IAT Min', 'Fwd PSH Flags', 'Bwd PSH Flags', 'Fwd RST Flags', 'Bwd RST Flags', 'Fwd Header Length', 'Bwd Header Length', 'Fwd Packets/s', 'Bwd Packets/s', 'Packet Length Mean', 'Packet Length Variance', 'FIN Flag Count', 'SYN Flag Count', 'RST Flag Count', 'PSH Flag Count', 'CWR Flag Count', 'ECE Flag Count', 'Down/Up Ratio', 'Fwd Bulk Rate Avg', 'Bwd Bytes/Bulk Avg', 'Bwd Bulk Rate Avg', 'Subflow Fwd Packets', 'Subflow Bwd Packets', 'FWD Init Win Bytes', 'Bwd Init Win Bytes', 'Fwd Act Data Pkts', 'Fwd Seg Size Min', 'Active Mean', 'Active Std', 'Active Max', 'Idle Std', 'ICMP Code', 'ICMP Type', 'Total TCP Flow Time']`
- Train machine learning models with the reduced feature set.
## End of Report ✅  
 
✅ Report Successfully Generated in  08:56 minutes

