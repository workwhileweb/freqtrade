<!-- Auto-translated from docs/ by script. Please review technical terms. -->

# Phân tích kiểm tra lại nâng cao

## Phân tích thẻ mua/nhập và bán/thoát

Có thể hữu ích nếu hiểu cách một chiến lược hoạt động theo các thẻ mua/nhập được sử dụng để
đánh dấu các điều kiện mua khác nhau. Bạn có thể muốn xem số liệu thống kê phức tạp hơn về mỗi lần mua và
điều kiện bán cao hơn những điều kiện được cung cấp bởi đầu ra kiểm tra ngược mặc định. Bạn cũng có thể muốn
xác định các giá trị chỉ báo trên nến tín hiệu dẫn đến việc mở giao dịch.

!!! Lưu ý
    Phân tích lý do mua sau đây chỉ có sẵn để kiểm tra lại, *không phải quá mức*.

Chúng ta cần chạy backtesting với tùy chọn `--export` được đặt thành `signals` để cho phép xuất
tín hiệu **và** giao dịch:``` bash
freqtrade backtesting -c <config.json> --timeframe <tf> --strategy <strategy_name> --timerange=<timerange> --export=signals
```Điều này sẽ yêu cầu freqtrade xuất ra một từ điển chiến lược, các cặp và tương ứng đã được chọn lọc.
DataFrame của nến dẫn đến tín hiệu vào và ra.
Tùy thuộc vào số lượng mục mà chiến lược của bạn tạo, tệp này có thể khá lớn, vì vậy hãy kiểm tra định kỳ thư mục `user_data/backtest_results` của bạn để xóa các bản xuất cũ.

Trước khi chạy backtest tiếp theo, hãy đảm bảo bạn xóa kết quả backtest cũ hoặc chạy
kiểm tra lại bằng tùy chọn `--cache none` để đảm bảo không có kết quả được lưu trong bộ nhớ đệm nào được sử dụng.

Nếu mọi việc suôn sẻ, bây giờ bạn sẽ thấy các tệp `backtest-result-{timestamp__signals.pkl` và `backtest-result-{timestamp__exited.pkl` trong thư mục `user_data/backtest_results`.

Để phân tích các thẻ vào/ra, bây giờ chúng ta cần sử dụng lệnh `freqtrade backtesting-analysis`
với tùy chọn `--analysis-groups` được cung cấp với các đối số được phân tách bằng dấu cách:``` bash
freqtrade backtesting-analysis -c <config.json> --analysis-groups 0 1 2 3 4 5
```Lệnh này sẽ đọc từ kết quả backtesting cuối cùng. Tùy chọn `--analysis-groups` là
được sử dụng để chỉ định các kết quả đầu ra dạng bảng khác nhau cho thấy lợi nhuận của từng nhóm hoặc giao dịch,
từ đơn giản nhất (0) đến chi tiết nhất trên mỗi cặp, mỗi thẻ mua và mỗi thẻ bán (4):

* 0: tỷ lệ thắng tổng thể và tóm tắt lợi nhuận theo enter_tag
* 1: tóm tắt lợi nhuận được nhóm theo enter_tag
* 2: tóm tắt lợi nhuận được nhóm theo enter_tag và exit_tag
* 3: tóm tắt lợi nhuận được nhóm theo cặp và enter_tag
* 4: tóm tắt lợi nhuận được nhóm theo cặp, enter_tag và exit_tag (điều này có thể khá lớn)
* 5: tóm tắt lợi nhuận được nhóm theo exit_tag

Có nhiều tùy chọn hơn bằng cách chạy với tùy chọn `-h`.

### Sử dụng tên tệp backtest

Theo mặc định, `backtesting-analysis` xử lý các kết quả backtest gần đây nhất trong thư mục `user_data/backtest_results`. 
Nếu bạn muốn phân tích kết quả từ lần kiểm tra ngược trước đó, hãy sử dụng tùy chọn `--backtest-filename` để chỉ định tệp mong muốn. Điều này cho phép bạn xem lại và phân tích lại kết quả đầu ra của backtest lịch sử bất cứ lúc nào bằng cách cung cấp tên tệp của kết quả backtest có liên quan:``` bash
freqtrade backtesting -c <config.json> --strategy <strategy_name> --timerange <timerange> --export signals --backtest-filename backtest-result-2025-03-05_20-38-34.zip
```Bạn sẽ thấy một số kết quả tương tự như bên dưới trong nhật ký có tên tệp có dấu thời gian đã được xuất:```
2022-06-14 16:28:32,698 - freqtrade.misc - INFO - dumping json to "mystrat_backtest-2022-06-14_16-28-32.json"
```Sau đó, bạn có thể sử dụng tên tệp đó trong `backtesting-analysis`:``` bash
freqtrade backtesting-analysis -c <config.json> --backtest-filename=backtest-result-2025-03-05_20-38-34.zip
```Để sử dụng kết quả từ một thư mục kết quả khác, bạn có thể sử dụng `--backtest-directory` để chỉ định thư mục``` bash
freqtrade backtesting-analysis -c <config.json> --backtest-directory custom_results/ --backtest-filename backtest-result-2025-03-05_20-38-34.zip
```### Điều chỉnh thẻ mua và thẻ bán để hiển thị

