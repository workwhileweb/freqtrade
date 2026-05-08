<!-- Auto-translated from docs/ by script. Please review technical terms. -->

# Cách cập nhật

Để cập nhật cài đặt freqtrade của bạn, vui lòng sử dụng một trong các phương pháp bên dưới, tương ứng với phương pháp cài đặt của bạn.

!!! Lưu ý “Theo dõi thay đổi”
    Những thay đổi đáng chú ý/hành vi đã thay đổi sẽ được ghi lại trong nhật ký thay đổi được đăng cùng với mỗi bản phát hành.
    Đối với nhánh phát triển, vui lòng theo dõi PR để tránh bị bất ngờ trước những thay đổi.

## Tại sao phải cập nhật?

Luôn cập nhật bot của bạn không chỉ đảm bảo rằng bạn có các tính năng và cải tiến mới nhất mà còn là yêu cầu bắt buộc để giữ cho bot của bạn hoạt động trơn tru.
Freqtrade phụ thuộc rất nhiều vào API của sàn giao dịch cơ bản, API này thay đổi khá thường xuyên nếu được xem xét trên các sàn giao dịch.
Để đảm bảo khả năng tương thích liên tục, hãy đảm bảo cập nhật bot của bạn thường xuyên.

## Docker

!!! Lưu ý "Cài đặt cũ sử dụng hình ảnh `master`"
    Chúng tôi đang chuyển từ bản chính sang bản ổn định cho bản phát hành Hình ảnh - vui lòng điều chỉnh tệp docker của bạn và thay thế `freqtradeorg/freqtrade:master` bằng `freqtradeorg/freqtrade:stable```` bash
docker compose pull
docker compose up -d
```## Cài đặt thông qua tập lệnh thiết lập``` bash
./setup.sh --update
```!!! Lưu ý
    Đảm bảo chạy lệnh này khi môi trường ảo của bạn bị tắt!

## Cài đặt gốc đơn giản

Hãy đảm bảo rằng bạn cũng đang cập nhật các phần phụ thuộc - nếu không mọi thứ có thể bị hỏng mà bạn không nhận ra.``` bash
git pull
pip install -U -r requirements.txt
pip install -e .

# Ensure freqUI is at the latest version
freqtrade install-ui 
```## Sự cố khi cập nhật

Các sự cố cập nhật thường thiếu phần phụ thuộc (bạn không làm theo hướng dẫn ở trên) - hoặc do phần phụ thuộc không cài đặt được.
Chúng tôi cố gắng đảm bảo rằng các phần phụ thuộc nặng nề có sẵn bánh xe cho các nền tảng chính, nhưng đôi khi điều này là không thể.

Vui lòng tham khảo các phần cài đặt tương ứng (các phần vấn đề thường gặp được liên kết bên dưới).

[Các sự cố cài đặt thường gặp](installation.md#troubleshooting)
[Các sự cố cài đặt thường gặp - windows](installation.md#windows-installation-error)