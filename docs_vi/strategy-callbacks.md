<!-- Auto-translated from docs/ by script. Please review technical terms. -->

# Lệnh gọi lại chiến lược

Mặc dù các chức năng chiến lược chính (`populate_indicators()`, `populate_entry_trend()`, `populate_exit_trend()`) nên được sử dụng theo cách vector hóa và chỉ được gọi [một lần trong quá trình kiểm tra ngược](bot-basics.md#backtesting-hyperopt-execution-logic), lệnh gọi lại được gọi là "bất cứ khi nào cần".

Vì vậy, bạn nên tránh thực hiện các phép tính nặng nề trong lệnh gọi lại để tránh sự chậm trễ trong quá trình thao tác.
Tùy thuộc vào lệnh gọi lại được sử dụng, chúng có thể được gọi khi vào/ra giao dịch hoặc trong suốt thời gian giao dịch.

Các cuộc gọi lại hiện có sẵn:

* [`bot_start()`](#bot-start)
* [`bot_loop_start()`](#bot-loop-start)
* [`custom_stake_amount()`](#stake-size-management)
* [`custom_exit()`](#custom-exit-signal)
* [`custom_stoploss()`](#custom-stoploss)
* [`custom_roi()`](#custom-roi)
* [`custom_entry_price()` và `custom_exit_price()`](#custom-order-price-rules)
* [`check_entry_timeout()` và `check_exit_timeout()`](#custom-order-timeout-rules)
* [`confirm_trade_entry()`](#trade-entry-buy-order-confirmation)
* [`confirm_trade_exit()`](#trade-exit-sell-order-confirmation)
* [`điều chỉnh_trade_position()`](#điều chỉnh-giao dịch-vị trí)
* [`điều chỉnh_entry_price()`](#điều chỉnh-giá nhập)
* [`đòn bẩy()`](#đòn bẩy-gọi lại)
* [`order_filled()`](#order-filled-callback)

!!! Tip "Callback calling sequence"
    Bạn có thể tìm thấy trình tự gọi lại trong [bot-basics](bot-basics.md#bot-execution-logic)

--8<-- "bao gồm/strategy-imports.md"

--8<-- "bao gồm/strategy-exit-comparisons.md"


## Khởi động bot

Một cuộc gọi lại đơn giản được gọi một lần khi chiến lược được tải.
Điều này có thể được sử dụng để thực hiện các hành động chỉ được thực hiện một lần và chạy sau khi nhà cung cấp dữ liệu và ví được đặt``` python
import requests

class AwesomeStrategy(IStrategy):

    # ... populate_* methods

    def bot_start(self, **kwargs) -> None:
        """
        Called only once after bot instantiation.
        :param **kwargs: Ensure to keep this here so updates to this won't break your strategy.
        """
        if self.config["runmode"].value in ("live", "dry_run"):
            # Assign this to the class by using self.*
            # can then be used by populate_* methods
            self.custom_remote_data = requests.get("https://some_remote_source.example.com")

```Trong hyperopt, điều này chỉ chạy một lần khi khởi động.

## Bắt đầu vòng lặp Bot

Một lệnh gọi lại đơn giản được gọi một lần khi bắt đầu mỗi vòng lặp điều chỉnh bot ở chế độ khô/trực tiếp (khoảng 5 lần một lần)
giây, trừ khi được định cấu hình khác) hoặc một lần trên mỗi nến ở chế độ backtest/hyperopt.
Điều này có thể được sử dụng để thực hiện các phép tính độc lập với từng cặp (áp dụng cho tất cả các cặp), tải dữ liệu ngoài, v.v.``` python
# Default imports
import requests

class AwesomeStrategy(IStrategy):

    # ... populate_* methods

    def bot_loop_start(self, current_time: datetime, **kwargs) -> None:
        """
        Called at the start of the bot iteration (one loop).
        Might be used to perform pair-independent tasks
        (e.g. gather some remote resource for comparison)
        :param current_time: datetime object, containing the current datetime
        :param **kwargs: Ensure to keep this here so updates to this won't break your strategy.
        """
        if self.config["runmode"].value in ("live", "dry_run"):
            # Assign this to the class by using self.*
            # can then be used by populate_* methods
            self.remote_data = requests.get("https://some_remote_source.example.com")

```## Quản lý quy mô cổ phần

Được gọi trước khi tham gia giao dịch, giúp bạn có thể quản lý quy mô vị thế của mình khi đặt giao dịch mới.```python
# Default imports

class AwesomeStrategy(IStrategy):
    def custom_stake_amount(self, pair: str, current_time: datetime, current_rate: float,
                            proposed_stake: float, min_stake: float | None, max_stake: float,
                            leverage: float, entry_tag: str | None, side: str,
                            **kwargs) -> float:

        dataframe, _ = self.dp.get_analyzed_dataframe(pair=pair, timeframe=self.timeframe)
        current_candle = dataframe.iloc[-1].squeeze()

        if current_candle["fastk_rsi_1h"] > current_candle["fastd_rsi_1h"]:
            if self.config["stake_amount"] == "unlimited":
                # Use entire available wallet during favorable conditions when in compounding mode.
                return max_stake
            else:
                # Compound profits during favorable conditions instead of using a static stake.
                return self.wallets.get_total_stake_amount() / self.config["max_open_trades"]

        # Use default stake amount.
        return proposed_stake
```Freqtrade sẽ quay trở lại giá trị `proposed_stake` nếu mã của bạn có ngoại lệ. Bản thân ngoại lệ sẽ được ghi lại.

!!! Mẹo
    Bạn không _have_ đảm bảo rằng `min_stake <= return_value <= max_stake`. Giao dịch sẽ thành công vì giá trị trả về sẽ được giới hạn trong phạm vi được hỗ trợ và hành động này sẽ được ghi lại.

!!! Mẹo
    Trả về `0` hoặc `Không` sẽ ngăn cản việc thực hiện giao dịch.

## Tín hiệu thoát tùy chỉnh

Yêu cầu giao dịch mở mỗi lần lặp lại điều chỉnh (khoảng 5 giây một lần) cho đến khi giao dịch được đóng.

Cho phép xác định các tín hiệu thoát tùy chỉnh, cho biết vị trí đã chỉ định sẽ bị đóng (thoát hoàn toàn). Điều này rất hữu ích khi chúng ta cần tùy chỉnh các điều kiện thoát cho từng giao dịch riêng lẻ hoặc nếu bạn cần dữ liệu giao dịch để đưa ra quyết định thoát.

Ví dụ: bạn có thể triển khai ROI thưởng rủi ro 1:2 với `custom_exit()`.

Tuy nhiên, việc sử dụng tín hiệu `custom_exit()` thay cho lệnh dừng lỗ *không được khuyến khích*. Về mặt này, đây là một phương pháp kém hơn so với việc sử dụng `custom_stoploss()` - phương pháp này cũng cho phép bạn giữ mức dừng lỗ khi trao đổi.

!!! Lưu ý
    Trả về một `chuỗi` hoặc `True` (không trống) từ phương thức này tương đương với việc đặt tín hiệu thoát trên nến tại thời điểm đã chỉ định. Phương thức này không được gọi khi tín hiệu thoát đã được đặt hoặc nếu tín hiệu thoát bị tắt (`use_exit_signal=False`). Độ dài tối đa của `string` là 64 ký tự. Vượt quá giới hạn này sẽ khiến tin nhắn bị cắt ngắn còn 64 ký tự.
    `custom_exit()` sẽ bỏ qua `exit_profit_only` và sẽ luôn được gọi trừ khi `use_exit_signal=False`, ngay cả khi có tín hiệu nhập mới.

Một ví dụ về cách chúng ta có thể sử dụng các chỉ báo khác nhau tùy thuộc vào lợi nhuận hiện tại và cũng có thể thoát các giao dịch được mở lâu hơn một ngày:``` python
# Default imports

class AwesomeStrategy(IStrategy):
    def custom_exit(self, pair: str, trade: Trade, current_time: datetime, current_rate: float,
                    current_profit: float, **kwargs):
        dataframe, _ = self.dp.get_analyzed_dataframe(pair, self.timeframe)
        last_candle = dataframe.iloc[-1].squeeze()

        # Above 20% profit, sell when rsi < 80
        if current_profit > 0.2:
            if last_candle["rsi"] < 80:
                return "rsi_below_80"

        # Between 2% and 10%, sell if EMA-long above EMA-short
        if 0.02 < current_profit < 0.1:
            if last_candle["emalong"] > last_candle["emashort"]:
                return "ema_long_below_80"

        # Sell any positions at a loss if they are held for more than one day.
        if current_profit < 0.0 and (current_time - trade.open_date_utc).days >= 1:
            return "unclog"
```Xem [Truy cập khung dữ liệu](strategy-advanced.md#dataframe-access) để biết thêm thông tin về việc sử dụng khung dữ liệu trong lệnh gọi lại chiến lược.

## Dừng lỗ tùy chỉnh

Yêu cầu mở giao dịch mỗi lần lặp lại (khoảng 5 giây một lần) cho đến khi giao dịch được đóng lại.

Việc sử dụng phương pháp dừng lỗ tùy chỉnh phải được bật bằng cách đặt `use_custom_stoploss=True` trên đối tượng chiến lược.

Giá dừng lỗ chỉ có thể tăng lên - nếu giá trị dừng lỗ được trả về từ `custom_stoploss` dẫn đến giá dừng lỗ thấp hơn mức đã đặt trước đó thì giá đó sẽ bị bỏ qua. Giá trị `stoploss` truyền thống đóng vai trò là mức thấp hơn tuyệt đối và sẽ được đặt làm mức dừng lỗ ban đầu (trước khi phương thức này được gọi lần đầu tiên cho giao dịch) và vẫn là bắt buộc.  
Vì mức dừng lỗ tùy chỉnh hoạt động như bình thường, khi thay đổi mức dừng lỗ, nó sẽ hoạt động tương tự như `trailing_stop` - và các giao dịch thoát do điều này sẽ có exit_reason là `"trailing_stop_loss"`.

Phương thức phải trả về giá trị dừng lỗ (float/number) dưới dạng phần trăm của giá hiện tại.
Ví dụ. Nếu `tỷ giá_hiện tại` là 200 USD thì việc trả về `0,02` sẽ đặt giá dừng lỗ thấp hơn 2%, ở mức 196 USD.
Trong quá trình kiểm tra ngược, `current_rate` (và `current_profit`) được cung cấp so với mức cao nhất của nến (hoặc mức thấp đối với các giao dịch bán khống) - trong khi mức dừng lỗ thu được được đánh giá so với mức thấp nhất của nến (hoặc mức cao đối với các giao dịch bán khống).

Giá trị tuyệt đối của giá trị trả về được sử dụng (dấu bị bỏ qua), do đó, trả về `0,05` hoặc `-0,05` có cùng kết quả, mức dừng lỗ thấp hơn 5% so với giá hiện tại.
Trả về `Không` sẽ được hiểu là "không muốn thay đổi" và là cách an toàn duy nhất để quay lại khi bạn không muốn sửa đổi điểm dừng.
Các giá trị `NaN` và `inf` được coi là không hợp lệ và sẽ bị bỏ qua (giống hệt với `None`).

Lệnh dừng lỗ trên sàn giao dịch hoạt động tương tự như `trailing_stop` và lệnh dừng lỗ trên sàn giao dịch được cập nhật như được định cấu hình trong `stoploss_on_exchange_interval` ([Thêm chi tiết về lệnh dừng lỗ trên sàn giao dịch](stoploss.md#stop-loss-on-exchangefreqtrade)).

Nếu bạn tham gia thị trường hợp đồng tương lai, vui lòng lưu ý phần [điểm dừng lỗ và đòn bẩy](stoploss.md#stoploss-and-leverage), vì giá trị điểm dừng lỗ được trả về từ `custom_stoploss` là rủi ro cho giao dịch này - không phải là biến động giá tương đối.

!!! Lưu ý "Sử dụng ngày tháng"
    Tất cả các phép tính dựa trên thời gian phải được thực hiện dựa trên `current_time` - không khuyến khích sử dụng `datetime.now()` hoặc `datetime.utcnow()` vì điều này sẽ phá vỡ hỗ trợ kiểm tra lại.

!!! Mẹo "Dừng lỗ"
    Bạn nên tắt `trailing_stop` khi sử dụng các giá trị dừng lỗ tùy chỉnh. Cả hai có thể hoạt động song song, nhưng bạn có thể gặp phải điểm dừng cuối để đẩy giá lên cao hơn trong khi chức năng tùy chỉnh của bạn không muốn điều này, gây ra hành vi xung đột.

### Điều chỉnh mức dừng lỗ sau khi điều chỉnh vị thế

Tùy thuộc vào chiến lược của bạn, bạn có thể cần phải điều chỉnh mức dừng lỗ theo cả hai hướng sau khi [điều chỉnh vị trí](#điều chỉnh-giao dịch-vị trí).
Đối với điều này, freqtrade sẽ thực hiện lệnh gọi bổ sung với `after_fill=True` sau khi lệnh được thực hiện, điều này sẽ cho phép chiến lược di chuyển điểm dừng theo bất kỳ hướng nào (đồng thời mở rộng khoảng cách giữa điểm dừng và giá hiện tại, điều này bị cấm).

!!! Lưu ý "khả năng tương thích ngược"
    Lệnh gọi này sẽ chỉ được thực hiện nếu tham số `after_fill` là một phần trong định nghĩa hàm của hàm `custom_stoploss` của bạn.
    Như vậy, điều này sẽ không ảnh hưởng (và cùng với đó là điều đáng ngạc nhiên) các chiến lược đang hoạt động hiện có.

### Ví dụ về mức dừng lỗ tùy chỉnhPhần tiếp theo sẽ hiển thị một số ví dụ về những gì có thể thực hiện được với chức năng dừng lỗ tùy chỉnh.
Tất nhiên, còn nhiều điều nữa có thể xảy ra và tất cả các ví dụ đều có thể được kết hợp theo ý muốn.

#### Trailing stop thông qua stoploss tùy chỉnh

Để mô phỏng mức dừng lỗ kéo dài thông thường là 4% (giảm 4% so với mức giá đạt tối đa), bạn sẽ sử dụng phương pháp rất đơn giản sau:``` python
# Default imports

class AwesomeStrategy(IStrategy):

    # ... populate_* methods

    use_custom_stoploss = True

    def custom_stoploss(self, pair: str, trade: Trade, current_time: datetime,
                        current_rate: float, current_profit: float, after_fill: bool, 
                        **kwargs) -> float | None:
        """
        Custom stoploss logic, returning the new distance relative to current_rate (as ratio).
        e.g. returning -0.05 would create a stoploss 5% below current_rate.
        The custom stoploss can never be below self.stoploss, which serves as a hard maximum loss.

        For full documentation please go to https://www.freqtrade.io/en/stable/strategy-advanced/

        When not implemented by a strategy, returns the initial stoploss value.
        Only called when use_custom_stoploss is set to True.

        :param pair: Pair that's currently analyzed
        :param trade: trade object.
        :param current_time: datetime object, containing the current datetime
        :param current_rate: Rate, calculated based on pricing settings in exit_pricing.
        :param current_profit: Current profit (as ratio), calculated based on current_rate.
        :param after_fill: True if the stoploss is called after the order was filled.
        :param **kwargs: Ensure to keep this here so updates to this won't break your strategy.
        :return float: New stoploss value, relative to the current_rate
        """
        return -0.04 * trade.leverage
```#### Điểm dừng theo thời gian

Sử dụng mức dừng lỗ ban đầu trong 60 phút đầu tiên, sau khi thay đổi thành mức dừng lỗ kéo dài 10% và sau 2 giờ (120 phút), chúng tôi sử dụng mức dừng lỗ kéo dài 5%.``` python
# Default imports

class AwesomeStrategy(IStrategy):

    # ... populate_* methods

    use_custom_stoploss = True

    def custom_stoploss(self, pair: str, trade: Trade, current_time: datetime,
                        current_rate: float, current_profit: float, after_fill: bool, 
                        **kwargs) -> float | None:

        # Make sure you have the longest interval first - these conditions are evaluated from top to bottom.
        if current_time - timedelta(minutes=120) > trade.open_date_utc:
            return -0.05 * trade.leverage
        elif current_time - timedelta(minutes=60) > trade.open_date_utc:
            return -0.10 * trade.leverage
        return None
```#### Dừng theo dõi dựa trên thời gian với các điều chỉnh sau khi điền

Sử dụng mức dừng lỗ ban đầu trong 60 phút đầu tiên, sau khi thay đổi thành mức dừng lỗ kéo dài 10% và sau 2 giờ (120 phút), chúng tôi sử dụng mức dừng lỗ kéo dài 5%.
Nếu một lệnh bổ sung được thực hiện, hãy đặt mức dừng lỗ ở mức -10% dưới mức `open_rate` mới ([Tính trung bình trên tất cả các mục](#position-điều chỉnh-tính toán)).``` python
# Default imports

class AwesomeStrategy(IStrategy):

    # ... populate_* methods

    use_custom_stoploss = True

    def custom_stoploss(self, pair: str, trade: Trade, current_time: datetime,
                        current_rate: float, current_profit: float, after_fill: bool, 
                        **kwargs) -> float | None:

        if after_fill: 
            # After an additional order, start with a stoploss of 10% below the new open rate
            return stoploss_from_open(0.10, current_profit, is_short=trade.is_short, leverage=trade.leverage)
        # Make sure you have the longest interval first - these conditions are evaluated from top to bottom.
        if current_time - timedelta(minutes=120) > trade.open_date_utc:
            return -0.05 * trade.leverage
        elif current_time - timedelta(minutes=60) > trade.open_date_utc:
            return -0.10 * trade.leverage
        return None
```#### Điểm dừng khác nhau cho mỗi cặp

Sử dụng mức dừng lỗ khác nhau tùy thuộc vào cặp.
Trong ví dụ này, chúng tôi sẽ theo dõi mức giá cao nhất với mức dừng lỗ kéo dài 10% cho `ETH/BTC` và `XRP/BTC`, với mức dừng lỗ kéo dài 5% cho `LTC/BTC` và với 15% cho tất cả các cặp khác.``` python
# Default imports

class AwesomeStrategy(IStrategy):

    # ... populate_* methods

    use_custom_stoploss = True

    def custom_stoploss(self, pair: str, trade: Trade, current_time: datetime,
                        current_rate: float, current_profit: float, after_fill: bool,
                        **kwargs) -> float | None:

        if pair in ("ETH/BTC", "XRP/BTC"):
            return -0.10 * trade.leverage
        elif pair in ("LTC/BTC"):
            return -0.05 * trade.leverage
        return -0.15 * trade.leverage
```#### Dừng lỗ kéo dài với mức bù dương

Sử dụng mức dừng lỗ ban đầu cho đến khi lợi nhuận trên 4%, sau đó sử dụng mức dừng lỗ kéo dài 50% lợi nhuận hiện tại với mức tối thiểu là 2,5% và tối đa là 5%.

Xin lưu ý rằng mức dừng lỗ chỉ có thể tăng lên, các giá trị thấp hơn mức dừng lỗ hiện tại sẽ bị bỏ qua.``` python
# Default imports

class AwesomeStrategy(IStrategy):

    # ... populate_* methods

    use_custom_stoploss = True

    def custom_stoploss(self, pair: str, trade: Trade, current_time: datetime,
                        current_rate: float, current_profit: float, after_fill: bool,
                        **kwargs) -> float | None:

        if current_profit < 0.04:
            return None # return None to keep using the initial stoploss

        # After reaching the desired offset, allow the stoploss to trail by half the profit
        desired_stoploss = current_profit / 2

        # Use a minimum of 2.5% and a maximum of 5%
        return max(min(desired_stoploss, 0.05), 0.025) * trade.leverage
```#### Dừng lỗ theo bước

Thay vì liên tục theo sau giá hiện tại, ví dụ này đặt mức giá dừng lỗ cố định dựa trên lợi nhuận hiện tại.

* Sử dụng mức dừng lỗ thông thường cho đến khi đạt được lợi nhuận 20%
* Khi lợi nhuận > 20% - đặt mức dừng lỗ cao hơn 7% so với giá mở.
* Khi lợi nhuận > 25% - đặt mức dừng lỗ cao hơn 15% so với giá mở.
* Khi lợi nhuận > 40% - đặt mức dừng lỗ ở mức 25% so với giá mở.``` python
# Default imports

class AwesomeStrategy(IStrategy):

    # ... populate_* methods

    use_custom_stoploss = True

    def custom_stoploss(self, pair: str, trade: Trade, current_time: datetime,
                        current_rate: float, current_profit: float, after_fill: bool,
                        **kwargs) -> float | None:

        # evaluate highest to lowest, so that highest possible stop is used
        if current_profit > 0.40:
            return stoploss_from_open(0.25, current_profit, is_short=trade.is_short, leverage=trade.leverage)
        elif current_profit > 0.25:
            return stoploss_from_open(0.15, current_profit, is_short=trade.is_short, leverage=trade.leverage)
        elif current_profit > 0.20:
            return stoploss_from_open(0.07, current_profit, is_short=trade.is_short, leverage=trade.leverage)

        # return maximum stoploss value, keeping current stoploss price unchanged
        return None
```#### Dừng lỗ tùy chỉnh bằng cách sử dụng chỉ báo từ ví dụ về khung dữ liệu

Giá trị dừng lỗ tuyệt đối có thể được lấy từ các chỉ báo được lưu trữ trong khung dữ liệu. Ví dụ sử dụng SAR parabol dưới mức giá làm điểm dừng lỗ.``` python
# Default imports

class AwesomeStrategy(IStrategy):

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # <...>
        dataframe["sar"] = ta.SAR(dataframe)

    use_custom_stoploss = True

    def custom_stoploss(self, pair: str, trade: Trade, current_time: datetime,
                        current_rate: float, current_profit: float, after_fill: bool,
                        **kwargs) -> float | None:

        dataframe, _ = self.dp.get_analyzed_dataframe(pair, self.timeframe)
        last_candle = dataframe.iloc[-1].squeeze()

        # Use parabolic sar as absolute stoploss price
        stoploss_price = last_candle["sar"]

        # Convert absolute price to percentage relative to current_rate
        if stoploss_price < current_rate:
            return stoploss_from_absolute(stoploss_price, current_rate, is_short=trade.is_short)

        # return maximum stoploss value, keeping current stoploss price unchanged
        return None
```Xem [Truy cập khung dữ liệu](strategy-advanced.md#dataframe-access) để biết thêm thông tin về việc sử dụng khung dữ liệu trong lệnh gọi lại chiến lược.

### Những công cụ trợ giúp phổ biến để tính toán mức dừng lỗ

#### Dừng lỗ so với giá mở cửa

Các giá trị dừng lỗ được trả về từ `custom_stoploss()` phải chỉ định phần trăm tương ứng với `current_rate`, nhưng thay vào đó, đôi khi bạn có thể muốn chỉ định mức dừng lỗ tương ứng với giá _entry_.
`stoploss_from_open()` là một hàm trợ giúp để tính toán giá trị dừng lỗ có thể được trả về từ `custom_stoploss`, giá trị này sẽ tương đương với lợi nhuận giao dịch mong muốn trên điểm vào lệnh.

??? Ví dụ "Trả về điểm dừng liên quan đến giá mở từ chức năng dừng lỗ tùy chỉnh"

    Giả sử giá mở là 100 USD và `current_price` là 121 USD (`current_profit` sẽ là `0,21`).  

    Nếu chúng tôi muốn giá dừng ở mức cao hơn 7% so với giá mở, chúng tôi có thể gọi `stoploss_from_open(0,07, current_profit, False)` và sẽ trả về `0,1157024793`.  11,57% dưới 121 USD là 107 USD, tương đương với 7% trên 100 USD.

    Hàm này sẽ xem xét đòn bẩy - vì vậy với đòn bẩy gấp 10 lần, mức dừng lỗ thực tế sẽ là 0,7% trên 100 USD (0,7% * 10x = 7%).``` python
    # Default imports

    class AwesomeStrategy(IStrategy):

        # ... populate_* methods

        use_custom_stoploss = True

        def custom_stoploss(self, pair: str, trade: Trade, current_time: datetime,
                            current_rate: float, current_profit: float, after_fill: bool,
                            **kwargs) -> float | None:

            # once the profit has risen above 10%, keep the stoploss at 7% above the open price
            if current_profit > 0.10:
                return stoploss_from_open(0.07, current_profit, is_short=trade.is_short, leverage=trade.leverage)

            return 1

    ```Bạn có thể tìm thấy ví dụ đầy đủ trong phần [Cắt lỗ tùy chỉnh](strategy-callbacks.md#custom-stoploss) của Tài liệu.

!!! Lưu ý
    Việc cung cấp thông tin đầu vào không hợp lệ cho `stoploss_from_open()` có thể tạo ra cảnh báo "Hàm CustomStoploss không trả về mức dừng lỗ hợp lệ".
    Điều này có thể xảy ra nếu tham số `current_profit` ở dưới mức `open_relative_stop` được chỉ định. Những tình huống như vậy có thể phát sinh khi đóng giao dịch
    bị chặn bởi phương thức `confirm_trade_exit()`. Cảnh báo có thể được giải quyết bằng cách không bao giờ chặn lệnh dừng lỗ bán bằng cách chọn `exit_reason` trong
    `confirm_trade_exit()` hoặc bằng cách sử dụng thành ngữ `return stoploss_from_open(...) hoặc 1`, sẽ yêu cầu không thay đổi mức dừng lỗ khi
    `lợi nhuận hiện tại < open_relative_stop`.

#### Tỷ lệ dừng lỗ so với giá tuyệt đối

Các giá trị dừng lỗ được trả về từ `custom_stoploss()` luôn chỉ định phần trăm tương ứng với `current_rate`. Để đặt mức dừng lỗ ở mức giá tuyệt đối được chỉ định, chúng ta cần sử dụng `stop_rate` để tính toán tỷ lệ phần trăm nào so với `current_rate` sẽ cho bạn kết quả tương tự như khi tỷ lệ phần trăm được chỉ định từ giá mở.

Hàm trợ giúp `stoploss_from_absolute()` có thể được sử dụng để chuyển đổi từ giá tuyệt đối sang giá dừng tương đối ở mức giá hiện tại mà có thể được trả về từ `custom_stoploss()`.

??? Ví dụ "Trả về điểm dừng sử dụng giá tuyệt đối từ hàm dừng lỗ tùy chỉnh"

    Nếu chúng ta muốn theo dõi giá dừng ở mức 2xATR dưới mức giá hiện tại, chúng ta có thể gọi `stoploss_from_absolute(current_rate + (side * Candle["atr"] * 2), current_rate=current_rate, is_short=trade.is_short, đòn bẩy=trade.leverage)`.
    Đối với hợp đồng tương lai, chúng ta cần điều chỉnh hướng (lên hoặc xuống), cũng như điều chỉnh đòn bẩy, vì lệnh gọi lại [`custom_stoploss`](strategy-callbacks.md#custom-stoploss) trả về ["rủi ro cho giao dịch này"](stoploss.md#stoploss-and-leverage) - không phải chuyển động giá tương đối.``` python
    # Default imports

    class AwesomeStrategy(IStrategy):

        use_custom_stoploss = True

        def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
            dataframe["atr"] = ta.ATR(dataframe, timeperiod=14)
            return dataframe

        def custom_stoploss(self, pair: str, trade: Trade, current_time: datetime,
                            current_rate: float, current_profit: float, after_fill: bool,
                            **kwargs) -> float | None:
            dataframe, _ = self.dp.get_analyzed_dataframe(pair, self.timeframe)
            trade_date = timeframe_to_prev_date(self.timeframe, trade.open_date_utc)
            candle = dataframe.iloc[-1].squeeze()
            side = 1 if trade.is_short else -1
            return stoploss_from_absolute(current_rate + (side * candle["atr"] * 2), 
                                          current_rate=current_rate, 
                                          is_short=trade.is_short,
                                          leverage=trade.leverage)

    ```---

## ROI tùy chỉnh

Yêu cầu mở giao dịch mỗi lần lặp lại (khoảng 5 giây một lần) cho đến khi giao dịch được đóng lại.

Việc sử dụng phương pháp ROI tùy chỉnh phải được bật bằng cách đặt `use_custom_roi=True` trên đối tượng chiến lược.

Phương pháp này cho phép bạn xác định ngưỡng ROI tối thiểu tùy chỉnh để thoát giao dịch, được biểu thị dưới dạng tỷ lệ (ví dụ: `0,05` cho lợi nhuận 5%). Nếu cả `minimal_roi` và `custom_roi` đều được xác định, ngưỡng thấp hơn trong hai ngưỡng sẽ kích hoạt thoát. Ví dụ: nếu `minimal_roi` được đặt thành `{"0": 0,10}` (10% sau 0 phút) và `custom_roi` trả về `0,05`, giao dịch sẽ thoát khi lợi nhuận đạt 5%. Ngoài ra, nếu `custom_roi` trả về `0,10` và `minimal_roi` được đặt thành `{"0": 0,05}` (5% sau 0 phút), giao dịch sẽ đóng khi lợi nhuận đạt 5%.

Phương thức này phải trả về một số float biểu thị ngưỡng ROI mới dưới dạng tỷ lệ hoặc `None` để quay lại logic `minimal_roi`. Việc trả về giá trị `NaN` hoặc `inf` được coi là không hợp lệ và sẽ được coi là `None`, khiến bot sử dụng cấu hình `minimal_roi`.

### Ví dụ về ROI tùy chỉnh

Các ví dụ sau minh họa cách sử dụng hàm `custom_roi` để triển khai các logic ROI khác nhau.

#### ROI tùy chỉnh mỗi bên

Sử dụng các ngưỡng ROI khác nhau tùy thuộc vào `bên`. Trong ví dụ này, 5% cho các mục dài và 2% cho các mục ngắn.```python
# Default imports

class AwesomeStrategy(IStrategy):

    use_custom_roi = True

    # ... populate_* methods

    def custom_roi(self, pair: str, trade: Trade, current_time: datetime, trade_duration: int,
                   entry_tag: str | None, side: str, **kwargs) -> float | None:
        """
        Custom ROI logic, returns a new minimum ROI threshold (as a ratio, e.g., 0.05 for +5%).
        Only called when use_custom_roi is set to True.

        If used at the same time as minimal_roi, an exit will be triggered when the lower
        threshold is reached. Example: If minimal_roi = {"0": 0.01} and custom_roi returns 0.05,
        an exit will be triggered if profit reaches 5%.

        :param pair: Pair that's currently analyzed.
        :param trade: trade object.
        :param current_time: datetime object, containing the current datetime.
        :param trade_duration: Current trade duration in minutes.
        :param entry_tag: Optional entry_tag (buy_tag) if provided with the buy signal.
        :param side: 'long' or 'short' - indicating the direction of the current trade.
        :param **kwargs: Ensure to keep this here so updates to this won't break your strategy.
        :return float: New ROI value as a ratio, or None to fall back to minimal_roi logic.
        """
        return 0.05 if side == "long" else 0.02
```#### ROI tùy chỉnh trên mỗi cặp

Sử dụng các ngưỡng ROI khác nhau tùy thuộc vào `cặp`.```python
# Default imports

class AwesomeStrategy(IStrategy):

    use_custom_roi = True

    # ... populate_* methods

    def custom_roi(self, pair: str, trade: Trade, current_time: datetime, trade_duration: int,
                   entry_tag: str | None, side: str, **kwargs) -> float | None:

        stake = trade.stake_currency
        roi_map = {
            f"BTC/{stake}": 0.02, # 2% for BTC
            f"ETH/{stake}": 0.03, # 3% for ETH
            f"XRP/{stake}": 0.04, # 4% for XRP
        }

        return roi_map.get(pair, 0.01) # 1% for any other pair
```#### ROI tùy chỉnh trên mỗi thẻ mục nhập

Sử dụng các ngưỡng ROI khác nhau tùy thuộc vào `entry_tag` được cung cấp cùng với tín hiệu mua.```python
# Default imports

class AwesomeStrategy(IStrategy):

    use_custom_roi = True

    # ... populate_* methods

    def custom_roi(self, pair: str, trade: Trade, current_time: datetime, trade_duration: int,
                   entry_tag: str | None, side: str, **kwargs) -> float | None:

        roi_by_tag = {
            "breakout": 0.08,       # 8% if tag is "breakout"
            "rsi_overbought": 0.05, # 5% if tag is "rsi_overbought"
            "mean_reversion": 0.03, # 3% if tag is "mean_reversion"
        }

        return roi_by_tag.get(entry_tag, 0.01)  # 1% if tag is unknown
```#### ROI tùy chỉnh dựa trên ATR

Giá trị ROI có thể được lấy từ các chỉ báo được lưu trữ trong khung dữ liệu. Ví dụ này sử dụng tỷ lệ ATR làm ROI.``` python
# Default imports
# <...>
import talib.abstract as ta

class AwesomeStrategy(IStrategy):

    use_custom_roi = True

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # <...>
        dataframe["atr"] = ta.ATR(dataframe, timeperiod=10)

    def custom_roi(self, pair: str, trade: Trade, current_time: datetime, trade_duration: int,
                   entry_tag: str | None, side: str, **kwargs) -> float | None:

        dataframe, _ = self.dp.get_analyzed_dataframe(pair, self.timeframe)
        last_candle = dataframe.iloc[-1].squeeze()
        atr_ratio = last_candle["atr"] / last_candle["close"]

        return atr_ratio # Returns the ATR value as ratio
```---

## Quy tắc đặt hàng tùy chỉnh

Theo mặc định, freqtrade sử dụng sổ đặt hàng để tự động đặt giá đặt hàng ([Tài liệu liên quan](configuration.md#prices-used-for-orders)), bạn cũng có tùy chọn tạo giá đặt hàng tùy chỉnh dựa trên chiến lược của mình.

Bạn có thể sử dụng tính năng này bằng cách tạo hàm `custom_entry_price()` trong tệp chiến lược của mình để tùy chỉnh giá vào lệnh và `custom_exit_price()` cho các điểm thoát.

Mỗi phương thức này đều được gọi ngay trước khi đặt lệnh trên sàn giao dịch.

!!! Lưu ý
    Nếu hàm đặt giá tùy chỉnh của bạn trả về Không có hoặc giá trị không hợp lệ thì giá sẽ quay trở lại `proposed_rate`, dựa trên cấu hình đặt giá thông thường.

!!! Lưu ý
    Khi sử dụng `custom_entry_price()`, đối tượng Giao dịch sẽ có sẵn ngay khi lệnh nhập đầu tiên liên quan đến giao dịch được tạo, đối với mục nhập đầu tiên, giá trị tham số `trade` sẽ là `None`.

### Ví dụ về giá vào và thoát lệnh tùy chỉnh``` python
# Default imports

class AwesomeStrategy(IStrategy):

    # ... populate_* methods

    def custom_entry_price(self, pair: str, trade: Trade | None, current_time: datetime, proposed_rate: float,
                           entry_tag: str | None, side: str, **kwargs) -> float:

        dataframe, last_updated = self.dp.get_analyzed_dataframe(pair=pair,
                                                                timeframe=self.timeframe)
        new_entryprice = dataframe["bollinger_10_lowerband"].iat[-1]

        return new_entryprice

    def custom_exit_price(self, pair: str, trade: Trade,
                          current_time: datetime, proposed_rate: float,
                          current_profit: float, exit_tag: str | None, **kwargs) -> float:

        dataframe, last_updated = self.dp.get_analyzed_dataframe(pair=pair,
                                                                timeframe=self.timeframe)
        new_exitprice = dataframe["bollinger_10_upperband"].iat[-1]

        return new_exitprice

```!!! Cảnh báo
    Việc sửa đổi giá vào và ra sẽ chỉ có tác dụng đối với các lệnh giới hạn. Tùy thuộc vào mức giá đã chọn, điều này có thể dẫn đến nhiều đơn hàng không được thực hiện. Theo mặc định, khoảng cách tối đa được phép giữa giá hiện tại và giá tùy chỉnh là 2%, giá trị này có thể được thay đổi trong cấu hình với thông số `custom_price_max_distance_ratio`.
    **Ví dụ**:
    Nếu new_entryprice là 97, thì giá_đề xuất là 100 và `tỷ lệ_giá_tối đa_khoảng cách_tùy chỉnh` được đặt thành 2%, Giá nhập tùy chỉnh hợp lệ được giữ lại sẽ là 98, thấp hơn 2% so với tỷ giá hiện tại (được đề xuất).

!!! Cảnh báo "Đang kiểm tra lại"
    Giá tùy chỉnh được hỗ trợ trong quá trình kiểm tra ngược (bắt đầu từ năm 2021.12) và các lệnh sẽ được thực hiện nếu giá nằm trong phạm vi thấp/cao của nến.
    Các đơn đặt hàng không được thực hiện ngay lập tức sẽ phải xử lý thời gian chờ thường xuyên, điều này xảy ra một lần cho mỗi nến (chi tiết).
    `custom_exit_price()` chỉ được gọi để bán loại exit_signal, Thoát tùy chỉnh và thoát một phần. Tất cả các loại thoát khác sẽ sử dụng giá kiểm tra ngược thông thường.

## Quy tắc hết thời gian đặt hàng tùy chỉnh

Thời gian chờ đặt hàng đơn giản, dựa trên thời gian có thể được định cấu hình thông qua chiến lược hoặc trong cấu hình trong phần `thời gian chờ chưa thực hiện`.

Tuy nhiên, freqtrade cũng cung cấp lệnh gọi lại tùy chỉnh cho cả hai loại đơn đặt hàng, cho phép bạn quyết định dựa trên tiêu chí tùy chỉnh xem đơn hàng có hết thời gian chờ hay không.

!!! Lưu ý
    Kiểm tra ngược sẽ thực hiện các lệnh nếu giá của chúng nằm trong phạm vi thấp/cao của nến.
    Lệnh gọi lại bên dưới sẽ được gọi một lần cho mỗi nến (chi tiết) đối với các đơn hàng không được thực hiện ngay lập tức (sử dụng giá tùy chỉnh).

!!! Mẹo "Thay thế đơn hàng"
    Nếu bạn muốn thay thế một đơn đặt hàng bằng một mức giá khác thay vì chỉ hủy đơn hàng đó, bạn có thể muốn xem [` adjustment_order_price()`](# adjustment-order-price), điều này sẽ cho phép bạn vừa hủy đơn hàng vừa thay thế nó bằng một mức giá mới.

### Ví dụ về thời gian chờ của đơn hàng tùy chỉnh

Được gọi cho mọi lệnh mở cho đến khi lệnh đó được khớp hoặc bị hủy.
`check_entry_timeout()` được gọi cho các mục nhập giao dịch, trong khi `check_exit_timeout()` được gọi cho các lệnh thoát giao dịch.

Bạn có thể xem bên dưới một ví dụ đơn giản áp dụng các thời gian chờ không thực hiện khác nhau tùy thuộc vào giá của nội dung.
Nó áp dụng thời gian chờ chặt chẽ cho các tài sản có giá cao hơn, đồng thời cho phép có nhiều thời gian hơn để lấp đầy các đồng tiền giá rẻ.

Hàm phải trả về `True` (hủy đơn hàng) hoặc `False` (giữ nguyên đơn hàng).``` python
    # Default imports

class AwesomeStrategy(IStrategy):

    # ... populate_* methods

    # Set unfilledtimeout to 25 hours, since the maximum timeout from below is 24 hours.
    unfilledtimeout = {
        "entry": 60 * 25,
        "exit": 60 * 25
    }

    def check_entry_timeout(self, pair: str, trade: Trade, order: Order,
                            current_time: datetime, **kwargs) -> bool:
        if trade.open_rate > 100 and trade.open_date_utc < current_time - timedelta(minutes=5):
            return True
        elif trade.open_rate > 10 and trade.open_date_utc < current_time - timedelta(minutes=3):
            return True
        elif trade.open_rate < 1 and trade.open_date_utc < current_time - timedelta(hours=24):
           return True
        return False


    def check_exit_timeout(self, pair: str, trade: Trade, order: Order,
                           current_time: datetime, **kwargs) -> bool:
        if trade.open_rate > 100 and trade.open_date_utc < current_time - timedelta(minutes=5):
            return True
        elif trade.open_rate > 10 and trade.open_date_utc < current_time - timedelta(minutes=3):
            return True
        elif trade.open_rate < 1 and trade.open_date_utc < current_time - timedelta(hours=24):
           return True
        return False
```!!! Lưu ý
    Đối với ví dụ trên, `unfilledtimeout` phải được đặt thành giá trị lớn hơn 24h, nếu không loại thời gian chờ đó sẽ được áp dụng trước tiên.

### Ví dụ về thời gian chờ của đơn hàng tùy chỉnh (sử dụng dữ liệu bổ sung)``` python
    # Default imports

class AwesomeStrategy(IStrategy):

    # ... populate_* methods

    # Set unfilledtimeout to 25 hours, since the maximum timeout from below is 24 hours.
    unfilledtimeout = {
        "entry": 60 * 25,
        "exit": 60 * 25
    }

    def check_entry_timeout(self, pair: str, trade: Trade, order: Order,
                            current_time: datetime, **kwargs) -> bool:
        ob = self.dp.orderbook(pair, 1)
        current_price = ob["bids"][0][0]
        # Cancel buy order if price is more than 2% above the order.
        if current_price > order.price * 1.02:
            return True
        return False


    def check_exit_timeout(self, pair: str, trade: Trade, order: Order,
                           current_time: datetime, **kwargs) -> bool:
        ob = self.dp.orderbook(pair, 1)
        current_price = ob["asks"][0][0]
        # Cancel sell order if price is more than 2% below the order.
        if current_price < order.price * 0.98:
            return True
        return False
```---

## Xác nhận đơn hàng bot

Xác nhận việc vào/ra giao dịch.
Đây là phương thức cuối cùng sẽ được gọi trước khi đặt hàng.

### Xác nhận nhập giao dịch (lệnh mua)

`confirm_trade_entry()` có thể được sử dụng để hủy bỏ mục nhập giao dịch vào giây gần nhất (có thể vì giá không như chúng ta mong đợi).``` python
# Default imports

class AwesomeStrategy(IStrategy):

    # ... populate_* methods

    def confirm_trade_entry(self, pair: str, order_type: str, amount: float, rate: float,
                            time_in_force: str, current_time: datetime, entry_tag: str | None,
                            side: str, **kwargs) -> bool:
        """
        Called right before placing a entry order.
        Timing for this function is critical, so avoid doing heavy computations or
        network requests in this method.

        For full documentation please go to https://www.freqtrade.io/en/stable/strategy-advanced/

        When not implemented by a strategy, returns True (always confirming).

        :param pair: Pair that's about to be bought/shorted.
        :param order_type: Order type (as configured in order_types). usually limit or market.
        :param amount: Amount in target (base) currency that's going to be traded.
        :param rate: Rate that's going to be used when using limit orders 
                     or current rate for market orders.
        :param time_in_force: Time in force. Defaults to GTC (Good-til-cancelled).
        :param current_time: datetime object, containing the current datetime
        :param entry_tag: Optional entry_tag (buy_tag) if provided with the buy signal.
        :param side: "long" or "short" - indicating the direction of the proposed trade
        :param **kwargs: Ensure to keep this here so updates to this won't break your strategy.
        :return bool: When True is returned, then the buy-order is placed on the exchange.
            False aborts the process
        """
        return True

```### Xác nhận thoát giao dịch (lệnh bán)

`confirm_trade_exit()` có thể được sử dụng để hủy bỏ việc thoát giao dịch (bán) vào giây gần nhất (có thể vì giá không như chúng ta mong đợi).

`confirm_trade_exit()` có thể được gọi nhiều lần trong một lần lặp cho cùng một giao dịch nếu áp dụng các lý do thoát khác nhau.
Các lý do rút lui (nếu có) sẽ theo trình tự sau:

* `exit_signal` / `custom_exit`* `stop_loss`
* `roi`
* `trailing_stop_loss`
``` python
# Default imports

class AwesomeStrategy(IStrategy):

    # ... populate_* methods

    def confirm_trade_exit(self, pair: str, trade: Trade, order_type: str, amount: float,
                           rate: float, time_in_force: str, exit_reason: str,
                           current_time: datetime, **kwargs) -> bool:
        """
        Called right before placing a regular exit order.
        Timing for this function is critical, so avoid doing heavy computations or
        network requests in this method.

        For full documentation please go to https://www.freqtrade.io/en/stable/strategy-advanced/

        When not implemented by a strategy, returns True (always confirming).

        :param pair: Pair for trade that's about to be exited.
        :param trade: trade object.
        :param order_type: Order type (as configured in order_types). usually limit or market.
        :param amount: Amount in base currency.
        :param rate: Rate that's going to be used when using limit orders
                     or current rate for market orders.
        :param time_in_force: Time in force. Defaults to GTC (Good-til-cancelled).
        :param exit_reason: Exit reason.
            Can be any of ["roi", "stop_loss", "stoploss_on_exchange", "trailing_stop_loss",
                           "exit_signal", "force_exit", "emergency_exit"]
        :param current_time: datetime object, containing the current datetime
        :param **kwargs: Ensure to keep this here so updates to this won't break your strategy.
        :return bool: When True, then the exit-order is placed on the exchange.
            False aborts the process
        """
        if exit_reason == "force_exit" and trade.calc_profit_ratio(rate) < 0:
            # Reject force-sells with negative profit
            # This is just a sample, please adjust to your needs
            # (this does not necessarily make sense, assuming you know when you're force-selling)
            return False
        return True

```!!! Cảnh báo
    `confirm_trade_exit()` có thể ngăn chặn việc thoát lệnh dừng lỗ, gây ra tổn thất đáng kể vì điều này sẽ bỏ qua lệnh thoát lệnh dừng lỗ.
    `confirm_trade_exit()` sẽ không được gọi cho Thanh lý - vì việc thanh lý là do sàn giao dịch ép buộc và do đó không thể bị từ chối.

## Điều chỉnh vị thế giao dịch

Thuộc tính chiến lược `position_ adjustment_enable` cho phép sử dụng lệnh gọi lại `just_trade_position()` trong chiến lược.
Vì lý do hiệu suất, nó bị tắt theo mặc định và freqtrade sẽ hiển thị thông báo cảnh báo khi khởi động nếu được bật.
`điều chỉnh_trade_position()` có thể được sử dụng để thực hiện các lệnh bổ sung, ví dụ: để quản lý rủi ro với DCA (Trung bình chi phí bằng đô la) hoặc để tăng hoặc giảm vị thế.

Các đơn đặt hàng bổ sung cũng dẫn đến phí bổ sung và những đơn đặt hàng đó không được tính vào `max_open_trades`.

Cuộc gọi lại này cũng được gọi khi có một lệnh mở (mua hoặc bán) đang chờ thực hiện - và sẽ hủy lệnh mở hiện tại để đặt một lệnh mới nếu số lượng, giá hoặc hướng khác nhau. Ngoài ra, các đơn đặt hàng đã được thực hiện một phần sẽ bị hủy và sẽ được thay thế bằng số tiền mới được trả về khi gọi lại.

`điều chỉnh_trade_position()` được gọi rất thường xuyên trong suốt thời gian giao dịch, vì vậy bạn phải duy trì việc triển khai của mình hiệu quả nhất có thể.

Điều chỉnh vị thế sẽ luôn được áp dụng theo hướng giao dịch, do đó giá trị dương sẽ luôn tăng vị thế của bạn (giá trị âm sẽ làm giảm vị thế của bạn), bất kể đó là giao dịch mua hay bán.
Các lệnh điều chỉnh có thể được chỉ định bằng một thẻ bằng cách trả về Tuple 2 phần tử, với phần tử đầu tiên là số tiền điều chỉnh và phần tử thứ 2 là thẻ (ví dụ: `return 250, "increase_favorable_conditions"`).

Không thể sửa đổi đòn bẩy và số tiền đặt cược được trả lại được coi là trước khi áp dụng đòn bẩy.

Tổng số cổ phần hiện được phân bổ cho vị thế này được giữ dưới dạng `trade.stake_amount`. Do đó, `trade.stake_amount` sẽ luôn được cập nhật trên mỗi lần nhập bổ sung và thoát một phần được thực hiện thông qua `just_trade_position()`.

!!! Nguy hiểm “Lỏng lẻo logic”
    Khi chạy khô và chạy trực tiếp, hàm này sẽ được gọi mỗi `throttle_process_secs` (mặc định là 5 giây). Nếu bạn có logic lỏng lẻo, (ví dụ: tăng vị trí nếu RSI của nến cuối cùng dưới 30), bot của bạn sẽ thực hiện nhập lại thêm sau mỗi 5 giây cho đến khi bạn hết tiền, đạt giới hạn `max_position_ adjustment` hoặc xuất hiện một cây nến mới có RSI lớn hơn 30.

    Điều tương tự cũng có thể xảy ra với việc thoát một phần.  
    Vì vậy, hãy đảm bảo có logic chặt chẽ và/hoặc kiểm tra lệnh đã khớp gần đây nhất và xem lệnh đó đã được mở chưa.

!!! Cảnh báo "Hiệu suất với nhiều điều chỉnh vị trí"
    Điều chỉnh vị trí có thể là một cách tiếp cận tốt để tăng sản lượng của chiến lược - nhưng nó cũng có thể có những hạn chế nếu sử dụng rộng rãi tính năng này.  
    Mỗi lệnh sẽ được gắn vào đối tượng giao dịch trong suốt thời gian giao dịch - do đó làm tăng mức sử dụng bộ nhớ.
    Do đó, các giao dịch có thời gian dài và điều chỉnh vị thế 10 giây hoặc thậm chí 100 giây không được khuyến khích và nên đóng định kỳ để không ảnh hưởng đến hiệu suất.

!!! Cảnh báo "Đang kiểm tra lại"
    Trong quá trình kiểm tra ngược, lệnh gọi lại này được gọi cho mỗi nến trong `timeframe` hoặc `timeframe_detail`, do đó hiệu suất trong thời gian chạy sẽ bị ảnh hưởng.
    Điều này cũng có thể gây ra kết quả sai lệch giữa việc kiểm tra trực tiếp và kiểm tra lại, vì việc kiểm tra ngược chỉ có thể điều chỉnh giao dịch một lần cho mỗi nến, trong khi việc kiểm tra trực tiếp có thể điều chỉnh giao dịch nhiều lần cho mỗi nến.### Tăng vị trí

Chiến lược này dự kiến sẽ trả về một **stake_amount** dương (bằng tiền đặt cược) giữa `min_stake` và `max_stake` nếu và khi một lệnh nhập bổ sung được thực hiện (vị trí tăng -> lệnh mua cho các giao dịch dài, lệnh bán cho các giao dịch ngắn).

Nếu không có đủ tiền trong ví (giá trị trả về cao hơn `max_stake`) thì tín hiệu sẽ bị bỏ qua.
Thuộc tính `max_entry_position_ adjustment` được sử dụng để giới hạn số lượng mục nhập bổ sung cho mỗi giao dịch (ngoài lệnh nhập đầu tiên) mà bot có thể thực hiện. Theo mặc định, giá trị là -1 nghĩa là bot không có giới hạn về số lượng mục điều chỉnh.

Các mục nhập bổ sung sẽ bị bỏ qua khi bạn đã đạt đến số lượng mục nhập bổ sung tối đa mà bạn đã đặt trên `max_entry_position_ adjustment`, nhưng lệnh gọi lại vẫn được gọi để tìm cách thoát một phần.

!!! Lưu ý "Về quy mô cổ phần"
    Sử dụng kích thước cổ phần cố định có nghĩa là số tiền đó sẽ được sử dụng cho lệnh đầu tiên, giống như không điều chỉnh vị trí.
    Nếu bạn muốn mua các đơn đặt hàng bổ sung với DCA, hãy đảm bảo để lại đủ tiền trong ví cho việc đó.
    Việc sử dụng số tiền đặt cược `"không giới hạn"` với các lệnh DCA yêu cầu bạn cũng phải triển khai lệnh gọi lại `custom_stake_amount()` để tránh phân bổ tất cả tiền cho lệnh ban đầu.

### Giảm vị trí

Chiến lược này dự kiến sẽ trả về số tiền âm (bằng đơn vị tiền tệ đặt cược) khi thoát một phần.
Trả lại toàn bộ cổ phần sở hữu tại thời điểm đó (`-trade.stake_amount`) dẫn đến việc thoát hoàn toàn.  
Trả về một giá trị lớn hơn giá trị trên (vì vậy số tiền stake_amount còn lại sẽ trở thành số âm) sẽ khiến bot bỏ qua tín hiệu.

Đối với thoát một phần, điều quan trọng cần biết là công thức được sử dụng để tính số tiền cho lệnh thoát một phần là `số tiền thoát một phần = Negative_stake_amount * Trade.amount / Trade.stake_amount`, trong đó ` Negative_stake_amount` là giá trị được trả về từ hàm `just_trade_position`. Như đã thấy trong công thức, công thức không quan tâm đến lãi/lỗ hiện tại của vị thế. Nó chỉ quan tâm đến `trade.amount` và `trade.stake_amount` mà không bị ảnh hưởng bởi biến động giá cả.

Ví dụ: giả sử bạn mua 2 SHITCOIN/USDT với tỷ lệ mở là 50, nghĩa là số tiền đặt cược của giao dịch là 100 USDT. Bây giờ giá tăng lên 200 và bạn muốn bán một nửa số đó. Trong trường hợp đó, bạn phải trả lại -50% của `trade.stake_amount` (0,5 * 100 USDT) tương đương với -50. Bot sẽ tính toán số tiền cần bán là `50 * 2 / 100` tương đương 1 SHITCOIN/USDT. Nếu bạn trả về -200 (50% của 2 * 200), bot sẽ bỏ qua nó vì `trade.stake_amount` chỉ có 100 USDT nhưng bạn yêu cầu bán 200 USDT, nghĩa là bạn đang yêu cầu bán 4 SHITCOIN/USDT.Quay lại ví dụ trên, vì tỷ giá hiện tại là 200 nên giá trị USDT hiện tại trong giao dịch của bạn hiện là 400 USDT. Giả sử bạn muốn bán một phần 100 USDT để lấy khoản đầu tư ban đầu và để lại lợi nhuận trong giao dịch với hy vọng giá tiếp tục tăng. Trong trường hợp đó, bạn phải thực hiện một cách tiếp cận khác. Đầu tiên, bạn cần tính toán chính xác số lượng cần bán. Trong trường hợp này, vì bạn muốn bán trị giá 100 USDT dựa trên tỷ giá hiện tại, số tiền chính xác bạn cần bán một phần là `100 * 2 / 400` tương đương 0,5 SHITCOIN/USDT. Vì hiện tại chúng tôi biết chính xác số tiền mình muốn bán (0,5), giá trị bạn cần trả về trong hàm `just_trade_position` là `-amount để thoát một phần * Trade.stake_amount / Trade.amount`, bằng -25. Bot sẽ bán 0,5 SHITCOIN/USDT, giữ 1,5 giao dịch. Bạn sẽ nhận được 100 USDT khi thoát một phần.

!!! Cảnh báo "Tính toán điểm dừng"
    Điểm dừng lỗ vẫn được tính từ giá mở cửa ban đầu chứ không phải giá trung bình.
    Quy tắc dừng lỗ thông thường vẫn được áp dụng (không thể di chuyển xuống).

    Trong khi lệnh `/stopentry` ngăn bot tham gia các giao dịch mới, tính năng điều chỉnh vị trí sẽ tiếp tục mua các lệnh mới trên các giao dịch hiện có.``` python
# Default imports

class DigDeeperStrategy(IStrategy):

    position_adjustment_enable = True

    # Attempts to handle large drops with DCA. High stoploss is required.
    stoploss = -0.30

    # ... populate_* methods

    # Example specific variables
    max_entry_position_adjustment = 3
    # This number is explained a bit further down
    max_dca_multiplier = 5.5

    # This is called when placing the initial order (opening trade)
    def custom_stake_amount(self, pair: str, current_time: datetime, current_rate: float,
                            proposed_stake: float, min_stake: float | None, max_stake: float,
                            leverage: float, entry_tag: str | None, side: str,
                            **kwargs) -> float:

        # We need to leave most of the funds for possible further DCA orders
        # This also applies to fixed stakes
        return proposed_stake / self.max_dca_multiplier

    def adjust_trade_position(self, trade: Trade, current_time: datetime,
                              current_rate: float, current_profit: float,
                              min_stake: float | None, max_stake: float,
                              current_entry_rate: float, current_exit_rate: float,
                              current_entry_profit: float, current_exit_profit: float,
                              **kwargs
                              ) -> float | None | tuple[float | None, str | None]:
        """
        Custom trade adjustment logic, returning the stake amount that a trade should be
        increased or decreased.
        This means extra entry or exit orders with additional fees.
        Only called when `position_adjustment_enable` is set to True.

        For full documentation please go to https://www.freqtrade.io/en/stable/strategy-advanced/

        When not implemented by a strategy, returns None

        :param trade: trade object.
        :param current_time: datetime object, containing the current datetime
        :param current_rate: Current entry rate (same as current_entry_profit)
        :param current_profit: Current profit (as ratio), calculated based on current_rate 
                               (same as current_entry_profit).
        :param min_stake: Minimal stake size allowed by exchange (for both entries and exits)
        :param max_stake: Maximum stake allowed (either through balance, or by exchange limits).
        :param current_entry_rate: Current rate using entry pricing.
        :param current_exit_rate: Current rate using exit pricing.
        :param current_entry_profit: Current profit using entry pricing.
        :param current_exit_profit: Current profit using exit pricing.
        :param **kwargs: Ensure to keep this here so updates to this won't break your strategy.
        :return float: Stake amount to adjust your trade,
                       Positive values to increase position, Negative values to decrease position.
                       Return None for no action.
                       Optionally, return a tuple with a 2nd element with an order reason
        """
        if trade.has_open_orders:
            # Only act if no orders are open
            return

        if current_profit > 0.05 and trade.nr_of_successful_exits == 0:
            # Take half of the profit at +5%
            return -(trade.stake_amount / 2), "half_profit_5%"

        if current_profit > -0.05:
            return None

        # Obtain pair dataframe (just to show how to access it)
        dataframe, _ = self.dp.get_analyzed_dataframe(trade.pair, self.timeframe)
        # Only buy when not actively falling price.
        last_candle = dataframe.iloc[-1].squeeze()
        previous_candle = dataframe.iloc[-2].squeeze()
        if last_candle["close"] < previous_candle["close"]:
            return None

        filled_entries = trade.select_filled_orders(trade.entry_side)
        count_of_entries = trade.nr_of_successful_entries
        # Allow up to 3 additional increasingly larger buys (4 in total)
        # Initial buy is 1x
        # If that falls to -5% profit, we buy 1.25x more, average profit should increase to roughly -2.2%
        # If that falls down to -5% again, we buy 1.5x more
        # If that falls once again down to -5%, we buy 1.75x more
        # Total stake for this trade would be 1 + 1.25 + 1.5 + 1.75 = 5.5x of the initial allowed stake.
        # That is why max_dca_multiplier is 5.5
        # Hope you have a deep wallet!
        try:
            # This returns first order stake size
            stake_amount = filled_entries[0].stake_amount_filled
            # This then calculates current safety order size
            stake_amount = stake_amount * (1 + (count_of_entries * 0.25))
            return stake_amount, "1/3rd_increase"
        except Exception as exception:
            return None

        return None

```### Tính toán điều chỉnh vị trí

* Tỷ lệ đầu vào được tính bằng cách sử dụng mức trung bình có trọng số.
* Thoát sẽ không ảnh hưởng đến tỷ lệ nhập cảnh trung bình.
* Lợi nhuận tương đối khi thoát một phần tương ứng với giá vào lệnh trung bình tại thời điểm này.
* Lợi nhuận tương đối khi thoát cuối cùng được tính dựa trên tổng vốn đầu tư. (Xem ví dụ bên dưới)

??? ví dụ "Ví dụ tính toán"
    *Ví dụ này giả định phí 0 để đơn giản và vị thế mua trên một đồng tiền ảo.*  
    
    * Mua 100@8\$ 
    * Mua 100@9\$ -> Giá trung bình: 8,5\$
    * Bán 100@10\$ -> Giá trung bình: 8,5\$, lợi nhuận thực hiện 150\$, 17,65%
    * Mua 150@11\$ -> Giá trung bình: 10\$, lợi nhuận thực hiện 150\$, 17,65%
    * Bán 100@12\$ -> Giá trung bình: 10\$, tổng lợi nhuận thực hiện 350\$, 20%
    * Bán 150@14\$ -> Giá trung bình: 10\$, tổng lợi nhuận thực hiện 950\$, 40% <- *Đây sẽ là thông báo "Thoát" cuối cùng*

    Tổng lợi nhuận cho giao dịch này là 950$ trên khoản đầu tư 3350$ (`100@8$ + 100@9$ + 150@11$`). Như vậy - lợi nhuận tương đối cuối cùng là 28,35% (`950 / 3350`).

## Điều chỉnh giá lệnh

Nhà phát triển chiến lược có thể sử dụng lệnh gọi lại `just_order_price()` để làm mới/thay thế các lệnh giới hạn khi có nến mới.  
Cuộc gọi lại này được gọi một lần mỗi lần lặp trừ khi đơn hàng đã được đặt (lại) trong nến hiện tại - giới hạn vị trí (lại) tối đa của mỗi đơn hàng ở mức một lần cho mỗi nến.
Điều này cũng có nghĩa là lệnh gọi đầu tiên sẽ ở đầu nến tiếp theo sau khi lệnh ban đầu được đặt.

Xin lưu ý rằng `custom_entry_price()`/`custom_exit_price()` vẫn là yếu tố quyết định mục tiêu giá của lệnh giới hạn ban đầu tại thời điểm phát ra tín hiệu.

Bạn có thể hủy đơn đặt hàng khỏi cuộc gọi lại này bằng cách trả về `Không`.

Việc trả về `current_order_rate` sẽ giữ nguyên đơn hàng trên sàn giao dịch.
Việc trả lại bất kỳ mức giá nào khác sẽ hủy đơn hàng hiện tại và thay thế nó bằng một đơn hàng mới.

Nếu việc hủy đơn hàng ban đầu không thành công thì đơn hàng đó sẽ không được thay thế - mặc dù rất có thể đơn hàng đó đã bị hủy khi trao đổi. Điều này xảy ra trong các mục nhập ban đầu sẽ dẫn đến việc xóa đơn hàng, trong khi đối với các lệnh điều chỉnh vị trí, nó sẽ dẫn đến quy mô giao dịch được giữ nguyên.  
Nếu lệnh đã được thực hiện một phần, lệnh sẽ không được thay thế. Tuy nhiên, bạn có thể sử dụng [`just_trade_position()`](#just-trade-position) để điều chỉnh quy mô giao dịch theo quy mô vị thế dự kiến, nếu điều này là cần thiết/mong muốn.

!!! Cảnh báo "Thời gian chờ thường xuyên"
    Cơ chế nhập `unfilledtimeout` (cũng như `check_entry_timeout()`/`check_exit_timeout()`) được ưu tiên hơn lệnh gọi lại này.
    Các đơn hàng bị hủy thông qua các phương pháp trên sẽ không được gọi lại. Hãy nhớ cập nhật giá trị thời gian chờ để phù hợp với mong đợi của bạn.```python
# Default imports

class AwesomeStrategy(IStrategy):

    # ... populate_* methods

    def adjust_order_price(
        self,
        trade: Trade,
        order: Order | None,
        pair: str,
        current_time: datetime,
        proposed_rate: float,
        current_order_rate: float,
        entry_tag: str | None,
        side: str,
        is_entry: bool,
        **kwargs,
    ) -> float | None:
        """
        Exit and entry order price re-adjustment logic, returning the user desired limit price.
        This only executes when a order was already placed, still open (unfilled fully or partially)
        and not timed out on subsequent candles after entry trigger.

        For full documentation please go to https://www.freqtrade.io/en/stable/strategy-callbacks/

        When not implemented by a strategy, returns current_order_rate as default.
        If current_order_rate is returned then the existing order is maintained.
        If None is returned then order gets canceled but not replaced by a new one.

        :param pair: Pair that's currently analyzed
        :param trade: Trade object.
        :param order: Order object
        :param current_time: datetime object, containing the current datetime
        :param proposed_rate: Rate, calculated based on pricing settings in entry_pricing.
        :param current_order_rate: Rate of the existing order in place.
        :param entry_tag: Optional entry_tag (buy_tag) if provided with the buy signal.
        :param side: 'long' or 'short' - indicating the direction of the proposed trade
        :param is_entry: True if the order is an entry order, False if it's an exit order.
        :param **kwargs: Ensure to keep this here so updates to this won't break your strategy.
        :return float or None: New entry price value if provided
        """

        # Limit entry orders to use and follow SMA200 as price target for the first 10 minutes since entry trigger for BTC/USDT pair.
        if (
            is_entry
            and pair == "BTC/USDT" 
            and entry_tag == "long_sma200" 
            and side == "long" 
            and (current_time - timedelta(minutes=10)) <= trade.open_date_utc
        ):
            # just cancel the order if it has been filled more than half of the amount
            if order.filled > order.remaining:
                return None
            else:
                dataframe, _ = self.dp.get_analyzed_dataframe(pair=pair, timeframe=self.timeframe)
                current_candle = dataframe.iloc[-1].squeeze()
                # desired price
                return current_candle["sma_200"]
        # default: maintain existing order
        return current_order_rate
```!!! nguy hiểm "Không tương thích với `just_*_price()`"
    Nếu bạn đã triển khai cả `điều chỉnh_order_price()` và `điều chỉnh_entry_price()`/`điều chỉnh_exit_price()` thì chỉ `điều chỉnh_order_price()` mới được sử dụng.
    Nếu cần điều chỉnh giá vào/ra, bạn có thể triển khai logic trong `just_order_price()` hoặc sử dụng lệnh gọi lại `just_entry_price()` / ` adjustment_exit_price()` phân tách, chứ không phải cả hai.
    Việc trộn những thứ này không được hỗ trợ và sẽ gây ra lỗi trong quá trình khởi động bot.

### Điều chỉnh giá vào

Nhà phát triển chiến lược có thể sử dụng lệnh gọi lại `just_entry_price()` để làm mới/thay thế các lệnh giới hạn mục nhập khi đến nơi.
Đó là tập hợp con của ` adjustment_order_price()` và chỉ được gọi cho các lệnh nhập.
Tất cả hành vi còn lại giống hệt với `just_order_price()`.

Ngày mở giao dịch (`trade.open_date_utc`) sẽ vẫn được giữ nguyên tại thời điểm đặt lệnh đầu tiên.
Vui lòng đảm bảo lưu ý điều này - và cuối cùng điều chỉnh logic của bạn trong các lệnh gọi lại khác để giải quyết vấn đề này và thay vào đó hãy sử dụng ngày của đơn hàng được thực hiện đầu tiên.

### Điều chỉnh giá thoát

Nhà phát triển chiến lược có thể sử dụng lệnh gọi lại `just_exit_price()` để làm mới/thay thế các lệnh giới hạn thoát khi đến nơi.
Đó là tập hợp con của ` adjustment_order_price()` và chỉ được gọi cho các lệnh thoát.
Tất cả hành vi còn lại giống hệt với `just_order_price()`.

## Tận dụng cuộc gọi lại

Khi giao dịch ở các thị trường cho phép đòn bẩy, phương thức này phải trả về Đòn bẩy mong muốn (Mặc định là 1 -> Không có đòn bẩy).

Giả sử số vốn là 500USDT, giao dịch có đòn bẩy=3 sẽ dẫn đến vị thế có 500 x 3 = 1500 USDT.

Các giá trị cao hơn `max_leverage` sẽ được điều chỉnh thành `max_leverage`.
Đối với các thị trường/sàn giao dịch không hỗ trợ đòn bẩy, phương pháp này sẽ bị bỏ qua.``` python
# Default imports

class AwesomeStrategy(IStrategy):
    def leverage(self, pair: str, current_time: datetime, current_rate: float,
                 proposed_leverage: float, max_leverage: float, entry_tag: str | None, side: str,
                 **kwargs) -> float:
        """
        Customize leverage for each new trade. This method is only called in futures mode.

        :param pair: Pair that's currently analyzed
        :param current_time: datetime object, containing the current datetime
        :param current_rate: Rate, calculated based on pricing settings in exit_pricing.
        :param proposed_leverage: A leverage proposed by the bot.
        :param max_leverage: Max leverage allowed on this pair
        :param entry_tag: Optional entry_tag (buy_tag) if provided with the buy signal.
        :param side: "long" or "short" - indicating the direction of the proposed trade
        :return: A leverage amount, which is between 1.0 and max_leverage.
        """
        return 1.0
```Tất cả các tính toán lợi nhuận đều bao gồm đòn bẩy. Stoploss/ROI cũng bao gồm đòn bẩy trong tính toán của họ.
Việc xác định mức dừng lỗ là 10% với đòn bẩy 10 lần sẽ kích hoạt mức dừng lỗ khi giá di chuyển xuống mức giảm 1%.

## Đã điền đơn hàng Gọi lại

Lệnh gọi lại `order_filled()` có thể được sử dụng để thực hiện các hành động cụ thể dựa trên trạng thái giao dịch hiện tại sau khi đơn hàng được thực hiện.
Nó sẽ được gọi là độc lập với loại lệnh (vào, ra, dừng lỗ hoặc điều chỉnh vị thế).

Giả sử rằng chiến lược của bạn cần lưu trữ giá trị cao của nến khi bắt đầu giao dịch, điều này có thể thực hiện được với lệnh gọi lại này như minh họa trong ví dụ sau.``` python
# Default imports

class AwesomeStrategy(IStrategy):
    def order_filled(self, pair: str, trade: Trade, order: Order, current_time: datetime, **kwargs) -> None:
        """
        Called right after an order fills. 
        Will be called for all order types (entry, exit, stoploss, position adjustment).
        :param pair: Pair for trade
        :param trade: trade object.
        :param order: Order object.
        :param current_time: datetime object, containing the current datetime
        :param **kwargs: Ensure to keep this here so updates to this won't break your strategy.
        """
        # Obtain pair dataframe (just to show how to access it)
        dataframe, _ = self.dp.get_analyzed_dataframe(trade.pair, self.timeframe)
        last_candle = dataframe.iloc[-1].squeeze()
        
        if (trade.nr_of_successful_entries == 1) and (order.ft_order_side == trade.entry_side):
            trade.set_custom_data(key="entry_candle_high", value=last_candle["high"])

        return None

```!!! Mẹo "Tìm hiểu thêm về cách lưu trữ dữ liệu"
    Bạn có thể tìm hiểu thêm về cách lưu trữ dữ liệu trên phần [Lưu trữ dữ liệu giao dịch tùy chỉnh](strategy-advanced.md#storing-information-persistent).
    Xin lưu ý rằng đây được coi là cách sử dụng nâng cao và cần được sử dụng cẩn thận.

## Vẽ biểu đồ chú thích gọi lại

Lệnh gọi lại chú thích biểu đồ được gọi bất cứ khi nào freqUI yêu cầu dữ liệu để hiển thị biểu đồ.
Lệnh gọi lại này không có ý nghĩa gì trong bối cảnh chu kỳ giao dịch và chỉ được sử dụng cho mục đích lập biểu đồ.

Sau đó, chiến lược có thể trả về danh sách các đối tượng `AnnotationType` sẽ được hiển thị trên biểu đồ.
Tùy theo nội dung trả về - biểu đồ có thể hiển thị vùng ngang, vùng dọc, ô hoặc đường.

### Các loại chú thích

Hiện tại, hai loại chú thích được hỗ trợ là `area` và `line`.

#### Khu vực``` json
{
    "type": "area", // Type of the annotation, currently only "area" is supported
    "start": "2024-01-01 15:00:00", // Start date of the area
    "end": "2024-01-01 16:00:00",  // End date of the area
    "y_start": 94000.2,  // Price / y axis value
    "y_end": 98000, // Price / y axis value
    "color": "",
    "z_level": 5, // z-level, higher values are drawn on top of lower values. Positions relative to the Chart elements need to be set in freqUI.
    "label": "some label"
}
```#### Đường kẻ``` json
{
    "type": "line", // Type of the annotation, currently only "line" is supported
    "start": "2024-01-01 15:00:00", // Start date of the line
    "end": "2024-01-01 16:00:00",  // End date of the line
    "y_start": 94000.2,  // Price / y axis value
    "y_end": 98000, // Price / y axis value
    "color": "",
    "z_level": 5, // z-level, higher values are drawn on top of lower values. Positions relative to the Chart elements need to be set in freqUI.
    "label": "some label",
    "width": 2, // Optional, line width in pixels. Defaults to 1
    "line_style": "dashed", // Optional, can be "solid", "dashed" or "dotted". Defaults to "solid"

}
```#### Điểm``` json
{
    "type": "point", // Type of the annotation, currently only "point" is supported
    "x": "2024-01-01 15:00:00", // Start date of the point
    "y": 94000.2,  // Price / y axis value
    "color": "",
    "z_level": 5, // z-level, higher values are drawn on top of lower values. Positions relative to the Chart elements need to be set in freqUI.
    "label": "some label",
    "size": 2, // Optional, line width in pixels. Defaults to 10
    "shape": "circle", // Optional, can be "circle", "rect", "roundRect", "triangle", "pin", "arrow", "none".
    "rotate": 0, // Optional, rotation of the shape/symbol in degrees. Defaults to 0

}
```Ví dụ dưới đây sẽ đánh dấu biểu đồ bằng các khu vực cho giờ 8 và 15, bằng màu xám, làm nổi bật giờ mở cửa và đóng cửa của thị trường.
Đây rõ ràng là một ví dụ rất cơ bản.``` python
# Default imports

class AwesomeStrategy(IStrategy):
    def plot_annotations(
        self, pair: str, start_date: datetime, end_date: datetime, dataframe: DataFrame, **kwargs
    ) -> list[AnnotationType]:
        """
        Retrieve area annotations for a chart.
        Must be returned as array, with type, label, color, start, end, y_start, y_end.
        All settings except for type are optional - though it usually makes sense to include either
        "start and end" or "y_start and y_end" for either horizontal or vertical plots
        (or all 4 for boxes).
        :param pair: Pair that's currently analyzed
        :param start_date: Start date of the chart data being requested
        :param end_date: End date of the chart data being requested
        :param dataframe: DataFrame with the analyzed data for the chart
        :param **kwargs: Ensure to keep this here so updates to this won't break your strategy.
        :return: List of AnnotationType objects
        """
        annotations = []
        while start_dt < end_date:
            start_dt += timedelta(hours=1)
            if start_dt.hour in (8, 15):
                annotations.append(
                    {
                        "type": "area",
                        "label": "Trade open and close hours",
                        "start": start_dt,
                        "end": start_dt + timedelta(hours=1),
                        # Omitting y_start and y_end will result in a vertical area spanning the whole height of the main Chart
                        "color": "rgba(133, 133, 133, 0.4)",
                    }
                )

        return annotations

```Các mục nhập sẽ được xác thực và sẽ không được chuyển đến giao diện người dùng nếu chúng không tương ứng với lược đồ dự kiến ​​và sẽ ghi lại lỗi nếu không.

!!! Cảnh báo "Nhiều chú thích"
    Sử dụng quá nhiều chú thích có thể khiến giao diện người dùng bị treo, đặc biệt khi vẽ biểu đồ lượng lớn dữ liệu lịch sử.
    Sử dụng tính năng chú thích một cách cẩn thận.

### Ví dụ về chú thích biểu đồ

![FreqUI - Chú thích cốt truyện](assets/freqUI-chart-annotations-dark.png#only-dark)
![FreqUI - Chú thích cốt truyện](assets/freqUI-chart-annotations-light.png#only-light)

??? Thông tin "Mã được sử dụng cho âm mưu trên"
    Đây là một mã ví dụ và nên được xử lý như vậy.``` python
    # Default imports

    class AwesomeStrategy(IStrategy):
        def plot_annotations(
            self, pair: str, start_date: datetime, end_date: datetime, dataframe: DataFrame, **kwargs
        ) -> list[AnnotationType]:
            annotations = []
            while start_dt < end_date:
                start_dt += timedelta(hours=1)
                if (start_dt.hour % 4) == 0:
                    annotations.append(
                        {
                            "type": "area",
                            "label": "4h",
                            "start": start_dt,
                            "end": start_dt + timedelta(hours=1),
                            "color": "rgba(133, 133, 133, 0.4)",
                        }
                    )
                elif (start_dt.hour % 2) == 0:
                price = dataframe.loc[dataframe["date"] == start_dt, "close"].mean()
                    annotations.append(
                        {
                            "type": "area",
                            "label": "2h",
                            "start": start_dt,
                            "end": start_dt + timedelta(hours=1),
                            "y_end": price * 1.01,
                            "y_start": price * 0.99,
                            "color": "rgba(0, 255, 0, 0.4)",
                            "z_level": 5,
                        }
                    )

            return annotations

    ```