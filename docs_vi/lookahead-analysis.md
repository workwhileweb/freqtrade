<!-- Auto-translated from docs/ by script. Please review technical terms. -->

# Phân tích tầm nhìn

Trang này giải thích cách xác thực chiến lược của bạn theo xu hướng nhìn trước.

Sự thiên vị nhìn trước là nguyên nhân của bất kỳ chiến lược nào vì đôi khi rất dễ đưa ra sự thiên vị này nhưng lại rất khó phát hiện.

Backtesting khởi tạo tất cả các dấu thời gian (tải toàn bộ khung dữ liệu vào bộ nhớ) và tính toán tất cả các chỉ báo cùng một lúc.
Điều này có nghĩa là nếu các chỉ báo hoặc tín hiệu vào/ra của bạn nhìn vào các nến trong tương lai, điều này sẽ làm sai lệch backtest của bạn.

Lệnh `lookahead-analysis` yêu cầu phải có sẵn dữ liệu lịch sử.
Để tìm hiểu cách lấy dữ liệu cho các cặp và trao đổi mà bạn quan tâm,
hãy đi tới phần [Tải xuống dữ liệu](data-download.md) của tài liệu.
`phân tích nhìn trước` cũng hỗ trợ các chiến lược freqai.

Lệnh này xâu chuỗi các backtest nội bộ và chọc vào chiến lược để kích động nó thể hiện sự thiên vị về phía trước.
Điều này được thực hiện bằng cách không nhìn vào chính mã chiến lược mà nhìn vào các giá trị chỉ báo đã thay đổi và các điểm vào/ra được di chuyển so với backtest đầy đủ.

`phân tích nhìn trước` có thể sử dụng các tùy chọn điển hình của [Backtesting](backtesting.md), nhưng buộc các tùy chọn sau:

- `--cache` bị buộc phải "không".
- `--max-open-trades` buộc phải ít nhất bằng số lượng cặp.
- `--dry-run-wallet` về cơ bản buộc phải là vô hạn (1 tỷ).
- `--stake-amount` buộc phải ở mức tĩnh 10000 (10k).
- `--enable-protections` buộc phải tắt.
- `order_types` buộc phải là "thị trường" (mục nhập muộn) trừ khi `--lookahead-allow-limit-orders` được đặt.

Chúng được thiết lập để tránh người dùng vô tình tạo ra kết quả dương tính giả.

## Tham chiếu lệnh phân tích nhìn trước

--8<-- "lệnh/lookahead-analysis.md"

!!! Lưu ý
    Kết quả đầu ra ở trên đã được giảm xuống thành các tùy chọn mà `phân tích nhìn trước` thêm vào bên cạnh các lệnh kiểm tra ngược thông thường.

###Giới thiệu

Nhiều chiến lược mà người lập trình không hề biết đã trở thành nạn nhân của khuynh hướng nhìn trước.
Điều này thường làm cho chiến lược backtest trông có vẻ sinh lợi, đôi khi đến mức cực đoan, nhưng điều này không thực tế vì chiến lược này đang "gian lận" bằng cách xem dữ liệu mà nó không có ở chế độ khô hoặc trực tiếp.

Lý do tại sao các chiến lược có thể "gian lận" là do quá trình kiểm tra lại freqtrade đưa vào khung dữ liệu đầy đủ bao gồm tất cả các dấu thời gian của nến ngay từ đầu.
Nếu lập trình viên không cẩn thận hoặc không biết cách mọi thứ hoạt động bên trong
(đôi khi có thể rất khó tìm ra) thì chiến lược sẽ hướng tới tương lai.

Lệnh này được thực hiện để cố gắng xác minh tính hợp lệ dưới dạng sai lệch nhìn về phía trước đã nói ở trên.

### Lệnh hoạt động như thế nào?

Nó sẽ bắt đầu bằng việc kiểm tra lại tất cả các cặp để tạo đường cơ sở cho các chỉ báo và điểm vào/ra.
Sau khi chạy thử nghiệm ngược ban đầu này, nó sẽ xem liệu `số tiền giao dịch tối thiểu` có được đáp ứng hay không và nếu không thì sẽ hủy phân tích nhìn trước cho chiến lược này.  
Nếu điều này xảy ra, hãy sử dụng khoảng thời gian rộng hơn để nhận được nhiều giao dịch hơn cho việc phân tích hoặc sử dụng khoảng thời gian diễn ra nhiều giao dịch hơn.

Sau khi thiết lập đường cơ sở, nó sẽ thực hiện các lần chạy thử ngược bổ sung cho từng mục nhập và thoát riêng biệt.  
Khi các quá trình kiểm tra ngược xác minh này hoàn tất, nó sẽ so sánh cả hai khung dữ liệu (đường cơ sở và được cắt lát) để tìm bất kỳ sự khác biệt nào về giá trị của các cột và báo cáo độ lệch.
Sau khi tất cả các tín hiệu đã được xác minh hoặc làm sai lệch, một bảng kết quả sẽ được tạo để người dùng xem.

### Làm thế nào để tìm và loại bỏ sự thiên vị? Làm thế nào tôi có thể cứu vãn một chiến lược thiên vị?

