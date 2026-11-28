# Loạt bài pháp lý về xổ số (trang tĩnh). Gọi từ make_pages.py: law_pages.build(page, card, tbl, esc)
# Nội dung tổng hợp từ văn bản pháp luật; mỗi bài ghi rõ căn cứ, ngày cập nhật và lưu ý "không phải tư vấn pháp lý".
UPD = "28/11/2026"
UPD_ISO = "2026-11-28"
NOTE = ("<p class='note'>Bài viết tổng hợp thông tin từ văn bản pháp luật để bạn đọc tham khảo, không phải tư vấn pháp lý. "
        "Với trường hợp cụ thể, hãy hỏi luật sư hoặc cơ quan có thẩm quyền. Cập nhật " + UPD + ".</p>")

ARTS = []  # (slug, nav title, title, desc, h1, body_html, faq[(q,a)], related_slugs)


def _faq_html(faq, esc):
    return "<h2>Câu hỏi thường gặp</h2>" + "".join(f"<h3>{esc(q)}</h3><p>{esc(a)}</p>" for q, a in faq)


def _basis(items):
    return "<h2>Căn cứ pháp lý</h2><ul>" + "".join(f"<li>{x}</li>" for x in items) + "</ul>"


def articles():
    A = []
    # 1. Bài trụ
    A.append(dict(
        slug="soi-cau-co-vi-pham-phap-luat-khong", nav="Soi cầu có vi phạm pháp luật không?",
        title="Soi cầu có vi phạm pháp luật không? Mức phạt theo Nghị định 389/2026",
        desc="Soi cầu, dự đoán xổ số có phạm pháp không? Từ 30/11/2026, cung cấp thông tin dự đoán trước kết quả xổ số bị phạt 80–100 triệu đồng. Xem thống kê kỳ đã quay khác gì dự đoán.",
        h1="Soi cầu có vi phạm pháp luật không?",
        body=(
            "<p><b>Trả lời ngắn:</b> đưa ra con số cho kỳ xổ số <b>chưa quay</b> (\"soi cầu hôm nay\", \"dự đoán XSMB ngày mai\", \"chốt số\") là hành vi <b>cung cấp thông tin dự đoán trước kết quả xổ số</b>. Hành vi này bị pháp luật cấm. "
            "Từ ngày <b>30/11/2026</b>, theo Nghị định 389/2026/NĐ-CP, cá nhân vi phạm bị phạt tiền từ <b>80 đến 100 triệu đồng</b> và phải nộp lại số lợi bất hợp pháp thu được.</p>"
            "<p>Ngược lại, xem và thống kê <b>kết quả đã quay</b> (bảng kết quả, lô gan, tần suất, đối chiếu cầu với kết quả đã công bố) là thông tin quá khứ, không phải dự đoán.</p>"
            "<h2>Quy định cấm dự đoán kết quả xổ số</h2>"
            "<p>Việc cấm cung cấp thông tin dự đoán trước kết quả xổ số đã có từ nhiều năm trước (Nghị định 78/2012/NĐ-CP sửa đổi quy định về kinh doanh xổ số). Mức phạt trước đây nằm trong Nghị định 98/2013/NĐ-CP.</p>"
            "<p>Ngày 14/10/2026, Chính phủ ban hành <b>Nghị định 389/2026/NĐ-CP</b> về xử phạt vi phạm hành chính trong lĩnh vực kinh doanh xổ số, có hiệu lực từ <b>30/11/2026</b>, thay thế phần quy định về xổ số trong Nghị định 98/2013. "
            "Khoản 2 Điều 18 của Nghị định này quy định phạt tiền từ 80.000.000 đồng đến 100.000.000 đồng đối với hành vi cung cấp thông tin dự đoán trước kết quả xổ số. Mức phạt này áp dụng cho cá nhân; người vi phạm còn bị buộc nộp lại số lợi bất hợp pháp có được.</p>"
            "<h2>Thế nào là \"dự đoán trước kết quả xổ số\"?</h2>"
            "<p>Văn bản không liệt kê từng hình thức. Theo cách hiểu thông thường, bất kỳ con số nào được đưa ra <b>cho một kỳ quay chưa diễn ra</b>, dưới tên gọi gì, đều có thể bị coi là dự đoán:</p>"
            "<ul><li>\"Soi cầu XSMB hôm nay\", \"cầu bạch thủ ngày mai\", \"song thủ lô\", \"lô xiên hôm nay\" kèm con số cụ thể.</li>"
            "<li>\"Dự đoán XSMB\", \"chốt số\", \"số đẹp hôm nay\", \"giờ vàng chốt số\", \"nuôi lô khung\".</li>"
            "<li>Bán hoặc cho \"số VIP\", nhóm kín chia sẻ số qua Zalo, Telegram, Facebook.</li>"
            "<li>Video, livestream đọc số cho kỳ sắp quay.</li></ul>"
            "<p>Ghi chú \"chỉ mang tính tham khảo\" ở cuối trang không làm thay đổi bản chất: thứ được đánh giá là con số đưa ra trước kỳ quay.</p>"
            "<h2>Thống kê kết quả đã quay khác gì dự đoán?</h2>"
            "<table><tr><th>Thống kê (thông tin quá khứ)</th><th>Dự đoán (bị cấm)</th></tr>"
            "<tr><td>Bảng kết quả các kỳ đã quay</td><td>Con số \"nên đánh\" cho kỳ tới</td></tr>"
            "<tr><td>Lô gan, tần suất, đầu đuôi tính đến kỳ gần nhất</td><td>\"Lô gan sắp về\", \"đánh lô gan hôm nay\"</td></tr>"
            "<tr><td>Cầu đã chạy và kết quả đối chiếu: cầu kỳ 26/11 ra 92, kỳ 27/11 số 92 về 1 nháy</td><td>\"Cầu hôm nay: 12–21\" cho kỳ chưa quay</td></tr>"
            "<tr><td>Tỉ lệ trúng thực tế của một cách chọn số trên 30, 90, 365 kỳ</td><td>\"Chính xác 100%\", \"cầu VIP\"</td></tr></table>"
            "<p>Thống kê kết quả đã quay giúp người đọc thấy một sự thật: các cách soi cầu phổ biến trúng ngang mức chọn ngẫu nhiên, vì mỗi kỳ quay độc lập với kỳ trước. "
            "Xem kiểm chứng đầy đủ tại <a href=\"../../thong-ke/kiem-chung-du-doan-xsmb/\">Dự đoán XSMB có chính xác không?</a></p>"
            "<h2>Chia sẻ số trên Facebook, Zalo, TikTok có bị phạt không?</h2>"
            "<p>Quy định phạt áp dụng cho <b>hành vi cung cấp thông tin dự đoán</b>, không phân biệt kênh. Đăng bài, bình luận, livestream hay nhắn nhóm đưa ra con số cho kỳ chưa quay đều có thể bị coi là cung cấp thông tin dự đoán trước kết quả xổ số. "
            "Nếu việc chia sẻ số gắn với thu tiền (bán số, nhóm VIP) thì người vi phạm còn bị buộc nộp lại số lợi bất hợp pháp. Nếu liên quan đến ghi lô đề thì có thể bị xử lý về đánh bạc hoặc tổ chức đánh bạc, xem <a href=\"../choi-lo-de-co-bi-phat-khong/\">Chơi lô đề có bị phạt không?</a></p>"
            "<h2>XS Lab xử lý chuyện này thế nào?</h2>"
            "<p>Các trang <a href=\"../../soi-cau/\">soi cầu trên XS Lab</a> chỉ thống kê các kỳ <b>đã quay</b>: cầu ghép từ kết quả trước đó và kết quả đối chiếu với kỳ đã công bố, kèm tỉ lệ trúng thực tế. "
            "Trang không đưa bất kỳ con số nào cho kỳ chưa quay, không bán số, không có nhóm VIP, không quảng cáo nhà cái.</p>"),
        faq=[("Soi cầu có phạm pháp không?", "Đưa ra con số cho kỳ xổ số chưa quay là cung cấp thông tin dự đoán trước kết quả xổ số, bị cấm. Từ 30/11/2026, cá nhân vi phạm bị phạt 80–100 triệu đồng theo khoản 2 Điều 18 Nghị định 389/2026/NĐ-CP. Thống kê kết quả đã quay không phải dự đoán."),
             ("Dự đoán xổ số bị phạt bao nhiêu tiền?", "Từ 30/11/2026, cá nhân cung cấp thông tin dự đoán trước kết quả xổ số bị phạt từ 80 đến 100 triệu đồng và buộc nộp lại số lợi bất hợp pháp."),
             ("Xem thống kê lô gan, tần suất có vi phạm không?", "Thống kê kết quả các kỳ đã quay là thông tin quá khứ. Điều bị cấm là đưa ra con số cho kỳ chưa quay, ví dụ khuyên đánh lô gan ở kỳ tới."),
             ("Nghị định 389/2026 có hiệu lực khi nào?", "Nghị định 389/2026/NĐ-CP ban hành ngày 14/10/2026, có hiệu lực từ ngày 30/11/2026."),
             ("Ghi \"chỉ mang tính tham khảo\" có tránh được phạt không?", "Không chắc. Thứ được đánh giá là việc đưa ra con số cho kỳ chưa quay, không phải dòng ghi chú.")],
        basis=["Nghị định 389/2026/NĐ-CP ngày 14/10/2026 quy định xử phạt vi phạm hành chính trong lĩnh vực kinh doanh xổ số (khoản 2 và điểm b khoản 5 Điều 18; Điều 3; Điều 30), hiệu lực từ 30/11/2026.",
               "Nghị định 78/2012/NĐ-CP sửa đổi, bổ sung Nghị định 30/2007/NĐ-CP về kinh doanh xổ số (hành vi bị nghiêm cấm).",
               "Nghị định 98/2013/NĐ-CP (phần xổ số được thay thế từ 30/11/2026)."],
        rel=["du-doan-xo-so-bi-phat-bao-nhieu", "nghi-dinh-389-2026-xu-phat-xo-so", "choi-lo-de-co-bi-phat-khong", "mua-ve-so-duoi-18-tuoi"]))
    # 2. Dự đoán bị phạt bao nhiêu
    A.append(dict(
        slug="du-doan-xo-so-bi-phat-bao-nhieu", nav="Dự đoán xổ số bị phạt bao nhiêu?",
        title="Dự đoán xổ số bị phạt bao nhiêu tiền từ 30/11/2026?",
        desc="Cung cấp thông tin dự đoán trước kết quả xổ số bị phạt 80–100 triệu đồng với cá nhân từ 30/11/2026 (Nghị định 389/2026), buộc nộp lại số lợi bất hợp pháp. Ai bị phạt, áp dụng với website, mạng xã hội ra sao.",
        h1="Dự đoán xổ số bị phạt bao nhiêu tiền?",
        body=(
            "<p>Từ ngày <b>30/11/2026</b>, hành vi <b>cung cấp thông tin dự đoán trước kết quả xổ số</b> bị phạt tiền <b>từ 80 triệu đến 100 triệu đồng</b> đối với cá nhân, theo khoản 2 Điều 18 Nghị định 389/2026/NĐ-CP.</p>"
            "<table><tr><th>Nội dung</th><th>Quy định</th></tr>"
            "<tr><td>Hành vi</td><td>Cung cấp thông tin dự đoán trước kết quả xổ số</td></tr>"
            "<tr><td>Mức phạt cá nhân</td><td>80.000.000 – 100.000.000 đồng</td></tr>"
            "<tr><td>Tổ chức</td><td>Nghị định quy định mức phạt cá nhân bằng 1/2 mức phạt tổ chức cho cùng hành vi; mức tối đa với tổ chức trong lĩnh vực xổ số là 200 triệu đồng</td></tr>"
            "<tr><td>Biện pháp khắc phục</td><td>Buộc nộp lại số lợi bất hợp pháp có được</td></tr>"
            "<tr><td>Hiệu lực</td><td>Từ 30/11/2026</td></tr></table>"
            "<h2>Những ai có thể bị phạt?</h2>"
            "<p>Quy định nhắm vào <b>người cung cấp</b> thông tin dự đoán, không phân biệt hình thức: chủ website soi cầu, người đăng bài hoặc livestream trên mạng xã hội, người bán \"số VIP\", quản trị nhóm chat chia sẻ số cho kỳ chưa quay. "
            "Người chỉ đọc hoặc xem không phải là người cung cấp.</p>"
            "<h2>Website ghi \"chỉ tham khảo\" có bị phạt không?</h2>"
            "<p>Văn bản không có ngoại lệ cho dòng ghi chú miễn trừ. Nếu trang đưa ra con số cụ thể cho kỳ chưa quay, dòng \"chỉ mang tính tham khảo\" không thay đổi việc đó là thông tin dự đoán trước kết quả.</p>"
            "<h2>Thông tin nào không phải dự đoán?</h2>"
            "<ul><li>Kết quả xổ số đã công bố, sổ kết quả các kỳ.</li><li>Thống kê lô gan, tần suất, đầu đuôi tính đến kỳ đã quay.</li>"
            "<li>Đối chiếu một cách chọn số với kết quả thật của các kỳ đã quay.</li><li>Giải thích xác suất, vì sao mỗi kỳ quay độc lập.</li></ul>"
            "<p>Xem thêm: <a href=\"../soi-cau-co-vi-pham-phap-luat-khong/\">Soi cầu có vi phạm pháp luật không?</a></p>"),
        faq=[("Dự đoán xổ số bị phạt bao nhiêu?", "Cá nhân bị phạt từ 80 đến 100 triệu đồng và buộc nộp lại số lợi bất hợp pháp, từ ngày 30/11/2026."),
             ("Trước 30/11/2026 có bị phạt không?", "Hành vi này đã bị cấm từ trước và từng bị xử phạt theo Nghị định 98/2013/NĐ-CP. Nghị định 389/2026 thay thế phần quy định về xổ số của văn bản đó từ 30/11/2026."),
             ("Chia sẻ số trong nhóm Zalo có bị phạt không?", "Đưa ra con số cho kỳ chưa quay, kể cả trong nhóm chat, có thể bị coi là cung cấp thông tin dự đoán trước kết quả xổ số.")],
        basis=["Nghị định 389/2026/NĐ-CP, khoản 2 và điểm b khoản 5 Điều 18; khoản 4 Điều 3; Điều 30.", "Nghị định 98/2013/NĐ-CP (phần xổ số, được thay thế từ 30/11/2026)."],
        rel=["soi-cau-co-vi-pham-phap-luat-khong", "nghi-dinh-389-2026-xu-phat-xo-so", "choi-lo-de-co-bi-phat-khong"]))
    # 3. Nghị định 389 tóm tắt
    A.append(dict(
        slug="nghi-dinh-389-2026-xu-phat-xo-so", nav="Nghị định 389/2026: điểm chính",
        title="Nghị định 389/2026/NĐ-CP xử phạt xổ số: điểm chính người mua vé cần biết",
        desc="Tóm tắt Nghị định 389/2026/NĐ-CP hiệu lực 30/11/2026: phạt dự đoán kết quả 80–100 triệu, làm giả vé 80–100 triệu, cạo sửa vé 60–100 triệu, bán vé cho người dưới 18 tuổi, mức phạt tối đa.",
        h1="Nghị định 389/2026/NĐ-CP: điểm chính người mua vé cần biết",
        body=(
            "<p>Nghị định 389/2026/NĐ-CP quy định xử phạt vi phạm hành chính trong lĩnh vực kinh doanh xổ số, ban hành ngày <b>14/10/2026</b>, có hiệu lực từ <b>30/11/2026</b>. "
            "Nghị định thay thế phần quy định về xổ số trong Nghị định 98/2013/NĐ-CP và một số văn bản sửa đổi.</p>"
            "<h2>Mức phạt tối đa</h2><p>Cá nhân tối đa <b>100 triệu đồng</b>, tổ chức tối đa <b>200 triệu đồng</b>. Nguyên tắc chung: mức phạt cá nhân bằng 1/2 mức phạt tổ chức cho cùng hành vi, trừ một số khoản ghi rõ là mức phạt cho cá nhân.</p>"
            "<h2>Các hành vi liên quan đến người mua vé và người dùng thông tin</h2>"
            "<table><tr><th>Hành vi</th><th>Mức phạt</th></tr>"
            "<tr><td>Cung cấp thông tin dự đoán trước kết quả xổ số</td><td>80 – 100 triệu đồng (cá nhân), buộc nộp lại số lợi bất hợp pháp</td></tr>"
            "<tr><td>Làm giả vé xổ số để dự thưởng, lĩnh thưởng</td><td>80 – 100 triệu đồng (cá nhân)</td></tr>"
            "<tr><td>Cạo sửa, tẩy xóa vé xổ số để dự thưởng, lĩnh thưởng</td><td>60 – 100 triệu đồng (cá nhân)</td></tr>"
            "<tr><td>Sử dụng kết quả xổ số để tổ chức chương trình dự thưởng trái quy định</td><td>60 – 100 triệu đồng (cá nhân)</td></tr>"
            "<tr><td>Bán vé cho người không đủ điều kiện dự thưởng (ví dụ người dưới 18 tuổi)</td><td>Cá nhân 10 – 15 triệu, tổ chức 20 – 30 triệu đồng (trước đây chỉ cảnh cáo)</td></tr>"
            "<tr><td>Người không đủ điều kiện dự thưởng mua vé để dự thưởng</td><td>Cảnh cáo hoặc 10 – 15 triệu đồng (trước đây chỉ cảnh cáo)</td></tr></table>"
            "<h2>Với doanh nghiệp, đại lý xổ số</h2>"
            "<ul><li>Thông tin kết quả trúng thưởng sai lệch so với biên bản của Hội đồng giám sát xổ số: phạt tổ chức 180 – 200 triệu đồng, đình chỉ hoạt động kinh doanh xổ số 1 – 3 tháng.</li>"
            "<li>Kinh doanh xổ số không có Giấy chứng nhận đủ điều kiện: phạt tổ chức 160 – 200 triệu đồng.</li>"
            "<li>Cố tình kéo dài thời gian trả thưởng: phạt tổ chức 20 – 40 triệu đồng.</li></ul>"
            "<h2>Điều này có ý nghĩa gì với người xem kết quả?</h2>"
            "<p>Xem kết quả và thống kê các kỳ đã quay không bị ảnh hưởng. Điều cần tránh là các trang, nhóm, video đưa ra con số cho kỳ chưa quay. "
            "Khi dò vé, hãy dùng kết quả chính thức của công ty xổ số kiến thiết và kiểm tra lại trước khi lĩnh thưởng.</p>"),
        faq=[("Nghị định 389/2026 có hiệu lực khi nào?", "Từ ngày 30/11/2026."),
             ("Nghị định 389/2026 thay thế văn bản nào?", "Nghị định thay thế phần quy định xử phạt về xổ số trong Nghị định 98/2013/NĐ-CP và các điều khoản sửa đổi liên quan."),
             ("Mức phạt tối đa trong lĩnh vực xổ số là bao nhiêu?", "Cá nhân tối đa 100 triệu đồng, tổ chức tối đa 200 triệu đồng."),
             ("Bán vé số cho người dưới 18 tuổi bị phạt không?", "Có. Từ 30/11/2026, cá nhân bị phạt 10–15 triệu đồng, tổ chức 20–30 triệu đồng.")],
        basis=["Nghị định 389/2026/NĐ-CP ngày 14/10/2026 (Điều 3, 8, 18, 30)."],
        rel=["soi-cau-co-vi-pham-phap-luat-khong", "du-doan-xo-so-bi-phat-bao-nhieu", "mua-ve-so-duoi-18-tuoi"]))
    # 4. Lô đề
    A.append(dict(
        slug="choi-lo-de-co-bi-phat-khong", nav="Chơi lô đề có bị phạt không?",
        title="Chơi lô đề có bị phạt không? Mức phạt hành chính và hình sự",
        desc="Chơi lô đề là đánh bạc trái phép: mua số lô, số đề bị phạt hành chính theo Nghị định 282/2025/NĐ-CP, từ 5 triệu đồng có thể bị truy cứu hình sự tội đánh bạc. Khác gì mua vé số kiến thiết.",
        h1="Chơi lô đề có bị phạt không?",
        body=(
            "<p><b>Có.</b> Lô đề là hình thức đánh bạc trái phép dựa trên kết quả xổ số kiến thiết, khác hoàn toàn với việc mua vé số hợp pháp tại đại lý. "
            "Người mua số lô, số đề có thể bị phạt hành chính; nếu số tiền đánh bạc từ 5 triệu đồng trở lên thì có thể bị truy cứu trách nhiệm hình sự.</p>"
            "<h2>Phạt hành chính</h2>"
            "<p>Từ ngày 15/12/2025, Nghị định 282/2025/NĐ-CP thay thế Nghị định 144/2021/NĐ-CP về xử phạt trong lĩnh vực an ninh, trật tự, phòng chống tệ nạn xã hội. Theo Nghị định này:</p>"
            "<ul><li>Mua số lô, số đề: phạt tiền từ 200.000 đến 500.000 đồng.</li>"
            "<li>Các hành vi đánh bạc, tổ chức đánh bạc, làm chủ lô đề, giúp sức hoặc che giấu: mức phạt cao hơn, có thể đến 20 triệu đồng, kèm tịch thu tang vật và buộc nộp lại số lợi bất hợp pháp.</li>"
            "<li>Tổ chức vi phạm bị phạt gấp đôi cá nhân.</li></ul>"
            "<h2>Truy cứu hình sự</h2>"
            "<ul><li><b>Tội đánh bạc</b> (Điều 321 Bộ luật Hình sự): áp dụng khi tiền hoặc hiện vật dùng để đánh bạc trị giá từ 5 triệu đồng trở lên, hoặc dưới 5 triệu nhưng đã bị xử phạt hay kết án về hành vi này mà còn vi phạm.</li>"
            "<li><b>Tội tổ chức đánh bạc</b> (Điều 322): áp dụng với người tổ chức, làm chủ lô đề, tổ chức mạng lưới ghi số; hình phạt nặng hơn, đặc biệt khi dùng internet hoặc có tính chuyên nghiệp.</li></ul>"
            "<h2>Lô đề khác gì vé số kiến thiết?</h2>"
            "<table><tr><th>Vé số kiến thiết</th><th>Lô đề</th></tr>"
            "<tr><td>Do công ty xổ số kiến thiết nhà nước phát hành, bán qua đại lý</td><td>Do cá nhân tự tổ chức, không được phép</td></tr>"
            "<tr><td>Hợp pháp với người từ 18 tuổi</td><td>Đánh bạc trái phép</td></tr>"
            "<tr><td>Tiền bán vé nộp ngân sách, dùng cho công trình phúc lợi</td><td>Tiền vào túi chủ lô đề</td></tr></table>"
            "<h2>Vì sao trang kết quả có mục \"lô tô\"?</h2>"
            "<p>Trên các trang kết quả, \"lô tô\" chỉ là cách gọi quen thuộc cho <b>2 chữ số cuối của mỗi giải</b>, dùng để dò nhanh kết quả và làm thống kê. Việc xem bảng này không liên quan đến việc chơi lô đề.</p>"),
        faq=[("Mua số đề bị phạt bao nhiêu?", "Theo Nghị định 282/2025/NĐ-CP (hiệu lực 15/12/2025), mua số lô, số đề bị phạt 200.000–500.000 đồng; nếu số tiền đánh bạc từ 5 triệu đồng trở lên có thể bị truy cứu hình sự tội đánh bạc."),
             ("Đánh đề bao nhiêu tiền thì bị đi tù?", "Theo Điều 321 Bộ luật Hình sự, đánh bạc với tiền hoặc hiện vật trị giá từ 5 triệu đồng trở lên có thể bị truy cứu trách nhiệm hình sự."),
             ("Ghi lô đề bị xử lý thế nào?", "Người làm chủ lô đề, tổ chức mạng lưới ghi số có thể bị phạt hành chính nặng hoặc truy cứu hình sự tội tổ chức đánh bạc theo Điều 322 Bộ luật Hình sự."),
             ("Mua vé số kiến thiết có phải đánh bạc không?", "Không. Vé số kiến thiết do công ty nhà nước phát hành là hình thức hợp pháp với người từ 18 tuổi.")],
        basis=["Nghị định 282/2025/NĐ-CP ngày 30/10/2025, hiệu lực 15/12/2025 (thay thế Nghị định 144/2021/NĐ-CP).", "Bộ luật Hình sự 2015 (sửa đổi 2017), Điều 321 và Điều 322."],
        rel=["soi-cau-co-vi-pham-phap-luat-khong", "du-doan-xo-so-bi-phat-bao-nhieu", "mua-ve-so-duoi-18-tuoi"]))
    # 5. Dưới 18 tuổi
    A.append(dict(
        slug="mua-ve-so-duoi-18-tuoi", nav="Dưới 18 tuổi mua vé số có bị phạt?",
        title="Dưới 18 tuổi có được mua vé số không? Mức phạt từ 30/11/2026",
        desc="Người dưới 18 tuổi không đủ điều kiện tham gia dự thưởng xổ số. Từ 30/11/2026, bán vé cho người dưới 18 tuổi bị phạt 10–15 triệu (cá nhân), người mua bị cảnh cáo hoặc phạt 10–15 triệu đồng.",
        h1="Dưới 18 tuổi có được mua vé số không?",
        body=(
            "<p><b>Không.</b> Theo Thông tư 75/2013/TT-BTC, người chưa đủ 18 tuổi thuộc nhóm <b>không đủ điều kiện tham gia dự thưởng xổ số</b>, cùng với người bị hạn chế hoặc mất năng lực hành vi dân sự.</p>"
            "<h2>Mức phạt từ 30/11/2026</h2>"
            "<table><tr><th>Hành vi</th><th>Trước 30/11/2026</th><th>Từ 30/11/2026</th></tr>"
            "<tr><td>Bán vé cho người không đủ điều kiện dự thưởng</td><td>Cảnh cáo</td><td>Cá nhân 10 – 15 triệu đồng; tổ chức 20 – 30 triệu đồng</td></tr>"
            "<tr><td>Người không đủ điều kiện mua vé để dự thưởng</td><td>Cảnh cáo</td><td>Cảnh cáo hoặc 10 – 15 triệu đồng</td></tr></table>"
            "<h2>Nếu người dưới 18 tuổi trúng thưởng thì sao?</h2>"
            "<p>Vì không đủ điều kiện dự thưởng, vé do người dưới 18 tuổi mua có thể không được trả thưởng. Cách an toàn là người lớn tự mua vé và tự đứng tên lĩnh thưởng.</p>"
            "<h2>Lời khuyên cho phụ huynh và người bán vé</h2>"
            "<ul><li>Người bán vé dạo, đại lý nên hỏi tuổi khi người mua có vẻ chưa đủ 18.</li><li>Phụ huynh không nên nhờ con đi mua vé số hộ.</li>"
            "<li>Các ứng dụng, trang web xổ số hợp pháp đều yêu cầu người dùng từ 18 tuổi.</li></ul>"),
        faq=[("Dưới 18 tuổi mua vé số có bị phạt không?", "Từ 30/11/2026, người không đủ điều kiện dự thưởng mua vé để dự thưởng có thể bị cảnh cáo hoặc phạt 10–15 triệu đồng."),
             ("Bán vé số cho học sinh bị phạt bao nhiêu?", "Từ 30/11/2026, cá nhân bán vé cho người không đủ điều kiện dự thưởng bị phạt 10–15 triệu đồng, tổ chức 20–30 triệu đồng."),
             ("Bao nhiêu tuổi thì được mua vé số?", "Từ đủ 18 tuổi trở lên và có đủ năng lực hành vi dân sự.")],
        basis=["Thông tư 75/2013/TT-BTC (đối tượng không đủ điều kiện tham gia dự thưởng).", "Nghị định 389/2026/NĐ-CP, hiệu lực 30/11/2026."],
        rel=["nghi-dinh-389-2026-xu-phat-xo-so", "soi-cau-co-vi-pham-phap-luat-khong", "choi-lo-de-co-bi-phat-khong"]))
    return A


