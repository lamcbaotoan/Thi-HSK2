# 🎯 Hệ Thống Thi Thử HSK 2 Chuẩn Hanban - Đầy Đủ 60 Câu (Nghe & Đọc)

Ứng dụng web thi thử HSK 2 toàn diện với **đầy đủ 60 câu hỏi** (35 câu Nghe hiểu + 25 câu Đọc hiểu - Thang điểm 200) được xây dựng mô phỏng **100% cấu trúc, giao diện, âm thanh và nội dung đề thi giấy chính thức** của Hanban / Viện Khổng Tử Trung Quốc.

🌐 **Trải nghiệm trực tuyến ngay tại:**  
👉 **[https://lamcbaotoan.github.io/Thi-HSK2/](https://lamcbaotoan.github.io/Thi-HSK2/)**

---

## 🌟 Tính Năng Nổi Bật

### 1. 🗂️ Đầy Đủ 60 Câu Chuẩn Hanban (Ngân Hàng 6 Đề - 360 Câu Hỏi)
- Tích hợp chuẩn xác 100% dữ liệu từ 6 bộ đề thi chính thức: **H20901, H20902, H21003, H21004, H21005, H21006**.
- **Đánh số câu hỏi chuẩn quốc tế từ Câu 1 đến Câu 60**:
  - **一、听 力 (Phần Nghe hiểu - Câu 1 đến 35)**:
    - *Phần 1 (Câu 1 - 10)*: Phán đoán Đúng / Sai theo tranh (√ / ×).
    - *Phần 2 (Câu 11 - 20)*: Nối tranh A - F theo đoạn hội thoại ngắn.
    - *Phần 3 (Câu 21 - 30)*: Trắc nghiệm A, B, C theo đoạn hội thoại ngắn.
    - *Phần 4 (Câu 31 - 35)*: Trắc nghiệm A, B, C theo đoạn hội thoại dài.
  - **二、阅 读 (Phần Đọc hiểu - Câu 36 đến 60)**:
    - *Phần 1 (Câu 36 - 40)*: Nối 6 tranh A - F với câu văn mô tả.
    - *Phần 2 (Câu 41 - 45)*: Điền từ A - F vào chỗ trống.
    - *Phần 3 (Câu 46 - 50)*: Đọc đoạn văn ngắn, phán đoán nhận định ★ Đúng (√) hay Sai (×).
    - *Phần 4 (Câu 51 - 60)*: Ghép nối cặp câu đối thoại (51-55 và 56-60).

### 2. 🎧 Tích Hợp Audio Kép (Dual-Voice Engine: Giọng Nữ 👩 + Giọng Nam 👨)
- Mô phỏng đúng quy chế phòng thi chuẩn Hanban ("每题听两次"):
  - **Lần 1:** Phát bằng **Giọng Nữ** (`👩 Nữ`, cao độ $1.15$, tốc độ $0.88$).
  - **Khoảng nghỉ:** Tự động dừng nghỉ $1.4$ giây giữa 2 lần phát với đồng hồ báo hiệu.
  - **Lần 2:** Tự động phát tiếp bằng **Giọng Nam** (`👨 Nam`, cao độ trầm $0.78 - 0.95$, tốc độ $0.86$).
- Có nút phát riêng lẻ từng giọng: `👩 Nữ` hoặc `👨 Nam` để luyện nghe theo nhu cầu.
- Floating Audio Player ghim góc dưới màn hình có hoạt ảnh sóng âm và hiển thị tiến trình phát thời gian thực.
- Trong chế độ Luyện tập và Xem lại sau khi nộp bài: Hiển thị trọn vẹn bản ghi lời thoại (听力材料) có kèm Pinyin và dịch nghĩa.

### 3. 🖼️ Hình Ảnh Minh Họa Cắt Gốc Từ Đề Thi Thật & Thẻ Ví Dụ (例如) Chuẩn Hanban
- Cắt trực tiếp **162 hình ảnh minh họa thật** từ các trang đề thi PDF gốc (bao gồm tranh cho phần Nghe 1-20 và phần Đọc 36-40).
- Hỗ trợ xem hình ảnh sắc nét, có **Lightbox phóng to** khi bấm vào ảnh.
- **Có đầy đủ thẻ Ví dụ (`例如`)** ở đầu cả 8 phần thi (4 phần Nghe + 4 phần Đọc) y hệt đề thi giấy chính thức.

### 4. 🔤 Phiên Âm Pinyin Đầy Đủ & Tra Từ Điển Tương Tác
- Toàn bộ đề thi được bọc thẻ `<ruby>` chuẩn HTML5 với Pinyin hiển thị phía trên chữ Hán.
- **Rà soát 100% chuẩn xác theo đề thi Hanban**:
  - Khử sạch hoàn toàn các dấu nháy đơn sai quy tắc (dùng `shǒujī`, `piányi`, `wàimiàn` thay vì `shǒu'jī`, `pián'yi`).
  - Chuẩn hóa các chữ đa âm: `眼睛得休息` với `得` đọc là **`děi`** (*cần phải*), `时间长` với `长` đọc là **`cháng`**, `笑着` với `着` đọc là **`zhe`**, `还有` với `还` đọc là **`hái`**.
  - Sửa chuẩn xác Câu 46 đề H20901: `买了个新手机` với lượng từ `个 (ge)`.
- **Chế độ Luyện tập (Study Mode)**: Hover hoặc chạm vào bất kỳ chữ Hán nào để xem tooltip dịch nghĩa tiếng Việt chi tiết.
- **Chế độ Thi thật (Exam Mode)**: Vẫn hiện Pinyin chuẩn đề thi nhưng ẩn nghĩa tiếng Việt để thử thách khả năng tự đọc hiểu.

### 5. 🎯 3 Phạm Vi Thi Linh Hoạt & Bảng Chuyển Câu Nhanh
- 🎓 **Toàn bộ đề thi (60 câu)**: Thời gian 50 phút, 200 điểm (Nghe 100đ, Đọc 100đ).
- 📖 **Chuyên đề Đọc hiểu (Câu 36 - 60)**: Thời gian 22 phút, 100 điểm.
- 🎧 **Chuyên đề Nghe hiểu (Câu 1 - 35)**: Thời gian 25 phút, 100 điểm.
- Hỗ trợ làm theo từng đề cụ thể (H20901 - H21006) hoặc làm đề trộn ngẫu nhiên từ ngân hàng câu hỏi.
- Thanh công cụ có **Bảng câu hỏi (Grid 1 - 60)** giúp thí sinh dễ dàng theo dõi câu đã làm / chưa làm và chuyển câu tức thì.

### 6. 📊 Báo Cáo Điểm & Lời Giải Chi Tiết
- Chấm điểm tự động và đánh giá kết quả Đỗ (≥ 60% tổng điểm) / Chưa đỗ.
- Tách bạch điểm số từng phần Nghe và Đọc.
- Chế độ xem lại (Review): Hiển thị đáp án đã chọn, đáp án đúng (tô màu xanh), giải thích chi tiết, lời thoại và dịch nghĩa toàn bài.

---

## 🚀 Hướng Dẫn Chạy Trên Máy Cục Bộ

1. Clone repository về máy:
   ```bash
   git clone https://github.com/lamcbaotoan/Thi-HSK2.git
   ```
2. Mở trực tiếp file `index.html` bằng bất kỳ trình duyệt nào (Chrome, Edge, Firefox, Safari) để làm bài ngay mà không cần cài đặt thêm server hay môi trường phức tạp.

---

*Hệ thống được phát triển phục vụ cộng đồng học tiếng Trung và luyện thi HSK 2 quốc tế.*
