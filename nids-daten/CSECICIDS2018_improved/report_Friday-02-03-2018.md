# Data Assessment Report on dataset: Friday-02-03-2018.csv
## Command line executed  
 ```dataset_assessment_prepare.py --drop-columns id,Protocol,Attempted Category,Src Port --drop-highly-correlated --correlation-threshold 0.95 --drop-categorical-columns --impute-strategy mean --assess-only --zero-variance --low-variance-threshold=0.01 --low-variance-sample-percentage=100 --missing-threshold=0.05 --descriptive-statistics --distribution-analysis --distribution-column Label -output . -input CSECICIDS2018_improved/Friday-02-03-2018.csv```  
# Report  
 ### Options used to generate this report  

| # | Option | Value |
|---|---|---|
| 1 | -input | CSECICIDS2018_improved/Friday-02-03-2018.csv |
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
 
✅ Dataset Loaded Successfully: `.../DATASET_engelen_improved/CSECICIDS2018_improved/Friday-02-03-2018.csv
- File Size: 3518.90 MB
- Number of Records: 6,311,371
- File loaded in 05:08 minutes

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
 Found 12598378 negative values:

### Columns with Negative Values

| # | Column | Negative Count |
|---|---|---|
| 1 | Fwd Header Length | 810 |
| 2 | Bwd Header Length | 1880 |
| 3 | ICMP Code | 6297844 |
| 4 | ICMP Type | 6297844 |

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
 ️Found 21 highly correlated features (threshold: 0.95):

### Highly Correlated Features

| # | Feature 1 | Feature 2 | Correlation |
|---|---|---|---|
| 1 | Total Length of Bwd Packet | Total Bwd packets | 0.9945 |
| 2 | Fwd Packet Length Std | Fwd Packet Length Max | 0.9705 |
| 3 | Bwd Packet Length Std | Bwd Packet Length Max | 0.9679 |
| 4 | Bwd IAT Total | Flow Duration | 0.9947 |
| 5 | Bwd IAT Std | Flow IAT Max | 0.9536 |
| 6 | Bwd IAT Max | Flow IAT Max | 0.9948 |
| 7 | Bwd IAT Max | Bwd IAT Std | 0.9587 |
| 8 | Fwd Packets/s | Flow Packets/s | 0.9635 |
| 9 | Packet Length Min | Fwd Packet Length Min | 0.9917 |
| 10 | ACK Flag Count | Total Bwd packets | 0.9679 |
| 11 | ACK Flag Count | Total Length of Bwd Packet | 0.9649 |
| 12 | Average Packet Size | Packet Length Mean | 1.0000 |
| 13 | Fwd Segment Size Avg | Fwd Packet Length Mean | 1.0000 |
| 14 | Bwd Segment Size Avg | Bwd Packet Length Mean | 1.0000 |
| 15 | Fwd Bytes/Bulk Avg | Total Length of Fwd Packet | 0.9834 |
| 16 | Fwd Packet/Bulk Avg | Total Length of Fwd Packet | 0.9776 |
| 17 | Fwd Packet/Bulk Avg | Fwd Bytes/Bulk Avg | 0.9928 |
| 18 | Bwd Packet/Bulk Avg | Bwd Bytes/Bulk Avg | 0.9993 |
| 19 | Subflow Fwd Bytes | Fwd Packet Length Mean | 0.9864 |
| 20 | Subflow Fwd Bytes | Fwd Segment Size Avg | 0.9864 |
| 21 | Subflow Bwd Bytes | Bwd Packet Length Mean | 0.9744 |
| 22 | Subflow Bwd Bytes | Bwd Segment Size Avg | 0.9744 |
| 23 | Active Min | Active Mean | 0.9824 |
| 24 | Idle Mean | Flow IAT Max | 0.9925 |
| 25 | Idle Mean | Bwd IAT Max | 0.9881 |
| 26 | Idle Max | Flow IAT Max | 0.9996 |
| 27 | Idle Max | Bwd IAT Std | 0.9533 |
| 28 | Idle Max | Bwd IAT Max | 0.9944 |
| 29 | Idle Max | Idle Mean | 0.9928 |
| 30 | Idle Min | Flow IAT Max | 0.9715 |
| 31 | Idle Min | Bwd IAT Max | 0.9677 |
| 32 | Idle Min | Idle Mean | 0.9928 |
| 33 | Idle Min | Idle Max | 0.9717 |

💡 To drop these features, use:
```python
df_numeric.drop(columns=['Total Length of Bwd Packet', 'Fwd Packet Length Std', 'Bwd Packet Length Std', 'Bwd IAT Total', 'Bwd IAT Std', 'Bwd IAT Max', 'Fwd Packets/s', 'Packet Length Min', 'ACK Flag Count', 'Average Packet Size', 'Fwd Segment Size Avg', 'Bwd Segment Size Avg', 'Fwd Bytes/Bulk Avg', 'Fwd Packet/Bulk Avg', 'Bwd Packet/Bulk Avg', 'Subflow Fwd Bytes', 'Subflow Bwd Bytes', 'Active Min', 'Idle Mean', 'Idle Max', 'Idle Min'], inplace=True)
```
## Descriptive Statistics Analysis
 Descriptive Statistics for Features

| # | Column | Count | Mean | Std | Min | 25% | 50% | 75% | Max |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Dst Port | 6311371.0 | 1419.3062548533433 | 2176.7887376415338 | 0.0 | 53.0 | 443.0 | 3389.0 | 65463.0 |
| 2 | Flow Duration | 6311371.0 | 19385845.578660645 | 37446912.6569617 | 0.0 | 1809.0 | 528902.0 | 5531690.5 | 120000000.0 |
| 3 | Total Fwd Packet | 6311371.0 | 7.761840177039188 | 69.55771712022074 | 0.0 | 1.0 | 5.0 | 9.0 | 45888.0 |
| 4 | Total Bwd packets | 6311371.0 | 9.516619130772062 | 179.93066872781654 | 0.0 | 1.0 | 5.0 | 8.0 | 122014.0 |
| 5 | Total Length of Fwd Packet | 6311371.0 | 1226.464652767204 | 48062.89247287037 | 0.0 | 42.0 | 286.0 | 1132.0 | 9544313.0 |
| 6 | Total Length of Bwd Packet | 6311371.0 | 6182.339921072617 | 254417.30637680396 | 0.0 | 89.0 | 252.0 | 1581.0 | 156129203.0 |
| 7 | Fwd Packet Length Max | 6311371.0 | 349.10183365864566 | 1098.1865388961965 | 0.0 | 40.0 | 140.0 | 661.0 | 64972.0 |
| 8 | Fwd Packet Length Min | 6311371.0 | 14.531204709721548 | 23.414200958487193 | 0.0 | 0.0 | 0.0 | 35.0 | 3473.0 |
| 9 | Fwd Packet Length Mean | 6311371.0 | 78.96369314042582 | 296.95518899913543 | 0.0 | 35.0 | 49.0 | 107.0 | 31358.14285714286 |
| 10 | Fwd Packet Length Std | 6311371.0 | 107.69925429066986 | 339.0214785426739 | 0.0 | 0.0 | 64.66396656120449 | 194.5379140424817 | 25412.394227522127 |
| 11 | Bwd Packet Length Max | 6311371.0 | 600.3375887742933 | 613.2023407247325 | 0.0 | 79.0 | 181.0 | 1173.0 | 65160.0 |
| 12 | Bwd Packet Length Min | 6311371.0 | 35.56122085043012 | 55.780467107737245 | 0.0 | 0.0 | 0.0 | 66.0 | 1460.0 |
| 13 | Bwd Packet Length Mean | 6311371.0 | 154.5020376723776 | 161.4001001180883 | 0.0 | 58.0 | 126.0 | 218.1875 | 29414.154761904767 |
| 14 | Bwd Packet Length Std | 6311371.0 | 203.05299578014518 | 228.05130005275984 | 0.0 | 0.0 | 61.7980582219215 | 430.0986044197418 | 20916.13861394901 |
| 15 | Flow Bytes/s | 6311368.0 | 83387.53829539787 | 665251.2511217985 | 0.0 | 132.3997723069893 | 1489.0643453111893 | 77770.13076393667 | 598000000.0 |
| 16 | Flow Packets/s | 6311368.0 | 1486.294150962622 | 20476.69779241738 | 0.0166668465297188 | 2.8295640474876285 | 15.713977670449708 | 1142.204454597373 | 5000000.0 |
| 17 | Flow IAT Mean | 6311371.0 | 979237.3328908861 | 2616923.2066499176 | 0.0 | 1384.0000000000002 | 78597.75 | 397434.3701923077 | 119998705.0 |
| 18 | Flow IAT Std | 6311371.0 | 2900969.474155389 | 6246227.849472443 | 0.0 | 0.0 | 106670.25305250625 | 1026754.6014989344 | 84814678.05946276 |
| 19 | Flow IAT Max | 6311371.0 | 11734304.818406492 | 25979847.9743777 | 0.0 | 1790.0 | 250802.0 | 4242059.0 | 119998705.0 |
| 20 | Flow IAT Min | 6311371.0 | 45781.578674427474 | 1433937.951248132 | 0.0 | 3.0 | 34.0 | 381.0 | 119998705.0 |
| 21 | Fwd IAT Total | 6311371.0 | 12270288.355820946 | 31007240.546578337 | 0.0 | 0.0 | 452123.0 | 3923969.0 | 119999994.0 |
| 22 | Fwd IAT Mean | 6311371.0 | 1241817.6026598758 | 4139716.5859967307 | 0.0 | 0.0 | 135819.5 | 354031.625 | 119998705.0 |
| 23 | Fwd IAT Std | 6311371.0 | 1828487.1144033791 | 5404139.408307126 | 0.0 | 0.0 | 100767.4956509621 | 405116.38557570305 | 84752323.96928416 |
| 24 | Fwd IAT Max | 6311371.0 | 4879318.906674636 | 13811589.564370902 | 0.0 | 0.0 | 236082.0 | 1261774.0 | 119998705.0 |
| 25 | Fwd IAT Min | 6311371.0 | 170820.1611437515 | 2927154.3816723106 | 0.0 | 0.0 | 20.0 | 256.0 | 119998705.0 |
| 26 | Bwd IAT Total | 6311371.0 | 19043568.64002623 | 37276688.97358804 | 0.0 | 0.0 | 339858.0 | 5123836.5 | 119999999.0 |
| 27 | Bwd IAT Mean | 6311371.0 | 2301721.6786756883 | 6473946.041510482 | 0.0 | 0.0 | 128037.0 | 704609.2916666667 | 119999898.0 |
| 28 | Bwd IAT Std | 6311371.0 | 3808101.313892021 | 8717278.111966651 | 0.0 | 0.0 | 20424.36599587202 | 774244.3117158574 | 84811458.60228801 |
| 29 | Bwd IAT Max | 6311371.0 | 11588583.15195494 | 25919342.054916903 | 0.0 | 0.0 | 206399.0 | 3014938.0 | 119999898.0 |
| 30 | Bwd IAT Min | 6311371.0 | 589972.8595553961 | 5427408.129166881 | 0.0 | 0.0 | 23.0 | 84649.0 | 119999898.0 |
| 31 | Fwd PSH Flags | 6311371.0 | 2.76288986972878 | 8.415064776061826 | 0.0 | 0.0 | 1.0 | 5.0 | 5247.0 |
| 32 | Bwd PSH Flags | 6311371.0 | 2.7223679292502374 | 13.183593268001083 | 0.0 | 0.0 | 1.0 | 5.0 | 17453.0 |
| 33 | Fwd URG Flags | 6311371.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| 34 | Bwd URG Flags | 6311371.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| 35 | Fwd RST Flags | 6311371.0 | 0.2720304352255635 | 0.44917914433990874 | 0.0 | 0.0 | 0.0 | 1.0 | 10.0 |
| 36 | Bwd RST Flags | 6311371.0 | 0.1904552909344103 | 0.40955050009117844 | 0.0 | 0.0 | 0.0 | 0.0 | 59.0 |
| 37 | Fwd Header Length | 6311371.0 | 142.69616538149953 | 464.0514835358227 | -32768.0 | 8.0 | 112.0 | 192.0 | 32720.0 |
| 38 | Bwd Header Length | 6311371.0 | 144.47855275818836 | 607.1009769307798 | -32764.0 | 8.0 | 112.0 | 172.0 | 32764.0 |
| 39 | Fwd Packets/s | 6311371.0 | 806.9202793680714 | 19113.479669772452 | 0.0 | 1.5439008065718922 | 8.193846748845486 | 569.8005698005697 | 5000000.0 |
| 40 | Bwd Packets/s | 6311371.0 | 679.373165110578 | 5517.316214372611 | 0.0 | 1.3140353168419834 | 7.211696059791516 | 570.1254275940707 | 2000000.0 |
| 41 | Packet Length Min | 6311371.0 | 14.512157659563984 | 23.112772251121292 | 0.0 | 0.0 | 0.0 | 35.0 | 1460.0 |
| 42 | Packet Length Max | 6311371.0 | 655.979734038769 | 1203.9258973460453 | 0.0 | 79.0 | 242.0 | 1173.0 | 65160.0 |
| 43 | Packet Length Mean | 6311371.0 | 117.15854002643779 | 174.6141946246399 | 0.0 | 50.66666666666666 | 83.0 | 160.5294117647059 | 16439.075 |
| 44 | Packet Length Std | 6311371.0 | 184.7412093194607 | 304.0729728925138 | 0.0 | 26.962937525425527 | 97.94729808736112 | 317.73127403515065 | 23620.15303950454 |
| 45 | Packet Length Variance | 6311371.0 | 126589.67261470029 | 4034158.8384312694 | 0.0 | 727.0 | 9593.673202614378 | 100953.1625 | 557911629.6096156 |
| 46 | FIN Flag Count | 6311371.0 | 0.49293980658085224 | 0.8241539489858694 | 0.0 | 0.0 | 0.0 | 1.0 | 19.0 |
| 47 | SYN Flag Count | 6311371.0 | 1.2138037836786968 | 2.9385797897181067 | 0.0 | 0.0 | 2.0 | 2.0 | 3562.0 |
| 48 | RST Flag Count | 6311371.0 | 0.46249729258508177 | 0.5397697095945659 | 0.0 | 0.0 | 0.0 | 1.0 | 59.0 |
| 49 | PSH Flag Count | 6311371.0 | 5.485257798979017 | 17.34406632866832 | 0.0 | 0.0 | 3.0 | 10.0 | 17582.0 |
| 50 | ACK Flag Count | 6311371.0 | 15.58460071512196 | 232.6909400327565 | 0.0 | 0.0 | 9.0 | 16.0 | 134688.0 |
| 51 | URG Flag Count | 6311371.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| 52 | CWR Flag Count | 6311371.0 | 0.39612027244159786 | 0.5629490763059337 | 0.0 | 0.0 | 0.0 | 1.0 | 9.0 |
| 53 | ECE Flag Count | 6311371.0 | 0.5613095791706747 | 0.807545413546251 | 0.0 | 0.0 | 0.0 | 1.0 | 7.0 |
| 54 | Down/Up Ratio | 6311371.0 | 0.9345062964274152 | 0.3423109144996333 | 0.0 | 0.875 | 1.0 | 1.0 | 25.107692307692307 |
| 55 | Average Packet Size | 6311371.0 | 117.1585400264378 | 174.6141946246399 | 0.0 | 50.66666666666666 | 83.0 | 160.52941176470588 | 16439.075 |
| 56 | Fwd Segment Size Avg | 6311371.0 | 78.96369314042582 | 296.95518899913543 | 0.0 | 35.0 | 49.0 | 107.0 | 31358.14285714286 |
| 57 | Bwd Segment Size Avg | 6311371.0 | 154.5020376723776 | 161.4001001180883 | 0.0 | 58.0 | 126.0 | 218.1875 | 29414.154761904763 |
| 58 | Fwd Bytes/Bulk Avg | 6311371.0 | 439.4506106517902 | 46867.437694523884 | 0.0 | 0.0 | 0.0 | 0.0 | 8452672.0 |
| 59 | Fwd Packet/Bulk Avg | 6311371.0 | 0.07637754142483463 | 5.704365247216664 | 0.0 | 0.0 | 0.0 | 0.0 | 1053.0 |
| 60 | Fwd Bulk Rate Avg | 6311371.0 | 25330.286292946494 | 4327750.986322173 | 0.0 | 0.0 | 0.0 | 0.0 | 2778500000.0 |
| 61 | Bwd Bytes/Bulk Avg | 6311371.0 | 1463.734732754579 | 72046.9171622108 | 0.0 | 0.0 | 0.0 | 0.0 | 101143913.0 |
| 62 | Bwd Packet/Bulk Avg | 6311371.0 | 1.1130600625442555 | 49.9553305938021 | 0.0 | 0.0 | 0.0 | 0.0 | 70149.0 |
| 63 | Bwd Bulk Rate Avg | 6311371.0 | 16295536.752786042 | 172068146.73366103 | 0.0 | 0.0 | 0.0 | 0.0 | 5496000000.0 |
| 64 | Subflow Fwd Packets | 6311371.0 | 0.012689794341039371 | 0.11193196793468536 | 0.0 | 0.0 | 0.0 | 0.0 | 1.0 |
| 65 | Subflow Fwd Bytes | 6311371.0 | 40.1604681455107 | 140.74437156567498 | 0.0 | 17.0 | 24.0 | 60.0 | 16435.0 |
| 66 | Subflow Bwd Packets | 6311371.0 | 0.001383376131746969 | 0.03716803224694297 | 0.0 | 0.0 | 0.0 | 0.0 | 1.0 |
| 67 | Subflow Bwd Bytes | 6311371.0 | 76.29475925278359 | 96.39331791566127 | 0.0 | 29.0 | 62.0 | 95.0 | 15940.0 |
| 68 | FWD Init Win Bytes | 6311371.0 | 5511.66351526475 | 7132.108671870702 | 0.0 | 0.0 | 8192.0 | 8192.0 | 65535.0 |
| 69 | Bwd Init Win Bytes | 6311371.0 | 14724.94555842146 | 26294.981736051475 | 0.0 | 0.0 | 0.0 | 5138.0 | 65535.0 |
| 70 | Fwd Act Data Pkts | 6311371.0 | 3.314238697107174 | 17.14543848129125 | 0.0 | 0.0 | 1.0 | 5.0 | 9262.0 |
| 71 | Fwd Seg Size Min | 6311371.0 | 15.91267824376035 | 6.295218501456383 | 0.0 | 8.0 | 20.0 | 20.0 | 48.0 |
| 72 | Active Mean | 6311371.0 | 453264.8605185369 | 1624235.0842687301 | 0.0 | 0.0 | 0.0 | 0.0 | 114675529.0 |
| 73 | Active Std | 6311371.0 | 45406.78157537396 | 445229.70775370556 | 0.0 | 0.0 | 0.0 | 0.0 | 75493202.61138456 |
| 74 | Active Max | 6311371.0 | 517423.21967841854 | 1794192.4178308148 | 0.0 | 0.0 | 0.0 | 0.0 | 114675529.0 |
| 75 | Active Min | 6311371.0 | 425308.1907858055 | 1594356.5507011716 | 0.0 | 0.0 | 0.0 | 0.0 | 114675529.0 |
| 76 | Idle Mean | 6311371.0 | 10938162.587691085 | 25589946.50129914 | 0.0 | 0.0 | 0.0 | 0.0 | 119998705.0 |
| 77 | Idle Std | 6311371.0 | 614780.4518985661 | 4197389.741989466 | 0.0 | 0.0 | 0.0 | 0.0 | 73400293.81829299 |
| 78 | Idle Max | 6311371.0 | 11398579.935226593 | 26116618.01772751 | 0.0 | 0.0 | 0.0 | 0.0 | 119998705.0 |
| 79 | Idle Min | 6311371.0 | 10437834.942949638 | 25443759.593060527 | 0.0 | 0.0 | 0.0 | 0.0 | 119998705.0 |
| 80 | ICMP Code | 6311371.0 | -0.9963863635967526 | 0.1333240940095694 | -1.0 | -1.0 | -1.0 | -1.0 | 13.0 |
| 81 | ICMP Type | 6311371.0 | -0.981092697608808 | 0.4171255499877608 | -1.0 | -1.0 | -1.0 | -1.0 | 13.0 |
| 82 | Total TCP Flow Time | 6311371.0 | 143982234.1466068 | 1506007738.4993505 | 0.0 | 0.0 | 863714.0 | 10155118.0 | 42737268774.0 |

## Distribution Analysis
 Distribution of target variable 'Label':

Distribution Analysis

| # | Class | Percentage |
|---|---|---|
| 1 | BENIGN | 0.9773 |
| 2 | Botnet Ares | 0.0226 |
| 3 | Botnet Ares - Attempted | 0.0000 |

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
| 24 | Bwd IAT Min | bwd_iat_min |
| 25 | Fwd PSH Flags | fwd_psh_flags |
| 26 | Bwd PSH Flags | bwd_psh_flags |
| 27 | Fwd RST Flags | fwd_rst_flags |
| 28 | Bwd RST Flags | bwd_rst_flags |
| 29 | Fwd Header Length | fwd_header_length |
| 30 | Bwd Header Length | bwd_header_length |
| 31 | Bwd Packets/s | bwd_packets/s |
| 32 | Packet Length Max | packet_length_max |
| 33 | Packet Length Mean | packet_length_mean |
| 34 | Packet Length Std | packet_length_std |
| 35 | Packet Length Variance | packet_length_variance |
| 36 | FIN Flag Count | fin_flag_count |
| 37 | SYN Flag Count | syn_flag_count |
| 38 | RST Flag Count | rst_flag_count |
| 39 | PSH Flag Count | psh_flag_count |
| 40 | CWR Flag Count | cwr_flag_count |
| 41 | ECE Flag Count | ece_flag_count |
| 42 | Down/Up Ratio | down/up_ratio |
| 43 | Fwd Bulk Rate Avg | fwd_bulk_rate_avg |
| 44 | Bwd Bytes/Bulk Avg | bwd_bytes/bulk_avg |
| 45 | Bwd Bulk Rate Avg | bwd_bulk_rate_avg |
| 46 | Subflow Fwd Packets | subflow_fwd_packets |
| 47 | Subflow Bwd Packets | subflow_bwd_packets |
| 48 | FWD Init Win Bytes | fwd_init_win_bytes |
| 49 | Bwd Init Win Bytes | bwd_init_win_bytes |
| 50 | Fwd Act Data Pkts | fwd_act_data_pkts |
| 51 | Fwd Seg Size Min | fwd_seg_size_min |
| 52 | Active Mean | active_mean |
| 53 | Active Std | active_std |
| 54 | Active Max | active_max |
| 55 | Idle Std | idle_std |
| 56 | ICMP Code | icmp_code |
| 57 | ICMP Type | icmp_type |
| 58 | Total TCP Flow Time | total_tcp_flow_time |

## Recommendation
 Based on the assessment, it is recommended to continue working with the available columns. You may consider the following:
- Performing further analysis using the available columns: `['Dst Port', 'Flow Duration', 'Total Fwd Packet', 'Total Bwd packets', 'Total Length of Fwd Packet', 'Fwd Packet Length Max', 'Fwd Packet Length Min', 'Fwd Packet Length Mean', 'Bwd Packet Length Max', 'Bwd Packet Length Min', 'Bwd Packet Length Mean', 'Flow Bytes/s', 'Flow Packets/s', 'Flow IAT Mean', 'Flow IAT Std', 'Flow IAT Max', 'Flow IAT Min', 'Fwd IAT Total', 'Fwd IAT Mean', 'Fwd IAT Std', 'Fwd IAT Max', 'Fwd IAT Min', 'Bwd IAT Mean', 'Bwd IAT Min', 'Fwd PSH Flags', 'Bwd PSH Flags', 'Fwd RST Flags', 'Bwd RST Flags', 'Fwd Header Length', 'Bwd Header Length', 'Bwd Packets/s', 'Packet Length Max', 'Packet Length Mean', 'Packet Length Std', 'Packet Length Variance', 'FIN Flag Count', 'SYN Flag Count', 'RST Flag Count', 'PSH Flag Count', 'CWR Flag Count', 'ECE Flag Count', 'Down/Up Ratio', 'Fwd Bulk Rate Avg', 'Bwd Bytes/Bulk Avg', 'Bwd Bulk Rate Avg', 'Subflow Fwd Packets', 'Subflow Bwd Packets', 'FWD Init Win Bytes', 'Bwd Init Win Bytes', 'Fwd Act Data Pkts', 'Fwd Seg Size Min', 'Active Mean', 'Active Std', 'Active Max', 'Idle Std', 'ICMP Code', 'ICMP Type', 'Total TCP Flow Time']`
- Train machine learning models with the reduced feature set.
## End of Report ✅  
 
✅ Report Successfully Generated in  08:59 minutes

