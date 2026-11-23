# XS Lab: kết quả & thống kê XSMB, XSMN (tự chạy trên GitHub, không cần Claude)

Ứng dụng học xác suất thống kê với dữ liệu Xổ số miền Bắc. Bản này chạy miễn phí:
- **GitHub Pages** lưu trang web để mở trên điện thoại và máy tính.
- **GitHub Actions** mỗi tối tự cập nhật kết quả, chấm điểm và khóa danh sách cho kỳ kế tiếp.

Nhật ký `predictions.json` chỉ được thêm dòng, không bao giờ bị xóa hay sửa.

---

## Cài đặt (làm một lần, khoảng 10 phút)

### 1. Tạo tài khoản và kho chứa
1. Đăng ký tài khoản miễn phí tại https://github.com.
2. Bấm **+** (góc trên bên phải) → **New repository**.
3. Đặt tên, ví dụ `xsmb-lab`. Chọn **Public**, vì GitHub Pages miễn phí cần kho công khai. Bấm **Create repository**.

### 2. Tải các file lên
1. Giải nén file zip trên máy tính.
2. Trong kho vừa tạo, bấm **uploading an existing file** (hoặc **Add file → Upload files**).
3. Kéo **toàn bộ nội dung** thư mục `xsmb-lab` vào: `index.html`, `xsmb.csv`, `recent.json`, `predictions.json`, thư mục `tools`, `README.md`. Bấm **Commit changes**.
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
- Chỉ báo tính theo kỳ của đài: 10, 26, 52 kỳ (khoảng 2,5 tháng, 6 tháng, 1 năm). Mỗi đài có 18 giải nên xác suất một số về là 1 − 0,99¹⁸ ≈ 16,55%.
- Dữ liệu từ 2008, gộp và đối chiếu 2 bộ dữ liệu mở (tuanseo5t-alt/xosomn-xosomt và Hpbt/xsmn-thong-ke).
- Nhập tay XSMN khi nguồn chậm: tab Actions → Run workflow → điền ô mn_ngay, mn_dai (ví dụ tp-hcm) và mn_ket_qua (18 số theo thứ tự ĐB, G1, G2, G3×2, G4×7, G5, G6×3, G7, G8).

## Lịch tự động
- Chạy lúc **16:50** (sau XSMN), **18:40, 19:40 và 22:40** (sau XSMB) giờ Việt Nam. GitHub đôi khi chạy trễ 5–30 phút.
- Dữ liệu lấy từ 4 bộ dữ liệu mở trên GitHub, tự chọn bộ mới nhất. Các bộ này có hôm cập nhật chậm.
- Kỳ quay kế tiếp được tính tự động, bỏ qua kỳ nghỉ Tết (từ 30 Tết đến hết mùng 3). Lịch Tết đã có sẵn đến năm 2040.

## Khi nguồn tự động chậm: nhập tay từ điện thoại
1. Mở kho trên GitHub (trình duyệt hoặc app GitHub) → tab **Actions** → **Cập nhật XSMB hằng ngày** → **Run workflow**.
2. Ô **ngày**: ví dụ `2026-11-24`.
3. Ô **ket_qua**: 27 số theo thứ tự ĐB, G1, G2 (2 số), G3 (6), G4 (4), G5 (6), G6 (3), G7 (4), cách nhau bằng dấu cách. Ví dụ kỳ 23/11/2026:
   ```
   94495 61045 37123 28361 65151 37136 02163 34224 96461 90071 6889 2594 2250 0000 6926 4809 5179 1028 9121 4735 512 375 889 50 51 52 57
   ```
4. Bấm **Run workflow**. Script tự kiểm tra: đủ 27 số, đúng số chữ số, không trùng ngày, không rơi vào ngày nghỉ Tết. Sau đó nó chấm điểm và khóa danh sách cho kỳ kế tiếp.

---

## Các file
| File | Nội dung |
| --- | --- |
| `index.html` | Ứng dụng (6 màn hình) |
| `xsmb.csv` | 2 số cuối 27 giải của mọi kỳ từ 2005 |
| `recent.json` | Đủ giải của 60 kỳ gần nhất (cho tờ kết quả) |
| `predictions.json` | Nhật ký danh sách khóa trước, chỉ thêm, không xóa |
| `tools/update.py` | Tải và gộp dữ liệu |
| `tools/add_day.py` | Nhập tay một kỳ (có kiểm tra) |
| `core.js` | Bộ tính toán chung cho trang web và script |
| `xsmn.csv`, `recent_mn.json`, `predictions_mn.json` | Dữ liệu, kết quả đủ giải 60 ngày và nhật ký khóa trước của XSMN |
| `tools/update_mn.py`, `tools/add_day_mn.py` | Tải/gộp dữ liệu XSMN, nhập tay một đài |
| `tools/predict.js` | Khóa danh sách (8 chỉ báo + Top 3) cho kỳ kế tiếp của XSMB và từng đài XSMN |
| `.github/workflows/update.yml` | Lịch chạy tự động |

Lưu ý: kho công khai thì ai có link cũng xem được trang. Đây là công cụ học thống kê; các danh sách số chỉ là xếp hạng theo dữ liệu quá khứ, xác suất mỗi số về trong ngày luôn khoảng 23,77%.

---
Dữ liệu: XSMB từ [kina2711/vietnam-lottery-xsmb](https://github.com/kina2711/vietnam-lottery-xsmb) (giấy phép MIT) và các bộ tương tự; XSMN từ [tuanseo5t-alt/xosomn-xosomt](https://github.com/tuanseo5t-alt/xosomn-xosomt) và [Hpbt/xsmn-thong-ke](https://github.com/Hpbt/xsmn-thong-ke).
