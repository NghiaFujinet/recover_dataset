# Requirements Engineering & BRD Dataset Repository (`recover_dataset`)

Kho lưu trữ tổng hợp các bộ dữ liệu phục vụ bài toán **Trích xuất Yêu cầu Hệ thống & Phân loại `Req/Not_Req`, `FR/NFR` từ văn bản thô (BRD/SRS/Hội thoại)**.

---

## Tổng Quan & Phân Nhóm Dataset Theo Loại Ground Truth

| Nhóm Ground Truth | Dataset / Tập con | Thư mục / File chính | Đầu vào thô (`Raw Input`) | Ground Truth hiện có | Quy mô thực tế | Lưu ý QA quan trọng |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **1. Có nhãn `FR / NFR` riêng** | **`nfr_locator`** *(8 văn xuôi)* | `nfr_locator/` (`NFRLocator_prose_8_docs.csv`) | `8` tài liệu văn xuôi `.txt` + `.pdf/.docx/.doc` (`01`–`08`) | `Not_Req`, `FR`, `NFR`, `FR+NFR`, `DB_Only` + 14 nhóm NFR con | **7.617 câu** (`5.280 Not_Req`, `964 FR`, `624 NFR`, `731 FR+NFR`, `18 DB_Only`) | Đã loại 3 file Excel RFP (`09`–`11`). `1.023` câu `Req` có `has_user_verified_true = 1`. `parsed_json/` vẫn giữ 11 file JSON gốc. |
| **1. Có nhãn `FR / NFR` riêng** | **`recover`** *(End-to-End Delphi)* | `ground_truth/experts_final_requirements.csv` | `raw_conversation/example_conversation.txt` (`133` lượt lời) | `FR` / `NFR` | **28 câu** (`24 FR`, `4 NFR`) | Câu chuẩn hóa tổng hợp (không phải span nguyên văn); $N=1$ hội thoại. (`baselines/recover_requirements_FR_NFR.csv` là output LLM, không phải GT.) |
| **2. Chỉ có `Req / Not_Req`** *(chưa tách FR/NFR)* | **`pure`** | `pure/` (`PURE_valid.csv`, `PURE_test.csv`, `PURE_train.csv`) | `7` file SRS thô trong `pure/raw/` (`1` valid + `6` test) | `Req` / `Not_Req` | `valid` **905** + `test` **1.534** = **2.439 câu** có raw (`train` 5.306 câu & `RFIs` 380 câu chưa có raw) | Chưa có nhãn `FR/NFR`; 7 file raw là SRS kỹ thuật; `train` (23 docs) thiếu file raw. |
| **2. Chỉ có `Req / Not_Req`** *(chưa tách FR/NFR)* | **`recover`** *(Turn-level RQ1.1)* | `ground_truth/turn_level/RQ1.1_turn_classification_oracle.xlsx` | `raw_conversation/example_conversation.txt` (`133` lượt lời) | `Req` / `NonReq` (suy ra từ `prediction` + `manual check`) | **133 lượt lời** (`51 Req`, `82 NonReq`) | Map 100% về hội thoại gốc; chưa tách `FR/NFR`. |
| **3. Chỉ có `User Story`** *(không có FR/NFR)* | **`inter2us_extended`** | `inter2us_extended/` (`public_system_desc/`, `data_annotation/`) | `int1.txt` (kịch bản 430 từ; `data_annotation/` không có transcript gốc) | User Stories + nhãn căn chỉnh `Coverage`/`Score` & tên tính năng tự do | `62` US người / `115` US tổng (`int1`); `50` cặp IAA; `39` US kèm tên chức năng | Không có nhãn `FR/NFR` hay `Req/Not_Req`. Giấy phép `MIT`. |
| **3. Chỉ có `User Story`** *(không có FR/NFR)* | **`recover`** *(Task 5 — Inter2US)* | `ground_truth/user_stories/` | `raw_conversation/example_conversation.txt` | `37` User Stories + `180` cặp căn chỉnh (`Score` `0`/`1`) | `37` US, `180` cặp | Không có nhãn `FR/NFR`. |
| **4. Chỉ có `BRD / SRS thô`** *(Unlabeled)* | **`raw_brd_unlabeled`** | `raw_brd_unlabeled/` | `6` file PDF toàn văn (`Doc-1`, `Doc-2`, `Doc-4`, `Doc-5`, `Doc-6`, `Doc-7`) | **Không có** (`0` file nhãn) | **292 trang / 56.232 từ** | `Doc-6` (MDOT, 47 tr) và `Doc-7` (GCC-Stat, 168 tr) là BRD thực tế rất tốt để tự gán nhãn. |

