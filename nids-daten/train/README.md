
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

| #  | **CNS2022**                     | **Selected Features**            | #  | **CNS2022**                     | **Selected Features**            |
|----|----------------------------------|----------------------------------|----|----------------------------------|----------------------------------|
| 1  | id                               | -                                | 40 | Bwd IAT Min                     | bwd_iat_min                      |
| 2  | Flow ID                          | -                                | 41 | Fwd PSH Flags                   | fwd_psh_flags                    |
| 3  | Src IP                           | -                                | 42 | Bwd PSH Flags                   | -                                |
| 4  | Src Port                         | -                                | 43 | Fwd URG Flags                   | fwd_urg_flags                    |
| 5  | Dst IP                           | -                                | 44 | Bwd URG Flags                   | -                                |
| 6  | Dst Port                         | dst_port                         | 45 | Fwd RST Flags                   | -                                |
| 7  | Protocol                         | -                                | 46 | Bwd RST Flags                   | -                                |
| 8  | Timestamp                        | -                                | 47 | Fwd Header Length               | fwd_header_len                   |
| 9  | Flow Duration                    | flow_duration                    | 48 | Bwd Header Length               | bwd_header_len                   |
| 10 | Total Fwd Packet                 | tot_fwd_pkts                     | 49 | Fwd Packets/s                   | fwd_pkts_s                       |
| 11 | Total Bwd packets                | tot_bwd_pkts                     | 50 | Bwd Packets/s                   | bwd_pkts_s                       |
| 12 | Total Length of Fwd Packet       | totlen_fwd_pkts                  | 51 | Packet Length Min               | pkt_len_min                      |
| 13 | Total Length of Bwd Packet       | totlen_bwd_pkts                  | 52 | Packet Length Max               | pkt_len_max                      |
| 14 | Fwd Packet Length Max            | fwd_pkt_len_max                  | 53 | Packet Length Mean              | pkt_len_mean                     |
| 15 | Fwd Packet Length Min            | fwd_pkt_len_min                  | 54 | Packet Length Std               | pkt_len_std                      |
| 16 | Fwd Packet Length Mean           | fwd_pkt_len_mean                 | 55 | Packet Length Variance          | pkt_len_var                      |
| 17 | Fwd Packet Length Std            | fwd_pkt_len_std                  | 56 | FIN Flag Count                  | fin_flag_cnt                     |
| 18 | Bwd Packet Length Max            | bwd_pkt_len_max                  | 57 | SYN Flag Count                  | syn_flag_cnt                     |
| 19 | Bwd Packet Length Min            | bwd_pkt_len_min                  | 58 | RST Flag Count                  | rst_flag_cnt                     |
| 20 | Bwd Packet Length Mean           | bwd_pkt_len_mean                 | 59 | PSH Flag Count                  | psh_flag_cnt                     |
| 21 | Bwd Packet Length Std            | bwd_pkt_len_std                  | 60 | ACK Flag Count                  | ack_flag_cnt                     |
| 22 | Flow Bytes/s                     | flow_byts_s                      | 61 | URG Flag Count                  | urg_flag_cnt                     |
| 23 | Flow Packets/s                   | flow_pkts_s                      | 62 | CWR Flag Count                  | cwr_flag_count                   |
| 24 | Flow IAT Mean                    | flow_iat_mean                    | 63 | ECE Flag Count                  | ece_flag_cnt                     |
| 25 | Flow IAT Std                     | flow_iat_std                     | 64 | Down/Up Ratio                   | down_up_ratio                    |
| 26 | Flow IAT Max                     | flow_iat_max                     | 65 | Average Packet Size             | pkt_size_avg                     |
| 27 | Flow IAT Min                     | flow_iat_min                     | 66 | Fwd Segment Size Avg            | fwd_seg_size_avg                 |
| 28 | Fwd IAT Total                    | fwd_iat_tot                      | 67 | Bwd Segment Size Avg            | bwd_seg_size_avg                 |
| 29 | Fwd IAT Mean                     | fwd_iat_mean                     | 68 | Fwd Bytes/Bulk Avg              | -                                |
| 30 | Fwd IAT Std                      | fwd_iat_std                      | 69 | Fwd Packet/Bulk Avg             | -                                |
| 31 | Fwd IAT Max                      | fwd_iat_max                      | 70 | Fwd Bulk Rate Avg               | -                                |
| 32 | Fwd IAT Min                      | fwd_iat_min                      | 71 | Bwd Bytes/Bulk Avg              | -                                |
| 33 | Bwd IAT Total                    | bwd_iat_tot                      | 72 | Bwd Packet/Bulk Avg             | -                                |
| 34 | Bwd IAT Mean                     | bwd_iat_mean                      | 73 | Bwd Bulk Rate Avg               | -                                |
| 35 | Bwd IAT Std                      | bwd_iat_std                      | 74 | Subflow Fwd Packets             | subflow_fwd_pkts                 |
| 36 | Bwd IAT Max                      | bwd_iat_max                      | 75 | Subflow Fwd Bytes               | subflow_fwd_byts                 |
| 37 | Bwd IAT Min                      | bwd_iat_min                      | 76 | Subflow Bwd Packets             | subflow_bwd_pkts                 |
| 38 | Active Mean                      | active_mean                      | 77 | Subflow Bwd Bytes               | subflow_bwd_byts                 |
| 39 | Active Std                       | active_std                       | 78 | FWD Init Win Bytes              | init_fwd_win_byts                |
| 79 | Bwd Init Win Bytes               | init_bwd_win_byts                | 80 | Fwd Act Data Pkts               | fwd_act_data_pkts                |
| 81 | Fwd Seg Size Min                 | fwd_seg_size_min                 | 82 | Active Mean                     | active_mean                      |
| 83 | Active Std                       | active_std                       | 84 | Active Max                      | active_max                      |
| 85 | Active Min                       | active_min                        | 86 | Idle Mean                       | idle_mean                        |
| 87 | Idle Std                         | idle_std                         | 88 | Idle Max                        | idle_max                         |
| 89 | Idle Min                         | idle_min                         | 90 | ICMP Code                       | -                                |
| 91 | ICMP Type                        | -                                | 92 | Total TCP Flow Time             | -                                |
| 93 | Label                            | -                                | 94 | Attempted Category              | -                                |



