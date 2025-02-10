# Data Assessment Report on dataset: wednesday.csv
## Command line executed  
 ```dataset_assessment_prepare.py --drop-columns id,Protocol,Attempted Category,Src Port --drop-highly-correlated --correlation-threshold 0.95 --drop-categorical-columns --impute-strategy mean --assess-only --zero-variance --low-variance-threshold=0.01 --low-variance-sample-percentage=100 --missing-threshold=0.05 --descriptive-statistics --distribution-analysis --distribution-column Label -output . -input CICIDS2017_improved/wednesday.csv```  
# Report  
 ### Options used to generate this report  

| # | Option | Value |
|---|---|---|
| 1 | -input | CICIDS2017_improved/wednesday.csv |
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
 
✅ Dataset Loaded Successfully: `.../DATASET_engelen_improved/CICIDS2017_improved/wednesday.csv
- File Size: 277.80 MB
- Number of Records: 496,641
- File loaded in 00:09 minutes

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
 Found 993386 negative values:

### Columns with Negative Values

| # | Column | Negative Count |
|---|---|---|
| 1 | Fwd Header Length | 64 |
| 2 | Bwd Header Length | 88 |
| 3 | ICMP Code | 496617 |
| 4 | ICMP Type | 496617 |

💡 To replace with zero, use:
```python
df_numeric.loc[:, df_numeric.columns] = np.where(df_numeric < 0, 0, df_numeric)
```
## Infinite Values ⚠️ 
 Found 2 infinite values:

### Columns with Infinite Values

| # | Column | Infinite Count |
|---|---|---|
| 1 | Flow Bytes/s | 1 |
| 2 | Flow Packets/s | 1 |

💡 To replace with NaN, use:
```python
df_numeric.replace([np.inf, -np.inf], np.nan, inplace=True)
```
## Missing Values ✅  
 No columns to drop, max missing =  0.0% and that's below threshold 0.05%
## Impute Missing Values ✅  
 No issues found
## Highly Correlated Features ⚠️  
 ️Found 27 highly correlated features (threshold: 0.95):

### Highly Correlated Features

| # | Feature 1 | Feature 2 | Correlation |
|---|---|---|---|
| 1 | Total Bwd packets | Total Fwd Packet | 0.9989 |
| 2 | Total Length of Bwd Packet | Total Fwd Packet | 0.9959 |
| 3 | Total Length of Bwd Packet | Total Bwd packets | 0.9926 |
| 4 | Bwd Packet Length Mean | Bwd Packet Length Max | 0.9513 |
| 5 | Bwd Packet Length Std | Bwd Packet Length Max | 0.9859 |
| 6 | Fwd IAT Total | Flow Duration | 0.9995 |
| 7 | Fwd IAT Mean | Flow IAT Mean | 0.9520 |
| 8 | Fwd IAT Max | Flow IAT Max | 0.9992 |
| 9 | Fwd IAT Min | Fwd IAT Mean | 0.9515 |
| 10 | Bwd IAT Total | Flow Duration | 0.9710 |
| 11 | Bwd IAT Total | Fwd IAT Total | 0.9706 |
| 12 | Bwd IAT Min | Fwd IAT Min | 0.9559 |
| 13 | Fwd Packets/s | Flow Packets/s | 0.9923 |
| 14 | Packet Length Max | Bwd Packet Length Max | 0.9948 |
| 15 | Packet Length Max | Bwd Packet Length Std | 0.9807 |
| 16 | Packet Length Mean | Bwd Packet Length Mean | 0.9779 |
| 17 | Packet Length Std | Bwd Packet Length Max | 0.9862 |
| 18 | Packet Length Std | Bwd Packet Length Mean | 0.9698 |
| 19 | Packet Length Std | Bwd Packet Length Std | 0.9871 |
| 20 | Packet Length Std | Packet Length Max | 0.9883 |
| 21 | Packet Length Std | Packet Length Mean | 0.9532 |
| 22 | Packet Length Variance | Bwd Packet Length Std | 0.9695 |
| 23 | RST Flag Count | Fwd RST Flags | 0.9772 |
| 24 | PSH Flag Count | Bwd PSH Flags | 0.9864 |
| 25 | ACK Flag Count | Total Fwd Packet | 0.9996 |
| 26 | ACK Flag Count | Total Bwd packets | 0.9998 |
| 27 | ACK Flag Count | Total Length of Bwd Packet | 0.9943 |
| 28 | Average Packet Size | Bwd Packet Length Mean | 0.9779 |
| 29 | Average Packet Size | Packet Length Mean | 1.0000 |
| 30 | Average Packet Size | Packet Length Std | 0.9532 |
| 31 | Fwd Segment Size Avg | Fwd Packet Length Mean | 1.0000 |
| 32 | Bwd Segment Size Avg | Bwd Packet Length Max | 0.9513 |
| 33 | Bwd Segment Size Avg | Bwd Packet Length Mean | 1.0000 |
| 34 | Bwd Segment Size Avg | Packet Length Mean | 0.9779 |
| 35 | Bwd Segment Size Avg | Packet Length Std | 0.9698 |
| 36 | Bwd Segment Size Avg | Average Packet Size | 0.9779 |
| 37 | Bwd Packet/Bulk Avg | Bwd Bytes/Bulk Avg | 0.9857 |
| 38 | Subflow Fwd Bytes | Fwd Packet Length Mean | 0.9745 |
| 39 | Subflow Fwd Bytes | Fwd Segment Size Avg | 0.9745 |
| 40 | Subflow Bwd Bytes | Bwd Packet Length Mean | 0.9836 |
| 41 | Subflow Bwd Bytes | Packet Length Mean | 0.9932 |
| 42 | Subflow Bwd Bytes | Average Packet Size | 0.9932 |
| 43 | Subflow Bwd Bytes | Bwd Segment Size Avg | 0.9836 |
| 44 | Idle Mean | Flow IAT Max | 0.9731 |
| 45 | Idle Mean | Fwd IAT Max | 0.9724 |
| 46 | Idle Max | Flow IAT Max | 0.9989 |
| 47 | Idle Max | Fwd IAT Max | 0.9981 |
| 48 | Idle Max | Idle Mean | 0.9742 |
| 49 | Idle Min | Idle Mean | 0.9837 |

💡 To drop these features, use:
```python
df_numeric.drop(columns=['Total Bwd packets', 'Total Length of Bwd Packet', 'Bwd Packet Length Mean', 'Bwd Packet Length Std', 'Fwd IAT Total', 'Fwd IAT Mean', 'Fwd IAT Max', 'Fwd IAT Min', 'Bwd IAT Total', 'Bwd IAT Min', 'Fwd Packets/s', 'Packet Length Max', 'Packet Length Mean', 'Packet Length Std', 'Packet Length Variance', 'RST Flag Count', 'PSH Flag Count', 'ACK Flag Count', 'Average Packet Size', 'Fwd Segment Size Avg', 'Bwd Segment Size Avg', 'Bwd Packet/Bulk Avg', 'Subflow Fwd Bytes', 'Subflow Bwd Bytes', 'Idle Mean', 'Idle Max', 'Idle Min'], inplace=True)
```
## Descriptive Statistics Analysis
 Descriptive Statistics for Features

| # | Column | Count | Mean | Std | Min | 25% | 50% | 75% | Max |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Dst Port | 496641.0 | 210.46643954083532 | 1904.3971983672004 | 0.0 | 53.0 | 80.0 | 80.0 | 65178.0 |
| 2 | Flow Duration | 496641.0 | 12102380.054566579 | 30782109.433359843 | 0.0 | 30481.0 | 155987.0 | 1271785.0 | 119999998.0 |
| 3 | Total Fwd Packet | 496641.0 | 13.214074150140645 | 882.425161904443 | 0.0 | 2.0 | 6.0 | 9.0 | 203943.0 |
| 4 | Total Bwd packets | 496641.0 | 14.454668462732638 | 1162.332721211793 | 0.0 | 2.0 | 5.0 | 7.0 | 272354.0 |
| 5 | Total Length of Fwd Packet | 496641.0 | 622.4366574648488 | 4791.59255145879 | 0.0 | 70.0 | 308.0 | 377.0 | 819734.0 |
| 6 | Total Length of Bwd Packet | 496641.0 | 23811.998332799747 | 2646550.58566399 | 0.0 | 158.0 | 859.0 | 11595.0 | 627046403.0 |
| 7 | Fwd Packet Length Max | 496641.0 | 270.2194965780111 | 450.0588171788912 | 0.0 | 42.0 | 202.0 | 359.0 | 24820.0 |
| 8 | Fwd Packet Length Min | 496641.0 | 18.12872275949831 | 33.075493966819884 | 0.0 | 0.0 | 0.0 | 38.0 | 1472.0 |
| 9 | Fwd Packet Length Mean | 496641.0 | 57.064298649892145 | 81.41243819148792 | 0.0 | 36.44444444444444 | 44.5 | 53.85714285714286 | 4503.205882352941 |
| 10 | Fwd Packet Length Std | 496641.0 | 86.43472891875956 | 141.6436178270473 | 0.0 | 0.0 | 76.55060962091244 | 131.15367213420186 | 6381.628607463828 |
| 11 | Bwd Packet Length Max | 496641.0 | 2363.242680326433 | 2845.3563890179094 | 0.0 | 98.0 | 566.0 | 4344.0 | 19530.0 |
| 12 | Bwd Packet Length Min | 496641.0 | 45.934485876115744 | 71.04135574107141 | 0.0 | 0.0 | 0.0 | 87.0 | 1983.0 |
| 13 | Bwd Packet Length Mean | 496641.0 | 763.1185489600668 | 842.7027192970056 | 0.0 | 90.0 | 207.0 | 1656.4285714285716 | 4370.686524002315 |
| 14 | Bwd Packet Length Std | 496641.0 | 930.4428708428895 | 1202.6829732118567 | 0.0 | 0.0 | 210.60769216721408 | 1762.5 | 6715.738331213727 |
| 15 | Flow Bytes/s | 496640.0 | 469842.5343060821 | 3718433.1452481663 | 0.0 | 1406.4153887112313 | 11979.003203497172 | 142400.03331388492 | 253000000.0 |
| 16 | Flow Packets/s | 496640.0 | 5552.093795544168 | 40618.5288439671 | 0.0250043192877876 | 10.243621238315496 | 75.00796959676967 | 199.95517671830066 | 2000000.0 |
| 17 | Flow IAT Mean | 496641.0 | 891049.6942753461 | 3606118.5796586275 | 0.0 | 5453.727272727273 | 16100.299999999996 | 126209.0 | 64161599.0 |
| 18 | Flow IAT Std | 496641.0 | 1762144.310044894 | 6306002.826658191 | 0.0 | 140.8734656822687 | 34919.641304581855 | 275668.54237755184 | 84798440.76644637 |
| 19 | Flow IAT Max | 496641.0 | 5033592.821875359 | 15343914.125990646 | 0.0 | 23868.0 | 120044.0 | 998968.0 | 119946338.0 |
| 20 | Flow IAT Min | 496641.0 | 46792.103195265794 | 1224549.408959377 | 0.0 | 1.0 | 3.0 | 15.0 | 64161599.0 |
| 21 | Fwd IAT Total | 496641.0 | 12044474.57237119 | 30755708.319638696 | 0.0 | 3.0 | 117985.0 | 1200934.0 | 119999998.0 |
| 22 | Fwd IAT Mean | 496641.0 | 1949093.7927243575 | 9469171.729458086 | 0.0 | 3.0 | 17792.4 | 155816.15384615384 | 119979271.0 |
| 23 | Fwd IAT Std | 496641.0 | 1505120.7487332807 | 5076671.4962293785 | 0.0 | 0.0 | 20380.75318366162 | 266404.16553471907 | 82774583.071858 |
| 24 | Fwd IAT Max | 496641.0 | 5012586.583991253 | 15345234.10816658 | 0.0 | 3.0 | 71010.0 | 998938.0 | 119987035.0 |
| 25 | Fwd IAT Min | 496641.0 | 1054170.5131775266 | 9077727.402288789 | 0.0 | 1.0 | 3.0 | 25.0 | 119979271.0 |
| 26 | Bwd IAT Total | 496641.0 | 11071979.49586925 | 30062168.66259845 | 0.0 | 3.0 | 51496.0 | 439010.0 | 119999992.0 |
| 27 | Bwd IAT Mean | 496641.0 | 2193236.520850151 | 10124828.389806638 | 0.0 | 3.0 | 9509.2 | 72572.8 | 119925316.0 |
| 28 | Bwd IAT Std | 496641.0 | 1389985.9604967409 | 5628221.453160246 | 0.0 | 0.0 | 6310.923300497472 | 76998.90102079844 | 82881543.57911418 |
| 29 | Bwd IAT Max | 496641.0 | 4498315.007995715 | 14978192.086576892 | 0.0 | 3.0 | 33238.0 | 232544.0 | 119926071.0 |
| 30 | Bwd IAT Min | 496641.0 | 1258717.1134602258 | 9277479.274423953 | 0.0 | 3.0 | 14.0 | 49.0 | 119925316.0 |
| 31 | Fwd PSH Flags | 496641.0 | 1.4569759645297107 | 3.928717842292443 | 0.0 | 0.0 | 1.0 | 1.0 | 641.0 |
| 32 | Bwd PSH Flags | 496641.0 | 1.6773403726232832 | 20.89775468090842 | 0.0 | 0.0 | 1.0 | 1.0 | 4619.0 |
| 33 | Fwd URG Flags | 496641.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| 34 | Bwd URG Flags | 496641.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| 35 | Fwd RST Flags | 496641.0 | 0.6612845093337039 | 1.0535757720918284 | 0.0 | 0.0 | 0.0 | 1.0 | 139.0 |
| 36 | Bwd RST Flags | 496641.0 | 0.034999124115810014 | 0.22634391217046892 | 0.0 | 0.0 | 0.0 | 0.0 | 11.0 |
| 37 | Fwd Header Length | 496641.0 | 208.90247079882653 | 627.0641878572027 | -32572.0 | 16.0 | 192.0 | 264.0 | 32740.0 |
| 38 | Bwd Header Length | 496641.0 | 197.9271304624467 | 766.1334559590949 | -32480.0 | 16.0 | 148.0 | 232.0 | 32584.0 |
| 39 | Fwd Packets/s | 496641.0 | 3874.9794460783837 | 39847.910229685265 | 0.0 | 5.449591280653952 | 39.41663381947182 | 113.0678124204992 | 2000000.0 |
| 40 | Bwd Packets/s | 496641.0 | 1677.1031701757224 | 5050.667737133491 | 0.0 | 4.008996187444626 | 32.97826732183491 | 85.42523461430507 | 666666.6666666666 |
| 41 | Packet Length Min | 496641.0 | 17.754434289557246 | 24.573142798715278 | 0.0 | 0.0 | 0.0 | 38.0 | 1408.0 |
| 42 | Packet Length Max | 496641.0 | 2396.493239583522 | 2842.4064305948996 | 0.0 | 100.0 | 796.0 | 4344.0 | 24820.0 |
| 43 | Packet Length Mean | 496641.0 | 373.3395903391124 | 369.48518787244075 | 0.0 | 67.0 | 139.5 | 796.4 | 1891.764705882353 |
| 44 | Packet Length Std | 496641.0 | 718.4806630576811 | 832.3582234361737 | 0.0 | 34.06366588218792 | 233.30833313160483 | 1499.291798628905 | 4302.185607539291 |
| 45 | Packet Length Variance | 496641.0 | 1209033.2802975127 | 1903606.8423372167 | 0.0 | 1160.3333333333333 | 54432.77830864789 | 2247875.897435897 | 18508801.00171821 |
| 46 | FIN Flag Count | 496641.0 | 0.8818301348458947 | 0.9532027357114239 | 0.0 | 0.0 | 1.0 | 2.0 | 36.0 |
| 47 | SYN Flag Count | 496641.0 | 1.2260002698126011 | 1.1971700883471987 | 0.0 | 0.0 | 2.0 | 2.0 | 13.0 |
| 48 | RST Flag Count | 496641.0 | 0.6962977281376286 | 1.0658804647308677 | 0.0 | 0.0 | 0.0 | 1.0 | 139.0 |
| 49 | PSH Flag Count | 496641.0 | 3.1343163371529936 | 22.525695395362497 | 0.0 | 0.0 | 2.0 | 2.0 | 4734.0 |
| 50 | ACK Flag Count | 496641.0 | 24.958130722191683 | 2044.2233804097136 | 0.0 | 0.0 | 10.0 | 13.0 | 474809.0 |
| 51 | URG Flag Count | 496641.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| 52 | CWR Flag Count | 496641.0 | 0.0006100986426815345 | 0.030195318994936937 | 0.0 | 0.0 | 0.0 | 0.0 | 4.0 |
| 53 | ECE Flag Count | 496641.0 | 0.0009161547274590701 | 0.04248879735993194 | 0.0 | 0.0 | 0.0 | 0.0 | 2.0 |
| 54 | Down/Up Ratio | 496641.0 | 0.8864888931448183 | 0.22944666566440375 | 0.0 | 0.7777777777777778 | 1.0 | 1.0 | 6.0 |
| 55 | Average Packet Size | 496641.0 | 373.3395903391124 | 369.48518787244075 | 0.0 | 67.0 | 139.5 | 796.4 | 1891.764705882353 |
| 56 | Fwd Segment Size Avg | 496641.0 | 57.064298649892145 | 81.41243819148792 | 0.0 | 36.44444444444444 | 44.5 | 53.85714285714285 | 4503.205882352941 |
| 57 | Bwd Segment Size Avg | 496641.0 | 763.1185489600668 | 842.7027192970055 | 0.0 | 90.0 | 207.0 | 1656.428571428571 | 4370.6865240023135 |
| 58 | Fwd Bytes/Bulk Avg | 496641.0 | 70.17570438203853 | 1263.6687281250624 | 0.0 | 0.0 | 0.0 | 0.0 | 351373.0 |
| 59 | Fwd Packet/Bulk Avg | 496641.0 | 0.22337865782325664 | 1.3935325542604442 | 0.0 | 0.0 | 0.0 | 0.0 | 84.0 |
| 60 | Fwd Bulk Rate Avg | 496641.0 | 166568.02961495327 | 4047150.260705665 | 0.0 | 0.0 | 0.0 | 0.0 | 791297297.0 |
| 61 | Bwd Bytes/Bulk Avg | 496641.0 | 5314.51369500303 | 284542.3205273203 | 0.0 | 0.0 | 0.0 | 11595.0 | 156761511.0 |
| 62 | Bwd Packet/Bulk Avg | 496641.0 | 2.365485330449963 | 96.36078767464008 | 0.0 | 0.0 | 0.0 | 4.0 | 45977.0 |
| 63 | Bwd Bulk Rate Avg | 496641.0 | 8241718.353414237 | 15628222.276201863 | 0.0 | 0.0 | 0.0 | 2124924.0 | 735833333.0 |
| 64 | Subflow Fwd Packets | 496641.0 | 0.015286696023888482 | 0.12269084423162492 | 0.0 | 0.0 | 0.0 | 0.0 | 1.0 |
| 65 | Subflow Fwd Bytes | 496641.0 | 30.21002293407109 | 42.87401614927203 | 0.0 | 19.0 | 23.0 | 28.0 | 1578.0 |
| 66 | Subflow Bwd Packets | 496641.0 | 2.8189376229509848e-05 | 0.0053092973496648745 | 0.0 | 0.0 | 0.0 | 0.0 | 1.0 |
| 67 | Subflow Bwd Bytes | 496641.0 | 342.4587096111678 | 367.3339483714307 | 0.0 | 43.0 | 101.0 | 773.0 | 1891.0 |
| 68 | FWD Init Win Bytes | 496641.0 | 14558.015169911465 | 14898.596275645854 | 0.0 | 0.0 | 8192.0 | 29200.0 | 65535.0 |
| 69 | Bwd Init Win Bytes | 496641.0 | 691.7101085089632 | 4140.3807992538195 | 0.0 | 0.0 | 114.0 | 235.0 | 65535.0 |
| 70 | Fwd Act Data Pkts | 496641.0 | 2.1246071105688014 | 4.727932088667993 | 0.0 | 1.0 | 1.0 | 2.0 | 641.0 |
| 71 | Fwd Seg Size Min | 496641.0 | 18.186521048403172 | 9.936088230580198 | 0.0 | 8.0 | 20.0 | 32.0 | 44.0 |
| 72 | Active Mean | 496641.0 | 150384.65512806168 | 904131.3541078467 | 0.0 | 0.0 | 0.0 | 0.0 | 100242139.0 |
| 73 | Active Std | 496641.0 | 77822.726095827 | 592148.0257528282 | 0.0 | 0.0 | 0.0 | 0.0 | 74154397.74458432 |
| 74 | Active Max | 496641.0 | 257923.1335330752 | 1361889.9513125645 | 0.0 | 0.0 | 0.0 | 0.0 | 104988417.0 |
| 75 | Active Min | 496641.0 | 101851.0851681597 | 791655.0515378724 | 0.0 | 0.0 | 0.0 | 0.0 | 100242139.0 |
| 76 | Idle Mean | 496641.0 | 4340811.509554884 | 14287741.858314091 | 0.0 | 0.0 | 0.0 | 0.0 | 119946338.0 |
| 77 | Idle Std | 496641.0 | 472509.0720894523 | 3568528.216095083 | 0.0 | 0.0 | 0.0 | 0.0 | 76914831.60257196 |
| 78 | Idle Max | 496641.0 | 4805784.994529247 | 15397727.406731104 | 0.0 | 0.0 | 0.0 | 0.0 | 119946338.0 |
| 79 | Idle Min | 496641.0 | 3927899.2016386082 | 13932933.11384221 | 0.0 | 0.0 | 0.0 | 0.0 | 119946338.0 |
| 80 | ICMP Code | 496641.0 | -0.9998469719576112 | 0.02887175759275493 | -1.0 | -1.0 | -1.0 | -1.0 | 10.0 |
| 81 | ICMP Type | 496641.0 | -0.9997422685601873 | 0.0407318433035784 | -1.0 | -1.0 | -1.0 | -1.0 | 8.0 |
| 82 | Total TCP Flow Time | 496641.0 | 44104775.10888952 | 420398892.56307346 | 0.0 | 0.0 | 98046.0 | 1197722.0 | 30290439669.0 |

## Distribution Analysis
 Distribution of target variable 'Label':

Distribution Analysis

| # | Class | Percentage |
|---|---|---|
| 1 | BENIGN | 0.6426 |
| 2 | DoS GoldenEye | 0.0152 |
| 3 | DoS GoldenEye - Attempted | 0.0002 |
| 4 | DoS Hulk | 0.3191 |
| 5 | DoS Hulk - Attempted | 0.0012 |
| 6 | DoS Slowhttptest | 0.0035 |
| 7 | DoS Slowhttptest - Attempted | 0.0068 |
| 8 | DoS Slowloris | 0.0078 |
| 9 | DoS Slowloris - Attempted | 0.0037 |
| 10 | Heartbleed | 0.0000 |

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
| 18 | Bwd IAT Mean | bwd_iat_mean |
| 19 | Bwd IAT Std | bwd_iat_std |
| 20 | Bwd IAT Max | bwd_iat_max |
| 21 | Fwd PSH Flags | fwd_psh_flags |
| 22 | Bwd PSH Flags | bwd_psh_flags |
| 23 | Fwd RST Flags | fwd_rst_flags |
| 24 | Bwd RST Flags | bwd_rst_flags |
| 25 | Fwd Header Length | fwd_header_length |
| 26 | Bwd Header Length | bwd_header_length |
| 27 | Bwd Packets/s | bwd_packets/s |
| 28 | Packet Length Min | packet_length_min |
| 29 | FIN Flag Count | fin_flag_count |
| 30 | SYN Flag Count | syn_flag_count |
| 31 | CWR Flag Count | cwr_flag_count |
| 32 | ECE Flag Count | ece_flag_count |
| 33 | Down/Up Ratio | down/up_ratio |
| 34 | Fwd Bytes/Bulk Avg | fwd_bytes/bulk_avg |
| 35 | Fwd Packet/Bulk Avg | fwd_packet/bulk_avg |
| 36 | Fwd Bulk Rate Avg | fwd_bulk_rate_avg |
| 37 | Bwd Bytes/Bulk Avg | bwd_bytes/bulk_avg |
| 38 | Bwd Bulk Rate Avg | bwd_bulk_rate_avg |
| 39 | Subflow Fwd Packets | subflow_fwd_packets |
| 40 | Subflow Bwd Packets | subflow_bwd_packets |
| 41 | FWD Init Win Bytes | fwd_init_win_bytes |
| 42 | Bwd Init Win Bytes | bwd_init_win_bytes |
| 43 | Fwd Act Data Pkts | fwd_act_data_pkts |
| 44 | Fwd Seg Size Min | fwd_seg_size_min |
| 45 | Active Mean | active_mean |
| 46 | Active Std | active_std |
| 47 | Active Max | active_max |
| 48 | Active Min | active_min |
| 49 | Idle Std | idle_std |
| 50 | ICMP Code | icmp_code |
| 51 | ICMP Type | icmp_type |
| 52 | Total TCP Flow Time | total_tcp_flow_time |

## Recommendation
 Based on the assessment, it is recommended to continue working with the available columns. You may consider the following:
- Performing further analysis using the available columns: `['Dst Port', 'Flow Duration', 'Total Fwd Packet', 'Total Length of Fwd Packet', 'Fwd Packet Length Max', 'Fwd Packet Length Min', 'Fwd Packet Length Mean', 'Fwd Packet Length Std', 'Bwd Packet Length Max', 'Bwd Packet Length Min', 'Flow Bytes/s', 'Flow Packets/s', 'Flow IAT Mean', 'Flow IAT Std', 'Flow IAT Max', 'Flow IAT Min', 'Fwd IAT Std', 'Bwd IAT Mean', 'Bwd IAT Std', 'Bwd IAT Max', 'Fwd PSH Flags', 'Bwd PSH Flags', 'Fwd RST Flags', 'Bwd RST Flags', 'Fwd Header Length', 'Bwd Header Length', 'Bwd Packets/s', 'Packet Length Min', 'FIN Flag Count', 'SYN Flag Count', 'CWR Flag Count', 'ECE Flag Count', 'Down/Up Ratio', 'Fwd Bytes/Bulk Avg', 'Fwd Packet/Bulk Avg', 'Fwd Bulk Rate Avg', 'Bwd Bytes/Bulk Avg', 'Bwd Bulk Rate Avg', 'Subflow Fwd Packets', 'Subflow Bwd Packets', 'FWD Init Win Bytes', 'Bwd Init Win Bytes', 'Fwd Act Data Pkts', 'Fwd Seg Size Min', 'Active Mean', 'Active Std', 'Active Max', 'Active Min', 'Idle Std', 'ICMP Code', 'ICMP Type', 'Total TCP Flow Time']`
- Train machine learning models with the reduced feature set.
## End of Report ✅  
 
✅ Report Successfully Generated in  00:20 minutes

