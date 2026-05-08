<!-- Auto-translated from docs/ by script. Please review technical terms. -->

# Freqtrade Strategies 101: Khởi đầu nhanh chóng để phát triển chiến lược

Với mục đích bắt đầu nhanh này, chúng tôi giả định rằng bạn đã quen với những kiến thức cơ bản về giao dịch và đã đọc phần 
Trang [Thông tin cơ bản về Freqtrade](bot-basics.md).

## Kiến thức bắt buộc

Chiến lược trong Freqtrade là một lớp Python xác định logic để mua và bán `tài sản` tiền điện tử.

Tài sản được định nghĩa là `cặp`, đại diện cho `coin` và `stake`. Đồng xu là tài sản bạn đang giao dịch bằng cách sử dụng loại tiền tệ khác làm tiền đặt cọc.

Dữ liệu được sàn giao dịch cung cấp dưới dạng `nến`, được tạo thành từ sáu giá trị: `ngày`, `mở`, `cao`, `thấp`, `đóng` và `khối lượng`.

Các hàm `phân tích kỹ thuật` phân tích dữ liệu nến bằng cách sử dụng các công thức tính toán và thống kê khác nhau, đồng thời tạo ra các giá trị phụ được gọi là `chỉ báo`.

Các chỉ báo được phân tích trên nến cặp tài sản để tạo ra `tín hiệu`.

Tín hiệu được chuyển thành `lệnh` trên một `trao đổi` tiền điện tử, tức là `giao dịch`.

Chúng tôi sử dụng thuật ngữ "vào" và "thoát" thay vì "mua" và "bán" vì Freqtrade hỗ trợ cả giao dịch "mua" và "bán".

- **dài**: Bạn mua xu dựa trên tiền đặt cược, ví dụ: mua đồng xu BTC bằng cách sử dụng USDT làm cổ phần của bạn và bạn kiếm được lợi nhuận bằng cách bán đồng xu với tỷ giá cao hơn mức bạn đã trả. Trong các giao dịch mua, lợi nhuận được tạo ra nhờ giá trị đồng xu tăng lên so với tiền đặt cược.
- **ngắn**: Bạn vay vốn từ sàn dưới dạng coin, sau đó bạn trả lại giá trị cổ phần của coin. Trong các giao dịch ngắn hạn, lợi nhuận được tạo ra bằng cách giá trị đồng xu giảm so với tiền đặt cược (bạn trả khoản vay với lãi suất thấp hơn).

Mặc dù Freqtrade hỗ trợ thị trường giao ngay và thị trường tương lai cho một số sàn giao dịch nhất định, nhưng để đơn giản, chúng tôi sẽ chỉ tập trung vào các giao dịch giao ngay (dài).

## Cấu trúc của một chiến lược cơ bản

### Khung dữ liệu chính

Chiến lược Freqtrade sử dụng cấu trúc dữ liệu dạng bảng với các hàng và cột được gọi là `khung dữ liệu` để tạo tín hiệu tham gia và thoát giao dịch.

Mỗi cặp trong danh sách cặp được định cấu hình của bạn có khung dữ liệu riêng. Các khung dữ liệu được lập chỉ mục theo cột `date`, ví dụ: `2024-06-31 12:00`.

5 cột tiếp theo biểu thị dữ liệu `open`, `high`, `low`, `close` và `volume` (OHLCV).

### Điền các giá trị chỉ báo

Hàm `populate_indicators` thêm các cột vào khung dữ liệu đại diện cho các giá trị chỉ báo phân tích kỹ thuật.

Ví dụ về các chỉ báo phổ biến bao gồm Chỉ số sức mạnh tương đối, Dải Bollinger, Chỉ số dòng tiền, Đường trung bình động và Phạm vi trung bình thực.

