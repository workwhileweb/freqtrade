<!-- Auto-translated from docs/ by script. Please review technical terms. -->

# Cách sử dụng Telegram

## Thiết lập bot Telegram của bạn

Dưới đây chúng tôi giải thích cách tạo Bot Telegram của bạn và cách nhận
Id người dùng Telegram.

### 1. Tạo bot Telegram của bạnStart a chat with the [Telegram BotFather](https://telegram.me/BotFather)
Gửi tin nhắn `/newbot`.

*Phản hồi của BotFather:*

> Được rồi, một bot mới. Chúng ta sẽ gọi nó như thế nào? Vui lòng chọn tên cho bot của bạn.

Chọn tên công khai cho bot của bạn (ví dụ: `Freqtrade bot`)

*Phản hồi của BotFather:*

> Tốt. Bây giờ hãy chọn tên người dùng cho bot của bạn. Nó phải kết thúc bằng `bot`. Như thế này chẳng hạn: TetrisBot hoặc tetris_bot.

Chọn id tên bot của bạn và gửi nó đến BotFather (ví dụ: "`My_own_freqtrade_bot`")

*Phản hồi của BotFather:*

> Xong! Xin chúc mừng bot mới của bạn. Bạn sẽ tìm thấy nó tại `t.me/yourbots_name_bot`. Bây giờ bạn có thể thêm mô tả, phần giới thiệu và ảnh hồ sơ cho bot của mình, xem /help để biết danh sách các lệnh. Nhân tiện, khi bạn tạo xong bot thú vị của mình, hãy ping bộ phận Hỗ trợ Bot của chúng tôi nếu bạn muốn có tên người dùng tốt hơn cho nó. Chỉ cần đảm bảo bot hoạt động đầy đủ trước khi bạn thực hiện việc này.

> Sử dụng mã thông báo này để truy cập API HTTP: `22222222:APITOKEN`> For a description of the Bot API, see this page: https://core.telegram.org/bots/api Father bot will return you the token (API key)
Sao chép Mã thông báo API (`22222222:APITOKEN` trong ví dụ trên) và tiếp tục sử dụng nó cho tham số cấu hình `token`.

Đừng quên bắt đầu cuộc trò chuyện với bot của bạn bằng cách nhấp vào nút `/BẮT ĐẦU`

### 2. Telegram user_id

#### Nhận id người dùng của bạnTalk to the [userinfobot](https://telegram.me/userinfobot)
Lấy "Id" của bạn, bạn sẽ sử dụng nó cho tham số cấu hình `chat_id`.

#### Sử dụng id nhóm

Để lấy ID nhóm, bạn có thể thêm bot vào nhóm, bắt đầu freqtrade và ra lệnh `/tg_info`.
Điều này sẽ trả lại id nhóm cho bạn mà không cần phải sử dụng một số bot ngẫu nhiên.
Mặc dù "chat_id" vẫn được yêu cầu nhưng không cần đặt thành id nhóm cụ thể này cho lệnh này.

Phản hồi cũng sẽ chứa "topic_id" nếu cần - cả hai đều ở định dạng sẵn sàng để sao chép/dán vào cấu hình của bạn.``` json
 {
    "enabled": true,
    "token": "********",
    "chat_id": "-1001332619709",
    "topic_id": "122"
}
```Đối với cấu hình Freqtrade, bạn có thể sử dụng toàn bộ giá trị (bao gồm `-` ) làm chuỗi:```json
   "chat_id": "-1001332619709"
```!!! Cảnh báo "Sử dụng nhóm telegram"
    Khi sử dụng nhóm điện tín, bạn sẽ cấp cho mọi thành viên trong nhóm điện tín quyền truy cập vào bot freqtrade của bạn và tất cả các lệnh có thể có qua điện tín. Hãy đảm bảo rằng bạn có thể tin tưởng mọi người trong nhóm telegram để tránh những bất ngờ khó chịu.

##### ID chủ đề nhóm

Để sử dụng một chủ đề cụ thể trong một nhóm, bạn có thể sử dụng tham số `topic_id` trong cấu hình. Điều này sẽ cho phép bạn sử dụng bot trong một chủ đề cụ thể trong một nhóm.  
Nếu không có điều này, bot sẽ luôn phản hồi kênh chung trong nhóm nếu chủ đề được bật cho cuộc trò chuyện nhóm.```json
   "chat_id": "-1001332619709",
   "topic_id": "3"
```Tương tự như id nhóm - bạn có thể sử dụng `/tg_info` từ chủ đề/chuỗi để lấy id chủ đề chính xác.

