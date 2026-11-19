# PURE Dataset: Raw SRS Documents & Req/Not_Req Ground Truth

Thư mục này lưu trữ các tài liệu **Software Requirements Specification (SRS) thô** trích từ bộ **PURE (PUblic REquirements Dataset)** *(Ferrari, Spagnolo, & Gnesi, 2017 — Zenodo DOI: `10.5281/zenodo.1414117`)* cùng bộ **Ground Truth phân loại `Req` / `Not_Req`** (xác định câu yêu cầu vs. văn bản mô tả thường).

---

## 1. Cấu trúc thư mục (`Directory Structure`)

```text
pure/
├── README.md                                # Tài liệu mô tả cấu trúc & ánh xạ dữ liệu
├── raw/                                     # [INPUT RAW] Tài liệu SRS thô gốc (PDF / DOC)
│   ├── 2001 - hats.pdf                      # Raw SRS tương ứng với PURE_valid.csv
│   ├── 2000 - nasa x38.doc                  # Raw SRS tương ứng với PURE_test_nasa_x38.csv
│   ├── 2001 - ctc network.pdf               # Raw SRS tương ứng với PURE_test_ctc-network.csv
│   ├── 2007 - nlm.doc                       # Raw SRS tương ứng với PURE_test_nlm.csv
│   ├── 2009 - warc III.pdf                  # Raw SRS tương ứng với PURE_test_warc_III.csv
│   ├── 2010 - fishing.pdf                   # Raw SRS tương ứng với PURE_test_fishing.csv
│   └── 2010 - home 1.3.pdf                  # Raw SRS tương ứng với PURE_test_home_1.3.csv
└── ground_truth/                            # [GROUND TRUTH] Nhãn chuẩn Req / Not_Req
    ├── PURE_train.csv                       # Tập huấn luyện (23 tài liệu PURE, 5.306 dòng)
    ├── PURE_valid.csv                       # Tập validation (1 tài liệu: hats.pdf, 905 dòng)
    ├── PURE_test.csv                        # Tập test chuẩn (6 tài liệu PURE, 1.534 dòng)
    ├── Final_dataset_RFIs.csv               # [Ngoài miền] Tập RFI (Request for Information, 380 dòng)
    └── test_by_doc/                         # PURE_test.csv đã tách riêng theo từng tài liệu
        ├── PURE_test_ctc-network.csv        # 118 dòng (82 Req, 36 Not_Req)
        ├── PURE_test_fishing.csv            # 97 dòng (74 Req, 23 Not_Req)
        ├── PURE_test_home_1.3.csv           # 103 dòng (65 Req, 38 Not_Req)
        ├── PURE_test_nasa_x38.csv           # 620 dòng (538 Req, 82 Not_Req)
        ├── PURE_test_nlm.csv                # 447 dòng (243 Req, 204 Not_Req)
        └── PURE_test_warc_III.csv           # 149 dòng (56 Req, 93 Not_Req)
```

---

## 2. Thống kê tổng quan các file Ground Truth (`ground_truth/`)

Bộ Ground Truth thật của **PURE** gồm 3 tập tách theo cấp độ tài liệu (không trùng file SRS giữa train / valid / test):

| File | Nguồn | Số tài liệu | Tổng dòng | Nhãn `Req` | Nhãn `Not_Req` | Vai trò |
|---|---|---:|---:|---:|---:|---|
| `PURE_train.csv` | PURE | 23 | **5.306** | 2.832 | 2.474 | Tập huấn luyện |
| `PURE_valid.csv` | PURE (`hats.pdf`) | 1 | **905** | 255 | 650 | Tập validation |
| `PURE_test.csv` | PURE | 6 | **1.534** | 1.058 | 476 | **Tập đánh giá chính (Test)** |
| **Tổng cộng PURE** | **PURE** | **30** | **7.745** | **4.145** | **3.600** | **Đầy đủ toàn văn SRS** |
| `Final_dataset_RFIs.csv` | RFI *(không phải PURE)* | — | 380 | 266 (`yes`) | 114 (`no`) | Tập kiểm thử ngoài miền (Out-of-domain) |

### Định dạng cột (`PURE_*.csv`)
* Cột 1 *(trống tên)*: Chỉ số dòng gốc (`index`).
* `Requirement`: Câu hoặc đoạn văn bản trích xuất từ tài liệu SRS.
* `Name of Doc`: Tên tài liệu SRS nguồn (dùng để ánh xạ 1-1 về file trong `raw/`).
* `Req/Not Req`: Nhãn chuẩn (`Req` hoặc `Not_Req`).