### Chi tiết từng nhóm

1. **Nhóm 1 — Có nhãn `FR / NFR` riêng:**
   * **`nfr_locator/`** *(đã loại bỏ 3 file Excel RFP `09`, `10`, `11` khỏi `raw/` và `NFRLocator_by_doc/`) — Xem [nfr_locator/README.md](nfr_locator/README.md)*: Bộ dữ liệu chính có đầy đủ 2 tầng (`Req/Not_Req` và `FR/NFR/FR+NFR/DB_Only` + 14 nhóm NFR con) trên **8 tài liệu văn xuôi** (`NFRLocator_prose_8_docs.csv`, `7.617` câu: `3` SRS/User Guide + `5` văn bản pháp quy/DUA y tế). Lưu ý: thư mục `parsed_json/` vẫn còn giữ 11 file JSON gốc; chỉ `1.023` câu `Req` trên tập 8 doc có `has_user_verified_true = 1`.
   * **`recover` (`experts_final_requirements.csv`)**: `28` yêu cầu chuẩn hóa qua Delphi (`24 FR`, `4 NFR`) trên cuộc phỏng vấn IFA (`133` lượt lời).
2. **Nhóm 2 — Chỉ có nhãn `Req / Not_Req` (Requirement không thôi):**
   * **`pure/`** *(xem [pure/README.md](pure/README.md))*: Có `2.439` câu gán nhãn `Req/Not_Req` khớp trực tiếp với `7` tài liệu SRS thô trong `pure/raw/` (`PURE_valid.csv` `905` câu + `PURE_test.csv` `1.534` câu). Tập `PURE_train.csv` (`5.306` câu, 23 docs) và `Final_dataset_RFIs.csv` (`380` câu) hiện chưa kèm file raw.
   * **`recover` (`RQ1.1_turn_classification_oracle.xlsx`)**: `133` lượt lời hội thoại gán nhãn `Req` (`51`) / `NonReq` (`82`).
3. **Nhóm 3 — Chỉ có `User Story` (và căn chỉnh, không có `FR/NFR`):**
   * **`inter2us_extended/`** *(xem [inter2us_extended/README.md](inter2us_extended/README.md))*: Kịch bản mô tả hệ thống `int1.txt` (`430` từ) + `115` User Stories (`62` do người viết) + căn chỉnh `Coverage`/`Score`; kèm `data_annotation/` (`Inter_annotation_agreement_clean.csv` `50` cặp, `g01`, `g04`, `user_story_functionality_H.csv` `39` US kèm tên tính năng tự do).
   * **`recover` (`ground_truth/user_stories/`)**: `37` User Stories và `180` cặp căn chỉnh trên hội thoại IFA.
4. **Nhóm 4 — Chỉ có `BRD / SRS thô` (Unlabeled — không có ground truth):**
   * **`raw_brd_unlabeled/`** *(xem [raw_brd_unlabeled/README.md](raw_brd_unlabeled/README.md))*: `6` file PDF toàn văn (`292` trang, `56.232` từ), gồm 2 BRD doanh nghiệp/chính phủ thực tế (`Doc-6` Maryland DOT CPMS, `Doc-7` GCC-Stat MARSA) và 4 tài liệu SRS/BRD học thuật/mẫu (`Doc-1`, `Doc-2`, `Doc-4`, `Doc-5`). Không có file nhãn ground truth.

---

# RECOVER Dataset: Conversational Requirements Elicitation Benchmark

Bộ dữ liệu chuẩn (Benchmark Dataset) cho bài toán **Trích xuất Yêu cầu Hệ thống Tự động từ Hội thoại (Conversational Requirements Elicitation)**, được cấu trúc lại từ nghiên cứu **RECOVER** (*Requirements EliCitation frOm conVERsations*: *"RECOVER: Toward the Automatic Requirements Generation from Stakeholders’ Conversations"*).

