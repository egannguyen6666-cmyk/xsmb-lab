# XS Lab: kết quả & thống kê XSMB, XSMN, XSMT (tự chạy trên GitHub, không cần Claude)

Trang kết quả xổ số và thống kê dữ liệu đã quay của XSMB, XSMN, XSMT. Bản này chạy miễn phí:
- **GitHub Pages** lưu trang web để mở trên điện thoại và máy tính.
- **GitHub Actions** tự lấy kết quả ngay sau mỗi giờ quay và cập nhật dữ liệu.

> Thông tin và kết quả xổ số trên XS Lab được chúng tôi cập nhật từ nguồn công khai và chỉ mang tính chất tham khảo. Vui lòng kiểm tra lại kết quả chính thức được công bố bởi các công ty xổ số kiến thiết.

XS Lab chỉ trình bày kết quả và thống kê của các kỳ đã quay, không đưa ra dự đoán. Từ 24/11/2026 đã bỏ phần danh sách cho kỳ tới và nhật ký khóa trước (các tệp `predictions*.json` cũ vẫn giữ nguyên trong kho, không còn được ghi thêm).

Các mục: Kết quả (kèm thống kê nhanh của kỳ), Trực tiếp, Dò vé (tối đa 17 số, mỗi số 2–6 chữ số), Thống kê, Vietlott (Keno, Mega 6/45, Power 6/55, Max 3D, Max 3D Pro), Thống kê dàn, Bản đồ số, Kiểm định, Mô phỏng, Về dữ liệu.

---

## Cài đặt (làm một lần, khoảng 10 phút)

### 1. Tạo tài khoản và kho chứa
1. Đăng ký tài khoản miễn phí tại https://github.com.
2. Bấm **+** (góc trên bên phải) → **New repository**.
3. Đặt tên, ví dụ `xsmb-lab`. Chọn **Public**, vì GitHub Pages miễn phí cần kho công khai. Bấm **Create repository**.

### 2. Tải các file lên
1. Giải nén file zip trên máy tính.
2. Trong kho vừa tạo, bấm **uploading an existing file** (hoặc **Add file → Upload files**).
3. Kéo **toàn bộ nội dung** thư mục `xsmb-lab` vào: `index.html`, `xsmb.csv`, `recent.json`, thư mục `tools`, `README.md`. Bấm **Commit changes**.
4. Thư mục `.github` là thư mục ẩn, nên trình duyệt có thể không kéo lên được. Nếu không thấy nó trong kho:
   - Bấm **Add file → Create new file**.
   - Gõ tên `.github/workflows/update.yml`.
   - Mở file `update.yml` trên máy bằng Notepad, chép toàn bộ nội dung, dán vào. Bấm **Commit changes**.

### 3. Cho phép tự động cập nhật
1. Vào **Settings → Actions → General**.
2. Ở mục **Workflow permissions**, chọn **Read and write permissions**. Bấm **Save**.

### 4. Bật trang web
1. Vào **Settings → Pages**.
2. Ở mục **Source**, chọn **Deploy from a branch**. Branch chọn **main**, thư mục **/ (root)**. Bấm **Save**.
3. Sau 1–2 phút, trang web có tại: `https://<tên-tài-khoản>.github.io/xsmb-lab/`

### 5. Chạy thử lần đầu
Vào tab **Actions** → **Cập nhật XSMB hằng ngày** → **Run workflow** → **Run workflow**. Đợi khoảng 1 phút, thấy dấu tích xanh là xong.

---

## Dùng trên điện thoại
- Mở link `https://<tên-tài-khoản>.github.io/xsmb-lab/` bằng Safari hoặc Chrome.
- **iPhone:** nút Chia sẻ → *Thêm vào MH chính*.
- **Android:** dấu ⋮ → *Thêm vào màn hình chính*.

---

