<!-- Auto-translated from docs/ by script. Please review technical terms. -->

# Khái niệm cơ bản về Freqtrade

Trang này cung cấp cho bạn một số khái niệm cơ bản về cách hoạt động và vận hành của Freqtrade.

## Thuật ngữ Freqtrade

* **Chiến lược**: Chiến lược giao dịch của bạn, cho bot biết phải làm gì.
* **Giao dịch**: Vị thế mở.
* **Lệnh mở**: Lệnh hiện được đặt trên sàn giao dịch và chưa hoàn tất.
* **Cặp**: Cặp có thể giao dịch, thường ở định dạng Cơ sở/Báo giá (ví dụ: `XRP/USDT` cho giao ngay, `XRP/USDT:USDT` cho hợp đồng tương lai).
* **Khung thời gian**: Độ dài nến sẽ sử dụng (ví dụ: `"5m"`, `"1h"`, ...).
* **Các chỉ báo**: Các chỉ báo kỹ thuật (SMA, EMA, RSI, ...).
* **Lệnh giới hạn**: Lệnh giới hạn thực hiện ở mức giá giới hạn được xác định hoặc tốt hơn.
* **Lệnh thị trường**: Đảm bảo khớp lệnh, có thể thay đổi giá tùy thuộc vào quy mô lệnh.
* **Lợi nhuận hiện tại**: Lợi nhuận hiện đang chờ xử lý (chưa thực hiện) cho giao dịch này. Điều này chủ yếu được sử dụng trong toàn bộ bot và giao diện người dùng.
* **Lợi nhuận thực hiện**: Lợi nhuận đã thực hiện. Chỉ phù hợp khi kết hợp với [thoát một phần](strategy-callbacks.md# adjustment-trade-position) - điều này cũng giải thích logic tính toán cho việc này.
* **Tổng lợi nhuận**: Tổng lợi nhuận đã thực hiện và chưa thực hiện. Con số tương đối (%) được tính dựa trên tổng số tiền đầu tư vào giao dịch này.

## Xử lý phí

Tất cả các tính toán lợi nhuận của Freqtrade đều bao gồm phí. Đối với các chế độ Backtesting / Hyperopt / Dry-run, phí mặc định của sàn giao dịch sẽ được sử dụng (cấp thấp nhất trên sàn giao dịch). Đối với các hoạt động trực tiếp, phí được sử dụng theo quy định của sàn giao dịch (điều này bao gồm giảm giá BNB, v.v.).

## Đặt tên theo cặpFreqtrade follows the [ccxt naming convention](https://docs.ccxt.com/#/README?id=consistency-of-base-and-quote-currencies) for currencies.
Sử dụng sai quy ước đặt tên sai thị trường thường sẽ dẫn đến việc bot không nhận ra cặp này, thường dẫn đến các lỗi như "cặp này không có sẵn".

### Đặt tên cặp điểm

Đối với các cặp giao ngay, việc đặt tên sẽ là `base/quote` (ví dụ: `ETH/USDT`).

### Đặt tên cặp tương lai

Đối với các cặp tương lai, việc đặt tên sẽ là `base/quote:settle` (ví dụ: `ETH/USDT:USDT`).

## Logic thực thi bot

Bắt đầu freqtrade ở chế độ chạy thử hoặc trực tiếp (sử dụng `freqtrade giao dịch`) sẽ khởi động bot và bắt đầu vòng lặp bot.
Thao tác này cũng sẽ chạy lệnh gọi lại `bot_start()`.

Theo mặc định, vòng lặp bot chạy vài giây một lần (`internals.process_throttle_secs`) và thực hiện các hành động sau:

* Tìm nạp các giao dịch mở từ sự kiên trì.
* Tính danh sách các cặp có thể giao dịch hiện tại.
* Tải xuống dữ liệu OHLCV cho danh sách cặp bao gồm tất cả [các cặp thông tin](strategy-customization.md#get-data-for-non-tradeable-pairs)  
  Bước này chỉ được thực hiện một lần trên mỗi Candle để tránh lưu lượng mạng không cần thiết.
* Gọi lại chiến lược `bot_loop_start()`.
* Phân tích chiến lược cho mỗi cặp.
  * Gọi `populate_indicators()`
  * Gọi `populate_entry_trend()`
  * Gọi `populate_exit_trend()`
* Cập nhật trạng thái lệnh mở giao dịch từ sàn giao dịch.
  * Gọi lại lệnh gọi lại chiến lược `order_filled()` cho các đơn hàng đã khớp.
  * Kiểm tra thời gian chờ cho các lệnh mở.
    * Gọi lại lệnh gọi lại chiến lược `check_entry_timeout()` cho các lệnh nhập đang mở.
    * Gọi lại lệnh gọi lại chiến lược `check_exit_timeout()` cho các lệnh thoát đang mở.
    * Gọi lại lệnh gọi lại chiến lược ` adjustment_order_price()` cho các lệnh đang mở.
      * Gọi lại lệnh gọi lại chiến lược ` adjustment_entry_price()` cho các lệnh nhập đang mở. *chỉ được gọi khi `just_order_price()` không được triển khai*
      * Gọi lại lệnh gọi lại chiến lược ` adjustment_exit_price()` cho các lệnh thoát đang mở. *chỉ được gọi khi `just_order_price()` không được triển khai*
* Xác minh các vị trí hiện có và cuối cùng đặt lệnh thoát.
  * Xem xét mức dừng lỗ, ROI và tín hiệu thoát, `custom_exit()` và `custom_stoploss()`.
  * Xác định giá thoát dựa trên cài đặt cấu hình `exit_pricing` hoặc bằng cách sử dụng lệnh gọi lại `custom_exit_price()`.
  * Trước khi đặt lệnh thoát, lệnh gọi lại chiến lược `confirm_trade_exit()` được gọi.
* Kiểm tra điều chỉnh vị thế cho các giao dịch đang mở nếu được bật bằng cách gọi `điều chỉnh_trade_position()` và đặt lệnh bổ sung nếu được yêu cầu.
* Kiểm tra xem các vị trí giao dịch có còn trống không (nếu đạt đến `max_open_trades`).
* Xác minh tín hiệu vào đang cố gắng vào vị trí mới.
  * Xác định giá nhập dựa trên cài đặt cấu hình `entry_pricing` hoặc bằng cách sử dụng lệnh gọi lại `custom_entry_price()`.
  * Trong chế độ Ký quỹ và Hợp đồng tương lai, lệnh gọi lại chiến lược `đòn bẩy()` được gọi để xác định mức đòn bẩy mong muốn.
  * Xác định quy mô cổ phần bằng cách gọi lại lệnh gọi lại `custom_stake_amount()`.
  * Trước khi đặt lệnh nhập, lệnh gọi lại chiến lược `confirm_trade_entry()` sẽ được gọi.

Vòng lặp này sẽ được lặp đi lặp lại nhiều lần cho đến khi dừng bot.

## Kiểm tra lại / logic thực thi Hyperopt

[backtesting](backtesting.md) hoặc [hyperopt](hyperopt.md) chỉ thực hiện một phần logic trên vì hầu hết các hoạt động giao dịch đều được mô phỏng đầy đủ.

* Tải dữ liệu lịch sử cho danh sách cặp được cấu hình.
* Gọi `bot_start()` một lần.
* Tính toán các chỉ số (gọi `populate_indicators()` một lần cho mỗi cặp).
* Tính toán các tín hiệu vào/ra (gọi `populate_entry_trend()` và `populate_exit_trend()` một lần trên mỗi cặp).
* Vòng trên mỗi nến mô phỏng điểm vào và thoát.
  * Gọi lại lệnh gọi lại chiến lược `bot_loop_start()`.* Kiểm tra thời gian chờ của Đơn hàng, thông qua cấu hình `unfilledtimeout` hoặc thông qua lệnh gọi lại chiến lược `check_entry_timeout()` / `check_exit_timeout()`.
  * Gọi lại lệnh gọi lại chiến lược ` adjustment_order_price()` cho các lệnh đang mở.
    * Gọi lại lệnh gọi lại chiến lược ` adjustment_entry_price()` cho các lệnh nhập đang mở. *chỉ được gọi khi `just_order_price()` không được triển khai!*
    * Gọi lại lệnh gọi lại chiến lược ` adjustment_exit_price()` cho các lệnh thoát đang mở. *chỉ được gọi khi `just_order_price()` không được triển khai!*
  * Kiểm tra tín hiệu nhập giao dịch (cột `enter_long` / `enter_short`).
  * Xác nhận mục nhập / thoát giao dịch (gọi `confirm_trade_entry()` và `confirm_trade_exit()` nếu được triển khai trong chiến lược).
  * Gọi `custom_entry_price()` (nếu được triển khai trong chiến lược) để xác định giá vào lệnh (Giá được di chuyển trong nến mở cửa).
  * Trong chế độ Ký quỹ và Hợp đồng tương lai, lệnh gọi lại chiến lược `đòn bẩy()` được gọi để xác định mức đòn bẩy mong muốn.
  * Xác định quy mô cổ phần bằng cách gọi lại lệnh gọi lại `custom_stake_amount()`.
  * Kiểm tra điều chỉnh vị thế cho các giao dịch đang mở nếu được bật và gọi `just_trade_position()` để xác định xem có yêu cầu lệnh bổ sung hay không.
  * Gọi lại lệnh gọi lại chiến lược `order_filled()` cho các lệnh nhập đã được điền.
  * Gọi `custom_stoploss()` và `custom_exit()` để tìm các điểm thoát tùy chỉnh.
  * Đối với các lệnh thoát dựa trên tín hiệu thoát, thoát tùy chỉnh và thoát một phần: Gọi `custom_exit_price()` để xác định giá thoát (Giá được di chuyển trong nến đóng cửa).
  * Gọi lại lệnh gọi lại chiến lược `order_filled()` cho các lệnh thoát đã được điền.
* Tạo đầu ra báo cáo backtest

!!! Lưu ý
    Cả Backtesting và Hyperopt đều bao gồm Phí mặc định của sàn giao dịch trong tính toán. Phí tùy chỉnh có thể được chuyển tới backtesting / hyperopt bằng cách chỉ định đối số `--fee`.

!!! Cảnh báo "Tần suất cuộc gọi lại"
    Backtesting sẽ gọi mỗi cuộc gọi lại ở mức tối đa. một lần cho mỗi nến (`--timeframe-detail` sửa đổi hành vi này thành một lần cho mỗi nến chi tiết).
    Hầu hết các lệnh gọi lại sẽ được gọi một lần trong mỗi lần lặp trực tiếp (thường là cứ sau ~ 5 giây) - điều này có thể gây ra kết quả kiểm tra ngược không khớp.