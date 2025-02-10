# Data Assessment Report on dataset: Wednesday-14-02-2018.csv
## Command line executed  
 ```dataset_assessment_prepare.py --drop-columns id,Protocol,Attempted Category,Src Port --drop-highly-correlated --correlation-threshold 0.95 --drop-categorical-columns --impute-strategy mean --assess-only --zero-variance --low-variance-threshold=0.01 --low-variance-sample-percentage=100 --missing-threshold=0.05 --descriptive-statistics --distribution-analysis --distribution-column Label -output . -input CSECICIDS2018_improved/Wednesday-14-02-2018.csv```  
# Report  
 ### Options used to generate this report  

| # | Option | Value |
|---|---|---|
| 1 | -input | CSECICIDS2018_improved/Wednesday-14-02-2018.csv |
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
 
✅ Dataset Loaded Successfully: `.../DATASET_engelen_improved/CSECICIDS2018_improved/Wednesday-14-02-2018.csv
- File Size: 3111.44 MB
- Number of Records: 5,898,350
- File loaded in 03:08 minutes

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
 Found 11781307 negative values:

### Columns with Negative Values

| # | Column | Negative Count |
|---|---|---|
| 1 | Fwd Header Length | 1068 |
| 2 | Bwd Header Length | 1519 |
| 3 | ICMP Code | 5889360 |
| 4 | ICMP Type | 5889360 |

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
 ️Found 21 highly correlated features (threshold: 0.95):

### Highly Correlated Features

| # | Feature 1 | Feature 2 | Correlation |
|---|---|---|---|
| 1 | Total Length of Bwd Packet | Total Bwd packets | 0.9937 |
| 2 | Fwd Packet Length Std | Fwd Packet Length Max | 0.9622 |
| 3 | Bwd Packet Length Std | Bwd Packet Length Max | 0.9748 |
| 4 | Fwd IAT Total | Flow Duration | 0.9583 |
| 5 | Bwd IAT Total | Flow Duration | 0.9950 |
| 6 | Bwd IAT Total | Fwd IAT Total | 0.9525 |
| 7 | Bwd IAT Max | Flow IAT Max | 0.9889 |
| 8 | Fwd Packets/s | Flow Packets/s | 0.9990 |
| 9 | Bwd Packets/s | Flow Packets/s | 0.9990 |
| 10 | Bwd Packets/s | Fwd Packets/s | 0.9960 |
| 11 | Packet Length Min | Fwd Packet Length Min | 0.9982 |
| 12 | ACK Flag Count | Total Bwd packets | 0.9844 |
| 13 | ACK Flag Count | Total Length of Bwd Packet | 0.9822 |
| 14 | Average Packet Size | Packet Length Mean | 1.0000 |
| 15 | Fwd Segment Size Avg | Fwd Packet Length Mean | 1.0000 |
| 16 | Bwd Segment Size Avg | Bwd Packet Length Mean | 1.0000 |
| 17 | Fwd Packet/Bulk Avg | Fwd Bytes/Bulk Avg | 0.9837 |
| 18 | Bwd Packet/Bulk Avg | Bwd Bytes/Bulk Avg | 0.9999 |
| 19 | Subflow Fwd Bytes | Fwd Packet Length Mean | 0.9721 |
| 20 | Subflow Fwd Bytes | Fwd Segment Size Avg | 0.9721 |
| 21 | Subflow Bwd Bytes | Bwd Packet Length Mean | 0.9798 |
| 22 | Subflow Bwd Bytes | Bwd Segment Size Avg | 0.9798 |
| 23 | Active Min | Active Mean | 0.9716 |
| 24 | Idle Mean | Flow IAT Max | 0.9823 |
| 25 | Idle Mean | Bwd IAT Max | 0.9712 |
| 26 | Idle Max | Flow IAT Max | 0.9992 |
| 27 | Idle Max | Bwd IAT Max | 0.9881 |
| 28 | Idle Max | Idle Mean | 0.9831 |
| 29 | Idle Min | Idle Mean | 0.9808 |

💡 To drop these features, use:
```python
df_numeric.drop(columns=['Total Length of Bwd Packet', 'Fwd Packet Length Std', 'Bwd Packet Length Std', 'Fwd IAT Total', 'Bwd IAT Total', 'Bwd IAT Max', 'Fwd Packets/s', 'Bwd Packets/s', 'Packet Length Min', 'ACK Flag Count', 'Average Packet Size', 'Fwd Segment Size Avg', 'Bwd Segment Size Avg', 'Fwd Packet/Bulk Avg', 'Bwd Packet/Bulk Avg', 'Subflow Fwd Bytes', 'Subflow Bwd Bytes', 'Active Min', 'Idle Mean', 'Idle Max', 'Idle Min'], inplace=True)
```
## Descriptive Statistics Analysis
 Descriptive Statistics for Features

| # | Column | Count | Mean | Std | Min | 25% | 50% | 75% | Max |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Dst Port | 5898350.0 | 726.5537931794485 | 1898.7616437329552 | 0.0 | 53.0 | 80.0 | 443.0 | 65533.0 |
| 2 | Flow Duration | 5898350.0 | 15326258.088767875 | 35052098.178238794 | 0.0 | 1082.0 | 72141.0 | 2921091.75 | 120000000.0 |
| 3 | Total Fwd Packet | 5898350.0 | 6.997888901133368 | 60.24968707513542 | 0.0 | 1.0 | 3.0 | 8.0 | 45421.0 |
| 4 | Total Bwd packets | 5898350.0 | 8.959192994651046 | 146.2236500953378 | 0.0 | 1.0 | 2.0 | 7.0 | 51142.0 |
| 5 | Total Length of Fwd Packet | 5898350.0 | 925.7420970271347 | 40584.33166067485 | 0.0 | 39.0 | 77.0 | 831.0 | 54229644.0 |
| 6 | Total Length of Bwd Packet | 5898350.0 | 6130.515872404994 | 209781.73882563857 | 0.0 | 67.0 | 168.0 | 1581.0 | 72777357.0 |
| 7 | Fwd Packet Length Max | 5898350.0 | 258.0932910051116 | 786.999009767228 | 0.0 | 36.0 | 47.0 | 431.0 | 64440.0 |
| 8 | Fwd Packet Length Min | 5898350.0 | 18.274458789322438 | 23.907521937770138 | 0.0 | 0.0 | 0.0 | 38.0 | 1487.0 |
| 9 | Fwd Packet Length Mean | 5898350.0 | 62.20046037232139 | 135.7836422369303 | 0.0 | 32.2 | 42.0 | 72.87499999999999 | 11196.850719424452 |
| 10 | Fwd Packet Length Std | 5898350.0 | 76.41678343455948 | 220.0626606717588 | 0.0 | 0.0 | 0.0 | 113.12766347720527 | 16981.965924100536 |
| 11 | Bwd Packet Length Max | 5898350.0 | 461.1718733205049 | 548.0436219604563 | 0.0 | 63.0 | 132.0 | 1149.0 | 65160.0 |
| 12 | Bwd Packet Length Min | 5898350.0 | 45.262657692405504 | 59.25026080622093 | 0.0 | 0.0 | 0.0 | 86.0 | 1460.0 |
| 13 | Bwd Packet Length Mean | 5898350.0 | 145.8172249818542 | 168.17835548334398 | 0.0 | 55.0 | 100.0 | 196.0909090909091 | 29306.925 |
| 14 | Bwd Packet Length Std | 5898350.0 | 155.399432802784 | 220.11237646778272 | 0.0 | 0.0 | 0.0 | 367.8296858299745 | 19798.10526593103 |
| 15 | Flow Bytes/s | 5898349.0 | 92417.9794044903 | 280240.6154652164 | 0.0 | 228.10580047679488 | 3079.7343215858577 | 114781.1725846408 | 190000000.0 |
| 16 | Flow Packets/s | 5898349.0 | 40568.837685142345 | 241194.4666224135 | 0.0166666990278406 | 5.282333692766795 | 80.65491793362101 | 2004.008016032064 | 3000000.0 |
| 17 | Flow IAT Mean | 5898350.0 | 774374.5563810483 | 2508075.070790055 | 0.0 | 995.0 | 18924.0 | 205154.84375 | 119999767.0 |
| 18 | Flow IAT Std | 5898350.0 | 1887769.0697264813 | 5024483.897652253 | 0.0 | 0.0 | 14414.29397042017 | 266904.00987233815 | 84799911.54855123 |
| 19 | Flow IAT Max | 5898350.0 | 6615112.226224113 | 17592136.24485793 | 0.0 | 1003.0 | 45125.0 | 968819.0 | 119999767.0 |
| 20 | Flow IAT Min | 5898350.0 | 45880.913448845866 | 1425672.3903784577 | 0.0 | 3.0 | 45.0 | 773.0 | 119999767.0 |
| 21 | Fwd IAT Total | 5898350.0 | 14085862.13559131 | 33979539.583791405 | 0.0 | 0.0 | 33527.0 | 2591892.25 | 119999998.0 |
| 22 | Fwd IAT Mean | 5898350.0 | 1347005.2292525293 | 4221938.876126747 | 0.0 | 0.0 | 19748.8 | 356054.9285714286 | 119999767.0 |
| 23 | Fwd IAT Std | 5898350.0 | 2074133.019983884 | 5840073.448151275 | 0.0 | 0.0 | 114.53438348243824 | 402630.52109628957 | 84747995.06156974 |
| 24 | Fwd IAT Max | 5898350.0 | 5503469.612677952 | 15052926.859761216 | 0.0 | 0.0 | 29202.0 | 1228808.75 | 119999767.0 |
| 25 | Fwd IAT Min | 5898350.0 | 156728.6460839048 | 2872432.866266745 | 0.0 | 0.0 | 4.0 | 142.0 | 119999767.0 |
| 26 | Bwd IAT Total | 5898350.0 | 15000640.808106504 | 34849620.45922099 | 0.0 | 0.0 | 695.0 | 2528317.25 | 120000000.0 |
| 27 | Bwd IAT Mean | 5898350.0 | 1807453.7285113053 | 6347785.103335758 | 0.0 | 0.0 | 180.5 | 370852.21875 | 119999696.0 |
| 28 | Bwd IAT Std | 5898350.0 | 2187793.7361922897 | 6255981.564866603 | 0.0 | 0.0 | 0.0 | 322559.6546763099 | 84776432.06788193 |
| 29 | Bwd IAT Max | 5898350.0 | 6470956.084137259 | 17473763.140046455 | 0.0 | 0.0 | 307.0 | 954240.0 | 119999696.0 |
| 30 | Bwd IAT Min | 5898350.0 | 582567.5523880407 | 5485456.899572773 | 0.0 | 0.0 | 0.0 | 322.75 | 119999696.0 |
| 31 | Fwd PSH Flags | 5898350.0 | 2.2105724482270466 | 7.527860486767632 | 0.0 | 0.0 | 0.0 | 4.0 | 12439.0 |
| 32 | Bwd PSH Flags | 5898350.0 | 2.2509615400917204 | 5.63363127665456 | 0.0 | 0.0 | 0.0 | 4.0 | 2300.0 |
| 33 | Fwd URG Flags | 5898350.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| 34 | Bwd URG Flags | 5898350.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| 35 | Fwd RST Flags | 5898350.0 | 0.18958827468698874 | 0.3944595719456601 | 0.0 | 0.0 | 0.0 | 0.0 | 4.0 |
| 36 | Bwd RST Flags | 5898350.0 | 0.1482502733815389 | 0.37688638096094135 | 0.0 | 0.0 | 0.0 | 0.0 | 16.0 |
| 37 | Fwd Header Length | 5898350.0 | 127.66605779582426 | 453.46243927552376 | -32736.0 | 8.0 | 60.0 | 172.0 | 32672.0 |
| 38 | Bwd Header Length | 5898350.0 | 138.54023447235244 | 636.4971252715862 | -32752.0 | 8.0 | 20.0 | 152.0 | 32764.0 |
| 39 | Fwd Packets/s | 5898350.0 | 20304.00720649366 | 120864.0084804051 | 0.0 | 2.845072889433867 | 42.02872663465479 | 1002.004008016032 | 3000000.0 |
| 40 | Bwd Packets/s | 5898350.0 | 20264.82360065098 | 120571.42920648702 | 0.0 | 2.465071260810301 | 39.76933784052496 | 1001.0010010010008 | 2000000.0 |
| 41 | Packet Length Min | 5898350.0 | 18.258391414548136 | 23.728676889139713 | 0.0 | 0.0 | 0.0 | 38.0 | 1460.0 |
| 42 | Packet Length Max | 5898350.0 | 502.2478737273983 | 902.8979969941234 | 0.0 | 63.0 | 132.0 | 1173.0 | 65160.0 |
| 43 | Packet Length Mean | 5898350.0 | 105.22852669086238 | 119.45835462382874 | 0.0 | 49.0 | 70.5 | 146.5 | 15139.070967741936 |
| 44 | Packet Length Std | 5898350.0 | 150.3600471889728 | 213.52030082617728 | 0.0 | 19.79898987322333 | 61.12193476233314 | 295.1596312078209 | 20410.197184699307 |
| 45 | Packet Length Variance | 5898350.0 | 68199.05492613524 | 712010.030815491 | 0.0 | 392.0 | 3735.8909090909087 | 87119.20789473686 | 416576149.1183076 |
| 46 | FIN Flag Count | 5898350.0 | 0.48434273991879084 | 0.8529091341170966 | 0.0 | 0.0 | 0.0 | 1.0 | 15.0 |
| 47 | SYN Flag Count | 5898350.0 | 0.9735092017259064 | 1.0551851800862784 | 0.0 | 0.0 | 0.0 | 2.0 | 178.0 |
| 48 | RST Flag Count | 5898350.0 | 0.33784973763849213 | 0.5192620370490074 | 0.0 | 0.0 | 0.0 | 1.0 | 16.0 |
| 49 | PSH Flag Count | 5898350.0 | 4.4615339883187675 | 11.060096851118397 | 0.0 | 0.0 | 0.0 | 8.0 | 12617.0 |
| 50 | ACK Flag Count | 5898350.0 | 14.354239575474496 | 196.97135796148868 | 0.0 | 0.0 | 3.0 | 15.0 | 74404.0 |
| 51 | URG Flag Count | 5898350.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| 52 | CWR Flag Count | 5898350.0 | 0.24233455118804412 | 0.4975035868947035 | 0.0 | 0.0 | 0.0 | 0.0 | 28.0 |
| 53 | ECE Flag Count | 5898350.0 | 0.31434214653250486 | 0.6490075402559984 | 0.0 | 0.0 | 0.0 | 0.0 | 7.0 |
| 54 | Down/Up Ratio | 5898350.0 | 0.9569919074658599 | 0.32151441738441544 | 0.0 | 0.8888888888888888 | 1.0 | 1.0 | 24.25 |
| 55 | Average Packet Size | 5898350.0 | 105.22852669086238 | 119.45835462382874 | 0.0 | 49.0 | 70.5 | 146.5 | 15139.070967741936 |
| 56 | Fwd Segment Size Avg | 5898350.0 | 62.20046037232138 | 135.7836422369303 | 0.0 | 32.2 | 42.0 | 72.875 | 11196.85071942446 |
| 57 | Bwd Segment Size Avg | 5898350.0 | 145.8172249818542 | 168.17835548334398 | 0.0 | 55.0 | 100.0 | 196.0909090909091 | 29306.925 |
| 58 | Fwd Bytes/Bulk Avg | 5898350.0 | 299.6962416608034 | 32874.17907288921 | 0.0 | 0.0 | 0.0 | 0.0 | 6383621.0 |
| 59 | Fwd Packet/Bulk Avg | 5898350.0 | 0.06950926954148194 | 4.061642114624483 | 0.0 | 0.0 | 0.0 | 0.0 | 1091.0 |
| 60 | Fwd Bulk Rate Avg | 5898350.0 | 17760.39579763832 | 4203862.124068578 | 0.0 | 0.0 | 0.0 | 0.0 | 3104000000.0 |
| 61 | Bwd Bytes/Bulk Avg | 5898350.0 | 1768.2411432010647 | 115588.7694101766 | 0.0 | 0.0 | 0.0 | 0.0 | 40436160.0 |
| 62 | Bwd Packet/Bulk Avg | 5898350.0 | 1.3379867251010875 | 80.24398201882563 | 0.0 | 0.0 | 0.0 | 0.0 | 27697.0 |
| 63 | Bwd Bulk Rate Avg | 5898350.0 | 18572186.4428252 | 182061216.77876443 | 0.0 | 0.0 | 0.0 | 0.0 | 5500000000.0 |
| 64 | Subflow Fwd Packets | 5898350.0 | 0.013447659091101748 | 0.11518169040830292 | 0.0 | 0.0 | 0.0 | 0.0 | 1.0 |
| 65 | Subflow Fwd Bytes | 5898350.0 | 31.063496231997085 | 53.48168583758764 | 0.0 | 16.0 | 21.0 | 35.0 | 4549.0 |
| 66 | Subflow Bwd Packets | 5898350.0 | 0.0008298931056990515 | 0.028795911579851396 | 0.0 | 0.0 | 0.0 | 0.0 | 1.0 |
| 67 | Subflow Bwd Bytes | 5898350.0 | 73.5288526452313 | 99.3549520038723 | 0.0 | 27.0 | 49.0 | 90.0 | 15126.0 |
| 68 | FWD Init Win Bytes | 5898350.0 | 5927.256177914162 | 9806.836207827086 | 0.0 | 0.0 | 258.0 | 8192.0 | 65535.0 |
| 69 | Bwd Init Win Bytes | 5898350.0 | 8977.628564768112 | 21482.329451168727 | 0.0 | 0.0 | 0.0 | 187.0 | 65535.0 |
| 70 | Fwd Act Data Pkts | 5898350.0 | 2.8202376935922757 | 21.075200349796486 | 0.0 | 0.0 | 1.0 | 5.0 | 45420.0 |
| 71 | Fwd Seg Size Min | 5898350.0 | 15.68128171437775 | 8.142234111509959 | 0.0 | 8.0 | 20.0 | 20.0 | 52.0 |
| 72 | Active Mean | 5898350.0 | 152326.8631009264 | 1264836.3330082255 | 0.0 | 0.0 | 0.0 | 0.0 | 114366734.0 |
| 73 | Active Std | 5898350.0 | 47304.51258414777 | 438588.80049783556 | 0.0 | 0.0 | 0.0 | 0.0 | 75966632.52169918 |
| 74 | Active Max | 5898350.0 | 224086.62460399943 | 1496584.7514445982 | 0.0 | 0.0 | 0.0 | 0.0 | 114366734.0 |
| 75 | Active Min | 5898350.0 | 124292.29451558487 | 1220014.7003001547 | 0.0 | 0.0 | 0.0 | 0.0 | 114366734.0 |
| 76 | Idle Mean | 5898350.0 | 5845742.996273049 | 16626088.257542556 | 0.0 | 0.0 | 0.0 | 0.0 | 119999767.0 |
| 77 | Idle Std | 5898350.0 | 690465.4793044728 | 4475426.4912412865 | 0.0 | 0.0 | 0.0 | 0.0 | 75853304.5178784 |
| 78 | Idle Max | 5898350.0 | 6354388.069251061 | 17671555.767986324 | 0.0 | 0.0 | 0.0 | 0.0 | 119999767.0 |
| 79 | Idle Min | 5898350.0 | 5281598.811542211 | 16190497.234069323 | 0.0 | 0.0 | 0.0 | 0.0 | 119999767.0 |
| 80 | ICMP Code | 5898350.0 | -0.9969508421846788 | 0.13865938251659343 | -1.0 | -1.0 | -1.0 | -1.0 | 13.0 |
| 81 | ICMP Type | 5898350.0 | -0.9863802588859596 | 0.35807667987044733 | -1.0 | -1.0 | -1.0 | -1.0 | 11.0 |
| 82 | Total TCP Flow Time | 5898350.0 | 130191393.74403773 | 1337059383.564345 | 0.0 | 0.0 | 1216.0 | 5120864.5 | 43640774176.0 |

## Distribution Analysis
 Distribution of target variable 'Label':

Distribution Analysis

| # | Class | Percentage |
|---|---|---|
| 1 | BENIGN | 0.9512 |
| 2 | FTP-BruteForce - Attempted | 0.0328 |
| 3 | SSH-BruteForce | 0.0160 |

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
| 18 | Fwd IAT Mean | fwd_iat_mean |
| 19 | Fwd IAT Std | fwd_iat_std |
| 20 | Fwd IAT Max | fwd_iat_max |
| 21 | Fwd IAT Min | fwd_iat_min |
| 22 | Bwd IAT Mean | bwd_iat_mean |
| 23 | Bwd IAT Std | bwd_iat_std |
| 24 | Bwd IAT Min | bwd_iat_min |
| 25 | Fwd PSH Flags | fwd_psh_flags |
| 26 | Bwd PSH Flags | bwd_psh_flags |
| 27 | Fwd RST Flags | fwd_rst_flags |
| 28 | Bwd RST Flags | bwd_rst_flags |
| 29 | Fwd Header Length | fwd_header_length |
| 30 | Bwd Header Length | bwd_header_length |
| 31 | Packet Length Max | packet_length_max |
| 32 | Packet Length Mean | packet_length_mean |
| 33 | Packet Length Std | packet_length_std |
| 34 | Packet Length Variance | packet_length_variance |
| 35 | FIN Flag Count | fin_flag_count |
| 36 | SYN Flag Count | syn_flag_count |
| 37 | RST Flag Count | rst_flag_count |
| 38 | PSH Flag Count | psh_flag_count |
| 39 | CWR Flag Count | cwr_flag_count |
| 40 | ECE Flag Count | ece_flag_count |
| 41 | Down/Up Ratio | down/up_ratio |
| 42 | Fwd Bytes/Bulk Avg | fwd_bytes/bulk_avg |
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
- Performing further analysis using the available columns: `['Dst Port', 'Flow Duration', 'Total Fwd Packet', 'Total Bwd packets', 'Total Length of Fwd Packet', 'Fwd Packet Length Max', 'Fwd Packet Length Min', 'Fwd Packet Length Mean', 'Bwd Packet Length Max', 'Bwd Packet Length Min', 'Bwd Packet Length Mean', 'Flow Bytes/s', 'Flow Packets/s', 'Flow IAT Mean', 'Flow IAT Std', 'Flow IAT Max', 'Flow IAT Min', 'Fwd IAT Mean', 'Fwd IAT Std', 'Fwd IAT Max', 'Fwd IAT Min', 'Bwd IAT Mean', 'Bwd IAT Std', 'Bwd IAT Min', 'Fwd PSH Flags', 'Bwd PSH Flags', 'Fwd RST Flags', 'Bwd RST Flags', 'Fwd Header Length', 'Bwd Header Length', 'Packet Length Max', 'Packet Length Mean', 'Packet Length Std', 'Packet Length Variance', 'FIN Flag Count', 'SYN Flag Count', 'RST Flag Count', 'PSH Flag Count', 'CWR Flag Count', 'ECE Flag Count', 'Down/Up Ratio', 'Fwd Bytes/Bulk Avg', 'Fwd Bulk Rate Avg', 'Bwd Bytes/Bulk Avg', 'Bwd Bulk Rate Avg', 'Subflow Fwd Packets', 'Subflow Bwd Packets', 'FWD Init Win Bytes', 'Bwd Init Win Bytes', 'Fwd Act Data Pkts', 'Fwd Seg Size Min', 'Active Mean', 'Active Std', 'Active Max', 'Idle Std', 'ICMP Code', 'ICMP Type', 'Total TCP Flow Time']`
- Train machine learning models with the reduced feature set.
## End of Report ✅  
 
✅ Report Successfully Generated in  05:43 minutes