## Miền Nam (XSMN)
- Chọn **Miền Nam** ở góc trên, rồi chọn đài. Mỗi đài là một chuỗi kỳ quay riêng (đa số đài quay 1 lần/tuần, TP.HCM 2 lần).
- Thống kê tính theo kỳ của đài: 10, 26, 52 kỳ (khoảng 2,5 tháng, 6 tháng, 1 năm). Mỗi đài có 18 giải nên xác suất một số về là 1 − 0,99¹⁸ ≈ 16,55%.
- Dữ liệu từ 2008, gộp và đối chiếu 2 bộ dữ liệu mở (tuanseo5t-alt/xosomn-xosomt và Hpbt/xsmn-thong-ke).
- Nhập tay XSMN khi nguồn chậm: tab Actions → Run workflow → điền ô mn_ngay, mn_dai (ví dụ tp-hcm) và mn_ket_qua (18 số theo thứ tự ĐB, G1, G2, G3×2, G4×7, G5, G6×3, G7, G8).

## Miền Trung (XSMT)
- Chọn **Miền Trung** ở góc trên rồi chọn đài (14 đài). Cách tính giống miền Nam (18 giải/đài, khung 10/26/52 kỳ).
- Dữ liệu từ 2009, bộ dữ liệu mở tuanseo5t-alt/xosomn-xosomt. Nhập tay: ô mt_ngay, mt_dai, mt_ket_qua trong Run workflow.

## Trực tiếp
- Mục **Trực tiếp** hiện bảng quay số của cả 3 miền (16:15 Nam, 17:15 Trung, 18:15 Bắc), vẽ lại theo giao diện XS Lab từ mã nhúng miễn phí của Xổ Số Minh Ngọc.
- Trang chỉ tải lại khoảng 5 giây một lần và chỉ trong khung giờ quay. Mục này hiện thêm thống kê nổi bật của kỳ đang quay (số về sau thời gian gan dài nhất, số nhiều nháy, tần suất các kỳ trước…).
- Quay xong, kết quả được đưa ngay vào tab Kết quả trên trình duyệt (nhãn "chờ đối chiếu"); máy chủ GitHub cũng tự đọc bảng kết quả công khai bằng `tools/fetch_minhngoc.py` và ghi vào dữ liệu.

## Lịch tự động
- Chạy lúc **16:40, 16:55** (sau XSMN), **17:40, 17:55** (sau XSMT), **18:40, 19:40 và 22:40** (sau XSMB) giờ Việt Nam. GitHub đôi khi chạy trễ 5–30 phút.
- Dữ liệu lấy từ 4 bộ dữ liệu mở trên GitHub, tự chọn bộ mới nhất. Các bộ này có hôm cập nhật chậm.
- Kỳ quay kế tiếp được tính tự động, bỏ qua kỳ nghỉ Tết (từ 30 Tết đến hết mùng 3). Lịch Tết đã có sẵn đến năm 2040.

## Khi nguồn tự động chậm: nhập tay từ điện thoại
1. Mở kho trên GitHub (trình duyệt hoặc app GitHub) → tab **Actions** → **Cập nhật XSMB hằng ngày** → **Run workflow**.
2. Ô **ngày**: ví dụ `2026-11-24`.
3. Ô **ket_qua**: 27 số theo thứ tự ĐB, G1, G2 (2 số), G3 (6), G4 (4), G5 (6), G6 (3), G7 (4), cách nhau bằng dấu cách. Ví dụ kỳ 23/11/2026:
   ```
   94495 61045 37123 28361 65151 37136 02163 34224 96461 90071 6889 2594 2250 0000 6926 4809 5179 1028 9121 4735 512 375 889 50 51 52 57
   ```
4. Bấm **Run workflow**. Script tự kiểm tra: đủ 27 số, đúng số chữ số, không trùng ngày, không rơi vào ngày nghỉ Tết. Sau đó ghi vào dữ liệu.

---

