# Data Assessment Report on dataset: Thursday-01-03-2018.csv
## Command line executed  
 ```dataset_assessment_prepare.py --drop-columns id,Protocol,Attempted Category,Src Port --drop-highly-correlated --correlation-threshold 0.95 --drop-categorical-columns --impute-strategy mean --assess-only --zero-variance --low-variance-threshold=0.01 --low-variance-sample-percentage=100 --missing-threshold=0.05 --descriptive-statistics --distribution-analysis --distribution-column Label -output . -input CSECICIDS2018_improved/Thursday-01-03-2018.csv```  
# Report  
 ### Options used to generate this report  

| # | Option | Value |
|---|---|---|
| 1 | -input | CSECICIDS2018_improved/Thursday-01-03-2018.csv |
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
 
✅ Dataset Loaded Successfully: `.../DATASET_engelen_improved/CSECICIDS2018_improved/Thursday-01-03-2018.csv
- File Size: 3631.97 MB
- Number of Records: 6,551,401
- File loaded in 09:12 minutes

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
 Found 13078183 negative values:

### Columns with Negative Values

| # | Column | Negative Count |
|---|---|---|
| 1 | Fwd Header Length | 866 |
| 2 | Bwd Header Length | 1735 |
| 3 | ICMP Code | 6537791 |
| 4 | ICMP Type | 6537791 |

💡 To replace with zero, use:
```python
df_numeric.loc[:, df_numeric.columns] = np.where(df_numeric < 0, 0, df_numeric)
```
## Infinite Values ⚠️ 
 Found 14 infinite values:

### Columns with Infinite Values

| # | Column | Infinite Count |
|---|---|---|
| 1 | Flow Bytes/s | 7 |
| 2 | Flow Packets/s | 7 |

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
| 1 | Total Length of Bwd Packet | Total Bwd packets | 0.9949 |
| 2 | Fwd Packet Length Std | Fwd Packet Length Max | 0.9743 |
| 3 | Bwd Packet Length Std | Bwd Packet Length Max | 0.9739 |
| 4 | Bwd IAT Total | Flow Duration | 0.9950 |
| 5 | Bwd IAT Max | Flow IAT Max | 0.9941 |
| 6 | Bwd IAT Max | Bwd IAT Std | 0.9544 |
| 7 | Fwd Packets/s | Flow Packets/s | 0.9811 |
| 8 | Bwd Packets/s | Flow Packets/s | 0.9786 |
| 9 | Packet Length Min | Fwd Packet Length Min | 0.9934 |
| 10 | Packet Length Std | Packet Length Max | 0.9513 |
| 11 | ACK Flag Count | Total Bwd packets | 0.9807 |
| 12 | ACK Flag Count | Total Length of Bwd Packet | 0.9758 |
| 13 | URG Flag Count | Fwd URG Flags | 1.0000 |
| 14 | Average Packet Size | Packet Length Mean | 1.0000 |
| 15 | Fwd Segment Size Avg | Fwd Packet Length Mean | 1.0000 |
| 16 | Bwd Segment Size Avg | Bwd Packet Length Mean | 1.0000 |
| 17 | Fwd Packet/Bulk Avg | Fwd Bytes/Bulk Avg | 0.9845 |
| 18 | Bwd Packet/Bulk Avg | Bwd Bytes/Bulk Avg | 0.9999 |
| 19 | Subflow Fwd Bytes | Fwd Packet Length Mean | 0.9769 |
| 20 | Subflow Fwd Bytes | Fwd Segment Size Avg | 0.9769 |
| 21 | Subflow Bwd Bytes | Bwd Packet Length Mean | 0.9750 |
| 22 | Subflow Bwd Bytes | Bwd Segment Size Avg | 0.9750 |
| 23 | Idle Mean | Flow IAT Max | 0.9919 |
| 24 | Idle Mean | Bwd IAT Max | 0.9866 |
| 25 | Idle Max | Flow IAT Max | 0.9996 |
| 26 | Idle Max | Bwd IAT Max | 0.9937 |
| 27 | Idle Max | Idle Mean | 0.9922 |
| 28 | Idle Min | Flow IAT Max | 0.9697 |
| 29 | Idle Min | Bwd IAT Max | 0.9649 |
| 30 | Idle Min | Idle Mean | 0.9924 |
| 31 | Idle Min | Idle Max | 0.9699 |

💡 To drop these features, use:
```python
df_numeric.drop(columns=['Total Length of Bwd Packet', 'Fwd Packet Length Std', 'Bwd Packet Length Std', 'Bwd IAT Total', 'Bwd IAT Max', 'Fwd Packets/s', 'Bwd Packets/s', 'Packet Length Min', 'Packet Length Std', 'ACK Flag Count', 'URG Flag Count', 'Average Packet Size', 'Fwd Segment Size Avg', 'Bwd Segment Size Avg', 'Fwd Packet/Bulk Avg', 'Bwd Packet/Bulk Avg', 'Subflow Fwd Bytes', 'Subflow Bwd Bytes', 'Idle Mean', 'Idle Max', 'Idle Min'], inplace=True)
```
## Descriptive Statistics Analysis
 Descriptive Statistics for Features

| # | Column | Count | Mean | Std | Min | 25% | 50% | 75% | Max |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Dst Port | 6551401.0 | 1212.0910783815552 | 2253.425807234015 | 0.0 | 53.0 | 443.0 | 3389.0 | 65535.0 |
| 2 | Flow Duration | 6551401.0 | 20469721.70439239 | 38561102.106411025 | 0.0 | 1484.0 | 447928.0 | 7047879.0 | 119999999.0 |
| 3 | Total Fwd Packet | 6551401.0 | 8.03043745910226 | 78.34769677319409 | 0.0 | 1.0 | 5.0 | 10.0 | 43506.0 |
| 4 | Total Bwd packets | 6551401.0 | 10.234347126668021 | 204.4871012255602 | 0.0 | 1.0 | 4.0 | 8.0 | 92316.0 |
| 5 | Total Length of Fwd Packet | 6551401.0 | 1219.551634070331 | 50728.1765445574 | 0.0 | 42.0 | 161.0 | 1132.0 | 41867805.0 |
| 6 | Total Length of Bwd Packet | 6551401.0 | 7105.243095179184 | 291514.2219313783 | 0.0 | 81.0 | 244.0 | 1581.0 | 111877880.0 |
| 7 | Fwd Packet Length Max | 6551401.0 | 337.11046690623886 | 1030.9945380165157 | 0.0 | 40.0 | 97.0 | 661.0 | 62780.0 |
| 8 | Fwd Packet Length Min | 6551401.0 | 15.838894764646524 | 23.867520074895953 | 0.0 | 0.0 | 0.0 | 36.0 | 2848.0 |
| 9 | Fwd Packet Length Mean | 6551401.0 | 75.1207632678051 | 177.78108375534498 | 0.0 | 34.0 | 46.0 | 103.46153846153844 | 12263.02913907286 |
| 10 | Fwd Packet Length Std | 6551401.0 | 101.59415948245592 | 291.1105044825558 | 0.0 | 0.0 | 42.72391992003231 | 191.01688550871765 | 14014.111190790383 |
| 11 | Bwd Packet Length Max | 6551401.0 | 584.7433260458336 | 600.0473369060413 | 0.0 | 73.0 | 175.0 | 1173.0 | 65160.0 |
| 12 | Bwd Packet Length Min | 6551401.0 | 39.5610120644424 | 58.72684598202704 | 0.0 | 0.0 | 0.0 | 71.0 | 1412.0 |
| 13 | Bwd Packet Length Mean | 6551401.0 | 156.2774896700505 | 162.20098401288965 | 0.0 | 60.0 | 126.0 | 211.0 | 33381.0588235294 |
| 14 | Bwd Packet Length Std | 6551401.0 | 196.5974132086851 | 228.58908318855487 | 0.0 | 0.0 | 56.79348554191757 | 420.4990798925441 | 21561.534286837246 |
| 15 | Flow Bytes/s | 6551394.0 | 82474.52607102171 | 291013.4682164528 | 0.0 | 100.29297232069314 | 1494.4498326902838 | 86402.26628895184 | 248000000.0 |
| 16 | Flow Packets/s | 6551394.0 | 4057.0761925290158 | 55206.758257382695 | 0.0166667066667626 | 2.068454316263266 | 17.631009419709322 | 1384.0830449826988 | 4000000.0 |
| 17 | Flow IAT Mean | 6551401.0 | 1002184.3004209729 | 2643004.2632751586 | 0.0 | 1440.0 | 69387.22222222222 | 515740.2916666666 | 119999712.0 |
| 18 | Flow IAT Std | 6551401.0 | 2900531.0148990345 | 6207876.9281269405 | 0.0 | 0.0 | 96066.52022947432 | 1383462.183961545 | 84815956.50852314 |
| 19 | Flow IAT Max | 6551401.0 | 11599821.805855878 | 25449298.775665373 | 0.0 | 1463.0 | 230907.0 | 5170174.0 | 119999712.0 |
| 20 | Flow IAT Min | 6551401.0 | 42057.78516732528 | 1374282.4450767043 | 0.0 | 4.0 | 39.0 | 412.0 | 119999712.0 |
| 21 | Fwd IAT Total | 6551401.0 | 13877643.466973705 | 33120361.644743714 | 0.0 | 0.0 | 406612.0 | 3972455.0 | 119999998.0 |
| 22 | Fwd IAT Mean | 6551401.0 | 1343143.3286827775 | 4313198.586789882 | 0.0 | 0.0 | 127618.75 | 379948.4444444445 | 119999712.0 |
| 23 | Fwd IAT Std | 6551401.0 | 1949464.8060719436 | 5519864.338005135 | 0.0 | 0.0 | 88623.74551815483 | 415351.6982348471 | 84776995.63198653 |
| 24 | Fwd IAT Max | 6551401.0 | 5239989.915673762 | 14150980.349574612 | 0.0 | 0.0 | 214476.0 | 1302210.0 | 119999712.0 |
| 25 | Fwd IAT Min | 6551401.0 | 194878.11233078237 | 3085393.9008106696 | 0.0 | 0.0 | 18.0 | 313.0 | 119999712.0 |
| 26 | Bwd IAT Total | 6551401.0 | 20133293.051541496 | 38402178.76971423 | 0.0 | 0.0 | 292116.0 | 5911519.0 | 119999999.0 |
| 27 | Bwd IAT Mean | 6551401.0 | 2369665.8489195528 | 6610141.745058497 | 0.0 | 0.0 | 116308.0 | 856862.1666666666 | 119999918.0 |
| 28 | Bwd IAT Std | 6551401.0 | 3762089.5816809926 | 8569316.10328439 | 0.0 | 0.0 | 13721.842174674166 | 1106895.4286424906 | 84792414.09535031 |
| 29 | Bwd IAT Max | 6551401.0 | 11450370.096473105 | 25377102.12628343 | 0.0 | 0.0 | 190770.0 | 5002684.0 | 119999918.0 |
| 30 | Bwd IAT Min | 6551401.0 | 630359.0606853404 | 5581082.768977348 | 0.0 | 0.0 | 15.0 | 69064.0 | 119999918.0 |
| 31 | Fwd PSH Flags | 6551401.0 | 2.6669622268580415 | 8.206787388006434 | 0.0 | 0.0 | 1.0 | 5.0 | 2566.0 |
| 32 | Bwd PSH Flags | 6551401.0 | 2.5798651311375993 | 12.562872370966028 | 0.0 | 0.0 | 1.0 | 5.0 | 17481.0 |
| 33 | Fwd URG Flags | 6551401.0 | 0.00028375610041272086 | 0.04442629941635556 | 0.0 | 0.0 | 0.0 | 0.0 | 20.0 |
| 34 | Bwd URG Flags | 6551401.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| 35 | Fwd RST Flags | 6551401.0 | 0.2585489729601348 | 0.44125673461141207 | 0.0 | 0.0 | 0.0 | 1.0 | 8.0 |
| 36 | Bwd RST Flags | 6551401.0 | 0.1902496885780614 | 0.4093699852059446 | 0.0 | 0.0 | 0.0 | 0.0 | 9.0 |
| 37 | Fwd Header Length | 6551401.0 | 142.96644030795855 | 469.1911853897363 | -32744.0 | 8.0 | 112.0 | 208.0 | 32752.0 |
| 38 | Bwd Header Length | 6551401.0 | 148.6738302234896 | 639.1113953288893 | -32764.0 | 8.0 | 100.0 | 172.0 | 32752.0 |
| 39 | Fwd Packets/s | 6551401.0 | 2053.719107869135 | 29032.865999924925 | 0.0 | 1.0722069745455385 | 9.212768897692202 | 691.0850034554251 | 4000000.0 |
| 40 | Bwd Packets/s | 6551401.0 | 2003.3527497804669 | 27306.4389537449 | 0.0 | 0.9374716927492776 | 8.204185775582703 | 692.5207756232687 | 2000000.0 |
| 41 | Packet Length Min | 6551401.0 | 15.813970935377029 | 23.57079622281702 | 0.0 | 0.0 | 0.0 | 36.0 | 624.0 |
| 42 | Packet Length Max | 6551401.0 | 639.7859909659018 | 1136.2827287407547 | 0.0 | 75.0 | 192.0 | 1173.0 | 65160.0 |
| 43 | Packet Length Mean | 6551401.0 | 116.13643141361867 | 129.1552613344276 | 0.0 | 52.0 | 83.0 | 159.35294117647058 | 17213.58333333334 |
| 44 | Packet Length Std | 6551401.0 | 180.07739122026265 | 250.44325770042423 | 0.0 | 22.62741699796952 | 81.2285216366316 | 312.0440909645339 | 22751.285146501723 |
| 45 | Packet Length Variance | 6551401.0 | 95149.68258249307 | 1077074.4229647617 | 0.0 | 512.0 | 6598.072727272727 | 97371.51470588232 | 517620975.81743 |
| 46 | FIN Flag Count | 6551401.0 | 0.45859595527735214 | 0.7926274458629456 | 0.0 | 0.0 | 0.0 | 1.0 | 20.0 |
| 47 | SYN Flag Count | 6551401.0 | 1.1458184287605049 | 2.792973667279382 | 0.0 | 0.0 | 2.0 | 2.0 | 2120.0 |
| 48 | RST Flag Count | 6551401.0 | 0.44880797252373955 | 0.5399227213940386 | 0.0 | 0.0 | 0.0 | 1.0 | 9.0 |
| 49 | PSH Flag Count | 6551401.0 | 5.246827357995641 | 16.2470288289926 | 0.0 | 0.0 | 2.0 | 10.0 | 17605.0 |
| 50 | ACK Flag Count | 6551401.0 | 16.093191059439043 | 269.99357643363516 | 0.0 | 0.0 | 8.0 | 17.0 | 135821.0 |
| 51 | URG Flag Count | 6551401.0 | 0.00028375610041272086 | 0.04442629941635556 | 0.0 | 0.0 | 0.0 | 0.0 | 20.0 |
| 52 | CWR Flag Count | 6551401.0 | 0.3436922881075361 | 0.5404822261526785 | 0.0 | 0.0 | 0.0 | 1.0 | 9.0 |
| 53 | ECE Flag Count | 6551401.0 | 0.4883106682066935 | 0.7745006046031898 | 0.0 | 0.0 | 0.0 | 1.0 | 13.0 |
| 54 | Down/Up Ratio | 6551401.0 | 0.9371233883984659 | 0.34834343566784187 | 0.0 | 0.8461538461538461 | 1.0 | 1.0 | 25.47457627118644 |
| 55 | Average Packet Size | 6551401.0 | 116.13643141361865 | 129.1552613344276 | 0.0 | 52.0 | 83.0 | 159.35294117647058 | 17213.583333333332 |
| 56 | Fwd Segment Size Avg | 6551401.0 | 75.1207632678051 | 177.78108375534498 | 0.0 | 34.0 | 46.0 | 103.46153846153848 | 12263.029139072847 |
| 57 | Bwd Segment Size Avg | 6551401.0 | 156.27748967005053 | 162.20098401288968 | 0.0 | 60.0 | 126.0 | 211.0 | 33381.05882352941 |
| 58 | Fwd Bytes/Bulk Avg | 6551401.0 | 389.1293172254301 | 45638.705318108245 | 0.0 | 0.0 | 0.0 | 0.0 | 8471288.0 |
| 59 | Fwd Packet/Bulk Avg | 6551401.0 | 0.07436333083564874 | 5.659810000669435 | 0.0 | 0.0 | 0.0 | 0.0 | 2461.0 |
| 60 | Fwd Bulk Rate Avg | 6551401.0 | 18349.236883530713 | 3734981.8127548206 | 0.0 | 0.0 | 0.0 | 0.0 | 2745000000.0 |
| 61 | Bwd Bytes/Bulk Avg | 6551401.0 | 2263.4713614690963 | 152822.75036002672 | 0.0 | 0.0 | 0.0 | 0.0 | 75996528.0 |
| 62 | Bwd Packet/Bulk Avg | 6551401.0 | 1.6790048418651218 | 106.08804783497361 | 0.0 | 0.0 | 0.0 | 0.0 | 52849.0 |
| 63 | Bwd Bulk Rate Avg | 6551401.0 | 17014923.79356019 | 174776649.63757908 | 0.0 | 0.0 | 0.0 | 0.0 | 5496000000.0 |
| 64 | Subflow Fwd Packets | 6551401.0 | 0.011876848936586236 | 0.10833185675167045 | 0.0 | 0.0 | 0.0 | 0.0 | 1.0 |
| 65 | Subflow Fwd Bytes | 6551401.0 | 38.120793552402 | 74.18869403969482 | 0.0 | 17.0 | 23.0 | 58.0 | 5837.0 |
| 66 | Subflow Bwd Packets | 6551401.0 | 0.0008653110991068933 | 0.029403443127883826 | 0.0 | 0.0 | 0.0 | 0.0 | 1.0 |
| 67 | Subflow Bwd Bytes | 6551401.0 | 77.33078436200135 | 97.38838148197195 | 0.0 | 29.0 | 62.0 | 95.0 | 17196.0 |
| 68 | FWD Init Win Bytes | 6551401.0 | 5068.275365986604 | 6486.633117093135 | 0.0 | 0.0 | 8192.0 | 8192.0 | 65535.0 |
| 69 | Bwd Init Win Bytes | 6551401.0 | 13570.345741315483 | 25516.28467896592 | 0.0 | 0.0 | 0.0 | 980.0 | 65535.0 |
| 70 | Fwd Act Data Pkts | 6551401.0 | 3.4870291102620645 | 20.82655295231551 | 0.0 | 0.0 | 1.0 | 5.0 | 35547.0 |
| 71 | Fwd Seg Size Min | 6551401.0 | 15.582825719262186 | 6.384301739044305 | 0.0 | 8.0 | 20.0 | 20.0 | 48.0 |
| 72 | Active Mean | 6551401.0 | 502386.3742541837 | 2027725.5397774172 | 0.0 | 0.0 | 0.0 | 7630.0 | 114762271.0 |
| 73 | Active Std | 6551401.0 | 113988.25153929568 | 1075172.6037976837 | 0.0 | 0.0 | 0.0 | 0.0 | 75407296.2085382 |
| 74 | Active Max | 6551401.0 | 669785.3210876575 | 2940363.80317397 | 0.0 | 0.0 | 0.0 | 11425.0 | 114762271.0 |
| 75 | Active Min | 6551401.0 | 418409.8002042617 | 1795281.6792561726 | 0.0 | 0.0 | 0.0 | 30.0 | 114762271.0 |
| 76 | Idle Mean | 6551401.0 | 10764856.480714329 | 25029123.03881583 | 0.0 | 0.0 | 0.0 | 5166960.5 | 119999712.0 |
| 77 | Idle Std | 6551401.0 | 649067.7956119283 | 4211879.0740141915 | 0.0 | 0.0 | 0.0 | 0.0 | 76106160.95308325 |
| 78 | Idle Max | 6551401.0 | 11273168.842715932 | 25582648.25773496 | 0.0 | 0.0 | 0.0 | 5170174.0 | 119999712.0 |
| 79 | Idle Min | 6551401.0 | 10228329.799703605 | 24873562.583645932 | 0.0 | 0.0 | 0.0 | 5046654.0 | 119999712.0 |
| 80 | ICMP Code | 6551401.0 | -0.9962429410136855 | 0.14209300102601555 | -1.0 | -1.0 | -1.0 | -1.0 | 13.0 |
| 81 | ICMP Type | 6551401.0 | -0.9819789690785223 | 0.40673486243172563 | -1.0 | -1.0 | -1.0 | -1.0 | 11.0 |
| 82 | Total TCP Flow Time | 6551401.0 | 147591398.65783182 | 1553055709.3694758 | 0.0 | 0.0 | 661345.0 | 11864525.0 | 39169231847.0 |

## Distribution Analysis
 Distribution of target variable 'Label':

Distribution Analysis

| # | Class | Percentage |
|---|---|---|
| 1 | BENIGN | 0.9939 |
| 2 | Infiltration - Communication Victim Attacker | 0.0000 |
| 3 | Infiltration - Dropbox Download | 0.0000 |
| 4 | Infiltration - Dropbox Download - Attempted | 0.0000 |
| 5 | Infiltration - NMAP Portscan | 0.0060 |

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
| 35 | Packet Length Variance | packet_length_variance |
| 36 | FIN Flag Count | fin_flag_count |
| 37 | SYN Flag Count | syn_flag_count |
| 38 | RST Flag Count | rst_flag_count |
| 39 | PSH Flag Count | psh_flag_count |
| 40 | CWR Flag Count | cwr_flag_count |
| 41 | ECE Flag Count | ece_flag_count |
| 42 | Down/Up Ratio | down/up_ratio |
| 43 | Fwd Bytes/Bulk Avg | fwd_bytes/bulk_avg |
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
| 56 | Active Min | active_min |
| 57 | Idle Std | idle_std |
| 58 | ICMP Code | icmp_code |
| 59 | ICMP Type | icmp_type |
| 60 | Total TCP Flow Time | total_tcp_flow_time |

## Recommendation
 Based on the assessment, it is recommended to continue working with the available columns. You may consider the following:
- Performing further analysis using the available columns: `['Dst Port', 'Flow Duration', 'Total Fwd Packet', 'Total Bwd packets', 'Total Length of Fwd Packet', 'Fwd Packet Length Max', 'Fwd Packet Length Min', 'Fwd Packet Length Mean', 'Bwd Packet Length Max', 'Bwd Packet Length Min', 'Bwd Packet Length Mean', 'Flow Bytes/s', 'Flow Packets/s', 'Flow IAT Mean', 'Flow IAT Std', 'Flow IAT Max', 'Flow IAT Min', 'Fwd IAT Total', 'Fwd IAT Mean', 'Fwd IAT Std', 'Fwd IAT Max', 'Fwd IAT Min', 'Bwd IAT Mean', 'Bwd IAT Std', 'Bwd IAT Min', 'Fwd PSH Flags', 'Bwd PSH Flags', 'Fwd URG Flags', 'Fwd RST Flags', 'Bwd RST Flags', 'Fwd Header Length', 'Bwd Header Length', 'Packet Length Max', 'Packet Length Mean', 'Packet Length Variance', 'FIN Flag Count', 'SYN Flag Count', 'RST Flag Count', 'PSH Flag Count', 'CWR Flag Count', 'ECE Flag Count', 'Down/Up Ratio', 'Fwd Bytes/Bulk Avg', 'Fwd Bulk Rate Avg', 'Bwd Bytes/Bulk Avg', 'Bwd Bulk Rate Avg', 'Subflow Fwd Packets', 'Subflow Bwd Packets', 'FWD Init Win Bytes', 'Bwd Init Win Bytes', 'Fwd Act Data Pkts', 'Fwd Seg Size Min', 'Active Mean', 'Active Std', 'Active Max', 'Active Min', 'Idle Std', 'ICMP Code', 'ICMP Type', 'Total TCP Flow Time']`
- Train machine learning models with the reduced feature set.
## End of Report ✅  
 
✅ Report Successfully Generated in  12:21 minutes

