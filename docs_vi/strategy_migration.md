<!-- Auto-translated from docs/ by script. Please review technical terms. -->

# Di chuyển chiến lược giữa V2 và V3

Để hỗ trợ các thị trường và loại hình giao dịch mới (cụ thể là giao dịch bán khống/giao dịch có đòn bẩy), một số thứ đã phải thay đổi trong giao diện.
Nếu bạn có ý định sử dụng các thị trường khác ngoài thị trường giao ngay, vui lòng chuyển chiến lược của bạn sang định dạng mới.

Chúng tôi đã nỗ lực rất nhiều để duy trì khả năng tương thích với các chiến lược hiện có, vì vậy nếu bạn chỉ muốn tiếp tục sử dụng freqtrade tại __spotthị trường__ thì hiện tại không cần phải thay đổi gì cả.

Bạn có thể sử dụng bản tóm tắt nhanh làm danh sách kiểm tra. Vui lòng tham khảo các phần chi tiết bên dưới để biết chi tiết di chuyển đầy đủ.

## Danh sách kiểm tra tóm tắt / di chuyển nhanh

Lưu ý: `forcesell`, `forcebuy`, `emergencysell` lần lượt được đổi thành `force_exit`, `force_enter`, `emergency_exit`.

* Phương pháp chiến lược:
  * [`populate_buy_trend()` -> `populate_entry_trend()`](#populate_buy_trend)
  * [`populate_sell_trend()` -> `populate_exit_trend()`](#populate_sell_trend)
  * [`custom_sell()` -> `custom_exit()`](#custom_sell)
  * [`check_buy_timeout()` -> `check_entry_timeout()`](#custom_entry_timeout)
  * [`check_sell_timeout()` -> `check_exit_timeout()`](#custom_entry_timeout)
  * Đối số `side` mới cho lệnh gọi lại không có đối tượng giao dịch
    * [`custom_stake_amount`](#custom_stake_amount)
    * [`confirm_trade_entry`](#confirm_trade_entry)
    * [`custom_entry_price`](#custom_entry_price)
  * [Đã thay đổi tên đối số trong `confirm_trade_exit`](#confirm_trade_exit)
* Cột khung dữ liệu:
  * [`buy` -> `enter_long`](#populate_buy_trend)
  * [`bán` -> `exit_long`](#populate_sell_trend)
  * [`buy_tag` -> `enter_tag` (được sử dụng cho cả giao dịch mua và bán)](#populate_buy_trend)
  * [Cột mới `enter_short` và cột mới tương ứng `exit_short`](#populate_sell_trend)
* đối tượng thương mại hiện có các thuộc tính mới sau:  * `is_short`
  * `entry_side`
  * `exit_side`
  * `trade_direction`
* được đổi tên thành: `sell_reason` -> `exit_reason`
* [Đã đổi tên `trade.nr_of_successful_buys` thành `trade.nr_of_successful_entries` (chủ yếu liên quan đến `just_trade_position()`)](# adjustment-trade-position-changes)
* Giới thiệu [gọi lại đòn bẩy` mới](strategy-callbacks.md#leverage-callback).
* Các cặp thông tin hiện có thể chuyển phần tử thứ 3 trong Tuple, xác định loại nến.
* Trình trang trí `@informative` hiện có một đối số `candle_type` tùy chọn.
* [các phương thức trợ giúp](#helper-methods) `stoploss_from_open` và `stoploss_from_absolute` hiện lấy `is_short` làm đối số bổ sung.
* `INTERFACE_VERSION` phải được đặt thành 3.
* [Cài đặt chiến lược/cấu hình](#strategyconfiguration-settings).
  * `order_time_in_force` mua -> vào, bán -> thoát.
  * `order_types` mua -> vào, bán -> thoát.
  * `unfilledtimeout` mua -> vào, bán -> thoát.
  * `ignore_buying_expired_candle_after` -> được chuyển đến cấp độ gốc thay vì "ask_strategy/exit_pricing"
* Thay đổi thuật ngữ
  * Lý do bán đã thay đổi để phản ánh cách đặt tên mới cho "thoát" thay vì bán. Hãy cẩn thận trong chiến lược của bạn nếu bạn đang sử dụng kiểm tra `exit_reason` và cuối cùng là cập nhật chiến lược của mình.
    * `sell_signal` -> `exit_signal`
    * `custom_sell` -> `custom_exit`
    * `buộc_sell` -> `buộc_exit`
    * `bán_khẩn cấp` -> `thoát_khẩn cấp`
  * Đặt hàng giá
    * `chiến lược giá thầu` -> `giá_đầu vào`
    * `ask_strategy` -> `exit_pricing`
    * `ask_last_balance` -> `price_last_balance`
    * `bid_last_balance` -> `price_last_balance`
  * Thuật ngữ Webhook đã thay đổi từ "bán" thành "thoát" và từ "mua" thành nhập
    * `webhookbuy` -> `entry`
    * `webhookbuyfill` -> `entry_fill`
    * `webhookbuycancel` -> `entry_cancel`
    * `webhooksell` -> `thoát`
    * `webhooksellfill` -> `exit_fill`
    * `webhooksellcancel` -> `exit_cancel`
  * Cài đặt thông báo Telegram
    * `mua` -> `nhập`
    * `buy_fill` -> `entry_fill`
    * `buy_cancel` -> `entry_cancel`
    * `bán` -> `thoát`
    * `sell_fill` -> `exit_fill`
    * `bán_hủy` -> `thoát_hủy`
  * Cài đặt chiến lược/cấu hình:
    * `use_sell_signal` -> `use_exit_signal`
    * `chỉ bán_lợi nhuận` -> `chỉ thoát_lợi nhuận`
    * `bán_lợi nhuận_bù đắp` -> `exit_profit_offset`
    * `ignore_roi_if_buy_signal` -> `ignore_roi_if_entry_signal`
    * `forcebuy_enable` -> `force_entry_enable`

## Giải thích mở rộng### `populate_buy_trend`
Trong `populate_buy_trend()` - bạn sẽ muốn thay đổi các cột bạn chỉ định từ `'buy`' thành `'enter_long'`, cũng như tên phương thức từ `populate_buy_trend` thành `populate_entry_trend`.```python hl_lines="1 9"
def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
    dataframe.loc[
        (
            (qtpylib.crossed_above(dataframe['rsi'], 30)) &  # Signal: RSI crosses above 30
            (dataframe['tema'] <= dataframe['bb_middleband']) &  # Guard
            (dataframe['tema'] > dataframe['tema'].shift(1)) &  # Guard
            (dataframe['volume'] > 0)  # Make sure Volume is not 0
        ),
        ['buy', 'buy_tag']] = (1, 'rsi_cross')

    return dataframe
```Sau đó:```python hl_lines="1 9"
def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
    dataframe.loc[
        (
            (qtpylib.crossed_above(dataframe['rsi'], 30)) &  # Signal: RSI crosses above 30
            (dataframe['tema'] <= dataframe['bb_middleband']) &  # Guard
            (dataframe['tema'] > dataframe['tema'].shift(1)) &  # Guard
            (dataframe['volume'] > 0)  # Make sure Volume is not 0
        ),
        ['enter_long', 'enter_tag']] = (1, 'rsi_cross')

    return dataframe
```Vui lòng tham khảo [Tài liệu chiến lược](strategy-customization.md#entry-signal-rules) về cách vào và thoát các giao dịch bán.### `populate_sell_trend`
Tương tự như `populate_buy_trend`, `populate_sell_trend()` sẽ được đổi tên thành `populate_exit_trend()`.
Chúng tôi cũng sẽ thay đổi cột từ `'sell'` thành `'exit_long'`.``` python hl_lines="1 9"
def populate_sell_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
    dataframe.loc[
        (
            (qtpylib.crossed_above(dataframe['rsi'], 70)) &  # Signal: RSI crosses above 70
            (dataframe['tema'] > dataframe['bb_middleband']) &  # Guard
            (dataframe['tema'] < dataframe['tema'].shift(1)) &  # Guard
            (dataframe['volume'] > 0)  # Make sure Volume is not 0
        ),
        ['sell', 'exit_tag']] = (1, 'some_exit_tag')
    return dataframe
```Sau đó``` python hl_lines="1 9"
def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
    dataframe.loc[
        (
            (qtpylib.crossed_above(dataframe['rsi'], 70)) &  # Signal: RSI crosses above 70
            (dataframe['tema'] > dataframe['bb_middleband']) &  # Guard
            (dataframe['tema'] < dataframe['tema'].shift(1)) &  # Guard
            (dataframe['volume'] > 0)  # Make sure Volume is not 0
        ),
        ['exit_long', 'exit_tag']] = (1, 'some_exit_tag')
    return dataframe
```Vui lòng tham khảo [Tài liệu chiến lược](strategy-customization.md#exit-signal-rules) để biết cách vào và thoát các giao dịch bán.### `custom_sell`
`custom_sell` đã được đổi tên thành `custom_exit`.
Giờ đây, nó cũng được gọi cho mỗi lần lặp lại, không phụ thuộc vào cài đặt lợi nhuận hiện tại và `exit_profit_only`.``` python hl_lines="2"
class AwesomeStrategy(IStrategy):
    def custom_sell(self, pair: str, trade: 'Trade', current_time: 'datetime', current_rate: float,
                    current_profit: float, **kwargs):
        dataframe, _ = self.dp.get_analyzed_dataframe(pair, self.timeframe)
        last_candle = dataframe.iloc[-1].squeeze()
        # ...
`````` python hl_lines="2"
class AwesomeStrategy(IStrategy):
    def custom_exit(self, pair: str, trade: 'Trade', current_time: 'datetime', current_rate: float,
                    current_profit: float, **kwargs):
        dataframe, _ = self.dp.get_analyzed_dataframe(pair, self.timeframe)
        last_candle = dataframe.iloc[-1].squeeze()
        # ...
```### `custom_entry_timeout`
`check_buy_timeout()` đã được đổi tên thành `check_entry_timeout()` và `check_sell_timeout()` đã được đổi tên thành `check_exit_timeout()`.``` python hl_lines="2 6"
class AwesomeStrategy(IStrategy):
    def check_buy_timeout(self, pair: str, trade: 'Trade', order: dict, 
                            current_time: datetime, **kwargs) -> bool:
        return False

    def check_sell_timeout(self, pair: str, trade: 'Trade', order: dict, 
                            current_time: datetime, **kwargs) -> bool:
        return False 
`````` python hl_lines="2 6"
class AwesomeStrategy(IStrategy):
    def check_entry_timeout(self, pair: str, trade: 'Trade', order: 'Order', 
                            current_time: datetime, **kwargs) -> bool:
        return False

    def check_exit_timeout(self, pair: str, trade: 'Trade', order: 'Order', 
                            current_time: datetime, **kwargs) -> bool:
        return False 
```### `custom_stake_amount`
Đối số chuỗi mới `side` - có thể là `"dài"` hoặc `"ngắn"`.``` python hl_lines="4"
class AwesomeStrategy(IStrategy):
    def custom_stake_amount(self, pair: str, current_time: datetime, current_rate: float,
                            proposed_stake: float, min_stake: Optional[float], max_stake: float,
                            entry_tag: Optional[str], **kwargs) -> float:
        # ... 
        return proposed_stake
`````` python hl_lines="4"
class AwesomeStrategy(IStrategy):
    def custom_stake_amount(self, pair: str, current_time: datetime, current_rate: float,
                            proposed_stake: float, min_stake: float | None, max_stake: float,
                            entry_tag: str | None, side: str, **kwargs) -> float:
        # ... 
        return proposed_stake
```### `confirm_trade_entry`
Đối số chuỗi mới `side` - có thể là `"dài"` hoặc `"ngắn"`.``` python hl_lines="4"
class AwesomeStrategy(IStrategy):
    def confirm_trade_entry(self, pair: str, order_type: str, amount: float, rate: float,
                            time_in_force: str, current_time: datetime, entry_tag: Optional[str], 
                            **kwargs) -> bool:
      return True
```Sau đó:``` python hl_lines="4"
class AwesomeStrategy(IStrategy):
    def confirm_trade_entry(self, pair: str, order_type: str, amount: float, rate: float,
                            time_in_force: str, current_time: datetime, entry_tag: str | None, 
                            side: str, **kwargs) -> bool:
      return True
```### `confirm_trade_exit`
Đã thay đổi đối số `sell_reason` thành `exit_reason`.
Để tương thích, `sell_reason` vẫn sẽ được cung cấp trong một khoảng thời gian giới hạn.``` python hl_lines="3"
class AwesomeStrategy(IStrategy):
    def confirm_trade_exit(self, pair: str, trade: Trade, order_type: str, amount: float,
                           rate: float, time_in_force: str, sell_reason: str,
                           current_time: datetime, **kwargs) -> bool:
    return True
```Sau đó:``` python hl_lines="3"
class AwesomeStrategy(IStrategy):
    def confirm_trade_exit(self, pair: str, trade: Trade, order_type: str, amount: float,
                           rate: float, time_in_force: str, exit_reason: str,
                           current_time: datetime, **kwargs) -> bool:
    return True
```### `custom_entry_price`
Đối số chuỗi mới `side` - có thể là `"dài"` hoặc `"ngắn"`.``` python hl_lines="3"
class AwesomeStrategy(IStrategy):
    def custom_entry_price(self, pair: str, current_time: datetime, proposed_rate: float,
                           entry_tag: Optional[str], **kwargs) -> float:
      return proposed_rate
```Sau đó:``` python hl_lines="3"
class AwesomeStrategy(IStrategy):
    def custom_entry_price(self, pair: str, trade: Trade | None, current_time: datetime, proposed_rate: float,
                           entry_tag: str | None, side: str, **kwargs) -> float:
      return proposed_rate
```### Điều chỉnh thay đổi vị thế giao dịch

Mặc dù bản thân vị thế giao dịch điều chỉnh không thay đổi nhưng bạn không nên sử dụng `trade.nr_of_successful_buys` nữa - mà thay vào đó hãy sử dụng `trade.nr_of_successful_entries`, cũng sẽ bao gồm các mục nhập ngắn.

### Phương thức trợ giúp

Đã thêm đối số "is_short" vào `stoploss_from_open` và `stoploss_from_absolute`.
Điều này phải được gán giá trị là `trade.is_short`.``` python hl_lines="5 7"
    def custom_stoploss(self, pair: str, trade: 'Trade', current_time: datetime,
                        current_rate: float, current_profit: float, **kwargs) -> float:
        # once the profit has risen above 10%, keep the stoploss at 7% above the open price
        if current_profit > 0.10:
            return stoploss_from_open(0.07, current_profit)

        return stoploss_from_absolute(current_rate - (candle['atr'] * 2), current_rate)

        return 1

```Sau đó:``` python hl_lines="5 7"
    def custom_stoploss(self, pair: str, trade: 'Trade', current_time: datetime,
                        current_rate: float, current_profit: float, after_fill: bool, 
                        **kwargs) -> float | None:
        # once the profit has risen above 10%, keep the stoploss at 7% above the open price
        if current_profit > 0.10:
            return stoploss_from_open(0.07, current_profit, is_short=trade.is_short)

        return stoploss_from_absolute(current_rate - (candle['atr'] * 2), current_rate, is_short=trade.is_short, leverage=trade.leverage)


```### Cài đặt chiến lược/cấu hình#### `order_time_in_force`
Thuộc tính `order_time_in_force` đã thay đổi từ `"mua"` thành `"nhập"` và `"bán"` thành `"thoát"`.``` python
    order_time_in_force: dict = {
        "buy": "gtc",
        "sell": "gtc",
    }
```Sau đó:``` python hl_lines="2 3"
    order_time_in_force: dict = {
        "entry": "GTC",
        "exit": "GTC",
    }
```#### `order_types`
`order_types` đã thay đổi tất cả các từ ngữ từ `buy` thành `entry` - và `sell` thành `exit`.
Và hai từ được nối với nhau bằng `_`.``` python hl_lines="2-6"
    order_types = {
        "buy": "limit",
        "sell": "limit",
        "emergencysell": "market",
        "forcesell": "market",
        "forcebuy": "market",
        "stoploss": "market",
        "stoploss_on_exchange": false,
        "stoploss_on_exchange_interval": 60
    }
```Sau đó:``` python hl_lines="2-6"
    order_types = {
        "entry": "limit",
        "exit": "limit",
        "emergency_exit": "market",
        "force_exit": "market",
        "force_entry": "market",
        "stoploss": "market",
        "stoploss_on_exchange": false,
        "stoploss_on_exchange_interval": 60
    }
```#### Cài đặt cấp độ chiến lược

* `use_sell_signal` -> `use_exit_signal`
* `chỉ bán_lợi nhuận` -> `chỉ thoát_lợi nhuận`
* `bán_lợi nhuận_bù đắp` -> `exit_profit_offset`
* `ignore_roi_if_buy_signal` -> `ignore_roi_if_entry_signal```` python hl_lines="2-5"
    # These values can be overridden in the config.
    use_sell_signal = True
    sell_profit_only = True
    sell_profit_offset: 0.01
    ignore_roi_if_buy_signal = False
```Sau đó:``` python hl_lines="2-5"
    # These values can be overridden in the config.
    use_exit_signal = True
    exit_profit_only = True
    exit_profit_offset: 0.01
    ignore_roi_if_entry_signal = False
```#### `unfilledtimeout`
`unfilledtimeout` đã thay đổi tất cả các từ từ `buy` thành `entry` - và `sell` thành `exit`.``` python hl_lines="2-3"
unfilledtimeout = {
        "buy": 10,
        "sell": 10,
        "exit_timeout_count": 0,
        "unit": "minutes"
    }
```Sau đó:``` python hl_lines="2-3"
unfilledtimeout = {
        "entry": 10,
        "exit": 10,
        "exit_timeout_count": 0,
        "unit": "minutes"
    }
```#### `order pricing`
Giá đặt hàng thay đổi theo 2 cách. `chiến lược giá thầu` đã được đổi tên thành `entry_pricing` và `ask_strategy` được đổi tên thành `exit_pricing`.
Các thuộc tính `ask_last_balance` -> `price_last_balance` và `bid_last_balance` -> `price_last_balance` cũng được đổi tên.
Ngoài ra, mặt giá bây giờ có thể được định nghĩa là `ask`, `bid`, `same` hoặc `other`.
Vui lòng tham khảo [tài liệu về giá](configuration.md#prices-used-for-orders) để biết thêm thông tin.``` json hl_lines="2-3 6 12-13 16"
{
    "bid_strategy": {
        "price_side": "bid",
        "use_order_book": true,
        "order_book_top": 1,
        "ask_last_balance": 0.0,
        "check_depth_of_market": {
            "enabled": false,
            "bids_to_ask_delta": 1
        }
    },
    "ask_strategy":{
        "price_side": "ask",
        "use_order_book": true,
        "order_book_top": 1,
        "bid_last_balance": 0.0
        "ignore_buying_expired_candle_after": 120
    }
}
```sau đó:``` json  hl_lines="2-3 6 12-13 16"
{
    "entry_pricing": {
        "price_side": "same",
        "use_order_book": true,
        "order_book_top": 1,
        "price_last_balance": 0.0,
        "check_depth_of_market": {
            "enabled": false,
            "bids_to_ask_delta": 1
        }
    },
    "exit_pricing":{
        "price_side": "same",
        "use_order_book": true,
        "order_book_top": 1,
        "price_last_balance": 0.0
    },
    "ignore_buying_expired_candle_after": 120
}
```## Chiến lược FreqAI

Phương thức `populate_any_indicators()` đã được chia thành `feature_engineering_expand_all()`, `feature_engineering_expand_basic()`, `feature_engineering_standard()` và`set_freqai_targets()`.

Đối với mỗi chức năng mới, cặp (và khung thời gian nếu cần) sẽ tự động được thêm vào cột.
Như vậy, việc định nghĩa các tính năng trở nên đơn giản hơn nhiều với logic mới.

Để biết giải thích đầy đủ về từng phương pháp, vui lòng truy cập [trang tài liệu freqAI] tương ứng (freqai-feature-engineering.md#defining-the-features)``` python linenums="1" hl_lines="12-37 39-42 63-65 67-75"

def populate_any_indicators(
        self, pair, df, tf, informative=None, set_generalized_indicators=False
    ):

        if informative is None:
            informative = self.dp.get_pair_dataframe(pair, tf)

        # first loop is automatically duplicating indicators for time periods
        for t in self.freqai_info["feature_parameters"]["indicator_periods_candles"]:

            t = int(t)
            informative[f"%-{pair}rsi-period_{t}"] = ta.RSI(informative, timeperiod=t)
            informative[f"%-{pair}mfi-period_{t}"] = ta.MFI(informative, timeperiod=t)
            informative[f"%-{pair}adx-period_{t}"] = ta.ADX(informative, timeperiod=t)
            informative[f"%-{pair}sma-period_{t}"] = ta.SMA(informative, timeperiod=t)
            informative[f"%-{pair}ema-period_{t}"] = ta.EMA(informative, timeperiod=t)

            bollinger = qtpylib.bollinger_bands(
                qtpylib.typical_price(informative), window=t, stds=2.2
            )
            informative[f"{pair}bb_lowerband-period_{t}"] = bollinger["lower"]
            informative[f"{pair}bb_middleband-period_{t}"] = bollinger["mid"]
            informative[f"{pair}bb_upperband-period_{t}"] = bollinger["upper"]

            informative[f"%-{pair}bb_width-period_{t}"] = (
                informative[f"{pair}bb_upperband-period_{t}"]
                - informative[f"{pair}bb_lowerband-period_{t}"]
            ) / informative[f"{pair}bb_middleband-period_{t}"]
            informative[f"%-{pair}close-bb_lower-period_{t}"] = (
                informative["close"] / informative[f"{pair}bb_lowerband-period_{t}"]
            )

            informative[f"%-{pair}roc-period_{t}"] = ta.ROC(informative, timeperiod=t)

            informative[f"%-{pair}relative_volume-period_{t}"] = (
                informative["volume"] / informative["volume"].rolling(t).mean()
            ) # (1)

        informative[f"%-{pair}pct-change"] = informative["close"].pct_change()
        informative[f"%-{pair}raw_volume"] = informative["volume"]
        informative[f"%-{pair}raw_price"] = informative["close"]
        # (2)

        indicators = [col for col in informative if col.startswith("%")]
        # This loop duplicates and shifts all indicators to add a sense of recency to data
        for n in range(self.freqai_info["feature_parameters"]["include_shifted_candles"] + 1):
            if n == 0:
                continue
            informative_shift = informative[indicators].shift(n)
            informative_shift = informative_shift.add_suffix("_shift-" + str(n))
            informative = pd.concat((informative, informative_shift), axis=1)

        df = merge_informative_pair(df, informative, self.config["timeframe"], tf, ffill=True)
        skip_columns = [
            (s + "_" + tf) for s in ["date", "open", "high", "low", "close", "volume"]
        ]
        df = df.drop(columns=skip_columns)

        # Add generalized indicators here (because in live, it will call this
        # function to populate indicators during training). Notice how we ensure not to
        # add them multiple times
        if set_generalized_indicators:
            df["%-day_of_week"] = (df["date"].dt.dayofweek + 1) / 7
            df["%-hour_of_day"] = (df["date"].dt.hour + 1) / 25
            # (3)

            # user adds targets here by prepending them with &- (see convention below)
            df["&-s_close"] = (
                df["close"]
                .shift(-self.freqai_info["feature_parameters"]["label_period_candles"])
                .rolling(self.freqai_info["feature_parameters"]["label_period_candles"])
                .mean()
                / df["close"]
                - 1
            )  # (4)

        return df
```1. Tính năng - Di chuyển đến `feature_engineering_expand_all`
2. Các tính năng cơ bản, chưa được mở rộng trên `indicator_ Periods_candles` - chuyển đến`feature_engineering_expand_basic()`.
3. Các tính năng tiêu chuẩn không nên mở rộng - chuyển đến `feature_engineering_standard()`.
4. Mục tiêu - Di chuyển phần này tới `set_freqai_targets()`.

### freqai - kỹ thuật tính năng mở rộng tất cả

Các tính năng bây giờ sẽ tự động mở rộng. Do đó, các vòng lặp mở rộng cũng như các phần `{pair}` / `{timeframe}` sẽ cần phải được loại bỏ.``` python linenums="1"
    def feature_engineering_expand_all(self, dataframe, period, **kwargs) -> DataFrame::
        """
        *Only functional with FreqAI enabled strategies*
        This function will automatically expand the defined features on the config defined
        `indicator_periods_candles`, `include_timeframes`, `include_shifted_candles`, and
        `include_corr_pairs`. In other words, a single feature defined in this function
        will automatically expand to a total of
        `indicator_periods_candles` * `include_timeframes` * `include_shifted_candles` *
        `include_corr_pairs` numbers of features added to the model.

        All features must be prepended with `%` to be recognized by FreqAI internals.

        More details on how these config defined parameters accelerate feature engineering
        in the documentation at:

        https://www.freqtrade.io/en/stable/freqai-parameter-table/#feature-parameters

        https://www.freqtrade.io/en/stable/freqai-feature-engineering/#defining-the-features

        :param df: strategy dataframe which will receive the features
        :param period: period of the indicator - usage example:
        dataframe["%-ema-period"] = ta.EMA(dataframe, timeperiod=period)
        """

        dataframe["%-rsi-period"] = ta.RSI(dataframe, timeperiod=period)
        dataframe["%-mfi-period"] = ta.MFI(dataframe, timeperiod=period)
        dataframe["%-adx-period"] = ta.ADX(dataframe, timeperiod=period)
        dataframe["%-sma-period"] = ta.SMA(dataframe, timeperiod=period)
        dataframe["%-ema-period"] = ta.EMA(dataframe, timeperiod=period)

        bollinger = qtpylib.bollinger_bands(
            qtpylib.typical_price(dataframe), window=period, stds=2.2
        )
        dataframe["bb_lowerband-period"] = bollinger["lower"]
        dataframe["bb_middleband-period"] = bollinger["mid"]
        dataframe["bb_upperband-period"] = bollinger["upper"]

        dataframe["%-bb_width-period"] = (
            dataframe["bb_upperband-period"]
            - dataframe["bb_lowerband-period"]
        ) / dataframe["bb_middleband-period"]
        dataframe["%-close-bb_lower-period"] = (
            dataframe["close"] / dataframe["bb_lowerband-period"]
        )

        dataframe["%-roc-period"] = ta.ROC(dataframe, timeperiod=period)

        dataframe["%-relative_volume-period"] = (
            dataframe["volume"] / dataframe["volume"].rolling(period).mean()
        )

        return dataframe

```### Freqai - tính năng kỹ thuật cơ bản

Các tính năng cơ bản. Đảm bảo xóa phần `{pair}` khỏi đối tượng địa lý của bạn.``` python linenums="1"
    def feature_engineering_expand_basic(self, dataframe: DataFrame, **kwargs) -> DataFrame::
        """
        *Only functional with FreqAI enabled strategies*
        This function will automatically expand the defined features on the config defined
        `include_timeframes`, `include_shifted_candles`, and `include_corr_pairs`.
        In other words, a single feature defined in this function
        will automatically expand to a total of
        `include_timeframes` * `include_shifted_candles` * `include_corr_pairs`
        numbers of features added to the model.

        Features defined here will *not* be automatically duplicated on user defined
        `indicator_periods_candles`

        All features must be prepended with `%` to be recognized by FreqAI internals.

        More details on how these config defined parameters accelerate feature engineering
        in the documentation at:

        https://www.freqtrade.io/en/stable/freqai-parameter-table/#feature-parameters

        https://www.freqtrade.io/en/stable/freqai-feature-engineering/#defining-the-features

        :param df: strategy dataframe which will receive the features
        dataframe["%-pct-change"] = dataframe["close"].pct_change()
        dataframe["%-ema-200"] = ta.EMA(dataframe, timeperiod=200)
        """
        dataframe["%-pct-change"] = dataframe["close"].pct_change()
        dataframe["%-raw_volume"] = dataframe["volume"]
        dataframe["%-raw_price"] = dataframe["close"]
        return dataframe
```### FreqAI - tiêu chuẩn kỹ thuật tính năng``` python linenums="1"
    def feature_engineering_standard(self, dataframe: DataFrame, **kwargs) -> DataFrame:
        """
        *Only functional with FreqAI enabled strategies*
        This optional function will be called once with the dataframe of the base timeframe.
        This is the final function to be called, which means that the dataframe entering this
        function will contain all the features and columns created by all other
        freqai_feature_engineering_* functions.

        This function is a good place to do custom exotic feature extractions (e.g. tsfresh).
        This function is a good place for any feature that should not be auto-expanded upon
        (e.g. day of the week).

        All features must be prepended with `%` to be recognized by FreqAI internals.

        More details about feature engineering available:

        https://www.freqtrade.io/en/stable/freqai-feature-engineering

        :param df: strategy dataframe which will receive the features
        usage example: dataframe["%-day_of_week"] = (dataframe["date"].dt.dayofweek + 1) / 7
        """
        dataframe["%-day_of_week"] = dataframe["date"].dt.dayofweek
        dataframe["%-hour_of_day"] = dataframe["date"].dt.hour
        return dataframe
```### FreqAI - đặt mục tiêu

Các mục tiêu giờ đây đã có phương pháp riêng của mình.``` python linenums="1"
    def set_freqai_targets(self, dataframe: DataFrame, **kwargs) -> DataFrame:
        """
        *Only functional with FreqAI enabled strategies*
        Required function to set the targets for the model.
        All targets must be prepended with `&` to be recognized by the FreqAI internals.

        More details about feature engineering available:

        https://www.freqtrade.io/en/stable/freqai-feature-engineering

        :param df: strategy dataframe which will receive the targets
        usage example: dataframe["&-target"] = dataframe["close"].shift(-1) / dataframe["close"]
        """
        dataframe["&-s_close"] = (
            dataframe["close"]
            .shift(-self.freqai_info["feature_parameters"]["label_period_candles"])
            .rolling(self.freqai_info["feature_parameters"]["label_period_candles"])
            .mean()
            / dataframe["close"]
            - 1
            )

        return dataframe
```### FreqAI - Đường dẫn dữ liệu mới

Nếu bạn đã tạo `IFreqaiModel` tùy chỉnh của riêng mình với hàm `train()`/`predict()` tùy chỉnh, *và* bạn vẫn dựa vào `data_cleaning_train/predict()`, thì bạn sẽ cần phải di chuyển sang quy trình mới. Nếu mô hình của bạn *không* dựa vào `data_cleaning_train/predict()` thì bạn không cần phải lo lắng về việc di chuyển này. Điều đó có nghĩa là hướng dẫn di chuyển này phù hợp với một tỷ lệ rất nhỏ người dùng thành thạo. Nếu bạn vô tình xem được hướng dẫn này, vui lòng hỏi kỹ hơn về vấn đề của bạn trong máy chủ bất hòa Freqtrade.

Việc chuyển đổi trước tiên bao gồm việc xóa `data_cleaning_train/predict()` và thay thế chúng bằng hàm `define_data_pipeline()` và `define_label_pipeline()` cho lớp `IFreqaiModel` của bạn:```python  linenums="1" hl_lines="11-14 47-49 55-57"
class MyCoolFreqaiModel(BaseRegressionModel):
    """
    Some cool custom IFreqaiModel you made before Freqtrade version 2023.6
    """
    def train(
        self, unfiltered_df: DataFrame, pair: str, dk: FreqaiDataKitchen, **kwargs
    ) -> Any:

        # ... your custom stuff

        # Remove these lines
        # data_dictionary = dk.make_train_test_datasets(features_filtered, labels_filtered)
        # self.data_cleaning_train(dk)
        # data_dictionary = dk.normalize_data(data_dictionary)
        # (1)

        # Add these lines. Now we control the pipeline fit/transform ourselves
        dd = dk.make_train_test_datasets(features_filtered, labels_filtered)
        dk.feature_pipeline = self.define_data_pipeline(threads=dk.thread_count)
        dk.label_pipeline = self.define_label_pipeline(threads=dk.thread_count)

        (dd["train_features"],
         dd["train_labels"],
         dd["train_weights"]) = dk.feature_pipeline.fit_transform(dd["train_features"],
                                                                  dd["train_labels"],
                                                                  dd["train_weights"])

        (dd["test_features"],
         dd["test_labels"],
         dd["test_weights"]) = dk.feature_pipeline.transform(dd["test_features"],
                                                             dd["test_labels"],
                                                             dd["test_weights"])

        dd["train_labels"], _, _ = dk.label_pipeline.fit_transform(dd["train_labels"])
        dd["test_labels"], _, _ = dk.label_pipeline.transform(dd["test_labels"])

        # ... your custom code

        return model

    def predict(
        self, unfiltered_df: DataFrame, dk: FreqaiDataKitchen, **kwargs
    ) -> tuple[DataFrame, npt.NDArray[np.int_]]:

        # ... your custom stuff

        # Remove these lines:
        # self.data_cleaning_predict(dk)
        # (2)

        # Add these lines:
        dk.data_dictionary["prediction_features"], outliers, _ = dk.feature_pipeline.transform(
            dk.data_dictionary["prediction_features"], outlier_check=True)

        # Remove this line
        # pred_df = dk.denormalize_labels_from_metadata(pred_df)
        # (3)

        # Replace with these lines
        pred_df, _, _ = dk.label_pipeline.inverse_transform(pred_df)
        if self.freqai_info.get("DI_threshold", 0) > 0:
            dk.DI_values = dk.feature_pipeline["di"].di_values
        else:
            dk.DI_values = np.zeros(outliers.shape[0])
        dk.do_predict = outliers

        # ... your custom code
        return (pred_df, dk.do_predict)
```1. Việc chuẩn hóa và làm sạch dữ liệu hiện đã được đồng nhất hóa với định nghĩa quy trình mới. Điều này được tạo trong các hàm `define_data_pipeline()` và `define_label_pipeline()` mới. Các hàm `data_cleaning_train()` và `data_cleaning_predict()` không còn được sử dụng nữa. Bạn có thể ghi đè `define_data_pipeline()` để tạo đường dẫn tùy chỉnh của riêng mình nếu muốn.
2. Việc chuẩn hóa và làm sạch dữ liệu hiện đã được đồng nhất hóa với định nghĩa quy trình mới. Điều này được tạo trong các hàm `define_data_pipeline()` và `define_label_pipeline()` mới. Các hàm `data_cleaning_train()` và `data_cleaning_predict()` không còn được sử dụng nữa. Bạn có thể ghi đè `define_data_pipeline()` để tạo đường dẫn tùy chỉnh của riêng mình nếu muốn.
3. Việc không chuẩn hóa dữ liệu được thực hiện với đường dẫn mới. Thay thế điều này bằng các dòng dưới đây.