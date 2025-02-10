# Data Assessment Report on dataset: thursday.csv
## Command line executed  
 ```dataset_assessment_prepare.py --drop-columns id,Protocol,Attempted Category,Src Port --drop-highly-correlated --correlation-threshold 0.95 --drop-categorical-columns --impute-strategy mean --assess-only --zero-variance --low-variance-threshold=0.01 --low-variance-sample-percentage=100 --missing-threshold=0.05 --descriptive-statistics --distribution-analysis --distribution-column Label -output . -input CICIDS2017_improved/thursday.csv```  
# Report  
 ### Options used to generate this report  

| # | Option | Value |
|---|---|---|
| 1 | -input | CICIDS2017_improved/thursday.csv |
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
 
✅ Dataset Loaded Successfully: `.../DATASET_engelen_improved/CICIDS2017_improved/thursday.csv
- File Size: 180.74 MB
- Number of Records: 362,076
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
## Zero Variance Columns ✅  
 No issues found!  
## Negative Values ⚠️  
 Found 724001 negative values:

### Columns with Negative Values

| # | Column | Negative Count |
|---|---|---|
| 1 | Fwd Header Length | 99 |
| 2 | Bwd Header Length | 128 |
| 3 | ICMP Code | 361887 |
| 4 | ICMP Type | 361887 |

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
 ️Found 25 highly correlated features (threshold: 0.95):

### Highly Correlated Features

| # | Feature 1 | Feature 2 | Correlation |
|---|---|---|---|
| 1 | Total Bwd packets | Total Fwd Packet | 0.9982 |
| 2 | Total Length of Bwd Packet | Total Fwd Packet | 0.9931 |
| 3 | Total Length of Bwd Packet | Total Bwd packets | 0.9866 |
| 4 | Fwd Packet Length Std | Fwd Packet Length Max | 0.9523 |
| 5 | Fwd IAT Total | Flow Duration | 0.9994 |
| 6 | Fwd IAT Max | Flow IAT Max | 0.9985 |
| 7 | Fwd IAT Min | Fwd IAT Mean | 0.9702 |
| 8 | Bwd IAT Total | Flow Duration | 0.9904 |
| 9 | Bwd IAT Total | Fwd IAT Total | 0.9898 |
| 10 | Bwd IAT Mean | Flow IAT Std | 0.9568 |
| 11 | Bwd IAT Mean | Fwd IAT Mean | 0.9660 |
| 12 | Bwd IAT Std | Fwd IAT Std | 0.9540 |
| 13 | Bwd IAT Max | Flow IAT Max | 0.9780 |
| 14 | Bwd IAT Max | Fwd IAT Max | 0.9766 |
| 15 | Bwd IAT Min | Fwd IAT Min | 0.9626 |
| 16 | Bwd IAT Min | Bwd IAT Mean | 0.9610 |
| 17 | Fwd Packets/s | Flow Packets/s | 0.9870 |
| 18 | Packet Length Mean | Bwd Packet Length Mean | 0.9601 |
| 19 | Packet Length Std | Packet Length Max | 0.9670 |
| 20 | ACK Flag Count | Total Fwd Packet | 0.9994 |
| 21 | ACK Flag Count | Total Bwd packets | 0.9997 |
| 22 | ACK Flag Count | Total Length of Bwd Packet | 0.9898 |
| 23 | URG Flag Count | Fwd URG Flags | 0.9996 |
| 24 | Average Packet Size | Bwd Packet Length Mean | 0.9601 |
| 25 | Average Packet Size | Packet Length Mean | 1.0000 |
| 26 | Fwd Segment Size Avg | Fwd Packet Length Mean | 1.0000 |
| 27 | Bwd Segment Size Avg | Bwd Packet Length Mean | 1.0000 |
| 28 | Bwd Segment Size Avg | Packet Length Mean | 0.9601 |
| 29 | Bwd Segment Size Avg | Average Packet Size | 0.9601 |
| 30 | Fwd Packet/Bulk Avg | Fwd Bytes/Bulk Avg | 0.9608 |
| 31 | Subflow Fwd Bytes | Fwd Packet Length Mean | 0.9792 |
| 32 | Subflow Fwd Bytes | Fwd Segment Size Avg | 0.9792 |
| 33 | Subflow Bwd Bytes | Bwd Packet Length Mean | 0.9886 |
| 34 | Subflow Bwd Bytes | Packet Length Mean | 0.9659 |
| 35 | Subflow Bwd Bytes | Average Packet Size | 0.9659 |
| 36 | Subflow Bwd Bytes | Bwd Segment Size Avg | 0.9886 |
| 37 | Idle Mean | Flow IAT Max | 0.9916 |
| 38 | Idle Mean | Fwd IAT Max | 0.9904 |
| 39 | Idle Mean | Bwd IAT Max | 0.9717 |
| 40 | Idle Max | Flow IAT Max | 0.9985 |
| 41 | Idle Max | Fwd IAT Max | 0.9970 |
| 42 | Idle Max | Bwd IAT Max | 0.9765 |
| 43 | Idle Max | Idle Mean | 0.9931 |
| 44 | Idle Min | Flow IAT Max | 0.9716 |
| 45 | Idle Min | Fwd IAT Max | 0.9707 |
| 46 | Idle Min | Bwd IAT Max | 0.9534 |
| 47 | Idle Min | Idle Mean | 0.9926 |
| 48 | Idle Min | Idle Max | 0.9729 |

💡 To drop these features, use:
```python
df_numeric.drop(columns=['Total Bwd packets', 'Total Length of Bwd Packet', 'Fwd Packet Length Std', 'Fwd IAT Total', 'Fwd IAT Max', 'Fwd IAT Min', 'Bwd IAT Total', 'Bwd IAT Mean', 'Bwd IAT Std', 'Bwd IAT Max', 'Bwd IAT Min', 'Fwd Packets/s', 'Packet Length Mean', 'Packet Length Std', 'ACK Flag Count', 'URG Flag Count', 'Average Packet Size', 'Fwd Segment Size Avg', 'Bwd Segment Size Avg', 'Fwd Packet/Bulk Avg', 'Subflow Fwd Bytes', 'Subflow Bwd Bytes', 'Idle Mean', 'Idle Max', 'Idle Min'], inplace=True)
```
## Descriptive Statistics Analysis
 Descriptive Statistics for Features

| # | Column | Count | Mean | Std | Min | 25% | 50% | 75% | Max |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Dst Port | 362076.0 | 2169.289707133309 | 7942.988472413306 | 0.0 | 53.0 | 80.0 | 443.0 | 65529.0 |
| 2 | Flow Duration | 362076.0 | 13020771.852417724 | 32462831.452398483 | 0.0 | 168.0 | 31689.0 | 1505558.5 | 119999993.0 |
| 3 | Total Fwd Packet | 362076.0 | 11.912095803091065 | 773.2711764855231 | 0.0 | 2.0 | 2.0 | 5.0 | 200754.0 |
| 4 | Total Bwd packets | 362076.0 | 13.702264165534308 | 1029.9828738748752 | 0.0 | 1.0 | 2.0 | 4.0 | 270687.0 |
| 5 | Total Length of Fwd Packet | 362076.0 | 579.8800528065931 | 23157.062105841494 | 0.0 | 41.0 | 70.0 | 168.0 | 12870252.0 |
| 6 | Total Length of Bwd Packet | 362076.0 | 19978.44286006253 | 2380134.340879873 | 0.0 | 32.0 | 158.0 | 374.0 | 627040563.0 |
| 7 | Fwd Packet Length Max | 362076.0 | 179.31448369955478 | 472.93377431988523 | 0.0 | 27.0 | 42.0 | 71.0 | 23360.0 |
| 8 | Fwd Packet Length Min | 362076.0 | 22.417202465780665 | 31.83355311755449 | 0.0 | 0.0 | 26.0 | 42.0 | 1472.0 |
| 9 | Fwd Packet Length Mean | 362076.0 | 45.21170361684281 | 80.59824055194558 | 0.0 | 15.125 | 38.0 | 50.0 | 4213.595238095238 |
| 10 | Fwd Packet Length Std | 362076.0 | 48.022730670125306 | 140.7607919936273 | 0.0 | 0.0 | 0.0 | 19.091883092036785 | 5437.255476783823 |
| 11 | Bwd Packet Length Max | 362076.0 | 448.7274025342746 | 855.6035580635668 | 0.0 | 23.0 | 99.0 | 206.0 | 13140.0 |
| 12 | Bwd Packet Length Min | 362076.0 | 55.3784481711022 | 71.11294845464714 | 0.0 | 0.0 | 23.0 | 102.0 | 1460.0 |
| 13 | Bwd Packet Length Mean | 362076.0 | 167.41805761940327 | 276.9478756611751 | 0.0 | 10.333333333333332 | 91.0 | 164.0 | 3494.9171641166663 |
| 14 | Bwd Packet Length Std | 362076.0 | 134.6167053125536 | 279.4010379168487 | 0.0 | 0.0 | 0.0 | 26.16295090390226 | 3166.398190373409 |
| 15 | Flow Bytes/s | 362075.0 | 504977.53380074434 | 4560068.049673801 | 0.0 | 4.597840052086594 | 2253.047498949138 | 13181.615404276374 | 242000000.0 |
| 16 | Flow Packets/s | 362075.0 | 53791.52944523979 | 211138.6494804856 | 0.0250000895836543 | 8.26470187168287 | 97.48330598385029 | 23809.52380952381 | 3000000.0 |
| 17 | Flow IAT Mean | 362076.0 | 820435.7806814014 | 3681099.838701481 | 0.0 | 56.0 | 12457.208695652174 | 178650.0 | 69000029.0 |
| 18 | Flow IAT Std | 362076.0 | 1550346.3862572238 | 5682157.2998591745 | 0.0 | 0.0 | 124.41998767615006 | 217717.07327409586 | 84819214.85657084 |
| 19 | Flow IAT Max | 362076.0 | 4442355.071222616 | 13588527.103814734 | 0.0 | 131.0 | 30950.0 | 955913.0 | 119976027.0 |
| 20 | Flow IAT Min | 362076.0 | 75903.62712524443 | 1983378.9405961202 | 0.0 | 2.0 | 3.0 | 48.0 | 69000029.0 |
| 21 | Fwd IAT Total | 362076.0 | 12931440.472389774 | 32447405.301838968 | 0.0 | 1.0 | 21.0 | 1328536.5 | 119999971.0 |
| 22 | Fwd IAT Mean | 362076.0 | 1855531.9878372252 | 9189481.940345766 | 0.0 | 1.0 | 11.0 | 114369.59090909091 | 119999570.0 |
| 23 | Fwd IAT Std | 362076.0 | 1226017.2684021909 | 3767679.23170727 | 0.0 | 0.0 | 0.0 | 56093.97832268332 | 83228041.45824479 |
| 24 | Fwd IAT Max | 362076.0 | 4401823.976250842 | 13591536.08017795 | 0.0 | 1.0 | 12.0 | 902841.75 | 119999570.0 |
| 25 | Fwd IAT Min | 362076.0 | 1090106.3837813055 | 8981575.384590326 | 0.0 | 1.0 | 3.0 | 48.0 | 119999570.0 |
| 26 | Bwd IAT Total | 362076.0 | 12693484.06414123 | 32195117.967998013 | 0.0 | 0.0 | 4.0 | 992949.0 | 119999992.0 |
| 27 | Bwd IAT Mean | 362076.0 | 1957782.7557664488 | 9090314.985365583 | 0.0 | 0.0 | 4.0 | 86754.41666666667 | 119962479.0 |
| 28 | Bwd IAT Std | 362076.0 | 1176506.2204566738 | 3936284.4824607866 | 0.0 | 0.0 | 0.0 | 18043.421965759528 | 83273028.29877065 |
| 29 | Bwd IAT Max | 362076.0 | 4282905.206365515 | 13359976.29813762 | 0.0 | 0.0 | 4.0 | 528981.25 | 119962479.0 |
| 30 | Bwd IAT Min | 362076.0 | 1155627.9546227865 | 8809751.362320388 | 0.0 | 0.0 | 3.0 | 48.0 | 119962479.0 |
| 31 | Fwd PSH Flags | 362076.0 | 1.3013207171974945 | 17.470080052689745 | 0.0 | 0.0 | 0.0 | 1.0 | 5520.0 |
| 32 | Bwd PSH Flags | 362076.0 | 1.8293535058937902 | 40.03834277959399 | 0.0 | 0.0 | 0.0 | 0.0 | 9761.0 |
| 33 | Fwd URG Flags | 362076.0 | 0.0017344424927363317 | 0.12479533221780799 | 0.0 | 0.0 | 0.0 | 0.0 | 16.0 |
| 34 | Bwd URG Flags | 362076.0 | 5.523702206166661e-06 | 0.0033237635915229166 | 0.0 | 0.0 | 0.0 | 0.0 | 2.0 |
| 35 | Fwd RST Flags | 362076.0 | 0.07850009390293751 | 0.6060747777954197 | 0.0 | 0.0 | 0.0 | 0.0 | 173.0 |
| 36 | Bwd RST Flags | 362076.0 | 0.2079646262110717 | 0.5591134113040778 | 0.0 | 0.0 | 0.0 | 0.0 | 10.0 |
| 37 | Fwd Header Length | 362076.0 | 160.7550127597521 | 778.4326751413289 | -32544.0 | 16.0 | 24.0 | 128.0 | 32716.0 |
| 38 | Bwd Header Length | 362076.0 | 164.37751190357827 | 902.375216505146 | -32764.0 | 16.0 | 16.0 | 80.0 | 32616.0 |
| 39 | Fwd Packets/s | 362076.0 | 46334.39270167728 | 204069.8621571031 | 0.0 | 4.122650529662481 | 53.987697386229094 | 11904.761904761905 | 2000000.0 |
| 40 | Bwd Packets/s | 362076.0 | 7456.988179367573 | 34180.45401638111 | 0.0 | 0.563594500829347 | 31.394780399194687 | 8620.689655172413 | 1000000.0 |
| 41 | Packet Length Min | 362076.0 | 22.198124150730784 | 26.176467480231658 | 0.0 | 0.0 | 25.0 | 42.0 | 1359.0 |
| 42 | Packet Length Max | 362076.0 | 483.31613804836553 | 921.641206042455 | 0.0 | 43.0 | 100.0 | 223.0 | 23360.0 |
| 43 | Packet Length Mean | 362076.0 | 107.98674387027826 | 164.35960056593575 | 0.0 | 18.77777777777777 | 66.5 | 109.5 | 1870.5001924069509 |
| 44 | Packet Length Std | 362076.0 | 140.32547366133312 | 244.48790592505702 | 0.0 | 0.0 | 34.06366588218792 | 102.19099764656376 | 3781.768642571413 |
| 45 | Packet Length Variance | 362076.0 | 79465.40961408081 | 227590.35262629823 | 0.0 | 0.0 | 1160.3333333333333 | 10443.0 | 14301774.065936426 |
| 46 | FIN Flag Count | 362076.0 | 0.5162866359548824 | 0.9413997016945279 | 0.0 | 0.0 | 0.0 | 0.0 | 31.0 |
| 47 | SYN Flag Count | 362076.0 | 0.9191219522973078 | 1.104976180743844 | 0.0 | 0.0 | 0.0 | 2.0 | 16.0 |
| 48 | RST Flag Count | 362076.0 | 0.2913034832466112 | 0.8304750184196663 | 0.0 | 0.0 | 0.0 | 0.0 | 173.0 |
| 49 | PSH Flag Count | 362076.0 | 3.1306742230912845 | 44.72129369470565 | 0.0 | 0.0 | 0.0 | 2.0 | 9861.0 |
| 50 | ACK Flag Count | 362076.0 | 22.884040919585942 | 1802.4903218039856 | 0.0 | 0.0 | 0.0 | 9.0 | 471441.0 |
| 51 | URG Flag Count | 362076.0 | 0.0017399661949424983 | 0.12483950971797682 | 0.0 | 0.0 | 0.0 | 0.0 | 16.0 |
| 52 | CWR Flag Count | 362076.0 | 0.0005551320717197495 | 0.03200533419143339 | 0.0 | 0.0 | 0.0 | 0.0 | 4.0 |
| 53 | ECE Flag Count | 362076.0 | 0.0014306388713971653 | 0.11090208318291815 | 0.0 | 0.0 | 0.0 | 0.0 | 14.0 |
| 54 | Down/Up Ratio | 362076.0 | 0.8714594445916495 | 0.36843133104715453 | 0.0 | 0.8695652173913043 | 1.0 | 1.0 | 6.0 |
| 55 | Average Packet Size | 362076.0 | 107.98674387027826 | 164.35960056593575 | 0.0 | 18.77777777777778 | 66.5 | 109.5 | 1870.500192406936 |
| 56 | Fwd Segment Size Avg | 362076.0 | 45.21170361684281 | 80.59824055194558 | 0.0 | 15.125 | 38.0 | 50.0 | 4213.595238095239 |
| 57 | Bwd Segment Size Avg | 362076.0 | 167.41805761940327 | 276.9478756611751 | 0.0 | 10.333333333333334 | 91.0 | 164.0 | 3494.9171641167127 |
| 58 | Fwd Bytes/Bulk Avg | 362076.0 | 90.02107844761873 | 5612.403420830749 | 0.0 | 0.0 | 0.0 | 0.0 | 1827185.0 |
| 59 | Fwd Packet/Bulk Avg | 362076.0 | 0.3067477546150532 | 11.1959818540956 | 0.0 | 0.0 | 0.0 | 0.0 | 3812.0 |
| 60 | Fwd Bulk Rate Avg | 362076.0 | 204026.65970956374 | 4449036.71069329 | 0.0 | 0.0 | 0.0 | 0.0 | 827500000.0 |
| 61 | Bwd Bytes/Bulk Avg | 362076.0 | 3554.5072553828477 | 294901.52629992104 | 0.0 | 0.0 | 0.0 | 0.0 | 156760051.0 |
| 62 | Bwd Packet/Bulk Avg | 362076.0 | 1.9239800483876313 | 112.94545561619931 | 0.0 | 0.0 | 0.0 | 0.0 | 44853.0 |
| 63 | Bwd Bulk Rate Avg | 362076.0 | 348770.9883753687 | 3269941.3665188984 | 0.0 | 0.0 | 0.0 | 0.0 | 644000000.0 |
| 64 | Subflow Fwd Packets | 362076.0 | 0.09558766667771407 | 0.2940253448622198 | 0.0 | 0.0 | 0.0 | 0.0 | 1.0 |
| 65 | Subflow Fwd Bytes | 362076.0 | 23.215457528253737 | 42.71589600040395 | 0.0 | 7.0 | 19.0 | 25.0 | 1701.0 |
| 66 | Subflow Bwd Packets | 362076.0 | 1.1047404412333323e-05 | 0.003323749821846152 | 0.0 | 0.0 | 0.0 | 0.0 | 1.0 |
| 67 | Subflow Bwd Bytes | 362076.0 | 84.28276107778477 | 153.96540562394503 | 0.0 | 4.0 | 43.0 | 80.0 | 1870.0 |
| 68 | FWD Init Win Bytes | 362076.0 | 5715.424891459252 | 12018.829148231971 | 0.0 | 0.0 | 0.0 | 8192.0 | 65535.0 |
| 69 | Bwd Init Win Bytes | 362076.0 | 784.3371916393244 | 4535.01180960261 | 0.0 | 0.0 | 0.0 | 58.0 | 65535.0 |
| 70 | Fwd Act Data Pkts | 362076.0 | 2.233489654105768 | 23.484521018678922 | 0.0 | 0.0 | 1.0 | 2.0 | 9130.0 |
| 71 | Fwd Seg Size Min | 362076.0 | 15.965421624189396 | 8.792564803633761 | 0.0 | 8.0 | 8.0 | 24.0 | 44.0 |
| 72 | Active Mean | 362076.0 | 95356.7097611852 | 671013.5287923649 | 0.0 | 0.0 | 0.0 | 0.0 | 103276216.0 |
| 73 | Active Std | 362076.0 | 56182.34520149551 | 423595.5122664568 | 0.0 | 0.0 | 0.0 | 0.0 | 63746213.01801418 |
| 74 | Active Max | 362076.0 | 196407.08020415602 | 1100155.039209817 | 0.0 | 0.0 | 0.0 | 0.0 | 103276216.0 |
| 75 | Active Min | 362076.0 | 64865.93132933418 | 599381.629041123 | 0.0 | 0.0 | 0.0 | 0.0 | 103276216.0 |
| 76 | Idle Mean | 362076.0 | 4126641.3719004807 | 13262962.307205953 | 0.0 | 0.0 | 0.0 | 0.0 | 119976027.0 |
| 77 | Idle Std | 362076.0 | 201064.50299171996 | 2039004.3103911194 | 0.0 | 0.0 | 0.0 | 0.0 | 76469325.3390464 |
| 78 | Idle Max | 362076.0 | 4271094.412504557 | 13622146.464099329 | 0.0 | 0.0 | 0.0 | 0.0 | 119976027.0 |
| 79 | Idle Min | 362076.0 | 3890512.7511958815 | 13065520.14571796 | 0.0 | 0.0 | 0.0 | 0.0 | 119976027.0 |
| 80 | ICMP Code | 362076.0 | -0.9975557617737713 | 0.13563292523260206 | -1.0 | -1.0 | -1.0 | -1.0 | 10.0 |
| 81 | ICMP Type | 362076.0 | -0.9971580552149273 | 0.14398166736794904 | -1.0 | -1.0 | -1.0 | -1.0 | 8.0 |
| 82 | Total TCP Flow Time | 362076.0 | 20025083.73091561 | 139667155.7821223 | 0.0 | 0.0 | 0.0 | 451037.25 | 28579656406.0 |

## Distribution Analysis
 Distribution of target variable 'Label':

Distribution Analysis

| # | Class | Percentage |
|---|---|---|
| 1 | BENIGN | 0.7959 |
| 2 | Infiltration | 0.0001 |
| 3 | Infiltration - Attempted | 0.0001 |
| 4 | Infiltration - Portscan | 0.1982 |
| 5 | Web Attack - Brute Force | 0.0002 |
| 6 | Web Attack - Brute Force - Attempted | 0.0036 |
| 7 | Web Attack - SQL Injection | 0.0000 |
| 8 | Web Attack - SQL Injection - Attempted | 0.0000 |
| 9 | Web Attack - XSS | 0.0000 |
| 10 | Web Attack - XSS - Attempted | 0.0018 |

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
| 22 | Fwd URG Flags | fwd_urg_flags |
| 23 | Bwd URG Flags | bwd_urg_flags |
| 24 | Fwd RST Flags | fwd_rst_flags |
| 25 | Bwd RST Flags | bwd_rst_flags |
| 26 | Fwd Header Length | fwd_header_length |
| 27 | Bwd Header Length | bwd_header_length |
| 28 | Bwd Packets/s | bwd_packets/s |
| 29 | Packet Length Min | packet_length_min |
| 30 | Packet Length Max | packet_length_max |
| 31 | Packet Length Variance | packet_length_variance |
| 32 | FIN Flag Count | fin_flag_count |
| 33 | SYN Flag Count | syn_flag_count |
| 34 | RST Flag Count | rst_flag_count |
| 35 | PSH Flag Count | psh_flag_count |
| 36 | CWR Flag Count | cwr_flag_count |
| 37 | ECE Flag Count | ece_flag_count |
| 38 | Down/Up Ratio | down/up_ratio |
| 39 | Fwd Bytes/Bulk Avg | fwd_bytes/bulk_avg |
| 40 | Fwd Bulk Rate Avg | fwd_bulk_rate_avg |
| 41 | Bwd Bytes/Bulk Avg | bwd_bytes/bulk_avg |
| 42 | Bwd Packet/Bulk Avg | bwd_packet/bulk_avg |
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
| 53 | Active Min | active_min |
| 54 | Idle Std | idle_std |
| 55 | ICMP Code | icmp_code |
| 56 | ICMP Type | icmp_type |
| 57 | Total TCP Flow Time | total_tcp_flow_time |

## Recommendation
 Based on the assessment, it is recommended to continue working with the available columns. You may consider the following:
- Performing further analysis using the available columns: `['Dst Port', 'Flow Duration', 'Total Fwd Packet', 'Total Length of Fwd Packet', 'Fwd Packet Length Max', 'Fwd Packet Length Min', 'Fwd Packet Length Mean', 'Bwd Packet Length Max', 'Bwd Packet Length Min', 'Bwd Packet Length Mean', 'Bwd Packet Length Std', 'Flow Bytes/s', 'Flow Packets/s', 'Flow IAT Mean', 'Flow IAT Std', 'Flow IAT Max', 'Flow IAT Min', 'Fwd IAT Mean', 'Fwd IAT Std', 'Fwd PSH Flags', 'Bwd PSH Flags', 'Fwd URG Flags', 'Bwd URG Flags', 'Fwd RST Flags', 'Bwd RST Flags', 'Fwd Header Length', 'Bwd Header Length', 'Bwd Packets/s', 'Packet Length Min', 'Packet Length Max', 'Packet Length Variance', 'FIN Flag Count', 'SYN Flag Count', 'RST Flag Count', 'PSH Flag Count', 'CWR Flag Count', 'ECE Flag Count', 'Down/Up Ratio', 'Fwd Bytes/Bulk Avg', 'Fwd Bulk Rate Avg', 'Bwd Bytes/Bulk Avg', 'Bwd Packet/Bulk Avg', 'Bwd Bulk Rate Avg', 'Subflow Fwd Packets', 'Subflow Bwd Packets', 'FWD Init Win Bytes', 'Bwd Init Win Bytes', 'Fwd Act Data Pkts', 'Fwd Seg Size Min', 'Active Mean', 'Active Std', 'Active Max', 'Active Min', 'Idle Std', 'ICMP Code', 'ICMP Type', 'Total TCP Flow Time']`
- Train machine learning models with the reduced feature set.
## End of Report ✅  
 
✅ Report Successfully Generated in  00:16 minutes

