# Data Assessment Report on Wednesday-14-02-2018.csv

## Command line executed  
 console ```V:\63184\DATASET_engelen_improved\dataset_assessment_prepare.py --drop-columns id,Attempted Category,Src Port --drop-highly-correlated --correlation-threshold 0.95 --feature-selection pca --drop-categorical-columns --impute-strategy mean --assess-only --scale-method standard --zero-variance --low-variance --low-variance-threshold=0.01 --low-variance-sample-percentage=100 -input CSECICIDS2018_improved/Wednesday-14-02-2018.csv -output .```
## Report  
 ## Options used to generate this report  

| # | Option | Value |
|---|---|---|
| 1 | -input | CSECICIDS2018_improved/Wednesday-14-02-2018.csv |
| 2 | -output | . |
| 3 | --drop-columns | id,Attempted Category,Src Port |
| 4 | --drop-categorical-columns | True |
| 5 | --drop-highly-correlated | True |
| 6 | --scale-method | standard |
| 7 | --feature-selection | pca |
| 8 | --impute-strategy | mean |
| 9 | --assess-only | True |
| 10 | --correlation-threshold | 0.95 |
| 11 | --zero-variance | True |
| 12 | --low-variance | True |
| 13 | --low-variance-threshold | 0.01 |
| 14 | --low-variance-sample-percentage | 100.0 |

## Dataset Loaded  
 
