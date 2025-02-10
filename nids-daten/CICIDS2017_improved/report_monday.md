# Data Assessment Report on dataset: monday.csv
## Command line executed  
 ```dataset_assessment_prepare.py --drop-columns id,Protocol,Attempted Category,Src Port --drop-highly-correlated --correlation-threshold 0.95 --drop-categorical-columns --impute-strategy mean --assess-only --zero-variance --low-variance-threshold=0.01 --low-variance-sample-percentage=100 --missing-threshold=0.05 --descriptive-statistics --distribution-analysis --distribution-column Label -output . -input CICIDS2017_improved/monday.csv```  
# Report  
 ### Options used to generate this report  

| # | Option | Value |
|---|---|---|
| 1 | -input | CICIDS2017_improved/monday.csv |
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
 
✅ Dataset Loaded Successfully: `.../DATASET_engelen_improved/CICIDS2017_improved/monday.csv
- File Size: 198.25 MB
- Number of Records: 371,624
- File loaded in 00:10 minutes

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
 Found 743195 negative values:

### Columns with Negative Values

| # | Column | Negative Count |
|---|---|---|
| 1 | Fwd Header Length | 46 |
| 2 | Bwd Header Length | 85 |
| 3 | ICMP Code | 371532 |
| 4 | ICMP Type | 371532 |

💡 To replace with zero, use:
```python
df_numeric.loc[:, df_numeric.columns] = np.where(df_numeric < 0, 0, df_numeric)
```
## Infinite Values ⚠️ 
 Found 6 infinite values:

### Columns with Infinite Values

| # | Column | Infinite Count |
|---|---|---|
| 1 | Flow Bytes/s | 3 |
| 2 | Flow Packets/s | 3 |

💡 To replace with NaN, use:
```python
df_numeric.replace([np.inf, -np.inf], np.nan, inplace=True)
```
## Missing Values ✅  
 No columns to drop, max missing =  0.0% and that's below threshold 0.05%
## Impute Missing Values ✅  
 No issues found
## Highly Correlated Features ⚠️  
 ️Found 26 highly correlated features (threshold: 0.95):

### Highly Correlated Features

| # | Feature 1 | Feature 2 | Correlation |
|---|---|---|---|
| 1 | Total Bwd packets | Total Fwd Packet | 0.9993 |
| 2 | Total Length of Bwd Packet | Total Fwd Packet | 0.9990 |
| 3 | Total Length of Bwd Packet | Total Bwd packets | 0.9973 |
| 4 | Fwd Packet Length Std | Fwd Packet Length Max | 0.9521 |
| 5 | Fwd IAT Total | Flow Duration | 0.9994 |
| 6 | Fwd IAT Max | Flow IAT Max | 0.9981 |
| 7 | Fwd IAT Min | Fwd IAT Mean | 0.9731 |
| 8 | Bwd IAT Total | Flow Duration | 0.9829 |
| 9 | Bwd IAT Total | Fwd IAT Total | 0.9824 |
| 10 | Bwd IAT Mean | Flow IAT Std | 0.9632 |
| 11 | Bwd IAT Std | Fwd IAT Std | 0.9548 |
| 12 | Bwd IAT Max | Flow IAT Max | 0.9575 |
| 13 | Bwd IAT Max | Fwd IAT Max | 0.9556 |
| 14 | Bwd IAT Min | Bwd IAT Mean | 0.9653 |
| 15 | Fwd Packets/s | Flow Packets/s | 0.9874 |
| 16 | Packet Length Mean | Bwd Packet Length Mean | 0.9530 |
| 17 | Packet Length Std | Packet Length Max | 0.9626 |
| 18 | RST Flag Count | Fwd RST Flags | 0.9692 |
| 19 | PSH Flag Count | Bwd PSH Flags | 0.9843 |
| 20 | ACK Flag Count | Total Fwd Packet | 0.9998 |
| 21 | ACK Flag Count | Total Bwd packets | 0.9999 |
| 22 | ACK Flag Count | Total Length of Bwd Packet | 0.9982 |
| 23 | Average Packet Size | Bwd Packet Length Mean | 0.9530 |
| 24 | Average Packet Size | Packet Length Mean | 1.0000 |
| 25 | Fwd Segment Size Avg | Fwd Packet Length Mean | 1.0000 |
| 26 | Bwd Segment Size Avg | Bwd Packet Length Mean | 1.0000 |
| 27 | Bwd Segment Size Avg | Packet Length Mean | 0.9530 |
| 28 | Bwd Segment Size Avg | Average Packet Size | 0.9530 |
| 29 | Bwd Packet/Bulk Avg | Bwd Bytes/Bulk Avg | 0.9967 |
| 30 | Subflow Fwd Bytes | Fwd Packet Length Mean | 0.9786 |
| 31 | Subflow Fwd Bytes | Fwd Segment Size Avg | 0.9786 |
| 32 | Subflow Bwd Bytes | Bwd Packet Length Mean | 0.9871 |
| 33 | Subflow Bwd Bytes | Packet Length Mean | 0.9597 |
| 34 | Subflow Bwd Bytes | Average Packet Size | 0.9597 |
| 35 | Subflow Bwd Bytes | Bwd Segment Size Avg | 0.9871 |
| 36 | Idle Mean | Flow IAT Max | 0.9887 |
| 37 | Idle Mean | Fwd IAT Max | 0.9868 |
| 38 | Idle Max | Flow IAT Max | 0.9988 |
| 39 | Idle Max | Fwd IAT Max | 0.9969 |
| 40 | Idle Max | Bwd IAT Max | 0.9562 |
| 41 | Idle Max | Idle Mean | 0.9899 |
| 42 | Idle Min | Flow IAT Max | 0.9603 |
| 43 | Idle Min | Fwd IAT Max | 0.9583 |
| 44 | Idle Min | Idle Mean | 0.9899 |
| 45 | Idle Min | Idle Max | 0.9614 |

💡 To drop these features, use:
```python
df_numeric.drop(columns=['Total Bwd packets', 'Total Length of Bwd Packet', 'Fwd Packet Length Std', 'Fwd IAT Total', 'Fwd IAT Max', 'Fwd IAT Min', 'Bwd IAT Total', 'Bwd IAT Mean', 'Bwd IAT Std', 'Bwd IAT Max', 'Bwd IAT Min', 'Fwd Packets/s', 'Packet Length Mean', 'Packet Length Std', 'RST Flag Count', 'PSH Flag Count', 'ACK Flag Count', 'Average Packet Size', 'Fwd Segment Size Avg', 'Bwd Segment Size Avg', 'Bwd Packet/Bulk Avg', 'Subflow Fwd Bytes', 'Subflow Bwd Bytes', 'Idle Mean', 'Idle Max', 'Idle Min'], inplace=True)
```
## Descriptive Statistics Analysis
 Descriptive Statistics for Features

| # | Column | Count | Mean | Std | Min | 25% | 50% | 75% | Max |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Dst Port | 371624.0 | 261.70207521580954 | 1934.6941687827211 | 0.0 | 53.0 | 53.0 | 443.0 | 65490.0 |
| 2 | Flow Duration | 371624.0 | 14845455.541006502 | 33473900.635717425 | 0.0 | 24239.0 | 77431.5 | 5321639.25 | 119999987.0 |
| 3 | Total Fwd Packet | 371624.0 | 14.638656276236196 | 1065.6366704881127 | 0.0 | 2.0 | 2.0 | 10.0 | 219759.0 |
| 4 | Total Bwd packets | 371624.0 | 16.7414375820722 | 1401.0758345125878 | 0.0 | 2.0 | 2.0 | 8.0 | 291922.0 |
| 5 | Total Length of Fwd Packet | 371624.0 | 697.067108152326 | 3892.0291961829603 | 0.0 | 64.0 | 90.0 | 599.0 | 908786.0 |
| 6 | Total Length of Bwd Packet | 371624.0 | 25530.415140034012 | 3194839.3965161843 | 0.0 | 126.0 | 233.0 | 1156.0 | 655452323.0 |
| 7 | Fwd Packet Length Max | 371624.0 | 263.3010865821368 | 512.8884968326222 | 0.0 | 38.0 | 48.0 | 389.0 | 23360.0 |
| 8 | Fwd Packet Length Min | 371624.0 | 27.066785245301702 | 38.39810814540332 | 0.0 | 0.0 | 33.0 | 44.0 | 1472.0 |
| 9 | Fwd Packet Length Mean | 371624.0 | 61.73750081315352 | 88.11389956652111 | 0.0 | 35.0 | 45.0 | 58.0 | 4613.126903553298 |
| 10 | Fwd Packet Length Std | 371624.0 | 73.51926925114937 | 158.47193598815852 | 0.0 | 0.0 | 0.0 | 107.2500782339292 | 7116.541297564128 |
| 11 | Bwd Packet Length Max | 371624.0 | 579.1465352076292 | 883.3332188947193 | 0.0 | 83.0 | 136.0 | 805.0 | 13140.0 |
| 12 | Bwd Packet Length Min | 371624.0 | 69.5615783695348 | 79.7258752057222 | 0.0 | 0.0 | 62.0 | 112.0 | 1550.0 |
| 13 | Bwd Packet Length Mean | 371624.0 | 214.62452914968026 | 282.17684954917286 | 0.0 | 71.55555555555556 | 116.0 | 218.55 | 2976.3168807752977 |
| 14 | Bwd Packet Length Std | 371624.0 | 180.37447344289043 | 301.96337983449104 | 0.0 | 0.0 | 0.0 | 300.0092855705827 | 2263.5626786108664 |
| 15 | Flow Bytes/s | 371621.0 | 531092.937644695 | 4181111.773755295 | 0.0 | 639.0600463739706 | 5099.122362593362 | 24831.373485345903 | 171166666.66666666 |
| 16 | Flow Packets/s | 371621.0 | 7070.574387464823 | 44654.57907944752 | 0.025002704459199 | 2.988720196388804 | 64.50017737548778 | 169.14749661705008 | 2000000.0 |
| 17 | Flow IAT Mean | 371624.0 | 1315311.005883881 | 5628265.877705251 | 0.0 | 6760.292410714286 | 26488.88461538462 | 362213.178125 | 64999977.0 |
| 18 | Flow IAT Std | 371624.0 | 2115401.4490601616 | 6994973.444590591 | 0.0 | 83.13843876330611 | 17918.642954569226 | 1250077.9193233668 | 84800261.56640792 |
| 19 | Flow IAT Max | 371624.0 | 6079831.614053451 | 16372753.951558812 | 0.0 | 23740.0 | 59739.0 | 4960291.0 | 119999735.0 |
| 20 | Flow IAT Min | 371624.0 | 285622.6446892558 | 4137481.2090499443 | 0.0 | 2.0 | 3.0 | 48.0 | 64999977.0 |
| 21 | Fwd IAT Total | 371624.0 | 14761331.736750048 | 33458147.283185042 | 0.0 | 3.0 | 48.0 | 5269124.5 | 119999987.0 |
| 22 | Fwd IAT Mean | 371624.0 | 2825824.5325415256 | 11899872.330144625 | 0.0 | 3.0 | 48.0 | 660687.0277777778 | 119987020.0 |
| 23 | Fwd IAT Std | 371624.0 | 1542897.907259012 | 4565395.5512879165 | 0.0 | 0.0 | 0.0 | 754294.8603279369 | 82800883.90858424 |
| 24 | Fwd IAT Max | 371624.0 | 6038365.503600413 | 16368164.430454895 | 0.0 | 3.0 | 48.0 | 4976842.25 | 119999869.0 |
| 25 | Fwd IAT Min | 371624.0 | 1896587.8098669623 | 11684309.966114508 | 0.0 | 1.0 | 3.0 | 48.0 | 119987020.0 |
| 26 | Bwd IAT Total | 371624.0 | 14201358.727966977 | 33085580.493101157 | 0.0 | 3.0 | 48.0 | 5093709.0 | 119999909.0 |
| 27 | Bwd IAT Mean | 371624.0 | 2711818.785951768 | 11321706.770195557 | 0.0 | 3.0 | 48.0 | 668393.9270833334 | 119974145.0 |
| 28 | Bwd IAT Std | 371624.0 | 1497433.635769299 | 4736293.066178646 | 0.0 | 0.0 | 0.0 | 142645.13161139167 | 84620454.91855389 |
| 29 | Bwd IAT Max | 371624.0 | 5659072.198539384 | 15848665.984376878 | 0.0 | 3.0 | 48.0 | 4901605.0 | 119974145.0 |
| 30 | Bwd IAT Min | 371624.0 | 1744951.0030245625 | 11030738.858366862 | 0.0 | 1.0 | 3.0 | 48.0 | 119974145.0 |
| 31 | Fwd PSH Flags | 371624.0 | 1.710519234495081 | 5.113421009730938 | 0.0 | 0.0 | 0.0 | 3.0 | 1105.0 |
| 32 | Bwd PSH Flags | 371624.0 | 2.1128882956967256 | 25.004270905276623 | 0.0 | 0.0 | 0.0 | 2.0 | 5099.0 |
| 33 | Fwd URG Flags | 371624.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| 34 | Bwd URG Flags | 371624.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| 35 | Fwd RST Flags | 371624.0 | 0.1710088691796009 | 0.8011906698905492 | 0.0 | 0.0 | 0.0 | 0.0 | 190.0 |
| 36 | Bwd RST Flags | 371624.0 | 0.031141691602264654 | 0.20550566329781123 | 0.0 | 0.0 | 0.0 | 0.0 | 12.0 |
| 37 | Fwd Header Length | 371624.0 | 193.57469915828904 | 705.9988089604567 | -32496.0 | 16.0 | 16.0 | 232.0 | 32652.0 |
| 38 | Bwd Header Length | 371624.0 | 195.79620261339417 | 886.144022601037 | -32764.0 | 16.0 | 16.0 | 200.0 | 32632.0 |
| 39 | Fwd Packets/s | 371624.0 | 4885.842244320896 | 43633.92376422578 | 0.0 | 1.6337951621767708 | 32.42226761339688 | 88.90140096660105 | 2000000.0 |
| 40 | Bwd Packets/s | 371624.0 | 2184.67506469054 | 7092.661272399948 | 0.0 | 1.2834525223349171 | 30.9060255968961 | 81.66348521891835 | 2000000.0 |
| 41 | Packet Length Min | 371624.0 | 26.58895281252018 | 26.815952683774157 | 0.0 | 0.0 | 33.0 | 44.0 | 1359.0 |
| 42 | Packet Length Max | 371624.0 | 629.5060948700838 | 944.0890968612831 | 0.0 | 84.0 | 138.0 | 1013.0 | 23360.0 |
| 43 | Packet Length Mean | 371624.0 | 139.09490668184338 | 164.91187282077786 | 0.0 | 59.0 | 82.5 | 142.0 | 1809.3060173261536 |
| 44 | Packet Length Std | 371624.0 | 186.4681018980964 | 253.91361072759034 | 0.0 | 25.98076211353316 | 56.56854249492381 | 284.3127963244816 | 4413.1467882595525 |
| 45 | Packet Length Variance | 371624.0 | 99242.30125069301 | 234705.9252749077 | 0.0 | 675.0 | 3200.0 | 80833.76615384617 | 19475864.57472561 |
| 46 | FIN Flag Count | 371624.0 | 0.7535169956730459 | 1.1010093253112798 | 0.0 | 0.0 | 0.0 | 2.0 | 60.0 |
| 47 | SYN Flag Count | 371624.0 | 0.7384883645835576 | 1.031206817683716 | 0.0 | 0.0 | 0.0 | 2.0 | 52.0 |
| 48 | RST Flag Count | 371624.0 | 0.20218285148429596 | 0.835818056531853 | 0.0 | 0.0 | 0.0 | 0.0 | 190.0 |
| 49 | PSH Flag Count | 371624.0 | 3.823407530191807 | 27.19730454627406 | 0.0 | 0.0 | 0.0 | 5.0 | 5216.0 |
| 50 | ACK Flag Count | 371624.0 | 28.32279400684563 | 2466.2785205794717 | 0.0 | 0.0 | 0.0 | 16.0 | 511681.0 |
| 51 | URG Flag Count | 371624.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| 52 | CWR Flag Count | 371624.0 | 0.00023410759262049814 | 0.015473694267635285 | 0.0 | 0.0 | 0.0 | 0.0 | 2.0 |
| 53 | ECE Flag Count | 371624.0 | 0.00037134307794975564 | 0.026951899073714727 | 0.0 | 0.0 | 0.0 | 0.0 | 2.0 |
| 54 | Down/Up Ratio | 371624.0 | 0.9267162696118131 | 0.22851016353031453 | 0.0 | 0.8823529411764706 | 1.0 | 1.0 | 5.0 |
| 55 | Average Packet Size | 371624.0 | 139.09490668184338 | 164.91187282077786 | 0.0 | 59.0 | 82.5 | 142.0 | 1809.306017326153 |
| 56 | Fwd Segment Size Avg | 371624.0 | 61.73750081315352 | 88.11389956652113 | 0.0 | 35.0 | 45.0 | 58.0 | 4613.1269035533 |
| 57 | Bwd Segment Size Avg | 371624.0 | 214.6245291496803 | 282.17684954917286 | 0.0 | 71.55555555555556 | 116.0 | 218.55 | 2976.3168807752986 |
| 58 | Fwd Bytes/Bulk Avg | 371624.0 | 80.98675812111166 | 1401.1677129836582 | 0.0 | 0.0 | 0.0 | 0.0 | 340409.0 |
| 59 | Fwd Packet/Bulk Avg | 371624.0 | 0.29997524379480334 | 1.8267998072038167 | 0.0 | 0.0 | 0.0 | 0.0 | 207.0 |
| 60 | Fwd Bulk Rate Avg | 371624.0 | 214236.67773609885 | 4366843.812500302 | 0.0 | 0.0 | 0.0 | 0.0 | 584400000.0 |
| 61 | Bwd Bytes/Bulk Avg | 371624.0 | 3891.8717816933245 | 318199.96998447046 | 0.0 | 0.0 | 0.0 | 0.0 | 156761876.0 |
| 62 | Bwd Packet/Bulk Avg | 371624.0 | 2.1290148106688482 | 117.82697959363615 | 0.0 | 0.0 | 0.0 | 0.0 | 56120.0 |
| 63 | Bwd Bulk Rate Avg | 371624.0 | 555316.7460739887 | 5949442.04450349 | 0.0 | 0.0 | 0.0 | 0.0 | 1127000000.0 |
| 64 | Subflow Fwd Packets | 371624.0 | 0.014038382881622284 | 0.11764924110784183 | 0.0 | 0.0 | 0.0 | 0.0 | 1.0 |
| 65 | Subflow Fwd Bytes | 371624.0 | 32.138933438098725 | 46.33334487951187 | 0.0 | 18.0 | 23.0 | 31.0 | 1598.0 |
| 66 | Subflow Bwd Packets | 371624.0 | 2.1527134953609024e-05 | 0.004639690664491651 | 0.0 | 0.0 | 0.0 | 0.0 | 1.0 |
| 67 | Subflow Bwd Bytes | 371624.0 | 106.31434729726821 | 155.5498536725014 | 0.0 | 34.0 | 56.0 | 105.0 | 1808.0 |
| 68 | FWD Init Win Bytes | 371624.0 | 10682.219409941232 | 19525.214464360008 | 0.0 | 0.0 | 0.0 | 8192.0 | 65535.0 |
| 69 | Bwd Init Win Bytes | 371624.0 | 963.8677722644393 | 4993.138174737863 | 0.0 | 0.0 | 0.0 | 119.0 | 65535.0 |
| 70 | Fwd Act Data Pkts | 371624.0 | 2.736822702516522 | 7.943931959837896 | 0.0 | 1.0 | 1.0 | 3.0 | 1430.0 |
| 71 | Fwd Seg Size Min | 371624.0 | 14.44489053451876 | 8.893550923486023 | 0.0 | 8.0 | 8.0 | 20.0 | 44.0 |
| 72 | Active Mean | 371624.0 | 124800.43488017739 | 777659.4272568884 | 0.0 | 0.0 | 0.0 | 0.0 | 101659665.0 |
| 73 | Active Std | 371624.0 | 66188.32554620034 | 490849.96198248636 | 0.0 | 0.0 | 0.0 | 0.0 | 64349504.50290726 |
| 74 | Active Max | 371624.0 | 239419.86346145565 | 1281923.583666237 | 0.0 | 0.0 | 0.0 | 0.0 | 101659665.0 |
| 75 | Active Min | 371624.0 | 86641.8536881364 | 680658.8058482102 | 0.0 | 0.0 | 0.0 | 0.0 | 101659665.0 |
| 76 | Idle Mean | 371624.0 | 5565505.072895748 | 15822343.805286227 | 0.0 | 0.0 | 0.0 | 0.0 | 119999735.0 |
| 77 | Idle Std | 371624.0 | 375126.12329563935 | 2899296.633727478 | 0.0 | 0.0 | 0.0 | 0.0 | 75145023.2323283 |
| 78 | Idle Max | 371624.0 | 5861658.82201903 | 16430346.298924077 | 0.0 | 0.0 | 0.0 | 0.0 | 119999735.0 |
| 79 | Idle Min | 371624.0 | 5199956.553486858 | 15529048.765316641 | 0.0 | 0.0 | 0.0 | 0.0 | 119999735.0 |
| 80 | ICMP Code | 371624.0 | -0.9988429164962435 | 0.08620281025763116 | -1.0 | -1.0 | -1.0 | -1.0 | 10.0 |
| 81 | ICMP Type | 371624.0 | -0.9987756441995135 | 0.08708699983503487 | -1.0 | -1.0 | -1.0 | -1.0 | 11.0 |
| 82 | Total TCP Flow Time | 371624.0 | 34663294.80406271 | 412624134.03343666 | 0.0 | 0.0 | 0.0 | 4386470.25 | 28503312990.0 |

## Distribution Analysis
 Distribution of target variable 'Label':

Distribution Analysis

| # | Class | Percentage |
|---|---|---|
| 1 | BENIGN | 1.0000 |

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
| 8 | Bwd Packet Length Max | bwd_packet_length_max |
| 9 | Bwd Packet Length Min | bwd_packet_length_min |
| 10 | Bwd Packet Length Mean | bwd_packet_length_mean |
| 11 | Bwd Packet Length Std | bwd_packet_length_std |
| 12 | Flow Bytes/s | flow_bytes/s |
| 13 | Flow Packets/s | flow_packets/s |
| 14 | Flow IAT Mean | flow_iat_mean |
| 15 | Flow IAT Std | flow_iat_std |
| 16 | Flow IAT Max | flow_iat_max |
| 17 | Flow IAT Min | flow_iat_min |
| 18 | Fwd IAT Mean | fwd_iat_mean |
| 19 | Fwd IAT Std | fwd_iat_std |
| 20 | Fwd PSH Flags | fwd_psh_flags |
| 21 | Bwd PSH Flags | bwd_psh_flags |
| 22 | Fwd RST Flags | fwd_rst_flags |
| 23 | Bwd RST Flags | bwd_rst_flags |
| 24 | Fwd Header Length | fwd_header_length |
| 25 | Bwd Header Length | bwd_header_length |
| 26 | Bwd Packets/s | bwd_packets/s |
| 27 | Packet Length Min | packet_length_min |
| 28 | Packet Length Max | packet_length_max |
| 29 | Packet Length Variance | packet_length_variance |
| 30 | FIN Flag Count | fin_flag_count |
| 31 | SYN Flag Count | syn_flag_count |
| 32 | CWR Flag Count | cwr_flag_count |
| 33 | ECE Flag Count | ece_flag_count |
| 34 | Down/Up Ratio | down/up_ratio |
| 35 | Fwd Bytes/Bulk Avg | fwd_bytes/bulk_avg |
| 36 | Fwd Packet/Bulk Avg | fwd_packet/bulk_avg |
| 37 | Fwd Bulk Rate Avg | fwd_bulk_rate_avg |
| 38 | Bwd Bytes/Bulk Avg | bwd_bytes/bulk_avg |
| 39 | Bwd Bulk Rate Avg | bwd_bulk_rate_avg |
| 40 | Subflow Fwd Packets | subflow_fwd_packets |
| 41 | Subflow Bwd Packets | subflow_bwd_packets |
| 42 | FWD Init Win Bytes | fwd_init_win_bytes |
| 43 | Bwd Init Win Bytes | bwd_init_win_bytes |
| 44 | Fwd Act Data Pkts | fwd_act_data_pkts |
| 45 | Fwd Seg Size Min | fwd_seg_size_min |
| 46 | Active Mean | active_mean |
| 47 | Active Std | active_std |
| 48 | Active Max | active_max |
| 49 | Active Min | active_min |
| 50 | Idle Std | idle_std |
| 51 | ICMP Code | icmp_code |
| 52 | ICMP Type | icmp_type |
| 53 | Total TCP Flow Time | total_tcp_flow_time |

## Recommendation
 Based on the assessment, it is recommended to continue working with the available columns. You may consider the following:
- Performing further analysis using the available columns: `['Dst Port', 'Flow Duration', 'Total Fwd Packet', 'Total Length of Fwd Packet', 'Fwd Packet Length Max', 'Fwd Packet Length Min', 'Fwd Packet Length Mean', 'Bwd Packet Length Max', 'Bwd Packet Length Min', 'Bwd Packet Length Mean', 'Bwd Packet Length Std', 'Flow Bytes/s', 'Flow Packets/s', 'Flow IAT Mean', 'Flow IAT Std', 'Flow IAT Max', 'Flow IAT Min', 'Fwd IAT Mean', 'Fwd IAT Std', 'Fwd PSH Flags', 'Bwd PSH Flags', 'Fwd RST Flags', 'Bwd RST Flags', 'Fwd Header Length', 'Bwd Header Length', 'Bwd Packets/s', 'Packet Length Min', 'Packet Length Max', 'Packet Length Variance', 'FIN Flag Count', 'SYN Flag Count', 'CWR Flag Count', 'ECE Flag Count', 'Down/Up Ratio', 'Fwd Bytes/Bulk Avg', 'Fwd Packet/Bulk Avg', 'Fwd Bulk Rate Avg', 'Bwd Bytes/Bulk Avg', 'Bwd Bulk Rate Avg', 'Subflow Fwd Packets', 'Subflow Bwd Packets', 'FWD Init Win Bytes', 'Bwd Init Win Bytes', 'Fwd Act Data Pkts', 'Fwd Seg Size Min', 'Active Mean', 'Active Std', 'Active Max', 'Active Min', 'Idle Std', 'ICMP Code', 'ICMP Type', 'Total TCP Flow Time']`
- Train machine learning models with the reduced feature set.
## End of Report ✅  
 
✅ Report Successfully Generated in  00:17 minutes

