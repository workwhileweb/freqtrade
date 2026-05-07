<!-- Auto-translated from docs/ by script. Please review technical terms. -->

#API REST

## Giao diện thường xuyên

FreqUI hiện có [phần tài liệu](freq-ui.md) riêng - vui lòng tham khảo phần đó để biết tất cả thông tin về FreqUI.

## Cấu hình

Kích hoạt API còn lại bằng cách thêm phần api_server vào cấu hình của bạn và đặt `api_server.enabled` thành `true`.

Cấu hình mẫu:``` json
    "api_server": {
        "enabled": true,
        "listen_ip_address": "127.0.0.1",
        "listen_port": 8080,
        "verbosity": "error",
        "enable_openapi": false,
        "jwt_secret_key": "somethingRandomSomethingRandom123",
        "CORS_origins": [],
        "username": "Freqtrader",
        "password": "SuperSecret1!",
        "ws_token": "sercet_Ws_t0ken"
    },
```!!! Nguy hiểm “Cảnh báo an ninh”
    Theo mặc định, cấu hình chỉ nghe trên localhost (vì vậy không thể truy cập được từ các hệ thống khác). Chúng tôi thực sự khuyên bạn không nên tiết lộ API này trên Internet và chọn một mật khẩu mạnh, duy nhất vì những người khác có khả năng có thể kiểm soát bot của bạn.

??? Lưu ý "Truy cập API/UI trên máy chủ từ xa"
    Nếu đang chạy trên VPS, bạn nên cân nhắc sử dụng đường hầm ssh hoặc thiết lập VPN (openVPN, wireguard) để kết nối với bot của mình.
    Điều này sẽ đảm bảo rằng freqUI không tiếp xúc trực tiếp với internet, điều này không được khuyến khích vì lý do bảo mật (freqUI không hỗ trợ https ngay từ đầu).
    Việc thiết lập các công cụ này không nằm trong hướng dẫn này, tuy nhiên bạn có thể tìm thấy nhiều hướng dẫn hay trên internet.You can then access the API by going to `http://127.0.0.1:8080/api/v1/ping` in a browser to check if the API is running correctly.
Điều này sẽ trả về phản hồi:``` output
{"status":"pong"}
```Tất cả các điểm cuối khác đều trả về thông tin nhạy cảm và yêu cầu xác thực và do đó không khả dụng thông qua trình duyệt web.

### Bảo mật

Để tạo mật khẩu an toàn, tốt nhất hãy sử dụng trình quản lý mật khẩu hoặc sử dụng mã bên dưới.``` python
import secrets
secrets.token_hex()
```!!! Gợi ý "mã thông báo JWT"
    Sử dụng phương pháp tương tự để tạo khóa bí mật JWT (`jwt_secret_key`).

!!! Nguy hiểm "Chọn mật khẩu"
    Hãy đảm bảo chọn mật khẩu thật mạnh và duy nhất để bảo vệ bot của bạn khỏi bị truy cập trái phép.
    Đồng thời thay đổi `jwt_secret_key` thành một cái gì đó ngẫu nhiên (không cần phải nhớ điều này, nhưng nó sẽ được sử dụng để mã hóa phiên của bạn, vì vậy tốt hơn là nó phải là một cái gì đó độc đáo!). Giá trị này cũng phải có 32 ký tự hoặc dài hơn để đảm bảo an toàn.

### Cấu hình với docker

Nếu chạy bot bằng docker, bạn cần cho bot lắng nghe các kết nối đến. Việc bảo mật sau đó được xử lý bởi docker.``` json
    "api_server": {
        "enabled": true,
        "listen_ip_address": "0.0.0.0",
        "listen_port": 8080,
        "username": "Freqtrader",
        "password": "SuperSecret1!",
        //...
    },
```Đảm bảo rằng 2 dòng sau có sẵn trong tệp docker-compose của bạn:```yml
    ports:
      - "127.0.0.1:8080:8080"
```!!! Nguy hiểm “Cảnh báo an ninh”
    Bằng cách sử dụng `"8080:8080"` (hoặc `"0.0.0.0:8080:8080"`) trong ánh xạ cổng docker, API sẽ có sẵn cho mọi người kết nối với máy chủ theo đúng cổng, vì vậy những người khác có thể điều khiển bot của bạn.
    Điều này **có thể** an toàn nếu bạn đang chạy bot trong môi trường an toàn (như mạng gia đình của bạn), nhưng bạn không nên đưa API ra internet.

