<!-- Auto-translated from docs/ by script. Please review technical terms. -->

# Hyperopt

Trang này giải thích cách điều chỉnh chiến lược của bạn bằng cách tìm ra chiến lược tối ưu
tham số, một quá trình được gọi là tối ưu hóa siêu tham số. Bot sử dụng các thuật toán có trong gói `optuna` để thực hiện việc này.
Việc tìm kiếm sẽ đốt cháy tất cả các lõi CPU của bạn, khiến máy tính xách tay của bạn phát ra âm thanh như máy bay chiến đấu và vẫn mất nhiều thời gian.

Nói chung, việc tìm kiếm các tham số tốt nhất bắt đầu bằng một vài kết hợp ngẫu nhiên (xem [bên dưới](#reproducible-results) để biết thêm chi tiết) và sau đó sử dụng một trong các thuật toán lấy mẫu của optuna (hiện là NSGAIIISampler) để nhanh chóng tìm thấy tổ hợp các tham số trong siêu không gian tìm kiếm giúp giảm thiểu giá trị của [hàm mất](#loss-functions).

Hyperopt yêu cầu phải có sẵn dữ liệu lịch sử, giống như việc kiểm tra lại (hyperopt chạy kiểm tra lại nhiều lần với các tham số khác nhau).
Để tìm hiểu cách lấy dữ liệu cho các cặp và trao đổi mà bạn quan tâm, hãy đi tới phần [Tải xuống dữ liệu](data-download.md) của tài liệu.

!!! Sâu bọ    Hyperopt can crash when used with only 1 CPU Core as found out in [Issue #1133](https://github.com/freqtrade/freqtrade/issues/1133)
!!! Lưu ý
    Kể từ bản phát hành 2021.4, bạn không còn phải viết một lớp hyperopt riêng mà có thể định cấu hình các tham số trực tiếp trong chiến lược.
    Phương thức cũ được hỗ trợ đến năm 2021.8 và đã bị xóa vào năm 2021.9.

## Cài đặt phụ thuộc hyperopt

Vì các phụ thuộc Hyperopt không cần thiết để tự chạy bot, nặng và không thể dễ dàng xây dựng trên một số nền tảng (như Raspberry PI), nên chúng không được cài đặt theo mặc định. Trước khi chạy Hyperopt, bạn cần cài đặt các phần phụ thuộc tương ứng, như được mô tả trong phần bên dưới.

!!! Lưu ý
    Vì Hyperopt là một quy trình sử dụng nhiều tài nguyên nên việc chạy nó trên Raspberry Pi không được khuyến khích cũng như không hỗ trợ.

### Docker

Docker-image bao gồm các phần phụ thuộc hyperopt, không cần thực hiện thêm hành động nào.

### Tập lệnh cài đặt dễ dàng (setup.sh) / Cài đặt thủ công```bash
source .venv/bin/activate
pip install -r requirements-hyperopt.txt
```## Tham chiếu lệnh Hyperopt

--8<-- "lệnh/hyperopt.md"

### Danh sách kiểm tra Hyperopt

Danh sách kiểm tra tất cả các nhiệm vụ/khả năng trong hyperopt

Tùy thuộc vào không gian bạn muốn tối ưu hóa, chỉ cần một số điều dưới đây:

* xác định các tham số bằng `space='buy'` - để tối ưu hóa tín hiệu vào lệnh
* xác định các tham số bằng `space='sell'` - để tối ưu hóa tín hiệu thoát
* xác định các tham số bằng `space='enter'` - để tối ưu hóa tín hiệu vào lệnh
* xác định các tham số bằng `space='exit'` - để tối ưu hóa tín hiệu thoát
* xác định các tham số với `space='protection'` - để tối ưu hóa bảo vệ
* xác định các tham số bằng `space='random_spacename'` - để kiểm soát tốt hơn những tham số nào được tối ưu hóa cùng nhau

Chọn tên không gian phù hợp nhất với tham số. Chúng tôi khuyên bạn nên sử dụng `buy` / `sell` hoặc `enter` / `exit` để rõ ràng (tuy nhiên không có giới hạn kỹ thuật nào về vấn đề này).

!!! Lưu ý
    `populate_indicators` cần tạo tất cả các chỉ báo mà bất kỳ khoảng trắng nào có thể sử dụng, nếu không hyperopt sẽ không hoạt động.


Hiếm khi bạn cũng cần tạo một [lớp lồng nhau](advanced-hyperopt.md#overriding-pre-define-spaces) có tên `HyperOpt` và triển khai

* `roi_space` - để tối ưu hóa ROI tùy chỉnh (nếu bạn cần phạm vi cho tham số ROI trong siêu không gian tối ưu hóa khác với mặc định)
* `generate_roi_table` - để tối ưu hóa ROI tùy chỉnh (nếu bạn cần phạm vi cho các giá trị trong bảng ROI khác với mặc định hoặc số mục nhập (bước) trong bảng ROI khác với 4 bước mặc định)
* `stoploss_space` - để tối ưu hóa mức dừng lỗ tùy chỉnh (nếu bạn cần phạm vi cho tham số mức dừng lỗ trong siêu không gian tối ưu hóa khác với mặc định)
* `trailing_space` - để tối ưu hóa điểm dừng theo dõi tùy chỉnh (nếu bạn cần phạm vi cho các tham số điểm dừng theo dõi trong siêu không gian tối ưu hóa khác với mặc định)
* `max_open_trades_space` - để tối ưu hóa max_open_trades tùy chỉnh (nếu bạn cần phạm vi cho tham số max_open_trades trong siêu không gian tối ưu hóa khác với mặc định)

!!! Mẹo "Tối ưu hóa nhanh chóng ROI, điểm dừng lỗ và điểm dừng lỗ cuối"
    Bạn có thể nhanh chóng tối ưu hóa các khoảng trống `roi`, `stoploss` và `trailing` mà không thay đổi bất kỳ điều gì trong chiến lược của mình.``` bash
    # Have a working strategy at hand.
    freqtrade hyperopt --hyperopt-loss SharpeHyperOptLossDaily --spaces roi stoploss trailing --strategy MyWorkingStrategy --config config.json -e 100
    ```### Logic thực thi Hyperopt

Trước tiên, Hyperopt sẽ tải dữ liệu của bạn vào bộ nhớ và sau đó sẽ chạy `populate_indicators()` một lần trên mỗi Cặp để tạo tất cả các chỉ báo, trừ khi `--analyze-per-epoch` được chỉ định.

Sau đó, Hyperopt sẽ sinh ra các quy trình khác nhau (số bộ xử lý, hoặc `-j <n>`) và chạy thử nghiệm ngược nhiều lần, thay đổi các tham số là một phần của `--spaces` được xác định.

Đối với mỗi bộ tham số mới, freqtrade sẽ chạy `populate_entry_trend()` đầu tiên, sau đó là `populate_exit_trend()`, sau đó chạy quy trình kiểm tra ngược thông thường để mô phỏng giao dịch.

Sau khi kiểm tra ngược, kết quả sẽ được chuyển vào [hàm mất](#hàm mất). Hàm này sẽ đánh giá xem kết quả này tốt hơn hay kém hơn kết quả trước đó.  
Dựa trên kết quả của hàm mất, hyperopt sẽ xác định bộ tham số tiếp theo để thử trong vòng kiểm tra ngược tiếp theo.

### Định cấu hình Bộ bảo vệ và Bộ kích hoạt của bạn

Có hai vị trí bạn cần thay đổi trong tệp chiến lược của mình để thêm tham số hyperopt mới nhằm tối ưu hóa:

* Xác định các thông số ở cấp độ hyperopt sẽ được tối ưu hóa.
* Trong `populate_entry_trend()` - sử dụng các giá trị tham số được xác định thay vì các hằng số thô.

Ở đó bạn có hai loại chỉ báo khác nhau: 1. `bảo vệ` và 2. `kích hoạt`.

1. Bảo vệ là các điều kiện như "không bao giờ nhập nếu ADX < 10" hoặc không bao giờ nhập nếu giá hiện tại trên EMA10.
2. Trình kích hoạt là những yếu tố thực sự kích hoạt mục nhập trong thời điểm cụ thể, như "nhập khi EMA5 vượt qua EMA10" hoặc "nhập khi giá đóng chạm vào dải Bollinger thấp hơn".

!!! Gợi ý "Bảo vệ và kích hoạt"
    Về mặt kỹ thuật, không có sự khác biệt giữa Guards và Triggers.  
    Tuy nhiên, hướng dẫn này sẽ phân biệt điều này để làm rõ rằng các tín hiệu không được "dính".
    Tín hiệu dính là tín hiệu đang hoạt động cho nhiều nến. Điều này có thể dẫn đến việc nhập tín hiệu muộn (ngay trước khi tín hiệu biến mất - nghĩa là khả năng thành công sẽ thấp hơn rất nhiều so với ngay lúc đầu).

Đối với mỗi vòng kỷ nguyên, tính năng siêu tối ưu hóa sẽ chọn một trình kích hoạt và có thể là nhiều bộ bảo vệ.

####Tối ưu hóa tín hiệu thoát

Tương tự như tín hiệu vào ở trên, tín hiệu thoát cũng có thể được tối ưu hóa.
Đặt các cài đặt tương ứng vào các phương pháp sau

* Xác định các tham số ở cấp độ hyperopt sẽ tối ưu hóa, đặt tên chúng là `sell_*` hoặc bằng cách xác định rõ ràng `space='sell'`.
* Trong `populate_exit_trend()` - sử dụng các giá trị tham số được xác định thay vì các hằng số thô.

Cấu hình và quy tắc giống với tín hiệu mua.

## Giải quyết một bí ẩn

Giả sử bạn tò mò: bạn nên sử dụng đường MACD giao nhau hay Dải Bollinger thấp hơn để kích hoạt các điểm vào lệnh mua của mình.
Và bạn cũng băn khoăn không biết nên sử dụng RSI hay ADX để hỗ trợ cho những quyết định đó.
Nếu bạn quyết định sử dụng RSI hoặc ADX, tôi nên sử dụng giá trị nào cho chúng?

Vì vậy, hãy sử dụng tối ưu hóa siêu tham số để giải quyết bí ẩn này.

### Xác định các chỉ số được sử dụng

Chúng tôi bắt đầu bằng cách tính toán các chỉ số mà chiến lược của chúng tôi sẽ sử dụng.``` python
class MyAwesomeStrategy(IStrategy):

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Generate all indicators used by the strategy
        """
        dataframe['adx'] = ta.ADX(dataframe)
        dataframe['rsi'] = ta.RSI(dataframe)
        macd = ta.MACD(dataframe)
        dataframe['macd'] = macd['macd']
        dataframe['macdsignal'] = macd['macdsignal']
        dataframe['macdhist'] = macd['macdhist']

        bollinger = ta.BBANDS(dataframe, timeperiod=20, nbdevup=2.0, nbdevdn=2.0)
        dataframe['bb_lowerband'] = bollinger['lowerband']
        dataframe['bb_middleband'] = bollinger['middleband']
        dataframe['bb_upperband'] = bollinger['upperband']
        return dataframe
```### Các thông số có thể siêu tùy chọn

Chúng tôi tiếp tục xác định các tham số có thể điều chỉnh được:```python
class MyAwesomeStrategy(IStrategy):
    buy_adx = DecimalParameter(20, 40, decimals=1, default=30.1, space="buy")
    buy_rsi = IntParameter(20, 40, default=30, space="buy")
    buy_adx_enabled = BooleanParameter(default=True, space="buy")
    buy_rsi_enabled = CategoricalParameter([True, False], default=False, space="buy")
    buy_trigger = CategoricalParameter(["bb_lower", "macd_cross_signal"], default="bb_lower", space="buy")
```Định nghĩa trên cho biết: Tôi có năm tham số tôi muốn kết hợp ngẫu nhiên để tìm ra sự kết hợp tốt nhất.  
`buy_rsi` là một tham số số nguyên, sẽ được kiểm tra trong khoảng từ 20 đến 40. Khoảng trắng này có kích thước là 20.  
`buy_adx` là tham số thập phân, sẽ được đánh giá trong khoảng từ 20 đến 40 với 1 chữ số thập phân (vì vậy các giá trị là 20,1, 20,2, ...). Không gian này có kích thước 200.  
Sau đó chúng ta có ba biến danh mục. Hai cái đầu tiên là `Đúng` hoặc `Sai`.
Chúng tôi sử dụng những thứ này để bật hoặc tắt bộ bảo vệ ADX và RSI.
Cái cuối cùng mà chúng tôi gọi là `kích hoạt` và sử dụng nó để quyết định kích hoạt mua nào chúng tôi muốn sử dụng.

!!! Lưu ý "Gán không gian tham số"
    - Các tham số phải được gán cho một biến có tên `buy_*`, `sell_*`, `enter_*` hoặc `exit_*` hoặc `protection_*` - hoặc chứa một khoảng trắng được gán rõ ràng thông qua tham số (`space='buy'`, `space='sell'`, `space='protection'`).  
    - Các tham số có phép gán xung đột (ví dụ: `buy_adx = IntParameter(4, 24, default=14, space='sell')`) sẽ sử dụng phép gán khoảng trắng rõ ràng.  
    - Nếu không có tham số nào cho một khoảng trắng, bạn sẽ gặp lỗi không tìm thấy khoảng trắng khi chạy hyperopt.  
    Các tham số có khoảng trống không rõ ràng (ví dụ: `adx_ Period = IntParameter(4, 24, default=14)` - không có khoảng trống rõ ràng hay ẩn) sẽ không được phát hiện và do đó sẽ bị bỏ qua.
    Các khoảng trắng cũng có thể được đặt tên tùy chỉnh (ví dụ: `space='my_custom_space'`), với giới hạn duy nhất là tên không gian không được là `all`, `default` - và phải dẫn đến một mã định danh python hợp lệ.

Vì vậy, hãy viết chiến lược mua bằng cách sử dụng các giá trị sau:```python
    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        conditions = []
        # GUARDS AND TRENDS
        if self.buy_adx_enabled.value:
            conditions.append(dataframe['adx'] > self.buy_adx.value)
        if self.buy_rsi_enabled.value:
            conditions.append(dataframe['rsi'] < self.buy_rsi.value)

        # TRIGGERS
        if self.buy_trigger.value == 'bb_lower':
            conditions.append(dataframe['close'] < dataframe['bb_lowerband'])
        if self.buy_trigger.value == 'macd_cross_signal':
            conditions.append(qtpylib.crossed_above(
                dataframe['macd'], dataframe['macdsignal']
            ))

        # Check that volume is not 0
        conditions.append(dataframe['volume'] > 0)

        if conditions:
            dataframe.loc[
                reduce(lambda x, y: x & y, conditions),
                'enter_long'] = 1

        return dataframe
```Hyperopt bây giờ sẽ gọi `populate_entry_trend()` nhiều lần (`epochs`) với các kết hợp giá trị khác nhau.  
Nó sẽ sử dụng dữ liệu lịch sử nhất định và mô phỏng các giao dịch mua dựa trên các tín hiệu mua được tạo bằng chức năng trên.  
Dựa trên kết quả, hyperopt sẽ cho bạn biết sự kết hợp tham số nào tạo ra kết quả tốt nhất (dựa trên [hàm mất mát](#hàm mất mát) được định cấu hình).

!!! Lưu ý
    Thiết lập ở trên hy vọng sẽ tìm thấy các dải ADX, RSI và Bollinger Bands trong các chỉ báo được điền sẵn.
    Khi bạn muốn kiểm tra một chỉ báo hiện không được bot sử dụng, hãy nhớ
    thêm nó vào phương thức `populate_indicators()` trong chiến lược hoặc tệp hyperopt của bạn.

## Các loại tham số

Có bốn loại tham số, mỗi loại phù hợp cho các mục đích khác nhau.

* `IntParameter` - xác định một tham số tích phân có ranh giới trên và dưới của không gian tìm kiếm.
* `DecimalParameter` - xác định tham số dấu phẩy động với số thập phân giới hạn (mặc định 3). Nên được ưu tiên thay vì `RealParameter` trong hầu hết các trường hợp.
* `RealParameter` - xác định tham số dấu phẩy động có ranh giới trên và dưới và không có giới hạn độ chính xác. Hiếm khi được sử dụng vì nó tạo ra một không gian với vô số khả năng.
* `CategoricalParameter` - xác định một tham số với số lượng lựa chọn được xác định trước.
* `BooleanParameter` - Viết tắt của `CategoricalParameter([True, False])` - tuyệt vời cho các tham số "bật".

### Tùy chọn tham số

Có hai tùy chọn tham số có thể giúp bạn nhanh chóng thử nghiệm các ý tưởng khác nhau:

* `optimize` - khi được đặt thành `False`, tham số sẽ không được đưa vào quá trình tối ưu hóa. (Mặc định: Đúng)
* `load` - khi được đặt thành `False`, kết quả của lần chạy hyperopt trước đó (trong `buy_params` và `sell_params` trong chiến lược của bạn hoặc tệp đầu ra JSON) sẽ không được sử dụng làm giá trị bắt đầu cho các hyperopt tiếp theo. Giá trị mặc định được chỉ định trong tham số sẽ được sử dụng thay thế. (Mặc định: Đúng)

!!! Mẹo "Tác động của `load=False` khi kiểm tra lại"
    Xin lưu ý rằng việc đặt tùy chọn `load` thành `False` có nghĩa là việc kiểm tra ngược cũng sẽ sử dụng giá trị mặc định được chỉ định trong tham số và *không phải* giá trị được tìm thấy thông qua quá trình tối ưu hóa quá mức.

!!! Cảnh báo
    Không thể sử dụng các tham số siêu thích hợp trong `populate_indicators` - vì hyperopt không tính toán lại các chỉ báo cho mỗi kỷ nguyên, do đó giá trị bắt đầu sẽ được sử dụng trong trường hợp này.

## Tối ưu hóa tham số chỉ báo

Giả sử bạn có sẵn một chiến lược đơn giản - chiến lược chéo EMA (2 đường trung bình động cắt nhau) - và bạn muốn tìm các thông số lý tưởng cho chiến lược này.
Theo mặc định, chúng tôi giả định mức dừng lỗ là 5% - và mức chốt lời (`minimal_roi`) là 10% - có nghĩa là freqtrade sẽ bán giao dịch sau khi đạt được lợi nhuận 10%.``` python
from pandas import DataFrame
from functools import reduce

import talib.abstract as ta

from freqtrade.strategy import (BooleanParameter, CategoricalParameter, DecimalParameter, 
                                IStrategy, IntParameter)
import freqtrade.vendor.qtpylib.indicators as qtpylib

class MyAwesomeStrategy(IStrategy):
    stoploss = -0.05
    timeframe = '15m'
    minimal_roi = {
        "0":  0.10
    }
    # Define the parameter spaces
    buy_ema_short = IntParameter(3, 50, default=5)
    buy_ema_long = IntParameter(15, 200, default=50)


    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """Generate all indicators used by the strategy"""
        
        # Calculate all ema_short values
        for val in self.buy_ema_short.range:
            dataframe[f'ema_short_{val}'] = ta.EMA(dataframe, timeperiod=val)
        
        # Calculate all ema_long values
        for val in self.buy_ema_long.range:
            dataframe[f'ema_long_{val}'] = ta.EMA(dataframe, timeperiod=val)
        
        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        conditions = []
        conditions.append(qtpylib.crossed_above(
                dataframe[f'ema_short_{self.buy_ema_short.value}'], dataframe[f'ema_long_{self.buy_ema_long.value}']
            ))

        # Check that volume is not 0
        conditions.append(dataframe['volume'] > 0)

        if conditions:
            dataframe.loc[
                reduce(lambda x, y: x & y, conditions),
                'enter_long'] = 1
        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        conditions = []
        conditions.append(qtpylib.crossed_above(
                dataframe[f'ema_long_{self.buy_ema_long.value}'], dataframe[f'ema_short_{self.buy_ema_short.value}']
            ))

        # Check that volume is not 0
        conditions.append(dataframe['volume'] > 0)

        if conditions:
            dataframe.loc[
                reduce(lambda x, y: x & y, conditions),
                'exit_long'] = 1
        return dataframe
```Phá vỡ nó:

Việc sử dụng `self.buy_ema_short.range` sẽ trả về một đối tượng phạm vi chứa tất cả các mục nhập nằm giữa giá trị Thông số thấp và cao.
Trong trường hợp này (`IntParameter(3, 50, default=5)`), vòng lặp sẽ chạy với tất cả các số từ 3 đến 50 (`[3, 4, 5, ... 49, 50]`).
Bằng cách sử dụng điều này trong một vòng lặp, hyperopt sẽ tạo ra 48 cột mới (`['buy_ema_3', 'buy_ema_4', ... , 'buy_ema_50']`).

Sau đó, chính Hyperopt sẽ sử dụng giá trị đã chọn để tạo tín hiệu mua và bán.

Mặc dù chiến lược này rất có thể quá đơn giản để mang lại lợi nhuận ổn định, nhưng nó sẽ là một ví dụ về cách tối ưu hóa các thông số chỉ báo.

!!! Lưu ý
    `self.buy_ema_short.range` sẽ hoạt động khác nhau giữa hyperopt và các chế độ khác. Đối với hyperopt, ví dụ trên có thể tạo ra 48 cột mới, tuy nhiên đối với tất cả các chế độ khác (kiểm tra lại, khô/trực tiếp), nó sẽ chỉ tạo cột cho giá trị đã chọn. Do đó, bạn nên tránh sử dụng cột kết quả có các giá trị rõ ràng (các giá trị khác ngoài `self.buy_ema_short.value`).

!!! Lưu ý
    Thuộc tính `range` cũng có thể được sử dụng với `DecimalParameter` và `CategoricalParameter`. `RealParameter` không cung cấp thuộc tính này do không gian tìm kiếm vô hạn.

??? Gợi ý "Mẹo về hiệu suất"
    Trong quá trình tăng cường thông thường, các chỉ báo được tính toán một lần và cung cấp cho mỗi kỷ nguyên, tăng tuyến tính mức sử dụng RAM như một hệ số tăng số lõi. Vì điều này cũng ảnh hưởng đến hiệu suất nên có hai lựa chọn thay thế để giảm mức sử dụng RAM

    * Di chuyển các phép tính `ema_short` và `ema_long` từ `populate_indicators()` sang `populate_entry_trend()`. Vì `populate_entry_trend()` sẽ được tính toán theo từng kỷ nguyên nên bạn không cần sử dụng chức năng `.range`.
    * hyperopt cung cấp `--analyze-per-epoch` sẽ chuyển việc thực thi `populate_indicators()` sang quy trình epoch, tính toán một giá trị duy nhất cho mỗi tham số trên mỗi epoch thay vì sử dụng chức năng `.range`. Trong trường hợp này, chức năng `.range` sẽ chỉ trả về giá trị thực sự được sử dụng.

    Những lựa chọn thay thế này sẽ giảm mức sử dụng RAM nhưng lại tăng mức sử dụng CPU. Tuy nhiên, quá trình chạy hyperopting của bạn sẽ ít có khả năng thất bại do sự cố Hết bộ nhớ (OOM).

    Cho dù bạn đang sử dụng chức năng `.range` hay các lựa chọn thay thế ở trên, bạn nên cố gắng sử dụng phạm vi không gian càng nhỏ càng tốt vì điều này sẽ cải thiện việc sử dụng CPU/RAM.

## Tối ưu hóa biện pháp bảo vệ

Freqtrade cũng có thể tối ưu hóa các biện pháp bảo vệ. Cách bạn tối ưu hóa các biện pháp bảo vệ là tùy thuộc vào bạn và những điều sau đây chỉ được coi là ví dụ.

Chiến lược sẽ chỉ cần xác định mục nhập "bảo vệ" là thuộc tính trả về danh sách cấu hình bảo vệ.``` python
from pandas import DataFrame
from functools import reduce

import talib.abstract as ta

from freqtrade.strategy import (BooleanParameter, CategoricalParameter, DecimalParameter, 
                                IStrategy, IntParameter)
import freqtrade.vendor.qtpylib.indicators as qtpylib

class MyAwesomeStrategy(IStrategy):
    stoploss = -0.05
    timeframe = '15m'
    # Define the parameter spaces
    cooldown_lookback = IntParameter(2, 48, default=5, space="protection", optimize=True)
    stop_duration = IntParameter(12, 200, default=5, space="protection", optimize=True)
    use_stop_protection = BooleanParameter(default=True, space="protection", optimize=True)


    @property
    def protections(self):
        prot = []

        prot.append({
            "method": "CooldownPeriod",
            "stop_duration_candles": self.cooldown_lookback.value
        })
        if self.use_stop_protection.value:
            prot.append({
                "method": "StoplossGuard",
                "lookback_period_candles": 24 * 3,
                "trade_limit": 4,
                "stop_duration_candles": self.stop_duration.value,
                "only_per_pair": False
            })

        return prot

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # ...
        
```Sau đó bạn có thể chạy hyperopt như sau:
`freqtrade hyperopt --hyperopt-loss SharpeHyperOptLossDaily --strategy MyAwesomeStrategy --bảo vệ không gian`

!!! Lưu ý
    Không gian bảo vệ không phải là một phần của không gian mặc định và chỉ khả dụng với giao diện Parameters Hyperopt, không có với giao diện hyperopt cũ (yêu cầu các tệp hyperopt riêng biệt).
    Freqtrade cũng sẽ tự động thay đổi cờ "--enable-protections" nếu không gian bảo vệ được chọn.

!!! Cảnh báo
    Nếu các biện pháp bảo vệ được xác định là thuộc tính thì các mục từ cấu hình sẽ bị bỏ qua.
    Do đó, không nên xác định các biện pháp bảo vệ trong cấu hình.

### Di chuyển từ thiết lập thuộc tính trước đó

Việc di chuyển từ thiết lập trước đó khá đơn giản và có thể được thực hiện bằng cách chuyển đổi mục nhập bảo vệ thành thuộc tính.
Nói một cách đơn giản, cấu hình sau sẽ được chuyển đổi thành bên dưới.``` python
class MyAwesomeStrategy(IStrategy):
    protections = [
        {
            "method": "CooldownPeriod",
            "stop_duration_candles": 4
        }
    ]
```Kết quả``` python
class MyAwesomeStrategy(IStrategy):
    
    @property
    def protections(self):
        return [
            {
                "method": "CooldownPeriod",
                "stop_duration_candles": 4
            }
        ]
```Sau đó, rõ ràng bạn cũng sẽ thay đổi các mục nhập thú vị tiềm năng thành các tham số để cho phép siêu tối ưu hóa.

### Tối ưu hóa `max_entry_position_ adjustment`

Mặc dù `max_entry_position_ adjustment` không phải là một không gian riêng biệt nhưng nó vẫn có thể được sử dụng trong hyperopt bằng cách sử dụng phương pháp thuộc tính được trình bày ở trên.``` python
from pandas import DataFrame
from functools import reduce

import talib.abstract as ta

from freqtrade.strategy import (BooleanParameter, CategoricalParameter, DecimalParameter, 
                                IStrategy, IntParameter)
import freqtrade.vendor.qtpylib.indicators as qtpylib

class MyAwesomeStrategy(IStrategy):
    stoploss = -0.05
    timeframe = '15m'

    # Define the parameter spaces
    max_epa = CategoricalParameter([-1, 0, 1, 3, 5, 10], default=1, space="buy", optimize=True)

    @property
    def max_entry_position_adjustment(self):
        return self.max_epa.value
        

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # ...
```??? Mẹo "Sử dụng `IntParameter`"
    Bạn cũng có thể sử dụng `IntParameter` cho việc tối ưu hóa này, nhưng bạn phải trả về một số nguyên một cách rõ ràng:``` python
    max_epa = IntParameter(-1, 10, default=1, space="buy", optimize=True)

    @property
    def max_entry_position_adjustment(self):
        return int(self.max_epa.value)
    ```## Hàm mất mát

Mỗi điều chỉnh siêu tham số yêu cầu một mục tiêu. Điều này thường được định nghĩa là hàm mất mát (đôi khi còn được gọi là hàm mục tiêu), hàm này sẽ giảm để có kết quả mong muốn hơn và tăng nếu có kết quả xấu.

Một hàm mất mát phải được chỉ định thông qua đối số `--hyperopt-loss <Class-name>` (hoặc tùy chọn thông qua cấu hình trong khóa `"hyperopt_loss"`).
Lớp này phải nằm trong tệp riêng của nó trong thư mục `user_data/hyperopts/`.

Hiện tại, các hàm mất mát sau được tích hợp sẵn:

* `ShortTradeDurHyperOptLoss` - (chức năng mất tối ưu hóa Freqtrade mặc định) - Chủ yếu dành cho thời gian giao dịch ngắn và tránh thua lỗ.
* `OnlyProfitHyperOptLoss` - chỉ xem xét số tiền lãi.
* `SharpeHyperOptLoss` - Tối ưu hóa Tỷ lệ Sharpe được tính trên lợi nhuận giao dịch so với độ lệch chuẩn.
* `SharpeHyperOptLossDaily` - Tối ưu hóa Tỷ lệ Sharpe được tính trên lợi nhuận giao dịch **hàng ngày** so với độ lệch chuẩn.
* `SortinoHyperOptLoss` - Tối ưu hóa Tỷ lệ Sortino được tính trên lợi nhuận giao dịch liên quan đến **nhược điểm** độ lệch chuẩn.
* `SortinoHyperOptLossDaily` - tối ưu hóa Tỷ lệ Sortino được tính trên lợi nhuận giao dịch **hàng ngày** so với **độ lệch chuẩn**.
* `MaxDrawDownHyperOptLoss` - Tối ưu hóa mức giảm tuyệt đối tối đa.
* `MaxDrawDownRelativeHyperOptLoss` - Tối ưu hóa cả mức giảm tuyệt đối tối đa đồng thời điều chỉnh mức giảm tương đối tối đa.
* `MaxDrawDownPerPairHyperOptLoss` - Tính tỷ lệ lãi/rút vốn trên mỗi cặp và trả về kết quả tệ nhất làm mục tiêu, buộc hyperopt phải tối ưu hóa các tham số cho tất cả các cặp trong danh sách cặp. Bằng cách này, chúng tôi ngăn chặn một hoặc nhiều cặp có kết quả tốt làm tăng số liệu, trong khi các cặp có kết quả kém không được trình bày và do đó không được tối ưu hóa.
* `CalmarHyperOptLoss` - Tối ưu hóa Tỷ lệ Calmar được tính trên lợi nhuận giao dịch liên quan đến mức rút vốn tối đa.
* `ProfitDrawDownHyperOptLoss` - Tối ưu hóa theo mục tiêu Lợi nhuận tối đa & Rút vốn tối thiểu. Biến `DRAWDOWN_MULT` trong tệp hyperoptloss có thể được điều chỉnh để chặt chẽ hơn hoặc linh hoạt hơn cho mục đích rút vốn.
* `MultiMetricHyperOptLoss` - Tối ưu hóa theo một số số liệu chính để đạt được hiệu suất cân bằng. Trọng tâm chính là tối đa hóa Lợi nhuận và giảm thiểu Rút vốn, đồng thời xem xét các số liệu bổ sung như Hệ số lợi nhuận, Tỷ lệ kỳ vọng và Tỷ lệ thắng. Hơn nữa, nó áp dụng hình phạt cho các giai đoạn có số lượng giao dịch thấp, khuyến khích các chiến lược có tần suất giao dịch phù hợp.

Việc tạo hàm mất tùy chỉnh được đề cập trong phần [Advanced Hyperopt](advanced-hyperopt.md) của tài liệu.

## Thực thi Hyperopt

Khi bạn đã cập nhật cấu hình hyperopt của mình, bạn có thể chạy nó.
Vì hyperopt thử rất nhiều kết hợp để tìm ra thông số tốt nhất nên sẽ mất thời gian để có kết quả tốt.

Chúng tôi thực sự khuyên bạn nên sử dụng `screen` hoặc` tmux` để tránh mất kết nối.```bash
freqtrade hyperopt --config config.json --hyperopt-loss <hyperoptlossname> --strategy <strategyname> -e 500 --spaces all
```Tùy chọn `-e` sẽ đặt số lượng đánh giá hyperopt sẽ thực hiện. Vì hyperopt sử dụng tìm kiếm Bayesian nên việc chạy quá nhiều kỷ nguyên cùng một lúc có thể không mang lại kết quả cao hơn. Kinh nghiệm cho thấy kết quả tốt nhất thường không cải thiện nhiều sau 500-1000 kỷ nguyên.  
Tùy chọn `--early-stop` sẽ được đặt sau bao nhiêu kỷ nguyên không có cải tiến mà hyperopt sẽ dừng. Giá trị tốt là 20-30% tổng số kỷ nguyên. Bất kỳ giá trị nào lớn hơn 0 và nhỏ hơn 20, nó sẽ được thay thế bằng 20. Dừng sớm theo mặc định bị tắt (`--early-stop=0`)

Thực hiện nhiều lần chạy (thực thi) với vài 1000 kỷ nguyên và trạng thái ngẫu nhiên khác nhau rất có thể sẽ tạo ra các kết quả khác nhau.

Tùy chọn `--spaces all` xác định rằng tất cả các tham số có thể phải được tối ưu hóa. Các khả năng được liệt kê dưới đây.

!!! Lưu ý
    Hyperopt sẽ lưu trữ kết quả hyperopt cùng với dấu thời gian của thời gian bắt đầu hyperopt.
    Các lệnh đọc (`hyperopt-list`, `hyperopt-show`) có thể sử dụng `--hyperopt-filename <filename>` để đọc và hiển thị các kết quả hyperopt cũ hơn.
    Bạn có thể tìm thấy danh sách tên tệp bằng `ls -l user_data/hyperopt_results/`.

### Thực thi Hyperopt với nguồn dữ liệu lịch sử khác

Nếu bạn muốn tăng cường tham số bằng cách sử dụng tập dữ liệu lịch sử thay thế
bạn có trên đĩa, hãy sử dụng tùy chọn `--datadir PATH`. Theo mặc định, hyperopt sử dụng dữ liệu từ thư mục `user_data/data`.

### Chạy Hyperopt với bộ thử nghiệm nhỏ hơn

Sử dụng đối số `--timerange` để thay đổi số lượng bộ kiểm tra bạn muốn sử dụng.
Ví dụ: để sử dụng dữ liệu của một tháng, hãy chuyển `--timerange 20210101-20210201` (từ tháng 1 năm 2021 - tháng 2 năm 2021) tới lệnh gọi hyperopt.

Lệnh đầy đủ:```bash
freqtrade hyperopt --strategy <strategyname> --timerange 20210101-20210201
```### Chạy Hyperopt với không gian tìm kiếm nhỏ hơn

Sử dụng tùy chọn `--spaces` để giới hạn không gian tìm kiếm được hyperopt sử dụng.
Để Hyperopt tối ưu hóa mọi thứ thường là một không gian tìm kiếm vô cùng hữu ích.
Thông thường, có thể sẽ hợp lý hơn khi bắt đầu bằng cách chỉ tìm kiếm thuật toán nhập ban đầu.
Hoặc có thể bạn chỉ muốn tối ưu hóa mức dừng lỗ hoặc bảng roi cho chiến lược mới tuyệt vời mà bạn có.

Giá trị pháp lý là:

* `all`: tối ưu hóa mọi thứ (bao gồm cả khoảng trắng tùy chỉnh)
* `mua`: chỉ cần tìm kiếm chiến lược mua mới
* `bán`: chỉ cần tìm kiếm chiến lược bán mới
* `enter`: chỉ cần tìm kiếm logic nhập mới
* `exit`: chỉ cần tìm kiếm logic nhập mới
* `roi`: chỉ tối ưu hóa bảng lợi nhuận tối thiểu cho chiến lược của bạn
* `stoploss`: tìm kiếm giá trị stoploss tốt nhất
* `trailing`: tìm kiếm các giá trị dừng cuối tốt nhất
* `giao dịch`: tìm kiếm các giá trị giao dịch mở tối đa tốt nhất
* `bảo vệ`: tìm kiếm các tham số bảo vệ tốt nhất (đọc [phần bảo vệ](#optimizing-protections) để biết cách xác định chính xác các thông số này)
* `mặc định`: `tất cả` ngoại trừ `theo dõi`, `giao dịch` và `bảo vệ`
* `custom_space_name`: mọi khoảng trắng tùy chỉnh được sử dụng bởi bất kỳ tham số nào trong chiến lược của bạn
* danh sách được phân tách bằng dấu cách của bất kỳ giá trị nào ở trên, ví dụ `--spaces roi stoploss`

Không gian tìm kiếm Hyperopt mặc định, được sử dụng khi không có tùy chọn dòng lệnh `--space` được chỉ định, không bao gồm siêu không gian `cuối`. Chúng tôi khuyên bạn nên chạy tối ưu hóa cho siêu không gian `dấu` một cách riêng biệt, khi các thông số tốt nhất cho các siêu không gian khác đã được tìm thấy, xác thực và dán vào chiến lược tùy chỉnh của bạn.

## Hiểu kết quả Hyperopt

Khi Hyperopt hoàn tất, bạn có thể sử dụng kết quả để cập nhật chiến lược của mình.
Cho kết quả sau từ hyperopt:```
Best result:

    44/100:    135 trades. Avg profit  0.57%. Total profit  0.03871918 BTC (0.7722%). Avg duration 180.4 mins. Objective: 1.94367

    # Buy hyperspace params:
    buy_params = {
        'buy_adx': 44,
        'buy_rsi': 29,
        'buy_adx_enabled': False,
        'buy_rsi_enabled': True,
        'buy_trigger': 'bb_lower'
    }
```Bạn nên hiểu kết quả này như sau:

* Trình kích hoạt mua hoạt động tốt nhất là `bb_low`.
* Bạn không nên sử dụng ADX vì `'buy_adx_enabled': False`.
* Bạn nên **cân nhắc** sử dụng chỉ báo RSI (`'buy_rsi_enabled': True`) và giá trị tốt nhất là `29.0` (`'buy_rsi': 29.0`)

### Tự động áp dụng tham số vào chiến lược

Khi sử dụng các tham số Hyperoptable, kết quả của lần chạy hyperopt sẽ được ghi vào tệp json bên cạnh chiến lược của bạn (vì vậy đối với `MyAwesomeStrategy.py`, tệp sẽ là `MyAwesomeStrategy.json`).  
Tệp này cũng được cập nhật khi sử dụng lệnh phụ `hyperopt-show`, trừ khi `--disable-param-export` được cung cấp cho một trong 2 lệnh.


Lớp chiến lược của bạn cũng có thể chứa các kết quả này một cách rõ ràng. Chỉ cần sao chép khối kết quả hyperopt và dán chúng ở cấp lớp, thay thế các tham số cũ (nếu có). Các tham số mới sẽ tự động được tải vào lần tiếp theo chiến lược được thực thi.

Khi đó, việc chuyển toàn bộ kết quả hyperopt sang chiến lược của bạn sẽ như sau:```python
class MyAwesomeStrategy(IStrategy):
    # Buy hyperspace params:
    buy_params = {
        'buy_adx': 44,
        'buy_rsi': 29,
        'buy_adx_enabled': False,
        'buy_rsi_enabled': True,
        'buy_trigger': 'bb_lower'
    }
```!!! Lưu ý
    Các giá trị trong tệp cấu hình sẽ ghi đè các tham số cấp độ tệp tham số - và cả hai sẽ ghi đè các tham số trong chiến lược.
    Do đó, mức độ phổ biến là: config > tệp tham số > chiến lược `*_params` > mặc định tham số

### Hiểu kết quả ROI của Hyperopt

Nếu bạn đang tối ưu hóa ROI (tức là nếu không gian tìm kiếm tối ưu hóa chứa 'tất cả', 'mặc định' hoặc 'roi'), kết quả của bạn sẽ trông như sau và bao gồm bảng ROI:```
Best result:

    44/100:    135 trades. Avg profit  0.57%. Total profit  0.03871918 BTC (0.7722%). Avg duration 180.4 mins. Objective: 1.94367

    # ROI table:
    minimal_roi = {
        0: 0.10674,
        21: 0.09158,
        78: 0.03634,
        118: 0
    }
```Để sử dụng bảng ROI tốt nhất được Hyperopt tìm thấy trong quá trình kiểm tra ngược và cho các giao dịch trực tiếp/chạy thử, hãy sao chép-dán bảng đó làm giá trị của thuộc tính `minimal_roi` trong chiến lược tùy chỉnh của bạn:```
    # Minimal ROI designed for the strategy.
    # This attribute will be overridden if the config file contains "minimal_roi"
    minimal_roi = {
        0: 0.10674,
        21: 0.09158,
        78: 0.03634,
        118: 0
    }
```Như đã nêu trong nhận xét, bạn cũng có thể sử dụng nó làm giá trị của cài đặt `minimal_roi` trong tệp cấu hình.

#### Không gian tìm kiếm ROI mặc định

Nếu bạn đang tối ưu hóa ROI, Freqtrade sẽ tạo siêu không gian tối ưu hóa 'roi' cho bạn -- đó là siêu không gian của các thành phần cho bảng ROI. Theo mặc định, mỗi bảng ROI do Freqtrade tạo bao gồm 4 hàng (bước). Hyperopt triển khai phạm vi thích ứng cho bảng ROI với phạm vi giá trị trong các bước ROI phụ thuộc vào khung thời gian được sử dụng. Theo mặc định, các giá trị thay đổi trong các phạm vi sau (đối với một số khung thời gian được sử dụng nhiều nhất, các giá trị được làm tròn đến 3 chữ số sau dấu thập phân):

| # bước | 1m |               | 5m |             | 1h |               | 1ngày |               |
| ------ | ------ | ------------- | -------- | ----------- | ---------- | ------------- | ------------ | ------------- |
| 1 | 0 | 0,011...0,119 | 0 | 0,03...0,31 | 0 | 0,068...0,711 | 0 | 0.121...1.258 |
| 2 | 2...8 | 0,007...0,042 | 10...40 | 0,02...0,11 | 120...480 | 0,045...0,252 | 2880...11520 | 0,081...0,446 |
| 3 | 4...20 | 0,003...0,015 | 20...100 | 0,01...0,04 | 240...1200 | 0,022...0,091 | 5760...28800 | 0,040...0,162 |
| 4 | 6...44 | 0,0 | 30...220 | 0,0 | 360...2640 | 0,0 | 8640...63360 | 0,0 |

Những phạm vi này là đủ trong hầu hết các trường hợp. Số phút trong các bước (phím chính tả ROI) được chia tỷ lệ tuyến tính tùy thuộc vào khung thời gian được sử dụng. Giá trị ROI trong các bước (giá trị chính xác ROI) được chia tỷ lệ theo logarit tùy thuộc vào khung thời gian được sử dụng.

Nếu bạn có các phương thức `generate_roi_table()` và `roi_space()` trong hyperopt tùy chỉnh của mình, hãy xóa chúng để sử dụng các bảng ROI thích ứng này và không gian siêu tối ưu hóa ROI do Freqtrade tạo theo mặc định.

Ghi đè phương thức `roi_space()` nếu bạn cần các thành phần của bảng ROI thay đổi trong các phạm vi khác. Ghi đè các phương thức `generate_roi_table()` và `roi_space()` và triển khai phương pháp tùy chỉnh của riêng bạn để tạo bảng ROI trong quá trình tối ưu hóa nếu bạn cần cấu trúc khác của bảng ROI hoặc số lượng hàng (bước) khác.

Bạn có thể tìm thấy mẫu cho các phương pháp này trong [phần ghi đè khoảng trắng được xác định trước](advanced-hyperopt.md#overriding-pre-define-spaces).

!!! Lưu ý "Giảm không gian tìm kiếm"
    Để giới hạn không gian tìm kiếm hơn nữa, Số thập phân được giới hạn ở 3 chữ số thập phân (độ chính xác là 0,001). Điều này thường là đủ, mọi giá trị chính xác hơn giá trị này thường sẽ dẫn đến kết quả bị trang bị quá mức. Tuy nhiên, bạn có thể [ghi đè các khoảng trắng được xác định trước](advanced-hyperopt.md#overriding-pre-define-spaces) để thay đổi điều này theo nhu cầu của bạn.

### Hiểu kết quả cắt lỗ của Hyperopt

Nếu bạn đang tối ưu hóa các giá trị điểm dừng (tức là nếu không gian tìm kiếm tối ưu hóa chứa 'tất cả', 'mặc định' hoặc 'điểm dừng'), kết quả của bạn sẽ như sau và bao gồm điểm dừng:```
Best result:

    44/100:    135 trades. Avg profit  0.57%. Total profit  0.03871918 BTC (0.7722%). Avg duration 180.4 mins. Objective: 1.94367

    # Buy hyperspace params:
    buy_params = {
        'buy_adx': 44,
        'buy_rsi': 29,
        'buy_adx_enabled': False,
        'buy_rsi_enabled': True,
        'buy_trigger': 'bb_lower'
    }

    stoploss: -0.27996
```Để sử dụng giá trị dừng lỗ tốt nhất này được Hyperopt tìm thấy trong quá trình kiểm tra ngược và cho các giao dịch trực tiếp/chạy thử, hãy sao chép-dán nó làm giá trị của thuộc tính `stoploss` trong chiến lược tùy chỉnh của bạn:``` python
    # Optimal stoploss designed for the strategy
    # This attribute will be overridden if the config file contains "stoploss"
    stoploss = -0.27996
```Như đã nêu trong nhận xét, bạn cũng có thể sử dụng nó làm giá trị của cài đặt `stoploss` trong tệp cấu hình.

#### Không gian tìm kiếm điểm dừng mặc định

Nếu bạn đang tối ưu hóa các giá trị dừng lỗ, Freqtrade sẽ tạo ra không gian siêu tối ưu hóa 'điểm dừng lỗ' cho bạn. Theo mặc định, các giá trị dừng lỗ trong siêu không gian đó thay đổi trong phạm vi -0,35...-0,02, đủ trong hầu hết các trường hợp.

Nếu bạn có phương thức `stoploss_space()` trong tệp hyperopt tùy chỉnh của mình, hãy xóa nó để sử dụng không gian siêu tối ưu hóa Stoploss do Freqtrade tạo theo mặc định.

Ghi đè phương thức `stoploss_space()` và xác định phạm vi mong muốn trong đó nếu bạn cần các giá trị dừng lỗ thay đổi trong phạm vi khác trong quá trình tối ưu hóa quá mức. Bạn có thể tìm thấy mẫu cho phương pháp này trong [phần ghi đè khoảng trắng được xác định trước](advanced-hyperopt.md#overriding-pre-define-spaces).

!!! Lưu ý "Giảm không gian tìm kiếm"
    Để giới hạn không gian tìm kiếm hơn nữa, Số thập phân được giới hạn ở 3 chữ số thập phân (độ chính xác là 0,001). Điều này thường là đủ, mọi giá trị chính xác hơn giá trị này thường sẽ dẫn đến kết quả bị trang bị quá mức. Tuy nhiên, bạn có thể [ghi đè các khoảng trắng được xác định trước](advanced-hyperopt.md#overriding-pre-define-spaces) để thay đổi điều này theo nhu cầu của bạn.

### Hiểu kết quả Dừng theo dõi Hyperopt

Nếu bạn đang tối ưu hóa các giá trị điểm dừng cuối (tức là nếu không gian tìm kiếm tối ưu hóa chứa 'tất cả' hoặc 'cuối'), kết quả của bạn sẽ trông như sau và bao gồm các tham số điểm dừng cuối:```
Best result:

    45/100:    606 trades. Avg profit  1.04%. Total profit  0.31555614 BTC ( 630.48%). Avg duration 150.3 mins. Objective: -1.10161

    # Trailing stop:
    trailing_stop = True
    trailing_stop_positive = 0.02001
    trailing_stop_positive_offset = 0.06038
    trailing_only_offset_is_reached = True
```Để sử dụng các thông số dừng theo dõi tốt nhất được Hyperopt tìm thấy trong quá trình kiểm tra ngược và cho các giao dịch trực tiếp/chạy thử, hãy sao chép-dán chúng dưới dạng giá trị của các thuộc tính tương ứng trong chiến lược tùy chỉnh của bạn:``` python
    # Trailing stop
    # These attributes will be overridden if the config file contains corresponding values.
    trailing_stop = True
    trailing_stop_positive = 0.02001
    trailing_stop_positive_offset = 0.06038
    trailing_only_offset_is_reached = True
```Như đã nêu trong nhận xét, bạn cũng có thể sử dụng nó làm giá trị của cài đặt tương ứng trong tệp cấu hình.

#### Không gian tìm kiếm dừng theo dõi mặc định

Nếu bạn đang tối ưu hóa các giá trị dừng treo, Freqtrade sẽ tạo siêu không gian tối ưu hóa 'dấu' cho bạn. Theo mặc định, tham số `trailing_stop` luôn được đặt thành True trong siêu không gian đó, giá trị của tham số `trailing_only_offset_is_reached` khác nhau giữa Đúng và Sai, giá trị của tham số `trailing_stop_posit` và `trailing_stop_posit_offset` khác nhau trong phạm vi 0,02...0,35 và 0,01...0,1 tương ứng, đủ trong hầu hết các trường hợp.

Ghi đè phương thức `trailing_space()` và xác định phạm vi mong muốn trong đó nếu bạn cần các giá trị của tham số điểm dừng theo dõi thay đổi trong các phạm vi khác trong quá trình tối ưu hóa quá mức. Bạn có thể tìm thấy mẫu cho phương pháp này trong [phần ghi đè khoảng trắng được xác định trước](advanced-hyperopt.md#overriding-pre-define-spaces).

!!! Lưu ý "Giảm không gian tìm kiếm"
    Để giới hạn không gian tìm kiếm hơn nữa, Số thập phân được giới hạn ở 3 chữ số thập phân (độ chính xác là 0,001). Điều này thường là đủ, mọi giá trị chính xác hơn giá trị này thường sẽ dẫn đến kết quả bị trang bị quá mức. Tuy nhiên, bạn có thể [ghi đè các khoảng trắng được xác định trước](advanced-hyperopt.md#overriding-pre-define-spaces) để thay đổi điều này theo nhu cầu của bạn.

### Kết quả có thể lặp lại

Việc tìm kiếm các tham số tối ưu bắt đầu bằng một vài kết hợp ngẫu nhiên (hiện tại là 30) trong siêu không gian của các tham số, các kỷ nguyên Hyperopt ngẫu nhiên. Các kỷ nguyên ngẫu nhiên này được đánh dấu bằng ký tự dấu hoa thị (`*`) trong cột đầu tiên trong đầu ra Hyperopt.

Trạng thái ban đầu để tạo các giá trị ngẫu nhiên này (trạng thái ngẫu nhiên) được kiểm soát bởi giá trị của tùy chọn dòng lệnh `--random-state`. Bạn có thể đặt nó thành một số giá trị tùy ý theo lựa chọn của bạn để có được kết quả có thể lặp lại.

Nếu bạn chưa đặt giá trị này một cách rõ ràng trong các tùy chọn dòng lệnh, Hyperopt sẽ tạo trạng thái ngẫu nhiên với một số giá trị ngẫu nhiên cho bạn. Giá trị trạng thái ngẫu nhiên cho mỗi lần chạy Hyperopt được hiển thị trong nhật ký, vì vậy bạn có thể sao chép và dán nó vào tùy chọn dòng lệnh `--random-state` để lặp lại tập hợp các kỷ nguyên ngẫu nhiên ban đầu được sử dụng.

Nếu bạn không thay đổi bất cứ điều gì trong các tùy chọn dòng lệnh, cấu hình, khoảng thời gian, các lớp Chiến lược và Hyperopt, dữ liệu lịch sử và Hàm mất - bạn sẽ nhận được các kết quả siêu tối ưu hóa tương tự với cùng một giá trị trạng thái ngẫu nhiên được sử dụng.

## Định dạng đầu ra

Theo mặc định, hyperopt in các kết quả được tô màu -- các kỷ nguyên có lợi nhuận dương được in bằng màu xanh lục. Việc đánh dấu này giúp bạn tìm ra các thời điểm có thể thú vị để phân tích sau này. Các kỷ nguyên có tổng lợi nhuận bằng 0 hoặc có lợi nhuận (lỗ) âm được in bằng màu bình thường. Nếu bạn không cần tô màu kết quả (ví dụ: khi bạn đang chuyển hướng đầu ra hyperopt sang một tệp), bạn có thể tắt tô màu bằng cách chỉ định tùy chọn `--no-color` trong dòng lệnh.

Bạn có thể sử dụng tùy chọn dòng lệnh `--print-all` nếu bạn muốn xem tất cả các kết quả ở đầu ra hyperopt, không chỉ những kết quả tốt nhất. Khi `--print-all` được sử dụng, các kết quả tốt nhất hiện tại cũng được tô màu theo mặc định -- chúng được in theo kiểu đậm (sáng). Tính năng này cũng có thể được tắt bằng tùy chọn dòng lệnh `--no-color`.

!!! Lưu ý "Windows và đầu ra màu"
    Windows vốn không hỗ trợ đầu ra màu nên nó tự động bị tắt. Để có đầu ra màu cho hyperopt chạy trong windows, vui lòng xem xét sử dụng WSL.## Xếp chồng vị trí và vô hiệu hóa các vị trí thị trường tối đa

Trong một số trường hợp, bạn có thể cần chạy Hyperopt (và Backtesting) với đối số `--eps`/`--enable-position-stake` hoặc bạn có thể cần đặt `max_open_trades` thành một số rất cao để vô hiệu hóa giới hạn về số lượng giao dịch mở.

Theo mặc định, hyperopt mô phỏng hoạt động của Freqtrade Live Run/Dry Run, trong đó chỉ có một
giao dịch mở cho mỗi cặp được cho phép. Tổng số giao dịch mở cho tất cả các cặp
cũng bị giới hạn bởi cài đặt `max_open_trades`. Trong quá trình Hyperopt/Backtesting, điều này có thể dẫn đến
các giao dịch tiềm năng bị ẩn (hoặc bị che giấu) bởi các giao dịch đã mở.

Đối số `--eps`/`--enable-position-stacking` cho phép mô phỏng việc mua cùng một cặp nhiều lần.
Sử dụng `--max-open-trades` với số lượng rất cao sẽ vô hiệu hóa giới hạn về số lượng giao dịch mở.

!!! Lưu ý
    Các hoạt động chạy thử/trực tiếp sẽ **KHÔNG** sử dụng xếp chồng vị trí - do đó, cũng hợp lý nếu xác thực chiến lược mà không có điều này vì nó gần với thực tế hơn.

Bạn cũng có thể bật xếp chồng vị trí trong tệp cấu hình bằng cách đặt rõ ràng
`"vị trí_xếp chồng"=true`.

## Lỗi hết bộ nhớ

Vì hyperopt tiêu tốn nhiều bộ nhớ (dữ liệu hoàn chỉnh cần phải có trong bộ nhớ một lần cho mỗi quá trình kiểm tra ngược song song), nên có khả năng bạn gặp phải lỗi "hết bộ nhớ".
Để chống lại những điều này, bạn có nhiều lựa chọn:

* Giảm số lượng cặp.
* Giảm phạm vi thời gian được sử dụng (`--timerange <timerange>`).
* Tránh sử dụng `--timeframe-detail` (điều này tải rất nhiều dữ liệu bổ sung vào bộ nhớ).
* Giảm số lượng tiến trình song song (`-j <n>`).
* Tăng bộ nhớ cho máy của bạn.
* Sử dụng `--analyze-per-epoch` nếu bạn đang sử dụng nhiều tham số có chức năng `.range`.


## Mục tiêu đã được đánh giá tại thời điểm này trước đây.

Nếu bạn thấy `Mục tiêu đã được đánh giá tại thời điểm này trước đây.` - thì đây là dấu hiệu cho thấy dung lượng của bạn đã cạn kiệt hoặc gần như vậy.
Về cơ bản, tất cả các điểm trong không gian của bạn đã bị tấn công (hoặc một điểm cực tiểu cục bộ đã bị tấn công) - và hyperopt không còn tìm thấy các điểm trong không gian đa chiều mà nó chưa thử nữa.
Freqtrade cố gắng giải quyết vấn đề "cực tiểu cục bộ" bằng cách sử dụng các điểm ngẫu nhiên mới trong trường hợp này.

Ví dụ:``` python
buy_ema_short = IntParameter(5, 20, default=10, space="buy", optimize=True)
# This is the only parameter in the buy space
```Không gian `buy_ema_short` có 15 giá trị có thể có (`5, 6, ... 19, 20`). Nếu bây giờ bạn chạy hyperopt cho không gian mua, hyperopt sẽ chỉ có 15 giá trị để thử trước khi hết tùy chọn.
Do đó, các kỷ nguyên của bạn phải được căn chỉnh theo các giá trị có thể - hoặc bạn nên sẵn sàng tạm dừng quá trình chạy nếu nhận thấy nhiều cảnh báo `Mục tiêu đã được đánh giá tại thời điểm này trước đây.`.

## Hiển thị chi tiết kết quả Hyperopt

Sau khi bạn chạy Hyperopt với số lượng kỷ nguyên mong muốn, sau này bạn có thể liệt kê tất cả các kết quả để phân tích, chỉ chọn tốt nhất hoặc có lợi nhuận một lần và hiển thị chi tiết cho bất kỳ kỷ nguyên nào được đánh giá trước đó. Điều này có thể được thực hiện bằng các lệnh phụ `hyperopt-list` và `hyperopt-show`. Việc sử dụng các lệnh phụ này được mô tả trong chương [Utils](utils.md#list-hyperopt-results).

## Xuất thông báo gỡ lỗi từ chiến lược của bạn

Nếu muốn xuất thông báo gỡ lỗi từ chiến lược của mình, bạn có thể sử dụng mô-đun `logging`. Theo mặc định, Freqtrade sẽ xuất tất cả các tin nhắn có mức `INFO` trở lên.``` python
import logging


logger = logging.getLogger(__name__)


class MyAwesomeStrategy(IStrategy):
    ...

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        logger.info("This is a debug message")
        ...

```!!! Lưu ý "sử dụng in"
    Các thông báo được in qua `print()` sẽ không được hiển thị trong đầu ra hyperopt trừ khi tính năng song song bị tắt (`-j 1`). 
    Thay vào đó, nên sử dụng mô-đun `logging`.

## Xác thực kết quả backtesting

Khi chiến lược tối ưu hóa đã được triển khai vào chiến lược của bạn, bạn nên kiểm tra lại chiến lược này để đảm bảo mọi thứ đều hoạt động như mong đợi.

Để đạt được kết quả tương tự (số lượng giao dịch, thời lượng, lợi nhuận, v.v.) như trong Hyperopt, vui lòng sử dụng cùng cấu hình và thông số (khoảng thời gian, khung thời gian, ...) được sử dụng cho hyperopt cho Backtesting.

### Tại sao kết quả backtest của tôi không khớp với kết quả hyperopt của tôi?

Nếu kết quả không khớp, hãy kiểm tra các yếu tố sau:* You may have added parameters to hyperopt in `populate_indicators()` where they will be calculated only once **for all epochs**. If you are, for example, trying to optimise multiple SMA timeperiod values, the hyperoptable timeperiod parameter should be placed in `populate_entry_trend()` which is calculated every epoch. See [Optimizing an indicator parameter](https://www.freqtrade.io/en/stable/hyperopt/#optimizing-an-indicator-parameter).
* Nếu bạn đã tắt tính năng tự động xuất các tham số hyperopt vào tệp tham số JSON, hãy kiểm tra kỹ để đảm bảo rằng bạn đã chuyển tất cả các giá trị hyperopt vào chiến lược của mình một cách chính xác.
* Kiểm tra nhật ký để xác minh tham số nào đang được đặt và giá trị nào đang được sử dụng.
* Đặc biệt quan tâm đến các thông số dừng lỗ, max_open_trades và điểm dừng lỗ cuối, vì chúng thường được đặt trong tệp cấu hình, ghi đè các thay đổi đối với chiến lược. Kiểm tra nhật ký backtest của bạn để đảm bảo rằng không có tham số nào do cấu hình vô tình đặt (như `stoploss`, `max_open_trades` hoặc `trailing_stop`).
* Xác minh rằng bạn không có tệp JSON tham số không mong muốn ghi đè các tham số hoặc cài đặt hyperopt mặc định trong chiến lược của bạn.
* Xác minh rằng mọi biện pháp bảo vệ được bật trong quá trình kiểm tra lại cũng được bật khi tăng cường chọn lọc và ngược lại. Khi sử dụng `--space Protection`, các biện pháp bảo vệ sẽ được kích hoạt tự động cho tính năng siêu tùy chọn.