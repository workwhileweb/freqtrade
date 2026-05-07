<!-- Auto-translated from docs/ by script. Please review technical terms. -->

## Bảo vệ

Các biện pháp bảo vệ sẽ bảo vệ chiến lược của bạn khỏi các sự kiện và điều kiện thị trường bất ngờ bằng cách tạm thời ngừng giao dịch đối với một cặp hoặc tất cả các cặp.
Tất cả thời gian kết thúc bảo vệ được làm tròn đến nến tiếp theo để tránh các giao dịch mua nội bộ nến đột ngột, bất ngờ.

!!! Mẹo "Mẹo sử dụng"
    Không phải tất cả Biện pháp bảo vệ đều có tác dụng với mọi chiến lược và bạn sẽ cần phải điều chỉnh các thông số cho chiến lược của mình để cải thiện hiệu suất.  

    Mỗi Bảo vệ có thể được cấu hình nhiều lần với các tham số khác nhau, để cho phép các mức bảo vệ khác nhau (ngắn hạn / dài hạn).

!!! Lưu ý "Kiểm tra lại"
    Các biện pháp bảo vệ được hỗ trợ bằng cách kiểm tra ngược và hyperopt, nhưng phải được bật rõ ràng bằng cách sử dụng cờ `--enable-protections`.

### Các biện pháp bảo vệ có sẵn