Các cột được thêm vào khung dữ liệu bằng cách gọi các hàm phân tích kỹ thuật, ví dụ: Hàm RSI của ta-lib `ta.RSI()` và gán chúng cho tên cột, ví dụ: `rsi````python
dataframe['rsi'] = ta.RSI(dataframe)
```??? Gợi ý "Thư viện phân tích kỹ thuật"
    Các thư viện khác nhau hoạt động theo những cách khác nhau để tạo ra các giá trị chỉ báo. Vui lòng kiểm tra tài liệu của từng thư viện để hiểu    how to integrate it into your strategy. You can also check the [Freqtrade example strategies](https://github.com/freqtrade/freqtrade-strategies) to give you ideas.
### Điền tín hiệu vào

Hàm `populate_entry_trend` xác định các điều kiện cho tín hiệu vào lệnh.

Cột khung dữ liệu `enter_long` được thêm vào khung dữ liệu và khi giá trị `1` có trong cột này, Freqtrade sẽ thấy tín hiệu vào.

??? Gợi ý "rút ngắn"
    Để thực hiện các giao dịch bán, hãy sử dụng cột `enter_short`.

### Điền tín hiệu thoát

Hàm `populate_exit_trend` xác định các điều kiện cho tín hiệu thoát.

Cột khung dữ liệu `exit_long` được thêm vào khung dữ liệu và khi giá trị `1` có trong cột này, Freqtrade sẽ thấy tín hiệu thoát.

??? Gợi ý "rút ngắn"
    Để thoát giao dịch bán, hãy sử dụng cột `exit_short`.

## Một chiến lược đơn giản

Đây là một ví dụ tối thiểu về chiến lược Freqtrade:```python
from freqtrade.strategy import IStrategy
from pandas import DataFrame
import talib.abstract as ta

class MyStrategy(IStrategy):

    timeframe = '15m'

    # set the initial stoploss to -10%
    stoploss = -0.10

    # exit profitable positions at any time when the profit is greater than 1%
    minimal_roi = {"0": 0.01}

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # generate values for technical analysis indicators
        dataframe['rsi'] = ta.RSI(dataframe, timeperiod=14)

        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # generate entry signals based on indicator values
        dataframe.loc[
            (dataframe['rsi'] < 30),
            'enter_long'] = 1

        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # generate exit signals based on indicator values
        dataframe.loc[
            (dataframe['rsi'] > 70),
            'exit_long'] = 1

        return dataframe
```## Thực hiện giao dịch

Khi tìm thấy tín hiệu (`1` trong cột vào hoặc ra), Freqtrade sẽ cố gắng thực hiện một lệnh, tức là `giao dịch` hoặc `vị trí`.

Mỗi vị thế giao dịch mới chiếm một `khe`. Vị trí đại diện cho số lượng giao dịch mới đồng thời tối đa có thể được mở.

Số lượng vị trí được xác định bởi tùy chọn `max_open_trades` [configuration](configuration.md).

Tuy nhiên, có thể có nhiều tình huống trong đó việc tạo tín hiệu không phải lúc nào cũng tạo ra lệnh giao dịch. Chúng bao gồm:

- không đủ số cổ phần còn lại để mua một tài sản hoặc số tiền trong ví của bạn để bán một tài sản (bao gồm mọi khoản phí)
- không còn đủ chỗ trống để mở giao dịch mới (số vị thế bạn mở bằng tùy chọn `max_open_trades`)
- đã có một giao dịch mở cho một cặp (Freqtrade không thể xếp chồng các vị trí - tuy nhiên nó có thể [điều chỉnh các vị trí hiện tại](strategy-callbacks.md# adjustment-trade-position))
- nếu tín hiệu vào và ra xuất hiện trên cùng một nến, chúng được coi là [va chạm](strategy-customization.md#colliding-signals) và sẽ không có lệnh nào được đưa ra
- chiến lược chủ động từ chối lệnh giao dịch do logic mà bạn chỉ định bằng cách sử dụng một trong các lệnh gọi lại [entry](strategy-callbacks.md#trade-entry-buy-order-confirmation) hoặc [exit](strategy-callbacks.md#trade-exit-sell-order-confirmation) có liên quan

Đọc qua tài liệu [tùy chỉnh chiến lược](strategy-customization.md) để biết thêm chi tiết.

## Kiểm tra lại và kiểm tra chuyển tiếp

Phát triển chiến lược có thể là một quá trình lâu dài và khó chịu, vì biến "bản năng" của con người thành một công cụ được điều khiển bằng máy tính.
Chiến lược ("algo") không phải lúc nào cũng đơn giản.

Do đó, một chiến lược cần được thử nghiệm để xác minh rằng nó sẽ hoạt động như dự định.

Freqtrade có hai chế độ thử nghiệm:

- **kiểm tra lại**: sử dụng dữ liệu lịch sử mà bạn [tải xuống từ một sàn giao dịch](data-download.md), kiểm tra lại là một cách nhanh chóng để đánh giá hiệu suất của một chiến lược. Tuy nhiên, có thể rất dễ làm sai lệch kết quả, do đó, một chiến lược sẽ có vẻ mang lại nhiều lợi nhuận hơn thực tế. Hãy kiểm tra [tài liệu backtesting](backtesting.md) để biết thêm thông tin.
- **chạy thử**: thường được gọi là _thử nghiệm chuyển tiếp_, các lần chạy thử sử dụng dữ liệu thời gian thực từ sàn giao dịch. Tuy nhiên, bất kỳ tín hiệu nào dẫn đến giao dịch đều được Freqtrade theo dõi như bình thường, nhưng không có bất kỳ giao dịch nào được mở trên chính sàn giao dịch. Thử nghiệm chuyển tiếp chạy trong thời gian thực, do đó, mặc dù mất nhiều thời gian hơn để nhận được kết quả nhưng đây là chỉ báo đáng tin cậy hơn nhiều về hiệu suất **tiềm năng** so với thử nghiệm ngược.

Chạy khô được bật bằng cách đặt `dry_run` thành true trong [configuration](configuration.md#using-dry-run-mode) của bạn.

!!! Cảnh báo "Backtests có thể rất không chính xác"
    Có nhiều lý do khiến kết quả backtest có thể không khớp với thực tế. Vui lòng kiểm tra tài liệu [kiểm tra lại các giả định](backtesting.md#assumptions-made-by-backtesting) và [các lỗi chiến lược phổ biến](strategy-customization.md#common-mistakes-when-developing-strategies).
    Một số trang web liệt kê và xếp hạng các chiến lược Freqtrade cho thấy kết quả backtest ấn tượng. Đừng cho rằng những kết quả này là có thể đạt được hoặc thực tế.

??? Gợi ý "Các lệnh hữu ích"
    Freqtrade bao gồm hai lệnh hữu ích để kiểm tra các sai sót cơ bản trong chiến lược: [lookahead-analysis](lookahead-analysis.md) và [recursive-analysis](recursive-analysis.md).

### Đánh giá kết quả chạy thử và chạy thử

Luôn chạy thử chiến lược của bạn sau khi kiểm tra lại chiến lược đó để xem liệu kết quả kiểm tra lại và chạy thử có đủ giống nhau hay không.Nếu có bất kỳ sự khác biệt đáng kể nào, hãy xác minh rằng tín hiệu vào và ra của bạn nhất quán và xuất hiện trên cùng một nến giữa hai chế độ. Tuy nhiên, sẽ luôn có sự khác biệt giữa chạy thử nghiệm và thử nghiệm ngược:

- Backtesting giả định tất cả các đơn đặt hàng được lấp đầy. Trong các đợt chạy thử, điều này có thể không xảy ra nếu sử dụng lệnh giới hạn hoặc không có khối lượng trên sàn giao dịch.
- Theo tín hiệu vào lệnh khi đóng nến, việc kiểm tra ngược giả định giao dịch được thực hiện ở mức giá mở của nến tiếp theo (trừ khi bạn có lệnh gọi lại giá tùy chỉnh trong chiến lược của mình). Trong các đợt chạy thử, thường có độ trễ giữa tín hiệu và thời điểm mở giao dịch.
  Điều này là do khi nến mới xuất hiện trên khung thời gian chính của bạn, ví dụ: cứ sau 5 phút, Freqtrade cần có thời gian để phân tích tất cả các khung dữ liệu cặp. Do đó, Freqtrade sẽ cố gắng mở giao dịch trong vài giây (lý tưởng nhất là độ trễ nhỏ nhất có thể)
  sau khi nến mở.
- Vì tỷ lệ đầu vào trong các lần chạy thử có thể không khớp với thử nghiệm ngược, điều này có nghĩa là việc tính toán lợi nhuận cũng sẽ khác. Do đó, điều bình thường là ROI, điểm dừng lỗ, điểm dừng lỗ cuối và điểm thoát lệnh gọi lại không giống nhau.
- Bạn càng có nhiều "độ trễ" tính toán giữa các ngọn nến mới xuất hiện và tín hiệu của bạn được nâng lên cũng như các giao dịch được mở sẽ dẫn đến mức giá khó dự đoán hơn. Đảm bảo máy tính của bạn đủ mạnh để xử lý dữ liệu cho số 
  số cặp bạn có trong danh sách cặp của mình trong một khoảng thời gian hợp lý. Freqtrade sẽ cảnh báo bạn trong nhật ký nếu có sự chậm trễ đáng kể trong quá trình xử lý dữ liệu.

## Kiểm soát hoặc giám sát bot đang chạy

Khi bot của bạn đang chạy ở chế độ khô hoặc trực tiếp, Freqtrade có sáu cơ chế để kiểm soát hoặc giám sát bot đang chạy:

- **[FreqUI](freq-ui.md)**: Dễ dàng nhất để bắt đầu, FreqUI là giao diện web để xem và kiểm soát hoạt động hiện tại của bot của bạn.
- **[Telegram](telegram-usage.md)**: Trên thiết bị di động, tích hợp Telegram có sẵn để nhận thông báo về hoạt động bot của bạn và kiểm soát các khía cạnh nhất định.- **[FTUI](https://github.com/freqtrade/ftui)**: FTUI is a terminal (command line) interface to Freqtrade, and allows monitoring of a running bot only.
- **[freqtrade-client](rest-api.md#standard-the-api)**: Triển khai REST API bằng python, giúp bạn dễ dàng thực hiện yêu cầu và sử dụng phản hồi của bot từ ứng dụng python hoặc dòng lệnh.
- **[Điểm cuối API REST](rest-api.md#available-endpoints)**: API REST cho phép lập trình viên phát triển các công cụ của riêng họ để tương tác với bot Freqtrade.
- **[Webhooks](webhook-config.md)**: Freqtrade có thể gửi thông tin đến các dịch vụ khác, ví dụ: discord, bởi webhooks.

### Nhật ký

Freqtrade tạo nhật ký gỡ lỗi mở rộng để giúp bạn hiểu điều gì đang xảy ra. Vui lòng tự làm quen với thông tin và thông báo lỗi mà bạn có thể thấy trong nhật ký bot của mình.

Việc ghi nhật ký theo mặc định xảy ra theo tiêu chuẩn (dòng lệnh). Thay vào đó, nếu bạn muốn ghi ra một tệp, nhiều lệnh freqtrade, bao gồm lệnh `trade`, hãy chấp nhận tùy chọn `--logfile` để ghi vào một tệp.

Hãy kiểm tra [FAQ](faq.md#how-do-i-search-the-bot-logs-for-something) để biết ví dụ.

## Suy nghĩ cuối cùng

Giao dịch thuật toán rất khó và hầu hết các chiến lược công khai đều không hoạt động tốt do thời gian và nỗ lực để làm cho một chiến lược hoạt động có lãi trong nhiều tình huống.

Do đó, việc thực hiện các chiến lược công khai và sử dụng backtests như một cách để đánh giá hiệu suất thường gặp nhiều vấn đề. Tuy nhiên, Freqtrade cung cấp những cách hữu ích để giúp bạn đưa ra quyết định và thực hiện thẩm định.

Có nhiều cách khác nhau để đạt được lợi nhuận và không có một mẹo, thủ thuật hoặc tùy chọn cấu hình nào có thể khắc phục được một chiến lược hoạt động kém.Freqtrade is an open source platform with a large and helpful community - make sure to visit our [discord channel](https://discord.gg/p7nuUNVfP7) to discuss your strategy with others!
Như mọi khi, chỉ đầu tư những gì bạn sẵn sàng mất.

## Kết luận

Phát triển chiến lược trong Freqtrade bao gồm việc xác định tín hiệu vào và ra dựa trên các chỉ báo kỹ thuật. Bằng cách làm theo cấu trúc và phương pháp được nêu ở trên, bạn có thể tạo và thử nghiệm các chiến lược giao dịch của riêng mình.

Các câu hỏi và câu trả lời phổ biến có sẵn trên [FAQ](faq.md) của chúng tôi.

Để tiếp tục, hãy tham khảo [Tài liệu tùy chỉnh chiến lược Freqtrade] (strategy-customization.md) chuyên sâu hơn.