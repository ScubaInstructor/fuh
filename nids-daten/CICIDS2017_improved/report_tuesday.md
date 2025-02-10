# Data Assessment Report on dataset: tuesday.csv
## Command line executed  
 ```dataset_assessment_prepare.py --drop-columns id,Protocol,Attempted Category,Src Port --drop-highly-correlated --correlation-threshold 0.95 --drop-categorical-columns --impute-strategy mean --assess-only --zero-variance --low-variance-threshold=0.01 --low-variance-sample-percentage=100 --missing-threshold=0.05 --descriptive-statistics --distribution-analysis --distribution-column Label -output . -input CICIDS2017_improved/tuesday.csv```  
# Report  
 ### Options used to generate this report  

| # | Option | Value |
|---|---|---|
| 1 | -input | CICIDS2017_improved/tuesday.csv |
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
 
✅ Dataset Loaded Successfully: `.../DATASET_engelen_improved/CICIDS2017_improved/tuesday.csv
- File Size: 170.13 MB
- Number of Records: 322,078
- File loaded in 00:06 minutes

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
 Found 644052 negative values:

### Columns with Negative Values

| # | Column | Negative Count |
|---|---|---|
| 1 | Fwd Header Length | 60 |
| 2 | Bwd Header Length | 82 |
| 3 | ICMP Code | 321955 |
| 4 | ICMP Type | 321955 |

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
 ️Found 23 highly correlated features (threshold: 0.95):

### Highly Correlated Features

| # | Feature 1 | Feature 2 | Correlation |
|---|---|---|---|
| 1 | Total Bwd packets | Total Fwd Packet | 0.9995 |
| 2 | Total Length of Bwd Packet | Total Fwd Packet | 0.9982 |
| 3 | Total Length of Bwd Packet | Total Bwd packets | 0.9971 |
| 4 | Fwd IAT Total | Flow Duration | 0.9995 |
| 5 | Fwd IAT Max | Flow IAT Max | 0.9984 |
| 6 | Fwd IAT Min | Fwd IAT Mean | 0.9717 |
| 7 | Bwd IAT Total | Flow Duration | 0.9873 |
| 8 | Bwd IAT Total | Fwd IAT Total | 0.9867 |
| 9 | Bwd IAT Mean | Flow IAT Std | 0.9625 |
| 10 | Bwd IAT Mean | Fwd IAT Mean | 0.9508 |
| 11 | Bwd IAT Max | Flow IAT Max | 0.9707 |
| 12 | Bwd IAT Max | Fwd IAT Max | 0.9691 |
| 13 | Bwd IAT Min | Bwd IAT Mean | 0.9637 |
| 14 | Fwd Packets/s | Flow Packets/s | 0.9903 |
| 15 | Packet Length Mean | Bwd Packet Length Mean | 0.9617 |
| 16 | Packet Length Std | Packet Length Max | 0.9642 |
| 17 | PSH Flag Count | Bwd PSH Flags | 0.9795 |
| 18 | ACK Flag Count | Total Fwd Packet | 0.9998 |
| 19 | ACK Flag Count | Total Bwd packets | 0.9999 |
| 20 | ACK Flag Count | Total Length of Bwd Packet | 0.9977 |
| 21 | Average Packet Size | Bwd Packet Length Mean | 0.9617 |
| 22 | Average Packet Size | Packet Length Mean | 1.0000 |
| 23 | Fwd Segment Size Avg | Fwd Packet Length Mean | 1.0000 |
| 24 | Bwd Segment Size Avg | Bwd Packet Length Mean | 1.0000 |
| 25 | Bwd Segment Size Avg | Packet Length Mean | 0.9617 |
| 26 | Bwd Segment Size Avg | Average Packet Size | 0.9617 |
| 27 | Bwd Packet/Bulk Avg | Bwd Bytes/Bulk Avg | 0.9952 |
| 28 | Subflow Fwd Bytes | Fwd Packet Length Mean | 0.9787 |
| 29 | Subflow Fwd Bytes | Fwd Segment Size Avg | 0.9787 |
| 30 | Subflow Bwd Bytes | Bwd Packet Length Mean | 0.9867 |
| 31 | Subflow Bwd Bytes | Packet Length Mean | 0.9707 |
| 32 | Subflow Bwd Bytes | Average Packet Size | 0.9707 |
| 33 | Subflow Bwd Bytes | Bwd Segment Size Avg | 0.9867 |
| 34 | Idle Mean | Flow IAT Max | 0.9907 |
| 35 | Idle Mean | Fwd IAT Max | 0.9891 |
| 36 | Idle Mean | Bwd IAT Max | 0.9631 |
| 37 | Idle Max | Flow IAT Max | 0.9984 |
| 38 | Idle Max | Fwd IAT Max | 0.9968 |
| 39 | Idle Max | Bwd IAT Max | 0.9690 |
| 40 | Idle Max | Idle Mean | 0.9923 |
| 41 | Idle Min | Flow IAT Max | 0.9686 |
| 42 | Idle Min | Fwd IAT Max | 0.9671 |
| 43 | Idle Min | Idle Mean | 0.9921 |
| 44 | Idle Min | Idle Max | 0.9701 |

💡 To drop these features, use:
```python
df_numeric.drop(columns=['Total Bwd packets', 'Total Length of Bwd Packet', 'Fwd IAT Total', 'Fwd IAT Max', 'Fwd IAT Min', 'Bwd IAT Total', 'Bwd IAT Mean', 'Bwd IAT Max', 'Bwd IAT Min', 'Fwd Packets/s', 'Packet Length Mean', 'Packet Length Std', 'PSH Flag Count', 'ACK Flag Count', 'Average Packet Size', 'Fwd Segment Size Avg', 'Bwd Segment Size Avg', 'Bwd Packet/Bulk Avg', 'Subflow Fwd Bytes', 'Subflow Bwd Bytes', 'Idle Mean', 'Idle Max', 'Idle Min'], inplace=True)
```
## Descriptive Statistics Analysis
 Descriptive Statistics for Features

| # | Column | Count | Mean | Std | Min | 25% | 50% | 75% | Max |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Dst Port | 322078.0 | 278.0800271983805 | 2297.7545104783753 | 0.0 | 53.0 | 53.0 | 389.0 | 65282.0 |
| 2 | Flow Duration | 322078.0 | 14953434.846577536 | 33928147.093522385 | 1.0 | 23658.0 | 73053.0 | 5450367.0 | 119999977.0 |
| 3 | Total Fwd Packet | 322078.0 | 16.144353231204864 | 1020.2018279454387 | 0.0 | 2.0 | 2.0 | 10.0 | 206445.0 |
| 4 | Total Bwd packets | 322078.0 | 19.570753047398455 | 1379.1802465037392 | 0.0 | 2.0 | 2.0 | 8.0 | 276073.0 |
| 5 | Total Length of Fwd Packet | 322078.0 | 666.1271990014841 | 6448.244704083629 | 0.0 | 62.0 | 88.0 | 438.0 | 2429858.0 |
| 6 | Total Length of Bwd Packet | 322078.0 | 30334.797623557028 | 3089195.5993432156 | 0.0 | 118.0 | 206.0 | 860.0 | 627039032.0 |
| 7 | Fwd Packet Length Max | 322078.0 | 227.49490806574804 | 519.9255589274045 | 0.0 | 37.0 | 47.0 | 239.0 | 24820.0 |
| 8 | Fwd Packet Length Min | 322078.0 | 28.040723054663776 | 40.22601448422656 | 0.0 | 0.0 | 34.0 | 44.0 | 1472.0 |
| 9 | Fwd Packet Length Mean | 322078.0 | 56.94128396699588 | 88.7996844500946 | 0.0 | 34.0 | 43.0 | 54.0 | 4080.837837837837 |
| 10 | Fwd Packet Length Std | 322078.0 | 60.368545809944656 | 153.3268275534427 | 0.0 | 0.0 | 0.0 | 76.716107246856 | 5367.047628887855 |
| 11 | Bwd Packet Length Max | 322078.0 | 593.863809387788 | 995.0733956798124 | 0.0 | 73.0 | 122.0 | 677.0 | 13140.0 |
| 12 | Bwd Packet Length Min | 322078.0 | 68.72602909854135 | 77.66521863102156 | 0.0 | 0.0 | 63.0 | 111.0 | 1454.0 |
| 13 | Bwd Packet Length Mean | 322078.0 | 220.92988156960345 | 325.3037823335335 | 0.0 | 67.0 | 110.5 | 198.0 | 3647.1686746987934 |
| 14 | Bwd Packet Length Std | 322078.0 | 172.29808729565352 | 313.1240688281739 | 0.0 | 0.0 | 0.0 | 214.44322676283423 | 3608.0101163937993 |
| 15 | Flow Bytes/s | 322078.0 | 560336.4713820717 | 4410038.420251536 | 0.0 | 429.65156142221724 | 4615.594081171238 | 102780.38905077521 | 169722222.2222222 |
| 16 | Flow Packets/s | 322078.0 | 7601.301677393641 | 48165.09719719831 | 0.0250006650176894 | 3.099610522904685 | 60.45316556545524 | 250.2796103991236 | 2000000.0 |
| 17 | Flow IAT Mean | 322078.0 | 1129020.4694869986 | 4765210.767399479 | 0.6666666666666667 | 4413.31043956044 | 30239.0 | 345147.34259259264 | 68000063.0 |
| 18 | Flow IAT Std | 322078.0 | 1958877.7356622126 | 6646530.640199431 | 0.0 | 79.18543637142712 | 17877.65108545676 | 1114849.0224959385 | 84789254.74225196 |
| 19 | Flow IAT Max | 322078.0 | 5487474.377933295 | 15515957.878273025 | 1.0 | 23521.0 | 60484.0 | 4527036.0 | 119946588.0 |
| 20 | Flow IAT Min | 322078.0 | 169747.8813796658 | 3091179.8025888717 | 0.0 | 3.0 | 3.0 | 49.0 | 68000063.0 |
| 21 | Fwd IAT Total | 322078.0 | 14869298.02133955 | 33908811.4922009 | 0.0 | 3.0 | 48.0 | 5413085.0 | 119999944.0 |
| 22 | Fwd IAT Mean | 322078.0 | 2524837.68551488 | 11032845.81833541 | 0.0 | 3.0 | 48.0 | 683381.8267045454 | 119996808.0 |
| 23 | Fwd IAT Std | 322078.0 | 1444614.20288126 | 4365725.967259699 | 0.0 | 0.0 | 0.0 | 995811.927969762 | 82650622.30336854 |
| 24 | Fwd IAT Max | 322078.0 | 5451398.431746347 | 15515638.09085146 | 0.0 | 3.0 | 48.0 | 4393242.0 | 119996808.0 |
| 25 | Fwd IAT Min | 322078.0 | 1620914.0875129628 | 10804699.722906236 | 0.0 | 1.0 | 3.0 | 48.0 | 119996808.0 |
| 26 | Bwd IAT Total | 322078.0 | 14472660.168300847 | 33595634.94018706 | 0.0 | 3.0 | 48.0 | 5282134.75 | 119999977.0 |
| 27 | Bwd IAT Mean | 322078.0 | 2548951.526160635 | 10744930.494093629 | 0.0 | 3.0 | 48.0 | 596261.703125 | 119976977.0 |
| 28 | Bwd IAT Std | 322078.0 | 1389113.5985696586 | 4549326.405862196 | 0.0 | 0.0 | 0.0 | 299064.5088606472 | 84463479.33445083 |
| 29 | Bwd IAT Max | 322078.0 | 5221740.789296381 | 15175228.848017154 | 0.0 | 3.0 | 48.0 | 4056169.0 | 119976977.0 |
| 30 | Bwd IAT Min | 322078.0 | 1606968.6548631077 | 10444445.107184732 | 0.0 | 1.0 | 3.0 | 48.0 | 119976977.0 |
| 31 | Fwd PSH Flags | 322078.0 | 1.78676593868566 | 6.104920558158789 | 0.0 | 0.0 | 0.0 | 3.0 | 1593.0 |
| 32 | Bwd PSH Flags | 322078.0 | 2.3053452890293658 | 25.30494621906385 | 0.0 | 0.0 | 0.0 | 2.0 | 4786.0 |
| 33 | Fwd URG Flags | 322078.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| 34 | Bwd URG Flags | 322078.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| 35 | Fwd RST Flags | 322078.0 | 0.10980880407851515 | 0.5835402024349801 | 0.0 | 0.0 | 0.0 | 0.0 | 110.0 |
| 36 | Bwd RST Flags | 322078.0 | 0.06425462155130124 | 0.3216962129152078 | 0.0 | 0.0 | 0.0 | 0.0 | 6.0 |
| 37 | Fwd Header Length | 322078.0 | 202.67592322356697 | 778.952456657456 | -32632.0 | 16.0 | 16.0 | 220.0 | 32740.0 |
| 38 | Bwd Header Length | 322078.0 | 226.98294202025596 | 963.5264283662074 | -32444.0 | 16.0 | 16.0 | 200.0 | 32652.0 |
| 39 | Fwd Packets/s | 322078.0 | 5457.8069670622035 | 47282.07250741149 | 0.0 | 1.5874543920549737 | 31.002945279801583 | 124.51386124001421 | 2000000.0 |
| 40 | Bwd Packets/s | 322078.0 | 2143.4947103314353 | 6690.066796289713 | 0.0 | 1.3978738689492642 | 27.117745261938417 | 100.26311333623688 | 2000000.0 |
| 41 | Packet Length Min | 322078.0 | 27.48435782636504 | 27.29644667241375 | 0.0 | 0.0 | 34.0 | 44.0 | 1408.0 |
| 42 | Packet Length Max | 322078.0 | 634.3423487478188 | 1059.6937906728785 | 0.0 | 75.0 | 123.0 | 825.0 | 24820.0 |
| 43 | Packet Length Mean | 322078.0 | 143.0393103359617 | 193.17625736655094 | 0.0 | 56.0 | 79.5 | 132.0 | 2125.666666666667 |
| 44 | Packet Length Std | 322078.0 | 181.29548957221795 | 274.7118270379458 | 0.0 | 21.361959960016154 | 46.66904755831214 | 206.68589644937202 | 3795.835519524016 |
| 45 | Packet Length Variance | 322078.0 | 108334.40814222964 | 286350.9428496925 | 0.0 | 456.3333333333333 | 2178.0 | 42719.05987847287 | 14408367.291280152 |
| 46 | FIN Flag Count | 322078.0 | 0.6831109234409056 | 1.0428112626747978 | 0.0 | 0.0 | 0.0 | 2.0 | 16.0 |
| 47 | SYN Flag Count | 322078.0 | 0.7073876514384714 | 1.028741545652906 | 0.0 | 0.0 | 0.0 | 2.0 | 11.0 |
| 48 | RST Flag Count | 322078.0 | 0.17407894981960892 | 0.6762008124038331 | 0.0 | 0.0 | 0.0 | 0.0 | 110.0 |
| 49 | PSH Flag Count | 322078.0 | 4.092111227715026 | 28.14425366986644 | 0.0 | 0.0 | 0.0 | 5.0 | 4899.0 |
| 50 | ACK Flag Count | 322078.0 | 32.783409608852516 | 2399.098898743332 | 0.0 | 0.0 | 0.0 | 16.0 | 482518.0 |
| 51 | URG Flag Count | 322078.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| 52 | CWR Flag Count | 322078.0 | 0.0005029837492781251 | 0.022696953714599944 | 0.0 | 0.0 | 0.0 | 0.0 | 2.0 |
| 53 | ECE Flag Count | 322078.0 | 0.0007886288414607641 | 0.037865784729120555 | 0.0 | 0.0 | 0.0 | 0.0 | 2.0 |
| 54 | Down/Up Ratio | 322078.0 | 0.9651782452555107 | 0.2760918591326539 | 0.0 | 1.0 | 1.0 | 1.0 | 16.928571428571427 |
| 55 | Average Packet Size | 322078.0 | 143.0393103359617 | 193.17625736655094 | 0.0 | 56.0 | 79.5 | 132.0 | 2125.6666666666665 |
| 56 | Fwd Segment Size Avg | 322078.0 | 56.9412839669959 | 88.7996844500946 | 0.0 | 34.0 | 43.0 | 54.0 | 4080.837837837838 |
| 57 | Bwd Segment Size Avg | 322078.0 | 220.92988156960345 | 325.3037823335335 | 0.0 | 67.0 | 110.5 | 198.0 | 3647.1686746987953 |
| 58 | Fwd Bytes/Bulk Avg | 322078.0 | 78.19335378386602 | 1425.5308799990908 | 0.0 | 0.0 | 0.0 | 0.0 | 340252.0 |
| 59 | Fwd Packet/Bulk Avg | 322078.0 | 0.2626786058035631 | 1.8457852516247537 | 0.0 | 0.0 | 0.0 | 0.0 | 324.0 |
| 60 | Fwd Bulk Rate Avg | 322078.0 | 234127.27294940976 | 4771019.75724208 | 0.0 | 0.0 | 0.0 | 0.0 | 974000000.0 |
| 61 | Bwd Bytes/Bulk Avg | 322078.0 | 5233.445109569731 | 355308.66525781294 | 0.0 | 0.0 | 0.0 | 0.0 | 156759758.0 |
| 62 | Bwd Packet/Bulk Avg | 322078.0 | 2.8467545128819727 | 138.911208160424 | 0.0 | 0.0 | 0.0 | 0.0 | 57208.0 |
| 63 | Bwd Bulk Rate Avg | 322078.0 | 525082.8464812872 | 6512939.831860523 | 0.0 | 0.0 | 0.0 | 0.0 | 1369000000.0 |
| 64 | Subflow Fwd Packets | 322078.0 | 0.0137233837766007 | 0.11634042521237462 | 0.0 | 0.0 | 0.0 | 0.0 | 1.0 |
| 65 | Subflow Fwd Bytes | 322078.0 | 29.112050497084557 | 46.38175781956355 | 0.0 | 17.0 | 22.0 | 28.0 | 1552.0 |
| 66 | Subflow Bwd Packets | 322078.0 | 1.8629027751041673e-05 | 0.004316102240399467 | 0.0 | 0.0 | 0.0 | 0.0 | 1.0 |
| 67 | Subflow Bwd Bytes | 322078.0 | 113.30654996615726 | 186.21305716487177 | 0.0 | 32.0 | 54.0 | 97.0 | 2059.0 |
| 68 | FWD Init Win Bytes | 322078.0 | 8599.64020827253 | 16413.001471159976 | 0.0 | 0.0 | 0.0 | 8192.0 | 65535.0 |
| 69 | Bwd Init Win Bytes | 322078.0 | 868.0640155490285 | 4840.160540815546 | 0.0 | 0.0 | 0.0 | 119.0 | 65535.0 |
| 70 | Fwd Act Data Pkts | 322078.0 | 2.852054471277144 | 7.270161630132438 | 0.0 | 1.0 | 1.0 | 3.0 | 1850.0 |
| 71 | Fwd Seg Size Min | 322078.0 | 14.327932985177503 | 9.044143190056033 | 0.0 | 8.0 | 8.0 | 20.0 | 44.0 |
| 72 | Active Mean | 322078.0 | 115590.25909582498 | 791217.3952848449 | 0.0 | 0.0 | 0.0 | 0.0 | 106879332.0 |
| 73 | Active Std | 322078.0 | 65896.99699937334 | 428348.2504942497 | 0.0 | 0.0 | 0.0 | 0.0 | 24126232.35117768 |
| 74 | Active Max | 322078.0 | 244511.91845453586 | 1272460.5499752697 | 0.0 | 0.0 | 0.0 | 0.0 | 106879332.0 |
| 75 | Active Min | 322078.0 | 81150.41899477766 | 730803.366290342 | 0.0 | 0.0 | 0.0 | 0.0 | 106879332.0 |
| 76 | Idle Mean | 322078.0 | 5014215.560981417 | 15148484.118530061 | 0.0 | 0.0 | 0.0 | 0.0 | 119946588.0 |
| 77 | Idle Std | 322078.0 | 258919.84914172182 | 2481932.182665282 | 0.0 | 0.0 | 0.0 | 0.0 | 75935267.38620608 |
| 78 | Idle Max | 322078.0 | 5205981.008479312 | 15584460.30303337 | 0.0 | 0.0 | 0.0 | 0.0 | 119946588.0 |
| 79 | Idle Min | 322078.0 | 4729819.315578835 | 14934504.828645881 | 0.0 | 0.0 | 0.0 | 0.0 | 119946588.0 |
| 80 | ICMP Code | 322078.0 | -0.9981277827110203 | 0.10723784380613187 | -1.0 | -1.0 | -1.0 | -1.0 | 10.0 |
| 81 | ICMP Type | 322078.0 | -0.9984724197244146 | 0.07815373673225066 | -1.0 | -1.0 | -1.0 | -1.0 | 3.0 |
| 82 | Total TCP Flow Time | 322078.0 | 48788196.4876738 | 639280868.8906845 | 0.0 | 0.0 | 0.0 | 5254646.0 | 28388744613.0 |

## Distribution Analysis
 Distribution of target variable 'Label':

Distribution Analysis

| # | Class | Percentage |
|---|---|---|
| 1 | BENIGN | 0.9784 |
| 2 | FTP-Patator | 0.0123 |
| 3 | FTP-Patator - Attempted | 0.0000 |
| 4 | SSH-Patator | 0.0092 |
| 5 | SSH-Patator - Attempted | 0.0001 |

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
| 11 | Bwd Packet Length Mean | bwd_packet_length_mean |
| 12 | Bwd Packet Length Std | bwd_packet_length_std |
| 13 | Flow Bytes/s | flow_bytes/s |
| 14 | Flow Packets/s | flow_packets/s |
| 15 | Flow IAT Mean | flow_iat_mean |
| 16 | Flow IAT Std | flow_iat_std |
| 17 | Flow IAT Max | flow_iat_max |
| 18 | Flow IAT Min | flow_iat_min |
| 19 | Fwd IAT Mean | fwd_iat_mean |
| 20 | Fwd IAT Std | fwd_iat_std |
| 21 | Bwd IAT Std | bwd_iat_std |
| 22 | Fwd PSH Flags | fwd_psh_flags |
| 23 | Bwd PSH Flags | bwd_psh_flags |
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
| 35 | CWR Flag Count | cwr_flag_count |
| 36 | ECE Flag Count | ece_flag_count |
| 37 | Down/Up Ratio | down/up_ratio |
| 38 | Fwd Bytes/Bulk Avg | fwd_bytes/bulk_avg |
| 39 | Fwd Packet/Bulk Avg | fwd_packet/bulk_avg |
| 40 | Fwd Bulk Rate Avg | fwd_bulk_rate_avg |
| 41 | Bwd Bytes/Bulk Avg | bwd_bytes/bulk_avg |
| 42 | Bwd Bulk Rate Avg | bwd_bulk_rate_avg |
| 43 | Subflow Fwd Packets | subflow_fwd_packets |
| 44 | Subflow Bwd Packets | subflow_bwd_packets |
| 45 | FWD Init Win Bytes | fwd_init_win_bytes |
| 46 | Bwd Init Win Bytes | bwd_init_win_bytes |
| 47 | Fwd Act Data Pkts | fwd_act_data_pkts |
| 48 | Fwd Seg Size Min | fwd_seg_size_min |
| 49 | Active Mean | active_mean |
| 50 | Active Std | active_std |
| 51 | Active Max | active_max |
| 52 | Active Min | active_min |
| 53 | Idle Std | idle_std |
| 54 | ICMP Code | icmp_code |
| 55 | ICMP Type | icmp_type |
| 56 | Total TCP Flow Time | total_tcp_flow_time |

## Recommendation
 Based on the assessment, it is recommended to continue working with the available columns. You may consider the following:
- Performing further analysis using the available columns: `['Dst Port', 'Flow Duration', 'Total Fwd Packet', 'Total Length of Fwd Packet', 'Fwd Packet Length Max', 'Fwd Packet Length Min', 'Fwd Packet Length Mean', 'Fwd Packet Length Std', 'Bwd Packet Length Max', 'Bwd Packet Length Min', 'Bwd Packet Length Mean', 'Bwd Packet Length Std', 'Flow Bytes/s', 'Flow Packets/s', 'Flow IAT Mean', 'Flow IAT Std', 'Flow IAT Max', 'Flow IAT Min', 'Fwd IAT Mean', 'Fwd IAT Std', 'Bwd IAT Std', 'Fwd PSH Flags', 'Bwd PSH Flags', 'Fwd RST Flags', 'Bwd RST Flags', 'Fwd Header Length', 'Bwd Header Length', 'Bwd Packets/s', 'Packet Length Min', 'Packet Length Max', 'Packet Length Variance', 'FIN Flag Count', 'SYN Flag Count', 'RST Flag Count', 'CWR Flag Count', 'ECE Flag Count', 'Down/Up Ratio', 'Fwd Bytes/Bulk Avg', 'Fwd Packet/Bulk Avg', 'Fwd Bulk Rate Avg', 'Bwd Bytes/Bulk Avg', 'Bwd Bulk Rate Avg', 'Subflow Fwd Packets', 'Subflow Bwd Packets', 'FWD Init Win Bytes', 'Bwd Init Win Bytes', 'Fwd Act Data Pkts', 'Fwd Seg Size Min', 'Active Mean', 'Active Std', 'Active Max', 'Active Min', 'Idle Std', 'ICMP Code', 'ICMP Type', 'Total TCP Flow Time']`
- Train machine learning models with the reduced feature set.
## End of Report ✅  
 
✅ Report Successfully Generated in  00:12 minutes

