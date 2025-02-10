Auswahl der features für das Modell:

**Vergleich CNS2022 Features (CICFlowmeter V4 optimized) mit CICIDS2017 Features (CICFlowmeter V4)**

Feature Mapping:
| #  | CNS2022 - CICIDS2017       | CNS2022 - CSECICIDS2018    | CICIDS2017 (Original)       | Renamed Dataset   |
|:---|:---------------------------|:---------------------------|:----------------------------|:------------------|
|   1| id                         | id                         | - | unnamed:_0 | - |
|   2| Flow ID                    | Flow ID                    | Flow ID | - |
|   3| Src IP                     | Src IP                     | Source IP | - |
|   4| Src Port                   | Src Port                   | Source Port | -|
|   5| Dst IP                     | Dst IP                     | Destination IP | -|
|   6| Dst Port                   | Dst Port                   | Destination Port |			dst_port	|				
|   7| Protocol                   | Protocol                   | Protocol | -|
|   8| Timestamp                  | Timestamp                  | Timestamp | -|
|   9| Flow Duration              | Flow Duration              | Flow Duration | flow_duration |
|  10| Total Fwd Packet           | Total Fwd Packet           | Total Fwd Packets | tot_fwd_pkts |
|  11| Total Bwd packets          | Total Bwd packets          | Total Backward Packets | tot_bwd_pkts |
|  12| Total Length of Fwd Packet | Total Length of Fwd Packet | Total Length of Fwd Packets | totlen_fwd_pkts |
|  13| Total Length of Bwd Packet | Total Length of Bwd Packet | Total Length of Bwd Packets | totlen_bwd_pkts |
|  14| Fwd Packet Length Max      | Fwd Packet Length Max      | Fwd Packet Length Max | fwd_pkt_len_max|
|  15| Fwd Packet Length Min      | Fwd Packet Length Min      | Fwd Packet Length Min |fwd_pkt_len_min |
|  16| Fwd Packet Length Mean     | Fwd Packet Length Mean     | Fwd Packet Length Mean | fwd_pkt_len_mean |
|  17| Fwd Packet Length Std      | Fwd Packet Length Std      | Fwd Packet Length Std | fwd_pkt_len_std |
|  18| Bwd Packet Length Max      | Bwd Packet Length Max      | Bwd Packet Length Max |bwd_pkt_len_max |
|  19| Bwd Packet Length Min      | Bwd Packet Length Min      | Bwd Packet Length Min |bwd_pkt_len_min |
|  20| Bwd Packet Length Mean     | Bwd Packet Length Mean     | Bwd Packet Length Mean |bwd_pkt_len_mean |
|  21| Bwd Packet Length Std      | Bwd Packet Length Std      | Bwd Packet Length Std |bwd_pkt_len_std |
|  22| Flow Bytes/s               | Flow Bytes/s               | Flow Bytes/s |flow_byts_s |
|  23| Flow Packets/s             | Flow Packets/s             | Flow Packets/s |flow_pkts_s |
|  24| Flow IAT Mean              | Flow IAT Mean              | Flow IAT Mean |flow_iat_mean |
|  25| Flow IAT Std               | Flow IAT Std               | Flow IAT Std |flow_iat_std |
|  26| Flow IAT Max               | Flow IAT Max               | Flow IAT Max |flow_iat_max |
|  27| Flow IAT Min               | Flow IAT Min               | Flow IAT Min |flow_iat_min |
|  28| Fwd IAT Total              | Fwd IAT Total              | Fwd IAT Total |fwd_iat_tot |
|  29| Fwd IAT Mean               | Fwd IAT Mean               | Fwd IAT Mean |fwd_iat_mean |
|  30| Fwd IAT Std                | Fwd IAT Std                | Fwd IAT Std |fwd_iat_std |
|  31| Fwd IAT Max                | Fwd IAT Max                | Fwd IAT Max |fwd_iat_max |
|  32| Fwd IAT Min                | Fwd IAT Min                | Fwd IAT Min |fwd_iat_min |
|  33| Bwd IAT Total              | Bwd IAT Total              | Bwd IAT Total |bwd_iat_tot |
|  34| Bwd IAT Mean               | Bwd IAT Mean               | Bwd IAT Mean |bwd_iat_mean |
|  35| Bwd IAT Std                | Bwd IAT Std                | Bwd IAT Std |bwd_iat_std |
|  36| Bwd IAT Max                | Bwd IAT Max                | Bwd IAT Max |bwd_iat_max |
|  37| Bwd IAT Min                | Bwd IAT Min                | Bwd IAT Min |bwd_iat_min |
|  38| Fwd PSH Flags              | Fwd PSH Flags              | Fwd PSH Flags | fwd_psh_flags |
|  39| Bwd PSH Flags              | Bwd PSH Flags              | Bwd PSH Flags ||
|  40| Fwd URG Flags              | Fwd URG Flags              | Fwd URG Flags | fwd_urg_flags |
|  41| Bwd URG Flags              | Bwd URG Flags              | Bwd URG Flags ||
|  42| Fwd RST Flags              | Fwd RST Flags              | -|
|  43| Bwd RST Flags              | Bwd RST Flags              | -|
|  44| Fwd Header Length          | Fwd Header Length          | Fwd Header Length |fwd_header_len
|  45| Bwd Header Length          | Bwd Header Length          | Bwd Header Length |bwd_header_len
|  46| Fwd Packets/s              | Fwd Packets/s              | Fwd Packets/s |fwd_pkts_s |
|  47| Bwd Packets/s              | Bwd Packets/s              | Bwd Packets/s |bwd_pkts_s |
|  48| Packet Length Min          | Packet Length Min          | Min Packet Length |pkt_len_min |
|  49| Packet Length Max          | Packet Length Max          | Max Packet Length |pkt_len_max |
|  50| Packet Length Mean         | Packet Length Mean         | Packet Length Mean |pkt_len_mean |
|  51| Packet Length Std          | Packet Length Std          | Packet Length Std |pkt_len_std |
|  52| Packet Length Variance     | Packet Length Variance     | Packet Length Variance| pkt_len_var |
|  53| FIN Flag Count             | FIN Flag Count             | FIN Flag Count |fin_flag_cnt |
|  54| SYN Flag Count             | SYN Flag Count             | SYN Flag Count |syn_flag_cnt |
|  55| RST Flag Count             | RST Flag Count             | RST Flag Count |rst_flag_cnt |
|  56| PSH Flag Count             | PSH Flag Count             | PSH Flag Count |psh_flag_cnt |
|  57| ACK Flag Count             | ACK Flag Count             | ACK Flag Count |ack_flag_cnt |
|  58| URG Flag Count             | URG Flag Count             | URG Flag Count |urg_flag_cnt |
|  59| CWR Flag Count             | CWR Flag Count             | CWE Flag Count |cwr_flag_count |
|  60| ECE Flag Count             | ECE Flag Count             | ECE Flag Count |ece_flag_cnt |
|  61| Down/Up Ratio              | Down/Up Ratio              | Down/Up Ratio | down_up_ratio |
|  62| Average Packet Size        | Average Packet Size        | Average Packet Size |pkt_size_avg |
|  63| Fwd Segment Size Avg       | Fwd Segment Size Avg       | Avg Fwd Segment Size |fwd_seg_size_avg |
|  64| Bwd Segment Size Avg       | Bwd Segment Size Avg       | Avg Bwd Segment Size |bwd_seg_size_avg |
|  65| Fwd Bytes/Bulk Avg         | Fwd Bytes/Bulk Avg         | Fwd Avg Bytes/Bulk  |
|  66| Fwd Packet/Bulk Avg        | Fwd Packet/Bulk Avg        | Fwd Avg Packets/Bulk |
|  67| Fwd Bulk Rate Avg          | Fwd Bulk Rate Avg          | Fwd Avg Bulk Rate
|  68| Bwd Bytes/Bulk Avg         | Bwd Bytes/Bulk Avg         | Bwd Avg Bytes/Bulk |
|  69| Bwd Packet/Bulk Avg        | Bwd Packet/Bulk Avg        | Bwd Avg Packets/Bulk |
|  70| Bwd Bulk Rate Avg          | Bwd Bulk Rate Avg          | Bwd Avg Bulk Rate |
|  71| Subflow Fwd Packets        | Subflow Fwd Packets        | Subflow Fwd Packets |subflow_fwd_pkts |
|  72| Subflow Fwd Bytes          | Subflow Fwd Bytes          | Subflow Fwd Bytes |subflow_fwd_byts |
|  73| Subflow Bwd Packets        | Subflow Bwd Packets        | Subflow Bwd Packets |subflow_bwd_pkts |
|  74| Subflow Bwd Bytes          | Subflow Bwd Bytes          | Subflow Bwd Bytes |subflow_bwd_byts |
|  75| FWD Init Win Bytes         | FWD Init Win Bytes         | Init_Win_bytes_forward  |init_fwd_win_byts |
|  76| Bwd Init Win Bytes         | Bwd Init Win Bytes         | Init_Win_bytes_backward |init_bwd_win_byts |
|  77| Fwd Act Data Pkts          | Fwd Act Data Pkts          | act_data_pkt_fwd |fwd_act_data_pkts |
|  78| Fwd Seg Size Min           | Fwd Seg Size Min           | min_seg_size_forward |fwd_seg_size_min |
|  79| Active Mean                | Active Mean                | Active Mean |active_mean |
|  80| Active Std                 | Active Std                 | Active Std |active_std |
|  81| Active Max                 | Active Max                 | Active Max |active_max |
|  82| Active Min                 | Active Min                 | Active Min |active_min |
|  83| Idle Mean                  | Idle Mean                  | Idle Mean |idle_mean |
|  84| Idle Std                   | Idle Std                   | Idle Std |idle_std |
|  85| Idle Max                   | Idle Max                   | Idle Max |idle_max |
|  86| Idle Min                   | Idle Min                   | Idle Min |idle_min |
|  87| ICMP Code                  | ICMP Code                  | -|
|  88| ICMP Type                  | ICMP Type                  | -|
|  89| Total TCP Flow Time        | Total TCP Flow Time        | -|
|  90| Label                      | Label                      | Label |
|  91| Attempted Category         | Attempted Category         | -|
|	|	|	|	|	attack_type |
|	|	|	|	|	attack_number |



