# Data Assessment Report on dataset: Wednesday-21-02-2018.csv
## Command line executed  
 ```dataset_assessment_prepare.py --drop-columns id,Attempted Category,Src Port --drop-highly-correlated --correlation-threshold 0.95 --drop-categorical-columns --impute-strategy mean --assess-only --zero-variance --low-variance-threshold=0.01 --low-variance-sample-percentage=100 --missing-threshold=0.05 --descriptive-statistics --distribution-analysis --distribution-column Label -output . -input CSECICIDS2018_improved/Wednesday-21-02-2018.csv```  
# Report  
 ### Options used to generate this report  

| # | Option | Value |
|---|---|---|
| 1 | -input | CSECICIDS2018_improved/Wednesday-21-02-2018.csv |
| 2 | -output | . |
| 3 | --drop-columns | id,Attempted Category,Src Port |
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
 
✅ Dataset Loaded Successfully: `.../DATASET_engelen_improved/CSECICIDS2018_improved/Wednesday-21-02-2018.csv
- File Size: 3769.58 MB
- Number of Records: 6,962,593
- File loaded in 05:36 minutes

## Assessment Mode  
 # 🔍 Running in assessment-only mode. No changes applied to the dataset.  
## Explicitly Defined Columns 🗑  
 ### Explicitly Defined Columns  

| # | Column |
|---|---|
| 1 | id |
| 2 | Attempted Category |
| 3 | Src Port |

Python Command to drop columns these columns manually 💡  
 ```python
df.drop(columns=['id', 'Attempted Category', 'Src Port'], inplace=True)
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
 Found 13910072 negative values:

### Columns with Negative Values

| # | Column | Negative Count |
|---|---|---|
| 1 | Fwd Header Length | 1736 |
| 2 | Bwd Header Length | 1936 |
| 3 | ICMP Code | 6953200 |
| 4 | ICMP Type | 6953200 |

💡 To replace with zero, use:
```python
df_numeric.loc[:, df_numeric.columns] = np.where(df_numeric < 0, 0, df_numeric)
```
## Infinite Values ⚠️ 
 Found 12 infinite values:

### Columns with Infinite Values

| # | Column | Infinite Count |
|---|---|---|
| 1 | Flow Bytes/s | 6 |
| 2 | Flow Packets/s | 6 |

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
| 1 | Total Length of Bwd Packet | Total Bwd packets | 0.9964 |
| 2 | Fwd Packet Length Std | Fwd Packet Length Max | 0.9737 |
| 3 | Bwd Packet Length Std | Bwd Packet Length Max | 0.9706 |
| 4 | Bwd IAT Total | Flow Duration | 0.9937 |
| 5 | Bwd IAT Max | Flow IAT Max | 0.9920 |
| 6 | Packet Length Min | Fwd Packet Length Min | 0.9977 |
| 7 | PSH Flag Count | Bwd PSH Flags | 0.9626 |
| 8 | ACK Flag Count | Total Bwd packets | 0.9886 |
| 9 | ACK Flag Count | Total Length of Bwd Packet | 0.9854 |
| 10 | Average Packet Size | Packet Length Mean | 1.0000 |
| 11 | Fwd Segment Size Avg | Fwd Packet Length Mean | 1.0000 |
| 12 | Bwd Segment Size Avg | Bwd Packet Length Mean | 1.0000 |
| 13 | Fwd Bytes/Bulk Avg | Total Length of Fwd Packet | 0.9941 |
| 14 | Fwd Packet/Bulk Avg | Total Fwd Packet | 0.9961 |
| 15 | Bwd Packet/Bulk Avg | Bwd Bytes/Bulk Avg | 0.9999 |
| 16 | Subflow Fwd Bytes | Fwd Packet Length Mean | 0.9762 |
| 17 | Subflow Fwd Bytes | Fwd Segment Size Avg | 0.9762 |
| 18 | Subflow Bwd Bytes | Bwd Packet Length Mean | 0.9765 |
| 19 | Subflow Bwd Bytes | Bwd Segment Size Avg | 0.9765 |
| 20 | Fwd Act Data Pkts | Total Fwd Packet | 0.9992 |
| 21 | Fwd Act Data Pkts | Fwd Packet/Bulk Avg | 0.9969 |
| 22 | Active Min | Active Mean | 0.9761 |
| 23 | Idle Mean | Flow IAT Max | 0.9874 |
| 24 | Idle Mean | Bwd IAT Max | 0.9800 |
| 25 | Idle Max | Flow IAT Max | 0.9994 |
| 26 | Idle Max | Bwd IAT Max | 0.9914 |
| 27 | Idle Max | Idle Mean | 0.9880 |
| 28 | Idle Min | Flow IAT Max | 0.9506 |
| 29 | Idle Min | Idle Mean | 0.9870 |
| 30 | Idle Min | Idle Max | 0.9511 |