## API nghỉ ngơi

### Sử dụng API

Chúng tôi khuyên bạn nên sử dụng API bằng cách sử dụng gói `freqtrade-client` được hỗ trợ (cũng có sẵn dưới dạng `scripts/rest_client.py`).

Lệnh này có thể được cài đặt độc lập với mọi bot freqtrade đang chạy bằng cách sử dụng `pip install freqtrade-client`.

Mô-đun này được thiết kế nhẹ và chỉ phụ thuộc vào mô-đun `request` và` python-rapidjson`, bỏ qua tất cả các phụ thuộc nặng nề mà freqtrade cần.``` bash
freqtrade-client <command> [optional parameters]
```Theo mặc định, tập lệnh giả định sử dụng `127.0.0.1` (localhost) và cổng `8080`, tuy nhiên, bạn có thể chỉ định tệp cấu hình để ghi đè hành vi này.

#### Cấu hình máy khách tối giản``` json
{
    "api_server": {
        "enabled": true,
        "listen_ip_address": "0.0.0.0",
        "listen_port": 8080,
        "username": "Freqtrader",
        "password": "SuperSecret1!",
        //...
    }
}
`````` bash
freqtrade-client --config rest_config.json <command> [optional parameters]
```Các lệnh có nhiều đối số có thể yêu cầu đối số từ khóa (để rõ ràng) - có thể được cung cấp như sau:``` bash
freqtrade-client --config rest_config.json forceenter BTC/USDT long enter_tag=GutFeeling
```Phương pháp này sẽ hoạt động với tất cả các đối số - hãy kiểm tra lệnh "show" để biết danh sách các tham số có sẵn.

??? Lưu ý "Sử dụng theo chương trình"
    Bạn có thể sử dụng gói `freqtrade-client` (có thể cài đặt độc lập với freqtrade) trong tập lệnh của riêng bạn để tương tác với API freqtrade.
    để làm như vậy, vui lòng sử dụng như sau:``` python
    from freqtrade_client import FtRestClient
    

    client = FtRestClient(server_url, username, password)

    # Get the status of the bot
    ping = client.ping()
    print(ping)

    # Add pairs to blacklist
    client.blacklist("BTC/USDT", "ETH/USDT")
    # Add pairs to blacklist by supplying a list
    client.blacklist(*listPairs)
    # ... 
    ```Để biết danh sách đầy đủ các lệnh có sẵn, vui lòng tham khảo danh sách bên dưới.

#### Freqtrade client- các lệnh có sẵn

Các lệnh có thể có có thể được liệt kê từ tập lệnh máy khách còn lại bằng lệnh `help`.``` bash
freqtrade-client help
```--8<-- "lệnh/freqtrade-client.md"


### Điểm cuối có sẵn

Nếu bạn muốn gọi API REST theo cách thủ công thông qua một tuyến đường khác, ví dụ: trực tiếp thông qua `curl`, bảng bên dưới hiển thị các tham số và điểm cuối URL có liên quan.All endpoints in the below table need to be prefixed with the base URL of the API, e.g. `http://127.0.0.1:8080/api/v1/` - so the command becomes `http://127.0.0.1:8080/api/v1/<command>`.
|  Điểm cuối | Phương pháp | Mô tả / Thông số |
|----------|---------|--------------------------|
| `/ping` | NHẬN | Lệnh đơn giản kiểm tra mức độ sẵn sàng của API - không yêu cầu xác thực.
| `/bắt đầu` | ĐĂNG | Bắt đầu giao dịch viên.
| `/tạm dừng` | ĐĂNG | Tạm dừng thương nhân. Xử lý khéo léo các giao dịch đang mở theo quy tắc của họ. Không vào vị trí mới.
| `/dừng` | ĐĂNG | Dừng thương nhân.
| `/ngưng mua` | ĐĂNG | Ngăn người giao dịch mở giao dịch mới. Đóng các giao dịch đang mở một cách duyên dáng theo quy tắc của họ.
| `/reload_config` | ĐĂNG | Tải lại tập tin cấu hình.
| `/giao dịch` | NHẬN | Liệt kê các giao dịch cuối cùng. Giới hạn ở 500 giao dịch mỗi cuộc gọi.
| `/trade/<tradeid>` | NHẬN | Nhận giao dịch cụ thể.<br/>*Thông số:*<br/>- `tradeid` (`int`)
| `/trades/<tradeid>` | XÓA | Xóa giao dịch khỏi cơ sở dữ liệu. Cố gắng đóng các lệnh đang mở. Yêu cầu xử lý thủ công giao dịch này trên sàn giao dịch.<br/>*Thông số:*<br/>- `tradeid` (`int`)
| `/trades/<tradeid>/open-order` | XÓA | Hủy lệnh đang mở cho giao dịch này.<br/>*Params:*<br/>- `tradeid` (`int`)
| `/trades/<tradeid>/tải lại` | ĐĂNG | Tải lại giao dịch từ Exchange. Chỉ hoạt động trực tiếp và có thể giúp khôi phục giao dịch đã được bán thủ công trên sàn giao dịch.<br/>*Params:*<br/>- `tradeid` (`int`)
| `/show_config` | NHẬN | Hiển thị một phần cấu hình hiện tại với các cài đặt liên quan đến hoạt động.
| `/log` | NHẬN | Hiển thị thông điệp tường trình cuối cùng.
| `/trạng thái` | NHẬN | Liệt kê tất cả các giao dịch mở.
| `/đếm` | NHẬN | Hiển thị số lượng giao dịch được sử dụng và có sẵn.
| `/mục` | NHẬN | Hiển thị số liệu thống kê lợi nhuận cho mỗi thẻ nhập cho cặp nhất định (hoặc tất cả các cặp nếu không có cặp). Cặp là tùy chọn.<br/>*Thông số:*<br/>- `pair` (`str`)
| `/thoát` | NHẬN | Hiển thị số liệu thống kê lợi nhuận cho từng lý do thoát khỏi cặp đã cho (hoặc tất cả các cặp nếu không có cặp). Cặp là tùy chọn.<br/>*Thông số:*<br/>- `pair` (`str`)
| `/mix_tags` | NHẬN | Hiển thị thống kê lợi nhuận cho từng kết hợp thẻ nhập + lý do thoát cho cặp nhất định (hoặc tất cả các cặp nếu không cung cấp cặp). Cặp là tùy chọn.<br/>*Thông số:*<br/>- `pair` (`str`)
| `/khóa` | NHẬN | Hiển thị các cặp hiện đang bị khóa.
| `/khóa` | ĐĂNG | Khóa một cặp cho đến khi "until". (Cho đến khi được làm tròn đến khung thời gian gần nhất). Bên là tùy chọn và có thể là `dài` hoặc `ngắn` (mặc định là `dài`). Lý do là không bắt buộc.<br/>*Params:*<br/>- `<pair>` (`str`)<br/>- `<until>` (`datetime`)<br/>- `[side]` (`str`)<br/>- `[reason]` (`str`)
| `/locks/<lockid>` | XÓA | Xóa (vô hiệu hóa) khóa theo id.<br/>*Params:*<br/>- `lockid` (`int`)
| `/lợi nhuận` | NHẬN | Hiển thị bản tóm tắt lãi/lỗ của bạn từ các giao dịch đóng và một số số liệu thống kê về hiệu suất của bạn.
| `/forceexit` | ĐĂNG | Thoát ngay lập tức giao dịch nhất định (bỏ qua `roi_tối thiểu`), sử dụng loại lệnh nhất định ("thị trường" hoặc "giới hạn", sử dụng cài đặt cấu hình của bạn nếu không được chỉ định) và số tiền đã chọn (bán toàn bộ nếu không được chỉ định). Nếu `all` được cung cấp dưới dạng `tradeid` thì tất cả các giao dịch hiện đang mở sẽ buộc phải thoát.<br/>*Params:*<br/>- `<tradeid>` (`int` hoặc `str`)<br/>- `<ordertype>` (`str`)<br/>- `[amount]` (`float`)| `/forceenter` | ĐĂNG | Nhập ngay cặp đã cho. Bên là tùy chọn và có thể là `dài` hoặc `ngắn` (mặc định là `dài`). Giá, số tiền đặt cược, thẻ tham gia và đòn bẩy là tùy chọn. Loại lệnh là tùy chọn và là `market` hoặc `long` (mặc định sử dụng giá trị được đặt trong cấu hình). (`force_entry_enable` phải được đặt thành True)<br/>*Params:*<br/>- `<pair>` (`str`)<br/>- `<side>` (`str`)<br/>- `[price]` (`float`)<br/>- `[ordertype]` (`str`)<br/>- `[stakeamount]` (`float`)<br/>- `[entry_tag]` (`str`)<br/>- `[đòn bẩy]` (`float`)
| `/biểu diễn` | NHẬN | Hiển thị hiệu suất của từng giao dịch đã hoàn thành được nhóm theo cặp.
| `/cân bằng` | NHẬN | Hiển thị số dư tài khoản trên mỗi loại tiền tệ.
| `/hàng ngày` | NHẬN | Hiển thị lãi hoặc lỗ mỗi ngày, trong n ngày qua (n mặc định là 7).<br/>*Thông số:*<br/>- `timescale` (`int`)
| `/hàng tuần` | NHẬN | Hiển thị lãi hoặc lỗ mỗi tuần, trong n ngày qua (n mặc định là 4).<br/>*Thông số:*<br/>- `timescale` (`int`)
| `/hàng tháng` | NHẬN | Hiển thị lãi hoặc lỗ mỗi tháng, trong n ngày qua (n mặc định là 3).<br/>*Thông số:*<br/>- `timescale` (`int`)
| `/thống kê` | NHẬN | Hiển thị tóm tắt lý do lãi/lỗ cũng như thời gian nắm giữ trung bình.
| `/danh sách trắng` | NHẬN | Hiển thị danh sách trắng hiện tại.
| `/danh sách đen` | NHẬN | Hiển thị danh sách đen hiện tại.
| `/danh sách đen` | ĐĂNG | Thêm cặp được chỉ định vào danh sách đen.<br/>*Params:*<br/>- `blacklist` (`str`)
| `/danh sách đen` | XÓA | Xóa danh sách các cặp đã chỉ định khỏi danh sách đen.<br/>*Params:*<br/>- `[pair,pair]` (`list[str]`)
| `/cặp_nến` | NHẬN | Trả về khung dữ liệu cho sự kết hợp cặp/khung thời gian trong khi bot đang chạy. **Alpha**
| `/cặp_nến` | ĐĂNG | Trả về khung dữ liệu cho một cặp/khung thời gian kết hợp trong khi bot đang chạy, được lọc theo danh sách các cột được cung cấp để trả về. **Alpha**<br/>*Thông số:*<br/>- `<column_list>` (`list[str]`)
| `/pair_history` | NHẬN | Trả về khung dữ liệu được phân tích trong một khoảng thời gian nhất định, được phân tích theo chiến lược nhất định. **Alpha**
| `/pair_history` | ĐĂNG | Trả về khung dữ liệu được phân tích trong một khoảng thời gian nhất định, được phân tích theo chiến lược nhất định, được lọc theo danh sách các cột được cung cấp để trả về. **Alpha**<br/>*Thông số:*<br/>- `<column_list>` (`list[str]`)
| `/plot_config` | NHẬN | Nhận cấu hình cốt truyện từ chiến lược (hoặc không có gì nếu không được định cấu hình). **Alpha**
| `/chiến lược` | NHẬN | Liệt kê các chiến lược trong thư mục chiến lược. **Alpha**
| `/chiến lược/<chiến lược>` | NHẬN | Nhận nội dung Chiến lược cụ thể theo tên lớp chiến lược. **Alpha**<br/>*Thông số:*<br/>- `<strategy>` (`str`)
| `/available_pairs` | NHẬN | Liệt kê dữ liệu backtest có sẵn. **Alpha**
| `/phiên bản` | NHẬN | Hiển thị phiên bản.
| `/sysinfo` | NHẬN | Hiển thị thông tin về tải hệ thống.
| `/sức khỏe` | NHẬN | Hiển thị tình trạng của bot (vòng lặp bot cuối cùng).

