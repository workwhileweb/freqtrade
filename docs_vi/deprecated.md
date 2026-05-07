<!-- Auto-translated from docs/ by script. Please review technical terms. -->

# Tính năng không được dùng nữa

Trang này chứa mô tả về các đối số dòng lệnh, tham số cấu hình
và các tính năng của bot đã được nhóm phát triển bot tuyên bố là KHÔNG DÙNG
và không còn được hỗ trợ nữa. Vui lòng tránh sử dụng chúng trong cấu hình của bạn.

## Tính năng đã bị xóa

### tùy chọn dòng lệnh `--refresh-pairs-cached`

`--refresh-pairs-cached` trong bối cảnh backtesting, hyperopt và edge cho phép làm mới dữ liệu nến để backtesting.
Vì điều này dẫn đến nhiều nhầm lẫn và làm chậm quá trình kiểm tra ngược (mặc dù không nằm trong quá trình kiểm tra ngược), nên điều này đã được coi là một lệnh phụ freqtrade riêng biệt `freqtrade download-data`.

Tùy chọn dòng lệnh này không còn được dùng nữa trong 2019.7-dev (nhánh phát triển) và bị xóa vào 2019.9.

### Tùy chọn dòng lệnh **--dynamic-whitelist**

Tùy chọn dòng lệnh này không được dùng nữa vào năm 2018 và đã xóa freqtrade 2019.6-dev (nhánh phát triển) và trong freqtrade 2019.7.
Thay vào đó, vui lòng tham khảo [danh sách cặp](plugins.md#pairlists-and-pairlist-handlers).

### tùy chọn dòng lệnh `--live`

`--live` trong bối cảnh backtesting được phép tải xuống dữ liệu đánh dấu mới nhất để backtesting.
Chỉ tải xuống 500 nến mới nhất nên không hiệu quả trong việc lấy dữ liệu backtest tốt.
Đã bị xóa vào năm 2019-7-dev (nhánh phát triển) và trong freqtrade 2019.8.

### `ticker_interval` (bây giờ là `khung thời gian`)

Hỗ trợ cho thuật ngữ `ticker_interval` không còn được dùng nữa vào năm 2020.6 mà thay vào đó là `khung thời gian` - và mã tương thích đã bị xóa vào năm 2022.3.

### Cho phép chạy nhiều cặp danh sách theo trình tự

Phần `"danh sách cặp"` trước đây trong cấu hình đã bị xóa và được thay thế bằng `"danh sách cặp"` - là danh sách để chỉ định một chuỗi các danh sách cặp.

Phần cũ của các tham số cấu hình ("danh sách cặp"`) không còn được dùng nữa vào năm 2019.11 và đã bị xóa vào năm 2020.4.

### ngừng sử dụng bidVolume và AskVolume từ danh sách cặp khối lượng

Vì chỉ có thể so sánh quoteVolume giữa các nội dung nên các tùy chọn khác (bidVolume, AskVolume) đã không được dùng nữa vào năm 2020.4 và đã bị xóa vào năm 2020.9.

### Sử dụng các bước đặt lệnh cho giá thoát

Sử dụng `order_book_min` và `order_book_max` được sử dụng để cho phép đẩy sổ đặt hàng và cố gắng tìm vị trí ROI tiếp theo - cố gắng đặt lệnh bán sớm.
Tuy nhiên, vì điều này làm tăng rủi ro và không mang lại lợi ích nên nó đã bị xóa vì mục đích bảo trì vào năm 2021.7.

### Chế độ Hyperopt kế thừa

Việc sử dụng các tệp hyperopt riêng biệt không còn được dùng nữa vào năm 2021.4 và bị xóa vào năm 2021.9.
Vui lòng chuyển sang [Chiến lược tham số hóa](hyperopt.md) mới để hưởng lợi từ giao diện hyperopt mới.

## Thay đổi chiến lược giữa V2 và V3

Hợp đồng tương lai biệt lập/giao dịch bán khống được giới thiệu vào năm 2022.4. Điều này đòi hỏi những thay đổi lớn về cài đặt cấu hình, giao diện chiến lược, ...

Chúng tôi đã nỗ lực rất nhiều để duy trì khả năng tương thích với các chiến lược hiện có, vì vậy nếu bạn chỉ muốn tiếp tục sử dụng freqtrade trên thị trường giao ngay thì không cần thay đổi gì.
Mặc dù trong tương lai, chúng tôi có thể ngừng hỗ trợ giao diện hiện tại nhưng chúng tôi sẽ thông báo riêng về điều này và có thời gian chuyển tiếp thích hợp.

Vui lòng làm theo hướng dẫn [Di chuyển chiến lược](strategy_migration.md) để di chuyển chiến lược của bạn sang định dạng mới nhằm bắt đầu sử dụng các chức năng mới.

### webhooks - những thay đổi kể từ phiên bản 2022.4

#### `buy_tag` đã được đổi tên thành `enter_tag`

Điều này chỉ áp dụng cho chiến lược của bạn và có thể áp dụng cho webhook.Chúng tôi sẽ giữ một lớp tương thích cho 1-2 phiên bản (vì vậy cả `buy_tag` và `enter_tag` vẫn hoạt động), nhưng việc hỗ trợ cho điều này trong webhooks sẽ biến mất sau đó.

#### Thay đổi cách đặt tên

Thuật ngữ Webhook đã thay đổi từ "bán" thành "thoát" và từ "mua" thành "nhập", loại bỏ "webhook" trong quá trình này.

* `webhookbuy`, `webhookentry` -> `entry`
* `webhookbuyfill`, `webhookentryfill` -> `entry_fill`
* `webhookbuycancel`, `webhookentrycancel` -> `entry_cancel`
* `webhooksell`, `webhookexit` -> `exit`
* `webhooksellfill`, `webhookexitfill` -> `exit_fill`
* `webhooksellcancel`, `webhookexitcancel` -> `exit_cancel`

## Loại bỏ `populate_any_indicators`

phiên bản 2023.3 đã loại bỏ `populate_any_indicators` để thay thế bằng các phương pháp phân tách cho kỹ thuật tính năng và mục tiêu. Vui lòng đọc [tài liệu di chuyển](strategy_migration.md#freqai-strategy) để biết đầy đủ chi tiết.

## Loại bỏ `bảo vệ` khỏi cấu hình

Cài đặt bảo vệ từ cấu hình thông qua `"bảo vệ": [],` đã bị xóa vào năm 2024.10 sau khi đưa ra cảnh báo không dùng nữa trong hơn 3 năm.

## lưu trữ dữ liệu hdf5

Việc sử dụng hdf5 làm bộ lưu trữ dữ liệu không còn được dùng nữa vào năm 2024.12 và bị xóa vào năm 2025.1. Chúng tôi khuyên bạn nên chuyển sang định dạng dữ liệu lông vũ.

Vui lòng sử dụng lệnh phụ [`convert-data`](data-download.md#sub-command-convert-data) để chuyển đổi dữ liệu hiện có của bạn sang một trong các định dạng được hỗ trợ trước khi cập nhật.

## Định cấu hình ghi nhật ký nâng cao qua config

Việc định cấu hình nhật ký hệ thống và nhật ký lần lượt thông qua `--logfile systemd` và `--logfile tạp chí` đã không được dùng nữa vào năm 2025.3.
Thay vào đó, vui lòng sử dụng [thiết lập nhật ký](advanced-setup.md#advanced-logging) dựa trên cấu hình.

## Loại bỏ mô-đun cạnh

Mô-đun biên không còn được dùng nữa vào năm 2023.9 và bị xóa vào năm 2025.6.
Tất cả các chức năng của cạnh đã bị xóa và việc cấu hình cạnh sẽ dẫn đến lỗi.

## Điều chỉnh để xử lý tỷ lệ cấp vốn linh hoạt

Với phiên bản 2025.12, việc xử lý tỷ lệ cấp vốn động đã được điều chỉnh để hỗ trợ tỷ lệ cấp vốn động xuống khoảng thời gian cấp vốn 1 giờ.
Do đó, khung thời gian đánh dấu và tỷ lệ cấp vốn đã được thay đổi thành 1 giờ cho mỗi sàn giao dịch tương lai được hỗ trợ.

Vì khung thời gian cho cả nến đánh dấu và nếnfund_fee đã thay đổi (thường từ 8h thành 1h) - dữ liệu đã tải xuống sẽ phải được điều chỉnh hoặc tải xuống lại một phần.
Bạn có thể tải xuống lại mọi thứ (`freqtrade download-data […] --erase` - :warning: có thể mất nhiều thời gian) - hoặc tải xuống dữ liệu cập nhật một cách có chọn lọc.

### Chiến lược

Hầu hết các chiến lược không cần điều chỉnh để tiếp tục hoạt động như mong đợi - tuy nhiên, các chiến lược sử dụng `@informative("8h", Candle_type="funding_rate")` hoặc tương tự sẽ phải chuyển khung thời gian sang 1h.
Điều tương tự cũng đúng với `dp.get_pair_dataframe(metadata["pair"], "8h", Candle_type="funding_rate")` - cần phải chuyển sang 1h.

freqtrade sẽ tự động điều chỉnh khung thời gian và trả về `fund_rates` mặc dù khung thời gian được cung cấp sai. Nó sẽ đưa ra cảnh báo - và vẫn có thể phá vỡ chiến lược của bạn.

### Tải lại dữ liệu có chọn lọc

Tập lệnh bên dưới sẽ dùng làm ví dụ - bạn có thể cần điều chỉnh khung thời gian và trao đổi theo nhu cầu của mình!``` bash
# Cleanup no longer needed data
rm user_data/data/<exchange>/futures/*-mark*
rm user_data/data/<exchange>/futures/*-funding_rate*

# download new data (only required once to fix the mark and funding fee data)
freqtrade download-data -t 1h --trading-mode futures --candle-types funding_rate mark [...] --timerange <full timerange you've got other data for>

```Kết quả của việc trên sẽ là dữ liệu về tỷ lệ cấp vốn và đánh dấu của bạn sẽ có khung thời gian 1h.
bạn có thể xác minh điều này bằng `freqtrade list-data --exchange <yourexchange> --show`.

!!! Lưu ý "Đối số bổ sung"
    Các đối số bổ sung cho các lệnh trên có thể cần thiết, như tệp cấu hình hoặc user_data rõ ràng nếu chúng khác với giá trị mặc định.

**Siêu thanh khoản** hiện là trường hợp đặc biệt - sẽ không còn yêu cầu dữ liệu đánh dấu 1 giờ nữa - mà thay vào đó sẽ sử dụng nến thông thường (dữ liệu này chưa bao giờ tồn tại và giống hệt với nến tương lai 1 giờ). Vì chúng tôi không hỗ trợ dữ liệu tải xuống cho siêu thanh khoản (họ không cung cấp dữ liệu lịch sử) - nên sẽ không có hành động cần thiết nào đối với người dùng siêu thanh khoản.

## Mô hình Catboost ở tần số AI

Các mẫu CatBoost đã bị xóa khỏi phiên bản 2025.12 và không còn được hỗ trợ tích cực nữa.
Nếu hiện có các bot sử dụng mô hình CatBoost, bạn vẫn có thể sử dụng chúng trong các mô hình tùy chỉnh của mình bằng cách sao chép/dán chúng từ lịch sử git (như được liên kết bên dưới) và cài đặt thư viện CatBoost theo cách thủ công.
Tuy nhiên, chúng tôi khuyên bạn nên chuyển sang các thư viện mô hình được hỗ trợ khác như LightGBM hoặc XGBoost để được hỗ trợ tốt hơn và có khả năng tương thích trong tương lai.* [CatboostRegressor](https://github.com/freqtrade/freqtrade/blob/c6f3b0081927e161a16b116cc47fb663f7831d30/freqtrade/freqai/prediction_models/CatboostRegressor.py)
* [CatboostClassifier](https://github.com/freqtrade/freqtrade/blob/c6f3b0081927e161a16b116cc47fb663f7831d30/freqtrade/freqai/prediction_models/CatboostClassifier.py)
* [CatboostClassifierMultiTarget](https://github.com/freqtrade/freqtrade/blob/c6f3b0081927e161a16b116cc47fb663f7831d30/freqtrade/freqai/prediction_models/CatboostClassifierMultiTarget.py)
