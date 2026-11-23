# NFRLocator Dataset (NaturaLiSE 2013 Corpus): Raw Documents & Multi-Label FR/NFR/Not_Req Ground Truth

Thư mục này lưu trữ bộ dữ liệu **NFRLocator** *(Slankas & Williams, 2013 — Workshop NaturaLiSE, ICSE; GitHub: `https://github.com/RealsearchGroup/NFRLocator`)* gồm **11 tài liệu thực tế toàn văn** (`.txt` kèm bản gốc `.docx`/`.pdf`/`.doc`/`.xls`/`.xlsx`) và **11.084 câu** được gán nhãn đa nhãn (`functional` FR, **14 nhóm NFR**, `database design`, và `Not_Req`) theo đúng thứ tự xuất hiện trong tài liệu gốc.

**Dataset link**: https://github.com/RealsearchGroup/NFRLocator

> **Lưu ý quan trọng:** Dữ liệu trong thư mục này đã **loại bỏ 792 câu rời của PROMISE (`PromiseData/promisedataALL`)** khỏi tập tổng hợp `.arff` gốc của tác giả để đảm bảo 100% câu đều truy vết tuần tự về 11 tài liệu thô trong `raw/`.

---

## 1. Cấu trúc thư mục (`Directory Structure`)

```text
nfr_locator/
├── README.md                                          # Tài liệu mô tả cấu trúc, thống kê & hướng dẫn kiểm tra
├── raw/                                               # [INPUT RAW] 11 thư mục tài liệu thô gốc (.txt + .pdf/.docx/.doc/.xls/.xlsx)
│   ├── 01_iTrust_requirements/                        # iTrust SRS & Use Cases (prose_srs_ug)
│   ├── 02_OpenEMR_4.1_Users_Guide/                    # OpenEMR 4.1 User Guide (prose_srs_ug)
│   ├── 03_OpenEMR_4.1.1_Linux_Installation/           # OpenEMR Linux Installation Guide (prose_srs_ug)
│   ├── 04_CMS_DUA_R_0235/                             # CMS Data Use Agreement (prose_regulation_dua)
│   ├── 05_NC_DETECT_DUA/                              # NC DETECT Data Use Agreement (prose_regulation_dua)
│   ├── 06_HIPAA_Combined_Rule/                        # HIPAA Combined Rule (prose_regulation_dua)
│   ├── 07_eCFR_45_CFR_part_170/                       # eCFR 45 CFR Part 170 EHR Certification (prose_regulation_dua)
│   ├── 08_Meaningful_Use_2010/                        # Meaningful Use 2010 Rule (prose_regulation_dua)
│   ├── 09_CCHIT_2011_Ambulatory_EHR/                  # CCHIT 2011 Criteria (excel_rfp_criteria)
│   ├── 10_LA_County_EHR_RFP/                          # LA County EHR RFP (excel_rfp_criteria)
│   └── 11_CCHCS_EHR_RFP/                              # California CCHCS EHR RFP (excel_rfp_criteria)
└── ground_truth/                                      # [GROUND TRUTH] Nhãn chuẩn & file JSON gốc
    ├── NFRLocator_all_11_docs.csv                     # Toàn bộ 11.084 câu trên 11 tài liệu
    ├── NFRLocator_prose_8_docs.csv                    # 7.617 câu chỉ trên 8 tài liệu văn xuôi thô liên tục (đã tách 3 bảng Excel RFP/CCHIT)
    ├── NFRLocator_by_doc/                             # 11 file CSV tách riêng từng tài liệu để đối chiếu 1-1 với raw/
    └── parsed_json/                                   # 11 file "- parsed.json" nguyên bản từ GitHub
```

---

## 2. Thống kê tổng quan 11 tài liệu