!!! Cảnh báo "trạng thái Alpha"
    Điểm cuối được gắn nhãn *trạng thái Alpha* ở trên có thể thay đổi bất kỳ lúc nào mà không cần thông báo trước.

### Tin nhắn WebSocket

Máy chủ API bao gồm điểm cuối websocket để đăng ký tin nhắn RPC từ Bot freqtrade.
Điều này có thể được sử dụng để sử dụng dữ liệu thời gian thực từ bot của bạn, chẳng hạn như thông báo điền vào/ra, thay đổi danh sách trắng, chỉ báo được điền cho các cặp, v.v.

Điều này cũng được sử dụng để thiết lập [Chế độ nhà sản xuất/người tiêu dùng](producer-consumer.md) trong Freqtrade.Assuming your rest API is set to `127.0.0.1` on port `8080`, the endpoint is available at `http://localhost:8080/api/v1/message/ws`.
Để truy cập điểm cuối websocket, cần phải có `ws_token` làm tham số truy vấn trong URL điểm cuối.

Để tạo `ws_token` an toàn, bạn có thể chạy đoạn mã sau:``` python
>>> import secrets
>>> secrets.token_urlsafe(25)
'hZ-y58LXyX_HZ8O1cJzVyN6ePWrLpNQv4Q'
```Sau đó, bạn sẽ thêm mã thông báo đó vào dưới `ws_token` trong cấu hình `api_server` của mình. Giống như vậy:``` json
"api_server": {
    "enabled": true,
    "listen_ip_address": "127.0.0.1",
    "listen_port": 8080,
    "verbosity": "error",
    "enable_openapi": false,
    "jwt_secret_key": "somethingRandomSomethingRandom123",
    "CORS_origins": [],
    "username": "Freqtrader",
    "password": "SuperSecret1!",
    "ws_token": "hZ-y58LXyX_HZ8O1cJzVyN6ePWrLpNQv4Q" // <-----
},
```You can now connect to the endpoint at `http://localhost:8080/api/v1/message/ws?token=hZ-y58LXyX_HZ8O1cJzVyN6ePWrLpNQv4Q`.
!!! Nguy hiểm "Tái sử dụng mã thông báo mẫu"
    Vui lòng không sử dụng mã thông báo mẫu ở trên. Để đảm bảo bạn an toàn, hãy tạo mã thông báo hoàn toàn mới.