✅ Dataset Loaded Successfully: `V:\63184\DATASET_engelen_improved\CSECICIDS2018_improved\Wednesday-14-02-2018.csv
- File Size: 3111.44 MB
- Number of Records: 5,898,350
- File loaded in 01:14 minutes

## Assessment Mode  
 # 🔍 Running in assessment-only mode. No changes applied to the dataset.  
Explicitly Defined Columns 🗑  
 ## Explicitly Dropped Columns  

| # | Column |
|---|---|
| 1 | id |
| 2 | Attempted Category |
| 3 | Src Port |

Python Command to drop columns these columns manually 💡  
  Use:
```python
df.drop(columns=['id', 'Attempted Category', 'Src Port'], inplace=True)
```
Leading Spaces in Feature Names ⚠️  
 No issues found!  
Identified Categorical Columns ⚠️  
 ## Categorical Columns

| # | Column |
|---|---|
| 1 | Flow ID |
| 2 | Src IP |
| 3 | Dst IP |
| 4 | Timestamp |
| 5 | Label |

Identify Categorical Columns  
 No categorical columns removed (Flag `--drop_categorical_columns=False`).
💡 To drop them manually, use:
```python
df.drop(columns=['Flow ID', 'Src IP', 'Dst IP', 'Timestamp', 'Label'], inplace=True)
```
Zero Variance Columns ⚠️
 ## Identified Zero Variance Columns

| # | Column | Unique Value |
|---|---|---|
| 1 | Fwd URG Flags | 0 |
| 2 | Bwd URG Flags | 0 |
| 3 | URG Flag Count | 0 |

To drop these columns, use:
```python
df_numeric.drop(columns=['Fwd URG Flags', 'Bwd URG Flags', 'URG Flag Count'], inplace=True)
```
## Negative Values 
 ⚠️ Found 11781307 negative values:

## Columns with Negative Values

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
Infinite Values ⚠️
 Found 2 infinite values:

## Columns with Infinite Values

| # | Column | Infinite Count |
|---|---|---|
| 1 | Flow Bytes/s | 1 |
| 2 | Flow Packets/s | 1 |

💡 To replace with NaN, use:
```python
df_numeric.replace([np.inf, -np.inf], np.nan, inplace=True)
```
Missing Values ✅  
 No issues found
Highly Correlated Features ⚠
 ️ Found 21 highly correlated features (threshold: 0.95):

## Highly Correlated Features

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
Low Variance Columns ✅  
 No low variance columns found (threshold: 0.01)
Feature Scaling
 ⚠️ Scaling recommended. To apply `standard` scaling, use:
``````
Feature Selection
 ⚠️ PCA analysis results:
  - 95% variance retained with 1 components (reduced from 62 to 1)
  - 99% variance retained with 2 components (reduced from 62 to 2)
  - 99.9% variance retained with 3 components (reduced from 62 to 3)

Feature Selection Command
 💡 To apply PCA, use:
```python
df_numeric_finite = df_numeric[~np.isinf(df_numeric).any(axis=1)]
pca = PCA(n_components=1)
df_numeric_pca = pd.DataFrame(pca.fit_transform(df_numeric_finite))
```
Available Columns
 After cleaning, the following columns are available: `['Dst Port', 'Protocol', 'Flow Duration', 'Total Fwd Packet', 'Total Bwd packets', 'Total Length of Fwd Packet', 'Fwd Packet Length Max', 'Fwd Packet Length Min', 'Fwd Packet Length Mean', 'Bwd Packet Length Max', 'Bwd Packet Length Min', 'Bwd Packet Length Mean', 'Flow Bytes/s', 'Flow Packets/s', 'Flow IAT Mean', 'Flow IAT Std', 'Flow IAT Max', 'Flow IAT Min', 'Fwd IAT Mean', 'Fwd IAT Std', 'Fwd IAT Max', 'Fwd IAT Min', 'Bwd IAT Mean', 'Bwd IAT Std', 'Bwd IAT Min', 'Fwd PSH Flags', 'Bwd PSH Flags', 'Fwd URG Flags', 'Bwd URG Flags', 'Fwd RST Flags', 'Bwd RST Flags', 'Fwd Header Length', 'Bwd Header Length', 'Packet Length Max', 'Packet Length Mean', 'Packet Length Std', 'Packet Length Variance', 'FIN Flag Count', 'SYN Flag Count', 'RST Flag Count', 'PSH Flag Count', 'URG Flag Count', 'CWR Flag Count', 'ECE Flag Count', 'Down/Up Ratio', 'Fwd Bytes/Bulk Avg', 'Fwd Bulk Rate Avg', 'Bwd Bytes/Bulk Avg', 'Bwd Bulk Rate Avg', 'Subflow Fwd Packets', 'Subflow Bwd Packets', 'FWD Init Win Bytes', 'Bwd Init Win Bytes', 'Fwd Act Data Pkts', 'Fwd Seg Size Min', 'Active Mean', 'Active Std', 'Active Max', 'Idle Std', 'ICMP Code', 'ICMP Type', 'Total TCP Flow Time']`
## Available Columns and Recommended Mapping  
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
| 29 | Bwd URG Flags | bwd_urg_flags |
| 30 | Fwd RST Flags | fwd_rst_flags |
| 31 | Bwd RST Flags | bwd_rst_flags |
| 32 | Fwd Header Length | fwd_header_length |
| 33 | Bwd Header Length | bwd_header_length |
| 34 | Packet Length Max | packet_length_max |
| 35 | Packet Length Mean | packet_length_mean |
| 36 | Packet Length Std | packet_length_std |
| 37 | Packet Length Variance | packet_length_variance |
| 38 | FIN Flag Count | fin_flag_count |
| 39 | SYN Flag Count | syn_flag_count |
| 40 | RST Flag Count | rst_flag_count |
| 41 | PSH Flag Count | psh_flag_count |
| 42 | URG Flag Count | urg_flag_count |
| 43 | CWR Flag Count | cwr_flag_count |
| 44 | ECE Flag Count | ece_flag_count |
| 45 | Down/Up Ratio | down/up_ratio |
| 46 | Fwd Bytes/Bulk Avg | fwd_bytes/bulk_avg |
| 47 | Fwd Bulk Rate Avg | fwd_bulk_rate_avg |
| 48 | Bwd Bytes/Bulk Avg | bwd_bytes/bulk_avg |
| 49 | Bwd Bulk Rate Avg | bwd_bulk_rate_avg |
| 50 | Subflow Fwd Packets | subflow_fwd_packets |
| 51 | Subflow Bwd Packets | subflow_bwd_packets |
| 52 | FWD Init Win Bytes | fwd_init_win_bytes |
| 53 | Bwd Init Win Bytes | bwd_init_win_bytes |
| 54 | Fwd Act Data Pkts | fwd_act_data_pkts |
| 55 | Fwd Seg Size Min | fwd_seg_size_min |
| 56 | Active Mean | active_mean |
| 57 | Active Std | active_std |
| 58 | Active Max | active_max |
| 59 | Idle Std | idle_std |
| 60 | ICMP Code | icmp_code |
| 61 | ICMP Type | icmp_type |
| 62 | Total TCP Flow Time | total_tcp_flow_time |

## Recommendation
 Based on the assessment, it is recommended to continue working with the available columns. You may consider the following:
- Performing further analysis using the available columns: `['Dst Port', 'Protocol', 'Flow Duration', 'Total Fwd Packet', 'Total Bwd packets', 'Total Length of Fwd Packet', 'Fwd Packet Length Max', 'Fwd Packet Length Min', 'Fwd Packet Length Mean', 'Bwd Packet Length Max', 'Bwd Packet Length Min', 'Bwd Packet Length Mean', 'Flow Bytes/s', 'Flow Packets/s', 'Flow IAT Mean', 'Flow IAT Std', 'Flow IAT Max', 'Flow IAT Min', 'Fwd IAT Mean', 'Fwd IAT Std', 'Fwd IAT Max', 'Fwd IAT Min', 'Bwd IAT Mean', 'Bwd IAT Std', 'Bwd IAT Min', 'Fwd PSH Flags', 'Bwd PSH Flags', 'Fwd URG Flags', 'Bwd URG Flags', 'Fwd RST Flags', 'Bwd RST Flags', 'Fwd Header Length', 'Bwd Header Length', 'Packet Length Max', 'Packet Length Mean', 'Packet Length Std', 'Packet Length Variance', 'FIN Flag Count', 'SYN Flag Count', 'RST Flag Count', 'PSH Flag Count', 'URG Flag Count', 'CWR Flag Count', 'ECE Flag Count', 'Down/Up Ratio', 'Fwd Bytes/Bulk Avg', 'Fwd Bulk Rate Avg', 'Bwd Bytes/Bulk Avg', 'Bwd Bulk Rate Avg', 'Subflow Fwd Packets', 'Subflow Bwd Packets', 'FWD Init Win Bytes', 'Bwd Init Win Bytes', 'Fwd Act Data Pkts', 'Fwd Seg Size Min', 'Active Mean', 'Active Std', 'Active Max', 'Idle Std', 'ICMP Code', 'ICMP Type', 'Total TCP Flow Time']`
- Training machine learning models with the reduced feature set.
## End of Report ✅  
 
✅ Report Successfully Generated in  03:47 minutes

