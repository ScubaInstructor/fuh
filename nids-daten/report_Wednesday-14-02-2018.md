# Data Cleaning Report: `Wednesday-14-02-2018.csv`

- **Options Used**: ```{'file_path': 'CSECICIDS2018_improved/Wednesday-14-02-2018.csv', 'output_path': '.', 'correlation_threshold': 0.95, 'missing_threshold': 0.1, 'impute_strategy': 'mean', 'drop_categorical_columns': True, 'drop_highly_correlated': True, 'drop_columns': 'id,Attempted Category,Src Port', 'scale_method': None, 'feature_selection': 'pca', 'balance_method': None, 'assess_only': True}```
- **Dataset Loaded**: 
✅ Dataset Loaded Successfully: `/Volumes/DATA/63184/DATASET_engelen_improved/CSECICIDS2018_improved/Wednesday-14-02-2018.csv`
- File Size: 3111.44 MB
- Number of Records: 5898350

- **Assessment Mode**: 🔍 Running in assessment-only mode. No changes applied to the dataset.
- **Explicitly Dropped Columns**: 🗑️ `['id', 'Attempted Category', 'Src Port']` to be manually removed
- **Python Command to Drop Columns**: 💡 To drop these columns, use:
```python
df.drop(columns=['id', 'Attempted Category', 'Src Port'], inplace=True)
```
- **Leading Spaces in Feature Names**: No issues found
- **Categorical Columns**: ⚠️ Found 5 categorical columns: `['Flow ID', 'Src IP', 'Dst IP', 'Timestamp', 'Label']`
- **Zero Variance Columns**: ⚠️ Found 3 zero variance columns: `['Fwd URG Flags', 'Bwd URG Flags', 'URG Flag Count']`
💡 To drop these columns, use:
```python
df_numeric.drop(columns=['Fwd URG Flags', 'Bwd URG Flags', 'URG Flag Count'], inplace=True)```
- **Negative Values**: ⚠️ Found 11781307 negative values in columns: `['Fwd Header Length', 'Bwd Header Length', 'ICMP Code', 'ICMP Type']`
💡 To replace with zero, use:
```python
df_numeric.loc[:, df_numeric.columns] = np.where(df_numeric < 0, 0, df_numeric)
```
- **Infinite Values**: ⚠️ Found 2 infinite values in columns `['Flow Bytes/s', 'Flow Packets/s']`.
💡 To replace with NaN, use:
```python
df_numeric.replace([np.inf, -np.inf], np.nan, inplace=True)
```
- **Missing Values**: No issues found
- **Highly Correlated Features**: ⚠️ Found 21 highly correlated features (threshold: 0.95).
💡 To drop these features, use:
```python
df_numeric.drop(columns=['Bwd Packet/Bulk Avg', 'Bwd Segment Size Avg', 'Subflow Bwd Bytes', 'Idle Max', 'Idle Min', 'Fwd Packet/Bulk Avg', 'Average Packet Size', 'Fwd Segment Size Avg', 'ACK Flag Count', 'Total Length of Bwd Packet', 'Idle Mean', 'Bwd Packet Length Std', 'Subflow Fwd Bytes', 'Packet Length Min', 'Fwd IAT Total', 'Fwd Packets/s', 'Active Min', 'Bwd IAT Total', 'Fwd Packet Length Std', 'Bwd IAT Max', 'Bwd Packets/s'], inplace=True)
```
- **Feature Scaling**: ⚠️ Scaling recommended but no method specified
- **Feature Selection**: ⚠️ PCA analysis results:
  - 95% variance retained with 1 components (reduced from 62 to 1)
  - 99% variance retained with 2 components (reduced from 62 to 2)
  - 99.9% variance retained with 3 components (reduced from 62 to 3)

