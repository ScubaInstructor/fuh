# Data Cleaning Report: `Wednesday-14-02-2018.csv`

- **File Size**: 3111.44 MB
- **Data set Name**: Wednesday-14-02-2018.csv
- **Number of Records**: 5898350
- **Explicitly Dropped Columns**: 🗑️ `['id', 'Attempted Category', 'Src Port']` to be manually removed
- **Python Command to Drop Columns**: 💡 To drop these columns, use:
``````
- **Leading Spaces in Feature Names**: No issues found
- **Categorical Columns**: ⚠️ Found 5 categorical columns: `['Flow ID', 'Src IP', 'Dst IP', 'Timestamp', 'Label']`
- **Categorical Columns Check**: No categorical columns removed (Flag `--drop_categorical_columns=False`).
💡 To drop them manually, use:
``````
- **Zero Variance Columns**: ⚠️ Found 3 zero variance columns: `['Fwd URG Flags', 'Bwd URG Flags', 'URG Flag Count']`
💡 To drop these columns, use:
``````
- **Negative Values**: ⚠️ Found 11781307 negative values in columns: `['Fwd Header Length', 'Bwd Header Length', 'ICMP Code', 'ICMP Type']`
💡 To replace with zero, use:
``````
- **Infinite Values**: ⚠️ Found 2 infinite values in columns `['Flow Bytes/s', 'Flow Packets/s']`.
💡 To replace with NaN, use:
``````
- **Missing Values**: No issues found
- **Highly Correlated Features**: ⚠️ Found 21 highly correlated features (threshold: 0.95).
Highly correlated feature pairs:
- Total Length of Bwd Packet: Correlated with ['Total Bwd packets'] (threshold: 0.95)
- Fwd Packet Length Std: Correlated with ['Fwd Packet Length Max'] (threshold: 0.95)
- Bwd Packet Length Std: Correlated with ['Bwd Packet Length Max'] (threshold: 0.95)
- Fwd IAT Total: Correlated with ['Flow Duration'] (threshold: 0.95)
- Bwd IAT Total: Correlated with ['Flow Duration', 'Fwd IAT Total'] (threshold: 0.95)
- Bwd IAT Max: Correlated with ['Flow IAT Max'] (threshold: 0.95)
- Fwd Packets/s: Correlated with ['Flow Packets/s'] (threshold: 0.95)
- Bwd Packets/s: Correlated with ['Flow Packets/s', 'Fwd Packets/s'] (threshold: 0.95)
- Packet Length Min: Correlated with ['Fwd Packet Length Min'] (threshold: 0.95)
- ACK Flag Count: Correlated with ['Total Bwd packets', 'Total Length of Bwd Packet'] (threshold: 0.95)
- Average Packet Size: Correlated with ['Packet Length Mean'] (threshold: 0.95)
- Fwd Segment Size Avg: Correlated with ['Fwd Packet Length Mean'] (threshold: 0.95)
- Bwd Segment Size Avg: Correlated with ['Bwd Packet Length Mean'] (threshold: 0.95)
- Fwd Packet/Bulk Avg: Correlated with ['Fwd Bytes/Bulk Avg'] (threshold: 0.95)
- Bwd Packet/Bulk Avg: Correlated with ['Bwd Bytes/Bulk Avg'] (threshold: 0.95)
- Subflow Fwd Bytes: Correlated with ['Fwd Packet Length Mean', 'Fwd Segment Size Avg'] (threshold: 0.95)
- Subflow Bwd Bytes: Correlated with ['Bwd Packet Length Mean', 'Bwd Segment Size Avg'] (threshold: 0.95)
- Active Min: Correlated with ['Active Mean'] (threshold: 0.95)
- Idle Mean: Correlated with ['Flow IAT Max', 'Bwd IAT Max'] (threshold: 0.95)
- Idle Max: Correlated with ['Flow IAT Max', 'Bwd IAT Max', 'Idle Mean'] (threshold: 0.95)
- Idle Min: Correlated with ['Idle Mean'] (threshold: 0.95)
💡 To drop these features, use:
``````
- **Feature Scaling**: ⚠️ Scaling recommended but no method specified
- **Feature Selection**: ⚠️ PCA analysis results:
 - 95% variance retained with 1 components (reduced from 83 to 1)
 - 99% variance retained with 2 components (reduced from 83 to 2)
 - 99.9% variance retained with 3 components (reduced from 83 to 3)

