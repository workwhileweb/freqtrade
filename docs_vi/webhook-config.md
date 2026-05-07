<!-- Auto-translated from docs/ by script. Please review technical terms. -->

#Cách sử dụng Webhook

## Cấu hình

Bật webhook bằng cách thêm phần webhook vào tệp cấu hình của bạn và đặt `webhook.enabled` thành `true`.

Cấu hình mẫu (được thử nghiệm bằng IFTTT).```json
  "webhook": {
        "enabled": true,
        "url": "https://maker.ifttt.com/trigger/<YOUREVENT>/with/key/<YOURKEY>/",
        "entry": {
            "value1": "Buying {pair}",
            "value2": "limit {limit:8f}",
            "value3": "{stake_amount:8f} {stake_currency}"
        },
        "entry_cancel": {
            "value1": "Cancelling Open Buy Order for {pair}",
            "value2": "limit {limit:8f}",
            "value3": "{stake_amount:8f} {stake_currency}"
        },
         "entry_fill": {
            "value1": "Buy Order for {pair} filled",
            "value2": "at {open_rate:8f}",
            "value3": ""
        },
        "exit": {
            "value1": "Exiting {pair}",
            "value2": "limit {limit:8f}",
            "value3": "profit: {profit_amount:8f} {stake_currency} ({profit_ratio})"
        },
        "exit_cancel": {
            "value1": "Cancelling Open Exit Order for {pair}",
            "value2": "limit {limit:8f}",
            "value3": "profit: {profit_amount:8f} {stake_currency} ({profit_ratio})"
        },
        "exit_fill": {
            "value1": "Exit Order for {pair} filled",
            "value2": "at {close_rate:8f}.",
            "value3": ""
        },
        "status": {
            "value1": "Status: {status}",
            "value2": "",
            "value3": ""
        }
    },
```The url in `webhook.url` should point to the correct url for your webhook. If you're using [IFTTT](https://ifttt.com) (as shown in the sample above) please insert your event and key to the url.
Bạn có thể đặt định dạng nội dung POST thành Dữ liệu được mã hóa biểu mẫu (mặc định), Mã hóa JSON hoặc dữ liệu thô. Sử dụng `"format": "form"`, `"format": "json"` hoặc `"format": "raw"` tương ứng. Cấu hình ví dụ để tích hợp Matter Extreme Cloud:```json
  "webhook": {
        "enabled": true,
        "url": "https://<YOURSUBDOMAIN>.cloud.mattermost.com/hooks/<YOURHOOK>",
        "format": "json",
        "status": {
            "text": "Status: {status}"
        }
    },
```Kết quả sẽ là một yêu cầu POST với ví dụ: nội dung `{"text">Trạng thái: đang chạy"}` và tiêu đề `Content-Type: application/json` dẫn đến thông báo `Trạng thái: đang chạy` trong kênh Matter Extreme.

Khi sử dụng cấu hình Mã hóa biểu mẫu hoặc Mã hóa JSON, bạn có thể định cấu hình bất kỳ số lượng giá trị tải trọng nào và cả khóa và giá trị sẽ được xuất ra trong yêu cầu POST. Tuy nhiên, khi sử dụng định dạng dữ liệu thô, bạn chỉ có thể định cấu hình một giá trị và nó **phải** được đặt tên là `"data"`. Trong trường hợp này, khóa dữ liệu sẽ không được xuất ra trong yêu cầu POST mà chỉ có giá trị. Ví dụ:```json
  "webhook": {
        "enabled": true,
        "url": "https://<YOURHOOKURL>",
        "format": "raw",
        "webhookstatus": {
            "data": "Status: {status}"
        }
    },
```Kết quả sẽ là một yêu cầu POST với ví dụ: `Trạng thái: đang chạy` nội dung và tiêu đề `Content-Type: text/plain`.

### Cấu hình Webhook lồng nhau

Một số mục tiêu webhook yêu cầu cấu trúc lồng nhau.
Điều này có thể được thực hiện bằng cách đặt nội dung dưới dạng từ điển hoặc danh sách thay vì trực tiếp dưới dạng văn bản.  

