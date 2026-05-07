<!-- Auto-translated from docs/ by script. Please review technical terms. -->

# Tùy chỉnh chiến lược

Trang này giải thích cách tùy chỉnh chiến lược của bạn, thêm chỉ báo mới và thiết lập quy tắc giao dịch.

Nếu bạn chưa có, hãy làm quen với:

- [Chiến lược Freqtrade 101](strategy-101.md), cung cấp sự khởi đầu nhanh chóng để phát triển chiến lược
- [Thông tin cơ bản về bot Freqtrade](bot-basics.md), cung cấp thông tin tổng thể về cách hoạt động của bot

## Phát triển chiến lược của riêng bạn

Bot bao gồm một tệp chiến lược mặc định.Also, several other strategies are available in the [strategy repository](https://github.com/freqtrade/freqtrade-strategies).
Tuy nhiên, rất có thể bạn sẽ có ý tưởng riêng cho một chiến lược.

Tài liệu này nhằm mục đích giúp bạn chuyển đổi ý tưởng của mình thành một chiến lược hiệu quả.

### Tạo mẫu chiến lược

Để bắt đầu, bạn có thể sử dụng lệnh:```bash
freqtrade new-strategy --strategy AwesomeStrategy
```Điều này sẽ tạo ra một chiến lược mới có tên là `AwesomeStrategy` từ một mẫu, chiến lược này sẽ được định vị bằng tên tệp `user_data/strategies/AwesomeStrategy.py`.

!!! Lưu ý
    Có sự khác biệt giữa *tên* của chiến lược và tên tệp. Trong hầu hết các lệnh, Freqtrade sử dụng *tên* của chiến lược, *không phải tên tệp*.

!!! Lưu ý
    Lệnh `chiến lược mới` tạo ra các ví dụ ban đầu sẽ không mang lại lợi nhuận ngay từ đầu.

??? Gợi ý "Các cấp độ mẫu khác nhau"
    `freqtrade new-strategy` có một tham số bổ sung, `--template`, tham số này kiểm soát lượng thông tin xây dựng trước mà bạn nhận được trong chiến lược đã tạo. Sử dụng `--template ở mức tối thiểu` để có được chiến lược trống mà không có bất kỳ ví dụ chỉ báo nào hoặc `--template nâng cao` để có được mẫu có các tính năng phức tạp hơn được xác định.

### Cấu trúc của một chiến lược

Tệp chiến lược chứa tất cả thông tin cần thiết để xây dựng logic chiến lược:

- Dữ liệu nến ở định dạng OHLCV
- Các chỉ số
- Logic đầu vào
  - Tín hiệu
- Thoát logic
  - Tín hiệu
  - ROI tối thiểu
  - Gọi lại ("chức năng tùy chỉnh")
- Dừng lỗ
  - Cố định/tuyệt đối
  - Trailing
  - Gọi lại ("chức năng tùy chỉnh")
- Giá cả [tùy chọn]
- Điều chỉnh vị trí [tùy chọn]

Bot này bao gồm một chiến lược mẫu có tên là `SampleStrategy` mà bạn có thể sử dụng làm cơ sở: `user_data/strategies/sample_strategy.py`.
Bạn có thể kiểm tra nó bằng tham số: `--strategy SampleStrategy`. Hãy nhớ rằng bạn sử dụng tên lớp chiến lược chứ không phải tên tệp.

Ngoài ra, còn có một thuộc tính tên là `INTERFACE_VERSION`, xác định phiên bản giao diện chiến lược mà bot nên sử dụng.
Phiên bản hiện tại là 3 - đây cũng là phiên bản mặc định khi nó không được đặt rõ ràng trong chiến lược.

Bạn có thể thấy các chiến lược cũ hơn được đặt thành giao diện phiên bản 2 và những chiến lược này sẽ cần được cập nhật thành thuật ngữ v3 vì các phiên bản trong tương lai sẽ yêu cầu phải đặt điều này.

Việc khởi động bot ở chế độ khô hoặc trực tiếp được thực hiện bằng lệnh `trade`:```bash
freqtrade trade --strategy AwesomeStrategy
```### Chế độ bot

Chiến lược Freqtrade có thể được bot Freqtrade xử lý ở 5 chế độ chính:

- kiểm tra lại
- siêu thích
- khô ("thử nghiệm chuyển tiếp")
- sống
- FreqAI (không được đề cập ở đây)

Kiểm tra [tài liệu cấu hình](configuration.md) về cách đặt bot ở chế độ khô hoặc trực tiếp.

**Luôn sử dụng chế độ khô khi thử nghiệm vì điều này cho bạn ý tưởng về cách chiến lược của bạn sẽ hoạt động trong thực tế mà không gặp rủi ro về vốn.**

## Đi sâu hơn**For the following section we will use the [user_data/strategies/sample_strategy.py](https://github.com/freqtrade/freqtrade/blob/develop/freqtrade/templates/sample_strategy.py)
tập tin làm tài liệu tham khảo.**

!!! Lưu ý "Chiến lược và kiểm tra lại"
    Để tránh các sự cố và sự khác biệt không mong muốn giữa chế độ kiểm tra lại và chế độ khô/sống, vui lòng lưu ý
    rằng trong quá trình kiểm tra ngược, phạm vi toàn thời gian sẽ được chuyển đến các phương thức `populate_*()` cùng một lúc.
    Do đó, tốt nhất nên sử dụng các phép toán được vector hóa (trên toàn bộ khung dữ liệu, không phải vòng lặp) và
    tránh tham chiếu chỉ mục (`df.iloc[-1]`), mà thay vào đó hãy sử dụng `df.shift()` để đến nến trước đó.

!!! Cảnh báo "Cảnh báo: Sử dụng dữ liệu trong tương lai"
    Vì việc kiểm tra ngược vượt qua toàn bộ phạm vi thời gian cho các phương thức `populate_*()` nên tác giả chiến lược
    cần phải cẩn thận để tránh chiến lược sử dụng dữ liệu từ tương lai.
    Một số mẫu phổ biến cho vấn đề này được liệt kê trong phần [Những sai lầm thường gặp](#common-mistakes-when-development-strategies) của tài liệu này.

??? Gợi ý "Phân tích nhìn trước và đệ quy"
    Freqtrade bao gồm hai lệnh hữu ích để giúp đánh giá tầm nhìn chung (sử dụng dữ liệu trong tương lai) và
    các vấn đề về sai lệch đệ quy (phương sai trong các giá trị chỉ báo). Trước khi thực hiện một chiến lược khô khan hoặc sống lâu hơn,
    bạn nên luôn luôn sử dụng các lệnh này trước tiên. Vui lòng kiểm tra các tài liệu liên quan để biết
    Phân tích [lookahead](lookahead-analysis.md) và [recursive](recursive-analysis.md).

### Khung dữ liệuFreqtrade uses [pandas](https://pandas.pydata.org/) to store/provide the candlestick (OHLCV) data.
Pandas là một thư viện tuyệt vời được phát triển để xử lý lượng lớn dữ liệu ở định dạng bảng.

Mỗi hàng trong khung dữ liệu tương ứng với một cây nến trên biểu đồ, trong đó cây nến hoàn chỉnh mới nhất luôn là cây nến cuối cùng trong khung dữ liệu (được sắp xếp theo ngày).

Nếu chúng ta nhìn vào một vài hàng đầu tiên của khung dữ liệu chính bằng hàm `head()` của gấu trúc, chúng ta sẽ thấy:```output
> dataframe.head()
                       date      open      high       low     close     volume
0 2021-11-09 23:25:00+00:00  67279.67  67321.84  67255.01  67300.97   44.62253
1 2021-11-09 23:30:00+00:00  67300.97  67301.34  67183.03  67187.01   61.38076
2 2021-11-09 23:35:00+00:00  67187.02  67187.02  67031.93  67123.81  113.42728
3 2021-11-09 23:40:00+00:00  67123.80  67222.40  67080.33  67160.48   78.96008
4 2021-11-09 23:45:00+00:00  67160.48  67160.48  66901.26  66943.37  111.39292
```Khung dữ liệu là một bảng trong đó các cột không phải là các giá trị đơn lẻ mà là một chuỗi các giá trị dữ liệu. Như vậy, những so sánh python đơn giản như sau sẽ không hoạt động:``` python
    if dataframe['rsi'] > 30:
        dataframe['enter_long'] = 1
```Phần trên sẽ thất bại với `Giá trị thực của Chuỗi không rõ ràng […]`.

Thay vào đó, điều này phải được viết theo cách tương thích với gấu trúc, để thao tác được thực hiện trên toàn bộ khung dữ liệu, tức là `vectorisation`.``` python
    dataframe.loc[
        (dataframe['rsi'] > 30)
    , 'enter_long'] = 1
```Với phần này, bạn có một cột mới trong khung dữ liệu của mình, cột này được gán `1` bất cứ khi nào RSI trên 30.

Freqtrade sử dụng cột mới này làm tín hiệu vào lệnh, trong đó người ta giả định rằng giao dịch sau đó sẽ mở ở nến mở tiếp theo.

Pandas cung cấp các cách nhanh chóng để tính toán số liệu, tức là "vector hóa". Để hưởng lợi từ tốc độ này, bạn không nên sử dụng vòng lặp mà thay vào đó hãy sử dụng các phương pháp vector hóa.

Các thao tác được vector hóa thực hiện các phép tính trên toàn bộ phạm vi dữ liệu và do đó, so với việc lặp qua từng hàng, sẽ nhanh hơn rất nhiều khi tính toán các chỉ báo.

??? Gợi ý "Tín hiệu vs Giao dịch"
    - Tín hiệu được tạo ra từ các chỉ báo khi đóng nến và là ý định tham gia giao dịch.
    - Giao dịch là các lệnh được thực hiện (trên sàn giao dịch ở chế độ trực tiếp), trong đó giao dịch sẽ mở càng gần thời điểm mở nến tiếp theo càng tốt.

!!! Cảnh báo "Giả định lệnh giao dịch"
    Trong backtesting, tín hiệu được tạo ra khi đóng nến. Giao dịch sau đó được bắt đầu ngay lập tức vào lần mở nến tiếp theo.

    Trong trường hợp khô và trực tiếp, việc này có thể bị trì hoãn do tất cả các khung dữ liệu cặp cần được phân tích trước, sau đó mới xử lý giao dịch 
    đối với mỗi cặp đó xảy ra. Điều này có nghĩa là trong dry/live bạn cần lưu ý đến việc tính toán càng thấp 
    trì hoãn càng tốt, thường bằng cách chạy số lượng cặp thấp và có CPU có tốc độ xung nhịp tốt.

####Tại sao tôi không thể xem dữ liệu nến "thời gian thực"?

Freqtrade không lưu trữ nến chưa hoàn thiện/chưa hoàn thành trong khung dữ liệu.

Việc sử dụng dữ liệu không đầy đủ để đưa ra quyết định chiến lược được gọi là "sửa lại" và bạn có thể thấy các nền tảng khác cho phép điều này.

Freqtrade thì không. Chỉ có dữ liệu nến hoàn chỉnh/hoàn thành mới có sẵn trong khung dữ liệu.

### Tùy chỉnh các chỉ số

Tín hiệu vào và ra cần có chỉ báo. Bạn có thể thêm nhiều chỉ báo hơn bằng cách mở rộng danh sách có trong phương thức `populate_indicators()` từ tệp chiến lược của bạn.

Bạn chỉ nên thêm các chỉ báo được sử dụng trong `populate_entry_trend()`, `populate_exit_trend()` hoặc để điền một chỉ báo khác, nếu không hiệu suất có thể bị ảnh hưởng.

Điều quan trọng là luôn trả về khung dữ liệu từ ba hàm này mà không xóa/sửa đổi các cột `"mở", "cao", "thấp", "đóng", "âm lượng"`, nếu không các trường này sẽ chứa nội dung không mong muốn.

Vật mẫu:```python
def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
    """
    Adds several different TA indicators to the given DataFrame

    Performance Note: For the best performance be frugal on the number of indicators
    you are using. Let uncomment only the indicator you are using in your strategies
    or your hyperopt configuration, otherwise you will waste your memory and CPU usage.
    :param dataframe: Dataframe with data from the exchange
    :param metadata: Additional information, like the currently traded pair
    :return: a Dataframe with all mandatory indicators for the strategies
    """
    dataframe['sar'] = ta.SAR(dataframe)
    dataframe['adx'] = ta.ADX(dataframe)
    stoch = ta.STOCHF(dataframe)
    dataframe['fastd'] = stoch['fastd']
    dataframe['fastk'] = stoch['fastk']
    dataframe['bb_lower'] = ta.BBANDS(dataframe, nbdevup=2, nbdevdn=2)['lowerband']
    dataframe['sma'] = ta.SMA(dataframe, timeperiod=40)
    dataframe['tema'] = ta.TEMA(dataframe, timeperiod=9)
    dataframe['mfi'] = ta.MFI(dataframe)
    dataframe['rsi'] = ta.RSI(dataframe)
    dataframe['ema5'] = ta.EMA(dataframe, timeperiod=5)
    dataframe['ema10'] = ta.EMA(dataframe, timeperiod=10)
    dataframe['ema50'] = ta.EMA(dataframe, timeperiod=50)
    dataframe['ema100'] = ta.EMA(dataframe, timeperiod=100)
    dataframe['ao'] = awesome_oscillator(dataframe)
    macd = ta.MACD(dataframe)
    dataframe['macd'] = macd['macd']
    dataframe['macdsignal'] = macd['macdsignal']
    dataframe['macdhist'] = macd['macdhist']
    hilbert = ta.HT_SINE(dataframe)
    dataframe['htsine'] = hilbert['sine']
    dataframe['htleadsine'] = hilbert['leadsine']
    dataframe['plus_dm'] = ta.PLUS_DM(dataframe)
    dataframe['plus_di'] = ta.PLUS_DI(dataframe)
    dataframe['minus_dm'] = ta.MINUS_DM(dataframe)
    dataframe['minus_di'] = ta.MINUS_DI(dataframe)

    # remember to always return the dataframe
    return dataframe
```!!! Lưu ý "Muốn có thêm ví dụ về chỉ báo?"    Look into the [user_data/strategies/sample_strategy.py](https://github.com/freqtrade/freqtrade/blob/develop/freqtrade/templates/sample_strategy.py).
Sau đó bỏ ghi chú các chỉ số bạn cần.

#### Thư viện chỉ báo

Ngay lập tức, freqtrade cài đặt các thư viện kỹ thuật sau:- [ta-lib](https://ta-lib.github.io/ta-lib-python/)
- [pandas-ta](https://twopirllc.github.io/pandas-ta/)
- [technical](https://technical.freqtrade.io)
Các thư viện kỹ thuật bổ sung có thể được cài đặt khi cần thiết hoặc các chỉ báo tùy chỉnh có thể được tác giả chiến lược viết/phát minh ra.

### Giai đoạn khởi động chiến lược

Một số chỉ báo có giai đoạn khởi động không ổn định, trong đó không có đủ dữ liệu nến để tính bất kỳ giá trị nào (NaN) hoặc phép tính không chính xác. Điều này có thể dẫn đến sự không nhất quán, vì Freqtrade không biết khoảng thời gian không ổn định này kéo dài bao lâu và sử dụng bất kỳ giá trị chỉ báo nào có trong khung dữ liệu.

Để giải quyết vấn đề này, chiến lược có thể được chỉ định thuộc tính `startup_candle_count`.

Điều này nên được đặt thành số lượng nến tối đa mà chiến lược yêu cầu để tính toán các chỉ số ổn định. Trong trường hợp người dùng bao gồm các khung thời gian cao hơn với các cặp thông tin, `startup_candle_count` không nhất thiết phải thay đổi. Giá trị là khoảng thời gian tối đa (tính bằng nến) mà bất kỳ khung thời gian cung cấp thông tin nào cũng cần để tính toán các chỉ báo ổn định.

Bạn có thể sử dụng [recursive-analysis](recursive-analysis.md) để kiểm tra và tìm `startup_candle_count` chính xác sẽ được sử dụng. Khi phân tích đệ quy cho thấy phương sai là 0% thì bạn có thể chắc chắn rằng mình có đủ dữ liệu nến khởi động.

Trong chiến lược ví dụ này, giá trị này phải được đặt thành 400 (`startup_candle_count = 400`), vì lịch sử cần thiết tối thiểu để tính toán ema100 nhằm đảm bảo giá trị chính xác là 400 nến.``` python
    dataframe['ema100'] = ta.EMA(dataframe, timeperiod=100)
```Bằng cách cho bot biết lượng lịch sử cần thiết, các giao dịch backtest có thể bắt đầu ở khoảng thời gian được chỉ định trong quá trình backtesting và hyperopt.

!!! Cảnh báo "Sử dụng x cuộc gọi để nhận OHLCV"
    Nếu bạn nhận được cảnh báo như `CẢNH BÁO - Sử dụng 3 cuộc gọi để nhận OHLCV. Điều này có thể khiến bot hoạt động chậm hơn. Vui lòng kiểm tra xem bạn có thực sự cần 1500 cây nến cho chiến lược của mình không` - bạn nên cân nhắc xem liệu bạn có thực sự cần nhiều dữ liệu lịch sử này cho tín hiệu của mình hay không.
    Việc có điều này sẽ khiến Freqtrade thực hiện nhiều cuộc gọi cho cùng một cặp, điều này rõ ràng sẽ chậm hơn một yêu cầu mạng.
    Do đó, Freqtrade sẽ mất nhiều thời gian hơn để làm mới nến - và do đó nên tránh nếu có thể.
    Điều này được giới hạn ở tổng số 5 cuộc gọi để tránh làm quá tải sàn giao dịch hoặc khiến freqtrade trở nên quá chậm.

!!! Cảnh báo
    `startup_candle_count` phải ở dưới `ohlcv_candle_limit * 5` (là 500 * 5 đối với hầu hết các sàn giao dịch) - vì chỉ số lượng nến này mới có sẵn trong các hoạt động Giao dịch Dry-Run/Live.

#### Ví dụ

Hãy thử kiểm tra lại 5 triệu nến trong 1 tháng (tháng 1 năm 2019) bằng cách sử dụng chiến lược mẫu với EMA100, như trên.``` bash
freqtrade backtesting --timerange 20190101-20190201 --timeframe 5m
```Giả sử `startup_candle_count` được đặt thành 400, quá trình kiểm tra lại biết rằng cần 400 nến để tạo tín hiệu vào lệnh hợp lệ. Nó sẽ tải dữ liệu từ `20190101 - (400 * 5m)` - tức là ~2018-12-30 11:40:00.

Nếu dữ liệu này có sẵn, các chỉ số sẽ được tính toán với phạm vi thời gian mở rộng này. Giai đoạn khởi động không ổn định (đến 2019-01-01 00:00:00) sau đó sẽ bị xóa trước khi tiến hành kiểm tra lại.

!!! Lưu ý "Dữ liệu nến khởi động không có sẵn"
    Nếu dữ liệu cho giai đoạn khởi động không có sẵn thì khoảng thời gian sẽ được điều chỉnh để tính cho giai đoạn khởi động này. Trong ví dụ của chúng tôi, quá trình kiểm tra lại sẽ bắt đầu từ 02/01/2019 09:20:00.

### Quy tắc tín hiệu vào lệnh

Chỉnh sửa phương thức `populate_entry_trend()` trong tệp chiến lược của bạn để cập nhật chiến lược vào lệnh của bạn.

Điều quan trọng là luôn trả về khung dữ liệu mà không xóa/sửa đổi các cột `"mở", "cao", "thấp", "đóng", "âm lượng"`, nếu không các trường này sẽ chứa nội dung không mong muốn. Chiến lược sau đó có thể tạo ra các giá trị không hợp lệ hoặc ngừng hoạt động hoàn toàn.

Phương thức này cũng sẽ xác định một cột mới, `"enter_long"` ("enter_short"` cho quần short), cần chứa `1` cho các mục nhập và `0` cho "không có hành động". `enter_long` là cột bắt buộc phải được đặt ngay cả khi chiến lược chỉ bán khống.

Bạn có thể đặt tên cho các tín hiệu vào lệnh bằng cách sử dụng cột `"enter_tag"`, cột này có thể giúp gỡ lỗi và đánh giá chiến lược của bạn sau này.

Mẫu từ `user_data/strategies/sample_strategy.py`:```python
def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
    """
    Based on TA indicators, populates the buy signal for the given dataframe
    :param dataframe: DataFrame populated with indicators
    :param metadata: Additional information, like the currently traded pair
    :return: DataFrame with buy column
    """
    dataframe.loc[
        (
            (qtpylib.crossed_above(dataframe['rsi'], 30)) &  # Signal: RSI crosses above 30
            (dataframe['tema'] <= dataframe['bb_middleband']) &  # Guard
            (dataframe['tema'] > dataframe['tema'].shift(1)) &  # Guard
            (dataframe['volume'] > 0)  # Make sure Volume is not 0
        ),
        ['enter_long', 'enter_tag']] = (1, 'rsi_cross')

    return dataframe
```??? Lưu ý "Nhập giao dịch bán"
    Các mục nhập ngắn có thể được tạo bằng cách cài đặt `enter_short` (tương ứng với `enter_long` cho các giao dịch dài hạn).
    Cột `enter_tag` vẫn giữ nguyên.
    Việc bán khống cần được hỗ trợ bởi sàn giao dịch và cấu hình thị trường của bạn!
    Ngoài ra, hãy đảm bảo bạn đặt [`can_short`](#can-short) một cách thích hợp cho chiến lược của mình nếu bạn có ý định bán khống.```python
    # allow both long and short trades
    can_short = True

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                (qtpylib.crossed_above(dataframe['rsi'], 30)) &  # Signal: RSI crosses above 30
                (dataframe['tema'] <= dataframe['bb_middleband']) &  # Guard
                (dataframe['tema'] > dataframe['tema'].shift(1)) &  # Guard
                (dataframe['volume'] > 0)  # Make sure Volume is not 0
            ),
            ['enter_long', 'enter_tag']] = (1, 'rsi_cross')

        dataframe.loc[
            (
                (qtpylib.crossed_below(dataframe['rsi'], 70)) &  # Signal: RSI crosses below 70
                (dataframe['tema'] > dataframe['bb_middleband']) &  # Guard
                (dataframe['tema'] < dataframe['tema'].shift(1)) &  # Guard
                (dataframe['volume'] > 0)  # Make sure Volume is not 0
            ),
            ['enter_short', 'enter_tag']] = (1, 'rsi_cross')

        return dataframe
    ```!!! Lưu ý
    Việc mua yêu cầu người bán phải mua. Do đó, khối lượng cần phải > 0 (`dataframe['volume'] > 0`) để đảm bảo rằng bot không mua/bán trong khoảng thời gian không hoạt động.

### Quy tắc tín hiệu thoát

Chỉnh sửa phương thức `populate_exit_trend()` vào tệp chiến lược của bạn để cập nhật chiến lược thoát.

Tín hiệu thoát có thể bị chặn bằng cách đặt `use_exit_signal` thành sai trong cấu hình hoặc chiến lược.

`use_exit_signal` sẽ không ảnh hưởng đến [quy tắc xung đột tín hiệu](#colliding-signals) - quy tắc này vẫn sẽ áp dụng và có thể ngăn các mục nhập.

Điều quan trọng là luôn trả về khung dữ liệu mà không xóa/sửa đổi các cột `"mở", "cao", "thấp", "đóng", "âm lượng"`, nếu không các trường này sẽ chứa nội dung không mong muốn. Chiến lược sau đó có thể tạo ra các giá trị không hợp lệ hoặc ngừng hoạt động hoàn toàn.

Phương thức này cũng sẽ xác định một cột mới, `"exit_long"` (`"exit_short"` cho quần short), cần chứa `1` cho lần thoát và `0` cho "không có hành động".

Bạn có thể đặt tên cho các tín hiệu thoát bằng cách sử dụng cột `"exit_tag"`. Cột này có thể giúp gỡ lỗi và đánh giá chiến lược của bạn sau này.

Mẫu từ `user_data/strategies/sample_strategy.py`:```python
def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
    """
    Based on TA indicators, populates the exit signal for the given dataframe
    :param dataframe: DataFrame populated with indicators
    :param metadata: Additional information, like the currently traded pair
    :return: DataFrame with buy column
    """
    dataframe.loc[
        (
            (qtpylib.crossed_above(dataframe['rsi'], 70)) &  # Signal: RSI crosses above 70
            (dataframe['tema'] > dataframe['bb_middleband']) &  # Guard
            (dataframe['tema'] < dataframe['tema'].shift(1)) &  # Guard
            (dataframe['volume'] > 0)  # Make sure Volume is not 0
        ),
        ['exit_long', 'exit_tag']] = (1, 'rsi_too_high')
    return dataframe
```??? Lưu ý "Thoát giao dịch bán"
    Bạn có thể tạo các lần thoát ngắn bằng cách đặt `exit_short` (tương ứng với `exit_long`).
    Cột `exit_tag` vẫn giữ nguyên.
    Việc bán khống cần được hỗ trợ bởi sàn giao dịch và cấu hình thị trường của bạn!
    Ngoài ra, hãy đảm bảo bạn đặt [`can_short`](#can-short) một cách thích hợp cho chiến lược của mình nếu bạn có ý định bán khống.```python
    # allow both long and short trades
    can_short = True

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                (qtpylib.crossed_above(dataframe['rsi'], 70)) &  # Signal: RSI crosses above 70
                (dataframe['tema'] > dataframe['bb_middleband']) &  # Guard
                (dataframe['tema'] < dataframe['tema'].shift(1)) &  # Guard
                (dataframe['volume'] > 0)  # Make sure Volume is not 0
            ),
            ['exit_long', 'exit_tag']] = (1, 'rsi_too_high')
        dataframe.loc[
            (
                (qtpylib.crossed_below(dataframe['rsi'], 30)) &  # Signal: RSI crosses below 30
                (dataframe['tema'] < dataframe['bb_middleband']) &  # Guard
                (dataframe['tema'] > dataframe['tema'].shift(1)) &  # Guard
                (dataframe['volume'] > 0)  # Make sure Volume is not 0
            ),
            ['exit_short', 'exit_tag']] = (1, 'rsi_too_low')
        return dataframe
    ```### ROI tối thiểu

Biến chiến lược `minimal_roi` xác định Lợi tức đầu tư (ROI) tối thiểu mà một giao dịch phải đạt được trước khi thoát, không phụ thuộc vào tín hiệu thoát.

Nó có định dạng sau, tức là một con trăn `dict`, với khóa dict (phía bên trái của dấu hai chấm) là số phút đã trôi qua kể từ khi giao dịch được mở và giá trị (phía bên phải của dấu hai chấm) là tỷ lệ phần trăm.```python
minimal_roi = {
    "40": 0.0,
    "30": 0.01,
    "20": 0.02,
    "0": 0.04
}
```Do đó, cấu hình trên có nghĩa là:

- Thoát khi đạt được lợi nhuận 4%
- Thoát khi đạt lợi nhuận 2% (có hiệu lực sau 20 phút)
- Thoát khi đạt lợi nhuận 1% (có hiệu lực sau 30 phút)
- Thoát khi giao dịch không thua lỗ (có hiệu lực sau 40 phút)

Việc tính toán bao gồm phí.

#### Vô hiệu hóa ROI tối thiểu

Để tắt hoàn toàn ROI, hãy đặt nó vào một từ điển trống:```python
minimal_roi = {}
```#### Sử dụng tính toán với ROI tối thiểu

Để sử dụng thời gian dựa trên thời lượng nến (khung thời gian), đoạn mã sau có thể hữu ích.

Điều này sẽ cho phép bạn thay đổi khung thời gian cho chiến lược nhưng thời gian ROI tối thiểu sẽ vẫn được đặt dưới dạng nến, ví dụ: sau 3 ngọn nến.``` python
from freqtrade.exchange import timeframe_to_minutes

class AwesomeStrategy(IStrategy):

    timeframe = "1d"
    timeframe_mins = timeframe_to_minutes(timeframe)
    minimal_roi = {
        "0": 0.05,                      # 5% for the first 3 candles
        str(timeframe_mins * 3): 0.02,  # 2% after 3 candles
        str(timeframe_mins * 6): 0.01,  # 1% After 6 candles
    }
```??? info "Các đơn hàng không được thực hiện ngay lập tức"
    `minimal_roi` sẽ lấy `trade.open_date` làm tham chiếu, đó là thời điểm giao dịch được bắt đầu, tức là khi lệnh đầu tiên cho giao dịch này được đặt.
    Điều này cũng đúng đối với các lệnh giới hạn không được thực hiện ngay lập tức (thường kết hợp với giá "giao ngay" thông qua `custom_entry_price()`), cũng như đối với các trường hợp giá đặt hàng ban đầu được thay thế thông qua `just_entry_price()`.
    Thời gian được sử dụng sẽ vẫn tính từ `trade.open_date` ban đầu (khi đơn hàng ban đầu được đặt lần đầu tiên), không phải từ ngày đặt hàng mới được đặt hoặc điều chỉnh.

### Dừng lỗ

Bạn nên đặt mức dừng lỗ để bảo vệ vốn của mình khỏi những biến động mạnh chống lại bạn.

Mẫu thiết lập mức dừng lỗ 10%:``` python
stoploss = -0.10
```Để có tài liệu đầy đủ về các tính năng dừng lỗ, hãy xem [trang dừng lỗ] (stoploss.md).

### Khung thời gian

Đây là tính chu kỳ của nến mà bot nên sử dụng trong chiến lược.

Các giá trị phổ biến là `"1m"`, `"5m"`, `"15m"`, `"1h"`, tuy nhiên tất cả các giá trị được trao đổi của bạn hỗ trợ sẽ hoạt động.

Xin lưu ý rằng các tín hiệu vào/ra giống nhau có thể hoạt động tốt với một khung thời gian nhưng không hoạt động tốt với các khung thời gian khác.

Cài đặt này có thể truy cập được trong các phương thức chiến lược dưới dạng thuộc tính `self.timeframe`.

### Có thể rút ngắn

Để sử dụng tín hiệu bán trên thị trường tương lai, bạn sẽ phải đặt `can_short = True`.

Các chiến lược cho phép điều này sẽ không được áp dụng trên thị trường giao ngay.

Nếu bạn có các giá trị `1` trong cột `enter_short` để đưa ra các tín hiệu bán, thì việc đặt `can_short = False` (là giá trị mặc định) sẽ có nghĩa là các tín hiệu bán này bị bỏ qua, ngay cả khi bạn đã chỉ định thị trường tương lai trong cấu hình của mình.

### Lệnh siêu dữ liệu

Lệnh `siêu dữ liệu` (có sẵn cho `populate_entry_trend`, `populate_exit_trend`, `populate_indicators`) chứa thông tin bổ sung.
Hiện tại đây là `cặp`, có thể được truy cập bằng cách sử dụng `siêu dữ liệu['pair']` và sẽ trả về một cặp ở định dạng `XRP/BTC` (hoặc `XRP/BTC:BTC` cho thị trường tương lai).

Không nên sửa đổi chính tả siêu dữ liệu và không lưu giữ thông tin trên nhiều chức năng trong chiến lược của bạn.

Thay vào đó, vui lòng kiểm tra phần [Lưu trữ thông tin](strategy-advanced.md#storing-information-persistent).

--8<-- "bao gồm/strategy-imports.md"

## Đang tải tệp chiến lược

Theo mặc định, freqtrade sẽ cố gắng tải các chiến lược từ tất cả các tệp `.py` trong `userdir` (mặc định `user_data/strategies`).

Giả sử chiến lược của bạn có tên là `AwesomeStrategy`, được lưu trữ trong tệp `user_data/strategies/AwesomeStrategy.py`, thì bạn có thể bắt đầu giao dịch freqtrade ở chế độ khô (hoặc trực tiếp, tùy thuộc vào cấu hình của bạn) với:```bash
freqtrade trade --strategy AwesomeStrategy
```Lưu ý rằng chúng tôi đang sử dụng tên lớp chứ không phải tên tệp.

Bạn có thể sử dụng `freqtrade list-strategies` để xem danh sách tất cả các chiến lược mà Freqtrade có thể tải (tất cả các chiến lược trong thư mục chính xác).
Nó cũng sẽ bao gồm trường "trạng thái", nêu bật các vấn đề tiềm ẩn.

??? Gợi ý "Tùy chỉnh thư mục chiến lược"
    Bạn có thể sử dụng một thư mục khác bằng cách sử dụng `--strategy-path user_data/otherPath`. Tham số này có sẵn cho tất cả các lệnh yêu cầu chiến lược.

## Cặp thông tin

### Nhận dữ liệu về các cặp không thể giao dịch

Dữ liệu về các cặp thông tin bổ sung (cặp tham chiếu) có thể có lợi cho một số chiến lược để xem dữ liệu trên khung thời gian rộng hơn.

Dữ liệu OHLCV cho các cặp này sẽ được tải xuống như một phần của quy trình làm mới danh sách trắng thông thường và có sẵn thông qua `DataProvider` giống như các cặp khác (xem bên dưới).

Các cặp này sẽ **không** được giao dịch trừ khi chúng cũng được chỉ định trong danh sách trắng cặp hoặc đã được chọn bởi Danh sách trắng động, ví dụ: `Danh sách cặp âm lượng`.

Các cặp cần được chỉ định dưới dạng bộ dữ liệu ở định dạng `("cặp", "khung thời gian")`, với cặp là đối số đầu tiên và khung thời gian là đối số thứ hai.

Vật mẫu:``` python
def informative_pairs(self):
    return [("ETH/USDT", "5m"),
            ("BTC/TUSD", "15m"),
            ]
```Bạn có thể tìm thấy mẫu đầy đủ [trong phần DataProvider](#complete-dataprovider-sample).

!!! Cảnh báo
    Vì các cặp này sẽ được làm mới như một phần của quá trình làm mới danh sách trắng thường xuyên, nên tốt nhất bạn nên giữ danh sách này ngắn gọn.
    Tất cả các khung thời gian và tất cả các cặp đều có thể được chỉ định miễn là chúng có sẵn (và đang hoạt động) trên sàn giao dịch đã sử dụng.
    Tuy nhiên, tốt hơn là sử dụng việc lấy mẫu lại cho các khung thời gian dài hơn bất cứ khi nào có thể
    để tránh cản trở việc trao đổi với quá nhiều yêu cầu và có nguy cơ bị chặn.

??? Lưu ý "Các loại nến thay thế"
    Informative_pairs cũng có thể cung cấp phần tử bộ thứ 3 xác định rõ ràng loại nến.
    Sự sẵn có của các loại nến thay thế sẽ phụ thuộc vào chế độ giao dịch và sàn giao dịch.
    Nói chung, các cặp giao ngay không thể được sử dụng trong thị trường tương lai và nến tương lai không thể được sử dụng làm cặp cung cấp thông tin cho bot giao ngay.
    Thông tin chi tiết về điều này có thể khác nhau, nếu có, bạn có thể tìm thấy thông tin này trong tài liệu trao đổi.``` python
    def informative_pairs(self):
        return [
            ("ETH/USDT", "5m", ""),   # Uses default candletype, depends on trading_mode (recommended)
            ("ETH/USDT", "5m", "spot"),   # Forces usage of spot candles (only valid for bots running on spot markets).
            ("BTC/TUSD", "15m", "futures"),  # Uses futures candles (only bots with `trading_mode=futures`)
            ("BTC/TUSD", "15m", "mark"),  # Uses mark candles (only bots with `trading_mode=futures`)
        ]
    ```***

### Trình trang trí cặp thông tin (`@informative()`)

Để dễ dàng xác định các cặp thông tin, hãy sử dụng trang trí `@informative`. Tất cả các phương thức `populate_indicators_*` được trang trí đều chạy độc lập,
và không có quyền truy cập vào dữ liệu từ các cặp thông tin khác. Tuy nhiên, tất cả các khung dữ liệu thông tin cho mỗi cặp đều được hợp nhất và chuyển sang phương thức `populate_indicators()` chính.

!!! Lưu ý
    Không sử dụng trình trang trí `@informative` nếu bạn cần sử dụng dữ liệu từ một cặp thông tin khi tạo một cặp thông tin khác. Thay vào đó, hãy xác định các cặp thông tin theo cách thủ công như được mô tả [trong phần DataProvider](#complete-dataprovider-sample).

Khi siêu tùy chọn, việc sử dụng thuộc tính `.value` tham số siêu tùy chọn không được hỗ trợ. Vui lòng sử dụng thuộc tính `.range`. Xem [tối ưu hóa tham số chỉ báo](hyperopt.md#optimizing-an-indicator-parameter) để biết thêm thông tin.

??? info "Tài liệu đầy đủ"``` python
    def informative(
        timeframe: str,
        asset: str = "",
        fmt: str | Callable[[Any], str] | None = None,
        *,
        candle_type: CandleType | str | None = None,
        ffill: bool = True,
    ) -> Callable[[PopulateIndicators], PopulateIndicators]:
        """
        A decorator for populate_indicators_Nn(self, dataframe, metadata), allowing these functions to
        define informative indicators.

        Example usage:

            @informative('1h')
            def populate_indicators_1h(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
                dataframe['rsi'] = ta.RSI(dataframe, timeperiod=14)
                return dataframe

        :param timeframe: Informative timeframe. Must always be equal or higher than strategy timeframe.
        :param asset: Informative asset, for example BTC, BTC/USDT, ETH/BTC. Do not specify to use
                    current pair. Also supports limited pair format strings (see below)
        :param fmt: Column format (str) or column formatter (callable(name, asset, timeframe)). When not
        specified, defaults to:
        * {base}_{quote}_{column}_{timeframe} if asset is specified.
        * {column}_{timeframe} if asset is not specified.
        Pair format supports these format variables:
        * {base} - base currency in lower case, for example 'eth'.
        * {BASE} - same as {base}, except in upper case.
        * {quote} - quote currency in lower case, for example 'usdt'.
        * {QUOTE} - same as {quote}, except in upper case.
        Format string additionally supports this variables.
        * {asset} - full name of the asset, for example 'BTC/USDT'.
        * {column} - name of dataframe column.
        * {timeframe} - timeframe of informative dataframe.
        :param ffill: ffill dataframe after merging informative pair.
        :param candle_type: '', mark, index, premiumIndex, or funding_rate
        """
    ```??? Ví dụ "Cách nhanh chóng và dễ dàng để xác định các cặp thông tin"

    Hầu hết chúng ta không cần sức mạnh và tính linh hoạt do `merge_informative_pair()` cung cấp, do đó chúng ta có thể sử dụng một công cụ trang trí để nhanh chóng xác định các cặp thông tin.``` python

    from datetime import datetime
    from freqtrade.persistence import Trade
    from freqtrade.strategy import IStrategy, informative

    class AwesomeStrategy(IStrategy):
        
        # This method is not required. 
        # def informative_pairs(self): ...

        # Define informative upper timeframe for each pair. Decorators can be stacked on same 
        # method. Available in populate_indicators as 'rsi_30m' and 'rsi_1h'.
        @informative('30m')
        @informative('1h')
        def populate_indicators_1h(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
            dataframe['rsi'] = ta.RSI(dataframe, timeperiod=14)
            return dataframe

        # Define BTC/STAKE informative pair. Available in populate_indicators and other methods as
        # 'btc_rsi_1h'. Current stake currency should be specified as {stake} format variable 
        # instead of hard-coding actual stake currency. Available in populate_indicators and other 
        # methods as 'btc_usdt_rsi_1h' (when stake currency is USDT).
        @informative('1h', 'BTC/{stake}')
        def populate_indicators_btc_1h(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
            dataframe['rsi'] = ta.RSI(dataframe, timeperiod=14)
            return dataframe

        # Define BTC/ETH informative pair. You must specify quote currency if it is different from
        # stake currency. Available in populate_indicators and other methods as 'eth_btc_rsi_1h'.
        @informative('1h', 'ETH/BTC')
        def populate_indicators_eth_btc_1h(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
            dataframe['rsi'] = ta.RSI(dataframe, timeperiod=14)
            return dataframe
    
        # Define BTC/STAKE informative pair. A custom formatter may be specified for formatting
        # column names. A callable `fmt(**kwargs) -> str` may be specified, to implement custom
        # formatting. Available in populate_indicators and other methods as 'rsi_upper_1h'.
        @informative('1h', 'BTC/{stake}', '{column}_{timeframe}')
        def populate_indicators_btc_1h_2(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
            dataframe['rsi_upper'] = ta.RSI(dataframe, timeperiod=14)
            return dataframe
    
        def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
            # Strategy timeframe indicators for current pair.
            dataframe['rsi'] = ta.RSI(dataframe, timeperiod=14)
            # Informative pairs are available in this method.
            dataframe['rsi_less'] = dataframe['rsi'] < dataframe['rsi_1h']
            return dataframe

    ```!!! Lưu ý
    Sử dụng định dạng chuỗi khi truy cập các khung dữ liệu thông tin của các cặp khác. Điều này sẽ cho phép dễ dàng thay đổi loại tiền đặt cược trong cấu hình mà không cần phải điều chỉnh mã chiến lược.``` python
    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        stake = self.config['stake_currency']
        dataframe.loc[
            (
                (dataframe[f'btc_{stake}_rsi_1h'] < 35)
                &
                (dataframe['volume'] > 0)
            ),
            ['enter_long', 'enter_tag']] = (1, 'buy_signal_rsi')
    
        return dataframe
    ```Ngoài ra, việc đổi tên cột có thể được sử dụng để xóa loại tiền đặt cược khỏi tên cột: `@informative('1h', 'BTC/{stake}', fmt='{base} y_{column_{timeframe}')`.

!!! Cảnh báo "Tên phương thức trùng lặp"
    Các phương thức được gắn thẻ với trình trang trí `@informative()` phải luôn có tên duy nhất! Việc sử dụng lại cùng tên (ví dụ khi dán sao chép các phương thức thông tin đã được xác định) sẽ ghi đè các phương thức đã xác định trước đó và không tạo ra bất kỳ lỗi nào do hạn chế của ngôn ngữ lập trình Python. Trong những trường hợp như vậy, bạn sẽ thấy rằng các chỉ báo được tạo theo các phương thức cao hơn trong tệp chiến lược không có sẵn trong khung dữ liệu. Xem xét cẩn thận tên phương thức và đảm bảo chúng là duy nhất!

### *merge_informative_pair()*

Phương pháp này giúp bạn hợp nhất một cặp thông tin vào khung dữ liệu chính thông thường một cách an toàn và nhất quán, không có sai lệch về phía trước.

Tùy chọn:

- Đổi tên các cột để tạo các cột độc đáo
- Hợp nhất khung dữ liệu mà không có sai lệch khi nhìn về phía trước
- Điền chuyển tiếp (tùy chọn)

Để biết mẫu đầy đủ, vui lòng tham khảo [ví dụ về nhà cung cấp dữ liệu hoàn chỉnh](#complete-dataprovider-sample) bên dưới.

Tất cả các cột của khung dữ liệu thông tin sẽ có sẵn trên khung dữ liệu trả về theo kiểu được đổi tên:

!!! Ví dụ "Đổi tên cột"
    Giả sử `inf_tf = '1d'` các cột kết quả sẽ là:``` python
    'date', 'open', 'high', 'low', 'close', 'rsi'                     # from the original dataframe
    'date_1d', 'open_1d', 'high_1d', 'low_1d', 'close_1d', 'rsi_1d'   # from the informative dataframe
    ```??? Ví dụ "Đổi tên cột - 1h"
    Giả sử `inf_tf = '1h'` các cột kết quả sẽ là:``` python
    'date', 'open', 'high', 'low', 'close', 'rsi'                     # from the original dataframe
    'date_1h', 'open_1h', 'high_1h', 'low_1h', 'close_1h', 'rsi_1h'   # from the informative dataframe
    ```??? Ví dụ "Triển khai tùy chỉnh"
    Việc triển khai tùy chỉnh cho việc này là có thể và có thể được thực hiện như sau:``` python

    # Shift date by 1 candle
    # This is necessary since the data is always the "open date"
    # and a 15m candle starting at 12:15 should not know the close of the 1h candle from 12:00 to 13:00
    minutes = timeframe_to_minutes(inf_tf)
    # Only do this if the timeframes are different:
    informative['date_merge'] = informative["date"] + pd.to_timedelta(minutes, 'm')

    # Rename columns to be unique
    informative.columns = [f"{col}_{inf_tf}" for col in informative.columns]
    # Assuming inf_tf = '1d' - then the columns will now be:
    # date_1d, open_1d, high_1d, low_1d, close_1d, rsi_1d

    # Combine the 2 dataframes
    # all indicators on the informative sample MUST be calculated before this point
    dataframe = pd.merge(dataframe, informative, left_on='date', right_on=f'date_merge_{inf_tf}', how='left')
    # FFill to have the 1d value available in every row throughout the day.
    # Without this, comparisons would only work once per day.
    dataframe = dataframe.ffill()

    ```!!! Cảnh báo "Khung thời gian cung cấp thông tin < khung thời gian"
    Không nên sử dụng các khung thời gian chứa thông tin nhỏ hơn khung thời gian của khung dữ liệu chính với phương pháp này vì nó sẽ không sử dụng bất kỳ thông tin bổ sung nào mà phương pháp này sẽ cung cấp.
    Để sử dụng thông tin chi tiết hơn một cách chính xác, cần áp dụng các phương pháp nâng cao hơn (nằm ngoài phạm vi của tài liệu này).

## Dữ liệu bổ sung (DataProvider)

Chiến lược này cung cấp quyền truy cập vào `DataProvider`. Điều này cho phép bạn có được dữ liệu bổ sung để sử dụng trong chiến lược của mình.

Tất cả các phương thức đều trả về `None` trong trường hợp thất bại, tức là các lỗi không đưa ra ngoại lệ.

Vui lòng luôn kiểm tra chế độ hoạt động để chọn đúng phương pháp lấy dữ liệu (xem ví dụ bên dưới).

!!! Cảnh báo "Hạn chế Hyperopt"
    DataProvider có sẵn trong hyperopt, tuy nhiên, nó chỉ có thể được sử dụng trong `populate_indicators()` **trong một chiến lược**, không phải trong tệp lớp hyperopt.
    Nó cũng không có sẵn trong các phương thức `populate_entry_trend()` và `populate_exit_trend()`.

### Các tùy chọn có thể có cho DataProvider

- [`available_pairs`](#available_pairs) - Thuộc tính có bộ dữ liệu liệt kê các cặp được lưu trong bộ nhớ đệm cùng với khung thời gian (cặp, khung thời gian) của chúng.
- [`current_whitelist()`](#current_whitelist) - Trả về danh sách hiện tại của các cặp thuộc danh sách trắng. Hữu ích khi truy cập danh sách trắng động (tức là VolumePairlist)
- [`get_pair_dataframe(pair, khung thời gian)`](#get_pair_dataframepair-timeframe) - Đây là một phương pháp phổ biến, trả về dữ liệu lịch sử (để kiểm tra ngược) hoặc dữ liệu trực tiếp được lưu trong bộ nhớ đệm (đối với chế độ Chạy khô và Chạy trực tiếp).
- [`get_analyzed_dataframe(pair, khung thời gian)`](#get_analyzed_dataframepair-timeframe) - Trả về khung dữ liệu được phân tích (sau khi gọi `populate_indicators()`, `populate_buy()`, `populate_sell()`) và thời gian phân tích mới nhất.
- `histocal_ohlcv(cặp, khung thời gian)` - Trả về dữ liệu lịch sử được lưu trên đĩa.- `market(pair)` - Returns market data for the pair: fees, limits, precisions, activity flag, etc. See [ccxt documentation](https://github.com/ccxt/ccxt/wiki/Manual#markets) for more details on the Market data structure.
- `ohlcv(cặp, khung thời gian)` - Dữ liệu nến (OHLCV) hiện được lưu trong bộ nhớ đệm cho cặp này, trả về DataFrame hoặc DataFrame trống.
- [`orderbook(pair, max)`](#orderbookpair-maximum) - Trả về dữ liệu sổ đặt hàng mới nhất cho cặp, một lệnh có giá thầu/yêu cầu với tổng số mục nhập `tối đa`.- [`ticker(pair)`](#tickerpair) - Returns current ticker data for the pair. See [ccxt documentation](https://github.com/ccxt/ccxt/wiki/Manual#price-tickers) for more details on the Ticker data structure.
- [`check_delisting(pair)`](#check_delistingpair) - Trả về Ngày giờ của lịch hủy cặp nếu có, nếu không thì trả về Không
- [`funding_rate(pair)`](#funding_ratepair) - Trả về dữ liệu tỷ lệ cấp vốn hiện tại cho cặp.
- `runmode` - Thuộc tính chứa runmode hiện tại.

### Ví dụ về cách sử dụng

### *cặp_có sẵn*``` python
for pair, timeframe in self.dp.available_pairs:
    print(f"available {pair}, {timeframe}")
```### *current_whitelist()*

Hãy tưởng tượng bạn đã phát triển một chiến lược giao dịch trong khung thời gian `5m` bằng cách sử dụng các tín hiệu được tạo từ khung thời gian `1d` trên 10 cặp trao đổi hàng đầu theo khối lượng.

Logic chiến lược có thể trông giống như thế này:

*Quét qua 10 cặp hàng đầu theo khối lượng bằng cách sử dụng `VolumePairList` cứ sau 5 phút và sử dụng RSI 14 ngày để vào và thoát.*

Do dữ liệu sẵn có hạn chế, rất khó để lấy mẫu nến `5 triệu` thành nến hàng ngày để sử dụng trong chỉ số RSI 14 ngày. Hầu hết các sàn giao dịch đều giới hạn người dùng chỉ ở mức 500-1000 nến, tức là chúng ta có khoảng 1,74 nến hàng ngày. Chúng ta cần ít nhất 14 ngày!

Vì chúng tôi không thể lấy mẫu lại dữ liệu nên chúng tôi sẽ phải sử dụng một cặp thông tin và vì danh sách trắng sẽ linh hoạt nên chúng tôi không biết nên sử dụng (các) cặp nào! Chúng tôi có một vấn đề!

Đây là lúc việc gọi `self.dp.current_whitelist()` trở nên hữu ích để chỉ truy xuất những cặp đó trong danh sách trắng.```python
    def informative_pairs(self):

        # get access to all pairs available in whitelist.
        pairs = self.dp.current_whitelist()
        # Assign timeframe to each pair so they can be downloaded and cached for strategy.
        informative_pairs = [(pair, '1d') for pair in pairs]
        return informative_pairs
```??? Lưu ý "Vẽ đồ thị với current_whitelist"
    Danh sách trắng hiện tại không được hỗ trợ cho `plot-dataframe`, vì lệnh này thường được sử dụng bằng cách cung cấp một danh sách cặp rõ ràng và do đó sẽ làm cho các giá trị trả về của phương thức này bị sai lệch.
    Nó cũng không được hỗ trợ cho hiển thị FreqUI trong [chế độ máy chủ web](utils.md#webserver-mode), vì cấu hình cho chế độ máy chủ web không yêu cầu đặt danh sách cặp.

### *get_pair_dataframe(cặp, khung thời gian)*``` python
# fetch live / historical candle (OHLCV) data for the first informative pair
inf_pair, inf_timeframe = self.informative_pairs()[0]
informative = self.dp.get_pair_dataframe(pair=inf_pair,
                                         timeframe=inf_timeframe)
```!!! Cảnh báo "Cảnh báo về việc kiểm tra lại"
    Trong quá trình kiểm tra ngược, hành vi `dp.get_pair_dataframe()` sẽ khác nhau tùy thuộc vào vị trí nó được gọi.
    Trong các phương thức `populate_*()`, `dp.get_pair_dataframe()` trả về toàn bộ phạm vi thời gian. Hãy đảm bảo không “nhìn về tương lai” để tránh bị bất ngờ khi chạy ở chế độ dry/live.
    Trong [callbacks](strategy-callbacks.md), bạn sẽ nhận được toàn bộ phạm vi thời gian tính đến nến (mô phỏng) hiện tại.

### *get_analyzed_dataframe(cặp, khung thời gian)*

Phương pháp này được freqtrade sử dụng nội bộ để xác định tín hiệu cuối cùng.
Nó cũng có thể được sử dụng trong các lệnh gọi lại cụ thể để nhận tín hiệu gây ra hành động (xem [Tài liệu chiến lược nâng cao](strategy-advanced.md) để biết thêm chi tiết về các lệnh gọi lại có sẵn).``` python
# fetch current dataframe
dataframe, last_updated = self.dp.get_analyzed_dataframe(pair=metadata['pair'],
                                                         timeframe=self.timeframe)
```!!! Lưu ý "Không có dữ liệu"
    Trả về một khung dữ liệu trống nếu cặp được yêu cầu không được lưu vào bộ đệm.
    Bạn có thể kiểm tra điều này bằng `if dataframe.empty:` và xử lý trường hợp này cho phù hợp.
    Điều này sẽ không xảy ra khi sử dụng các cặp thuộc danh sách trắng.

### *sổ đặt hàng(cặp, tối đa)*

Truy xuất sổ đặt hàng hiện tại cho một cặp.``` python
if self.dp.runmode.value in ('live', 'dry_run'):
    ob = self.dp.orderbook(metadata['pair'], 1)
    dataframe['best_bid'] = ob['bids'][0][0]
    dataframe['best_ask'] = ob['asks'][0][0]
```The orderbook structure is aligned with the order structure from [ccxt](https://github.com/ccxt/ccxt/wiki/Manual#order-book-structure), so the result will be formatted as follows:
``` js
{
    'bids': [
        [ price, amount ], // [ float, float ]
        [ price, amount ],
        ...
    ],
    'asks': [
        [ price, amount ],
        [ price, amount ],
        //...
    ],
    //...
}
```Do đó, việc sử dụng `ob['bids'][0][0]` như được trình bày ở trên sẽ sử dụng giá thầu tốt nhất. `ob['bids'][0][1]` sẽ xem xét số tiền ở vị trí sổ đặt hàng này.

!!! Cảnh báo "Cảnh báo về việc kiểm tra lại"
    Sổ đặt hàng không phải là một phần của dữ liệu lịch sử, điều đó có nghĩa là việc kiểm tra lại và hyperopt sẽ không hoạt động chính xác nếu sử dụng phương pháp này vì phương pháp này sẽ trả về các giá trị cập nhật.

### *mã (cặp)*``` python
if self.dp.runmode.value in ('live', 'dry_run'):
    ticker = self.dp.ticker(metadata['pair'])
    dataframe['last_price'] = ticker['last']
    dataframe['volume24h'] = ticker['quoteVolume']
    dataframe['vwap'] = ticker['vwap']
```!!! Cảnh báo
    Mặc dù cấu trúc dữ liệu mã đánh dấu là một phần của Giao diện hợp nhất ccxt, nhưng các giá trị được phương thức này trả về có thể
    khác nhau cho các trao đổi khác nhau. Ví dụ: nhiều sàn giao dịch không trả về giá trị `vwap` và một số sàn giao dịch
    không phải lúc nào cũng điền vào trường `cuối` (vì vậy có thể là Không), v.v. Vì vậy, bạn cần xác minh cẩn thận mã đánh dấu
    dữ liệu được trả về từ trao đổi và thêm xử lý lỗi/mặc định thích hợp.

!!! Cảnh báo "Cảnh báo về việc kiểm tra lại"
    Phương thức này sẽ luôn trả về các giá trị cập nhật/thời gian thực. Do đó, việc sử dụng trong quá trình backtesting/hyperopt mà không kiểm tra runmode sẽ dẫn đến kết quả sai, ví dụ: toàn bộ khung dữ liệu của bạn sẽ chứa cùng một giá trị trong tất cả các hàng.

### *check_delisting(cặp)*```python
def custom_exit(self, pair: str, trade: Trade, current_time: datetime, current_rate: float, current_profit: float, **kwargs):
    if self.dp.runmode.value in ('live', 'dry_run'):
        delisting_dt = self.dp.check_delisting(pair)
        if delisting_dt is not None:
            return "delist"
```!!! Lưu ý “Có sẵn thông tin hủy niêm yết”
    Phương thức này chỉ khả dụng đối với một số sàn giao dịch nhất định và sẽ trả về `Không` trong trường hợp phương thức này không khả dụng hoặc nếu cặp này không được lên lịch hủy niêm yết.

!!! Cảnh báo "Cảnh báo về việc kiểm tra lại"
    Phương thức này sẽ luôn trả về các giá trị cập nhật/thời gian thực. Do đó, việc sử dụng trong quá trình backtesting/hyperopt mà không kiểm tra runmode sẽ dẫn đến kết quả sai, ví dụ: toàn bộ khung dữ liệu của bạn sẽ chứa cùng một giá trị trong tất cả các hàng.

### *tỷ lệ cấp vốn(cặp)*

Truy xuất tỷ lệ cấp vốn hiện tại cho cặp này và chỉ hoạt động đối với các cặp tương lai ở định dạng `cơ sở/báo giá:thanh toán` (ví dụ: `ETH/USDT:USDT`).``` python
if self.dp.runmode.value in ('live', 'dry_run'):
    funding_rate = self.dp.funding_rate(metadata['pair'])
    dataframe['current_funding_rate'] = funding_rate['fundingRate']
    dataframe['next_funding_timestamp'] = funding_rate['fundingTimestamp']
    dataframe['next_funding_datetime'] = funding_rate['fundingDatetime']
```The funding rate structure is aligned with the funding rate structure from [ccxt](https://github.com/ccxt/ccxt/wiki/Manual#funding-rate-structure), so the result will be formatted as follows:
``` python
{
    "info": {
        # ... 
    },
    "symbol": "BTC/USDT:USDT",
    "markPrice": 110730.7,
    "indexPrice": 110782.52,
    "interestRate": 0.0001,
    "estimatedSettlePrice": 110822.67200153,
    "timestamp": 1757146321001,
    "datetime": "2025-09-06T08:12:01.001Z",
    "fundingRate": 5.609e-05,
    "fundingTimestamp": 1757174400000,
    "fundingDatetime": "2025-09-06T16:00:00.000Z",
    "nextFundingRate": None,
    "nextFundingTimestamp": None,
    "nextFundingDatetime": None,
    "previousFundingRate": None,
    "previousFundingTimestamp": None,
    "previousFundingDatetime": None,
    "interval": None,
}
```Do đó, việc sử dụng `funding_rate['fundingRate']` như được trình bày ở trên sẽ sử dụng tỷ lệ cấp vốn hiện tại.
Trên thực tế, dữ liệu có sẵn sẽ khác nhau giữa các sàn giao dịch, vì vậy mã này có thể không hoạt động như mong đợi trên các sàn giao dịch.

!!! Cảnh báo "Cảnh báo về việc kiểm tra lại"
    Tỷ lệ tài trợ hiện tại không phải là một phần của dữ liệu lịch sử, điều đó có nghĩa là việc kiểm tra ngược và siêu tối ưu sẽ không hoạt động chính xác nếu sử dụng phương pháp này vì phương pháp này sẽ trả về các giá trị cập nhật.
    Chúng tôi khuyên bạn nên sử dụng tỷ lệ cấp vốn có sẵn trước đây để kiểm tra lại (được tải xuống tự động và ở tần suất mà sàn giao dịch cung cấp, thường là 4 giờ hoặc 8 giờ).
    `self.dp.get_pair_dataframe(pair=siêu dữ liệu['pair'], khung thời gian='8h', Candle_type="funding_rate")`

### Gửi thông báo

Chức năng `.send_msg()` của nhà cung cấp dữ liệu cho phép bạn gửi thông báo tùy chỉnh từ chiến lược của mình.
Thông báo giống hệt nhau sẽ chỉ được gửi một lần cho mỗi nến, trừ khi đối số thứ 2 (`always_send`) được đặt thành True.``` python
    self.dp.send_msg(f"{metadata['pair']} just got hot!")

    # Force send this notification, avoid caching (Please read warning below!)
    self.dp.send_msg(f"{metadata['pair']} just got hot!", always_send=True)
```Thông báo sẽ chỉ được gửi ở chế độ giao dịch (Trực tiếp/Chạy thử) - vì vậy phương pháp này có thể được gọi mà không cần điều kiện để kiểm tra lại.

!!! Cảnh báo "Spam"
    Bạn có thể tự spam khá tốt bằng cách đặt `always_send=True` trong phương pháp này. Hãy sử dụng điều này một cách hết sức cẩn thận và chỉ trong những điều kiện mà bạn biết sẽ không xảy ra trong suốt một ngọn nến để tránh một thông báo cứ sau 5 giây.

### Mẫu DataProvider hoàn chỉnh```python
from freqtrade.strategy import IStrategy, merge_informative_pair
from pandas import DataFrame

class SampleStrategy(IStrategy):
    # strategy init stuff...

    timeframe = '5m'

    # more strategy init stuff..

    def informative_pairs(self):

        # get access to all pairs available in whitelist.
        pairs = self.dp.current_whitelist()
        # Assign tf to each pair so they can be downloaded and cached for strategy.
        informative_pairs = [(pair, '1d') for pair in pairs]
        # Optionally Add additional "static" pairs
        informative_pairs += [("ETH/USDT", "5m"),
                              ("BTC/TUSD", "15m"),
                            ]
        return informative_pairs

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        if not self.dp:
            # Don't do anything if DataProvider is not available.
            return dataframe

        inf_tf = '1d'
        # Get the informative pair
        informative = self.dp.get_pair_dataframe(pair=metadata['pair'], timeframe=inf_tf)
        # Get the 14 day rsi
        informative['rsi'] = ta.RSI(informative, timeperiod=14)

        # Use the helper function merge_informative_pair to safely merge the pair
        # Automatically renames the columns and merges a shorter timeframe dataframe and a longer timeframe informative pair
        # use ffill to have the 1d value available in every row throughout the day.
        # Without this, comparisons between columns of the original and the informative pair would only work once per day.
        # Full documentation of this method, see below
        dataframe = merge_informative_pair(dataframe, informative, self.timeframe, inf_tf, ffill=True)

        # Calculate rsi of the original dataframe (5m timeframe)
        dataframe['rsi'] = ta.RSI(dataframe, timeperiod=14)

        # Do other stuff
        # ...

        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:

        dataframe.loc[
            (
                (qtpylib.crossed_above(dataframe['rsi'], 30)) &  # Signal: RSI crosses above 30
                (dataframe['rsi_1d'] < 30) &                     # Ensure daily RSI is < 30
                (dataframe['volume'] > 0)                        # Ensure this candle had volume (important for backtesting)
            ),
            ['enter_long', 'enter_tag']] = (1, 'rsi_cross')

```***

## Dữ liệu bổ sung (Ví)

Chiến lược này cung cấp quyền truy cập vào đối tượng `ví`. Phần này chứa số dư hiện tại của ví/tài khoản của bạn trên sàn giao dịch.

!!! Lưu ý "Backtesting/Hyperopt"
    Ví hoạt động khác nhau tùy thuộc vào chức năng mà nó được gọi.
    Trong các phương thức `populate_*()`, nó sẽ trả về ví đầy đủ như đã định cấu hình.
    Trong [callbacks](strategy-callbacks.md), bạn sẽ nhận được trạng thái ví tương ứng với ví được mô phỏng thực tế tại thời điểm đó trong quá trình mô phỏng.

Luôn kiểm tra xem có sẵn `ví` hay không để tránh lỗi trong quá trình kiểm tra lại.``` python
if self.wallets:
    free_eth = self.wallets.get_free('ETH')
    used_eth = self.wallets.get_used('ETH')
    total_eth = self.wallets.get_total('ETH')
```### Các tùy chọn có thể có cho Ví

- `get_free(asset)` - số dư hiện có để giao dịch
- `get_used(asset)` - số dư hiện đang bị ràng buộc (lệnh mở)
- `get_total(asset)` - tổng số dư khả dụng - tổng của 2 số trên

***

## Dữ liệu bổ sung (Giao dịch)

Lịch sử giao dịch có thể được truy xuất trong chiến lược bằng cách truy vấn cơ sở dữ liệu.

Ở đầu tệp, nhập đối tượng được yêu cầu:```python
from freqtrade.persistence import Trade
```Các truy vấn mẫu sau đây giao dịch từ hôm nay cho cặp hiện tại (`siêu dữ liệu ['cặp']`). Các bộ lọc khác có thể dễ dàng được thêm vào.``` python
trades = Trade.get_trades_proxy(pair=metadata['pair'],
                                open_date=datetime.now(timezone.utc) - timedelta(days=1),
                                is_open=False,
            ]).order_by(Trade.close_date).all()
# Summarize profit for this pair.
curdayprofit = sum(trade.close_profit for trade in trades)
```Để biết danh sách đầy đủ các phương thức có sẵn, vui lòng tham khảo tài liệu [Trade object](trade-object.md).

!!! Cảnh báo
    Lịch sử giao dịch không có sẵn trong các phương pháp `populate_*` trong quá trình kiểm tra ngược hoặc siêu tối ưu và sẽ dẫn đến kết quả trống.

## Ngăn chặn giao dịch xảy ra đối với một cặp cụ thể

Freqtrade tự động khóa các cặp cho nến hiện tại (cho đến khi nến đó kết thúc) khi một cặp thoát ra, ngăn chặn việc cặp đó quay trở lại ngay lập tức.

Điều này nhằm ngăn chặn "thác nước" của nhiều giao dịch thường xuyên trong một cây nến.

Các cặp đã khóa sẽ hiển thị thông báo `Cặp <cặp> hiện đang bị khóa.`.

### Khóa các cặp từ trong chiến lược

Đôi khi có thể muốn khóa một cặp sau khi một số sự kiện nhất định xảy ra (ví dụ: nhiều giao dịch thua liên tiếp).

Freqtrade có một phương pháp dễ dàng để thực hiện việc này từ bên trong chiến lược, bằng cách gọi `self.lock_pair(pair, Until, [reason])`.
`cho đến` phải là một đối tượng ngày giờ trong tương lai, sau đó giao dịch sẽ được kích hoạt lại cho cặp đó, trong khi `lý do` là một chuỗi tùy chọn nêu chi tiết lý do tại sao cặp đó bị khóa.

Bạn cũng có thể mở khóa theo cách thủ công bằng cách gọi `self.unlock_pair(pair)` hoặc `self.unlock_reason(<reason>)`, cung cấp lý do cặp được mở khóa.
`self.unlock_reason(<reason>)` sẽ mở khóa tất cả các cặp hiện bị khóa với lý do được cung cấp.

Để xác minh xem một cặp hiện có bị khóa hay không, hãy sử dụng `self.is_pair_locked(pair)`.

!!! Lưu ý
    Các cặp bị khóa sẽ luôn được làm tròn đến cây nến tiếp theo. Vì vậy, giả sử khung thời gian `5m`, khóa có `cho đến` được đặt thành 10:18 sẽ khóa cặp cho đến khi nến từ 10:15-10:20 kết thúc.

!!! Cảnh báo
    Các cặp khóa thủ công không khả dụng trong quá trình kiểm tra lại. Chỉ cho phép khóa thông qua Bảo vệ.

#### Ví dụ khóa cặp``` python
from freqtrade.persistence import Trade
from datetime import timedelta, datetime, timezone
# Put the above lines at the top of the strategy file, next to all the other imports
# --------

# Within populate indicators (or populate_entry_trend):
if self.config['runmode'].value in ('live', 'dry_run'):
    # fetch closed trades for the last 2 days
    trades = Trade.get_trades_proxy(
        pair=metadata['pair'], is_open=False, 
        open_date=datetime.now(timezone.utc) - timedelta(days=2))
    # Analyze the conditions you'd like to lock the pair .... will probably be different for every strategy
    sumprofit = sum(trade.close_profit for trade in trades)
    if sumprofit < 0:
        # Lock pair for 12 hours
        self.lock_pair(metadata['pair'], until=datetime.now(timezone.utc) + timedelta(hours=12))
```## In khung dữ liệu chính

Để kiểm tra khung dữ liệu chính hiện tại, bạn có thể đưa ra câu lệnh in bằng `populate_entry_trend()` hoặc `populate_exit_trend()`.
Bạn cũng có thể muốn in cặp này để biết rõ dữ liệu nào hiện đang được hiển thị.``` python
def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
    dataframe.loc[
        (
            #>> whatever condition<<<
        ),
        ['enter_long', 'enter_tag']] = (1, 'somestring')

    # Print the Analyzed pair
    print(f"result for {metadata['pair']}")

    # Inspect the last 5 rows
    print(dataframe.tail())

    return dataframe
```Cũng có thể in nhiều hàng bằng cách sử dụng `print(dataframe)` thay vì `print(dataframe.tail())`. Tuy nhiên, điều này không được khuyến khích vì có thể dẫn đến nhiều đầu ra (~500 dòng mỗi cặp cứ sau 5 giây).

## Những lỗi thường gặp khi xây dựng chiến lược

### Nhìn về tương lai trong khi kiểm tra lại

Backtesting phân tích toàn bộ khung thời gian của khung dữ liệu cùng một lúc vì lý do hiệu suất. Vì điều này, các tác giả chiến lược cần đảm bảo rằng các chiến lược không hướng tới tương lai, tức là sử dụng dữ liệu không có sẵn ở chế độ khô hoặc trực tiếp.

Đây là điểm khó khăn phổ biến, có thể gây ra sự khác biệt lớn giữa phương pháp kiểm tra lại và phương pháp chạy thử/chạy trực tiếp. Các chiến lược nhìn về tương lai sẽ hoạt động tốt trong quá trình kiểm tra lại, thường mang lại lợi nhuận hoặc tỷ lệ thắng đáng kinh ngạc, nhưng sẽ thất bại hoặc hoạt động kém trong điều kiện thực tế.

Danh sách sau đây chứa một số mẫu phổ biến cần tránh để tránh gây thất vọng:

- không sử dụng `shift(-1)` hoặc các giá trị âm khác. Điều này sử dụng dữ liệu từ tương lai trong quá trình kiểm tra ngược, dữ liệu này không có sẵn ở chế độ khô hoặc trực tiếp.
- không sử dụng `.iloc[-1]` hoặc bất kỳ vị trí tuyệt đối nào khác trong khung dữ liệu trong các hàm `populate_`, vì điều này sẽ khác nhau giữa chạy thử và thử nghiệm ngược. Tuy nhiên, việc lập chỉ mục `iloc` tuyệt đối là an toàn để sử dụng trong các cuộc gọi lại - xem [Cuộc gọi lại chiến lược](strategy-callbacks.md).
- không sử dụng các hàm sử dụng tất cả các giá trị khung dữ liệu hoặc cột, ví dụ: `dataframe['mean_volume'] = dataframe['volume'].mean()`. Vì quá trình kiểm tra ngược sử dụng toàn bộ khung dữ liệu nên tại bất kỳ điểm nào trong khung dữ liệu, chuỗi `'mean_volume'` sẽ bao gồm dữ liệu từ tương lai. Thay vào đó, hãy sử dụng phép tính cán(), ví dụ: `dataframe['volume'].rolling(<window>).mean()`.
- không sử dụng `.resample('1h')`. Điều này sử dụng đường viền bên trái của khoảng thời gian, do đó di chuyển dữ liệu từ ranh giới giờ đến đầu giờ. Thay vào đó, hãy sử dụng `.resample('1h', label='right')`.
- không sử dụng `.merge()` để kết hợp các khung thời gian dài hơn vào các khung thời gian ngắn hơn. Thay vào đó, hãy sử dụng trình trợ giúp [informative pair](#informative-pairs). (Việc hợp nhất đơn giản có thể ngầm gây ra sai lệch khi nhìn về phía trước vì ngày đề cập đến ngày mở chứ không phải ngày đóng).

!!! Mẹo "Xác định vấn đề"
    Bạn phải luôn sử dụng hai lệnh trợ giúp [lookahead-analysis](lookahead-analysis.md) và [recursive-analysis](recursive-analysis.md), mỗi lệnh có thể giúp bạn tìm ra vấn đề với chiến lược của mình theo những cách khác nhau.
    Hãy đối xử với chúng như chính bản thân chúng - những người trợ giúp xác định những vấn đề phổ biến nhất. Kết quả âm tính của mỗi lỗi không đảm bảo rằng không có lỗi nào nêu trên.

### Tín hiệu xung đột

Khi các tín hiệu xung đột va chạm nhau (ví dụ: cả `'enter_long'` và `'exit_long'` đều được đặt thành `1`), freqtrade sẽ không làm gì và bỏ qua tín hiệu vào. Điều này sẽ tránh các giao dịch vào và thoát ngay lập tức. Rõ ràng, điều này có thể dẫn đến việc bỏ sót các mục nhập.

Các quy tắc sau được áp dụng và tín hiệu vào lệnh sẽ bị bỏ qua nếu có nhiều hơn một trong 3 tín hiệu được đặt:

- `enter_long` -> `exit_long`, `enter_short`
- `enter_short` -> `exit_short`, `enter_long`

## Ý tưởng chiến lược tiếp theoTo get additional ideas for strategies, head over to the [strategy repository](https://github.com/freqtrade/freqtrade-strategies). Feel free to use them as examples, but results will depend on the current market situation, pairs used, etc. Therefore, these strategies should be considered only for learning purposes, not real world trading. Please backtest the strategy for your exchange/desired pairs first, then dry run to evaluate carefully, and use at your own risk.
Hãy thoải mái sử dụng bất kỳ ý tưởng nào trong số đó làm nguồn cảm hứng cho chiến lược của riêng bạn. Chúng tôi vui lòng chấp nhận Yêu cầu Kéo chứa các chiến lược mới vào kho lưu trữ.

## Các bước tiếp theo

Bây giờ bạn đã có một chiến lược hoàn hảo và có thể bạn muốn kiểm tra lại nó.
Bước tiếp theo của bạn là tìm hiểu [cách sử dụng backtesting](backtesting.md).