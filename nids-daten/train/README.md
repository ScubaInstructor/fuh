
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

| #  | **CNS2022 - CICIDS2017**        | **CNS2022 - CSECICIDS2018**       | **CICIDS2017 (Original)**        | **Renamed Dataset**              |
|----|---------------------------------|----------------------------------|----------------------------------|----------------------------------|
| 1  | id                              | id                               | Flow ID                          | unnamed:_0                      |
| 2  | Flow ID                         | Flow ID                         | Source IP                        | dst_port                        |
| 3  | Src IP                          | Src IP                          | Source Port                      | flow_duration                   |
| 4  | Src Port                        | Src Port                        | Destination IP                   | tot_fwd_pkts                    |
| 5  | Dst IP                          | Dst IP                          | Destination Port                  | tot_bwd_pkts                    |
| 6  | Dst Port                        | Dst Port                        | Protocol                          | totlen_fwd_pkts                 |
| 7  | Protocol                        | Protocol                        | Timestamp                         | totlen_bwd_pkts                 |
| 8  | Timestamp                       | Timestamp                       | Flow Duration                     | fwd_pkt_len_max                 |
| 9  | Flow Duration                   | Flow Duration                   | Total Fwd Packets                 | fwd_pkt_len_min                 |
| 10 | Total Fwd Packet                | Total Fwd Packet                | Total Backward Packets            | fwd_pkt_len_mean                |
| 11 | Total Bwd Packets               | Total Bwd Packets               | Total Length of Fwd Packets       | fwd_pkt_len_std                 |
| 12 | Total Length of Fwd Packet      | Total Length of Fwd Packet      | Total Length of Bwd Packets       | bwd_pkt_len_max                 |
| 13 | Total Length of Bwd Packet      | Total Length of Bwd Packet      | Fwd Packet Length Max             | bwd_pkt_len_min                 |
| 14 | Fwd Packet Length Max           | Fwd Packet Length Max           | Fwd Packet Length Min             | bwd_pkt_len_mean                |
| 15 | Fwd Packet Length Min           | Fwd Packet Length Min           | Fwd Packet Length Mean            | bwd_pkt_len_std                 |
| 16 | Fwd Packet Length Mean          | Fwd Packet Length Mean          | Fwd Packet Length Std             | flow_byts_s                     |
| 17 | Fwd Packet Length Std           | Fwd Packet Length Std           | Bwd Packet Length Max             | flow_pkts_s                     |
| 18 | Bwd Packet Length Max           | Bwd Packet Length Max           | Bwd Packet Length Min             | flow_iat_mean                   |
| 19 | Bwd Packet Length Min           | Bwd Packet Length Min           | Bwd Packet Length Mean            | flow_iat_std                    |
| 20 | Bwd Packet Length Mean          | Bwd Packet Length Mean          | Bwd Packet Length Std             | flow_iat_max                    |
| 21 | Bwd Packet Length Std           | Bwd Packet Length Std           | Flow Bytes/s                      | flow_iat_min                    |
| 22 | Flow Bytes/s                    | Flow Bytes/s                    | Flow Packets/s                    | fwd_iat_tot                     |
| 23 | Flow Packets/s                  | Flow Packets/s                  | Flow IAT Mean                     | fwd_iat_mean                    |
| 24 | Flow IAT Mean                   | Flow IAT Mean                   | Flow IAT Std                      | fwd_iat_std                     |
| 25 | Flow IAT Std                    | Flow IAT Std                    | Flow IAT Max                      | fwd_iat_max                     |
| 26 | Flow IAT Max                    | Flow IAT Max                    | Flow IAT Min                      | fwd_iat_min                     |
| 27 | Flow IAT Min                    | Flow IAT Min                    | Fwd IAT Total                     | bwd_iat_tot                     |
| 28 | Fwd IAT Total                   | Fwd IAT Total                   | Fwd IAT Mean                      | bwd_iat_mean                    |
| 29 | Fwd IAT Mean                    | Fwd IAT Mean                    | Fwd IAT Std                       | bwd_iat_std                     |
| 30 | Fwd IAT Std                     | Fwd IAT Std                     | Fwd IAT Max                       | bwd_iat_max                     |
| 31 | Fwd IAT Max                     | Fwd IAT Max                     | Fwd IAT Min                       | bwd_iat_min                     |
| 32 | Fwd IAT Min                     | Fwd IAT Min                     | Bwd IAT Total                     | fwd_psh_flags                   |
| 33 | Bwd IAT Total                   | Bwd IAT Total                   | Bwd IAT Mean                      | fwd_urg_flags                   |
| 34 | Bwd IAT Mean                    | Bwd IAT Mean                    | Bwd IAT Std                       | fwd_header_len                  |
| 35 | Bwd IAT Std                     | Bwd IAT Std                     | Bwd IAT Max                       | bwd_header_len                  |
| 36 | Bwd IAT Max                     | Bwd IAT Max                     | Bwd IAT Min                       | fwd_pkts_s                      |
| 37 | Bwd IAT Min                     | Bwd IAT Min                     | Fwd PSH Flags                     | bwd_pkts_s                      |
| 38 | Fwd PSH Flags                   | Fwd PSH Flags                   | Bwd PSH Flags                     | pkt_len_min                     |
| 39 | Bwd PSH Flags                   | Bwd PSH Flags                   | Fwd URG Flags                     | pkt_len_max                     |
| 40 | Fwd URG Flags                   | Fwd URG Flags                   | Bwd URG Flags                     | pkt_len_mean                    |
| 41 | Bwd URG Flags                   | Bwd URG Flags                   | Fwd Header Length                 | pkt_len_std                     |
| 42 | Fwd RST Flags                   | Fwd RST Flags                   | Bwd Header Length                 | pkt_len_var                     |
| 43 | Bwd RST Flags                   | Bwd RST Flags                   | Fwd Packets/s                     | fin_flag_cnt                    |
| 44 | Fwd Header Length               | Fwd Header Length               | Bwd Packets/s                     | syn_flag_cnt                    |
| 45 | Bwd Header Length               | Bwd Header Length               | Min Packet Length                 | rst_flag_cnt                    |
| 46 | Fwd Packets/s                   | Fwd Packets/s                   | Max Packet Length                 | psh_flag_cnt                    |
| 47 | Bwd Packets/s                   | Bwd Packets/s                   | Packet Length Mean                | ack_flag_cnt                    |
| 48 | Min Packet Length               | Min Packet Length               | Packet Length Std                 | urg_flag_cnt                    |
| 49 | Max Packet Length               | Max Packet Length               | Packet Length Variance            | cwr_flag_count                  |
| 50 | Packet Length Mean              | Packet Length Mean              | FIN Flag Count                    | ece_flag_cnt                    |
| 51 | Packet Length Std               | Packet Length Std               | SYN Flag Count                    | down_up_ratio                   |
| 52 | Packet Length Variance          | Packet Length Variance          | RST Flag Count                    | pkt_size_avg                    |
| 53 | FIN Flag Count                  | FIN Flag Count                  | PSH Flag Count                    | fwd_seg_size_avg                |
| 54 | SYN Flag Count                  | SYN Flag Count                  | ACK Flag Count                    | bwd_seg_size_avg                |
| 55 | RST Flag Count                  | RST Flag Count                  | URG Flag Count                    | attack_type                     |
| 56 | Label                           | Label                           | Label                             | attack_number                    |




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