Nếu bạn tìm thấy một chiến lược thiên vị trực tuyến và muốn có kết quả tương tự, chỉ cần không thiên vị,
thì hầu hết thời gian bạn sẽ không gặp may.Thông thường, sự thiên vị trong chiến lược là yếu tố thúc đẩy lợi nhuận "quá tốt để có thể là sự thật".
Việc loại bỏ các điều kiện hoặc chỉ báo đẩy lợi nhuận tăng lên khỏi sự thiên vị thường sẽ làm cho chiến lược trở nên tồi tệ hơn đáng kể.
Bạn có thể cứu vãn được một phần nếu các chỉ báo hoặc điều kiện sai lệch không phải là cốt lõi của chiến lược, hoặc ở đó
là các tín hiệu vào và ra khác không bị sai lệch.

### Ví dụ về thành kiến nhìn trước

- `shift(-10)` nhìn vào 10 ngọn nến trong tương lai.
- Sử dụng `iloc[]` trong các hàm populate_* để truy cập một hàng cụ thể trong khung dữ liệu.
- Vòng lặp for có xu hướng gây ra sai lệch khi nhìn về phía trước nếu bạn không kiểm soát chặt chẽ những số nào được lặp qua.
- Các hàm tổng hợp như `.mean()`, `.min()` và `.max()`, không có cửa sổ cuộn,
  sẽ tính toán giá trị trên **toàn bộ** khung dữ liệu, do đó nến tín hiệu sẽ "nhìn thấy" một giá trị bao gồm cả các nến trong tương lai.
  Thay vào đó, một ví dụ không thiên vị sẽ là nhìn lại các nến bằng cách sử dụng `rolling()`:
  ví dụ: `dataframe['volume_mean_12'] = dataframe['volume'].rolling(12).mean()`
- `ta.MACD(dataframe, 12, 26, 1)` sẽ đưa ra độ lệch với chu kỳ tín hiệu là 1.

### Các cột trong bảng kết quả có ý nghĩa gì?

- `filename`: tên của file chiến lược đã kiểm tra
- `strategy`: tên lớp chiến lược đã được kiểm tra
- `has_bias`: kết quả phân tích nhìn trước. “Không” sẽ tốt, “Có” sẽ không tốt.
- `total_signals`: số lượng tín hiệu đã kiểm tra (mặc định là 20)
- `biased_entry_signals`: tìm thấy độ lệch trong nhiều mục đó
- `biased_exit_signals`: tìm thấy sự thiên vị ở nhiều lần thoát
- `biased_indicators`: hiển thị cho bạn các chỉ báo được xác định trong populate_indicators

Bạn có thể nhận được kết quả dương tính giả trong `biased_exit_signals` nếu bạn có các tín hiệu vào lệnh sai lệch được ghép nối với các lần thoát đó.
Tuy nhiên, một lệnh vào lệnh sai lệch thường cũng sẽ dẫn đến một lệnh thoát lệnh sai lệch,
ngay cả khi bản thân lối ra không tạo ra sai lệch -
đặc biệt nếu các điều kiện vào và ra của bạn sử dụng cùng một chỉ báo sai lệch.

**Giải quyết sự thiên vị trong các mục nhập trước, sau đó giải quyết các kết quả cuối cùng.**

### Hãy cẩn thận

- `phân tích nhìn trước` chỉ có thể xác minh / làm sai lệch các giao dịch mà nó đã tính toán và xác minh.
Nếu chiến lược có nhiều tín hiệu/loại tín hiệu khác nhau, bạn phải chọn tham số phù hợp để đảm bảo rằng tất cả các tín hiệu đã được kích hoạt ít nhất một lần. Các tín hiệu không được kích hoạt sẽ không được xác minh.  
Điều này sẽ dẫn đến kết quả âm tính giả, tức là chiến lược sẽ được báo cáo là không thiên vị.
- `phân tích nhìn trước` có quyền truy cập vào các tùy chọn kiểm tra ngược tương tự và điều này có thể gây ra sự cố.
Vui lòng không sử dụng bất kỳ tùy chọn nào như bật xếp chồng vị trí vì điều này sẽ làm sai lệch số lượng tín hiệu đã kiểm tra.
Nếu bạn quyết định làm như vậy, hãy đảm bảo gấp đôi rằng bạn sẽ không bao giờ hết chỗ `max_open_trades`,
và bạn có đủ vốn trong cấu hình ví backtest.
- lệnh giới hạn kết hợp với các lệnh gọi lại `custom_entry_price()` và `custom_exit_price()` có thể gây ra các mục nhập trễ/trì hoãn và tồn tại, gây ra kết quả dương tính giả.
Để tránh điều này - lệnh thị trường buộc phải thực hiện lệnh này. Điều này ngầm có nghĩa là các lệnh gọi lại `custom_entry_price()` và `custom_exit_price()` không được gọi.
Việc sử dụng `--lookahead-allow-limit-orders` sẽ bỏ qua phần ghi đè và sử dụng các loại đơn đặt hàng đã được định cấu hình của bạn - tuy nhiên cuối cùng đã cho thấy kết quả dương tính giả.
- Trong bảng kết quả có cột `biased_indicators`
sẽ gắn cờ sai các chỉ báo mục tiêu FreqAI được xác định trong `set_freqai_targets()` là sai lệch.  
**Những điều này không mang tính thiên vị và có thể bỏ qua một cách an toàn.**