#### Người dùng được ủy quyền

Đối với các nhóm, việc giới hạn người có thể gửi lệnh tới bot có thể hữu ích.

Nếu `"authorized_users": []` hiện diện và trống, thì không người dùng nào được phép điều khiển bot.
Trong ví dụ bên dưới, chỉ người dùng có id "1234567" mới được phép điều khiển bot - tất cả những người dùng khác sẽ chỉ có thể nhận tin nhắn.```json
   "chat_id": "-1001332619709",
   "topic_id": "3",
   "authorized_users": ["1234567"]
```## Kiểm soát tiếng ồn điện tín

Freqtrade cung cấp các phương tiện để kiểm soát mức độ chi tiết của bot điện tín của bạn.
Mỗi cài đặt có các giá trị có thể có sau:

* `on` - Tin nhắn sẽ được gửi và người dùng sẽ được thông báo.
* `im lặng` - Tin nhắn sẽ được gửi, Thông báo sẽ không có âm thanh/rung.
* `off` - Bỏ qua việc gửi tất cả loại tin nhắn.

Cấu hình ví dụ hiển thị các cài đặt khác nhau:``` json
"telegram": {
    "enabled": true,
    "token": "your_telegram_token",
    "chat_id": "your_telegram_chat_id",
    "allow_custom_messages": true,
    "notification_settings": {
        "status": "silent",
        "warning": "on",
        "startup": "off",
        "entry": "silent",
        "entry_fill": "on",
        "entry_cancel": "silent",
        "exit": {
            "roi": "silent",
            "emergency_exit": "on",
            "force_exit": "on",
            "exit_signal": "silent",
            "trailing_stop_loss": "on",
            "stop_loss": "on",
            "stoploss_on_exchange": "on",
            "custom_exit": "silent",  // custom_exit without specifying an exit reason
            "partial_exit": "on",
            // "custom_exit_message": "silent",  // Disable individual custom exit reasons
            "*": "off"  // Disable all other exit reasons
        },
        // "exit": "off",  // Simplistic configuration to disable all exit messages
        "exit_cancel": "on",
        "exit_fill": "off",
        "protection_trigger": "off",
        "protection_trigger_global": "on",
        "strategy_msg": "off",
        "show_candle": "off"
    },
    "reload": true,
    "balance_dust_level": 0.01
},
```* Thông báo `entry` được gửi khi đơn hàng được đặt, trong khi thông báo `entry_fill` được gửi khi đơn hàng được khớp trên sàn giao dịch.  
* Thông báo `exit` được gửi khi đơn hàng được đặt, trong khi thông báo `exit_fill` được gửi khi đơn hàng được khớp trên sàn giao dịch.  
    Thông báo thoát (`exit` và `exit_fill`) có thể được kiểm soát thêm ở cấp độ lý do thoát riêng lẻ, với lý do thoát cụ thể làm khóa. mặc định cho tất cả lý do thoát là `bật` - nhưng có thể được định cấu hình thông qua khóa `*` đặc biệt - sẽ hoạt động như ký tự đại diện cho tất cả lý do thoát không được xác định rõ ràng.