def build(page, card, tbl, esc, BASE):
    A = articles(); by = {a["slug"]: a for a in A}
    for a in A:
        rel = "<h2>Bài liên quan</h2><ul class='ls'>" + "".join(f'<li><a href="../{s}/">{by[s]["nav"]}</a></li>' for s in a["rel"]) + "</ul>"
        links = ("<p class='cauln'><a href=\"../../soi-cau/\">Soi cầu (thống kê kỳ đã quay)</a> · <a href=\"../../thong-ke/kiem-chung-du-doan-xsmb/\">Dự đoán XSMB có chính xác?</a> · "
                 "<a href=\"../\">Tất cả bài pháp lý xổ số</a></p>")
        body = (f"<p class='note'>Cập nhật {UPD} · Bài tổng hợp, không phải tư vấn pháp lý.</p>" + a["body"] + _faq_html(a["faq"], esc) + _basis(a["basis"]) + rel + links + NOTE)
        ld = [{"@context": "https://schema.org", "@type": "Article", "headline": a["h1"], "datePublished": UPD_ISO, "dateModified": UPD_ISO, "inLanguage": "vi",
               "author": {"@type": "Organization", "name": "XS Lab"}, "publisher": {"@type": "Organization", "name": "XS Lab"}, "mainEntityOfPage": BASE + f"phap-ly/{a['slug']}/"},
              {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": x}} for q, x in a["faq"]]}]
        page(f"phap-ly/{a['slug']}/", a["title"], a["desc"], [("Pháp lý xổ số", "phap-ly/"), (a["nav"], f"phap-ly/{a['slug']}/")], a["h1"], body, ld=ld)
    hub = ("<p>Các bài tổng hợp quy định pháp luật liên quan đến xổ số mà người mua vé và người xem kết quả hay thắc mắc, cập nhật theo Nghị định 389/2026/NĐ-CP có hiệu lực từ 30/11/2026.</p>"
           + card("<ul class='ls'>" + "".join(f'<li><a href="{a["slug"]}/">{a["nav"]}</a><br><span class="note">{esc(a["desc"])}</span></li>' for a in A) + "</ul>")
           + "<h2>XS Lab và quy định mới</h2>" + card("<p>XS Lab chỉ đăng kết quả xổ số và thống kê các kỳ đã quay. Các trang <a href=\"../soi-cau/\">soi cầu</a> chỉ đối chiếu cầu với kết quả đã công bố, không đưa con số cho kỳ chưa quay, không bán số, không quảng cáo.</p>")
           + NOTE)
    page("phap-ly/", "Pháp lý xổ số: soi cầu, dự đoán, lô đề, vé số – quy định mới 2026", "Tổng hợp quy định pháp luật về xổ số: soi cầu có phạm pháp không, dự đoán xổ số bị phạt bao nhiêu, chơi lô đề có bị phạt không, người dưới 18 tuổi mua vé số, Nghị định 389/2026.",
         [("Pháp lý xổ số", "phap-ly/")], "Pháp lý xổ số", hub)
    return [a["slug"] for a in A]