* **Nguồn dữ liệu gốc 1 — RECOVER (Figshare)**: https://figshare.com/s/46661b70336a46d66ac8
* **Nguồn dữ liệu gốc 2 — Inter2US / User Stories (Zenodo)**: https://zenodo.org/records/20596692

---

## 1. Cấu trúc thư mục (`Directory Structure`)

```text
recover_dataset/
├── README.md                                           # Tài liệu tổng hợp & ánh xạ dữ liệu toàn repo
├── raw_conversation/                                   # [INPUT RAW] Dữ liệu hội thoại đầu vào
│   └── example_conversation.txt                        # Bản ghi cuộc phỏng vấn stakeholder (133 turns, ~40 phút)
├── ground_truth/                                       # [GROUND TRUTH / ORACLES] Nhãn chuẩn do chuyên gia tạo
│   ├── experts_final_requirements.txt                  # 28 câu requirements chuẩn (Delphi consensus) dạng plain text
│   ├── experts_final_requirements.csv                  # 28 câu requirements chuẩn kèm nhãn FR/NFR, nhóm & timestamp gốc
│   ├── experts_individual/                             # Kết quả trích xuất độc lập của 3 chuyên gia trước khi gộp
│   │   ├── expert_1_requirements.txt                   # 104 câu requirements của Chuyên gia 1 (mức chi tiết cao)
│   │   ├── expert_2_requirements.txt                   # 35 câu requirements của Chuyên gia 2 (mức trung bình)
│   │   ├── expert_3_requirements.txt                   # 17 câu requirements của Chuyên gia 3 (mức khái quát)
│   │   └── experts_delphi_execution.xlsx               # Bảng đối chiếu & gộp Delphi (Initial Set 40 câu -> Final Set 28 câu)
│   ├── turn_level/                                     # Ground truth ở cấp độ từng lượt lời (Turn-level Oracles)
│   │   ├── RQ1.1_turn_classification_oracle.xlsx       # Nhãn Req/NonReq & kiểm tra thủ công (tp/tn/fp/fn) cho 133 turns
│   │   └── RQ1.2_turn_requirements_oracle.xlsx         # 57 turns kèm 4 câu trả lời chuẩn (Answer 1..4) do 20 người viết
│   └── user_stories/                                   # [Inter2US] Ground truth dạng User Stories & Alignment trên cùng hội thoại
│       ├── user_stories.csv                            # 37 User Stories chuẩn ("As a..., I want..., so that...")
│       ├── chunks_turns_3s1.csv                        # Hội thoại cắt thành các chunk trượt 3 lượt lời (stride 1)
│       └── all_pairs_annotated.csv                     # Nhãn căn chỉnh cặp (User Story, Chunk Text) với Score 0/1
├── baselines/                                          # [BASELINES] Kết quả đầu ra của các mô hình trong bài báo RECOVER
│   ├── Step1-2_predicted_turns.txt                     # 62 lượt lời / cặp Q&A sau khi lọc qua Step 1 (SVC) & Step 2 (DialogTag)
│   ├── recover_requirements.txt                        # 135 câu requirements do RECOVER (Llama-2-7b) sinh ra ở Step 3
│   ├── recover_requirements_FR_NFR.csv                 # 135 câu của RECOVER kèm nhãn kiểm tra FR/NFR & Hallucination
│   ├── Step3_Results_Formatted.xlsx                    # File Excel gốc phân tích FR/NFR trên 135 câu của RECOVER
│   └── llm_only_requirements.txt                       # 31 câu requirements khi đưa thẳng toàn bộ hội thoại vào LLM
├── evaluation/                                         # [EVALUATION] Script đánh giá tự động
│   └── RQ2_results_evaluation.ipynb                    # Notebook tính điểm BLEU, ROUGE-1, METEOR giữa Output và Ground Truth
├── nfr_locator/                                        # [NHÓM 1: FR/NFR] 8 tài liệu văn xuôi thô + nhãn Req/FR/NFR/14 lớp NFR
├── pure/                                               # [NHÓM 2: Req/Not_Req] 7 SRS thô (valid+test) + PURE train/valid/test CSV
├── inter2us_extended/                                  # [NHÓM 3: User Story] Kịch bản int1.txt + User Stories + IAA alignment
└── raw_brd_unlabeled/                                  # [NHÓM 4: BRD Thô Unlabeled] 6 tài liệu BRD/SRS PDF toàn văn (chưa có nhãn)
```