#### Sử dụng WebSocket

Sau khi kết nối với WebSocket, bot sẽ phát các tin nhắn RPC tới bất kỳ ai đã đăng ký chúng. Để đăng ký danh sách tin nhắn, bạn phải gửi yêu cầu JSON thông qua WebSocket như yêu cầu bên dưới. Khóa `data` phải là danh sách các chuỗi loại thông báo.``` json
{
  "type": "subscribe",
  "data": ["whitelist", "analyzed_df"] // A list of string message types
}
```Để biết danh sách các loại thông báo, vui lòng tham khảo enum RPCMessageType trong `freqtrade/enums/rpcmessagetype.py`

Giờ đây, bất cứ khi nào những loại tin nhắn RPC đó được gửi trong bot, bạn sẽ nhận được chúng thông qua WebSocket miễn là kết nối được kích hoạt. Chúng thường có dạng giống như yêu cầu:``` json
{
  "type": "analyzed_df",
  "data": {
      "key": ["NEO/BTC", "5m", "spot"],
      "df": {}, // The dataframe
      "la": "2022-09-08 22:14:41.457786+00:00"
  }
}
```#### Thiết lập proxy ngượcWhen using [Nginx](https://nginx.org/en/docs/), the following configuration is required for WebSockets to work (Note this configuration is incomplete, it's missing some information and can not be used as is):
Vui lòng đảm bảo thay thế `<freqtrade_listen_ip>` (và cổng tiếp theo) bằng IP và Cổng phù hợp với cấu hình/thiết lập của bạn.```
http {
    map $http_upgrade $connection_upgrade {
        default upgrade;
        '' close;
    }

    #...

    server {
        #...

        location / {
            proxy_http_version 1.1;
            proxy_pass http://<freqtrade_listen_ip>:8080;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection $connection_upgrade;
            proxy_set_header Host $host;
        }
    }
}
```Để định cấu hình đúng proxy ngược của bạn (một cách an toàn), vui lòng tham khảo tài liệu của nó về proxy websockets.- **Traefik**: Traefik supports websockets out of the box, see the [documentation](https://doc.traefik.io/traefik/)
- **Caddy**: Caddy v2 supports websockets out of the box, see the [documentation](https://caddyserver.com/docs/v2-upgrade#proxy)
!!! Mẹo "chứng chỉ SSL"
    Bạn có thể sử dụng các công cụ như certbot để thiết lập chứng chỉ ssl nhằm truy cập giao diện người dùng của bot thông qua kết nối được mã hóa bằng cách sử dụng bất kỳ proxy ngược nào ở trên.
    Mặc dù điều này sẽ bảo vệ dữ liệu của bạn trong quá trình truyền tải nhưng chúng tôi khuyên bạn không nên chạy API freqtrade bên ngoài mạng riêng của mình (VPN, đường hầm SSH).

###Giao diện OpenAPI

Để bật giao diện openAPI dựng sẵn (Giao diện người dùng Swagger), hãy chỉ định `"enable_openapi": true` trong cấu hình api_server.This will enable the Swagger UI at the `/docs` endpoint. By default, that's running at <http://localhost:8080/docs> - but it'll depend on your settings.
### Sử dụng API nâng cao bằng mã thông báo JWT

!!! Lưu ý
    Những việc dưới đây phải được thực hiện trong một ứng dụng (ứng dụng khách API Freqtrade REST, tìm nạp thông tin qua API) và không nhằm mục đích sử dụng thường xuyên.

API REST của Freqtrade cũng cung cấp JWT (Mã thông báo web JSON).
Bạn có thể đăng nhập bằng lệnh sau và sau đó sử dụng access_token kết quả.``` bash
> curl -X POST --user Freqtrader http://localhost:8080/api/v1/token/login
{"access_token":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1ODkxMTk2ODEsIm5iZiI6MTU4OTExOTY4MSwianRpIjoiMmEwYmY0NWUtMjhmOS00YTUzLTlmNzItMmM5ZWVlYThkNzc2IiwiZXhwIjoxNTg5MTIwNTgxLCJpZGVudGl0eSI6eyJ1IjoiRnJlcXRyYWRlciJ9LCJmcmVzaCI6ZmFsc2UsInR5cGUiOiJhY2Nlc3MifQ.qt6MAXYIa-l556OM7arBvYJ0SDI9J8bIk3_glDujF5g","refresh_token":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1ODkxMTk2ODEsIm5iZiI6MTU4OTExOTY4MSwianRpIjoiZWQ1ZWI3YjAtYjMwMy00YzAyLTg2N2MtNWViMjIxNWQ2YTMxIiwiZXhwIjoxNTkxNzExNjgxLCJpZGVudGl0eSI6eyJ1IjoiRnJlcXRyYWRlciJ9LCJ0eXBlIjoicmVmcmVzaCJ9.d1AT_jYICyTAjD0fiQAr52rkRqtxCjUGEMwlNuuzgNQ"}

> access_token="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1ODkxMTk2ODEsIm5iZiI6MTU4OTExOTY4MSwianRpIjoiMmEwYmY0NWUtMjhmOS00YTUzLTlmNzItMmM5ZWVlYThkNzc2IiwiZXhwIjoxNTg5MTIwNTgxLCJpZGVudGl0eSI6eyJ1IjoiRnJlcXRyYWRlciJ9LCJmcmVzaCI6ZmFsc2UsInR5cGUiOiJhY2Nlc3MifQ.qt6MAXYIa-l556OM7arBvYJ0SDI9J8bIk3_glDujF5g"
# Use access_token for authentication
> curl -X GET --header "Authorization: Bearer ${access_token}" http://localhost:8080/api/v1/count

```Vì mã thông báo truy cập có thời gian chờ ngắn (15 phút) - nên sử dụng yêu cầu `mã thông báo/làm mới` theo định kỳ để nhận mã thông báo truy cập mới:``` bash
> curl -X POST --header "Authorization: Bearer ${refresh_token}"http://localhost:8080/api/v1/token/refresh
{"access_token":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1ODkxMTk5NzQsIm5iZiI6MTU4OTExOTk3NCwianRpIjoiMDBjNTlhMWUtMjBmYS00ZTk0LTliZjAtNWQwNTg2MTdiZDIyIiwiZXhwIjoxNTg5MTIwODc0LCJpZGVudGl0eSI6eyJ1IjoiRnJlcXRyYWRlciJ9LCJmcmVzaCI6ZmFsc2UsInR5cGUiOiJhY2Nlc3MifQ.1seHlII3WprjjclY6DpRhen0rqdF4j6jbvxIhUFaSbs"}
```--8<-- "bao gồm/cors.md"