Điều này chỉ được hỗ trợ cho định dạng JSON.```json
"webhook": {
    "enabled": true,
    "url": "https://<yourhookurl>",
    "format": "json",
    "status": {
        "msgtype": "text",
        "text": {
            "content": "Status update: {status}"
        }
    }
}
```Kết quả sẽ là một yêu cầu POST với ví dụ: `{"msgtype:"text","text":{"content">Cập nhật trạng thái: đang chạy"}}` nội dung và tiêu đề `Content-Type: application/json`.

## Cấu hình bổ sung

Tham số `webhook.retries` có thể được đặt cho số lần thử lại tối đa mà yêu cầu webhook sẽ thử nếu không thành công (tức là trạng thái phản hồi HTTP không phải là 200). Theo mặc định, giá trị này được đặt thành `0` và bị tắt. Có thể đặt tham số `webhook.retry_delay` bổ sung để chỉ định thời gian tính bằng giây giữa các lần thử lại. Theo mặc định, giá trị này được đặt thành `0,1` (tức là 100 mili giây). Lưu ý rằng việc tăng số lần thử lại hoặc độ trễ thử lại có thể làm chậm trình giao dịch nếu có vấn đề về kết nối với webhook.
Bạn cũng có thể chỉ định `webhook.timeout` - xác định khoảng thời gian bot sẽ đợi cho đến khi nó giả định máy chủ khác không phản hồi (mặc định là 10 giây).

Cấu hình ví dụ cho lần thử lại:```json
  "webhook": {
        "enabled": true,
        "url": "https://<YOURHOOKURL>",
        "timeout": 10,
        "retries": 3,
        "retry_delay": 0.2,
        "status": {
            "status": "Status: {status}"
        }
    },
```Thông báo tùy chỉnh có thể được gửi đến điểm cuối Webhook thông qua hàm `self.dp.send_msg()` từ trong chiến lược. Để bật tính năng này, hãy đặt tùy chọn `allow_custom_messages` thành `true`:```json
  "webhook": {
        "enabled": true,
        "url": "https://<YOURHOOKURL>",
        "allow_custom_messages": true,
        "strategy_msg": {
            "status": "StrategyMessage: {msg}"
        }
    },
```Tải trọng khác nhau có thể được cấu hình cho các sự kiện khác nhau. Không phải tất cả các trường đều cần thiết nhưng bạn nên định cấu hình ít nhất một trong các lệnh, nếu không webhook sẽ không bao giờ được gọi.

## Các loại tin nhắn Webhook

### Mục nhập / Điền mục nhập

Các trường trong `webhook.entry` và `webhook.entry_fill` được điền khi bot đặt Lệnh mua/ngắn để tăng vị thế hoặc khi lệnh đó được thực hiện tương ứng. Các tham số được điền bằng string.format.
Các thông số có thể là:* `trade_id`
* `exchange`
* `pair`
* `direction`
* `leverage`
* ~~`giới hạn` # Không dùng nữa - không nên sử dụng nữa.~~* `open_rate`
* `amount`
* `open_date`
* `stake_amount`
* `stake_currency`
* `base_currency`
* `quote_currency`
* `fiat_currency`
* `order_type`
* `current_rate`
* `enter_tag`
### Hủy mục nhập

Các trường trong `webhook.entry_cancel` được điền khi bot hủy một lệnh mua/ngắn. Các tham số được điền bằng string.format.
Các thông số có thể là:* `trade_id`
* `exchange`
* `pair`
* `direction`
* `leverage`
* `limit`
* `amount`
* `open_date`
* `stake_amount`
* `stake_currency`
* `base_currency`
* `quote_currency`
* `fiat_currency`
* `order_type`
* `current_rate`
* `enter_tag`
### Thoát / Thoát điền