---

## 2. Chi tiết Input Raw vs. Ground Truth theo từng bài toán

Tùy vào mục tiêu thực nghiệm, bạn chọn cặp **Input Raw $\rightarrow$ Ground Truth** tương ứng trong bảng dưới đây:

| Bài toán (Task) | Input Raw | Ground Truth (Oracle) | Baseline để so sánh |
| :--- | :--- | :--- | :--- |
| **Task 1: End-to-End Conversational RE**<br>*(Trích xuất danh sách requirements từ toàn bộ cuộc hội thoại)* | `raw_conversation/example_conversation.txt`<br>*(133 lượt lời có timestamp & speaker)* | `ground_truth/experts_final_requirements.txt`<br>hoặc `ground_truth/experts_final_requirements.csv`<br>*(28 requirements đồng thuận qua Delphi)* | • `baselines/recover_requirements.txt` (135 câu)<br>• `baselines/llm_only_requirements.txt` (31 câu) |
| **Task 2: Turn-Level Requirement Identification**<br>*(Phân loại lượt lời nào có chứa thông tin yêu cầu: `Req` vs `NonReq`)* | Cột `sentence` (133 turns) trong<br>`ground_truth/turn_level/RQ1.1_turn_classification_oracle.xlsx` | Suy ra từ cột `prediction` + `manual check`:<br>• **True `Req` (51 turns)**: `tp` (39) + `fn` (12)<br>• **True `NonReq` (82 turns)**: `tn` (59) + `fp` (23) | Cột `prediction` (`62 Req`, `71 NonReq`) của mô hình `FastText + SVC` |
| **Task 3: Turn-Level Requirement Generation**<br>*(Sinh câu requirement từ từng đoạn trích hội thoại)* | Cột `Turns` (57 đoạn trích) trong<br>`ground_truth/turn_level/RQ1.2_turn_requirements_oracle.xlsx` | Các cột `Answer 1`, `Answer 2`, `Answer 3`, `Answer 4` *(do 4 chuyên gia độc lập viết cho mỗi turn)* | Cột `LLM requirements` trong cùng file Excel |
| **Task 4: FR vs. NFR Classification & Groundedness**<br>*(Phân loại yêu cầu Chức năng `FR` và Phi chức năng `NFR`)* | • 28 câu chuẩn: `ground_truth/experts_final_requirements.csv`<br>• 135 câu máy sinh: `baselines/recover_requirements_FR_NFR.csv` | • Cột `label` (`24 FR`, `4 NFR`) trong `experts_final_requirements.csv`<br>• Cột `label` (`119 FR`, `16 NFR` — gồm `11` NFR có thật trong hội thoại & `5` NFR do LLM tự suy diễn) trong `recover_requirements_FR_NFR.csv` | Kết quả phân tích trong `baselines/Step3_Results_Formatted.xlsx` |
| **Task 5: User Story Elicitation & Alignment**<br>*(Trích xuất User Stories & căn chỉnh hội thoại — Inter2US)* | `raw_conversation/example_conversation.txt`<br>*(hoặc `ground_truth/user_stories/chunks_turns_3s1.csv`)* | • 37 User Stories: `ground_truth/user_stories/user_stories.csv`<br>• Nhãn căn chỉnh `(User Story, Chunk)`: `ground_truth/user_stories/all_pairs_annotated.csv` (`Score` = `0` / `1`) | — |

---

## 3. Mô tả Dữ liệu Đầu vào (`raw_conversation/example_conversation.txt`)