* [`StoplossGuard`](#stoploss-guard) Dừng giao dịch nếu xảy ra một lượng dừng lỗ nhất định trong một khoảng thời gian nhất định.
* [`MaxDrawdown`](#maxdrawdown) Dừng giao dịch nếu đạt đến mức rút tiền tối đa.
* [`LowProfitPairs`](#low-profit-pairs) Khóa các cặp có lợi nhuận thấp
* [`CooldownPeriod`](#cooldown- Period) Không tham gia giao dịch ngay sau khi bán giao dịch.

### Cài đặt chung cho tất cả các Biện pháp bảo vệ

| Tham số | Mô tả |
| --------- | ---------- |
| `phương pháp` | Tên bảo vệ để sử dụng. <br> **Loại dữ liệu:** Chuỗi, được chọn từ [Các biện pháp bảo vệ có sẵn](#available-protections) |
| `stop_duration_candles` | Nên đặt ổ khóa cho bao nhiêu ngọn nến? <br> **Loại dữ liệu:** Số nguyên dương (tính bằng nến) |
| `dừng_duration` | nên khóa bảo vệ trong bao nhiêu phút. <br>Không thể sử dụng cùng với `stop_duration_candles`. <br> **Datatype:** Float (tính bằng phút) |
| `nhìn lại_thời_nến` | Chỉ các giao dịch hoàn thành trong nến `thời gian nhìn lại' nến` cuối cùng mới được xem xét. Cài đặt này có thể bị một số Biện pháp bảo vệ bỏ qua. <br> **Loại dữ liệu:** Số nguyên dương (tính bằng nến). |
| `thời gian nhìn lại` | Chỉ những giao dịch hoàn thành sau `current_time - lookback_ Period` mới được xem xét. <br>Không thể sử dụng cùng với `lookback_ Period_candles`. <br>Cài đặt này có thể bị một số Biện pháp bảo vệ bỏ qua. <br> **Datatype:** Float (tính bằng phút) |
| `giới hạn giao dịch` | Số lượng giao dịch được yêu cầu tối thiểu (không được tất cả các Biện pháp bảo vệ sử dụng). <br> **Loại dữ liệu:** Số nguyên dương |
| `mở khóa_at` | Thời gian giao dịch sẽ được mở khóa thường xuyên (không được sử dụng bởi tất cả các Biện pháp bảo vệ). <br> **Loại dữ liệu:** chuỗi <br>**Định dạng đầu vào:** "HH:MM" (24 giờ) |

!!! Lưu ý "Thời lượng"
    Khoảng thời gian (`stop_duration*` và `lookback_ Period*` có thể được xác định bằng phút hoặc nến).
    Để linh hoạt hơn khi thử nghiệm các khung thời gian khác nhau, tất cả các ví dụ bên dưới sẽ sử dụng định nghĩa "nến".

#### Bảo vệ dừng lỗ

`StoplossGuard` chọn tất cả các giao dịch trong `lookback_ Period` tính bằng phút (hoặc theo nến khi sử dụng `lookback_ Period_candles`).
Nếu `trade_limit` hoặc nhiều giao dịch dẫn đến dừng lỗ, giao dịch sẽ dừng trong `stop_duration` tính bằng phút (hoặc theo nến khi sử dụng `stop_duration_candles` hoặc cho đến thời gian đã đặt khi sử dụng `unlock_at`).

Điều này áp dụng cho tất cả các cặp, trừ khi `only_per_pair` được đặt thành true, khi đó sẽ chỉ xem xét một cặp mỗi lần.

Tương tự, tính năng bảo vệ này theo mặc định sẽ xem xét tất cả các giao dịch (mua và bán). Đối với các bot tương lai, việc cài đặt `only_per_side` sẽ khiến bot chỉ xem xét một bên và sau đó sẽ chỉ khóa một bên này, chẳng hạn như cho phép tiếp tục bán khống sau một loạt lệnh dừng lỗ dài.`required_profit` sẽ xác định lợi nhuận (hoặc lỗ) tương đối cần thiết để xem xét các điểm dừng lỗ. Thông thường, điều này không nên được đặt và mặc định là 0,0 - có nghĩa là tất cả các lệnh dừng lỗ sẽ kích hoạt một khối.

Ví dụ dưới đây dừng giao dịch cho tất cả các cặp trong 4 nến sau giao dịch cuối cùng nếu bot chạm mức dừng lỗ 4 lần trong 24 nến cuối cùng.``` python
@property
def protections(self):
    return [
        {
            "method": "StoplossGuard",
            "lookback_period_candles": 24,
            "trade_limit": 4,
            "stop_duration_candles": 4,
            "required_profit": 0.0,
            "only_per_pair": False,
            "only_per_side": False
        }
    ]
```!!! Lưu ý
    `StoplossGuard` xem xét tất cả các giao dịch có kết quả `"stop_loss"`, `"stoploss_on_exchange"` và `"trailing_stop_loss"` nếu lợi nhuận thu được là âm.
    `trade_limit` và `lookback_ Period` sẽ cần được điều chỉnh cho phù hợp với chiến lược của bạn.

#### Rút tiền tối đa

Tính năng bảo vệ `MaxDrawdown` đánh giá các giao dịch đã đóng trong `thời gian xem lại` (hoặc `thời gian xem lại` hiện tại).  
Nó hỗ trợ 2 chế độ tính toán:

- `chế độ tính toán: "ratios"` (mặc định): Xấp xỉ kế thừa dựa trên tỷ lệ lợi nhuận tích lũy.
- `chế độ tính toán: "vốn chủ sở hữu"`: Mức rút vốn từ đỉnh đến đáy tiêu chuẩn trên đường cong vốn sở hữu tài khoản, sử dụng số dư ban đầu và lợi nhuận tuyệt đối tích lũy.

Với `chế độ tính toán: "tỷ lệ"`, tỷ lệ rút vốn được lấy từ tỷ lệ lợi nhuận giao dịch tích lũy, không phải từ đường cong vốn chủ sở hữu tài khoản. Điều này được giữ lại để tương thích ngược và có thể khác với mức rút vốn ở cấp tài khoản khi kích thước vị thế thay đổi theo thời gian.

Đối với các thiết lập mới, nên sử dụng `chế độ tính toán: "vốn chủ sở hữu". Chỉ ưu tiên `chế độ tính toán: "tỷ lệ"` khi bạn cố tình dựa vào hành vi cũ, đặc biệt với cấu hình số tiền đặt cược cố định trong đó hành vi dựa trên tỷ lệ dễ lý giải hơn.

Nếu mức giảm được quan sát vượt quá `max_allowed_drawdown`, giao dịch sẽ dừng trong `stop_duration` sau giao dịch cuối cùng - giả sử rằng bot cần một thời gian để thị trường phục hồi.

Mẫu dưới đây ngừng giao dịch cho 12 nến nếu mức giảm tối đa > 20% khi xem xét tất cả các cặp - với giao dịch `trade_limit` tối thiểu - trong 48 nến cuối cùng. Nếu muốn, có thể sử dụng `lookback_ Period` và/hoặc `stop_duration`.``` python
@property
def protections(self):
    return  [
        {
            "method": "MaxDrawdown",
            "calculation_mode": "equity",
            "lookback_period_candles": 48,
            "trade_limit": 20,
            "stop_duration_candles": 12,
            "max_allowed_drawdown": 0.2
        },
    ]
```#### Cặp lợi nhuận thấp

`LowProfitPairs` sử dụng tất cả các giao dịch cho một cặp trong `thời gian xem lại` tính bằng phút (hoặc theo nến khi sử dụng `thời gian xem lại_nến`) để xác định tỷ lệ lợi nhuận tổng thể.
Nếu tỷ lệ đó thấp hơn `required_profit`, cặp đó sẽ bị khóa trong `stop_duration` tính bằng phút (hoặc trong nến khi sử dụng `stop_duration_candles` hoặc cho đến thời gian đã đặt khi sử dụng `unlock_at`).

Đối với các bot tương lai, việc cài đặt `only_per_side` sẽ khiến bot chỉ xem xét một bên và sau đó sẽ chỉ khóa một bên này, chẳng hạn như cho phép tiếp tục bán khống sau một chuỗi thua lỗ kéo dài.

Ví dụ dưới đây sẽ ngừng giao dịch một cặp trong 60 phút nếu cặp đó không có lợi nhuận yêu cầu là 2% (và tối thiểu 2 giao dịch) trong 6 cây nến cuối cùng.``` python
@property
def protections(self):
    return [
        {
            "method": "LowProfitPairs",
            "lookback_period_candles": 6,
            "trade_limit": 2,
            "stop_duration": 60,
            "required_profit": 0.02,
            "only_per_pair": False,
        }
    ]
```#### Thời gian hồi chiêu

`CooldownPeriod` khóa một cặp trong `stop_duration` tính bằng phút (hoặc theo nến khi sử dụng `stop_duration_candles` hoặc cho đến thời gian đã đặt khi sử dụng `unlock_at`) sau khi thoát, tránh việc vào lại cặp này trong `stop_duration` phút.

Ví dụ dưới đây sẽ dừng giao dịch một cặp với 2 nến sau khi đóng giao dịch, cho phép cặp này "hạ nhiệt".``` python
@property
def protections(self):
    return  [
        {
            "method": "CooldownPeriod",
            "stop_duration_candles": 2
        }
    ]
```!!! Lưu ý
    Biện pháp bảo vệ này chỉ áp dụng ở cấp độ cặp và sẽ không bao giờ khóa tất cả các cặp trên toàn cầu.
    Biện pháp bảo vệ này không xem xét `thời gian xem lại` vì nó chỉ xem xét giao dịch mới nhất.

### Ví dụ đầy đủ về Bảo vệ

Tất cả các biện pháp bảo vệ có thể được kết hợp theo ý muốn, cũng với các thông số khác nhau, tạo ra bức tường ngày càng tăng cho các cặp hoạt động kém.
Tất cả các biện pháp bảo vệ được đánh giá theo trình tự chúng được xác định.

Ví dụ dưới đây giả định khung thời gian là 1 giờ:

* Khóa mỗi cặp sau khi bán để lấy thêm 5 nến (`CooldownPeriod`), tạo cơ hội cho các cặp khác được lấp đầy.
* Dừng giao dịch trong 4 giờ (`4 * 1 giờ nến`) nếu 2 ngày qua (`48 * 1 giờ nến`) có 20 giao dịch, gây ra mức giảm tối đa hơn 20%. (`Drawdown tối đa`).
* Dừng giao dịch nếu xuất hiện nhiều hơn 4 điểm dừng cho tất cả các cặp trong giới hạn 1 ngày (`24 * 1 giờ nến`) (`StoplossGuard`).
* Khóa tất cả các cặp có 2 Giao dịch trong vòng 6 giờ qua (`6 * 1 giờ nến`) với tỷ lệ lợi nhuận tổng hợp dưới 0,02 (<2%) (`LowProfitPairs`).
* Khóa tất cả các cặp cho 2 nến có lợi nhuận dưới 0,01 (<1%) trong vòng 24h qua (`24 * 1h nến`), tối thiểu 4 giao dịch.``` python
from freqtrade.strategy import IStrategy

class AwesomeStrategy(IStrategy)
    timeframe = '1h'
    
    @property
    def protections(self):
        return [
            {
                "method": "CooldownPeriod",
                "stop_duration_candles": 5
            },
            {
                "method": "MaxDrawdown",
                "calculation_mode": "equity",
                "lookback_period_candles": 48,
                "trade_limit": 20,
                "stop_duration_candles": 4,
                "max_allowed_drawdown": 0.2
            },
            {
                "method": "StoplossGuard",
                "lookback_period_candles": 24,
                "trade_limit": 4,
                "stop_duration_candles": 2,
                "only_per_pair": False
            },
            {
                "method": "LowProfitPairs",
                "lookback_period_candles": 6,
                "trade_limit": 2,
                "stop_duration_candles": 60,
                "required_profit": 0.02
            },
            {
                "method": "LowProfitPairs",
                "lookback_period_candles": 24,
                "trade_limit": 4,
                "stop_duration_candles": 2,
                "required_profit": 0.01
            }
        ]
    # ...
```