* Thông báo `*_fill` bị tắt theo mặc định và phải được bật một cách rõ ràng.  
* Thông báo `protection_trigger` được gửi khi kích hoạt bảo vệ và thông báo `protection_trigger_global` kích hoạt khi kích hoạt biện pháp bảo vệ toàn cầu.  
* `strategy_msg` - Nhận thông báo từ chiến lược, được gửi qua `self.dp.send_msg()` từ chiến lược [chi tiết thêm](strategy-customization.md#send-notification).  
* `show_candle` - hiển thị giá trị nến như một phần của thông báo vào/ra. Chỉ các giá trị có thể là `"ohlc"` hoặc `"off"`.  
* `balance_dust_level` sẽ xác định những gì lệnh `/balance` coi là "bụi" - Các loại tiền tệ có số dư dưới mức này sẽ được hiển thị.  
* `allow_custom_messages` vô hiệu hóa hoàn toàn các thông báo chiến lược.  
* `tải lại` cho phép bạn tắt các nút tải lại trên các tin nhắn đã chọn.  

## Tạo bàn phím tùy chỉnh (nút tắt lệnh)

Telegram cho phép chúng ta tạo một bàn phím tùy chỉnh với các nút lệnh.
Bàn phím tùy chỉnh mặc định trông như thế này.```python
[
    ["/daily", "/profit", "/balance"], # row 1, 3 commands
    ["/status", "/status table", "/performance"], # row 2, 3 commands
    ["/count", "/start", "/stop", "/help"] # row 3, 4 commands
]
```### Cách sử dụng

Bạn có thể tạo bàn phím của riêng mình trong `config.json`:``` json
"telegram": {
      "enabled": true,
      "token": "your_telegram_token",
      "chat_id": "your_telegram_chat_id",
      "keyboard": [
          ["/daily", "/stats", "/balance", "/profit"],
          ["/status table", "/performance"],
          ["/reload_config", "/count", "/logs"]
      ]
   },
```!!! Lưu ý "Các lệnh được hỗ trợ"
    Chỉ cho phép các lệnh sau. Đối số lệnh không được hỗ trợ!

    `/start`, `/pause`, `/stop`, `/status`, `/status table`, `/trades`, `/profit`, `/performance`, `/daily`, `/stats`, `/count`, `/locks`, `/balance`, `/stopentry`, `/reload_config`, `/show_config`, `/logs`, `/danh sách trắng`, `/danh sách đen`, `/help`, `/version`, `/marketdir`

## Lệnh Telegram

Theo mặc định, bot Telegram hiển thị các lệnh được xác định trước. Một số lệnh
chỉ có sẵn bằng cách gửi chúng đến bot. Bảng dưới đây liệt kê các
mệnh lệnh chính thức. Bạn có thể yêu cầu trợ giúp về `/help` bất cứ lúc nào.

|  Lệnh | Mô tả |
|----------|-------------|
| **Lệnh hệ thống**
| `/bắt đầu` | Bắt đầu giao dịch viên
| `/tạm dừng | /dừng lại | /ngưng mua` | Tạm dừng thương nhân. Xử lý khéo léo các giao dịch đang mở theo quy tắc của họ. Không vào vị trí mới.
| `/dừng` | Dừng giao dịch viên
| `/reload_config` | Tải lại tập tin cấu hình
| `/show_config` | Hiển thị một phần cấu hình hiện tại với các cài đặt liên quan đến hoạt động
| `/log [giới hạn]` | Hiển thị thông điệp tường trình cuối cùng.
| `/giúp` | Hiển thị thông báo trợ giúp
| `/phiên bản` | Hiển thị phiên bản
| **Trạng thái** |
| `/trạng thái` | Liệt kê tất cả các giao dịch mở
| `/trạng thái <trade_id>` | Liệt kê một hoặc nhiều giao dịch cụ thể. Phân tách nhiều <trade_id> bằng một khoảng trống.
| `/bảng trạng thái` | Liệt kê tất cả các giao dịch mở ở định dạng bảng. Lệnh mua đang chờ xử lý được đánh dấu bằng dấu hoa thị (*) Lệnh bán đang chờ xử lý được đánh dấu bằng dấu hoa thị kép (**)
| `/đặt hàng <trade_id>` | Liệt kê các lệnh của một hoặc nhiều giao dịch cụ thể. Phân tách nhiều <trade_id> bằng một khoảng trống.
| `/giao dịch [giới hạn]` | Liệt kê tất cả các giao dịch đã đóng gần đây ở định dạng bảng.
| `/đếm` | Hiển thị số lượng giao dịch được sử dụng và có sẵn
| `/khóa` | Hiển thị các cặp hiện đang bị khóa.
| `/mở khóa <pair hoặc lock_id>` | Tháo khóa cho cặp này (hoặc cho id khóa này).
| `/marketdir [dài | ngắn | thậm chí | không có]` | Cập nhật biến do người dùng quản lý thể hiện hướng thị trường hiện tại. Nếu không có hướng nào được cung cấp, hướng hiện được đặt sẽ được hiển thị.
| `/list_custom_data <trade_id> [key]` | Liệt kê custom_data cho tổ hợp ID Thương mại và Khóa. Nếu không có Khóa nào được cung cấp, nó sẽ liệt kê tất cả các cặp khóa-giá trị được tìm thấy cho ID Thương mại đó.
| **Sửa đổi trạng thái giao dịch** |
| `/forceexit <trade_id> | /fx <tradeid>` | Thoát ngay lập tức giao dịch nhất định (Bỏ qua `minim_roi`).
| `/forceexit tất cả | /fx tất cả` | Thoát ngay lập tức tất cả các giao dịch đang mở (Bỏ qua `minimum_roi`).
| `/fx` | bí danh cho `/forceexit`
| `/forcelong <cặp> [tỷ lệ]` | Mua ngay cặp đã cho. Tỷ giá là tùy chọn và chỉ áp dụng cho các đơn đặt hàng giới hạn. (`force_entry_enable` phải được đặt thành True)
| `/forceshort <cặp> [tỷ lệ]` | Ngay lập tức rút ngắn cặp đã cho. Tỷ giá là tùy chọn và chỉ áp dụng cho các đơn đặt hàng giới hạn. Điều này sẽ chỉ hoạt động trên các thị trường không giao ngay. (`force_entry_enable` phải được đặt thành True)
| `/xóa <trade_id>` | Xóa một giao dịch cụ thể khỏi Cơ sở dữ liệu. Cố gắng đóng các lệnh đang mở. Yêu cầu xử lý thủ công giao dịch này trên sàn giao dịch.
| `/reload_trade <trade_id>` | Tải lại giao dịch từ Exchange. Chỉ hoạt động trực tiếp và có thể giúp khôi phục giao dịch đã được bán thủ công trên sàn giao dịch.
| `/cancel_open_order <trade_id> | /coo <trade_id>` | Hủy một lệnh mở cho một giao dịch.
| **Số liệu** |
| `/lợi nhuận [<n>]` | Hiển thị bản tóm tắt lãi/lỗ của bạn từ các giao dịch đóng và một số thống kê về hiệu suất của bạn trong n ngày qua (tất cả các giao dịch theo mặc định)| `/profit_[dài|ngắn] [<n>]` | Hiển thị bản tóm tắt lãi/lỗ của bạn từ các giao dịch đóng theo một hướng và một số thống kê về hiệu suất của bạn trong n ngày qua (tất cả các giao dịch theo mặc định)
| `/biểu diễn` | Hiển thị hiệu suất của từng giao dịch đã hoàn thành được nhóm theo cặp
| `/cân bằng` | Hiển thị số dư do bot quản lý trên mỗi loại tiền tệ
| `/cân bằng đầy` | Hiển thị số dư tài khoản theo loại tiền tệ
| `/hàng ngày <n>` | Hiển thị lãi hoặc lỗ mỗi ngày, trong n ngày qua (n mặc định là 7)
| `/tuần <n>` | Hiển thị lãi hoặc lỗ mỗi tuần, trong n tuần qua (n mặc định là 8)
| `/tháng <n>` | Hiển thị lãi hoặc lỗ mỗi tháng, trong n tháng qua (n mặc định là 6)
| `/thống kê` | Hiển thị Thắng / thua theo lý do Thoát cũng như Trung bình. thời hạn nắm giữ để mua và bán
| `/thoát` | Hiển thị Thắng / thua theo lý do Thoát cũng như Trung bình. thời hạn nắm giữ để mua và bán
| `/mục` | Hiển thị Thắng / thua theo lý do Thoát cũng như Trung bình. thời hạn nắm giữ để mua và bán
| `/danh sách trắng [đã sắp xếp] [chỉ cơ bản]` | Hiển thị danh sách trắng hiện tại. Tùy chọn hiển thị theo thứ tự bảng chữ cái và/hoặc chỉ với loại tiền cơ bản của mỗi cặp.
| `/danh sách đen [cặp]` | Hiển thị danh sách đen hiện tại hoặc thêm một cặp vào danh sách đen.

## Lệnh Telegram đang hoạt động

Dưới đây là ví dụ về tin nhắn Telegram bạn sẽ nhận được cho mỗi lệnh.

### /bắt đầu

> **Trạng thái:** `đang chạy`

### /tạm dừng | /dừng lại | /ngưng mua

> **Trạng thái:** `đã tạm dừng, từ giờ sẽ không có mục nào nữa. Chạy /start để kích hoạt các mục.`

Ngăn bot mở giao dịch mới bằng cách thay đổi trạng thái thành `tạm dừng`.
Các giao dịch mở sẽ tiếp tục được quản lý theo các quy tắc thông thường của chúng (tín hiệu ROI/thoát lệnh, dừng lỗ, v.v.).
Lưu ý rằng việc điều chỉnh vị thế vẫn hoạt động nhưng chỉ ở phía thoát - nghĩa là khi bot bị `tạm dừng`, nó chỉ có thể giảm quy mô vị thế của các giao dịch đang mở.

Sau đó, hãy cho bot thời gian để đóng các giao dịch đang mở (có thể kiểm tra qua `/bảng trạng thái`).
Khi tất cả các vị trí đã đóng, hãy chạy `/stop` để dừng hoàn toàn bot.

Sử dụng `/start` để đưa bot về trạng thái `đang chạy`, cho phép bot mở các vị trí mới.

!!! Cảnh báo
    Tín hiệu tạm dừng/dừng CHỈ hoạt động khi bot đang chạy và không được duy trì lâu dài, vì vậy việc khởi động lại bot sẽ khiến tín hiệu này được đặt lại.

### /dừng lại

> `Dừng giao dịch ...`
> **Trạng thái:** `đã dừng`

### /trạng thái

Đối với mỗi giao dịch mở, bot sẽ gửi cho bạn thông báo sau.
Thẻ Nhập có thể được cấu hình thông qua Chiến lược.

> **ID giao dịch:** `123` `(kể từ 1 ngày trước)`  
> **Cặp hiện tại:** CVC/BTC  
> **Hướng:** Dài  
> **Đòn bẩy:** 1,0  
> **Số tiền:** `26.64180098`  
> **Nhập thẻ:** Tín hiệu dài tuyệt vời  
> **Tỷ lệ mở:** `0,00007489`  
> **Tỷ giá hiện tại:** `0,00007489`  
> **Lợi nhuận chưa thực hiện:** `12,95%`  
> **Cắt lỗ:** `0,00007389 (-0,02%)`  

###/bảng trạng thái

Trả về trạng thái của tất cả các giao dịch đang mở ở định dạng bảng.```
ID L/S    Pair     Since   Profit
----    --------  -------  --------
  67 L   SC/BTC    1 d      13.33%
 123 S   CVC/BTC   1 h      12.95%
```### /đếm

Trả về số lượng giao dịch đã sử dụng và có sẵn.```
current    max
---------  -----
     2     10
```### /lợi nhuận

Cũng có sẵn dưới dạng `/profit_long` và `/profit_short` để chỉ hiển thị lợi nhuận cho các giao dịch mua hoặc bán.

Trả về bản tóm tắt lãi/lỗ và hiệu suất của bạn.

> **ROI:** Đóng giao dịch  
> ∙ `0,00485701 BTC (2,2%) (15,2 Σ%)`  
> ∙ `62,968 USD`  
> **ROI:** Tất cả giao dịch  
> ∙ `0,00255280 BTC (1,5%) (6,43 Σ%)`  
> ∙ `33,095 EUR`  
>  
> **Tổng số giao dịch:** `138`  
> **Bot đã bắt đầu:** `2022-07-11 18:40:44`  
> **Mở giao dịch đầu tiên:** `3 ngày trước`  
> **Mở giao dịch mới nhất:** `2 phút trước`  
> **Trung bình Thời lượng:** `2:33:45`  
> **Thành tích tốt nhất:** `PAY/BTC: 50,23%`  
> **Khối lượng giao dịch:** `0,5 BTC`  
> **Hệ số lợi nhuận:** `1.04`  
> **Thắng / Thua:** `102 / 36`  
> **Tỷ lệ thắng:** `73,91%`  
> **Kỳ vọng (Tỷ lệ):** `4,87 (1,66)`  
> **Mức rút tối đa:** `9,23% (0,01255 BTC)`  

Lợi nhuận tương đối `1,2%` là lợi nhuận trung bình trên mỗi giao dịch.  
Lợi nhuận tương đối của `15,2 Σ%` được dựa trên vốn ban đầu - vì vậy trong trường hợp này, vốn ban đầu là `0,00485701 * 1,152 = 0,00738 BTC`.  
**Vốn ban đầu(**) được lấy từ cài đặt `available_capital` hoặc được tính bằng cách sử dụng kích thước ví hiện tại - lợi nhuận.  
**Hệ số lợi nhuận** được tính bằng tổng lợi nhuận / tổng lỗ - và sẽ đóng vai trò là thước đo tổng thể cho chiến lược.  
**Kỳ vọng** tương ứng với lợi nhuận trung bình trên mỗi đơn vị tiền tệ gặp rủi ro, tức là tỷ lệ thắng và tỷ lệ rủi ro-lợi nhuận (lợi nhuận trung bình của các giao dịch thắng so với mức lỗ trung bình của các giao dịch thua).  
**Tỷ lệ kỳ vọng** là lãi hoặc lỗ dự kiến ​​của giao dịch tiếp theo dựa trên hiệu suất của tất cả các giao dịch trong quá khứ.  
**Mức rút vốn tối đa** tương ứng với chỉ số kiểm tra ngược `Giảm mức rút tuyệt đối (Tài khoản)` - được tính bằng `(Giảm mức rút tuyệt đối) / (DrawdownHigh + số dư ban đầu)`.  
**Ngày bắt đầu bot** sẽ là ngày khởi động bot lần đầu tiên. Đối với các bot cũ hơn, điều này sẽ mặc định là ngày mở giao dịch đầu tiên.  

### /forceexit <trade_id>

> **BINANCE:** Thoát BTC/LTC với giới hạn `0,01650000 (lợi nhuận: ~-4,07%, -0,00008168)`

!!! Mẹo
    Bạn có thể nhận danh sách tất cả các giao dịch đang mở bằng cách gọi `/forceexit` không có tham số, thao tác này sẽ hiển thị danh sách các nút để thoát giao dịch một cách đơn giản.
    Lệnh này có bí danh là `/fx` - có khả năng tương tự nhưng gõ nhanh hơn trong các tình huống "khẩn cấp".

### /forcelong <cặp> [tỷ lệ] | /forceshort <cặp> [tỷ lệ]

`/forcebuy <pair> [rate]` cũng được hỗ trợ trong thời gian dài nhưng sẽ bị coi là không dùng nữa.

> **BINANCE:** Mua ETH/BTC với giới hạn `0,03400000` (`1,000000 ETH`, `225,290 USD`)

Việc bỏ qua cặp này sẽ mở ra một truy vấn yêu cầu cặp đó giao dịch (dựa trên danh sách trắng hiện tại).
Các giao dịch được tạo thông qua `/forcelong` sẽ có thẻ mua là `force_entry`.

![Ảnh chụp màn hình Telegram buộc mua](assets/telegram_forcebuy.png)

Lưu ý rằng để tính năng này hoạt động, `force_entry_enable` cần được đặt thành true.

[Thêm chi tiết](configuration.md#hiểu-force_entry_enable)

### /hiệu suất

Trả về hiệu suất của từng loại tiền điện tử mà bot đã bán.
> Hiệu suất:  
> 1. `RCN/BTC 0,003 BTC (57,77%) (1)`  
> 2. `TRẢ/BTC 0,0012 BTC (56,91%) (1)`  
> 3. `VIB/BTC 0,0011 BTC (47,07%) (1)`  
> 4. `SALT/BTC 0,0010 BTC (30,24%) (1)`  
> 5. `STORJ/BTC 0,0009 BTC (27,24%) (1)`  
> ...  

Hiệu suất tương đối được tính toán dựa trên tổng mức đầu tư bằng tiền tệ, tổng hợp tất cả các mục nhập đã điền cho loại tiền tệ đó.

### /cân bằng

Trả lại số dư của tất cả loại tiền điện tử mà bạn có trên sàn giao dịch.

> **Tiền tệ:** BTC  
> **Có sẵn:** 3.05890234> **Số dư:** 3.05890234  
> **Đang chờ xử lý:** 0,0  
>
> **Tiền tệ:** CVC  
> **Có sẵn:** 86.64180098  
> **Số dư:** 86.64180098  
> **Đang chờ xử lý:** 0,0  

### /hàng ngày <n>

Theo mặc định `/daily` sẽ trả về 7 ngày cuối cùng. Ví dụ bên dưới nếu cho `/daily 3`:

> **Lợi nhuận hàng ngày trong 3 ngày qua:**```
Day (count)     USDT          USD         Profit %
--------------  ------------  ----------  ----------
2022-06-11 (1)  -0.746 USDT   -0.75 USD   -0.08%
2022-06-10 (0)  0 USDT        0.00 USD    0.00%
2022-06-09 (5)  20 USDT       20.10 USD   5.00%
```### /hàng tuần <n>

Theo mặc định, `/weekly` sẽ trả về 8 tuần trước, bao gồm cả tuần hiện tại. Mỗi tuần bắt đầu
từ thứ Hai. Ví dụ bên dưới nếu cho `/week 3`:

> **Lợi nhuận hàng tuần trong 3 tuần qua (bắt đầu từ Thứ Hai):**```
Monday (count)  Profit BTC      Profit USD   Profit %
-------------  --------------  ------------    ----------
2018-01-03 (5)  0.00224175 BTC  29,142 USD   4.98%
2017-12-27 (1)  0.00033131 BTC   4,307 USD   0.00%
2017-12-20 (4)  0.00269130 BTC  34.986 USD   5.12%
```### /hàng tháng <n>

Theo mặc định `/monthly` sẽ trả về 6 tháng trước, bao gồm cả tháng hiện tại. Ví dụ dưới đây
nếu cho `/tháng 3`:

> **Lợi nhuận hàng tháng trong 3 tháng qua:**```
Month (count)  Profit BTC      Profit USD    Profit %
-------------  --------------  ------------    ----------
2018-01 (20)    0.00224175 BTC  29,142 USD  4.98%
2017-12 (5)    0.00033131 BTC   4,307 USD   0.00%
2017-11 (10)    0.00269130 BTC  34.986 USD  5.10%
```### /danh sách trắng

Hiển thị danh sách trắng hiện tại

> Sử dụng danh sách trắng `StaticPairList` với 22 cặp  
> `IOTA/BTC, NEO/BTC, TRX/BTC, VET/BTC, ADA/BTC, ETC/BTC, NCASH/BTC, DASH/BTC, XRP/BTC, XVG/BTC, EOS/BTC, LTC/BTC, OMG/BTC, BTG/BTC, LSK/BTC, ZEC/BTC, HOT/BTC, IOTX/BTC, XMR/BTC, AST/BTC, XLM/BTC, NANO/BTC`

### /danh sách đen [cặp]

Hiển thị danh sách đen hiện tại.
Nếu Cặp được đặt thì cặp này sẽ được thêm vào danh sách cặp.
Cũng hỗ trợ nhiều cặp, cách nhau bằng dấu cách.  
Sử dụng `/reload_config` để đặt lại danh sách đen.

> Sử dụng blacklist `StaticPairList` với 2 cặp  
>`DODGE/BTC`, `HẤP DẪN/BTC`.  

### /phiên bản

> **Phiên bản:** `0.14.3`

### /marketdir

Nếu hướng thị trường được cung cấp, lệnh sẽ cập nhật biến do người dùng quản lý đại diện cho hướng thị trường hiện tại.
Biến này không được đặt theo bất kỳ hướng thị trường hợp lệ nào khi khởi động bot và phải do người dùng đặt. Ví dụ bên dưới dành cho `/marketdir long`:```
Successfully updated marketdirection from none to long.
```Nếu không có hướng thị trường nào được cung cấp, lệnh sẽ đưa ra hướng thị trường hiện được đặt. Ví dụ bên dưới dành cho `/marketdir`:```
Currently set marketdirection: even
```Bạn có thể sử dụng hướng thị trường trong chiến lược của mình thông qua `self.market_direction`.

!!! Cảnh báo "Bot khởi động lại"
    Xin lưu ý rằng hướng thị trường không được duy trì và sẽ được đặt lại sau khi khởi động lại/tải lại bot.

!!! Nguy hiểm "Backtesting"
    Vì giá trị/biến này dự kiến sẽ được thay đổi thủ công trong giao dịch khô/trực tiếp.
    Các chiến lược sử dụng `market_direction` có thể sẽ không tạo ra kết quả đáng tin cậy và có thể lặp lại (những thay đổi đối với biến này sẽ không được phản ánh để kiểm tra lại). Sử dụng có nguy cơ của riêng bạn.