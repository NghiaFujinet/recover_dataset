# Inter2US Extended Dataset: Public System Description & IAA Annotations

Thư mục này bổ sung các phần dữ liệu công khai còn thiếu từ repository **`francdente/inter2us`** (*Automated Alignment between Elicitation Interviews and Requirements / Text2Stories*, Dente, Dalpiaz, & Papotti, `arXiv:2510.08622`, Zenodo `10.5281/zenodo.20596692`) chưa có trong `ground_truth/user_stories/`.

**Dataset link**: https://zenodo.org/records/20596692

* **Giấy phép:** `MIT License` (file `LICENSE` kèm theo từ `francdente/inter2us`).
* **Lưu ý:** File `int2.txt` trong cả `public_interview/` và `public_system_desc/` của repo gốc đều có kích thước `0 bytes` (rỗng), nên không tải về.

---

## 1. Cấu trúc thư mục (`Directory Structure`)

```text
inter2us_extended/
├── README.md                                              # Tài liệu mô tả cấu trúc & thống kê
├── LICENSE                                                # MIT License (Copyright 2025 Francesco Dente)
├── public_system_desc/                                    # Kịch bản BRD/Mô tả hệ thống Travel Agency ("Roteiros & Aventuras")
│   ├── int1.txt                                           # Văn bản mô tả nghiệp vụ gốc (51 dòng, 430 từ)
│   ├── user_stories.csv                                   # Toàn bộ 115 User Stories (gồm 62 Human + 53 LLM)
│   ├── user_stories_human_only.csv                        # [ĐÃ LỌC] 62 User Stories chỉ của 7 nhóm người (Group A..G)
│   ├── chunks_turns_3s1.csv                               # 37 dòng tách theo xuống dòng của int1.txt (file phụ)
│   ├── all_pairs_annotated.csv                            # Toàn bộ 580 cặp (User Story, Chunk) trên 23 câu/chunks
│   └── all_pairs_annotated_human_only.csv                 # [ĐÃ LỌC] 310 cặp căn chỉnh chỉ của 7 nhóm người (Group A..G)
└── data_annotation/                                       # Dữ liệu đánh giá đồng thuận & nhãn chức năng
    ├── README.md                                          # Ghi chú gốc của tác giả
    ├── Inter_annotation_agreement.csv                     # Bản gốc (52 dòng, có 2 dòng trống ở giữa)
    ├── Inter_annotation_agreement_clean.csv               # [ĐÃ LÀM SẠCH] Đúng 50 cặp (US, Chunk phỏng vấn thật g01/g04) từ 3 tác giả
    ├── g01_user_stories.csv                               # 53 User Stories dự án nha khoa PreDent (chỉ 2 dòng đầu có Chunk)
    ├── g04_user_stories.csv                               # 44 dòng (43 US duy nhất) dự án xếp ca/chat nhân viên (không có Chunk)
    └── user_story_functionality_H.csv                     # 39 User Stories kèm tên chức năng tự do (không phải nhãn FR/NFR)
```

---

## 2. Chi tiết dữ liệu trong `public_system_desc/`

1. **Văn bản đầu vào (`int1.txt`):** Mô tả kịch bản hệ thống *Travel Agency ("Roteiros & Aventuras")* gồm các mục `Context`, `Users`, `Actions`, `Functional Requirements` (430 từ).
2. **Ground Truth User Stories (`user_stories.csv` vs `user_stories_human_only.csv`):**
   * File gốc `user_stories.csv` chứa **115 User Stories**, nhưng đối chiếu cột `Group` trong `all_pairs_annotated.csv` cho thấy có **62 US do 7 nhóm người (`A–G`) viết** và **53 US do LLM (`GPT`, `Qwen3-0.6B/1.7B/4B/8B`) sinh ra**.
   * Dùng `user_stories_human_only.csv` (62 US) và `all_pairs_annotated_human_only.csv` (310 cặp) nếu bạn muốn benchmark thuần dữ liệu do con người viết.
3. **Chunking trong `all_pairs_annotated.csv`:**
   * 580 cặp gốc (và 310 cặp human-only) ánh xạ về **23 chunks** (`Chunk Index 0..22`) được tách từ `int1.txt` theo dấu chấm `.` (khác với file `chunks_turns_3s1.csv` 37 dòng tách theo xuống dòng).
   * Nhãn gồm `Coverage` (`Fully covered`: 161, `Partially covered`: 141, `Not covered`: 278 trên tổng 580 cặp) và `Score` (`1`: 302, `0`: 278).

---

## 3. Chi tiết dữ liệu trong `data_annotation/`

* **`Inter_annotation_agreement_clean.csv`:** Chứa **50 cặp `(User Story, Chunk Text)`** lấy từ **2 cuộc phỏng vấn thật** (`g01`: phòng khám nha khoa PreDent; `g04`: quản lý ca làm & chat nhân viên) được 3 tác giả (`Author 1`, `Author 2`, `Author 3`) chấm độc lập `0`/`1` (đồng thuận tuyệt đối 3/3 đạt `66,0%`, Fleiss' $\kappa = 0.4670$).
* **`user_story_functionality_H.csv`:** Cột `functionality` là **tên tính năng ngắn bằng văn bản tự do** (ví dụ `Manage events date`, `Upload Rider`), **không phải** nhãn phân loại `FR`/`NFR`.
