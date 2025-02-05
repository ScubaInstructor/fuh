
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


Auswahl der features für das Modell:

| CNS2022 | Selected features |
|--------------|-------------|
| id | - |
| Flow ID | - |
| Src IP | - |
| Src Port | - |
| Dst IP | - |
| Dst Port | dst_port |
| Protocol | - |
| Timestamp | - |
| Flow Duration | flow_duration |
| Total Fwd Packet | tot_fwd_pkts |
| Total Bwd packets | tot_bwd_pkts |
| Total Length of Fwd Packet | totlen_fwd_pkts |
| Total Length of Bwd Packet | totlen_bwd_pkts |
| Fwd Packet Length Max | fwd_pkt_len_max |
| Fwd Packet Length Min | fwd_pkt_len_min |
| Fwd Packet Length Mean | fwd_pkt_len_mean |
| Fwd Packet Length Std | fwd_pkt_len_std |
| Bwd Packet Length Max | bwd_pkt_len_max |
| Bwd Packet Length Min | bwd_pkt_len_min |
| Bwd Packet Length Mean | bwd_pkt_len_mean |
| Bwd Packet Length Std | bwd_pkt_len_std |
| Flow Bytes/s | flow_byts_s |
| Flow Packets/s | flow_pkts_s |
| Flow IAT Mean | flow_iat_mean |
| Flow IAT Std | flow_iat_std |
| Flow IAT Max | flow_iat_max |
| Flow IAT Min | flow_iat_min |
| Fwd IAT Total | fwd_iat_tot |
| Fwd IAT Mean | fwd_iat_mean |
| Fwd IAT Std | fwd_iat_std |
| Fwd IAT Max | fwd_iat_max |
| Fwd IAT Min | fwd_iat_min |
| Bwd IAT Total | bwd_iat_tot |
| Bwd IAT Mean | bwd_iat_mean |
| Bwd IAT Std | bwd_iat_std |
| Bwd IAT Max | bwd_iat_max |
| Bwd IAT Min | bwd_iat_min |
| Fwd PSH Flags | fwd_psh_flags |
| Bwd PSH Flags | - |
| Fwd URG Flags | fwd_urg_flags |
| Bwd URG Flags | - |
| Fwd RST Flags | - |
| Bwd RST Flags | - |
| Fwd Header Length | fwd_header_len |
| Bwd Header Length | bwd_header_len |
| Fwd Packets/s | fwd_pkts_s |
| Bwd Packets/s | bwd_pkts_s |
| Packet Length Min | pkt_len_min |
| Packet Length Max | pkt_len_max |
| Packet Length Mean | pkt_len_mean |
| Packet Length Std | pkt_len_std |
| Packet Length Variance | pkt_len_var |
| FIN Flag Count | fin_flag_cnt |
| SYN Flag Count | syn_flag_cnt |
| RST Flag Count | rst_flag_cnt |
| PSH Flag Count | psh_flag_cnt |
| ACK Flag Count | ack_flag_cnt |
| URG Flag Count | urg_flag_cnt |
| CWR Flag Count | cwr_flag_count |
| ECE Flag Count | ece_flag_cnt |
| Down/Up Ratio | down_up_ratio |
| Average Packet Size | pkt_size_avg |
| Fwd Segment Size Avg | fwd_seg_size_avg |
| Bwd Segment Size Avg | bwd_seg_size_avg |
| Fwd Bytes/Bulk Avg | - |
| Fwd Packet/Bulk Avg | - |
| Fwd Bulk Rate Avg | - |
| Bwd Bytes/Bulk Avg | - |
| Bwd Packet/Bulk Avg | - |
| Bwd Bulk Rate Avg | - |
| Subflow Fwd Packets | subflow_fwd_pkts |
| Subflow Fwd Bytes | subflow_fwd_byts |
| Subflow Bwd Packets | subflow_bwd_pkts |
| Subflow Bwd Bytes | subflow_bwd_byts |
| FWD Init Win Bytes | init_fwd_win_byts |
| Bwd Init Win Bytes | init_bwd_win_byts |
| Fwd Act Data Pkts | fwd_act_data_pkts |
| Fwd Seg Size Min | fwd_seg_size_min |
| Active Mean | active_mean |
| Active Std | active_std |
| Active Max | active_max |
| Active Min | active_min |
| Idle Mean | idle_mean |
| Idle Std | idle_std |
| Idle Max | idle_max |
| Idle Min | idle_min |
| ICMP Code | - |
| ICMP Type | - |
| Total TCP Flow Time | - |
| Label | - |
| Attempted Category | - |
