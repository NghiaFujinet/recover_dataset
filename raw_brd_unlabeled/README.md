# Raw BRD / SRS Documents (Unlabeled) — `naushadnizarali/brd-srs-documents`

Thư mục này lưu trữ **6 tài liệu BRD và SRS thô (PDF toàn văn)** tải từ Hugging Face Dataset [`naushadnizarali/brd-srs-documents`](https://huggingface.co/datasets/naushadnizarali/brd-srs-documents).

> **Lưu ý quan trọng:**
> 1. Các tài liệu này **KHÔNG có nhãn ground truth (`FR`/`NFR` hay `Req`/`Not_Req`)** đi kèm — chỉ phù hợp làm tập văn bản BRD thô đầu vào (Unlabeled / Case Study / Tự gán nhãn).
> 2. File `Doc-3.pdf` (*Amazing Lunch Indicator SRS*) đã được **bỏ qua không tải về** vì trang 1 chứa danh sách họ tên kèm mã số định danh cá nhân (PII dạng `YYMMDD-XXXX`).

---

## Danh sách 6 tài liệu trong thư mục

| Tên file | Nguồn gốc | Loại tài liệu | Số trang | Dung lượng | Ghi chú kiểm tra thực tế |
| :--- | :--- | :--- | ---: | ---: | :--- |
| `Doc-1_CS310_Web_Publishing_Annotated_SRS.pdf` | `Doc-1.pdf` | SRS giảng dạy (`CS 310`, *Web Publishing System*, 2004) | 30 | 273.654 B | Đọc text sạch, có chú thích sư phạm `<<Annotated Version>>` |
| `Doc-2_Amazon_Fresh_BRD.pdf` | `Doc-2.pdf` | BRD (*Amazon Fresh*, v0.01, 2017) | 14 | 240.975 B | Trang 1 bị lỗi font/mojibake tiêu đề; trang 3 trở đi đọc sạch |
| `Doc-4_IRAP_Credit_Scoring_Smart_Contract_BRD.pdf` | `Doc-4.pdf` | BRD (*IRAP Credit Scoring App*, Phase 2.0) | 21 | 767.126 B | Đọc text sạch, có cấu trúc In-Scope / Out-of-Scope |
| `Doc-5_STAMPS-R-US_BRD.pdf` | `Doc-5.pdf` | BRD bài tập (*IS 623 — STAMPS-R-US*) | 12 | 964.932 B | Có 1 trang ảnh/rỗng (`<20` ký tự); các trang còn lại đọc sạch |
| `Doc-6_Maryland_DOT_CPMS_BRD.pdf` | `Doc-6.pdf` | **BRD thực tế** (*Maryland DOT — Capital Program Management System*, 2014) | 47 | 1.098.484 B | Tài liệu BRD cơ quan nhà nước Mỹ thật, đọc text sạch |
| `Doc-7_StatStart_GCC-Stat_BRD.pdf` | `Doc-7.pdf` | **BRD thực tế** (*StatStart — GCC-Stat's Strategies*, 2019) | 168 | 10.372.167 B | Tài liệu BRD doanh nghiệp quy mô lớn (168 trang), đọc text sạch |
