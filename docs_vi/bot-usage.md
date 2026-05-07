<!-- Auto-translated from docs/ by script. Please review technical terms. -->

# Khởi động bot

Trang này giải thích các thông số khác nhau của bot và cách chạy nó.

!!! Lưu ý
    Nếu bạn đã sử dụng `setup.sh`, đừng quên kích hoạt môi trường ảo của bạn (`source .venv/bin/activate`) trước khi chạy các lệnh freqtrade.

!!! Cảnh báo "Đồng hồ cập nhật"
    Đồng hồ trên hệ thống chạy bot phải chính xác, được đồng bộ hóa với máy chủ NTP đủ thường xuyên để tránh các vấn đề khi liên lạc với các sàn giao dịch.

## Lệnh của bot

--8<-- "lệnh/main.md"

### Lệnh giao dịch Bot

--8<-- "commands/trade.md"

### Làm cách nào để chỉ định tập tin cấu hình nào sẽ được sử dụng?

Bot cho phép bạn chọn tập tin cấu hình nào bạn muốn sử dụng bằng cách
tùy chọn dòng lệnh `-c/--config`:```bash
freqtrade trade -c path/far/far/away/config.json
```Theo mặc định, bot tải tệp cấu hình `config.json` từ hiện tại
thư mục làm việc.

### Làm cách nào để sử dụng nhiều file cấu hình?

Bot cho phép bạn sử dụng nhiều tệp cấu hình bằng cách chỉ định nhiều
Tùy chọn `-c/--config` trong dòng lệnh. Thông số cấu hình
được xác định trong các tệp cấu hình sau ghi đè các tham số có cùng tên
được xác định trong các tệp cấu hình trước đó được chỉ định trong dòng lệnh trước đó.

Ví dụ: bạn có thể tạo một tệp cấu hình riêng bằng khóa và bí mật của mình
đối với Sàn giao dịch bạn sử dụng để giao dịch, hãy chỉ định tệp cấu hình mặc định với
khóa trống và giá trị bí mật khi chạy ở Chế độ khô (thực tế không
yêu cầu họ):```bash
freqtrade trade -c ./config.json
```và chỉ định cả hai tệp cấu hình khi chạy ở Chế độ giao dịch trực tiếp thông thường:```bash
freqtrade trade -c ./config.json -c path/to/secrets/keys.config.json
```Điều này có thể giúp bạn ẩn khóa Exchange riêng tư và bí mật Exchange trên máy cục bộ của bạn
bằng cách đặt quyền truy cập tệp thích hợp cho tệp chứa bí mật thực sự và ngoài ra,
ngăn chặn việc vô tình tiết lộ dữ liệu riêng tư nhạy cảm khi bạn xuất bản các ví dụ
cấu hình của bạn trong các vấn đề của dự án hoặc trên Internet.

Xem thêm chi tiết về kỹ thuật này với các ví dụ trong trang tài liệu trên
[cấu hình](configuration.md).

### Nơi lưu trữ dữ liệu tùy chỉnh

Freqtrade cho phép tạo thư mục dữ liệu người dùng bằng cách sử dụng `freqtrade create-userdir --userdir someDirectory`.
Thư mục này sẽ trông như sau:```
user_data/
├── backtest_results
├── data
├── hyperopts
├── hyperopt_results
├── plot
└── strategies
```Bạn có thể thêm cài đặt mục nhập "user_data_dir" vào cấu hình của mình để luôn trỏ bot của bạn vào thư mục này.
Ngoài ra, hãy chuyển `--userdir` vào mọi lệnh.
Bot sẽ không khởi động được nếu thư mục không tồn tại nhưng sẽ tạo các thư mục con cần thiết.

Thư mục này phải chứa các chiến lược tùy chỉnh của bạn, các hàm hyperopt và loss hyperopt tùy chỉnh, dữ liệu lịch sử backtesting (được tải xuống bằng lệnh backtesting hoặc tập lệnh tải xuống) và kết quả đầu ra của biểu đồ.

Bạn nên sử dụng tính năng kiểm soát phiên bản để theo dõi các thay đổi đối với chiến lược của mình.

### Cách sử dụng **--chiến lược**?

Tham số này sẽ cho phép bạn tải lớp chiến lược tùy chỉnh của mình.
Để kiểm tra quá trình cài đặt bot, bạn có thể sử dụng `SampleStrategy` được cài đặt bởi lệnh phụ `create-userdir` (thường là `user_data/strategy/sample_strategy.py`).

Bot sẽ tìm kiếm tệp chiến lược của bạn trong `user_data/strategies`.
Để sử dụng các thư mục khác, vui lòng đọc phần tiếp theo về `--strategy-path`.

Để tải một chiến lược, chỉ cần chuyển tên lớp (ví dụ: `CustomStrategy`) vào tham số này.

**Ví dụ:**
Trong `user_data/strategies` bạn có một tệp `my_awesome_strategy.py` có
một lớp chiến lược có tên `AwesomeStrategy` để tải nó:```bash
freqtrade trade --strategy AwesomeStrategy
```Nếu bot không tìm thấy tệp chiến lược của bạn, nó sẽ hiển thị lỗi
thông báo lý do (Không tìm thấy tệp hoặc lỗi trong mã của bạn).

Tìm hiểu thêm về tệp chiến lược trong
[Tùy chỉnh chiến lược](strategy-customization.md).

### Cách sử dụng **--strategy-path**?

Tham số này cho phép bạn thêm đường dẫn tra cứu chiến lược bổ sung, đường dẫn này sẽ được
được kiểm tra trước các vị trí mặc định (Đường dẫn được truyền phải là một thư mục!):```bash
freqtrade trade --strategy AwesomeStrategy --strategy-path /some/directory
```#### Làm thế nào để cài đặt chiến lược?

Điều này rất đơn giản. Sao chép dán tập tin chiến lược của bạn vào thư mục
`user_data/strategies` hoặc sử dụng `--strategy-path`. Và thì đấy, bot đã sẵn sàng để sử dụng nó.

### Cách sử dụng **--db-url**?

Khi bạn chạy bot ở chế độ Chạy thử, theo mặc định sẽ không có giao dịch nào được thực hiện
được lưu trữ trong cơ sở dữ liệu. Nếu bạn muốn lưu trữ các hành động bot của mình trong DB
sử dụng `--db-url`. Điều này cũng có thể được sử dụng để chỉ định cơ sở dữ liệu tùy chỉnh
ở chế độ sản xuất. Lệnh ví dụ:```bash
freqtrade trade -c config.json --db-url sqlite:///tradesv3.dry_run.sqlite
```## Bước tiếp theo

Chiến lược tối ưu của bot sẽ thay đổi theo thời gian tùy theo xu hướng thị trường. Bước tiếp theo là
[Tùy chỉnh chiến lược](strategy-customization.md).