# Ground Truth Bộ Kiểm Thử Conflict & Nhiễu — RECOVER (`v1_thap`, `v2_vua`, `v3_cao`)

> [!WARNING]
> **KHÔNG ĐƯA THƯ MỤC NÀY VÀO PROMPT CỦA AGENT CẦN TEST.**  
> Toàn bộ thư mục `ground_truth/conflict_variants/` là **đáp án chấm điểm (Ground Truth)**. Khi đánh giá hệ thống BRD / Conflict Detector, chỉ truyền vào các file hội thoại thô trong `raw_conversation/`.

---

## 1. Ánh Xạ File Đầu Vào & Ground Truth Tương Ứng

| Biến thể | Hội thoại đầu vào (`raw_conversation/`) | GT 28 Requirements | GT Conflict & Decoy | Tổng lượt | Lỗi thật phải bắt | Decoy không được báo nhầm | Độ khó (`Dễ / TB / Khó`) | Trạng thái 28 GT (`GIU_NGUYEN / DOI_Y / CHUA_CHOT / LIEN_QUAN_XUNG_DOT`) |
| :--- | :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **`v1_thap`** | [example_conversation_conflict_v1_thap.txt](file:///Users/jakepham/Documents/SourceCode/research_brd_dataset/recover_dataset/raw_conversation/example_conversation_conflict_v1_thap.txt) | [v1_thap_requirements_gt.csv](file:///Users/jakepham/Documents/SourceCode/research_brd_dataset/recover_dataset/ground_truth/conflict_variants/v1_thap_requirements_gt.csv) | [v1_thap_conflicts_gt.csv](file:///Users/jakepham/Documents/SourceCode/research_brd_dataset/recover_dataset/ground_truth/conflict_variants/v1_thap_conflicts_gt.csv) | 142 (+9) | **6** | **3** | `2 / 3 / 1` | `22 / 1 / 0 / 5` |
| **`v2_vua`** | [example_conversation_conflict_v2_vua.txt](file:///Users/jakepham/Documents/SourceCode/research_brd_dataset/recover_dataset/raw_conversation/example_conversation_conflict_v2_vua.txt) | [v2_vua_requirements_gt.csv](file:///Users/jakepham/Documents/SourceCode/research_brd_dataset/recover_dataset/ground_truth/conflict_variants/v2_vua_requirements_gt.csv) | [v2_vua_conflicts_gt.csv](file:///Users/jakepham/Documents/SourceCode/research_brd_dataset/recover_dataset/ground_truth/conflict_variants/v2_vua_conflicts_gt.csv) | 148 (+15) | **11** | **4** | `3 / 5 / 3` | `14 / 1 / 1 / 12` |
| **`v3_cao`** | [example_conversation_conflict_v3_cao.txt](file:///Users/jakepham/Documents/SourceCode/research_brd_dataset/recover_dataset/raw_conversation/example_conversation_conflict_v3_cao.txt) | [v3_cao_requirements_gt.csv](file:///Users/jakepham/Documents/SourceCode/research_brd_dataset/recover_dataset/ground_truth/conflict_variants/v3_cao_requirements_gt.csv) | [v3_cao_conflicts_gt.csv](file:///Users/jakepham/Documents/SourceCode/research_brd_dataset/recover_dataset/ground_truth/conflict_variants/v3_cao_conflicts_gt.csv) | 155 (+22) | **17** *(đủ 16/16 mã)* | **6** | `4 / 8 / 5` | `11 / 2 / 1 / 14` |

* **Mâu thuẫn có sẵn trong bản gốc (`133` lượt):** Xem [preexisting_conflicts.csv](file:///Users/jakepham/Documents/SourceCode/research_brd_dataset/recover_dataset/ground_truth/conflict_variants/preexisting_conflicts.csv) (`PRE01`–`PRE10`), dùng để phân biệt khi chấm FP (lưu ý `PRE10` là nhiễu ASR, không miễn trừ cho FP ngữ nghĩa).
* **Quy ước mã lỗi:**
  * **Nhóm A (Mâu thuẫn trực tiếp):** `A1` số liệu NFR, `A2` hành vi FR, `A3` FR↔NFR, `A4` vai trò/quyền, `A5` đơn vị/định dạng.
  * **Nhóm B (Mâu thuẫn cấu trúc/ngầm):** `B1` ghép 3+ lượt, `B2` khoảng cách xa (`>= 30` lượt), `B3` thứ tự/thời gian quy trình, `B4` thuật ngữ nhập nhằng.
  * **Nhóm C (Chất lượng yêu cầu):** `C1` NFR mơ hồ không đo được, `C3` thiếu thông tin/module chưa định nghĩa, `C4` yêu cầu bất khả thi.
  * **Nhóm D (Động thái hội thoại):** `D1` rút lại/đổi ý (phải cập nhật GT theo ý mới nhất), `D2` bất đồng chưa chốt (`CHUA_CHOT`), `D3` chen ngang lạc đề, `D4` tham chiếu mơ hồ.
  * **Nhóm E (Decoy — bẫy nhất quán, KHÔNG được báo lỗi):** `E1` khác phạm vi/vai trò/giai đoạn, `E2` hai ngưỡng bổ sung hợp lệ, `E3` paraphrase xác nhận lại.

---

## 2. Bản 1 — `v1_thap` (Phải bắt `6` conflict, không báo nhầm `3` decoy)

### Các Conflict PHẢI BẮT ĐƯỢC (`6` mục)

| ID | Mã lỗi (`Chấp nhận`) | Vị trí (`Turn`, `Seq ID`, `Timestamp`) | Độ khó / Mức độ | Req bị ảnh hưởng & GT | Nội dung mâu thuẫn cần phát hiện |
| :--- | :---: | :--- | :---: | :---: | :--- |
| **`V1_E01`** | `D1` (`D1`) | `T066` (`S069`, `0:20:36`), `T067` (`S070`, `0:20:56`) → **`T104a`** (`S111`, `0:33:20`) | TB / Nghiêm trọng | `#15` (`DOI_Y`) | `spk_1` rút lại quyết định chỉ thông báo trong app (không email), yêu cầu gửi thêm email khi đổi lịch quan trọng. |
| **`V1_E02`** | `A1` (`A1`) | `T080` (`S083`, `0:25:20`), `T081` (`S084`, `0:25:37`) → **`T081a`** (`S085`, `0:26:10`) | Dễ / Nghiêm trọng | `#21` (`LIEN_QUAN_XUNG_DOT`) | Mâu thuẫn tải NFR: `50.000` concurrent users vs giới hạn cứng tối đa `10.000` users và bác bỏ `50.000`. |
| **`V1_E03`** | `A4` (`A4`) | `T030` (`S031`, `0:08:44`) → **`T030a`** (`S032`, `0:09:10`) | TB / Nghiêm trọng | `#5, #7` (`LIEN_QUAN_XUNG_DOT`) | Mâu thuẫn quyền: IFA chỉ xem giám sát sổ ngân sách đội vs IFA được sửa và ghi đè trực tiếp giao dịch. |
| **`V1_E04`** | `B2` (`B2/A4`) | `T018` (`S018`, `0:05:04`), `T072` (`S075`, `0:22:16`) → **`T115a`** (`S123`, `0:35:50`) | Khó / Nghiêm trọng | `#10` (`LIEN_QUAN_XUNG_DOT`) | Mâu thuẫn xa (`>= 43` lượt): chỉ trọng tài được cập nhật sự kiện trận đấu vs team manager sửa trực tiếp thẻ đỏ. |
| **`V1_E05`** | `C1` (`C1`) | **`T120a`** (`S129`, `0:36:50`) | TB / Nhẹ | `#1` (`LIEN_QUAN_XUNG_DOT`) | NFR mơ hồ không đo được (`"super fast"`, `"very intuitive"`, `"high availability"`) thiếu SLA định lượng. |
| **`V1_E06`** | `D3` (`D3`) | **`T055a`** (`S058`, `0:17:00`) | Dễ / Nhẹ | — (`GIU_NGUYEN`) | Chen ngang lạc đề hoàn toàn về lịch ăn trưa và lỗi Outlook cá nhân, không phải requirement. |

### Decoy KHÔNG ĐƯỢC BÁO NHẦM (`3` mục)
* **`V1_DEC_E1`** (`E1`, `T024a` / `S025` @ `0:07:21`): Phân biệt phạm vi export công khai (sự kiện trận đấu) vs bảo mật (ngân sách).
* **`V1_DEC_E2`** (`E2`, `T081b` / `S086` @ `0:26:22`): Hai ngưỡng độ trễ hợp lệ (`2s` ngày thường vs tối đa `4s` ngày cao điểm chung kết).
* **`V1_DEC_E3`** (`E3`, `T094a` / `S100` @ `0:30:40`): Paraphrase xác nhận lại yêu cầu mã hóa dữ liệu tài chính từ `T094`.

---

## 3. Bản 2 — `v2_vua` (Phải bắt `11` conflict, không báo nhầm `4` decoy)

### Các Conflict PHẢI BẮT ĐƯỢC (`11` mục)

| ID | Mã lỗi (`Chấp nhận`) | Vị trí (`Turn`, `Seq ID`, `Timestamp`) | Độ khó / Mức độ | Req bị ảnh hưởng & GT | Nội dung mâu thuẫn cần phát hiện |
| :--- | :---: | :--- | :---: | :---: | :--- |
| **`V2_E01`** | `D1` (`D1`) | `T086` (`S097`, `0:27:16`) → **`T086a`** (`S098`, `0:27:20`) | Dễ / TB | `#25` (`DOI_Y`) | Đổi ý live recording cho trọng tài từ bản tương lai (`future version`) sang bắt buộc có ngay ở `v1`. |
| **`V2_E02`** | `D2` (`D2`) | `T044` (`S048`, `0:14:07`), `T049` (`S053`, `0:15:50`) → **`T049a`** (`S054`, `0:16:00`) | Dễ / Nghiêm trọng | `#12` (`CHUA_CHOT`) | Bất đồng chưa chốt giữa hai đại diện IFA: yêu cầu người duyệt thứ 2 vs đòi 1 người tự duyệt đổi lịch khẩn cấp. |
| **`V2_E03`** | `D3` (`D3`) | **`T061a`** (`S067`, `0:18:52`) | TB / Nhẹ | — (`GIU_NGUYEN`) | Chen ngang lạc đề chuyện gõ cửa đặt phòng họp, không chứa requirement. |
| **`V2_E04`** | `D4` (`D4`) | **`T098a`** (`S111`, `0:31:46`) | Khó / TB | `#4` (`GIU_NGUYEN`) | Tham chiếu mơ hồ hàng loạt (`"that thing"`, `"them"`, `"that page"`, `"the ones from the other group"`). |
| **`V2_E05`** | `A1` (`A1`) | `T081` (`S090`, `0:25:37`) → **`T081a`** (`S091`, `0:26:12`) | Dễ / TB | `#22` (`LIEN_QUAN_XUNG_DOT`) | Mâu thuẫn độ trễ NFR: `~2` giây vs ngưỡng `15` giây và bác bỏ `2` giây. |
| **`V2_E06`** | `A2` (`A2`) | `T040` (`S043`, `0:13:20`), `T042` (`S045`, `0:13:27`) → **`T043a`** (`S047`, `0:14:05`) | TB / Nghiêm trọng | `#11, #13` (`LIEN_QUAN_XUNG_DOT`) | Mâu thuẫn hành vi FR: các đội không có quyền góp ý lịch & lịch cố định vs CLB giải hạng nhất được chọn và khóa slot cuối tuần trong hệ thống mới. |
| **`V2_E07`** | `A4` (`A4`) | `T099` (`S112`, `0:31:49`), `T100` (`S113`, `0:32:08`) → **`T100a`** (`S114`, `0:32:10`) | TB / Nghiêm trọng | `#4, #5` (`LIEN_QUAN_XUNG_DOT`) | Mâu thuẫn quyền: cấm cầu thủ vào budgeting portal xem lương vs cấp tab read-only xem lương và chi phí đội. |
| **`V2_E08`** | `B1` (`B1/A2`) | `T018` (`S019`, `0:05:04`), `T067` (`S073`, `0:20:56`) → **`T083a`** (`S094`, `0:26:58`) | Khó / Nghiêm trọng | `#9, #23, #24` (`LIEN_QUAN_XUNG_DOT`) | Mâu thuẫn ngầm ghép 3 lượt: trọng tài nhập real-time trên mobile app trong trận vs dùng desktop-only trên office PC, không cần điện thoại. |
| **`V2_E09`** | `B2` (`B2/A2`) | `T122` (`S137`, `0:37:20`), `T022` (`S023`, `0:06:35`) ↔ **`T074a`** (`S081`, `0:23:05`) | TB / Nghiêm trọng | `#19` (`LIEN_QUAN_XUNG_DOT`) | Mâu thuẫn xa (`48` lượt): tự động xóa sạch lịch và dữ liệu cũ sau `12` tháng vs giữ toàn bộ archive quá khứ (`T122`). |
| **`V2_E10`** | `C1` (`C1`) | **`T118a`** (`S133`, `0:36:18`) | TB / Nhẹ | `#3` (`LIEN_QUAN_XUNG_DOT`) | NFR mơ hồ không kiểm thử được (`"super seamless"`, `"modern"`, `"strong security"`, `"zero friction"`). |
| **`V2_E11`** | `C3` (`C3`) | **`T077a`** (`S085`, `0:24:05`) | Khó / TB | `#15, #16` (`LIEN_QUAN_XUNG_DOT`) | Thiếu thông tin: nhắc tới `"ticketing settlement module"` và `"stadium turnstile gateway"` chưa từng tồn tại/định nghĩa trong hội thoại. |

### Decoy KHÔNG ĐƯỢC BÁO NHẦM (`4` mục)
* **`V2_DEC_E1a`** (`E1`, `T036a` / `S039` @ `0:12:50`): Khác giai đoạn (trọng tài gửi ngày nghỉ trước bốc thăm vs sau khi phân công chỉ IFA đổi).
* **`V2_DEC_E1b`** (`E1`, `T024a` / `S026` @ `0:07:21`): Khác phạm vi dữ liệu (export thống kê trận đấu công khai vs ngân sách nội bộ).
* **`V2_DEC_E2`** (`E2`, `T080a` / `S089` @ `0:25:30`): Hai ngưỡng tải hợp lệ (`50.000` tối thiểu khi ra mắt vs `80.000` mục tiêu mở rộng ngày derby).
* **`V2_DEC_E3`** (`E3`, `T012a` / `S013` @ `0:03:50`): Paraphrase tóm tắt đúng mô hình ngân sách từ `T004` và `T011`.

---

## 4. Bản 3 — `v3_cao` (Phải bắt `17` conflict phủ đủ 16/16 mã, không báo nhầm `6` decoy)

### Các Conflict PHẢI BẮT ĐƯỢC (`17` mục)

| ID | Mã lỗi (`Chấp nhận`) | Vị trí (`Turn`, `Seq ID`, `Timestamp`) | Độ khó / Mức độ | Req bị ảnh hưởng & GT | Nội dung mâu thuẫn cần phát hiện |
| :--- | :---: | :--- | :---: | :---: | :--- |
| **`V3_E01`** | `D1` (`D1`) | `T066` (`S077`, `0:20:36`), `T067` (`S078`, `0:20:56`) → **`T079a`** (`S094`, `0:25:05`) | TB / Nghiêm trọng | `#15` (`DOI_Y`) | Rút lại lập trường không dùng email, bổ sung bắt buộc gửi email khi đổi lịch hoặc vi phạm ngân sách. |
| **`V3_E02`** | `D1` (`D1`) | `T120` (`S141`, `0:36:30`) → **`T120a`** (`S142`, `0:36:52`) | Dễ / Nghiêm trọng | `#1` (`DOI_Y`) | Đổi ý bỏ bước chờ IFA duyệt đăng ký đội, cho kích hoạt ngay khi tải tài liệu. |
| **`V3_E03`** | `D2` (`D2`) | `T022` (`S024`, `0:06:35`), `T023` (`S025`, `0:07:12`) → **`T024a`** (`S027`, `0:07:21`) | Dễ / Nghiêm trọng | `#17` (`CHUA_CHOT`) | Bất đồng chưa chốt: khách vãng lai được tải dữ liệu trận đấu vs hai đại diện CLB phản đối chỉ cho nhà báo trả phí export. |
| **`V3_E04`** | `D3` (`D3`) | **`T050a`** (`S058`, `0:16:14`) | TB / Nhẹ | — (`GIU_NGUYEN`) | Chen ngang chuyện phiếm trận Champions League (có từ bẫy `"referee"` nhưng không phải requirement). |
| **`V3_E05`** | `D4` (`D4`) | **`T065a`** (`S076`, `0:20:22`) | Khó / TB | `#14, #16` (`GIU_NGUYEN`) | Tham chiếu mơ hồ (`"that part over there"`, `"the previous one"`, `"they"`, `"the other side"`). |
| **`V3_E06`** | `A1` (`A1`) | `T080` (`S095`, `0:25:20`), `T081` (`S096`, `0:25:37`) → **`T081a`** (`S097`, `0:26:15`) | Dễ / Nghiêm trọng | `#21, #22` (`LIEN_QUAN_XUNG_DOT`) | Mâu thuẫn số liệu NFR kép: `50.000` users & `2s` vs mục tiêu `5.000` users & `10s`. |
| **`V3_E07`** | `A2` (`A2`) | `T040` (`S045`, `0:13:20`), `T042` (`S047`, `0:13:27`) → **`T042a`** (`S048`, `0:13:45`) | TB / Nghiêm trọng | `#12` (`LIEN_QUAN_XUNG_DOT`) | Mâu thuẫn hành vi FR: lịch đã chốt không đổi trừ bất khả kháng do IFA chỉnh vs team manager tự do dời lịch sân nhà trước 24h. |
| **`V3_E08`** | `A3` (`A3`) | `T094` (`S113`, `0:30:14`), `T022` (`S024`, `0:06:35`) → **`T094a`** (`S114`, `0:30:35`) | TB / Nghiêm trọng | `#18, #20` (`LIEN_QUAN_XUNG_DOT`) | Mâu thuẫn FR↔NFR: bắt buộc mã hóa & bảo mật ngân sách vs xuất công khai plain unencrypted CSV lên fan portal. |
| **`V3_E09`** | `A4` (`A4`) | `T014` (`S015`, `0:04:11`), `T030` (`S033`, `0:08:44`) → **`T014a`** (`S016`, `0:04:16`) | Dễ / Nghiêm trọng | `#5, #7` (`LIEN_QUAN_XUNG_DOT`) | Mâu thuẫn quyền: chỉ IFA và các đội vào budgeting portal vs fan mua vé mùa được xem và biểu quyết giao dịch chi tiêu. |
| **`V3_E10`** | `A5` (`A5`) | `T092` (`S110`, `0:29:00`) → **`T092a`** (`S111`, `0:29:35`) | TB / TB | `#5` (`LIEN_QUAN_XUNG_DOT`) | Mâu thuẫn đơn vị/định dạng: đa tiền tệ (`currency` localization) vs chỉ lưu/hiển thị duy nhất US Dollars không chuyển đổi. |
| **`V3_E11`** | `B1` (`B1/A2`) | `T018` (`S020`, `0:05:04`), `T067` (`S078`, `0:20:56`), `T081` (`S096`, `0:25:37`) → **`T085a`** (`S103`, `0:27:15`) | Khó / Nghiêm trọng | `#9, #22, #24` (`LIEN_QUAN_XUNG_DOT`) | Mâu thuẫn ngầm ghép 3 lượt: trọng tài nhập real-time trên điện thoại trong trận vs cấm dùng điện thoại, bắt nhập sau trận trên desktop. |
| **`V3_E12`** | `B2` (`B2/A4`) | `T034` (`S038`, `0:11:24`), `T124` (`S146`, `0:38:46`) ↔ **`T075a`** (`S089`, `0:23:11`) | TB / Nghiêm trọng | `#8, #13` (`LIEN_QUAN_XUNG_DOT`) | Mâu thuẫn xa (`>= 41` lượt cả hai đầu): IFA bổ nhiệm & phân công theo policy vs trọng tài tự đăng ký và tự chọn trận. |
| **`V3_E13`** | `B3` (`B3`) | `T104` (`S124`, `0:32:51`) → **`T105a`** (`S126`, `0:33:50`) | Khó / TB | `#27` (`LIEN_QUAN_XUNG_DOT`) | Mâu thuẫn thứ tự quy trình: đảo ngược đưa module real-time trọng tài (Phase 3) lên chạy trước đăng ký đội & tạo giải/mùa (Phase 1). |
| **`V3_E14`** | `B4` (`B4`) | `T032` (`S035`, `0:09:39`), `T004` (`S004`, `0:02:25`) → **`T032a`** (`S036`, `0:10:40`) | Khó / TB | `#11, #13` (`LIEN_QUAN_XUNG_DOT`) | Mâu thuẫn thuật ngữ ngầm: dùng từ `"team"` chỉ tổ trọng tài (1 chính 2 biên) trùng tên CLB, và đổi `"IFA"` thành `"league board"`. |
| **`V3_E15`** | `C1` (`C1`) | **`T074a`** (`S087`, `0:23:05`) | TB / Nhẹ | `#23, #24` (`LIEN_QUAN_XUNG_DOT`) | NFR mơ hồ không đo được (`"super snappy"`, `"modern"`, `"very user friendly"`, `"optimal throughput"`). |
| **`V3_E16`** | `C3` (`C3`) | **`T083a`** (`S100`, `0:26:58`) *(LOI_CHONG)* | Khó / TB | `#9, #22` (`LIEN_QUAN_XUNG_DOT`) | Lỗi chồng (`C3`): tham chiếu module `"var telemetry hub"` chưa từng được nhắc/định nghĩa trong dự án. |
| **`V3_E17`** | `C4` (`C4`) | **`T083a`** (`S100`, `0:26:58`) *(LOI_CHONG)* | TB / Nghiêm trọng | `#22` (`LIEN_QUAN_XUNG_DOT`) | Lỗi chồng (`C4`): yêu cầu bất khả thi về vật lý/kỹ thuật (`"100 percent uptime"` và `"zero millisecond latency worldwide"`). |

### Decoy KHÔNG ĐƯỢC BÁO NHẦM (`6` mục)
* **`V3_DEC_E1a`** (`E1`, `T059a` / `S069` @ `0:18:35`): Khác vai trò/trang (cầu thủ đăng trang cá nhân vs team manager đăng thông báo trang CLB).
* **`V3_DEC_E1b`** (`E1`, `T036a` / `S041` @ `0:12:50`): Khác giai đoạn phân công trọng tài (gửi ngày nghỉ trước vs IFA chốt lịch).
* **`V3_DEC_E2a`** (`E2`, `T054a` / `S063` @ `0:16:50`): Hai ngưỡng nghỉ hợp lệ (`2` ngày tối thiểu vs `5–7` ngày mục tiêu).
* **`V3_DEC_E2b`** (`E2`, `T010a` / `S011` @ `0:03:32`): Trạng thái hiện tại (báo cáo thủ công 1 lần/năm) vs hệ thống mới (kiểm tra báo cáo trực tiếp theo yêu cầu, khớp Req `#20`).
* **`V3_DEC_E3a`** (`E3`, `T044a` / `S051` @ `0:14:30`): Paraphrase xác nhận cơ chế giải trình & duyệt chéo từ `T044`/`T049`.
* **`V3_DEC_E3b`** (`E3`, `T069a` / `S081` @ `0:21:45`): Khẳng định lại kiến trúc một hệ thống backend thống nhất của `T069`.

---

## 5. Script Kiểm Tra Toàn Vẹn & Chấm Điểm Tự Động

Chạy trực tiếp bằng script độc lập [eval_conflicts.py](file:///Users/jakepham/Documents/SourceCode/research_brd_dataset/recover_dataset/evaluation/eval_conflicts.py):

```bash
# 1. Kiểm tra tính toàn vẹn của 3 bản conversation & các file GT CSV
python3 recover_dataset/evaluation/eval_conflicts.py --check

# 2. Chấm điểm đầu ra của agent/model (1 file JSON hoặc thư mục chứa v1_thap.json, v2_vua.json, v3_cao.json)
python3 recover_dataset/evaluation/eval_conflicts.py --pred path/to/preds/ --out eval_report.json
```

* **Định dạng file JSON đầu vào (`--pred`):**
  ```json
  {
    "bien_the": "v1_thap",
    "findings": [
      {
        "loai": "D1",
        "vi_tri": ["0:20:36", "0:20:56", "0:33:20"],
        "mo_ta": "spk_1 đổi ý yêu cầu gửi thêm email khi đổi lịch quan trọng",
        "do_tin_cay": 0.95
      }
    ]
  }
  ```
* `vi_tri` hỗ trợ tự động cả 3 kiểu: **timestamp** từ file `.txt` (`"[0:33:20]"` hoặc `"0:33:20"`), **ID tuần tự mù** (`"S111"`), hoặc **ID chuẩn** (`"T104a"`).
* Script bắt buộc có lượt chèn mới để tính TP, hỗ trợ `acceptable_loai` (ví dụ `B2`/`A4`), quét `decoy_trips` trên mọi dự đoán (kể cả TP), và chỉ miễn trừ `PRE01`–`PRE09` (bỏ `PRE10`).