Các trường trong `webhook.exit` và `webhook.exit_fill` được lấp đầy khi bot đặt lệnh thoát hoặc khi lệnh thoát đó được lấp đầy tương ứng. Các tham số được điền bằng string.format.
Các thông số có thể là:* `trade_id`
* `exchange`
* `pair`
* `direction`
* `leverage`
* `gain`
* `amount`
* `open_rate`
* `close_rate`
* `current_rate`
* `profit_amount`
* `profit_ratio`
* `stake_currency`
* `base_currency`
* `quote_currency`
* `fiat_currency`
* `enter_tag`
* `exit_reason`
* `order_type`
* `open_date`
* `close_date`
* `sub_trade`
* `is_final_exit`
### Thoát và hủy

Các trường trong `webhook.exit_cancel` được điền khi bot hủy lệnh thoát. Các tham số được điền bằng string.format.
Các thông số có thể là:* `trade_id`
* `exchange`
* `pair`
* `direction`
* `leverage`
* `gain`
* `order_rate`
* `amount`
* `open_rate`
* `current_rate`
* `profit_amount`
* `profit_ratio`
* `stake_currency`
* `base_currency`
* `quote_currency`
* `fiat_currency`
* `exit_reason`
* `order_type`
* `open_date`
* `close_date`
### Trạng thái

Các trường trong `webhook.status` được sử dụng cho các thông báo trạng thái thông thường (Đã bắt đầu / Đã dừng / ...). Các tham số được điền bằng string.format.

Giá trị duy nhất có thể có ở đây là `{status}`.

## Bất hòa

Một dạng webhook đặc biệt có sẵn cho Discord.
Bạn có thể cấu hình điều này như sau:```json
"discord": {
    "enabled": true,
    "webhook_url": "https://discord.com/api/webhooks/<Your webhook URL ...>",
    "exit_fill": [
        {"Trade ID": "{trade_id}"},
        {"Exchange": "{exchange}"},
        {"Pair": "{pair}"},
        {"Direction": "{direction}"},
        {"Open rate": "{open_rate}"},
        {"Close rate": "{close_rate}"},
        {"Amount": "{amount}"},
        {"Open date": "{open_date:%Y-%m-%d %H:%M:%S}"},
        {"Close date": "{close_date:%Y-%m-%d %H:%M:%S}"},
        {"Profit": "{profit_amount} {stake_currency}"},
        {"Profitability": "{profit_ratio:.2%}"},
        {"Enter tag": "{enter_tag}"},
        {"Exit Reason": "{exit_reason}"},
        {"Strategy": "{strategy}"},
        {"Timeframe": "{timeframe}"},
    ],
    "entry_fill": [
        {"Trade ID": "{trade_id}"},
        {"Exchange": "{exchange}"},
        {"Pair": "{pair}"},
        {"Direction": "{direction}"},
        {"Open rate": "{open_rate}"},
        {"Amount": "{amount}"},
        {"Open date": "{open_date:%Y-%m-%d %H:%M:%S}"},
        {"Enter tag": "{enter_tag}"},
        {"Strategy": "{strategy} {timeframe}"},
    ]
}
```Ở trên thể hiện mặc định (`exit_fill` và `entry_fill` là tùy chọn và sẽ mặc định theo cấu hình ở trên) - rõ ràng là có thể sửa đổi.
Để tắt một trong hai giá trị mặc định (`entry_fill` / `exit_fill`), bạn có thể gán cho chúng một mảng trống (`exit_fill: []`).

Các trường có sẵn tương ứng với các trường dành cho webhook và được ghi lại trong các phần webhook tương ứng.

Các thông báo sẽ trông như sau theo mặc định.

![discord-notification](assets/discord_notification.png)

Tin nhắn tùy chỉnh có thể được gửi từ chiến lược đến điểm cuối Discord thông qua hàm dataprovider.send_msg(). Để bật tính năng này, hãy đặt tùy chọn `allow_custom_messages` thành `true`:```json
  "discord": {
        "enabled": true,
        "webhook_url": "https://discord.com/api/webhooks/<Your webhook URL ...>",
        "allow_custom_messages": true,
    },
```