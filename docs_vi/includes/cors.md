<!-- Auto-translated from docs/ by script. Please review technical terms. -->

## CORS

Toàn bộ phần này chỉ cần thiết trong các trường hợp có nguồn gốc chéo (khi bạn có nhiều API bot chạy trên `localhost:8081`, `localhost:8082`, ...) và muốn kết hợp chúng thành một phiên bản FreqUI.

??? info "Giải thích kỹ thuật"    All web-based front-ends are subject to [CORS](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS) - Cross-Origin Resource Sharing.
Vì hầu hết các yêu cầu tới API Freqtrade phải được xác thực nên chính sách CORS phù hợp là chìa khóa để tránh các vấn đề bảo mật.
    Ngoài ra, tiêu chuẩn không cho phép các chính sách `*` CORS đối với các yêu cầu có thông tin xác thực, vì vậy cài đặt này phải được đặt phù hợp.

Người dùng có thể cho phép truy cập từ các URL gốc khác nhau vào API bot thông qua cài đặt cấu hình `CORS_origins`.
Nó bao gồm một danh sách các URL được phép sử dụng tài nguyên từ API của bot.Assuming your application is deployed as `https://frequi.freqtrade.io/home/` - this would mean that the following configuration becomes necessary:
```jsonc
{
    //...
    "jwt_secret_key": "somethingRandomSomethingRandom123",
    "CORS_origins": ["https://frequi.freqtrade.io"],
    //...
}
```In the following (pretty common) case, FreqUI is accessible on `http://localhost:8080/trade` (this is what you see in your navbar when navigating to freqUI).
![freqUI url](assets/frequi_url.png)The correct configuration for this case is `http://localhost:8080` - the main part of the URL including the port.
```jsonc
{
    //...
    "jwt_secret_key": "somethingRandomSomethingRandom123",
    "CORS_origins": ["http://localhost:8080"],
    //...
}
```!!! Mẹo "dấu gạch chéo"    The trailing slash is not allowed in the `CORS_origins` configuration (e.g. `"http://localhots:8080/"`).
Cấu hình như vậy sẽ không có hiệu lực và lỗi cors sẽ vẫn còn.

!!! Lưu ý
    Chúng tôi thực sự khuyên bạn cũng nên đặt `jwt_secret_key` thành thứ gì đó ngẫu nhiên và chỉ có bạn biết để tránh truy cập trái phép vào bot của bạn.