Die Datensets haben folgende features:

| # | Feature | # | Feature | # | Feature | # | Feature |
|---|---------|---|---------|---|---------|---|---------|
| 1 | id | 22 | Flow Bytes/s | 43 | Fwd Header Length | 64 | Bwd Bulk Rate Avg |
| 2 | Flow ID | 23 | Flow Packets/s | 44 | Bwd Header Length | 65 | Subflow Fwd Packets |
| 3 | Src IP | 24 | Flow IAT Mean | 45 | Fwd Packets/s | 66 | Subflow Fwd Bytes |
| 4 | Src Port | 25 | Flow IAT Std | 46 | Bwd Packets/s | 67 | Subflow Bwd Packets |
| 5 | Dst IP | 26 | Flow IAT Max | 47 | Packet Length Min | 68 | Subflow Bwd Bytes |
| 6 | Dst Port | 27 | Flow IAT Min | 48 | Packet Length Max | 69 | FWD Init Win Bytes |
| 7 | Protocol | 28 | Fwd IAT Mean | 49 | Packet Length Mean | 70 | Bwd Init Win Bytes |
| 8 | Timestamp | 29 | Fwd IAT Std | 50 | Packet Length Std | 71 | Fwd Act Data Pkts |
| 9 | Flow Duration | 30 | Fwd IAT Max | 51 | Packet Length Variance | 72 | Fwd Seg Size Min |
| 10 | Total Fwd Packet | 31 | Fwd IAT Min | 52 | FIN Flag Count | 73 | Active Mean |
| 11 | Total Bwd packets | 32 | Bwd IAT Total | 53 | SYN Flag Count | 74 | Active Std |
| 12 | Total Length of Fwd Packet | 33 | Bwd IAT Mean | 54 | RST Flag Count | 75 | Active Max |
| 13 | Total Length of Bwd Packet | 34 | Bwd IAT Std | 55 | PSH Flag Count | 76 | Active Min |
| 14 | Fwd Packet Length Max | 35 | Bwd IAT Max | 56 | ACK Flag Count | 77 | Idle Mean |
| 15 | Fwd Packet Length Min | 36 | Bwd IAT Min | 57 | URG Flag Count | 78 | Idle Std |
| 16 | Fwd Packet Length Mean | 37 | Fwd PSH Flags | 58 | CWR Flag Count | 79 | Idle Max |
| 17 | Fwd Packet Length Std | 38 | Bwd PSH Flags | 59 | ECE Flag Count | 80 | Idle Min |
| 18 | Bwd Packet Length Max | 39 | Fwd URG Flags | 60 | Down/Up Ratio | 81 | ICMP Code |
| 19 | Bwd Packet Length Min | 40 | Bwd URG Flags | 61 | Average Packet Size | 82 | ICMP Type |
| 20 | Bwd Packet Length Mean | 41 | Fwd RST Flags | 62 | Fwd Segment Size Avg | 83 | Total TCP Flow Time |
| 21 | Bwd Packet Length Std | 42 | Bwd RST Flags | 63 | Bwd Segment Size Avg | 84 | Label |
| | | | | | | 85 | Attempted Category |


