# 🎯 Hệ Thống Thi Thử HSK 2 Chuẩn Hanban (Phần Đọc Hiểu - Reading)

Ứng dụng web thi thử HSK 2 (Phần Đọc hiểu - 25 câu - 100 điểm) được xây dựng mô phỏng **100% cấu trúc, giao diện và nội dung đề thi giấy chính thức** của Hanban / Viện Khổng Tử Trung Quốc.

🌐 **Trải nghiệm trực tuyến ngay tại:**  
👉 **[https://lamcbaotoan.github.io/Thi-HSK2/](https://lamcbaotoan.github.io/Thi-HSK2/)**

---

## 🌟 Tính Năng Nổi Bật

### 1. 🗂️ Ngân Hàng 6 Đề Thi Thật (150 Câu Hỏi)
- Tích hợp đầy đủ dữ liệu từ 6 bộ đề thi chính thức: **H20901, H20902, H21003, H21004, H21005, H21006**.
- Hỗ trợ 2 hình thức:
  - **Làm từng đề cụ thể**: Ôn tập trọn vẹn theo từng đề chuẩn.
  - **Đề ngẫu nhiên (Trộn đề)**: Hệ thống tự động bốc ngẫu nhiên 25 câu hỏi từ 6 bộ đề theo đúng tỷ lệ 4 phần của bài thi HSK 2.

### 2. 🖼️ Hình Ảnh Minh Họa Gốc Từ Đề Thi Giấy
- Trích xuất trực tiếp **36 hình vẽ minh họa** từ trang thi Đọc hiểu của 6 file đề PDF gốc (thay thế hoàn toàn emoji).
- Hình ảnh sắc nét, hiển thị chân thực bối cảnh đề thi, có tính năng **Lightbox phóng to** khi bấm vào ảnh.

### 3. 🔤 Phiên Âm Pinyin Đầy Đủ (Thẻ `<ruby>`)
- Đề thi HSK 2 chuẩn luôn có Pinyin đi kèm trên từng chữ Hán.
- Hệ thống chuẩn hóa **100% Pinyin** (bao gồm cả trợ từ ngữ pháp `了, 的, 吗, 呢, 吧, 过, 着...`).
- Hiển thị thanh thoát, dễ đọc như đề thi in.

### 4. ⚡ Hai Chế Độ Làm Bài Chuyên Biệt
- **🌱 Chế độ Luyện tập (Study Mode)**:
  - Không giới hạn thời gian.
  - Mặc định hiện Pinyin trên chữ Hán.
  - **Di chuột (hover) hoặc chạm** vào chữ để hiện tooltip dịch nghĩa tiếng Việt chi tiết từng từ.
  - Nút **"Ẩn / Hiện Pinyin"** trên thanh công cụ để tự thử thách nhớ mặt chữ.
- **⏱️ Chế độ Thi thật (Exam Mode)**:
  - Đồng hồ đếm ngược **22 phút** ghim góc màn hình.
  - Mặc định hiện Pinyin chuẩn như đề thi giấy.
  - Vô hiệu hóa toàn bộ tooltip dịch nghĩa tiếng Việt (thử thách tự hiểu câu).
  - Tự động nộp bài khi hết giờ (Auto-submit).

### 5. 📊 Chấm Điểm & Báo Cáo Chi Tiết
- Thang điểm chuẩn: **100 điểm** cho 25 câu (mỗi câu 4 điểm, 60 điểm là Đạt).
- Phân tích chi tiết tỷ lệ đúng từng phần:
  - *Phần 1: Nối tranh (Câu 1-5)*
  - *Phần 2: Điền từ vào chỗ trống (Câu 6-10)*
  - *Phần 3: Phán đoán Đúng / Sai (Câu 11-15)*
  - *Phần 4: Ghép cặp đối thoại (Câu 16-25)*
- **Chế độ Xem lại (Review)**: Đối chiếu đáp án đúng/sai, kèm hình ảnh minh họa và giải thích nghĩa chi tiết.

---

## 🚀 Hướng Dẫn Cài Đặt & Chạy Offline

Ứng dụng được đóng gói trong **MỘT file duy nhất `index.html`** (bao gồm HTML, Tailwind CSS CDN, JavaScript và dữ liệu Base64 hình ảnh).

1. Tải về hoặc clone repository:
   ```bash
   git clone https://github.com/lamcbaotoan/Thi-HSK2.git
   ```
2. Mở file `index.html` trực tiếp bằng bất kỳ trình duyệt nào (Chrome, Edge, Firefox, Safari) trên máy tính hoặc điện thoại mà không cần cài thêm bất kỳ phần mềm hay web server nào.

---

## ⚙️ Kích Hoạt GitHub Pages

Repository đã được thiết lập sẵn GitHub Actions (`.github/workflows/deploy.yml`). Khi bạn push code lên branch `main`, GitHub sẽ tự động triển khai web.

Nếu website chưa kích hoạt tự động, bạn chỉ cần thực hiện 2 bước đơn giản trên GitHub:
1. Vào repository: **Settings** -> **Pages**.
2. Ở mục **Build and deployment** -> **Source**:
   - Chọn **GitHub Actions** (hoặc chọn **Deploy from a branch** -> chọn nhánh `main` / thư mục `/(root)` -> bấm **Save**).
3. Đợi khoảng 1-2 phút, trang web sẽ hoạt động tại:  
   `https://lamcbaotoan.github.io/Thi-HSK2/`

---

*Phát triển phục vụ cộng đồng học tiếng Trung và luyện thi HSK 2.*