---

## 3. Ánh xạ cặp `Raw SRS <-> Ground Truth` cho tập Test & Valid

Toàn bộ **6 tài liệu của `PURE_test.csv`** và **1 tài liệu của `PURE_valid.csv`** đều đã có đủ file raw gốc trong `raw/`. Kết quả đối chiếu trực tiếp nội dung file raw với các file CSV tách riêng trong `ground_truth/test_by_doc/`:

| Tập | `Name of Doc` | File Raw (`raw/`) | Định dạng / Kích thước | File Ground Truth tương ứng | Tổng dòng | `Req` | `Not_Req` | Tỷ lệ khớp nội dung |
|---|---|---|---|---|---:|---:|---:|---:|
| **Valid** | `hats.pdf` | `2001 - hats.pdf` | PDF (369,0 KB) | `ground_truth/PURE_valid.csv` | 905 | 255 | 650 | — |
| **Test** | `ctc-network.pdf` | `2001 - ctc network.pdf` | PDF, 32 trang (271,2 KB) | `test_by_doc/PURE_test_ctc-network.csv` | 118 | 82 | 36 | **100,0%** (118/118) |
| **Test** | `nasa x38.doc` | `2000 - nasa x38.doc` | DOC nhị phân (900,5 KB) | `test_by_doc/PURE_test_nasa_x38.csv` | 620 | 538 | 82 | **99,8%** (619/620) |
| **Test** | `home 1.3.pdf` | `2010 - home 1.3.pdf` | PDF, 15 trang (129,6 KB) | `test_by_doc/PURE_test_home_1.3.csv` | 103 | 65 | 38 | **94,2%** (97/103) |
| **Test** | `fishing.pdf` | `2010 - fishing.pdf` | PDF, 49 trang (417,9 KB) | `test_by_doc/PURE_test_fishing.csv` | 97 | 74 | 23 | **90,7%** (88/97) |
| **Test** | `nlm.doc` | `2007 - nlm.doc` | DOC nhị phân (3.396,5 KB) | `test_by_doc/PURE_test_nlm.csv` | 447 | 243 | 204 | **88,4%** (395/447) |
| **Test** | `warc III.pdf` | `2009 - warc III.pdf` | PDF, 10 trang (536,3 KB) | `test_by_doc/PURE_test_warc_III.csv` | 149 | 56 | 93 | **83,9%** (125/149) |

*(Tổng 6 file trong `test_by_doc/` = `1.534` dòng, khớp tuyệt đối với `PURE_test.csv`. Phần nhỏ chưa khớp chuỗi thô khi kiểm tra tự động là do ngắt dòng/bảng biểu hoặc ký tự đặc biệt trong PDF/DOC.)*

---

## 4. Lưu ý quan trọng khi sử dụng & Chất lượng nhãn

1. **Phạm vi bài toán (Tầng 1 vs. Tầng 2):**
   * Các file `PURE_*.csv` chỉ cung cấp Ground Truth cho **Tầng 1 — Requirement Identification (`Req` vs. `Not_Req`)**.
   * **Chưa có nhãn phân loại `FR` / `NFR`** (Tầng 2). Để chạy bài toán `Raw SRS -> FR / NFR`, sử dụng tập câu `Req` (ví dụ `1.058` câu trong `PURE_test.csv` hoặc `255` câu trong `PURE_valid.csv`) làm đầu vào sạch cho mô hình/pipeline phân loại `FR` vs. `NFR`.
2. **Độ sạch của nhãn `Req` / `Not_Req` trên `PURE_test.csv`:**
   * **0 xung đột nhãn** giữa các câu trùng lặp trên toàn bộ 1.534 dòng.
   * Gán nhãn theo ngữ nghĩa thực tế (không dựa máy móc vào từ khóa `shall`/`must`).
   * Tồn tại một tỷ lệ rất nhỏ câu biên (~1%, gồm 15 câu `Not_Req` có chứa `shall`/`must` tập trung ở `home 1.3.pdf` và `nlm.doc`) do nằm ở phần *Overall Description / User Characteristics* trong SRS gốc. Nên giữ nguyên nhãn gốc nếu cần so sánh chuẩn với các nghiên cứu trước.