Để chỉ hiển thị các thẻ mua và bán nhất định trong đầu ra được hiển thị, hãy sử dụng hai tùy chọn sau:```
--enter-reason-list : Space-separated list of enter signals to analyse. Default: "all"
--exit-reason-list : Space-separated list of exit signals to analyse. Default: "all"
```Ví dụ:``` bash
freqtrade backtesting-analysis -c <config.json> --analysis-groups 0 2 --enter-reason-list enter_tag_a enter_tag_b --exit-reason-list roi custom_exit_tag_a stop_loss
```### Xuất tín hiệu chỉ báo nến

Sức mạnh thực sự của `phân tích kiểm tra ngược freqtrade` đến từ khả năng in ra chỉ báo
các giá trị hiện diện trên nến tín hiệu để cho phép điều tra và điều chỉnh chi tiết tín hiệu mua
các chỉ số. Để in ra một cột cho một bộ chỉ báo nhất định, hãy sử dụng `--indicator-list`
tùy chọn:``` bash
freqtrade backtesting-analysis -c <config.json> --analysis-groups 0 2 --enter-reason-list enter_tag_a enter_tag_b --exit-reason-list roi custom_exit_tag_a stop_loss --indicator-list rsi rsi_1h bb_lowerband ema_9 macd macdsignal
```Các chỉ báo phải có trong DataFrame chính của chiến lược của bạn (dành cho DataFrame chính của bạn).
khung thời gian hoặc khung thời gian cung cấp thông tin), nếu không chúng sẽ bị bỏ qua trong tập lệnh
đầu ra.

!!! Lưu ý "Danh sách chỉ số"
    Các giá trị chỉ báo sẽ được hiển thị cho cả điểm vào và điểm thoát. Nếu `--indicator-list all` được chỉ định, 
    chỉ các chỉ báo tại điểm vào mới được hiển thị để tránh danh sách quá lớn, điều này có thể xảy ra tùy thuộc vào chiến lược.

Có một loạt các lĩnh vực liên quan đến nến và thương mại được đưa vào phân tích.
có thể truy cập tự động bằng cách đưa chúng vào danh sách chỉ báo và chúng bao gồm:

* **open_date :** ngày giờ mở giao dịch
* **ngày_đóng:** ngày giờ đóng giao dịch
* **min_rate :** giá tối thiểu được thấy trong toàn bộ vị thế
* **max_rate :** giá tối đa được thấy trong toàn bộ vị thế
* **mở :** tín hiệu giá mở nến
* **đóng :** tín hiệu giá đóng nến
* **cao :** tín hiệu nến giá cao
* **thấp :** tín hiệu nến giá thấp
* **khối lượng :** khối lượng nến tín hiệu
* **tỷ lệ lợi nhuận :** tỷ lệ lợi nhuận giao dịch
* **profit_abs :** lợi nhuận tuyệt đối của giao dịch 

