<!-- Auto-translated from docs/ by script. Please review technical terms. -->

# Tần suất UIFreqtrade provides a builtin webserver, which can serve [FreqUI](https://github.com/freqtrade/frequi), the freqtrade frontend.
Theo mặc định, giao diện người dùng được cài đặt tự động như một phần của quá trình cài đặt (script, docker).
freqUI cũng có thể được cài đặt thủ công bằng cách sử dụng lệnh `freqtrade install-ui`.
Lệnh tương tự này cũng có thể được sử dụng để cập nhật freqUI lên các bản phát hành mới.Once the bot is started in trade / dry-run mode (with `freqtrade trade`) - the UI will be available under the configured API port (by default `http://127.0.0.1:8080`).
??? Lưu ý "Bạn đang muốn đóng góp cho freqUI?"    Developers should not use this method, but instead clone the corresponding use the method described in the [freqUI repository](https://github.com/freqtrade/frequi) to get the source-code of freqUI. A working installation of node will be required to build the frontend.
!!! mẹo "không cần freqUI để chạy freqtrade"
    freqUI là thành phần tùy chọn của freqtrade và không bắt buộc phải chạy bot.
    Nó là một giao diện người dùng có thể được sử dụng để giám sát bot và tương tác với nó - nhưng bản thân freqtrade sẽ hoạt động hoàn toàn bình thường nếu không có nó.

## Cấu hình

FreqUI không có tệp cấu hình riêng - nhưng giả sử có sẵn thiết lập hoạt động cho [rest-api](rest-api.md).
Vui lòng tham khảo trang tài liệu tương ứng để thiết lập với freqUI

## giao diện người dùng

FreqUI là một ứng dụng web hiện đại, đáp ứng, có thể được sử dụng để giám sát và tương tác với bot của bạn.

FreqUI cung cấp chủ đề sáng cũng như chủ đề tối.
Chủ đề có thể dễ dàng chuyển đổi thông qua một nút nổi bật ở đầu trang.
Chủ đề của ảnh chụp màn hình trên trang này sẽ thích ứng với Chủ đề tài liệu đã chọn, vì vậy để xem phiên bản tối (hoặc sáng), vui lòng chuyển chủ đề của Tài liệu.

### Đăng nhập

Ảnh chụp màn hình bên dưới hiển thị màn hình đăng nhập của freqUI.

![FreqUI - login](assets/frequi-login-CORS.png#only-dark)
![FreqUI - login](asset/frequi-login-CORS-light.png#only-light)

!!! Gợi ý "CORS"
    Lỗi Cors hiển thị trong ảnh chụp màn hình này là do giao diện người dùng đang chạy trên một cổng khác với API và [CORS](#cors) chưa được thiết lập chính xác.

### Chế độ xem giao dịch

Chế độ xem giao dịch cho phép bạn hình dung các giao dịch mà bot đang thực hiện và tương tác với bot.
Trên trang này, bạn cũng có thể tương tác với bot bằng cách khởi động và dừng nó và - nếu được định cấu hình - buộc vào và thoát giao dịch.

![FreqUI - chế độ xem giao dịch](assets/freqUI-trade-pane-dark.png#only-dark)
![FreqUI - chế độ xem giao dịch](asset/freqUI-trade-pane-light.png#only-light)

### Trang tổng quan

Chế độ xem trang tổng quan cung cấp cái nhìn tổng quan về hiệu suất và trạng thái của bot.
Nếu nhiều bot được kết nối, trang tổng quan sẽ hiển thị tổng quan về tất cả các bot được kết nối, cho phép bạn dễ dàng chuyển đổi giữa chúng hoặc chỉ hiển thị một tập hợp con các bot có sẵn.

#### Số dư trên Ví

Tính năng mới trong freqtrade 2026.4: Điều này cho thấy sự cân bằng của bot theo thời gian.

So với biểu đồ "Lợi nhuận tích lũy", biểu đồ này sẽ hiển thị số dư thực tế của bot theo thời gian, bao gồm lãi và lỗ chưa thực hiện, cũng như tiền gửi và rút tiền.

Dữ liệu lịch sử đã được điền lại dựa trên dữ liệu trao đổi có sẵn - tuy nhiên được coi là nỗ lực tốt nhất và có thể không chính xác 100%.
Cụ thể hơn, nó sẽ không bao gồm tiền gửi và rút tiền và sẽ giả định số dư ban đầu của số dư hiện tại - lãi/lỗ.

Để rõ ràng - dòng đánh dấu "Bắt đầu ghi lại" được hiển thị trên biểu đồ, cho biết thời điểm diễn ra quá trình di chuyển sang hệ thống theo dõi số dư ví mới.
Chỉ ngoài điểm này, số dư trong ví mới được mong đợi là chính xác.

### Trình cấu hình sơ đồ

Các lô FreqUI có thể được định cấu hình thông qua đối tượng cấu hình `plot_config` trong chiến lược (có thể được tải thông qua nút "từ chiến lược") hoặc thông qua giao diện người dùng.
Nhiều cấu hình biểu đồ có thể được tạo và chuyển đổi theo ý muốn - cho phép các chế độ xem linh hoạt, khác nhau vào biểu đồ của bạn.

Có thể truy cập cấu hình lô thông qua nút "Bộ cấu hình lô" (biểu tượng Cog) ở góc trên cùng bên phải của chế độ xem giao dịch.

![FreqUI - cấu hình cốt truyện](assets/freqUI-plot-configurator-dark.png#only-dark)
![FreqUI - cấu hình cốt truyện](asset/freqUI-plot-configurator-light.png#only-light)

### Cài đặt

Một số cài đặt liên quan đến giao diện người dùng có thể được thay đổi bằng cách truy cập trang cài đặt.

Những điều bạn có thể thay đổi (trong số những điều khác):

* Múi giờ của giao diện người dùng* Trực quan hóa các giao dịch đang mở như một phần của favicon (tab trình duyệt)
* Màu nến (lên/xuống -> đỏ/xanh)
* Bật / tắt các loại thông báo trong ứng dụng

![FreqUI - Chế độ xem cài đặt](assets/frequi-settings-dark.png#only-dark)
![FreqUI - Chế độ xem cài đặt](asset/frequi-settings-light.png#only-light)

## Chế độ máy chủ web

khi freqtrade được khởi động ở [chế độ máy chủ web](utils.md#webserver-mode) (freqtrade bắt đầu bằng `freqtrade webserver`), máy chủ web sẽ khởi động ở chế độ đặc biệt cho phép các tính năng bổ sung, ví dụ:

* Tải dữ liệu
* Kiểm tra danh sách cặp
* [Chiến lược backtesting](#backtesting)
* ... được mở rộng

###Đang kiểm tra lại

Khi freqtrade được khởi động ở [chế độ máy chủ web](utils.md#webserver-mode) (freqtrade bắt đầu bằng `freqtrade webserver`), chế độ xem backtesting sẽ khả dụng.
Chế độ xem này cho phép bạn kiểm tra lại các chiến lược và trực quan hóa kết quả.

Bạn cũng có thể tải và trực quan hóa các kết quả backtest trước đó cũng như so sánh các kết quả với nhau.

![FreqUI - Backtesting](assets/freqUI-backtesting-dark.png#only-dark)
![FreqUI - Backtesting](assets/freqUI-backtesting-light.png#only-light)


--8<-- "bao gồm/cors.md"