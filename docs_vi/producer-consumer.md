<!-- Auto-translated from docs/ by script. Please review technical terms. -->

# Chế độ nhà sản xuất / người tiêu dùng

freqtrade cung cấp một cơ chế trong đó một phiên bản (còn được gọi là `consumer`) có thể nghe tin nhắn từ một phiên bản freqtrade ngược dòng (còn được gọi là `producer`) bằng cách sử dụng websocket tin nhắn. Chủ yếu là các tin nhắn `analyzed_df` và `whitelist`. Điều này cho phép tái sử dụng các chỉ báo (và tín hiệu) đã tính toán cho các cặp trong nhiều bot mà không cần phải tính toán chúng nhiều lần.

Xem [Message Websocket](rest-api.md#message-websocket) trong tài liệu Rest API để thiết lập cấu hình `api_server` cho websocket tin nhắn của bạn (đây sẽ là nhà sản xuất của bạn).

!!! Lưu ý
    Chúng tôi thực sự khuyên bạn nên đặt `ws_token` thành thứ gì đó ngẫu nhiên và chỉ có bạn biết để tránh truy cập trái phép vào bot của bạn.

## Cấu hình

Cho phép đăng ký một phiên bản bằng cách thêm phần `external_message_consumer` vào tệp cấu hình của người tiêu dùng.```json
{
    //...
   "external_message_consumer": {
        "enabled": true,
        "producers": [
            {
                "name": "default", // This can be any name you'd like, default is "default"
                "host": "127.0.0.1", // The host from your producer's api_server config
                "port": 8080, // The port from your producer's api_server config
                "secure": false, // Use a secure websockets connection, default false
                "ws_token": "sercet_Ws_t0ken" // The ws_token from your producer's api_server config
            }
        ],
        // The following configurations are optional, and usually not required
        // "wait_timeout": 300,
        // "ping_timeout": 10,
        // "sleep_time": 10,
        // "remove_entry_exit_signals": false,
        // "message_size_limit": 8
    }
    //...
}
```|  Tham số | Mô tả |
|----------||-------------|
| `đã bật` | **Bắt buộc.** Bật chế độ tiêu dùng. Nếu được đặt thành sai, tất cả các cài đặt khác trong phần này sẽ bị bỏ qua.<br>*Mặc định là `false`.*<br> **Datatype:** boolean .
| `nhà sản xuất` | **Bắt buộc.** Danh sách nhà sản xuất <br> **Loại dữ liệu:** Array.
| `nhà sản xuất.name` | **Bắt buộc.** Tên của nhà sản xuất này. Tên này phải được sử dụng trong lệnh gọi tới `get_producer_pairs()` và `get_producer_df()` nếu có nhiều hơn một nhà sản xuất được sử dụng.<br> **Datatype:** string
| `nhà sản xuất.host` | **Bắt buộc.** Tên máy chủ hoặc địa chỉ IP từ nhà sản xuất của bạn.<br> **Loại dữ liệu:** chuỗi
| `nhà sản xuất.port` | **Bắt buộc.** Cổng khớp với máy chủ ở trên.<br>*Mặc định là `8080`.*<br> **Loại dữ liệu:** Số nguyên
| `nhà sản xuất.secure` | **Tùy chọn.** Sử dụng ssl trong kết nối ổ cắm web. Mặc định là Sai.<br> **Loại dữ liệu:** chuỗi
| `producers.ws_token` | **Bắt buộc.** `ws_token` như được định cấu hình trên nhà sản xuất.<br> **Loại dữ liệu:** chuỗi
| | **Cài đặt tùy chọn**
| `chờ_thời gian chờ` | Hết thời gian cho đến khi chúng tôi ping lại nếu không nhận được tin nhắn. <br>*Mặc định là `300`.*<br> **Loại dữ liệu:** Số nguyên - tính bằng giây.
| `ping_timeout` | Hết thời gian chờ Ping <br>*Mặc định là `10`.*<br> **Loại dữ liệu:** Số nguyên - tính bằng giây.
| `thời gian ngủ` | Thời gian ngủ trước khi thử kết nối lại.<br>*Mặc định là `10`.*<br> **Loại dữ liệu:** Số nguyên - tính bằng giây.
| `remove_entry_exit_signals` | Xóa các cột tín hiệu khỏi khung dữ liệu (đặt chúng thành 0) khi nhận khung dữ liệu.<br>*Mặc định là `false`.*<br> **Loại dữ liệu:** Boolean.
| `ban_candle_limit` | Những nến ban đầu được mong đợi từ Nhà sản xuất.<br>*Mặc định là `1500`.*<br> **Loại dữ liệu:** Số nguyên - Số lượng nến.
| `tin nhắn_size_limit` | Giới hạn kích thước cho mỗi tin nhắn<br>*Mặc định là `8`.*<br> **Loại dữ liệu:** Số nguyên - Megabyte.

Thay vì (hoặc cũng như) tính toán các chỉ báo trong `populate_indicators()`, phiên bản người theo dõi lắng nghe kết nối với thông báo của phiên bản nhà sản xuất (hoặc nhiều phiên bản nhà sản xuất trong cấu hình nâng cao) và yêu cầu các khung dữ liệu được phân tích gần đây nhất của nhà sản xuất cho từng cặp trong danh sách trắng đang hoạt động.

Sau đó, một phiên bản tiêu dùng sẽ có bản sao đầy đủ của các khung dữ liệu được phân tích mà không cần phải tự tính toán chúng.

## Ví dụ

### Ví dụ - Chiến lược của nhà sản xuất

Một chiến lược đơn giản với nhiều chỉ số. Không có cân nhắc đặc biệt nào được yêu cầu trong chiến lược.```py
class ProducerStrategy(IStrategy):
    #...
    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Calculate indicators in the standard freqtrade way which can then be broadcast to other instances
        """
        dataframe['rsi'] = ta.RSI(dataframe)
        bollinger = qtpylib.bollinger_bands(qtpylib.typical_price(dataframe), window=20, stds=2)
        dataframe['bb_lowerband'] = bollinger['lower']
        dataframe['bb_middleband'] = bollinger['mid']
        dataframe['bb_upperband'] = bollinger['upper']
        dataframe['tema'] = ta.TEMA(dataframe, timeperiod=9)

        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Populates the entry signal for the given dataframe
        """
        dataframe.loc[
            (
                (qtpylib.crossed_above(dataframe['rsi'], self.buy_rsi.value)) &
                (dataframe['tema'] <= dataframe['bb_middleband']) &
                (dataframe['tema'] > dataframe['tema'].shift(1)) &
                (dataframe['volume'] > 0)
            ),
            'enter_long'] = 1

        return dataframe
```!!! Mẹo "Tần suất AI"
    Bạn có thể sử dụng điều này để thiết lập [FreqAI](freqai.md) trên một máy mạnh mẽ, trong khi bạn điều hành người tiêu dùng trên các máy đơn giản như quả mâm xôi, có thể diễn giải các tín hiệu được tạo từ nhà sản xuất theo nhiều cách khác nhau.


### Ví dụ - Chiến lược tiêu dùng

Một chiến lược tương đương về mặt logic không tự tính toán các chỉ số nhưng sẽ có sẵn các khung dữ liệu được phân tích tương tự để đưa ra quyết định giao dịch dựa trên các chỉ số được tính toán trong nhà sản xuất. Trong ví dụ này, người tiêu dùng có cùng tiêu chí đầu vào, tuy nhiên điều này không cần thiết. Người tiêu dùng có thể sử dụng logic khác nhau để vào/ra giao dịch và chỉ sử dụng các chỉ báo theo quy định.```py
class ConsumerStrategy(IStrategy):
    #...
    process_only_new_candles = False # required for consumers

    _columns_to_expect = ['rsi_default', 'tema_default', 'bb_middleband_default']

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Use the websocket api to get pre-populated indicators from another freqtrade instance.
        Use `self.dp.get_producer_df(pair)` to get the dataframe
        """
        pair = metadata['pair']
        timeframe = self.timeframe

        producer_pairs = self.dp.get_producer_pairs()
        # You can specify which producer to get pairs from via:
        # self.dp.get_producer_pairs("my_other_producer")

        # This func returns the analyzed dataframe, and when it was analyzed
        producer_dataframe, _ = self.dp.get_producer_df(pair)
        # You can get other data if the producer makes it available:
        # self.dp.get_producer_df(
        #   pair,
        #   timeframe="1h",
        #   candle_type=CandleType.SPOT,
        #   producer_name="my_other_producer"
        # )

        if not producer_dataframe.empty:
            # If you plan on passing the producer's entry/exit signal directly,
            # specify ffill=False or it will have unintended results
            merged_dataframe = merge_informative_pair(dataframe, producer_dataframe,
                                                      timeframe, timeframe,
                                                      append_timeframe=False,
                                                      suffix="default")
            return merged_dataframe
        else:
            dataframe[self._columns_to_expect] = 0

        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Populates the entry signal for the given dataframe
        """
        # Use the dataframe columns as if we calculated them ourselves
        dataframe.loc[
            (
                (qtpylib.crossed_above(dataframe['rsi_default'], self.buy_rsi.value)) &
                (dataframe['tema_default'] <= dataframe['bb_middleband_default']) &
                (dataframe['tema_default'] > dataframe['tema_default'].shift(1)) &
                (dataframe['volume'] > 0)
            ),
            'enter_long'] = 1

        return dataframe
```!!! Mẹo "Sử dụng tín hiệu ngược dòng"
    Bằng cách đặt `remove_entry_exit_signals=false`, bạn cũng có thể sử dụng trực tiếp tín hiệu của nhà sản xuất. Chúng phải có sẵn dưới dạng `enter_long_default` (giả sử `suffix="default"` đã được sử dụng) - và có thể được sử dụng làm tín hiệu trực tiếp hoặc làm chỉ báo bổ sung.