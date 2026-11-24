# XS Lab: kết quả và thống kê xổ số (https://xslab.live)

Trang kết quả XSMB, XSMN, XSMT, Vietlott và thống kê dữ liệu đã quay. Không quảng cáo, không dự đoán. Trang tự chạy miễn phí, không cần Claude:

- **GitHub Pages** đưa trang lên mạng (tên miền xslab.live, khai báo trong tệp `CNAME`).
- **GitHub Actions** tự lấy kết quả sau mỗi giờ quay, rồi tạo lại các trang, sơ đồ trang web và RSS.
- **Cloudflare** (gói miễn phí) giữ bản lưu sẵn để trang nhanh và chịu tải. Bot tự xoá bản lưu sẵn sau mỗi lần cập nhật.

> Thông tin và kết quả xổ số trên XS Lab được chúng tôi cập nhật từ nguồn công khai và chỉ mang tính chất tham khảo.

Mọi số liệu là thống kê của các kỳ đã quay. Từ 24/11/2026 trang không còn phần gợi ý số; các tệp `predictions*.json` chỉ là nhật ký cũ, giữ nguyên.

---

## Lịch tự động

| Tệp | Chạy lúc (giờ Việt Nam) | Việc làm |
| --- | --- | --- |
| `.github/workflows/main.yml` | 16:36, 16:42, 16:55 (XSMN) · 17:36, 17:42, 17:55 (XSMT) · 18:34, 18:38, 18:45, 19:40, 22:40 (XSMB) | Lấy kết quả 3 miền và Vietlott, tạo lại trang, sơ đồ trang web, RSS, rồi xoá bản lưu sẵn Cloudflare |
| `.github/workflows/keno.yml` | 15 phút một lần, 6:00–22:59 | Lấy kết quả Keno |

GitHub đôi khi chạy trễ 5–15 phút. Muốn chạy ngay: tab **Actions** → chọn bot → **Run workflow**.

Kiểm tra định kỳ: vào tab **Actions**, các lần chạy gần đây phải có dấu ✓ xanh. Nếu nhiều lần liên tiếp có dấu ✗ đỏ thì nguồn dữ liệu có thể đã đổi định dạng, cần sửa script trong `tools/`.

## Khi nguồn tự động chậm: nhập tay

Tab **Actions** → **Cập nhật xổ số hằng ngày** → **Run workflow**, rồi điền:

- **XSMB:** ô `ngay` (ví dụ `2026-11-24`) và ô `ket_qua`. Ô `ket_qua` gồm 27 số theo thứ tự ĐB, G1, G2 (2 số), G3 (6), G4 (4), G5 (6), G6 (3), G7 (4), cách nhau bằng dấu cách.
- **XSMN:** ô `mn_ngay`, `mn_dai` (ví dụ `tp-hcm`) và `mn_ket_qua` (18 số theo thứ tự ĐB, G1, G2, G3 (2), G4 (7), G5, G6 (3), G7, G8).
- **XSMT:** ô `mt_ngay`, `mt_dai`, `mt_ket_qua`, cùng cách như XSMN.

Script tự kiểm tra đủ số giải, đúng số chữ số, không trùng ngày, không rơi vào nghỉ Tết.

## Khoá và tài khoản

| Ở đâu | Dùng để |
| --- | --- |
| GitHub → Settings → Secrets and variables → Actions: `CF_API_TOKEN`, `CF_ZONE_ID` | Bot xoá bản lưu sẵn Cloudflare. Khoá chỉ có quyền Cache Purge cho xslab.live. Thay khoá: Cloudflare → My Profile → API Tokens → Roll, rồi dán vào `CF_API_TOKEN`. Nếu khoá hỏng, web vẫn chạy, kết quả chỉ chậm khoảng 10 phút. |
| Namecheap | Tên miền xslab.live. Nên bật tự động gia hạn. |
| Cloudflare → Email Routing | Hộp thư lienhe@xslab.live chuyển tiếp về Gmail. |
| Google Search Console | Theo dõi index. Sơ đồ trang web: `https://xslab.live/sitemap.xml`. |

## Trực tiếp

Trang trực tiếp lấy số ngay trên trình duyệt người xem, từ nguồn quay trực tiếp công khai của Minh Ngọc, khoảng 3 giây một lần trong giờ quay (16:15 Nam, 17:15 Trung, 18:15 Bắc). Nếu nguồn đó lỗi, trang tự chuyển sang bảng kết quả công khai của Minh Ngọc. Quay xong, kết quả hiện ngay ở mục Kết quả và Dò vé với nhãn "chờ đối chiếu", cho tới khi bot lưu bản chính thức.

---

## Các tệp

| Tệp | Nội dung |
| --- | --- |
| `index.html` và các thư mục `xsmb/`, `truc-tiep/`, `do-ve/`, `thong-ke*/`, `vietlott/`, `keno/`… | Ứng dụng chính. Mỗi thư mục là một mục, có tiêu đề và nội dung riêng cho Google |
| `xsmb/<ngày>/`, `xsmn/<ngày>/`, `*/thang-MM-YYYY/`, `*/so-ket-qua/`, `<game>/ky-NNNNN/`, `so/NN/`, `thong-ke/<bảng>/` | Trang tĩnh theo ngày, tháng, kỳ Vietlott, từng số 00–99 và các bảng thống kê (tạo bởi `tools/make_pages.py`) |
| `xsmb.csv`, `xsmn.csv`, `xsmt.csv` | 2 số cuối các giải, toàn bộ lịch sử (XSMB từ 2005) |
| `xsmb_full.csv`, `xsmn_full.csv`, `xsmt_full.csv` | Kết quả đủ giải toàn bộ lịch sử |
| `recent*.json` | Kết quả đủ giải các kỳ gần nhất, cho bảng kết quả |
| `vietlott_*.csv` | Keno, Mega 6/45, Power 6/55, Max 3D, Max 3D Pro |
| `predictions*.json` | Nhật ký cũ, giữ nguyên, không còn dùng |
| `sitemap.xml` → `sitemap-chinh.xml`, `sitemap-xsmb.xml`, `sitemap-xsmn.xml`, `sitemap-xsmt.xml`, `sitemap-vietlott.xml` | Sơ đồ trang web cho Google |
| `rss.xml`, `robots.txt`, `llms.txt`, `404.html` | RSS, hướng dẫn cho máy tìm kiếm, giới thiệu cho AI, trang không tìm thấy |
| `assets/` | CSS, biểu tượng và JS dùng chung cho các trang tĩnh |
| `tools/update.py`, `tools/update_mn.py`, `tools/update_full.py`, `tools/update_vietlott.py` | Tải và gộp dữ liệu từ các nguồn mở |
| `tools/fetch_minhngoc.py`, `tools/fetch_keno.py` | Lấy kết quả vừa quay và Keno (có kiểm tra) |
| `tools/add_day.py`, `tools/add_day_mn.py` | Nhập tay một kỳ |
| `tools/make_pages.py`, `tools/shell.py`, `tools/make_rss.py` | Tạo trang tĩnh, khung chung (menu, chân trang), RSS |

Dữ liệu lịch sử: XSMB từ [kina2711/vietnam-lottery-xsmb](https://github.com/kina2711/vietnam-lottery-xsmb) (giấy phép MIT) và các bộ tương tự; XSMN, XSMT từ tuanseo5t-alt/xosomn-xosomt và Hpbt/xsmn-thong-ke. Vietlott từ vietvudanh/vietlott-data. Kết quả vừa quay lấy từ bảng công khai của Minh Ngọc.