* **Bối cảnh nghiệp vụ**: Cuộc phỏng vấn thu thập yêu cầu cho hệ thống quản lý của **IFA (Football Association)** gồm 4 phân hệ chính:
  1. **Budgeting Portal** (`[0:00:00]` – `[0:04:22]`, `[0:08:31]` – `[0:09:23]`)
  2. **Reporting & Real-time Game Events Portal** (`[0:04:22]` – `[0:08:31]`, `[0:21:57]` – `[0:23:09]`)
  3. **Scheduling & Referee Allocation Portal** (`[0:09:23]` – `[0:17:04]`)
  4. **Fan Portal & Notifications** (`[0:17:04]` – `[0:21:56]`, `[0:23:13]` – `[0:25:19]`)
  5. **Non-Functional / Technical / Registration / Archives** (`[0:25:20]` – `[0:39:49]`)
* **Định dạng**: Mỗi lượt lời có cấu trúc `[H:MM:SS] spk_<id>: <nội dung>`, cách nhau 1 dòng trống:
  * `spk_0`, `spk_2`: Chuyên viên phân tích yêu cầu (Requirements Analysts / Interviewers).
  * `spk_1`: Đại diện khách hàng / Stakeholder của IFA.

---

## 4. Quy trình xây dựng Ground Truth (`ground_truth/`)

Bộ 28 câu trong `ground_truth/experts_final_requirements.txt` (và `.csv`) được tạo qua **Phương pháp Delphi 2 vòng**:
1. **Vòng 1 (Độc lập)**: 3 chuyên gia phần mềm đọc `example_conversation.txt` và trích xuất độc lập:
   * `expert_1_requirements.txt`: **104 câu** (tách nhỏ từng chi tiết theo thứ tự thời gian hội thoại).
   * `expert_2_requirements.txt`: **35 câu** (gom theo nhóm chức năng).
   * `expert_3_requirements.txt`: **17 câu** (tổng hợp mức cao).
2. **Vòng 2 (Đối chiếu & Đồng thuận trong `experts_delphi_execution.xlsx`)**:
   * Sheet `Initial Set` ánh xạ 40 yêu cầu ứng viên với số thứ tự câu của từng chuyên gia (`Expert 1`, `Expert 2`, `Expert 3`).
   * Sheet `Final Set` gộp các câu trùng lặp, sắp xếp lại theo luồng kiến trúc hệ thống (đưa nhóm *Registration* ở cuối cuộc gọi lên đầu) và chuẩn hóa theo mẫu câu IEEE (`"The system must..."`), chốt lại **28 câu Ground Truth**.

---

## 5. Bảng Truy vết (Traceability) 28 câu Ground Truth về Hội thoại Gốc

