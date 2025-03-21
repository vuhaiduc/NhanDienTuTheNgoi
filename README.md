# Hệ thống phát hiện tư thế ngồi thông minh

Hệ thống phát hiện tư thế ngồi thông minh là một ứng dụng sử dụng công nghệ Computer Vision và Machine Learning để theo dõi và cảnh báo người dùng về tư thế ngồi không đúng. Hệ thống này giúp người dùng cải thiện tư thế ngồi, tránh các vấn đề sức khỏe liên quan đến việc ngồi sai tư thế trong thời gian dài.

## Tính năng chính

- **Phát hiện tư thế ngồi**: Sử dụng thư viện MediaPipe để nhận diện các điểm keypoint trên cơ thể và xác định tư thế ngồi.
- **Cảnh báo tư thế sai**: Hệ thống sẽ cảnh báo bằng âm thanh và hiển thị thông báo khi phát hiện tư thế ngồi không đúng.
- **Theo dõi thời gian**: Theo dõi thời gian ngồi đúng và sai tư thế, hiển thị thông tin trực tiếp trên giao diện.
- **Giao diện trực quan**: Giao diện web đơn giản, dễ sử dụng với hiệu ứng hình ảnh và âm thanh thân thiện.

## Công nghệ sử dụng

- **Python**: Ngôn ngữ lập trình chính.
- **Flask**: Framework web để xây dựng giao diện và xử lý yêu cầu HTTP.
- **MediaPipe**: Thư viện AI của Google để nhận diện các điểm keypoint trên cơ thể.
- **OpenCV**: Xử lý hình ảnh và video.
- **gTTS**: Chuyển đổi văn bản thành giọng nói để cảnh báo người dùng.
- **HTML/CSS/JavaScript**: Xây dựng giao diện người dùng và xử lý tương tác.

## Video demo

Dưới đây là video demo về cách hệ thống hoạt động:

[![Xem video demo trên YouTube](https://i9.ytimg.com/vi_webp/PpePOWZTrzA/mq2.webp?sqp=CIjv774G-oaymwEmCMACELQB8quKqQMa8AEB-AH-CYAC0AWKAgwIABABGDggZShlMA8=&rs=AOn4CLDcSgrikfD21yGEIPjOkRpwixEhhQ)](https://youtu.be/PpePOWZTrzA)

## Cài đặt và chạy ứng dụng

### Yêu cầu hệ thống

- Python 3.x
- Webcam hoặc thiết bị camera tương thích.
- Các thư viện Python cần thiết (xem trong `requirements.txt`).

### Các bước cài đặt

1. **Clone repository**:
   ```bash
   git clone https://github.com/your-repository/smart-posture-detection.git
   cd smart-posture-detection
2. **Cài đặt các thư viện cần thiết**:
    ```bash
   pip install -r requirements.txt
3. **Chạy ứng dụng**:
    ```bash
    python app.py
4. **Truy cập ứng dụng**:
Mở trình duyệt và truy cập địa chỉ http://localhost:5000.
## Cấu trúc thư mục

- **app.py**: File chính chứa mã nguồn Python để xử lý logic và chạy ứng dụng.
- **templates/index.html**: File HTML chứa giao diện người dùng.
- **static/**: Thư mục chứa các tệp tĩnh như CSS, JavaScript, hình ảnh (nếu có).
- **requirements.txt**: Danh sách các thư viện Python cần thiết.

## Hướng dẫn sử dụng

1. **Khởi động ứng dụng**: Chạy lệnh `python app.py` để khởi động máy chủ.
2. **Truy cập giao diện**: Mở trình duyệt và truy cập `http://localhost:5000`.
3. **Theo dõi tư thế**: Hệ thống sẽ hiển thị video trực tiếp từ webcam và cảnh báo khi phát hiện tư thế ngồi sai.
4. **Tải lại trang**: Nếu cần, nhấn nút "Tải lại" để khởi động lại hệ thống.
## Giấy phép

Dự án này được phân phối dưới giấy phép MIT. Xem tệp `LICENSE` để biết thêm chi tiết.

## Liên hệ

Nếu bạn có bất kỳ câu hỏi hoặc góp ý nào, vui lòng liên hệ qua email: **dnagbinh12@gmai.com**.

## Tác giả

**Nhóm 5 - CNTT 16_04 - Đại học Đại Nam**:

- Tạ Việt Anh
- Đặng Thanh Bình
- Vũ Hải Đức
- Nguyễn Tuấn Anh

## Lời cảm ơn

Cảm ơn tất cả các thành viên trong nhóm đã đóng góp vào dự án này. Đặc biệt chúng tôi xin gửi lời cảm ơn chân thành đến:

- **Thầy Lê Trung Hiếu** - Người đã tận tình hướng dẫn, chia sẻ kiến thức và kinh nghiệm quý báu, giúp chúng tôi vượt qua những khó khăn trong quá trình thực hiện dự án.
- **Thầy Nguyễn Văn Nhân** - Người đã truyền cảm hứng, động viên và hỗ trợ chúng tôi trong việc phát triển và hoàn thiện hệ thống.

Nhờ sự giúp đỡ và định hướng của hai thầy, chúng tôi đã có thể hoàn thành dự án một cách suôn sẻ và hiệu quả. Chúng tôi luôn trân trọng những đóng góp và sự hỗ trợ quý báu từ các thầy.