#### Đầu ra mẫu cho các giá trị chỉ báo``` bash
freqtrade backtesting-analysis -c user_data/config.json --analysis-groups 0 --indicator-list chikou_span tenkan_sen 
```Trong ví dụ này,
chúng tôi mong muốn hiển thị các giá trị chỉ báo `chikou_span` và `tenkan_sen` ở cả điểm vào và điểm thoát của giao dịch.

Đầu ra mẫu cho các chỉ báo có thể trông như thế này:

| cặp | open_date | enter_reason | exit_reason | chikou_span (mục nhập) | tenkan_sen (mục nhập) | chikou_span (thoát) | tenkan_sen (thoát) |
|----------||--------------------------|--------------|-------------|----------------------|-------------------|-----------------------------------|-------------------|
| DOGE/USDT | 2024-07-06 00:35:00+00:00 |              | exit_signal | 0,105 | 0,106 | 0,105 | 0,107 |
| BTC/USDT | 2024-08-05 14:20:00+00:00 |              | roi | 54643.440 | 51696.400 | 54386.000 | 52072.010 |

Như được hiển thị trong bảng, `chikou_span (entry)` đại diện cho giá trị chỉ báo tại thời điểm nhập giao dịch, 
trong khi `chikou_span (exit)` phản ánh giá trị của nó tại thời điểm thoát. 
Chế độ xem chi tiết này về các giá trị chỉ báo sẽ nâng cao khả năng phân tích.

Hậu tố `(entry)` và `(exit)` được thêm vào chỉ báo
để phân biệt các giá trị tại điểm vào và ra của giao dịch.

!!! Lưu ý "Chỉ báo toàn thương mại"
    Một số chỉ báo trên toàn thương mại không có hậu tố `(entry)` hoặc `(exit)`. Các chỉ số này bao gồm: `cặp`, `số tiền đặt cược`, 
    `max_stake_amount`, `amount`, `open_date`, `close_date`, `open_rate`, `close_rate`, `fee_open`, `fee_close`, `trade_duration`, 
    `tỷ lệ lợi nhuận`, `tỷ lệ lợi nhuận`, `exit_reason`,`initial_stop_loss_abs`, `tỷ lệ_stop_loss_abs` ban đầu`, `stop_loss_abs`, `tỷ lệ dừng_lỗ`, 
    `min_rate`, `max_rate`, `is_open`, `enter_tag`, `đòn bẩy`, `is_short`, `open_timestamp`, `close_timestamp` và `orders`

#### Lọc các chỉ báo dựa trên tín hiệu vào hoặc thoát

Theo mặc định, tùy chọn `--indicator-list` hiển thị các giá trị chỉ báo cho cả tín hiệu vào và ra. Để lọc các giá trị chỉ báo dành riêng cho tín hiệu vào lệnh, bạn có thể sử dụng đối số `--entry-only`. Tương tự, để chỉ hiển thị các giá trị chỉ báo ở tín hiệu thoát, hãy sử dụng đối số `--exit-only`.

Ví dụ: Hiển thị giá trị chỉ báo khi có tín hiệu vào lệnh:``` bash
freqtrade backtesting-analysis -c user_data/config.json --analysis-groups 0 --indicator-list chikou_span tenkan_sen --entry-only
```Ví dụ: Hiển thị giá trị chỉ báo khi có tín hiệu thoát:``` bash
freqtrade backtesting-analysis -c user_data/config.json --analysis-groups 0 --indicator-list chikou_span tenkan_sen --exit-only
```!!! ghi chú 
    Khi sử dụng các bộ lọc này, tên chỉ báo sẽ không có hậu tố là `(entry)` hoặc `(exit)`.

### Lọc sản lượng giao dịch theo ngày

Để chỉ hiển thị các giao dịch giữa các ngày trong phạm vi thời gian đã được kiểm tra lại của bạn, hãy cung cấp tùy chọn `timerange` thông thường ở định dạng `YYYYMMDD-[YYYYMMDD]`:```
--timerange : Timerange to filter output trades, start date inclusive, end date exclusive. e.g. 20220101-20221231
```Ví dụ: nếu khoảng thời gian backtest của bạn là `20220101-20221231` nhưng bạn chỉ muốn thực hiện giao dịch vào tháng 1:``` bash
freqtrade backtesting-analysis -c <config.json> --timerange 20220101-20220201
```### In ra các tín hiệu bị từ chối

Sử dụng tùy chọn `--rejected-signals` để in ra các tín hiệu bị từ chối.``` bash
freqtrade backtesting-analysis -c <config.json> --rejected-signals
```### Ghi bảng vào CSV

Một số kết quả đầu ra dạng bảng có thể trở nên lớn, vì vậy việc in chúng ra thiết bị đầu cuối là không thích hợp.
Sử dụng tùy chọn `--analysis-to-csv` để tắt tính năng in ra khỏi bảng để chuẩn hóa và ghi chúng vào tệp CSV.``` bash
freqtrade backtesting-analysis -c <config.json> --analysis-to-csv
```Theo mặc định, thao tác này sẽ ghi một tệp trên mỗi bảng đầu ra mà bạn đã chỉ định trong lệnh `backtesting-analysis`, ví dụ:``` bash
freqtrade backtesting-analysis -c <config.json> --analysis-to-csv --rejected-signals --analysis-groups 0 1
```Điều này sẽ ghi vào `user_data/backtest_results`:

* bị từ chối_signals.csv
* nhóm_0.csv
* nhóm_1.csv

Để ghi đè nơi các tệp sẽ được ghi, hãy chỉ định tùy chọn `--analysis-csv-path`.``` bash
freqtrade backtesting-analysis -c <config.json> --analysis-to-csv --analysis-csv-path another/data/path/
```