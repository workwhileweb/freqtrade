<!-- Auto-translated from docs/ by script. Please review technical terms. -->

# Chiến lược nâng cao

Trang này giải thích một số khái niệm nâng cao có sẵn cho các chiến lược.
Nếu bạn mới bắt đầu, trước tiên hãy làm quen với [Freqtrade cơ bản](bot-basics.md) và các phương pháp được mô tả trong [Tùy chỉnh chiến lược](strategy-customization.md).

Trình tự lệnh gọi của các phương thức được mô tả ở đây được đề cập trong [logic thực thi bot](bot-basics.md#bot-execution-logic). Những tài liệu đó cũng hữu ích trong việc quyết định phương pháp nào phù hợp nhất với nhu cầu tùy chỉnh của bạn.

!!! Lưu ý
    Các phương thức gọi lại *chỉ* nên được triển khai nếu chiến lược sử dụng chúng.

!!! Mẹo
    Bắt đầu với mẫu chiến lược chứa tất cả các phương thức gọi lại có sẵn bằng cách chạy `freqtrade new-strategy --strategy MyAwesomeStrategy --template Advanced`

## Lưu trữ thông tin (Persistent)

Freqtrade cho phép lưu trữ/truy xuất thông tin tùy chỉnh của người dùng liên quan đến giao dịch cụ thể trong cơ sở dữ liệu.

Khi sử dụng một đối tượng giao dịch, thông tin có thể được lưu trữ bằng cách sử dụng `trade.set_custom_data(key='my_key', value=my_value)` và được truy xuất bằng cách sử dụng `trade.get_custom_data(key='my_key')`. Mỗi mục nhập dữ liệu được liên kết với một giao dịch và một khóa do người dùng cung cấp (thuộc loại `chuỗi`). Điều này có nghĩa là điều này chỉ có thể được sử dụng trong các lệnh gọi lại cũng cung cấp đối tượng giao dịch.

Để dữ liệu có thể được lưu trữ trong cơ sở dữ liệu, freqtrade phải tuần tự hóa dữ liệu. Điều này được thực hiện bằng cách chuyển đổi dữ liệu thành chuỗi được định dạng JSON.
Freqtrade sẽ cố gắng đảo ngược hành động này khi truy xuất, do đó, từ góc độ chiến lược, điều này sẽ không liên quan.```python
from freqtrade.persistence import Trade
from datetime import timedelta

class AwesomeStrategy(IStrategy):

    def bot_loop_start(self, **kwargs) -> None:
        for trade in Trade.get_open_order_trades():
            fills = trade.select_filled_orders(trade.entry_side)
            if trade.pair == 'ETH/USDT':
                trade_entry_type = trade.get_custom_data(key='entry_type')
                if trade_entry_type is None:
                    trade_entry_type = 'breakout' if 'entry_1' in trade.enter_tag else 'dip'
                elif len(fills) > 1:
                    trade_entry_type = 'buy_up'
                trade.set_custom_data(key='entry_type', value=trade_entry_type)
        return super().bot_loop_start(**kwargs)

    def adjust_entry_price(self, trade: Trade, order: Order | None, pair: str,
                           current_time: datetime, proposed_rate: float, current_order_rate: float,
                           entry_tag: str | None, side: str, **kwargs) -> float:
        # Limit orders to use and follow SMA200 as price target for the first 10 minutes since entry trigger for BTC/USDT pair.
        if (
            pair == 'BTC/USDT' 
            and entry_tag == 'long_sma200' 
            and side == 'long' 
            and (current_time - timedelta(minutes=10)) > trade.open_date_utc 
            and order.filled == 0.0
        ):
            dataframe, _ = self.dp.get_analyzed_dataframe(pair=pair, timeframe=self.timeframe)
            current_candle = dataframe.iloc[-1].squeeze()
            # store information about entry adjustment
            existing_count = trade.get_custom_data('num_entry_adjustments', default=0)
            if not existing_count:
                existing_count = 1
            else:
                existing_count += 1
            trade.set_custom_data(key='num_entry_adjustments', value=existing_count)

            # adjust order price
            return current_candle['sma_200']

        # default: maintain existing order
        return current_order_rate

    def custom_exit(self, pair: str, trade: Trade, current_time: datetime, current_rate: float, current_profit: float, **kwargs):

        entry_adjustment_count = trade.get_custom_data(key='num_entry_adjustments')
        trade_entry_type = trade.get_custom_data(key='entry_type')
        if entry_adjustment_count is None:
            if current_profit > 0.01 and (current_time - timedelta(minutes=100) > trade.open_date_utc):
                return True, 'exit_1'
        else
            if entry_adjustment_count > 0 and if current_profit > 0.05:
                return True, 'exit_2'
            if trade_entry_type == 'breakout' and current_profit > 0.1:
                return True, 'exit_3

        return False, None
```Trên đây là một ví dụ đơn giản - có nhiều cách đơn giản hơn để truy xuất dữ liệu giao dịch như điều chỉnh điểm vào lệnh.

!!! Lưu ý
    Chúng tôi khuyên bạn nên sử dụng các kiểu dữ liệu đơn giản `[bool, int, float, str]` để đảm bảo không có vấn đề gì khi tuần tự hóa dữ liệu cần được lưu trữ.
    Việc lưu trữ lượng lớn dữ liệu có thể dẫn đến các tác dụng phụ ngoài ý muốn, chẳng hạn như cơ sở dữ liệu trở nên lớn (và do đó, cũng chậm).

!!! Cảnh báo "Dữ liệu không thể tuần tự hóa"
    Nếu dữ liệu được cung cấp không thể được tuần tự hóa, một cảnh báo sẽ được ghi lại và mục nhập cho `key` được chỉ định sẽ chứa `None` làm dữ liệu.

??? Lưu ý "Tất cả thuộc tính"
    custom-data có các trình truy cập sau thông qua đối tượng Trade (giả sử là `trade` bên dưới):

    * `trade.get_custom_data(key='something', default=0)` - Trả về giá trị thực tế được cung cấp trong loại được cung cấp.
    * `trade.get_custom_data_entry(key='something')` - Trả về mục nhập - bao gồm siêu dữ liệu. Giá trị có thể được truy cập thông qua thuộc tính `.value`.
    * `trade.set_custom_data(key='something', value={'some': 'value'})` - đặt hoặc cập nhật khóa tương ứng cho giao dịch này. Giá trị phải có thể tuần tự hóa - và chúng tôi khuyên bạn nên giữ dữ liệu được lưu trữ ở mức tương đối nhỏ.

    "giá trị" có thể là bất kỳ loại nào (cả trong cài đặt và nhận) - nhưng phải có khả năng tuần tự hóa json.

## Lưu trữ thông tin (Non-Persistent)

!!! Cảnh báo "Không dùng nữa"
    Phương pháp lưu trữ thông tin này không được dùng nữa và chúng tôi khuyên bạn không nên sử dụng phương pháp lưu trữ không liên tục.  
    Thay vào đó, vui lòng sử dụng [Bộ nhớ liên tục](#storing-information-persistent).

    Do đó, nội dung của nó đã bị thu gọn.

??? Tóm tắt "Lưu trữ thông tin"
    Việc lưu trữ thông tin có thể được thực hiện bằng cách tạo một từ điển mới trong lớp chiến lược.

    Tên của biến có thể được chọn theo ý muốn, nhưng phải có tiền tố `custom_` để tránh xung đột việc đặt tên với các biến chiến lược được xác định trước.```python
    class AwesomeStrategy(IStrategy):
        # Create custom dictionary
        custom_info = {}

        def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
            # Check if the entry already exists
            if not metadata["pair"] in self.custom_info:
                # Create empty entry for this pair
                self.custom_info[metadata["pair"]] = {}

            if "crosstime" in self.custom_info[metadata["pair"]]:
                self.custom_info[metadata["pair"]]["crosstime"] += 1
            else:
                self.custom_info[metadata["pair"]]["crosstime"] = 1
    ```!!! Cảnh báo
        Dữ liệu không được lưu giữ sau khi khởi động lại bot (hoặc tải lại cấu hình). Ngoài ra, lượng dữ liệu phải được giữ ở mức nhỏ (không có DataFrames, v.v.), nếu không bot sẽ bắt đầu tiêu tốn nhiều bộ nhớ và cuối cùng hết bộ nhớ và gặp sự cố.

    !!! Lưu ý
        Nếu dữ liệu dành riêng cho từng cặp, hãy đảm bảo sử dụng cặp làm một trong các khóa trong từ điển.

## Truy cập khung dữ liệu

Bạn có thể truy cập khung dữ liệu trong các chức năng chiến lược khác nhau bằng cách truy vấn nó từ nhà cung cấp dữ liệu.``` python
from freqtrade.exchange import timeframe_to_prev_date

class AwesomeStrategy(IStrategy):
    def confirm_trade_exit(self, pair: str, trade: 'Trade', order_type: str, amount: float,
                           rate: float, time_in_force: str, exit_reason: str,
                           current_time: 'datetime', **kwargs) -> bool:
        # Obtain pair dataframe.
        dataframe, _ = self.dp.get_analyzed_dataframe(pair, self.timeframe)

        # Obtain last available candle. Do not use current_time to look up latest candle, because 
        # current_time points to current incomplete candle whose data is not available.
        last_candle = dataframe.iloc[-1].squeeze()
        # <...>

        # In dry/live runs trade open date will not match candle open date therefore it must be 
        # rounded.
        trade_date = timeframe_to_prev_date(self.timeframe, trade.open_date_utc)
        # Look up trade candle.
        trade_candle = dataframe.loc[dataframe['date'] == trade_date]
        # trade_candle may be empty for trades that just opened as it is still incomplete.
        if not trade_candle.empty:
            trade_candle = trade_candle.squeeze()
            # <...>
```!!! Cảnh báo "Sử dụng .iloc[-1]"
    Bạn có thể sử dụng `.iloc[-1]` ở đây vì `get_analyzed_dataframe()` chỉ trả về những nến mà quá trình kiểm tra ngược được phép xem.
    Điều này sẽ không hoạt động trong các phương thức `populate_*`, vì vậy hãy đảm bảo không sử dụng `.iloc[]` trong khu vực đó.
    Ngoài ra, tính năng này sẽ chỉ hoạt động kể từ phiên bản 2021.5.

***

## Nhập thẻ

Khi chiến lược của bạn có nhiều tín hiệu vào lệnh, bạn có thể đặt tên cho tín hiệu được kích hoạt.
Sau đó, bạn có thể truy cập tín hiệu vào của mình trên `custom_exit````python
def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
    dataframe["enter_tag"] = ""
    signal_rsi = (qtpylib.crossed_above(dataframe["rsi"], 35))
    signal_bblower = (dataframe["bb_lowerband"] < dataframe["close"])
    # Additional conditions
    dataframe.loc[
        (
            signal_rsi
            | signal_bblower
            # ... additional signals to enter a long position
        )
        & (dataframe["volume"] > 0)
            , "enter_long"
        ] = 1
    # Concatenate the tags so all signals are kept
    dataframe.loc[signal_rsi, "enter_tag"] += "long_signal_rsi "
    dataframe.loc[signal_bblower, "enter_tag"] += "long_signal_bblower "

    return dataframe

def custom_exit(self, pair: str, trade: Trade, current_time: datetime, current_rate: float,
                current_profit: float, **kwargs):
    dataframe, _ = self.dp.get_analyzed_dataframe(pair, self.timeframe)
    last_candle = dataframe.iloc[-1].squeeze()
    if "long_signal_rsi" in trade.enter_tag and last_candle["rsi"] > 80:
        return "exit_signal_rsi"
    if "long_signal_bblower" in trade.enter_tag and last_candle["high"] > last_candle["bb_upperband"]:
        return "exit_signal_bblower"
    # ...
    return None

```!!! Lưu ý
    `enter_tag` được giới hạn ở 255 ký tự, dữ liệu còn lại sẽ bị cắt bớt.

!!! Cảnh báo
    Chỉ có một cột `enter_tag`, được sử dụng cho cả giao dịch mua và bán.
    Do đó, cột này phải được coi là "lần ghi cuối cùng thắng" (rốt cuộc nó chỉ là một cột khung dữ liệu).
    Trong các tình huống lạ, khi nhiều tín hiệu xung đột với nhau (hoặc nếu tín hiệu bị vô hiệu hóa lại dựa trên các điều kiện khác nhau), điều này có thể dẫn đến kết quả kỳ lạ khi áp dụng thẻ sai cho tín hiệu vào.
    Những kết quả này là kết quả của chiến lược ghi đè các thẻ trước đó - trong đó thẻ cuối cùng sẽ "dính" và sẽ là thẻ mà freqtrade sẽ sử dụng.

##Thẻ thoát

Tương tự như [Gắn thẻ mục nhập](#enter-tag), bạn cũng có thể chỉ định thẻ thoát.``` python
def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
    dataframe["exit_tag"] = ""
    rsi_exit_signal = (dataframe["rsi"] > 70)
    ema_exit_signal  = (dataframe["ema20"] < dataframe["ema50"])
    # Additional conditions
    dataframe.loc[
        (
            rsi_exit_signal
            | ema_exit_signal
            # ... additional signals to exit a long position
        ) &
        (dataframe["volume"] > 0)
        ,
    "exit_long"] = 1
    # Concatenate the tags so all signals are kept
    dataframe.loc[rsi_exit_signal, "exit_tag"] += "exit_signal_rsi "
    dataframe.loc[rsi_exit_signal2, "exit_tag"] += "exit_signal_rsi "

    return dataframe
```Sau đó, thẻ thoát được cung cấp sẽ được sử dụng làm lý do thoát - và được hiển thị như vậy trong kết quả kiểm tra ngược.

!!! Lưu ý
    `exit_reason` được giới hạn ở 100 ký tự, dữ liệu còn lại sẽ bị cắt bớt.

##Phiên bản chiến lược

Bạn có thể triển khai lập phiên bản chiến lược tùy chỉnh bằng cách sử dụng phương pháp "phiên bản" và trả về phiên bản bạn muốn có cho chiến lược này.``` python
def version(self) -> str:
    """
    Returns version of the strategy.
    """
    return "1.1"
```!!! Lưu ý
    Bạn nên đảm bảo triển khai kiểm soát phiên bản phù hợp (như kho git) cùng với điều này, vì freqtrade sẽ không giữ các phiên bản lịch sử của chiến lược của bạn, do đó, cuối cùng người dùng có thể quay lại phiên bản trước của chiến lược hay không.

## Chiến lược phái sinh

Các chiến lược có thể được bắt nguồn từ các chiến lược khác. Điều này tránh trùng lặp mã chiến lược tùy chỉnh của bạn. Bạn có thể sử dụng kỹ thuật này để ghi đè các phần nhỏ trong chiến lược chính của mình, giữ nguyên phần còn lại:``` python title="user_data/strategies/myawesomestrategy.py"
class MyAwesomeStrategy(IStrategy):
    ...
    stoploss = 0.13
    trailing_stop = False
    # All other attributes and methods are here as they
    # should be in any custom strategy...
    ...

`````` python title="user_data/strategies/MyAwesomeStrategy2.py"
from myawesomestrategy import MyAwesomeStrategy
class MyAwesomeStrategy2(MyAwesomeStrategy):
    # Override something
    stoploss = 0.08
    trailing_stop = True
```Cả thuộc tính và phương thức đều có thể bị ghi đè, thay đổi hành vi của chiến lược ban đầu theo cách bạn cần.

Mặc dù về mặt kỹ thuật, việc giữ lớp con trong cùng một tệp là có thể, nhưng điều này có thể dẫn đến một số vấn đề với các tệp tham số hyperopt, do đó chúng tôi khuyên bạn nên sử dụng các tệp chiến lược riêng biệt và nhập chiến lược gốc như được hiển thị ở trên.

## Chiến lược nhúng

Freqtrade cung cấp cho bạn một cách dễ dàng để nhúng chiến lược vào tệp cấu hình của bạn.
Điều này được thực hiện bằng cách sử dụng mã hóa BASE64 và cung cấp chuỗi này tại trường cấu hình chiến lược,
trong tập tin cấu hình bạn đã chọn.

### Mã hóa chuỗi thành BASE64

Đây là một ví dụ nhanh về cách tạo chuỗi BASE64 trong python```python
from base64 import urlsafe_b64encode

with open(file, 'r') as f:
    content = f.read()
content = urlsafe_b64encode(content.encode('utf-8'))
```Biến 'nội dung' sẽ chứa tệp chiến lược ở dạng được mã hóa BASE64. Bây giờ có thể được đặt trong tệp cấu hình của bạn như sau```json
"strategy": "NameOfStrategy:BASE64String"
```Vui lòng đảm bảo rằng 'NameOfStrategy' giống với tên chiến lược!

## Cảnh báo hiệu suất

Khi thực hiện một chiến lược, đôi khi người ta có thể được chào đón bởi những điều sau đây trong nhật ký

> Cảnh báo hiệu suất: DataFrame bị phân mảnh cao.This is a warning from [`pandas`](https://github.com/pandas-dev/pandas) and as the warning continues to say:
sử dụng `pd.concat(axis=1)`.
Điều này có thể có tác động nhỏ đến hiệu suất, thường chỉ hiển thị trong quá trình hyperopt (khi tối ưu hóa một chỉ báo).

Ví dụ:```python
for val in self.buy_ema_short.range:
    dataframe[f'ema_short_{val}'] = ta.EMA(dataframe, timeperiod=val)
```nên được viết lại thành```python
frames = [dataframe]
for val in self.buy_ema_short.range:
    frames.append(DataFrame({
        f'ema_short_{val}': ta.EMA(dataframe, timeperiod=val)
    }))

# Combine all dataframes, and reassign the original dataframe column
dataframe = pd.concat(frames, axis=1)
```Tuy nhiên, Freqtrade cũng chống lại điều này bằng cách chạy `dataframe.copy()` trên khung dữ liệu ngay sau phương thức `populate_indicators()` - vì vậy hiệu suất của điều này sẽ ở mức thấp đến không tồn tại.