💡 To drop these features, use:
```python
df_numeric.drop(columns=['Total Length of Bwd Packet', 'Fwd Packet Length Std', 'Bwd Packet Length Std', 'Bwd IAT Total', 'Bwd IAT Max', 'Packet Length Min', 'PSH Flag Count', 'ACK Flag Count', 'Average Packet Size', 'Fwd Segment Size Avg', 'Bwd Segment Size Avg', 'Fwd Bytes/Bulk Avg', 'Fwd Packet/Bulk Avg', 'Bwd Packet/Bulk Avg', 'Subflow Fwd Bytes', 'Subflow Bwd Bytes', 'Fwd Act Data Pkts', 'Active Min', 'Idle Mean', 'Idle Max', 'Idle Min'], inplace=True)
```
## Descriptive Statistics Analysis
 Descriptive Statistics for Features

| # | Column | Count | Mean | Std | Min | 25% | 50% | 75% | Max |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Dst Port | 6962593.0 | 762.7007560258082 | 1741.8715842003498 | 0.0 | 53.0 | 80.0 | 443.0 | 65535.0 |
| 2 | Protocol | 6962593.0 | 10.027843936878114 | 5.320292319291452 | 0.0 | 6.0 | 6.0 | 17.0 | 17.0 |
| 3 | Flow Duration | 6962593.0 | 14427512.495135361 | 33911566.60154227 | 0.0 | 1827.0 | 51716.0 | 2762021.0 | 119999998.0 |
| 4 | Total Fwd Packet | 6962593.0 | 36.14623962652994 | 1904.0030327282377 | 0.0 | 1.0 | 5.0 | 8.0 | 309629.0 |
| 5 | Total Bwd packets | 6962593.0 | 9.400518025396574 | 237.28004283872974 | 0.0 | 1.0 | 5.0 | 7.0 | 145026.0 |
| 6 | Total Length of Fwd Packet | 6962593.0 | 1871.5623374797292 | 73647.95576121403 | 0.0 | 42.0 | 234.0 | 671.0 | 13343631.0 |
| 7 | Total Length of Bwd Packet | 6962593.0 | 6783.0895226821385 | 330966.3135922489 | 0.0 | 93.0 | 312.0 | 1579.0 | 211703210.0 |
| 8 | Fwd Packet Length Max | 6962593.0 | 298.1193848326335 | 948.3335222024842 | 0.0 | 40.0 | 140.0 | 380.0 | 51956.0 |
| 9 | Fwd Packet Length Min | 6962593.0 | 15.228979634455152 | 23.0940318429677 | 0.0 | 0.0 | 0.0 | 36.0 | 1457.0 |
| 10 | Fwd Packet Length Mean | 6962593.0 | 67.5309314707677 | 158.27675118576073 | 0.0 | 35.0 | 48.0 | 69.0 | 9027.979253112037 |
| 11 | Fwd Packet Length Std | 6962593.0 | 96.06270495974769 | 265.5546235639666 | 0.0 | 0.0 | 66.18761213399378 | 145.34441853748632 | 11583.677675339288 |
| 12 | Bwd Packet Length Max | 6962593.0 | 572.3029008014687 | 545.2891149900456 | 0.0 | 84.0 | 231.0 | 1149.0 | 65160.0 |
| 13 | Bwd Packet Length Min | 6962593.0 | 37.610881894144896 | 56.567283660357425 | 0.0 | 0.0 | 0.0 | 69.0 | 1430.0 |
| 14 | Bwd Packet Length Mean | 6962593.0 | 159.3479565650401 | 157.51610733113785 | 0.0 | 63.0 | 136.0 | 187.0 | 39014.49065420562 |
| 15 | Bwd Packet Length Std | 6962593.0 | 210.48198799725492 | 226.28261269852837 | 0.0 | 0.0 | 86.23842917555181 | 418.1447117924607 | 22139.852185110383 |
| 16 | Flow Bytes/s | 6962587.0 | 99063.51289919297 | 383439.613430691 | 0.0 | 658.0472784918602 | 6767.148569670871 | 132103.32103321032 | 506000000.0 |
| 17 | Flow Packets/s | 6962587.0 | 1497.4891921279973 | 9129.89119925267 | 0.016666925559577 | 5.755982973971749 | 100.52271813429834 | 1748.2517482517485 | 3000000.0 |
| 18 | Flow IAT Mean | 6962593.0 | 721225.1069939525 | 2366112.246746602 | 0.0 | 1038.0 | 15392.333333333332 | 187174.6875 | 119998136.0 |
| 19 | Flow IAT Std | 6962593.0 | 1878814.1643914876 | 5052706.96033406 | 0.0 | 0.0 | 12273.572671032309 | 260206.8380763087 | 84804272.98317759 |
| 20 | Flow IAT Max | 6962593.0 | 6917935.103769961 | 18923998.14563642 | 0.0 | 1422.0 | 37867.0 | 967217.0 | 119998136.0 |
| 21 | Flow IAT Min | 6962593.0 | 39251.78940475194 | 1343254.068112835 | 0.0 | 3.0 | 28.0 | 430.0 | 119998136.0 |
| 22 | Fwd IAT Total | 6962593.0 | 12110458.212156016 | 31590115.829053834 | 0.0 | 0.0 | 36035.0 | 2465085.0 | 119999998.0 |
| 23 | Fwd IAT Mean | 6962593.0 | 1155996.4799320027 | 3893668.523059359 | 0.0 | 0.0 | 16167.5 | 315519.75 | 119998136.0 |
| 24 | Fwd IAT Std | 6962593.0 | 1785562.3040932962 | 5407005.6888202205 | 0.0 | 0.0 | 7349.828886897073 | 392073.1544454549 | 84742694.58913796 |
| 25 | Fwd IAT Max | 6962593.0 | 4730109.863782071 | 13898552.654795447 | 0.0 | 0.0 | 29413.0 | 1190733.0 | 119998136.0 |
| 26 | Fwd IAT Min | 6962593.0 | 130072.82272193707 | 2625507.5500875316 | 0.0 | 0.0 | 35.0 | 313.0 | 119998136.0 |
| 27 | Bwd IAT Total | 6962593.0 | 14110300.004935661 | 33690758.05931305 | 0.0 | 0.0 | 21930.0 | 2386645.0 | 119999988.0 |
| 28 | Bwd IAT Mean | 6962593.0 | 1710372.448239912 | 6067348.804245102 | 0.0 | 0.0 | 5844.5 | 356577.1666666667 | 119999427.0 |
| 29 | Bwd IAT Std | 6962593.0 | 2266818.743351331 | 6546077.749073021 | 0.0 | 0.0 | 1412.2460538683288 | 331974.94008677686 | 84831531.24248555 |
| 30 | Bwd IAT Max | 6962593.0 | 6794820.709681149 | 18832769.060587157 | 0.0 | 0.0 | 16740.0 | 953700.0 | 119999427.0 |
| 31 | Bwd IAT Min | 6962593.0 | 528989.3041977321 | 5217756.035167594 | 0.0 | 0.0 | 18.0 | 642.0 | 119999427.0 |
| 32 | Fwd PSH Flags | 6962593.0 | 2.061232216215999 | 5.869795683352608 | 0.0 | 0.0 | 1.0 | 4.0 | 1029.0 |
| 33 | Bwd PSH Flags | 6962593.0 | 2.110312925084089 | 19.93270591093973 | 0.0 | 0.0 | 1.0 | 4.0 | 17922.0 |
| 34 | Fwd URG Flags | 6962593.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| 35 | Bwd URG Flags | 6962593.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| 36 | Fwd RST Flags | 6962593.0 | 0.18883151722354014 | 0.3940044671390324 | 0.0 | 0.0 | 0.0 | 0.0 | 7.0 |
| 37 | Bwd RST Flags | 6962593.0 | 0.11627205554022761 | 0.3415578720976374 | 0.0 | 0.0 | 0.0 | 0.0 | 14.0 |
| 38 | Fwd Header Length | 6962593.0 | 125.58293957437984 | 520.9973963178334 | -32764.0 | 8.0 | 112.0 | 172.0 | 32696.0 |
| 39 | Bwd Header Length | 6962593.0 | 130.72237886086404 | 582.1112546663694 | -32768.0 | 8.0 | 112.0 | 152.0 | 32752.0 |
| 40 | Fwd Packets/s | 6962593.0 | 754.1657566407247 | 6784.26895021974 | 0.0 | 3.2074258322869107 | 50.99699117752052 | 874.8906386701663 | 3000000.0 |
| 41 | Bwd Packets/s | 6962593.0 | 743.3221450290847 | 5236.161099887296 | 0.0 | 2.6028497486390814 | 49.87033712347896 | 873.9730816290858 | 2000000.0 |
| 42 | Packet Length Min | 6962593.0 | 15.214301769470081 | 22.903342267470375 | 0.0 | 0.0 | 0.0 | 36.0 | 1166.0 |
| 43 | Packet Length Max | 6962593.0 | 620.3251886186655 | 1043.0836293028046 | 0.0 | 85.0 | 243.0 | 1149.0 | 65160.0 |
| 44 | Packet Length Mean | 6962593.0 | 114.22108048789283 | 119.22455508030087 | 0.0 | 54.0 | 89.5 | 141.0 | 22876.539726027386 |
| 45 | Packet Length Std | 6962593.0 | 186.2665576320723 | 233.3777027759939 | 0.0 | 31.81980515339464 | 100.40916292848976 | 302.1200828221197 | 25216.961646542008 |
| 46 | Packet Length Variance | 6962593.0 | 89160.37482256386 | 1006192.9458060734 | 0.0 | 1012.5 | 10082.0 | 91276.54444444444 | 635895154.6831707 |
| 47 | FIN Flag Count | 6962593.0 | 0.7088864737605659 | 0.9413563698343719 | 0.0 | 0.0 | 0.0 | 2.0 | 15.0 |
| 48 | SYN Flag Count | 6962593.0 | 1.1695352579132516 | 1.0774489407643102 | 0.0 | 0.0 | 2.0 | 2.0 | 290.0 |
| 49 | RST Flag Count | 6962593.0 | 0.30511578085922875 | 0.5025471515957906 | 0.0 | 0.0 | 0.0 | 1.0 | 14.0 |
| 50 | PSH Flag Count | 6962593.0 | 4.171545141300087 | 21.48436237624435 | 0.0 | 0.0 | 2.0 | 8.0 | 18046.0 |
| 51 | ACK Flag Count | 6962593.0 | 14.897528262818177 | 304.30742570488763 | 0.0 | 0.0 | 9.0 | 14.0 | 183661.0 |
| 52 | URG Flag Count | 6962593.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| 53 | CWR Flag Count | 6962593.0 | 0.39180805197144225 | 0.5300292039748979 | 0.0 | 0.0 | 0.0 | 1.0 | 46.0 |
| 54 | ECE Flag Count | 6962593.0 | 0.47922505308008095 | 0.6804880077994886 | 0.0 | 0.0 | 0.0 | 1.0 | 8.0 |
| 55 | Down/Up Ratio | 6962593.0 | 0.9545721110558066 | 0.31904559579749353 | 0.0 | 0.8888888888888888 | 1.0 | 1.0 | 25.14583333333333 |
| 56 | Average Packet Size | 6962593.0 | 114.22108048789283 | 119.22455508030087 | 0.0 | 54.0 | 89.5 | 141.0 | 22876.5397260274 |
| 57 | Fwd Segment Size Avg | 6962593.0 | 67.5309314707677 | 158.27675118576073 | 0.0 | 35.0 | 48.0 | 69.0 | 9027.979253112033 |
| 58 | Bwd Segment Size Avg | 6962593.0 | 159.3479565650401 | 157.51610733113785 | 0.0 | 63.0 | 136.0 | 187.0 | 39014.490654205605 |
| 59 | Fwd Bytes/Bulk Avg | 6962593.0 | 1246.512851318467 | 72806.84128965315 | 0.0 | 0.0 | 0.0 | 0.0 | 9908128.0 |
| 60 | Fwd Packet/Bulk Avg | 6962593.0 | 28.840427122481525 | 1884.942761009543 | 0.0 | 0.0 | 0.0 | 0.0 | 309629.0 |
| 61 | Fwd Bulk Rate Avg | 6962593.0 | 17142.882959696195 | 4013296.184186761 | 0.0 | 0.0 | 0.0 | 0.0 | 2922500000.0 |
| 62 | Bwd Bytes/Bulk Avg | 6962593.0 | 2125.485850458299 | 176084.8198143877 | 0.0 | 0.0 | 0.0 | 0.0 | 52925802.0 |
| 63 | Bwd Packet/Bulk Avg | 6962593.0 | 1.5681544217793573 | 122.44923318162841 | 0.0 | 0.0 | 0.0 | 0.0 | 36253.0 |
| 64 | Bwd Bulk Rate Avg | 6962593.0 | 17586282.30223338 | 178997247.7927407 | 0.0 | 0.0 | 0.0 | 0.0 | 5840000000.0 |
| 65 | Subflow Fwd Packets | 6962593.0 | 0.011535644838065358 | 0.10678284213264957 | 0.0 | 0.0 | 0.0 | 0.0 | 1.0 |
| 66 | Subflow Fwd Bytes | 6962593.0 | 33.799631688941176 | 63.305432497998304 | 0.0 | 17.0 | 24.0 | 34.0 | 4292.0 |
| 67 | Subflow Bwd Packets | 6962593.0 | 0.0006461673115174189 | 0.02541160900196117 | 0.0 | 0.0 | 0.0 | 0.0 | 1.0 |
| 68 | Subflow Bwd Bytes | 6962593.0 | 79.70115602046536 | 94.36147736757806 | 0.0 | 31.0 | 67.0 | 93.0 | 22874.0 |
| 69 | FWD Init Win Bytes | 6962593.0 | 13907.488725680218 | 22751.44201933158 | 0.0 | 0.0 | 8192.0 | 8192.0 | 65535.0 |
| 70 | Bwd Init Win Bytes | 6962593.0 | 9304.067660712037 | 21863.557428290205 | 0.0 | 0.0 | 64.0 | 219.0 | 65535.0 |
| 71 | Fwd Act Data Pkts | 6962593.0 | 31.728381365965237 | 1902.459746643797 | 0.0 | 0.0 | 1.0 | 5.0 | 309628.0 |
| 72 | Fwd Seg Size Min | 6962593.0 | 15.684982304724691 | 6.2737063000730195 | 0.0 | 8.0 | 20.0 | 20.0 | 52.0 |
| 73 | Active Mean | 6962593.0 | 198943.29952223107 | 1265840.5608207227 | 0.0 | 0.0 | 0.0 | 0.0 | 111837322.0 |
| 74 | Active Std | 6962593.0 | 39992.53233179975 | 401344.0402629777 | 0.0 | 0.0 | 0.0 | 0.0 | 75309833.55956692 |
| 75 | Active Max | 6962593.0 | 259107.06814084924 | 1453118.5146242303 | 0.0 | 0.0 | 0.0 | 0.0 | 111837322.0 |
| 76 | Active Min | 6962593.0 | 175149.3630569818 | 1230654.7293771987 | 0.0 | 0.0 | 0.0 | 0.0 | 111837322.0 |
| 77 | Idle Mean | 6962593.0 | 6250584.111722993 | 18233246.838231985 | 0.0 | 0.0 | 0.0 | 0.0 | 119998136.0 |
| 78 | Idle Std | 6962593.0 | 562752.0207990125 | 4023420.650436708 | 0.0 | 0.0 | 0.0 | 0.0 | 74497936.38183565 |
| 79 | Idle Max | 6962593.0 | 6663841.223092891 | 19001156.831110902 | 0.0 | 0.0 | 0.0 | 0.0 | 119998136.0 |
| 80 | Idle Min | 6962593.0 | 5785511.485448166 | 17923057.093081225 | 0.0 | 0.0 | 0.0 | 0.0 | 119998136.0 |
| 81 | ICMP Code | 6962593.0 | -0.9970699134647106 | 0.13662645136105406 | -1.0 | -1.0 | -1.0 | -1.0 | 13.0 |
| 82 | ICMP Type | 6962593.0 | -0.9882983250636652 | 0.3295257737686361 | -1.0 | -1.0 | -1.0 | -1.0 | 11.0 |
| 83 | Total TCP Flow Time | 6962593.0 | 146730746.35750473 | 1614887137.514751 | 0.0 | 0.0 | 30025.0 | 3599779.0 | 43568696135.0 |