- **Feature Selection Command**: 💡 To apply PCA, use:
``````
- **Available Columns**: After cleaning, the following columns are available: `['Dst Port', 'Protocol', 'Flow Duration', 'Total Fwd Packet', 'Total Bwd packets', 'Total Length of Fwd Packet', 'Total Length of Bwd Packet', 'Fwd Packet Length Max', 'Fwd Packet Length Min', 'Fwd Packet Length Mean', 'Fwd Packet Length Std', 'Bwd Packet Length Max', 'Bwd Packet Length Min', 'Bwd Packet Length Mean', 'Bwd Packet Length Std', 'Flow Bytes/s', 'Flow Packets/s', 'Flow IAT Mean', 'Flow IAT Std', 'Flow IAT Max', 'Flow IAT Min', 'Fwd IAT Total', 'Fwd IAT Mean', 'Fwd IAT Std', 'Fwd IAT Max', 'Fwd IAT Min', 'Bwd IAT Total', 'Bwd IAT Mean', 'Bwd IAT Std', 'Bwd IAT Max', 'Bwd IAT Min', 'Fwd PSH Flags', 'Bwd PSH Flags', 'Fwd URG Flags', 'Bwd URG Flags', 'Fwd RST Flags', 'Bwd RST Flags', 'Fwd Header Length', 'Bwd Header Length', 'Fwd Packets/s', 'Bwd Packets/s', 'Packet Length Min', 'Packet Length Max', 'Packet Length Mean', 'Packet Length Std', 'Packet Length Variance', 'FIN Flag Count', 'SYN Flag Count', 'RST Flag Count', 'PSH Flag Count', 'ACK Flag Count', 'URG Flag Count', 'CWR Flag Count', 'ECE Flag Count', 'Down/Up Ratio', 'Average Packet Size', 'Fwd Segment Size Avg', 'Bwd Segment Size Avg', 'Fwd Bytes/Bulk Avg', 'Fwd Packet/Bulk Avg', 'Fwd Bulk Rate Avg', 'Bwd Bytes/Bulk Avg', 'Bwd Packet/Bulk Avg', 'Bwd Bulk Rate Avg', 'Subflow Fwd Packets', 'Subflow Fwd Bytes', 'Subflow Bwd Packets', 'Subflow Bwd Bytes', 'FWD Init Win Bytes', 'Bwd Init Win Bytes', 'Fwd Act Data Pkts', 'Fwd Seg Size Min', 'Active Mean', 'Active Std', 'Active Max', 'Active Min', 'Idle Mean', 'Idle Std', 'Idle Max', 'Idle Min', 'ICMP Code', 'ICMP Type', 'Total TCP Flow Time']`
- **Recommendation**: Based on the assessment, it is recommended to continue working with the available columns. You may consider the following:
- Performing further analysis using the available columns: `['Dst Port', 'Protocol', 'Flow Duration', 'Total Fwd Packet', 'Total Bwd packets', 'Total Length of Fwd Packet', 'Total Length of Bwd Packet', 'Fwd Packet Length Max', 'Fwd Packet Length Min', 'Fwd Packet Length Mean', 'Fwd Packet Length Std', 'Bwd Packet Length Max', 'Bwd Packet Length Min', 'Bwd Packet Length Mean', 'Bwd Packet Length Std', 'Flow Bytes/s', 'Flow Packets/s', 'Flow IAT Mean', 'Flow IAT Std', 'Flow IAT Max', 'Flow IAT Min', 'Fwd IAT Total', 'Fwd IAT Mean', 'Fwd IAT Std', 'Fwd IAT Max', 'Fwd IAT Min', 'Bwd IAT Total', 'Bwd IAT Mean', 'Bwd IAT Std', 'Bwd IAT Max', 'Bwd IAT Min', 'Fwd PSH Flags', 'Bwd PSH Flags', 'Fwd URG Flags', 'Bwd URG Flags', 'Fwd RST Flags', 'Bwd RST Flags', 'Fwd Header Length', 'Bwd Header Length', 'Fwd Packets/s', 'Bwd Packets/s', 'Packet Length Min', 'Packet Length Max', 'Packet Length Mean', 'Packet Length Std', 'Packet Length Variance', 'FIN Flag Count', 'SYN Flag Count', 'RST Flag Count', 'PSH Flag Count', 'ACK Flag Count', 'URG Flag Count', 'CWR Flag Count', 'ECE Flag Count', 'Down/Up Ratio', 'Average Packet Size', 'Fwd Segment Size Avg', 'Bwd Segment Size Avg', 'Fwd Bytes/Bulk Avg', 'Fwd Packet/Bulk Avg', 'Fwd Bulk Rate Avg', 'Bwd Bytes/Bulk Avg', 'Bwd Packet/Bulk Avg', 'Bwd Bulk Rate Avg', 'Subflow Fwd Packets', 'Subflow Fwd Bytes', 'Subflow Bwd Packets', 'Subflow Bwd Bytes', 'FWD Init Win Bytes', 'Bwd Init Win Bytes', 'Fwd Act Data Pkts', 'Fwd Seg Size Min', 'Active Mean', 'Active Std', 'Active Max', 'Active Min', 'Idle Mean', 'Idle Std', 'Idle Max', 'Idle Min', 'ICMP Code', 'ICMP Type', 'Total TCP Flow Time']`
- Training machine learning models with the reduced feature set.
- **Available Columns and Recommended Mapping**: The following columns are available after cleaning. Recommended mapping:
| # | Column Name | Mapping |
|---|---|---|
| 1 | Dst Port | dst_port |
| 2 | Protocol | protocol |
| 3 | Flow Duration | flow_duration |
| 4 | Total Fwd Packet | total_fwd_packet |
| 5 | Total Bwd packets | total_bwd_packets |
| 6 | Total Length of Fwd Packet | total_length_of_fwd_packet |
| 7 | Total Length of Bwd Packet | total_length_of_bwd_packet |
| 8 | Fwd Packet Length Max | fwd_packet_length_max |
| 9 | Fwd Packet Length Min | fwd_packet_length_min |
| 10 | Fwd Packet Length Mean | fwd_packet_length_mean |
| 11 | Fwd Packet Length Std | fwd_packet_length_std |
| 12 | Bwd Packet Length Max | bwd_packet_length_max |
| 13 | Bwd Packet Length Min | bwd_packet_length_min |
| 14 | Bwd Packet Length Mean | bwd_packet_length_mean |
| 15 | Bwd Packet Length Std | bwd_packet_length_std |
| 16 | Flow Bytes/s | flow_bytes/s |
| 17 | Flow Packets/s | flow_packets/s |
| 18 | Flow IAT Mean | flow_iat_mean |
| 19 | Flow IAT Std | flow_iat_std |
| 20 | Flow IAT Max | flow_iat_max |
| 21 | Flow IAT Min | flow_iat_min |
| 22 | Fwd IAT Total | fwd_iat_total |
| 23 | Fwd IAT Mean | fwd_iat_mean |
| 24 | Fwd IAT Std | fwd_iat_std |
| 25 | Fwd IAT Max | fwd_iat_max |
| 26 | Fwd IAT Min | fwd_iat_min |
| 27 | Bwd IAT Total | bwd_iat_total |
| 28 | Bwd IAT Mean | bwd_iat_mean |
| 29 | Bwd IAT Std | bwd_iat_std |
| 30 | Bwd IAT Max | bwd_iat_max |
| 31 | Bwd IAT Min | bwd_iat_min |
| 32 | Fwd PSH Flags | fwd_psh_flags |
| 33 | Bwd PSH Flags | bwd_psh_flags |
| 34 | Fwd URG Flags | fwd_urg_flags |
| 35 | Bwd URG Flags | bwd_urg_flags |
| 36 | Fwd RST Flags | fwd_rst_flags |
| 37 | Bwd RST Flags | bwd_rst_flags |
| 38 | Fwd Header Length | fwd_header_length |
| 39 | Bwd Header Length | bwd_header_length |
| 40 | Fwd Packets/s | fwd_packets/s |
| 41 | Bwd Packets/s | bwd_packets/s |
| 42 | Packet Length Min | packet_length_min |
| 43 | Packet Length Max | packet_length_max |
| 44 | Packet Length Mean | packet_length_mean |
| 45 | Packet Length Std | packet_length_std |
| 46 | Packet Length Variance | packet_length_variance |
| 47 | FIN Flag Count | fin_flag_count |
| 48 | SYN Flag Count | syn_flag_count |
| 49 | RST Flag Count | rst_flag_count |
| 50 | PSH Flag Count | psh_flag_count |
| 51 | ACK Flag Count | ack_flag_count |
| 52 | URG Flag Count | urg_flag_count |
| 53 | CWR Flag Count | cwr_flag_count |
| 54 | ECE Flag Count | ece_flag_count |
| 55 | Down/Up Ratio | down/up_ratio |
| 56 | Average Packet Size | average_packet_size |
| 57 | Fwd Segment Size Avg | fwd_segment_size_avg |
| 58 | Bwd Segment Size Avg | bwd_segment_size_avg |
| 59 | Fwd Bytes/Bulk Avg | fwd_bytes/bulk_avg |
| 60 | Fwd Packet/Bulk Avg | fwd_packet/bulk_avg |
| 61 | Fwd Bulk Rate Avg | fwd_bulk_rate_avg |
| 62 | Bwd Bytes/Bulk Avg | bwd_bytes/bulk_avg |
| 63 | Bwd Packet/Bulk Avg | bwd_packet/bulk_avg |
| 64 | Bwd Bulk Rate Avg | bwd_bulk_rate_avg |
| 65 | Subflow Fwd Packets | subflow_fwd_packets |
| 66 | Subflow Fwd Bytes | subflow_fwd_bytes |
| 67 | Subflow Bwd Packets | subflow_bwd_packets |
| 68 | Subflow Bwd Bytes | subflow_bwd_bytes |
| 69 | FWD Init Win Bytes | fwd_init_win_bytes |
| 70 | Bwd Init Win Bytes | bwd_init_win_bytes |
| 71 | Fwd Act Data Pkts | fwd_act_data_pkts |
| 72 | Fwd Seg Size Min | fwd_seg_size_min |
| 73 | Active Mean | active_mean |
| 74 | Active Std | active_std |
| 75 | Active Max | active_max |
| 76 | Active Min | active_min |
| 77 | Idle Mean | idle_mean |
| 78 | Idle Std | idle_std |
| 79 | Idle Max | idle_max |
| 80 | Idle Min | idle_min |
| 81 | ICMP Code | icmp_code |
| 82 | ICMP Type | icmp_type |
| 83 | Total TCP Flow Time | total_tcp_flow_time |

