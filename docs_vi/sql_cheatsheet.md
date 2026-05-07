<!-- Auto-translated from docs/ by script. Please review technical terms. -->

#Trình trợ giúp SQL

Trang này chứa một số trợ giúp nếu bạn muốn truy vấn db sqlite của mình.

!!! Mẹo "Các hệ cơ sở dữ liệu khác"
    Để sử dụng các Hệ thống cơ sở dữ liệu khác như PostgreSQL hoặc MariaDB, bạn có thể sử dụng các truy vấn tương tự, nhưng bạn cần sử dụng ứng dụng khách tương ứng cho hệ thống cơ sở dữ liệu. [Nhấp vào đây](advanced-setup.md#use-a-other-database-system) để tìm hiểu cách thiết lập một hệ thống cơ sở dữ liệu khác với freqtrade.

!!! Cảnh báo
    Nếu bạn không quen với SQL, bạn nên hết sức cẩn thận khi chạy các truy vấn trên cơ sở dữ liệu của mình.  
    Luôn đảm bảo có bản sao lưu cơ sở dữ liệu của bạn trước khi chạy bất kỳ truy vấn nào.

## Cài đặt sqlite3

Sqlite3 là một ứng dụng sqlite dựa trên thiết bị đầu cuối.
Vui lòng sử dụng trình soạn thảo Cơ sở dữ liệu trực quan như SqliteBrowser nếu bạn cảm thấy thoải mái hơn với điều đó.

### Cài đặt Ubuntu/Debian```bash
sudo apt-get install sqlite3
```### Sử dụng sqlite3 qua docker

Hình ảnh docker freqtrade có chứa sqlite3, vì vậy bạn có thể chỉnh sửa cơ sở dữ liệu mà không cần phải cài đặt bất cứ thứ gì trên hệ thống máy chủ.``` bash
docker compose exec freqtrade /bin/bash
sqlite3 <database-file>.sqlite
```## Mở cơ sở dữ liệu```bash
sqlite3
.open <filepath>
```## Cấu trúc bảng

### Liệt kê bảng```bash
.tables
```### Hiển thị cấu trúc bảng```bash
.schema <table_name>
```### Nhận tất cả các giao dịch trong bảng```sql
SELECT * FROM trades;
```## Truy vấn phá hoại

Các truy vấn ghi vào cơ sở dữ liệu.
Các truy vấn này thường không cần thiết vì freqtrade cố gắng tự xử lý tất cả các hoạt động của cơ sở dữ liệu - hoặc hiển thị chúng thông qua các lệnh API hoặc điện tín.

!!! Cảnh báo
    Vui lòng đảm bảo bạn có bản sao lưu cơ sở dữ liệu của mình trước khi chạy bất kỳ truy vấn nào dưới đây.

!!! Nguy hiểm
    Bạn cũng **không bao giờ** chạy bất kỳ truy vấn viết nào (`update`, `insert`, `delete`) trong khi bot được kết nối với cơ sở dữ liệu.
    Điều này có thể và sẽ dẫn đến hỏng dữ liệu - rất có thể là không có khả năng phục hồi.

### Sửa lỗi giao dịch vẫn mở sau khi thoát thủ công trên sàn giao dịch

!!! Cảnh báo
    Việc bán thủ công một cặp trên sàn giao dịch sẽ không bị bot phát hiện và nó vẫn sẽ cố gắng bán. Bất cứ khi nào có thể, nên sử dụng /forceexit <tradeid> để thực hiện điều tương tự.  
    Chúng tôi khuyên bạn nên sao lưu tệp cơ sở dữ liệu của mình trước khi thực hiện bất kỳ thay đổi thủ công nào.

!!! Lưu ý
    Điều này không cần thiết sau /forceexit, vì các lệnh Force_exit sẽ được bot tự động đóng trong lần lặp tiếp theo.```sql
UPDATE trades
SET is_open=0,
  close_date=<close_date>,
  close_rate=<close_rate>,
  close_profit = close_rate / open_rate - 1,
  close_profit_abs = (amount * <close_rate> * (1 - fee_close) - (amount * (open_rate * (1 - fee_open)))),
  exit_reason=<exit_reason>
WHERE id=<trade_ID_to_update>;
```#### Ví dụ```sql
UPDATE trades
SET is_open=0,
  close_date='2020-06-20 03:08:45.103418',
  close_rate=0.19638016,
  close_profit=0.0496,
  close_profit_abs = (amount * 0.19638016 * (1 - fee_close) - (amount * (open_rate * (1 - fee_open)))),
  exit_reason='force_exit'  
WHERE id=31;
```### Xóa giao dịch khỏi cơ sở dữ liệu

!!! Mẹo "Sử dụng Phương pháp RPC để xóa giao dịch"
    Hãy cân nhắc sử dụng `/delete <tradeid>` thông qua telegram hoặc API còn lại. Đó là cách được khuyến nghị để xóa giao dịch, vì nó cũng sẽ xóa các lệnh và dữ liệu tùy chỉnh tương ứng, đồng thời cũng sẽ kích hoạt các sự kiện cần thiết trong bot để giữ mọi thứ được đồng bộ hóa.

Nếu bạn vẫn muốn xóa trực tiếp giao dịch khỏi cơ sở dữ liệu, bạn có thể sử dụng truy vấn bên dưới.

!!! Nguy hiểm
    Một số hệ thống (Ubuntu) vô hiệu hóa khóa ngoại trong gói sqlite3 của chúng. Khi sử dụng sqlite - vui lòng đảm bảo rằng các khóa ngoại được bật bằng cách chạy `PRAGMA external_keys = ON` trước truy vấn trên.```sql
DELETE FROM trades WHERE id = <tradeid>;
DELETE FROM orders WHERE ft_trade_id = <tradeid>;
DELETE FROM trade_custom_data WHERE ft_trade_id = <tradeid>;


DELETE FROM trades WHERE id = 31;
DELETE FROM orders WHERE ft_trade_id = 31;
DELETE FROM trade_custom_data WHERE ft_trade_id = 31;
```!!! Cảnh báo
    Điều này sẽ xóa giao dịch được chỉ định khỏi cơ sở dữ liệu. Hãy đảm bảo rằng bạn đã lấy đúng id và **KHÔNG BAO GIỜ** chạy truy vấn này mà không có mệnh đề `where`.