## Các file
| File | Nội dung |
| --- | --- |
| `index.html` | Ứng dụng (9 mục) |
| `xsmb.csv` | 2 số cuối 27 giải của mọi kỳ từ 2005 |
| `recent.json` | Đủ giải của 60 kỳ gần nhất (cho tờ kết quả) |
| `predictions*.json` | Nhật ký cũ (đến 24/11/2026), giữ nguyên, không còn dùng |
| `tools/update.py` | Tải và gộp dữ liệu |
| `tools/add_day.py` | Nhập tay một kỳ (có kiểm tra) |
| `core.js` | Bộ tính toán chung cho trang web và script |
| `xsmn.csv`, `recent_mn.json` | Dữ liệu và kết quả đủ giải 60 ngày của XSMN |
| `xsmt.csv`, `recent_mt.json` | Dữ liệu và kết quả đủ giải của XSMT |
| `tools/update_mn.py`, `tools/add_day_mn.py` | Tải/gộp dữ liệu XSMN hoặc XSMT, nhập tay một đài |
| `tools/fetch_minhngoc.py` | Lấy kết quả vừa quay từ bảng công khai Minh Ngọc (có kiểm tra) |
| `vietlott_*.csv`, `tools/update_vietlott.py` | Kết quả Vietlott Keno (6.000 kỳ gần nhất), Mega 6/45, Power 6/55, Max 3D, Max 3D Pro và script cập nhật (từ vietvudanh/vietlott-data) |
| `xsmb/`, `xsmn/`, `xsmt/`, `truc-tiep-xsmb/`, `truc-tiep-xsmn/`, `truc-tiep-xsmt/`, `xsmb-30-ngay/`, `xsmn-30-ngay/`, `xsmt-30-ngay/`, `truc-tiep/`, `do-ve/`, `thong-ke/`, `thong-ke-dan/`, `vietlott/`, `keno/`, `mega-645/`, `power-655/`, `max-3d/`, `max-3d-pro/`, `ve-du-lieu/` | Trang con cho công cụ tìm kiếm (tiêu đề, mô tả, đường dẫn riêng), tạo từ cùng mã nguồn |
| `robots.txt`, `sitemap.xml`, `rss.xml`, `tools/make_rss.py` | Cho công cụ tìm kiếm; nguồn RSS kết quả các kỳ gần nhất (tạo lại mỗi lần cập nhật) |
| `xsmb/<ngày>/`, `xsmn/<ngày>/`, `xsmt/<ngày>/`, `xsmn/<đài>/`, `xsmt/<đài>/`, `*/thu-2/`…`*/chu-nhat/`, `*/so-ket-qua/`, `tools/make_pages.py` | Trang tĩnh cho SEO: kết quả từng ngày (giữ vĩnh viễn, mỗi ngày thêm trang mới), từng đài, theo thứ, sổ kết quả; tạo lại sitemap.xml mỗi lần cập nhật |
| `xsmb_full.csv`, `xsmn_full.csv`, `xsmt_full.csv`, `tools/update_full.py` | Kết quả đủ giải toàn bộ lịch sử (cho 3 càng, 4 càng, giải nhất, giải tám) |
| `thong-ke/<bảng>/` | Trang thống kê tĩnh: lô gan, tần suất, đầu đuôi, giải đặc biệt, giải nhất, giải tám, 3 càng, 4 càng (tạo lại mỗi ngày) |
| `hoi-dap/`, `mien-tru-trach-nhiem/`, `chinh-sach-bao-mat/`, `cookies/`, `rss/` | Hỏi đáp, tuyên bố miễn trừ trách nhiệm, chính sách bảo mật, chính sách cookie, hướng dẫn RSS |
| `.github/workflows/update.yml` | Lịch chạy tự động |

Lưu ý: kho công khai thì ai có link cũng xem được trang. Mọi con số là thống kê dữ liệu đã quay; xác suất mỗi số về trong một kỳ XSMB luôn khoảng 23,77%.

---
Dữ liệu: XSMB từ [kina2711/vietnam-lottery-xsmb](https://github.com/kina2711/vietnam-lottery-xsmb) (giấy phép MIT) và các bộ tương tự; XSMN từ [tuanseo5t-alt/xosomn-xosomt](https://github.com/tuanseo5t-alt/xosomn-xosomt) và [Hpbt/xsmn-thong-ke](https://github.com/Hpbt/xsmn-thong-ke).