| # | `doc_slug` | Thể loại (`doc_genre`) | Tổng câu | `Not_Req` | `FR` (only) | `NFR` (only) | `FR+NFR` | `DB_Only` | Câu có `USER` (`TRUE`) |
| :-: | :--- | :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | `01_iTrust_requirements` | `prose_srs_ug` | **1.165** | 376 | 242 | 42 | 492 | 13 | 406 |
| 2 | `02_OpenEMR_4.1_Users_Guide` | `prose_srs_ug` | **473** | 95 | 183 | 18 | 177 | 0 | 223 |
| 3 | `03_OpenEMR_4.1.1_Linux_Installation` | `prose_srs_ug` | **225** | 184 | 0 | 39 | 2 | 0 | 39 |
| 4 | `04_CMS_DUA_R_0235` | `prose_regulation_dua` | **140** | 108 | 1 | 30 | 1 | 0 | 27 |
| 5 | `05_NC_DETECT_DUA` | `prose_regulation_dua` | **62** | 42 | 0 | 20 | 0 | 0 | 19 |
| 6 | `06_HIPAA_Combined_Rule` | `prose_regulation_dua` | **2.642** | 2.018 | 267 | 306 | 50 | 1 | 158 |
| 7 | `07_eCFR_45_CFR_part_170` | `prose_regulation_dua` | **1.475** | 1.146 | 155 | 161 | 9 | 4 | 115 |
| 8 | `08_Meaningful_Use_2010` | `prose_regulation_dua` | **1.435** | 1.311 | 116 | 8 | 0 | 0 | 36 |
| — | **Cộng 8 tài liệu văn xuôi (`NFRLocator_prose_8_docs.csv`)** | — | **7.617** | **5.280** | **964** | **624** | **731** | **18** | **1.023** |
| 9 | `09_CCHIT_2011_Ambulatory_EHR` | `excel_rfp_criteria` | **306** | 7 | 206 | 69 | 22 | 2 | 116 |
| 10 | `10_LA_County_EHR_RFP` | `excel_rfp_criteria` | **1.268** | 380 | 601 | 248 | 38 | 1 | 394 |
| 11 | `11_CCHCS_EHR_RFP` | `excel_rfp_criteria` | **1.893** | 409 | 817 | 496 | 170 | 1 | 647 |
| **Σ** | **Tổng 11 tài liệu (`NFRLocator_all_11_docs.csv`)** | — | **11.084** | **6.076** | **2.588** | **1.437** | **961** | **22** | **2.180** |

---

## 3. Định dạng các cột trong CSV (`ground_truth/*.csv`)

* `doc_slug`: Mã định danh tài liệu (khớp 1-1 với thư mục trong `raw/` và file trong `NFRLocator_by_doc/`).
* `doc_id`: Giá trị `documentID` gốc trong JSON (lưu ý một số tài liệu dùng chuỗi `"unknown"`).
* `doc_genre`: Phân nhóm nguồn tài liệu:
  * `prose_srs_ug`: Văn xuôi SRS & User/Install Guide phần mềm (`iTrust`, `OpenEMR`).
  * `prose_regulation_dua`: Văn xuôi quy định pháp lý & thỏa thuận sử dụng dữ liệu (`HIPAA`, `eCFR`, `Meaningful Use`, `DUA`).
  * `excel_rfp_criteria`: Danh sách yêu cầu trích xuất từ file Excel RFP/CCHIT.
* `sentence_index`: Thứ tự câu tuần tự (`0..N-1`) từ đầu đến cuối văn bản thô `.txt` (khớp 99,50% theo thứ tự).
* `sentence`: Nội dung câu gốc.
* `req_or_not_req`: Nhãn Tầng 1 (`Req` / `Not_Req`).
* `fr_nfr_label`: Nhãn Tầng 2 tổng hợp (`FR`, `NFR`, `FR+NFR`, `DB_Only`, `Not_Req`).
* `is_functional`, `is_nfr`, `is_database_design`: Cờ nhị phân (`0`/`1`).
* `nfr_subcategories`: Danh sách các nhãn NFR con có giá trị `TRUE` (trong 14 lớp: `access control`, `audit`, `availability`, `capacity and performance`, `legal`, `look and feel`, `maintainability`, `operational`, `privacy`, `recoverability`, `reliability`, `security`, `usability`, `other nonfunctional`), phân cách bằng `;`.
* `has_user_verified_true`: `1` nếu có ít nhất 1 nhãn `TRUE` mang `source="USER"` (người gán nhãn bấm chọn trực tiếp trên GUI); `0` nếu nhãn `TRUE` chỉ giữ nguyên gợi ý `ML_INSTANCE` (hoặc `NOT_SET` ở HIPAA).
* `true_sources`: Tập các giá trị `source` của các nhãn `TRUE` (`USER`, `ML_INSTANCE`, `NOT_SET`).
* `comments`: Ghi chú hòa giải giữa các annotator (nếu có).

---

## 4. Lưu ý quan trọng khi review & sử dụng

1. **Cơ chế `USER` vs `ML_INSTANCE`:** Toàn bộ `11.084` câu đều có `trained = true` trong JSON gốc. Tuy nhiên, theo mã nguồn Java của `NFRLocator`, khi người gán nhãn đồng ý với dự đoán của bộ phân loại $k$-NN (`InstanceLearner`) mà không bấm sửa checkbox, `source` vẫn giữ nguyên là `ML_INSTANCE`. Chỉ khi người gán chủ động sửa mới đổi thành `USER`. Có thể dùng cột `has_user_verified_true = 1` để lọc tập con có độ tin cậy cao nhất hoặc rà soát lại các câu chỉ mang `ML_INSTANCE`.
2. **Giấy phép:** Repo gốc `RealsearchGroup/NFRLocator` chưa có file `LICENSE` tường minh (`README.md` gốc ghi chú *"need copyright status added for the various documents"*). Chỉ sử dụng cho mục đích nghiên cứu học thuật.