- **Feature Selection Command**: 💡 To apply PCA, use:
```python
df_numeric_finite = df_numeric[~np.isinf(df_numeric).any(axis=1)]
pca = PCA(n_components=1)
df_numeric_pca = pd.DataFrame(pca.fit_transform(df_numeric_finite))
```
**Available Columns**: After cleaning, the following columns are available: `['Dst Port', 'Protocol', 'Flow Duration', 'Total Fwd Packet', 'Total Bwd packets', 'Total Length of Fwd Packet', 'Fwd Packet Length Max', 'Fwd Packet Length Min', 'Fwd Packet Length Mean', 'Bwd Packet Length Max', 'Bwd Packet Length Min', 'Bwd Packet Length Mean', 'Flow Bytes/s', 'Flow Packets/s', 'Flow IAT Mean', 'Flow IAT Std', 'Flow IAT Max', 'Flow IAT Min', 'Fwd IAT Mean', 'Fwd IAT Std', 'Fwd IAT Max', 'Fwd IAT Min', 'Bwd IAT Mean', 'Bwd IAT Std', 'Bwd IAT Min', 'Fwd PSH Flags', 'Bwd PSH Flags', 'Fwd URG Flags', 'Bwd URG Flags', 'Fwd RST Flags', 'Bwd RST Flags', 'Fwd Header Length', 'Bwd Header Length', 'Packet Length Max', 'Packet Length Mean', 'Packet Length Std', 'Packet Length Variance', 'FIN Flag Count', 'SYN Flag Count', 'RST Flag Count', 'PSH Flag Count', 'URG Flag Count', 'CWR Flag Count', 'ECE Flag Count', 'Down/Up Ratio', 'Fwd Bytes/Bulk Avg', 'Fwd Bulk Rate Avg', 'Bwd Bytes/Bulk Avg', 'Bwd Bulk Rate Avg', 'Subflow Fwd Packets', 'Subflow Bwd Packets', 'FWD Init Win Bytes', 'Bwd Init Win Bytes', 'Fwd Act Data Pkts', 'Fwd Seg Size Min', 'Active Mean', 'Active Std', 'Active Max', 'Idle Std', 'ICMP Code', 'ICMP Type', 'Total TCP Flow Time']`

**Available Columns and Recommended Mapping**: The following columns are available after cleaning. Recommended mapping:
  
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

- **Recommendation**: Based on the assessment, it is recommended to continue working with the available columns. You may consider the following:
- Performing further analysis using the available columns: `['Dst Port', 'Protocol', 'Flow Duration', 'Total Fwd Packet', 'Total Bwd packets', 'Total Length of Fwd Packet', 'Fwd Packet Length Max', 'Fwd Packet Length Min', 'Fwd Packet Length Mean', 'Bwd Packet Length Max', 'Bwd Packet Length Min', 'Bwd Packet Length Mean', 'Flow Bytes/s', 'Flow Packets/s', 'Flow IAT Mean', 'Flow IAT Std', 'Flow IAT Max', 'Flow IAT Min', 'Fwd IAT Mean', 'Fwd IAT Std', 'Fwd IAT Max', 'Fwd IAT Min', 'Bwd IAT Mean', 'Bwd IAT Std', 'Bwd IAT Min', 'Fwd PSH Flags', 'Bwd PSH Flags', 'Fwd URG Flags', 'Bwd URG Flags', 'Fwd RST Flags', 'Bwd RST Flags', 'Fwd Header Length', 'Bwd Header Length', 'Packet Length Max', 'Packet Length Mean', 'Packet Length Std', 'Packet Length Variance', 'FIN Flag Count', 'SYN Flag Count', 'RST Flag Count', 'PSH Flag Count', 'URG Flag Count', 'CWR Flag Count', 'ECE Flag Count', 'Down/Up Ratio', 'Fwd Bytes/Bulk Avg', 'Fwd Bulk Rate Avg', 'Bwd Bytes/Bulk Avg', 'Bwd Bulk Rate Avg', 'Subflow Fwd Packets', 'Subflow Bwd Packets', 'FWD Init Win Bytes', 'Bwd Init Win Bytes', 'Fwd Act Data Pkts', 'Fwd Seg Size Min', 'Active Mean', 'Active Std', 'Active Max', 'Idle Std', 'ICMP Code', 'ICMP Type', 'Total TCP Flow Time']`
- Training machine learning models with the reduced feature set.
