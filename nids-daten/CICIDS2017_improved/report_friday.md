# Data Assessment Report on dataset: friday.csv
## Command line executed  
 ```dataset_assessment_prepare.py --drop-columns id,Protocol,Attempted Category,Src Port --drop-highly-correlated --correlation-threshold 0.95 --drop-categorical-columns --impute-strategy mean --assess-only --zero-variance --low-variance-threshold=0.01 --low-variance-sample-percentage=100 --missing-threshold=0.05 --descriptive-statistics --distribution-analysis --distribution-column Label -output . -input CICIDS2017_improved/friday.csv```  
# Report  
 ### Options used to generate this report  

| # | Option | Value |
|---|---|---|
| 1 | -input | CICIDS2017_improved/friday.csv |
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
 
✅ Dataset Loaded Successfully: `.../DATASET_engelen_improved/CICIDS2017_improved/friday.csv
- File Size: 271.98 MB
- Number of Records: 547,557
- File loaded in 00:12 minutes

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
 Found 1094893 negative values:

### Columns with Negative Values

| # | Column | Negative Count |
|---|---|---|
| 1 | Fwd Header Length | 40 |
| 2 | Bwd Header Length | 89 |
| 3 | ICMP Code | 547382 |
| 4 | ICMP Type | 547382 |

💡 To replace with zero, use:
```python
df_numeric.loc[:, df_numeric.columns] = np.where(df_numeric < 0, 0, df_numeric)
```
## Infinite Values ✅
 No issues found
## Missing Values ✅  
 No columns to drop, max missing =  0.0% and that's below threshold 0.05%
## Impute Missing Values ✅  
 No issues found
## Highly Correlated Features ⚠️  
 ️Found 28 highly correlated features (threshold: 0.95):

### Highly Correlated Features

| # | Feature 1 | Feature 2 | Correlation |
|---|---|---|---|
| 1 | Total Bwd packets | Total Fwd Packet | 0.9996 |
| 2 | Total Length of Bwd Packet | Total Fwd Packet | 0.9974 |
| 3 | Total Length of Bwd Packet | Total Bwd packets | 0.9962 |
| 4 | Bwd Packet Length Mean | Bwd Packet Length Max | 0.9527 |
| 5 | Bwd Packet Length Std | Bwd Packet Length Max | 0.9903 |
| 6 | Fwd IAT Total | Flow Duration | 0.9995 |
| 7 | Fwd IAT Mean | Flow IAT Mean | 0.9576 |
| 8 | Fwd IAT Max | Flow IAT Max | 0.9984 |
| 9 | Fwd IAT Min | Fwd IAT Mean | 0.9689 |
| 10 | Bwd IAT Total | Flow Duration | 0.9850 |
| 11 | Bwd IAT Total | Fwd IAT Total | 0.9845 |
| 12 | Bwd IAT Mean | Fwd IAT Mean | 0.9784 |
| 13 | Bwd IAT Max | Flow IAT Max | 0.9572 |
| 14 | Bwd IAT Max | Fwd IAT Max | 0.9554 |
| 15 | Bwd IAT Min | Fwd IAT Mean | 0.9530 |
| 16 | Bwd IAT Min | Fwd IAT Min | 0.9803 |
| 17 | Bwd IAT Min | Bwd IAT Mean | 0.9605 |
| 18 | Fwd Packets/s | Flow Packets/s | 0.9567 |
| 19 | Packet Length Max | Bwd Packet Length Max | 0.9910 |
| 20 | Packet Length Max | Bwd Packet Length Std | 0.9811 |
| 21 | Packet Length Mean | Bwd Packet Length Mean | 0.9744 |
| 22 | Packet Length Std | Bwd Packet Length Max | 0.9858 |
| 23 | Packet Length Std | Bwd Packet Length Mean | 0.9684 |
| 24 | Packet Length Std | Bwd Packet Length Std | 0.9854 |
| 25 | Packet Length Std | Packet Length Max | 0.9910 |
| 26 | Packet Length Variance | Bwd Packet Length Max | 0.9585 |
| 27 | Packet Length Variance | Bwd Packet Length Std | 0.9771 |
| 28 | Packet Length Variance | Packet Length Max | 0.9615 |
| 29 | Packet Length Variance | Packet Length Std | 0.9588 |
| 30 | PSH Flag Count | Bwd PSH Flags | 0.9747 |
| 31 | ACK Flag Count | Total Fwd Packet | 0.9998 |
| 32 | ACK Flag Count | Total Bwd packets | 0.9999 |
| 33 | ACK Flag Count | Total Length of Bwd Packet | 0.9968 |
| 34 | Average Packet Size | Bwd Packet Length Mean | 0.9744 |
| 35 | Average Packet Size | Packet Length Mean | 1.0000 |
| 36 | Fwd Segment Size Avg | Fwd Packet Length Mean | 1.0000 |
| 37 | Bwd Segment Size Avg | Bwd Packet Length Max | 0.9527 |
| 38 | Bwd Segment Size Avg | Bwd Packet Length Mean | 1.0000 |
| 39 | Bwd Segment Size Avg | Packet Length Mean | 0.9744 |
| 40 | Bwd Segment Size Avg | Packet Length Std | 0.9684 |
| 41 | Bwd Segment Size Avg | Average Packet Size | 0.9744 |
| 42 | Bwd Packet/Bulk Avg | Bwd Bytes/Bulk Avg | 0.9864 |
| 43 | Subflow Fwd Bytes | Fwd Packet Length Mean | 0.9762 |
| 44 | Subflow Fwd Bytes | Fwd Segment Size Avg | 0.9762 |
| 45 | Subflow Bwd Bytes | Bwd Packet Length Mean | 0.9866 |
| 46 | Subflow Bwd Bytes | Packet Length Mean | 0.9894 |
| 47 | Subflow Bwd Bytes | Average Packet Size | 0.9894 |
| 48 | Subflow Bwd Bytes | Bwd Segment Size Avg | 0.9866 |
| 49 | Idle Mean | Flow IAT Max | 0.9892 |
| 50 | Idle Mean | Fwd IAT Max | 0.9875 |
| 51 | Idle Max | Flow IAT Max | 0.9968 |
| 52 | Idle Max | Fwd IAT Max | 0.9951 |
| 53 | Idle Max | Bwd IAT Max | 0.9554 |
| 54 | Idle Max | Idle Mean | 0.9924 |
| 55 | Idle Min | Flow IAT Max | 0.9674 |
| 56 | Idle Min | Fwd IAT Max | 0.9658 |
| 57 | Idle Min | Idle Mean | 0.9922 |
| 58 | Idle Min | Idle Max | 0.9706 |

💡 To drop these features, use:
```python
df_numeric.drop(columns=['Total Bwd packets', 'Total Length of Bwd Packet', 'Bwd Packet Length Mean', 'Bwd Packet Length Std', 'Fwd IAT Total', 'Fwd IAT Mean', 'Fwd IAT Max', 'Fwd IAT Min', 'Bwd IAT Total', 'Bwd IAT Mean', 'Bwd IAT Max', 'Bwd IAT Min', 'Fwd Packets/s', 'Packet Length Max', 'Packet Length Mean', 'Packet Length Std', 'Packet Length Variance', 'PSH Flag Count', 'ACK Flag Count', 'Average Packet Size', 'Fwd Segment Size Avg', 'Bwd Segment Size Avg', 'Bwd Packet/Bulk Avg', 'Subflow Fwd Bytes', 'Subflow Bwd Bytes', 'Idle Mean', 'Idle Max', 'Idle Min'], inplace=True)
```
## Descriptive Statistics Analysis
 Descriptive Statistics for Features

| # | Column | Count | Mean | Std | Min | 25% | 50% | 75% | Max |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Dst Port | 547557.0 | 2826.089161493689 | 8604.258903148097 | 0.0 | 53.0 | 80.0 | 1055.0 | 65525.0 |
| 2 | Flow Duration | 547557.0 | 9252255.049213141 | 26093392.625652205 | 1.0 | 71.0 | 31141.0 | 5032396.0 | 119999993.0 |
| 3 | Total Fwd Packet | 547557.0 | 8.726116185164285 | 648.6441279550718 | 0.0 | 1.0 | 2.0 | 8.0 | 207963.0 |
| 4 | Total Bwd packets | 547557.0 | 9.444565588605387 | 874.4271097217992 | 0.0 | 1.0 | 2.0 | 5.0 | 284603.0 |
| 5 | Total Length of Fwd Packet | 547557.0 | 374.740299183464 | 3088.263160065707 | 0.0 | 0.0 | 41.0 | 88.0 | 624776.0 |
| 6 | Total Length of Bwd Packet | 547557.0 | 14087.191139917853 | 1958687.8147577427 | 0.0 | 0.0 | 168.0 | 4158.0 | 627039464.0 |
| 7 | Fwd Packet Length Max | 547557.0 | 129.86649426452405 | 495.92342974254575 | 0.0 | 0.0 | 27.0 | 47.0 | 24820.0 |
| 8 | Fwd Packet Length Min | 547557.0 | 15.274008002819798 | 31.526135159765236 | 0.0 | 0.0 | 0.0 | 35.0 | 1472.0 |
| 9 | Fwd Packet Length Mean | 547557.0 | 33.84772277591443 | 107.69139476049573 | 0.0 | 0.0 | 16.02 | 44.0 | 5775.5 |
| 10 | Fwd Packet Length Std | 547557.0 | 37.066980999204134 | 169.46287817483838 | 0.0 | 0.0 | 0.0 | 7.071067811865476 | 7018.511024426763 |
| 11 | Bwd Packet Length Max | 547557.0 | 1542.2082742070688 | 2879.0480501931306 | 0.0 | 0.0 | 102.0 | 1460.0 | 13032.0 |
| 12 | Bwd Packet Length Min | 547557.0 | 39.10345954850363 | 68.7783901613152 | 0.0 | 0.0 | 0.0 | 74.0 | 1454.0 |
| 13 | Bwd Packet Length Mean | 547557.0 | 495.0973943559536 | 841.7847340884584 | 0.0 | 0.0 | 94.0 | 359.57142857142856 | 3865.0 |
| 14 | Bwd Packet Length Std | 547557.0 | 644.0211626731597 | 1296.9984934363924 | 0.0 | 0.0 | 0.0 | 587.3167704815595 | 6694.376371253711 |
| 15 | Flow Bytes/s | 547557.0 | 337176.4022775563 | 3324236.3109615482 | 0.0 | 0.0 | 1226.603502337333 | 6368.09974039645 | 178176470.5882353 |
| 16 | Flow Packets/s | 547557.0 | 24213.942366850624 | 94546.8594658097 | 0.0250074609759821 | 3.0023283056009937 | 107.14381378405164 | 28985.50724637681 | 2000000.0 |
| 17 | Flow IAT Mean | 547557.0 | 622811.8272455621 | 2884371.9853367656 | 0.6666666666666666 | 58.0 | 11403.23076923077 | 361215.6470588236 | 67999523.0 |
| 18 | Flow IAT Std | 547557.0 | 1341843.8215774011 | 4882117.328061853 | 0.0 | 0.0 | 128.46140795325783 | 1179748.7206616886 | 84783368.78540537 |
| 19 | Flow IAT Max | 547557.0 | 4018439.2767474437 | 11772768.042578362 | 1.0 | 71.0 | 30769.0 | 4147953.0 | 119991197.0 |
| 20 | Flow IAT Min | 547557.0 | 30822.36059807472 | 1119429.5131786165 | 0.0 | 3.0 | 6.0 | 51.0 | 67999523.0 |
| 21 | Fwd IAT Total | 547557.0 | 9203249.48587453 | 26070603.00480041 | 0.0 | 0.0 | 3.0 | 4937450.0 | 119999993.0 |
| 22 | Fwd IAT Mean | 547557.0 | 1406637.4507131346 | 7729302.377606597 | 0.0 | 0.0 | 3.0 | 649555.8571428572 | 119964198.0 |
| 23 | Fwd IAT Std | 547557.0 | 1198076.7218376657 | 3356666.4737959644 | 0.0 | 0.0 | 0.0 | 1387040.6150908128 | 81923507.22870153 |
| 24 | Fwd IAT Max | 547557.0 | 3994023.096075842 | 11768532.00421422 | 0.0 | 0.0 | 3.0 | 4112628.0 | 119991382.0 |
| 25 | Fwd IAT Min | 547557.0 | 752102.8287812958 | 7522465.843854916 | 0.0 | 0.0 | 1.0 | 4.0 | 119964198.0 |
| 26 | Bwd IAT Total | 547557.0 | 8001880.912631927 | 25996774.350053433 | 0.0 | 0.0 | 4.0 | 573543.0 | 119999871.0 |
| 27 | Bwd IAT Mean | 547557.0 | 1337450.9675262675 | 7737487.927151605 | 0.0 | 0.0 | 4.0 | 108941.2 | 119894965.0 |
| 28 | Bwd IAT Std | 547557.0 | 840044.7762776795 | 3446497.786827255 | 0.0 | 0.0 | 0.0 | 112192.86687478548 | 81949316.62621485 |
| 29 | Bwd IAT Max | 547557.0 | 2987870.067556437 | 11507476.355117371 | 0.0 | 0.0 | 4.0 | 500289.0 | 119991381.0 |
| 30 | Bwd IAT Min | 547557.0 | 789820.2513272591 | 7459781.3084389735 | 0.0 | 0.0 | 3.0 | 32.0 | 119894965.0 |
| 31 | Fwd PSH Flags | 547557.0 | 0.975611671478951 | 4.2419476545796915 | 0.0 | 0.0 | 0.0 | 1.0 | 855.0 |
| 32 | Bwd PSH Flags | 547557.0 | 1.232786723573984 | 15.286067724490337 | 0.0 | 0.0 | 0.0 | 1.0 | 4753.0 |
| 33 | Fwd URG Flags | 547557.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| 34 | Bwd URG Flags | 547557.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| 35 | Fwd RST Flags | 547557.0 | 0.24223962071528626 | 0.9067552601316874 | 0.0 | 0.0 | 0.0 | 0.0 | 101.0 |
| 36 | Bwd RST Flags | 547557.0 | 0.3145864266185986 | 0.4727471724024691 | 0.0 | 0.0 | 0.0 | 1.0 | 4.0 |
| 37 | Fwd Header Length | 547557.0 | 135.0448190781964 | 576.2274399606783 | -32708.0 | 16.0 | 40.0 | 172.0 | 32748.0 |
| 38 | Bwd Header Length | 547557.0 | 127.56870243645866 | 697.0851351481496 | -32568.0 | 16.0 | 20.0 | 112.0 | 32680.0 |
| 39 | Fwd Packets/s | 547557.0 | 13041.97047499473 | 55878.875490407234 | 0.0 | 1.7195683686872494 | 60.71276789508834 | 14492.753623188406 | 2000000.0 |
| 40 | Bwd Packets/s | 547557.0 | 11171.971891855896 | 44190.48557863823 | 0.0 | 1.241324912185129 | 42.78440936122877 | 14285.714285714286 | 1000000.0 |
| 41 | Packet Length Min | 547557.0 | 15.02902711498529 | 24.519753453873317 | 0.0 | 0.0 | 0.0 | 35.0 | 1359.0 |
| 42 | Packet Length Max | 547557.0 | 1575.9867009279399 | 2894.5355796085196 | 0.0 | 0.0 | 102.0 | 1460.0 | 24820.0 |
| 43 | Packet Length Mean | 547557.0 | 224.57038388860786 | 333.09586588280007 | 0.0 | 0.0 | 68.5 | 225.28125 | 2090.11197043912 |
| 44 | Packet Length Std | 547557.0 | 475.0417444358548 | 851.943052641833 | 0.0 | 0.0 | 35.35533905932738 | 475.9733483157207 | 4693.160684645995 |
| 45 | Packet Length Variance | 547557.0 | 951470.2983645244 | 2236329.190590508 | 0.0 | 0.0 | 1250.0 | 226550.6283068784 | 22025757.211906865 |
| 46 | FIN Flag Count | 547557.0 | 0.5370089324033845 | 0.8469780928668205 | 0.0 | 0.0 | 0.0 | 1.0 | 16.0 |
| 47 | SYN Flag Count | 547557.0 | 0.9905343188015129 | 0.8820672780893611 | 0.0 | 0.0 | 1.0 | 2.0 | 12.0 |
| 48 | RST Flag Count | 547557.0 | 0.5579711335988765 | 0.9562807432599641 | 0.0 | 0.0 | 1.0 | 1.0 | 101.0 |
| 49 | PSH Flag Count | 547557.0 | 2.208398395052935 | 17.416480777642 | 0.0 | 0.0 | 0.0 | 2.0 | 4869.0 |
| 50 | ACK Flag Count | 547557.0 | 16.088505854185044 | 1522.9129877701191 | 0.0 | 0.0 | 1.0 | 12.0 | 492566.0 |
| 51 | URG Flag Count | 547557.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| 52 | CWR Flag Count | 547557.0 | 0.00034882213175979854 | 0.04074288275136582 | 0.0 | 0.0 | 0.0 | 0.0 | 23.0 |
| 53 | ECE Flag Count | 547557.0 | 0.0003269066051570887 | 0.025099116964583973 | 0.0 | 0.0 | 0.0 | 0.0 | 2.0 |
| 54 | Down/Up Ratio | 547557.0 | 0.9132255770467538 | 0.20296499226205955 | 0.0 | 0.8571428571428571 | 1.0 | 1.0 | 9.071428571428571 |
| 55 | Average Packet Size | 547557.0 | 224.5703838886078 | 333.0958658828 | 0.0 | 0.0 | 68.5 | 225.28125 | 2090.1119704391167 |
| 56 | Fwd Segment Size Avg | 547557.0 | 33.84772277591443 | 107.69139476049573 | 0.0 | 0.0 | 16.02 | 44.0 | 5775.5 |
| 57 | Bwd Segment Size Avg | 547557.0 | 495.0973943559535 | 841.7847340884584 | 0.0 | 0.0 | 94.0 | 359.57142857142856 | 3865.0 |
| 58 | Fwd Bytes/Bulk Avg | 547557.0 | 54.748093805759034 | 1495.461988579704 | 0.0 | 0.0 | 0.0 | 0.0 | 207918.0 |
| 59 | Fwd Packet/Bulk Avg | 547557.0 | 0.16977410570954257 | 1.4762661681642784 | 0.0 | 0.0 | 0.0 | 0.0 | 360.0 |
| 60 | Fwd Bulk Rate Avg | 547557.0 | 139527.56093155599 | 3385779.3049209565 | 0.0 | 0.0 | 0.0 | 0.0 | 487000000.0 |
| 61 | Bwd Bytes/Bulk Avg | 547557.0 | 2691.070940559613 | 278027.4125341197 | 0.0 | 0.0 | 0.0 | 0.0 | 156759758.0 |
| 62 | Bwd Packet/Bulk Avg | 547557.0 | 1.2920810070914992 | 98.25821643197474 | 0.0 | 0.0 | 0.0 | 0.0 | 58270.0 |
| 63 | Bwd Bulk Rate Avg | 547557.0 | 1203375.900339143 | 6637903.885491567 | 0.0 | 0.0 | 0.0 | 0.0 | 872666666.0 |
| 64 | Subflow Fwd Packets | 547557.0 | 0.005898929243896069 | 0.07657768987975097 | 0.0 | 0.0 | 0.0 | 0.0 | 1.0 |
| 65 | Subflow Fwd Bytes | 547557.0 | 16.973491344280138 | 48.40630406681785 | 0.0 | 0.0 | 8.0 | 22.0 | 1777.0 |
| 66 | Subflow Bwd Packets | 547557.0 | 1.8262938835591545e-06 | 0.0013514044115508696 | 0.0 | 0.0 | 0.0 | 0.0 | 1.0 |
| 67 | Subflow Bwd Bytes | 547557.0 | 207.1142383350044 | 333.9519573388321 | 0.0 | 0.0 | 45.0 | 173.0 | 2090.0 |
| 68 | FWD Init Win Bytes | 547557.0 | 9199.048046139489 | 12582.069687516656 | 0.0 | 0.0 | 1024.0 | 8192.0 | 65535.0 |
| 69 | Bwd Init Win Bytes | 547557.0 | 580.5391091703694 | 3886.9336988901227 | 0.0 | 0.0 | 0.0 | 229.0 | 65535.0 |
| 70 | Fwd Act Data Pkts | 547557.0 | 1.5853819784972158 | 5.164703488216298 | 0.0 | 0.0 | 1.0 | 1.0 | 855.0 |
| 71 | Fwd Seg Size Min | 547557.0 | 20.087048471665963 | 10.994899041821789 | 0.0 | 8.0 | 20.0 | 24.0 | 44.0 |
| 72 | Active Mean | 547557.0 | 133760.66431426437 | 733984.9077762307 | 0.0 | 0.0 | 0.0 | 0.0 | 110097488.0 |
| 73 | Active Std | 547557.0 | 37994.85154625686 | 383547.6889061662 | 0.0 | 0.0 | 0.0 | 0.0 | 70514318.10105315 |
| 74 | Active Max | 547557.0 | 202393.58489435803 | 1071617.4478661837 | 0.0 | 0.0 | 0.0 | 0.0 | 110097488.0 |
| 75 | Active Min | 547557.0 | 112581.76046694683 | 668297.0998747454 | 0.0 | 0.0 | 0.0 | 0.0 | 110097488.0 |
| 76 | Idle Mean | 547557.0 | 3610677.938136805 | 11492795.778513733 | 0.0 | 0.0 | 0.0 | 0.0 | 119991197.0 |
| 77 | Idle Std | 547557.0 | 145516.97088085642 | 1870863.2662038119 | 0.0 | 0.0 | 0.0 | 0.0 | 76635214.00412633 |
| 78 | Idle Max | 547557.0 | 3716373.053574331 | 11829619.864882348 | 0.0 | 0.0 | 0.0 | 0.0 | 119991197.0 |
| 79 | Idle Min | 547557.0 | 3451524.209503303 | 11314019.254303217 | 0.0 | 0.0 | 0.0 | 0.0 | 119991197.0 |
| 80 | ICMP Code | 547557.0 | -0.999262177271042 | 0.05005132766448113 | -1.0 | -1.0 | -1.0 | -1.0 | 10.0 |
| 81 | ICMP Type | 547557.0 | -0.9984439976112076 | 0.09361519910214584 | -1.0 | -1.0 | -1.0 | -1.0 | 8.0 |
| 82 | Total TCP Flow Time | 547557.0 | 15616638.244661286 | 189945250.3041776 | 0.0 | 0.0 | 48.0 | 4507917.0 | 26760499117.0 |

## Distribution Analysis
 Distribution of target variable 'Label':

Distribution Analysis

| # | Class | Percentage |
|---|---|---|
| 1 | BENIGN | 0.5270 |
| 2 | Botnet | 0.0013 |
| 3 | Botnet - Attempted | 0.0074 |
| 4 | DDoS | 0.1738 |
| 5 | Portscan | 0.2905 |

## Recommended Columns and Mapping  
 The following columns are available after cleaning.
Recommended mapping:
| # | Column Name | Mapping |
|---|---|---|
| 1 | Dst Port | dst_port |
| 2 | Flow Duration | flow_duration |
| 3 | Total Fwd Packet | total_fwd_packet |
| 4 | Total Length of Fwd Packet | total_length_of_fwd_packet |
| 5 | Fwd Packet Length Max | fwd_packet_length_max |
| 6 | Fwd Packet Length Min | fwd_packet_length_min |
| 7 | Fwd Packet Length Mean | fwd_packet_length_mean |
| 8 | Fwd Packet Length Std | fwd_packet_length_std |
| 9 | Bwd Packet Length Max | bwd_packet_length_max |
| 10 | Bwd Packet Length Min | bwd_packet_length_min |
| 11 | Flow Bytes/s | flow_bytes/s |
| 12 | Flow Packets/s | flow_packets/s |
| 13 | Flow IAT Mean | flow_iat_mean |
| 14 | Flow IAT Std | flow_iat_std |
| 15 | Flow IAT Max | flow_iat_max |
| 16 | Flow IAT Min | flow_iat_min |
| 17 | Fwd IAT Std | fwd_iat_std |
| 18 | Bwd IAT Std | bwd_iat_std |
| 19 | Fwd PSH Flags | fwd_psh_flags |
| 20 | Bwd PSH Flags | bwd_psh_flags |
| 21 | Fwd RST Flags | fwd_rst_flags |
| 22 | Bwd RST Flags | bwd_rst_flags |
| 23 | Fwd Header Length | fwd_header_length |
| 24 | Bwd Header Length | bwd_header_length |
| 25 | Bwd Packets/s | bwd_packets/s |
| 26 | Packet Length Min | packet_length_min |
| 27 | FIN Flag Count | fin_flag_count |
| 28 | SYN Flag Count | syn_flag_count |
| 29 | RST Flag Count | rst_flag_count |
| 30 | CWR Flag Count | cwr_flag_count |
| 31 | ECE Flag Count | ece_flag_count |
| 32 | Down/Up Ratio | down/up_ratio |
| 33 | Fwd Bytes/Bulk Avg | fwd_bytes/bulk_avg |
| 34 | Fwd Packet/Bulk Avg | fwd_packet/bulk_avg |
| 35 | Fwd Bulk Rate Avg | fwd_bulk_rate_avg |
| 36 | Bwd Bytes/Bulk Avg | bwd_bytes/bulk_avg |
| 37 | Bwd Bulk Rate Avg | bwd_bulk_rate_avg |
| 38 | Subflow Fwd Packets | subflow_fwd_packets |
| 39 | Subflow Bwd Packets | subflow_bwd_packets |
| 40 | FWD Init Win Bytes | fwd_init_win_bytes |
| 41 | Bwd Init Win Bytes | bwd_init_win_bytes |
| 42 | Fwd Act Data Pkts | fwd_act_data_pkts |
| 43 | Fwd Seg Size Min | fwd_seg_size_min |
| 44 | Active Mean | active_mean |
| 45 | Active Std | active_std |
| 46 | Active Max | active_max |
| 47 | Active Min | active_min |
| 48 | Idle Std | idle_std |
| 49 | ICMP Code | icmp_code |
| 50 | ICMP Type | icmp_type |
| 51 | Total TCP Flow Time | total_tcp_flow_time |

## Recommendation
 Based on the assessment, it is recommended to continue working with the available columns. You may consider the following:
- Performing further analysis using the available columns: `['Dst Port', 'Flow Duration', 'Total Fwd Packet', 'Total Length of Fwd Packet', 'Fwd Packet Length Max', 'Fwd Packet Length Min', 'Fwd Packet Length Mean', 'Fwd Packet Length Std', 'Bwd Packet Length Max', 'Bwd Packet Length Min', 'Flow Bytes/s', 'Flow Packets/s', 'Flow IAT Mean', 'Flow IAT Std', 'Flow IAT Max', 'Flow IAT Min', 'Fwd IAT Std', 'Bwd IAT Std', 'Fwd PSH Flags', 'Bwd PSH Flags', 'Fwd RST Flags', 'Bwd RST Flags', 'Fwd Header Length', 'Bwd Header Length', 'Bwd Packets/s', 'Packet Length Min', 'FIN Flag Count', 'SYN Flag Count', 'RST Flag Count', 'CWR Flag Count', 'ECE Flag Count', 'Down/Up Ratio', 'Fwd Bytes/Bulk Avg', 'Fwd Packet/Bulk Avg', 'Fwd Bulk Rate Avg', 'Bwd Bytes/Bulk Avg', 'Bwd Bulk Rate Avg', 'Subflow Fwd Packets', 'Subflow Bwd Packets', 'FWD Init Win Bytes', 'Bwd Init Win Bytes', 'Fwd Act Data Pkts', 'Fwd Seg Size Min', 'Active Mean', 'Active Std', 'Active Max', 'Active Min', 'Idle Std', 'ICMP Code', 'ICMP Type', 'Total TCP Flow Time']`
- Train machine learning models with the reduced feature set.
## End of Report ✅  
 
✅ Report Successfully Generated in  00:22 minutes