## Distribution Analysis
 Distribution of target variable 'Label':

Distribution Analysis

| # | Class | Percentage |
|---|---|---|
| 1 | BENIGN | 0.8443 |
| 2 | DDoS-HOIC | 0.1554 |
| 3 | DDoS-LOIC-UDP | 0.0002 |
| 4 | DDoS-LOIC-UDP - Attempted | 0.0000 |

## Recommended Columns and Mapping  
 The following columns are available after cleaning.
Recommended mapping:
| # | Column Name | Mapping |
|---|---|---|
| 1 | Dst Port | dst_port |
| 2 | Protocol | protocol |
| 3 | Flow Duration | flow_duration |
| 4 | Total Fwd Packet | total_fwd_packet |
| 5 | Total Bwd packets | total_bwd_packets |
| 6 | Total Length of Fwd Packet | total_length_of_fwd_packet |
| 7 | Fwd Packet Length Max | fwd_packet_length_max |
| 8 | Fwd Packet Length Min | fwd_packet_length_min |
| 9 | Fwd Packet Length Mean | fwd_packet_length_mean |
| 10 | Bwd Packet Length Max | bwd_packet_length_max |
| 11 | Bwd Packet Length Min | bwd_packet_length_min |
| 12 | Bwd Packet Length Mean | bwd_packet_length_mean |
| 13 | Flow Bytes/s | flow_bytes/s |
| 14 | Flow Packets/s | flow_packets/s |
| 15 | Flow IAT Mean | flow_iat_mean |
| 16 | Flow IAT Std | flow_iat_std |
| 17 | Flow IAT Max | flow_iat_max |
| 18 | Flow IAT Min | flow_iat_min |
| 19 | Fwd IAT Total | fwd_iat_total |
| 20 | Fwd IAT Mean | fwd_iat_mean |
| 21 | Fwd IAT Std | fwd_iat_std |
| 22 | Fwd IAT Max | fwd_iat_max |
| 23 | Fwd IAT Min | fwd_iat_min |
| 24 | Bwd IAT Mean | bwd_iat_mean |
| 25 | Bwd IAT Std | bwd_iat_std |
| 26 | Bwd IAT Min | bwd_iat_min |
| 27 | Fwd PSH Flags | fwd_psh_flags |
| 28 | Bwd PSH Flags | bwd_psh_flags |
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
| 42 | CWR Flag Count | cwr_flag_count |
| 43 | ECE Flag Count | ece_flag_count |
| 44 | Down/Up Ratio | down/up_ratio |
| 45 | Fwd Bulk Rate Avg | fwd_bulk_rate_avg |
| 46 | Bwd Bytes/Bulk Avg | bwd_bytes/bulk_avg |
| 47 | Bwd Bulk Rate Avg | bwd_bulk_rate_avg |
| 48 | Subflow Fwd Packets | subflow_fwd_packets |
| 49 | Subflow Bwd Packets | subflow_bwd_packets |
| 50 | FWD Init Win Bytes | fwd_init_win_bytes |
| 51 | Bwd Init Win Bytes | bwd_init_win_bytes |
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
- Performing further analysis using the available columns: `['Dst Port', 'Protocol', 'Flow Duration', 'Total Fwd Packet', 'Total Bwd packets', 'Total Length of Fwd Packet', 'Fwd Packet Length Max', 'Fwd Packet Length Min', 'Fwd Packet Length Mean', 'Bwd Packet Length Max', 'Bwd Packet Length Min', 'Bwd Packet Length Mean', 'Flow Bytes/s', 'Flow Packets/s', 'Flow IAT Mean', 'Flow IAT Std', 'Flow IAT Max', 'Flow IAT Min', 'Fwd IAT Total', 'Fwd IAT Mean', 'Fwd IAT Std', 'Fwd IAT Max', 'Fwd IAT Min', 'Bwd IAT Mean', 'Bwd IAT Std', 'Bwd IAT Min', 'Fwd PSH Flags', 'Bwd PSH Flags', 'Fwd RST Flags', 'Bwd RST Flags', 'Fwd Header Length', 'Bwd Header Length', 'Fwd Packets/s', 'Bwd Packets/s', 'Packet Length Max', 'Packet Length Mean', 'Packet Length Std', 'Packet Length Variance', 'FIN Flag Count', 'SYN Flag Count', 'RST Flag Count', 'CWR Flag Count', 'ECE Flag Count', 'Down/Up Ratio', 'Fwd Bulk Rate Avg', 'Bwd Bytes/Bulk Avg', 'Bwd Bulk Rate Avg', 'Subflow Fwd Packets', 'Subflow Bwd Packets', 'FWD Init Win Bytes', 'Bwd Init Win Bytes', 'Fwd Seg Size Min', 'Active Mean', 'Active Std', 'Active Max', 'Idle Std', 'ICMP Code', 'ICMP Type', 'Total TCP Flow Time']`
- Train machine learning models with the reduced feature set.
## End of Report ✅  
 
✅ Report Successfully Generated in  14:30 minutes