| ID | Requirement (`experts_final_requirements.csv`) | Nhãn | Phân hệ (`Category`) | Vị trí trong `example_conversation.txt` | Đối chiếu Delphi (`E1 / E2 / E3`) |
| :-: | :--- | :-: | :--- | :--- | :--- |
| **1** | The system must allow team managers or owners to submit valid documents for team registration, which the IFA can approve, enabling the management of team resources such as players, coaches, and stadiums. | `FR` | Registration & Team Management | `[0:36:30] spk_1` (Line 239) | E1: `97, 98` \| E2: `1` \| E3: `16` |
| **2** | The system must allow teams to register their own page on which to post team information, with customization options. | `FR` | Registration & Fan Portal | `[0:18:57] spk_0`, `[0:19:24] spk_1` (Lines 123–125) | E2: `4` |
| **3** | The system must allow general users to register to have an account on the platform, with clear registration steps. | `FR` | Registration & User Account | `[0:36:09] spk_1`, `[0:36:25] spk_0` (Lines 235–237) | E1: `100` \| E2: `2` \| E3: `11, 17` |
| **4** | The system must allow players to register their own page on which to post their information, ensuring privacy settings. | `FR` | Registration & Player Portal | `[0:18:28] spk_1`, `[0:18:57] spk_0`, `[0:31:26] spk_1` (Lines 117, 123, 193) | E1: `83, 84` \| E2: `5` \| E3: `11` |
| **5** | The system must have a budgeting portal to allow teams to manage income and expenses, important for financial transparency. | `FR` | Budgeting Portal | `[0:00:00] spk_0`, `[0:01:17] spk_1`, `[0:02:25] spk_1` (Lines 1–7) | E1: `3–8, 98` \| E2: `6, 7` \| E3: `1, 6` |
| **6** | The system must allow the IFA financial team to specify policies for spending money, including policy update notifications. | `FR` | Budgeting Policy | `[0:02:44] spk_1`, `[0:37:20] spk_1` (Lines 11, 243) | E1: `1, 2, 93` \| E2: `8` \| E3: `1` |
| **7** | The system must allow the IFA financial team to access the financial data of the teams securely, with audit trails. | `FR` | Budgeting Access & Audit | `[0:03:08] spk_2`, `[0:03:16] spk_1`, `[0:08:44] spk_1` (Lines 13–15, 59) | E1: `9–12, 32` \| E2: `9` \| E3: `1, 5, 6` |
| **8** | The system must allow the IFA to appoint and register referees, ensuring a secure verification process. | `FR` | Referee Management | `[0:37:20] spk_1`, `[0:38:46] spk_1` (Lines 243, 247) | E1: `91, 92, 101` \| E2: `3` \| E3: `17` |
| **9** | The system must allow referees to post events on a game in real-time, with a mobile interface. | `FR` | Game Event Reporting | `[0:05:04] spk_1` (Line 35) | E1: `22, 24, 88` \| E2: `10, 11` \| E3: `4` |
| **10** | The system must ensure that only referees can update game events to maintain data coherence and reliability. | `NFR` | Data Integrity & Reliability | `[0:05:04] spk_1`, `[0:22:16] spk_1` (Lines 35, 143) | E1: `23, 63` |
| **11** | The system must automatically schedule the games in a season according to predefined policies, including a conflict resolution mechanism. | `FR` | Match Scheduling | `[0:09:39] spk_1`, `[0:15:32] spk_1` (Lines 63, 93) | E1: `34–38, 94` \| E2: `15` \| E3: `7` |
| **12** | The system must allow the IFA representative to schedule and reschedule games, with an interface for scheduling and ensuring notifications for changes. | `FR` | Match Rescheduling | `[0:13:27] spk_1`, `[0:14:07] spk_1`, `[0:17:25] spk_1` (Lines 83–93, 113) | E1: `43–46, 52` \| E2: `16, 20` \| E3: `7` |
| **13** | The system must allow the IFA representative to define policies to guide the scheduling of games and the assignments of referees to games, ensuring fairness in assignments. | `FR` | Scheduling & Referee Policy | `[0:09:39] spk_1`, `[0:11:24] spk_1`, `[0:12:29] spk_1` (Lines 63, 67–71) | E1: `34, 39–42, 94, 95` \| E2: `17–19, 23, 24` \| E3: `7, 8` |
| **14** | The system must allow fans to register for notifications about their favorite players and teams, with customizable notification preferences. | `FR` | Fan Subscriptions | `[0:18:28] spk_1`, `[0:19:29] spk_0`, `[0:24:49] spk_1` (Lines 117, 127, 157) | E1: `50, 51, 54, 66` \| E2: `25, 26` \| E3: `11` |
| **15** | The system must send notifications to fans based on their registrations, ensuring timely delivery. | `FR` | Fan Notifications | `[0:17:25] spk_1`, `[0:20:08] spk_1`, `[0:23:42] spk_1` (Lines 113, 129, 153) | E1: `52, 53, 57, 67` \| E2: `27` \| E3: `9, 10` |
| **16** | The system must provide automatic notifications for users interested in specific match information, with user preferences management. | `FR` | Match Notifications | `[0:17:25] spk_1`, `[0:20:08] spk_1`, `[0:24:49] spk_1` (Lines 113, 129, 157) | E1: `50, 52, 57, 69` \| E2: `27, 30` \| E3: `9, 14` |
| **17** | The system must allow any user (also not registered to the platform) to see and download information about events posted, ensuring public access is read-only and including data export formats. | `FR` | Public Data Access & Export | `[0:06:35] spk_1`, `[0:07:12] spk_2`, `[0:07:20] spk_1` (Lines 43–47) | E1: `25, 26, 64` \| E2: `12–14` \| E3: `3` |
| **18** | The system must encrypt financial and budget data to comply with security standards and prevent data leakage. | `NFR` | Security & Encryption | `[0:30:14] spk_1` (Line 187) | E1: `82` \| E2: `36` |
| **19** | The system must maintain archives of past season schedules, ensuring they are searchable. | `FR` | Schedule Archives | `[0:37:03] spk_0`, `[0:37:20] spk_1` (Lines 241–243) | E1: `99` \| E2: `31` \| E3: `13` |
| **20** | The system must allow the IFA and teams to generate financial reports at specific intervals and on-demand, providing real-time data for ongoing monitoring. | `FR` | Financial Reporting | `[0:02:25] spk_1`, `[0:03:26] spk_1`, `[0:07:55] spk_1` (Lines 7, 19, 51) | E1: `13–19, 30` |
| **21** | The system must allow access to at least 50000 users, ensuring scalability. | `NFR` | Scalability & Capacity | `[0:25:20] spk_2`, `[0:25:37] spk_1` (Lines 159–161) | E1: `70` \| E2: `34` |
| **22** | The system must respond very fast (approximately 2 seconds) to all actors except referees, who should have immediate real-time updates during a game. | `NFR` | Performance & Latency | `[0:25:37] spk_1`, `[0:26:53] spk_1` (Lines 161, 165) | E1: `70–73` \| E2: `35` |
| **23** | The system must provide a web-based application for administrative and team use, ensuring cross-browser compatibility. | `FR` | Web Application Interface | `[0:20:56] spk_1` (Line 133) | E1: `60, 62` \| E2: `33` \| E3: `12` |
| **24** | The system must provide a mobile application for referees and fans, ensuring platform compatibility. | `FR` | Mobile Application Interface | `[0:20:56] spk_1` (Line 133) | E1: `61, 62` \| E2: `33` \| E3: `12` |
| **25** | The system must support live recording features for referees as a potential future enhancement. | `FR` | Live Recording (Future) | `[0:27:04] spk_0`, `[0:27:16] spk_1` (Lines 167–171) | E1: `75` |
| **26** | The system must allow the IFA administrator to set policies on notifications, with a policy management interface. | `FR` | Notification & Policy Reminders | `[0:24:21] spk_0`, `[0:24:49] spk_1` (Lines 155–157) | E1: `68, 94` \| E2: `29` \| E3: `10` |
| **27** | The system must allow the IFA to define leagues and seasons, with hierarchical management. | `FR` | League & Season Management | `[0:32:51] spk_1`, `[0:37:20] spk_1` (Lines 207, 243) | E1: `86, 89, 90` \| E2: `32` |
| **28** | The system must allow team managers to report new players joining or leaving the team, and the number of events and losses in tournaments. | `FR` | Team Roster & Tournament Report | `[0:07:23] spk_0`, `[0:38:46] spk_1` (Lines 49, 247) | E1: `27–29, 102` |

---

## 6. Kết quả Benchmark Baseline (RQ2 Evaluation)

Kết quả chạy từ `evaluation/RQ2_results_evaluation.ipynb` so sánh với Ground Truth (`experts_final_requirements.txt`):

| Phương pháp | Số câu sinh ra | BLEU | ROUGE-1 (%) | METEOR (%) |
| :--- | :---: | :---: | :---: | :---: |
| **LLM-Only Baseline** (`baselines/llm_only_requirements.txt`) | 31 | 49.36 | **43.96** | 35.34 |
| **RECOVER Pipeline** (`baselines/recover_requirements.txt`) | 135 | **78.82** | 37.20 | **39.10** |

---

## 7. Nguồn dữ liệu & Trích dẫn (`Source & Citation`)

* **RECOVER (System Requirements & Turn-level Oracles)**:
  * Bài báo: *RECOVER: Toward the Automatic Requirements Generation from Stakeholders’ Conversations*
  * Online Appendix (Figshare): https://figshare.com/s/46661b70336a46d66ac8
* **Inter2US (User Stories & Interview-to-Story Alignment)**:
  * Bài báo: *Automatic Alignment between Elicitation Interviews and Requirements*
  * Reproducibility Package (Zenodo): https://zenodo.org/records/20596692

