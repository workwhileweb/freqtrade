<!-- Auto-translated from docs/ by script. Please review technical terms. -->

#Dữ liệu luồng đơn hàng

Hướng dẫn này hướng dẫn bạn cách sử dụng dữ liệu giao dịch công khai để phân tích luồng đơn hàng nâng cao trong Freqtrade.

!!! Cảnh báo "Tính năng thử nghiệm"    The orderflow feature is currently in beta and may be subject to changes in future releases. Please report any issues or feedback on the [Freqtrade GitHub repository](https://github.com/freqtrade/freqtrade/issues).
Hiện tại nó cũng chưa được thử nghiệm với freqAI - và việc kết hợp hai tính năng này được coi là nằm ngoài phạm vi tại thời điểm này.

!!! Cảnh báo "Hiệu suất"
    Luồng đặt hàng yêu cầu dữ liệu giao dịch thô. Dữ liệu này khá lớn và có thể khiến khởi động ban đầu chậm khi freqtrade cần tải xuống dữ liệu giao dịch cho nến X cuối cùng. Ngoài ra, việc bật tính năng này sẽ làm tăng mức sử dụng bộ nhớ. Hãy đảm bảo có đủ nguồn lực sẵn có.

## Bắt đầu

### Kích hoạt giao dịch công khai

Trong tệp `config.json` của bạn, hãy đặt tùy chọn `use_public_trades` thành true trong phần `exchange`.```json
"exchange": {
   ...
   "use_public_trades": true,
}
```### Định cấu hình Xử lý luồng đơn hàng

Xác định cài đặt mong muốn của bạn để xử lý luồng đơn hàng trong phần luồng đơn hàng của config.json. Tại đây, bạn có thể điều chỉnh các yếu tố như:

- `cache_size`: Có bao nhiêu nến luồng lệnh trước đó được lưu vào bộ đệm thay vì tính toán từng nến mới
- `max_candles`: Lọc số lượng nến bạn muốn nhận dữ liệu giao dịch.
- `scale`: Điều này kiểm soát kích thước thùng giá cho biểu đồ dấu chân.
- `stacked_imbalance_range`: Xác định các mức giá mất cân bằng liên tiếp tối thiểu cần thiết để xem xét.
- `imbalance_volume`: Lọc ra sự mất cân bằng với âm lượng dưới ngưỡng này.
- `imbalance_ratio`: Lọc ra sự mất cân bằng với tỷ lệ (chênh lệch giữa khối lượng yêu cầu và giá thầu) thấp hơn giá trị này.```json
"orderflow": {
    "cache_size": 1000, 
    "max_candles": 1500, 
    "scale": 0.5, 
    "stacked_imbalance_range": 3, //  needs at least this amount of imbalance next to each other
    "imbalance_volume": 1, //  filters out below
    "imbalance_ratio": 3 //  filters out ratio lower than
  },
```## Tải xuống dữ liệu giao dịch để kiểm tra lại

Để tải xuống dữ liệu giao dịch lịch sử để kiểm tra lại, hãy sử dụng cờ --dl-trades với lệnh freqtrade download-data.```bash
freqtrade download-data -p BTC/USDT:USDT --timerange 20230101- --trading-mode futures --timeframes 5m --dl-trades
```!!! Cảnh báo "Tính khả dụng của dữ liệu"
    Không phải tất cả các sàn giao dịch đều cung cấp dữ liệu giao dịch công khai. Đối với các sàn giao dịch được hỗ trợ, freqtrade sẽ cảnh báo bạn nếu không có dữ liệu giao dịch công khai nếu bạn bắt đầu tải xuống dữ liệu bằng cờ `--dl-trades`.

## Truy cập dữ liệu luồng đơn hàng

Sau khi được kích hoạt, một số cột mới sẽ có sẵn trong khung dữ liệu của bạn:``` python

dataframe["trades"] # Contains information about each individual trade.
dataframe["orderflow"] # Represents a footprint chart dict (see below)
dataframe["imbalances"] # Contains information about imbalances in the order flow.
dataframe["bid"] # Total bid volume 
dataframe["ask"] # Total ask volume
dataframe["delta"] # Difference between ask and bid volume.
dataframe["min_delta"] # Minimum delta within the candle
dataframe["max_delta"] # Maximum delta within the candle
dataframe["total_trades"] # Total number of trades
dataframe["stacked_imbalances_bid"] # List of price levels of stacked bid imbalance range beginnings
dataframe["stacked_imbalances_ask"] # List of price levels of stacked ask imbalance range beginnings
```You can access these columns in your strategy code for further analysis. Đây là một ví dụ:``` python
def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
    # Calculating cumulative delta
    dataframe["cum_delta"] = cumulative_delta(dataframe["delta"])
    # Accessing total trades
    total_trades = dataframe["total_trades"]
    ...

def cumulative_delta(delta: Series):
    cumdelta = delta.cumsum()
    return cumdelta

```### Biểu đồ dấu chân (`dataframe["orderflow"]`)

Cột này cung cấp thông tin phân tích chi tiết về các lệnh mua và bán ở các mức giá khác nhau, cung cấp những hiểu biết có giá trị về động lực của dòng lệnh. Tham số `scale` trong cấu hình của bạn xác định kích thước ngăn giá cho biểu diễn này

Cột `orderflow` chứa một lệnh có cấu trúc sau:``` output
{
    "price": {
        "bid_amount": 0.0,
        "ask_amount": 0.0,
        "bid": 0,
        "ask": 0,
        "delta": 0.0,
        "total_volume": 0.0,
        "total_trades": 0
    }
}
```#### Giải thích về cột Dòng lệnh

- key: Thùng giá - được đánh dấu theo khoảng `scale`
- `bid_amount`: Tổng khối lượng mua ở mỗi mức giá.
- `ask_amount`: Tổng khối lượng bán ra ở mỗi mức giá.
- `bid`: Số lượng lệnh mua ở mỗi mức giá.
- `ask`: Số lượng lệnh bán ở mỗi mức giá.
- `delta`: Chênh lệch giữa khối lượng hỏi và lượng đặt mua ở mỗi mức giá.
- `total_volume`: Tổng khối lượng (số tiền đặt mua + số tiền đặt mua) ở mỗi mức giá.
- `total_trades`: Tổng số giao dịch (ask + bid) ở mỗi mức giá.

Bằng cách tận dụng các tính năng này, bạn có thể có được những hiểu biết có giá trị về tâm lý thị trường và các cơ hội giao dịch tiềm năng dựa trên phân tích luồng đơn hàng.

### Dữ liệu giao dịch thô (`dataframe["trades"]`)

Liệt kê các giao dịch riêng lẻ xảy ra trong nến. Dữ liệu này có thể được sử dụng để phân tích chi tiết hơn về động lực của dòng lệnh.

Mỗi mục riêng lẻ chứa một lệnh với các phím sau:

- `timestamp`: Dấu thời gian của giao dịch.
- `date`: Ngày giao dịch.
- `price`: Giá của giao dịch.
- `số tiền`: Khối lượng giao dịch.
- `side`: Mua hoặc bán.
- `id`: Mã định danh duy nhất cho giao dịch.
- `cost`: Tổng chi phí giao dịch (giá * số tiền).

### Mất cân bằng (`dataframe["mất cân bằng"]`)

Cột này cung cấp thông tin về sự mất cân bằng trong luồng đơn hàng. Sự mất cân bằng xảy ra khi có sự khác biệt đáng kể giữa khối lượng yêu cầu và giá thầu ở một mức giá nhất định.

Mỗi hàng trông như sau - với giá là chỉ mục và các giá trị giá thầu và yêu cầu mất cân bằng tương ứng dưới dạng cột``` output
{
    "price": {
        "bid_imbalance": False,
        "ask_imbalance": False
    }
}
```