**Vergleich CNS2022 Features (CICFlowmeter V4 optimized) mit CICIDS2017 Features (CICFlowmeter V4)**

| #  | **CNS2022**                     | **CICIDS2017**                   | #  | **CNS2022**                     | **CICIDS2017**                   |
|----|----------------------------------|----------------------------------|----|----------------------------------|----------------------------------|
| 1  | id                               | (Not in CICIDS2017)              | 38 | Fwd PSH Flags                   | Fwd PSH Flags                   |
| 2  | Flow ID                          | Flow ID                          | 39 | Bwd PSH Flags                   | (Not in CICIDS2017)              |
| 3  | Src IP                           | Source IP                        | 40 | Fwd URG Flags                   | Fwd URG Flags                   |
| 4  | Src Port                         | Source Port                      | 41 | Bwd URG Flags                   | (Not in CICIDS2017)              |
| 5  | Dst IP                           | Destination IP                   | 42 | Fwd RST Flags                   | (Not in CICIDS2017)              |
| 6  | Dst Port                         | Destination Port                 | 43 | Bwd RST Flags                   | (Not in CICIDS2017)              |
| 7  | Protocol                         | Protocol                         | 44 | Fwd Header Length               | Fwd Header Length               |
| 8  | Timestamp                        | Timestamp                        | 45 | Bwd Header Length               | Bwd Header Length               |
| 9  | Flow Duration                    | Flow Duration                    | 46 | Fwd Packets/s                   | Fwd Packets/s                   |
| 10 | Total Fwd Packet                 | Total Fwd Packets                | 47 | Bwd Packets/s                   | Bwd Packets/s                   |
| 11 | Total Bwd packets                | Total Backward Packets           | 48 | Packet Length Min               | Min Packet Length               |
| 12 | Total Length of Fwd Packet       | Total Length of Fwd Packets      | 49 | Packet Length Max               | Max Packet Length               |
| 13 | Total Length of Bwd Packet       | Total Length of Bwd Packets      | 50 | Packet Length Mean              | Packet Length Mean              |
| 14 | Fwd Packet Length Max            | Fwd Packet Length Max            | 51 | Packet Length Std               | Packet Length Std               |
| 15 | Fwd Packet Length Min            | Fwd Packet Length Min            | 52 | Packet Length Variance          | Packet Length Variance          |
| 16 | Fwd Packet Length Mean           | Fwd Packet Length Mean           | 53 | FIN Flag Count                  | FIN Flag Count                  |
| 17 | Fwd Packet Length Std            | Fwd Packet Length Std            | 54 | SYN Flag Count                  | SYN Flag Count                  |
| 18 | Bwd Packet Length Max            | Bwd Packet Length Max            | 55 | RST Flag Count                  | RST Flag Count                  |
| 19 | Bwd Packet Length Min            | Bwd Packet Length Min            | 56 | PSH Flag Count                  | PSH Flag Count                  |
| 20 | Bwd Packet Length Mean           | Bwd Packet Length Mean           | 57 | ACK Flag Count                  | ACK Flag Count                  |
| 21 | Bwd Packet Length Std            | Bwd Packet Length Std            | 58 | URG Flag Count                  | URG Flag Count                  |
| 22 | Flow Bytes/s                     | Flow Bytes/s                     | 59 | CWR Flag Count                  | CWE Flag Count                  |
| 23 | Flow Packets/s                   | Flow Packets/s                   | 60 | ECE Flag Count                  | ECE Flag Count                  |
| 24 | Flow IAT Mean                    | Flow IAT Mean                    | 61 | Down/Up Ratio                   | Down/Up Ratio                   |
| 25 | Flow IAT Std                     | Flow IAT Std                     | 62 | Average Packet Size             | Average Packet Size             |
| 26 | Flow IAT Max                     | Flow IAT Max                     | 63 | Fwd Segment Size Avg            | Avg Fwd Segment Size            |
| 27 | Flow IAT Min                     | Flow IAT Min                     | 64 | Bwd Segment Size Avg            | Avg Bwd Segment Size            |
| 28 | Fwd IAT Total                    | Fwd IAT Total                    | 65 | Fwd Bytes/Bulk Avg              | Fwd Avg Bytes/Bulk              |
| 29 | Fwd IAT Mean                     | Fwd IAT Mean                     | 66 | Fwd Packet/Bulk Avg             | Fwd Avg Packets/Bulk            |
| 30 | Fwd IAT Std                      | Fwd IAT Std                      | 67 | Fwd Bulk Rate Avg               | Fwd Avg Bulk Rate               |
| 31 | Fwd IAT Max                      | Fwd IAT Max                      | 68 | Bwd Bytes/Bulk Avg              | Bwd Avg Bytes/Bulk              |
| 32 | Fwd IAT Min                      | Fwd IAT Min                      | 69 | Bwd Packet/Bulk Avg             | Bwd Avg Packets/Bulk            |
| 33 | Bwd IAT Total                    | Bwd IAT Total                    | 70 | Bwd Bulk Rate Avg               | Bwd Avg Bulk Rate               |
| 34 | Bwd IAT Mean                     | Bwd IAT Mean                     | 71 | Subflow Fwd Packets             | Subflow Fwd Packets             |
| 35 | Bwd IAT Std                      | Bwd IAT Std                      | 72 | Subflow Fwd Bytes               | Subflow Fwd Bytes               |
| 36 | Bwd IAT Max                      | Bwd IAT Max                      | 73 | Subflow Bwd Packets             | Subflow Bwd Packets             |
| 37 | Bwd IAT Min                      | Bwd IAT Min                      | 74 | Subflow Bwd Bytes               | Subflow Bwd Bytes               |


