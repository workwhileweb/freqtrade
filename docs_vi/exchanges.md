<!-- Auto-translated from docs/ by script. Please review technical terms. -->

# Ghi chú dành riêng cho trao đổi

Trang này kết hợp các vấn đề phổ biến và Thông tin dành riêng cho sàn giao dịch và rất có thể không áp dụng cho các sàn giao dịch khác.

## Tổng quan nhanh về các tính năng trao đổi được hỗ trợ

--8<-- "bao gồm/exchange-features.md"

## Cấu hình trao đổiFreqtrade is based on [CCXT library](https://github.com/ccxt/ccxt) that supports over 100 cryptocurrency
thị trường trao đổi và API giao dịch. Danh sách cập nhật đầy đủ có thể được tìm thấy trong[CCXT repo homepage](https://github.com/ccxt/ccxt/tree/master/python).
Tuy nhiên, bot đã được nhóm phát triển thử nghiệm chỉ với một vài trao đổi.
Bạn có thể tìm thấy danh sách hiện tại trong phần "Trang chủ" của tài liệu này.

Vui lòng kiểm tra các sàn giao dịch khác và gửi phản hồi hoặc PR của bạn để cải thiện bot hoặc xác nhận các sàn giao dịch hoạt động hoàn hảo..

Một số sàn giao dịch yêu cầu cấu hình đặc biệt, bạn có thể tìm thấy cấu hình này bên dưới.

### Cấu hình trao đổi mẫu

Cấu hình trao đổi cho "binance" sẽ như sau:```json
"exchange": {
    "name": "binance",
    "key": "your_exchange_key",
    "secret": "your_exchange_secret",
    "ccxt_config": {},
    "ccxt_async_config": {},
    // ... 
```### Đặt giới hạn tỷ lệ

Thông thường, giới hạn tốc độ do CCXT đặt ra là đáng tin cậy và hoạt động tốt.
Trong trường hợp xảy ra sự cố liên quan đến giới hạn tốc độ (thường là Ngoại lệ DDOS trong nhật ký của bạn), bạn có thể dễ dàng thay đổi cài đặt rateLimit thành các giá trị khác.```json
"exchange": {
    "name": "kraken",
    "key": "your_exchange_key",
    "secret": "your_exchange_secret",
    "ccxt_config": {"enableRateLimit": true},
    "ccxt_async_config": {
        "enableRateLimit": true,
        "rateLimit": 3100
    },
```Cấu hình này cho phép kraken cũng như giới hạn tỷ lệ để tránh bị cấm trao đổi.
`"rateLimit": 3100` xác định thời gian chờ là 3,1 giây giữa mỗi cuộc gọi. Điều này cũng có thể bị vô hiệu hóa hoàn toàn bằng cách đặt `"enableRateLimit"` thành sai.

!!! Lưu ý
    Cài đặt tối ưu để giới hạn tỷ lệ tùy thuộc vào sàn giao dịch và quy mô của danh sách trắng, do đó, thông số lý tưởng sẽ khác nhau tùy theo nhiều cài đặt khác.
    Chúng tôi cố gắng cung cấp các giá trị mặc định hợp lý cho mỗi trao đổi nếu có thể, nếu bạn gặp phải lệnh cấm, vui lòng đảm bảo rằng `"enableRateLimit"` được bật và tăng tham số `"rateLimit"` từng bước.

##Binance

!!! Cảnh báo "Hạn chế vị trí máy chủ và địa lý ip"    Please be aware that Binance restricts API access regarding the server country. The current and non-exhaustive countries blocked are Canada, Malaysia, Netherlands and United States. Please go to [binance terms > b. Eligibility](https://www.binance.com/en/terms) to find up to date list.
Binance hỗ trợ [time_in_force](configuration.md#hiểu-order_time_in_force).

!!! Mẹo "Cắt lỗ trên sàn giao dịch"
    Binance hỗ trợ `stoploss_on_exchange` và sử dụng lệnh `stop-loss-limit`. Nó mang lại những lợi ích to lớn, vì vậy chúng tôi khuyên bạn nên hưởng lợi từ nó bằng cách kích hoạt tính năng dừng lỗ khi trao đổi.
    Về hợp đồng tương lai, Binance hỗ trợ cả lệnh `stop-limit` cũng như `stop-market`. Bạn có thể sử dụng `"giới hạn"` hoặc `"thị trường"` trong cài đặt cấu hình `order_types.stoploss` để quyết định nên sử dụng loại nào.

### Đề xuất danh sách đen của Binance

Đối với Binance, bạn nên thêm `"BNB/<STAKE>"` vào danh sách đen của mình để tránh các vấn đề, trừ khi bạn sẵn sàng duy trì đủ `BNB` bổ sung trong tài khoản hoặc trừ khi bạn sẵn sàng vô hiệu hóa việc sử dụng `BNB` để trả phí.
Tài khoản Binance có thể sử dụng `BNB` để trả phí và nếu giao dịch diễn ra trên `BNB`, các giao dịch tiếp theo có thể tiêu tốn vị thế này và khiến giao dịch BNB ban đầu không thể bán được vì số tiền dự kiến ​​không còn nữa.

Nếu không có đủ `BNB` để trả phí giao dịch thì `BNB` sẽ không trả phí và sẽ không xảy ra việc giảm phí. Freqtrade sẽ không bao giờ mua BNB để trả phí. BNB cần phải được mua và theo dõi thủ công để đạt được mục đích này.

### các trang web của Binance

Binance đã được chia thành 2 và người dùng phải sử dụng ID sàn giao dịch ccxt chính xác cho sàn giao dịch của mình, nếu không thì khóa API sẽ không được nhận dạng.* [binance.com](https://www.binance.com/) - International users. Use exchange id: `binance`.
* [binance.us](https://www.binance.us/) - US based users. Use exchange id: `binanceus`.
### Khóa RSA của Binance

Freqtrade hỗ trợ khóa API RSA binance.

Chúng tôi khuyên bạn nên sử dụng chúng làm biến môi trường.``` bash
export FREQTRADE__EXCHANGE__SECRET="$(cat ./rsa_binance.private)"
```Tuy nhiên, chúng cũng có thể được cấu hình thông qua tệp cấu hình. Vì json không hỗ trợ chuỗi nhiều dòng nên bạn sẽ phải thay thế tất cả các dòng mới bằng `\n` để có tệp json hợp lệ.``` json
// ...
 "key": "<someapikey>",
 "secret": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBABACAFQA<...>s8KX8=\n-----END PRIVATE KEY-----"
// ...
```### Hợp đồng tương lai BinanceBinance has specific (unfortunately complex) [Futures Trading Quantitative Rules](https://www.binance.com/en/support/faq/4f462ebe6ff445d4a170be7d9e897272) which need to be followed, and which prohibit a too low stake-amount (among others) for too many orders.
Vi phạm các quy tắc này sẽ dẫn đến hạn chế giao dịch.

Khi giao dịch trên thị trường Binance Futures, phải sử dụng sổ lệnh vì không có dữ liệu mã giá cho hợp đồng tương lai.``` jsonc
  "entry_pricing": {
      "use_order_book": true,
      "order_book_top": 1,
      "check_depth_of_market": {
          "enabled": false,
          "bids_to_ask_delta": 1
      }
  },
  "exit_pricing": {
      "use_order_book": true,
      "order_book_top": 1
  },
```#### Binance tách biệt cài đặt tương lai

Người dùng cũng sẽ phải đặt "Chế độ vị trí" trong cài đặt tương lai thành "Chế độ một chiều" và "Chế độ tài sản" được đặt thành "Chế độ tài sản đơn".
Các cài đặt này sẽ được kiểm tra khi khởi động và freqtrade sẽ hiển thị lỗi nếu cài đặt này sai.

![Cài đặt hợp đồng tương lai Binance](asset/binance_futures_settings.png)

Freqtrade sẽ không cố gắng thay đổi các cài đặt này.

#### Hợp đồng tương lai BNFCR của Binance

Chế độ BNFCR là một loại chế độ tương lai đặc biệt trên Binance để giải quyết các vấn đề pháp lý ở Châu Âu.  
Để sử dụng hợp đồng tương lai BNFCR, bạn sẽ phải có sự kết hợp cài đặt sau:``` jsonc
{
    // ...
    "trading_mode": "futures",
    "margin_mode": "cross",
    "proxy_coin": "BNFCR",
    "stake_currency": "USDT" // or "USDC"
    // ...
}
```Cài đặt `stake_currency` xác định thị trường mà bot sẽ hoạt động. Lựa chọn này thực sự tùy ý.

Trên sàn giao dịch, bạn sẽ phải sử dụng "Chế độ đa tài sản" - và "Chế độ vị thế được đặt thành "Chế độ một chiều".  
Freqtrade sẽ kiểm tra các cài đặt này khi khởi động nhưng sẽ không cố gắng thay đổi chúng.

## Bingx

BingX hỗ trợ [time_in_force](configuration.md#hiểu-order_time_in_force) với cài đặt "GTC" (tốt cho đến khi bị hủy), "IOC" (ngay lập tức hoặc hủy) và cài đặt "PO" (Chỉ đăng).

!!! Mẹo "Cắt lỗ trên sàn giao dịch"
    Bingx hỗ trợ `stoploss_on_exchange` và có thể sử dụng cả lệnh dừng giới hạn và lệnh dừng thị trường. Nó mang lại những lợi ích to lớn, vì vậy chúng tôi khuyên bạn nên hưởng lợi từ nó bằng cách kích hoạt tính năng dừng lỗ khi trao đổi.

## Kraken

Kraken hỗ trợ [time_in_force](configuration.md#under-order_time_in_force) với cài đặt "GTC" (tốt cho đến khi bị hủy), "IOC" (ngay lập tức hoặc hủy) và cài đặt "PO" (Chỉ đăng).

!!! Mẹo "Cắt lỗ trên sàn giao dịch"
    Kraken hỗ trợ `stoploss_on_exchange` và có thể sử dụng cả lệnh dừng lỗ thị trường và lệnh dừng lỗ-giới hạn. Nó mang lại những lợi ích to lớn, vì vậy chúng tôi khuyên bạn nên tận dụng nó.
    Bạn có thể sử dụng `"giới hạn"` hoặc `"thị trường"` trong cài đặt cấu hình `order_types.stoploss` để quyết định nên sử dụng loại nào.

### Dữ liệu lịch sử của Kraken

API Kraken chỉ cung cấp 720 nến lịch sử, đủ cho các chế độ giao dịch khô và trực tiếp của Freqtrade, nhưng lại là một vấn đề đối với việc kiểm tra lại.
Để tải xuống dữ liệu cho sàn giao dịch Kraken, bắt buộc phải sử dụng `--dl-trades`, nếu không bot sẽ tải đi tải lại 720 cây nến giống nhau và bạn sẽ không có đủ dữ liệu backtest.To speed up downloading, you can download the [trades zip files](https://support.kraken.com/hc/en-us/articles/360047543791-Downloadable-historical-market-data-time-and-sales-) kraken provides.
Chúng thường được cập nhật mỗi quý một lần. Freqtrade dự kiến ​​các tệp này sẽ được đặt trong `user_data/data/kraken/trades_csv`.

Cấu trúc như sau có thể hợp lý nếu sử dụng các tệp gia tăng, với lịch sử "đầy đủ" trong một thư mục và các tệp gia tăng trong các thư mục khác nhau.
Giả định cho chế độ này là dữ liệu được tải xuống và giải nén, giữ nguyên tên tệp.
Nội dung trùng lặp sẽ bị bỏ qua (dựa trên dấu thời gian) - mặc dù giả định là không có khoảng trống trong dữ liệu.

Điều này có nghĩa là nếu lịch sử "đầy đủ" của bạn kết thúc vào Quý 4 năm 2022 - thì cả hai bản cập nhật gia tăng Quý 1 năm 2023 và Quý 2 năm 2023 đều có sẵn.
Không có điều này sẽ dẫn đến dữ liệu không đầy đủ và do đó kết quả không hợp lệ khi sử dụng dữ liệu.```
└── trades_csv
    ├── Kraken_full_history
    │   ├── BCHEUR.csv
    │   └── XBTEUR.csv
    ├── Kraken_Trading_History_Q1_2023
    │   ├── BCHEUR.csv
    │   └── XBTEUR.csv
    └── Kraken_Trading_History_Q2_2023
        ├── BCHEUR.csv
        └── XBTEUR.csv
```Bạn có thể chuyển đổi các tệp này thành tệp freqtrade:``` bash
freqtrade convert-trade-data --exchange kraken --format-from kraken_csv --format-to feather
# Convert trade data to different ohlcv timeframes
freqtrade trades-to-ohlcv -p BTC/EUR BCH/EUR --exchange kraken -t 1m 5m 15m 1h
```Dữ liệu được chuyển đổi cũng giúp có thể tải xuống dữ liệu và sẽ bắt đầu tải xuống sau giao dịch được tải mới nhất.``` bash
freqtrade download-data --exchange kraken --dl-trades -p BTC/EUR BCH/EUR 
```!!! Cảnh báo "Tải dữ liệu từ kraken"
    Việc tải xuống dữ liệu kraken sẽ yêu cầu nhiều bộ nhớ (RAM) hơn đáng kể so với bất kỳ sàn giao dịch nào khác vì dữ liệu giao dịch cần được chuyển đổi thành nến trên máy của bạn.
    Cũng sẽ mất nhiều thời gian vì freqtrade sẽ cần tải xuống mọi giao dịch đã xảy ra trên sàn giao dịch cho sự kết hợp cặp/khoảng thời gian, do đó hãy kiên nhẫn.

!!! Cảnh báo "điều chỉnh giới hạn tỷ lệ"
    Vui lòng lưu ý rằng mục nhập cấu hình rateLimit giữ độ trễ tính bằng mili giây giữa các yêu cầu, KHÔNG phải tốc độ yêu cầu/giây.
    Vì vậy, để giảm thiểu ngoại lệ "Vượt quá giới hạn tỷ lệ" của API Kraken, cấu hình này phải được tăng lên, KHÔNG giảm.

## Hợp đồng tương lai Kraken

Kraken Futures sử dụng id sàn giao dịch `krakenfutures` và hỗ trợ chế độ hợp đồng tương lai biệt lập.```jsonc
"exchange": {
    "name": "krakenfutures",
    "key": "your_exchange_key",
    "secret": "your_exchange_secret"
},
"trading_mode": "futures",
"margin_mode": "isolated",
"stake_currency": "USD"
```!!! Mẹo "Cắt lỗ trên sàn giao dịch"
    Kraken Futures hỗ trợ `stoploss_on_exchange` với cả lệnh dừng `giới hạn` và `thị trường`.
    Sử dụng `order_types.stoploss_price_type` để chọn nguồn giá kích hoạt (`mark`, `last` hoặc `index`).

!!! Lưu ý “Tài sản đảm bảo”
    Kraken Futures được thanh toán bằng USD. Sử dụng USD làm tiền tệ đặt cược của bạn.

!!! Lưu ý "Tài khoản Flex (Đa tài sản thế chấp)"
    Tài khoản linh hoạt Kraken Futures cho phép thế chấp bằng nhiều loại tiền tệ, trong khi giao dịch vẫn được thanh toán bằng USD.
    Freqtrade lấy số dư `USD` từ các trường ký quỹ Kraken, vì vậy hãy đặt `stake_currency` thành `USD`.

## Kucoin

Kucoin yêu cầu một cụm mật khẩu cho mỗi khóa api, do đó bạn sẽ cần thêm khóa này vào cấu hình để phần trao đổi của bạn trông như sau:```json
"exchange": {
    "name": "kucoin",
    "key": "your_exchange_key",
    "secret": "your_exchange_secret",
    "password": "your_exchange_api_key_password",
    // ...
}
```Kucoin hỗ trợ [time_in_force](configuration.md#hiểu-order_time_in_force) với cài đặt "GTC" (tốt cho đến khi bị hủy), "FOK" (toàn bộ hoặc hủy) và "IOC" (ngay lập tức hoặc hủy).

!!! Mẹo "Cắt lỗ trên sàn giao dịch"
    Kucoin hỗ trợ `stoploss_on_exchange` và có thể sử dụng cả lệnh dừng lỗ thị trường và lệnh dừng lỗ-giới hạn. Nó mang lại những lợi ích to lớn, vì vậy chúng tôi khuyên bạn nên tận dụng nó.
    Bạn có thể sử dụng `"giới hạn"` hoặc `"thị trường"` trong cài đặt cấu hình `order_types.stoploss` để quyết định loại lệnh dừng lỗ nào sẽ được sử dụng.

### Danh sách đen Kucoin

Đối với Kucoin, bạn nên thêm `"KCS/<STAKE>"` vào danh sách đen của mình để tránh các vấn đề, trừ khi bạn sẵn sàng duy trì đủ `KCS` bổ sung trên tài khoản hoặc trừ khi bạn sẵn sàng vô hiệu hóa việc sử dụng `KCS` để trả phí.
Tài khoản Kucoin có thể sử dụng `KCS` để trả phí và nếu giao dịch diễn ra trên `KCS`, các giao dịch tiếp theo có thể tiêu tốn vị thế này và khiến giao dịch `KCS` ban đầu không thể bán được vì số tiền dự kiến ​​không còn nữa.

##HTX

!!! Mẹo "Cắt lỗ trên sàn giao dịch"
    HTX hỗ trợ `stoploss_on_exchange` và sử dụng lệnh `stop-limit`. Nó mang lại những lợi ích to lớn, vì vậy chúng tôi khuyên bạn nên hưởng lợi từ nó bằng cách kích hoạt tính năng dừng lỗ khi trao đổi.

## được rồiX

OKX yêu cầu cụm mật khẩu cho mỗi khóa api, do đó bạn sẽ cần thêm khóa này vào cấu hình để phần trao đổi của bạn trông như sau:```json
"exchange": {
    "name": "okx",
    "key": "your_exchange_key",
    "secret": "your_exchange_secret",
    "password": "your_exchange_api_key_password",
    // ...
}
```Nếu bạn đã đăng ký OKX trên máy chủ lưu trữ my.okx.com (OKX EAA)- bạn sẽ cần sử dụng `"myokx"` làm tên trao đổi.
Sử dụng trao đổi sai sẽ dẫn đến lỗi "Lỗi OKX 50119: Khóa API không tồn tại" - vì 2 cái này là các thực thể riêng biệt.

!!! Cảnh báo
    OKX chỉ cung cấp 100 nến cho mỗi lệnh gọi api. Do đó, chiến lược sẽ chỉ có một lượng dữ liệu khá thấp ở chế độ backtesting.

!!! Cảnh báo "Tương lai"
    OKX Futures có khái niệm về "chế độ vị trí" - có thể là "Mua/Bán" hoặc mua/bán (chế độ phòng hộ).
    Freqtrade hỗ trợ cả hai chế độ (chúng tôi khuyên bạn nên sử dụng chế độ Mua/Bán) - nhưng việc thay đổi chế độ giữa giao dịch không được hỗ trợ và sẽ dẫn đến các trường hợp ngoại lệ và không thể thực hiện giao dịch.
    OKX cũng chỉ cung cấp nến MARK trong ~3 tháng qua. Do đó, việc kiểm tra lại các hợp đồng tương lai trước ngày đó sẽ dẫn đến sai lệch nhỏ vì phí cấp vốn không thể được tính toán chính xác nếu không có dữ liệu này.

##Gate.io

!!! Mẹo "Cắt lỗ trên sàn giao dịch"
    Gate.io hỗ trợ `stoploss_on_exchange` và sử dụng lệnh `stop-loss-limit`. Nó mang lại những lợi ích to lớn, vì vậy chúng tôi khuyên bạn nên hưởng lợi từ nó bằng cách kích hoạt tính năng dừng lỗ khi trao đổi.

Gate.io hỗ trợ [time_in_force](configuration.md#hiểu-order_time_in_force) với cài đặt "GTC" (tốt cho đến khi bị hủy) và cài đặt "IOC" (ngay lập tức hoặc hủy).

Gate.io cho phép sử dụng `POINT` để thanh toán phí. Vì đây không phải là loại tiền tệ có thể giao dịch (không có sẵn trên thị trường thông thường), việc tính phí tự động sẽ không thành công (và mặc định có mức phí là 0).
Tham số cấu hình `exchange.unknown_fee_rate` có thể được sử dụng để chỉ định tỷ giá hối đoái giữa Điểm và loại tiền đặt cược. Rõ ràng, việc thay đổi đồng tiền đặt cược cũng sẽ yêu cầu thay đổi giá trị này.

Khóa API cổng yêu cầu các quyền sau đối với loại thị trường bạn muốn giao dịch:

* "Giao dịch giao ngay" _or_ "Hợp đồng tương lai vĩnh viễn" (Đọc và viết) (chọn cả hai hoặc chọn một lựa chọn phù hợp với thị trường bạn muốn giao dịch)
* "Ví" (chỉ đọc)
* "Tài khoản" (chỉ đọc)

Nếu không có các quyền này, bot sẽ không khởi động chính xác và hiển thị các lỗi như "thiếu quyền".

## Bybit

!!! Mẹo "Cắt lỗ trên sàn giao dịch"
    Bybit (chỉ hợp đồng tương lai) hỗ trợ `stoploss_on_exchange` và sử dụng các lệnh `stop-loss-limit`. Nó mang lại những lợi ích to lớn, vì vậy chúng tôi khuyên bạn nên hưởng lợi từ nó bằng cách kích hoạt tính năng dừng lỗ khi trao đổi.
    Về hợp đồng tương lai, Bybit hỗ trợ cả lệnh `stop-limit` cũng như `stop-market`. Bạn có thể sử dụng `"giới hạn"` hoặc `"thị trường"` trong cài đặt cấu hình `order_types.stoploss` để quyết định nên sử dụng loại nào.

Bybit hỗ trợ [time_in_force](configuration.md#under-order_time_in_force) với cài đặt "GTC" (tốt cho đến khi bị hủy), "FOK" (toàn bộ hoặc hủy), "IOC" (ngay lập tức hoặc hủy) và cài đặt "PO" (Chỉ đăng).

!!! Cảnh báo "Tài khoản hợp nhất"
    Freqtrade giả định các tài khoản được dành riêng cho bot.
    Do đó, chúng tôi khuyên bạn nên sử dụng một tài khoản phụ cho mỗi bot. Điều này đặc biệt quan trọng khi sử dụng tài khoản hợp nhất.  
    Các cấu hình khác (nhiều bot trên một tài khoản, giao dịch thủ công không phải bot trên tài khoản bot) không được hỗ trợ và có thể dẫn đến hành vi không mong muốn.

### Hợp đồng tương lai Bybit

Giao dịch tương lai trên bybit được hỗ trợ cho chế độ tương lai biệt lập.

Khi khởi động, freqtrade sẽ đặt chế độ vị thế thành "Chế độ một chiều" cho toàn bộ tài khoản (phụ). Điều này tránh thực hiện lệnh gọi này nhiều lần (làm chậm hoạt động của bot), nhưng có nghĩa là những thay đổi thủ công đối với cài đặt này có thể dẫn đến các ngoại lệ và lỗi.Vì bybit không cung cấp lịch sử tỷ lệ cấp vốn nên tính toán chạy thử cũng được sử dụng cho các giao dịch trực tiếp.

Khóa API để giao dịch hợp đồng tương lai trực tiếp phải có các quyền sau:

* Đọc-ghi
* Hợp đồng - Đơn đặt hàng
* Hợp đồng - Vị thế

Chúng tôi thực sự khuyên bạn nên giới hạn tất cả các khóa API ở IP mà bạn sẽ sử dụng nó.

### Chế độ demo BybitBybit has a [demo mode](https://learn.bybit.com/en/bybit-guide/how-to-use-bybit-demo-trading) - which can be activated by setting `exchange.demo_trading` to `true` in the configuration.
Bybit sử dụng thị trường trực tiếp để mô phỏng các giao dịch của bạn (không có tác động đến thị trường) - làm cho nó hoạt động rất giống với chế độ chạy thử của freqtrade.  

Bạn sẽ cần sử dụng các khóa API riêng biệt để giao dịch demo. Bạn có thể tạo khóa này trên trang demo của bybit.

Chế độ demo không tương thích với chế độ chạy khô.

##Bitmart

Bitmart yêu cầu Bản ghi nhớ khóa API (tên bạn đặt cho khóa API) đi cùng với khóa trao đổi và bí mật.
Do đó, cần phải vượt qua UID.```json
"exchange": {
    "name": "bitmart",
    "uid": "your_bitmart_api_key_memo",
    "secret": "your_exchange_secret",
    "password": "your_exchange_api_key_password",
    // ...
}
```!!! Cảnh báo "Xác minh cần thiết"
    Bitmart yêu cầu Xác minh Lvl2 để giao dịch thành công trên thị trường giao ngay thông qua API - mặc dù giao dịch qua UI chỉ hoạt động tốt chỉ với xác minh Lvl1.

## Bitget

Bitget yêu cầu cụm mật khẩu cho mỗi khóa api, do đó bạn sẽ cần thêm khóa này vào cấu hình để phần trao đổi của bạn trông như sau:```json
"exchange": {
    "name": "bitget",
    "key": "your_exchange_key",
    "secret": "your_exchange_secret",
    "password": "your_exchange_api_key_password",
    // ...
}
```Bitget hỗ trợ [time_in_force](configuration.md#under-order_time_in_force) với cài đặt "GTC" (tốt cho đến khi bị hủy), "FOK" (toàn bộ hoặc hủy), "IOC" (ngay lập tức hoặc hủy) và cài đặt "PO" (Chỉ đăng).

!!! Mẹo "Cắt lỗ trên sàn giao dịch"
    Bitget hỗ trợ `stoploss_on_exchange` và có thể sử dụng cả lệnh dừng lỗ thị trường và lệnh dừng lỗ-giới hạn. Nó mang lại những lợi ích to lớn, vì vậy chúng tôi khuyên bạn nên tận dụng nó.
    Bạn có thể sử dụng `"giới hạn"` hoặc `"thị trường"` trong cài đặt cấu hình `order_types.stoploss` để quyết định loại lệnh dừng lỗ nào sẽ được sử dụng.

### Hợp đồng tương lai Bitget

Giao dịch tương lai trên bitget được hỗ trợ cho chế độ tương lai biệt lập.

Khi khởi động, freqtrade sẽ đặt chế độ vị thế thành "Chế độ một chiều" cho toàn bộ tài khoản (phụ). Điều này tránh thực hiện lệnh gọi này nhiều lần (làm chậm hoạt động của bot), nhưng có nghĩa là những thay đổi thủ công đối với cài đặt này có thể dẫn đến các ngoại lệ và lỗi.

## Siêu thanh khoản

!!! Mẹo "Cắt lỗ trên sàn giao dịch"
    Hyperliquid hỗ trợ `stoploss_on_exchange` và sử dụng các lệnh `stop-loss-limit`. Nó mang lại những lợi ích to lớn, vì vậy chúng tôi khuyên bạn nên tận dụng nó.

!!! Cảnh báo "Tài khoản hợp nhất"
    Các tài khoản hợp nhất siêu thanh khoản được hỗ trợ - mặc dù điều này phụ thuộc vào giả định của freqtrade về việc "sở hữu" tài khoản và là tài khoản duy nhất giao dịch trên tài khoản đó (trong trường hợp này, được mở rộng cho cả hợp đồng giao ngay và hợp đồng tương lai).
    Do đó, chúng tôi khuyên bạn nên sử dụng tài khoản phụ nếu có thể và tránh giao dịch thủ công trên cùng một tài khoản trong khi bot đang chạy.
    Freqtrade sẽ cố gắng phát hiện loại tài khoản khi khởi động - việc thay đổi loại tài khoản khi đang giao dịch không được hỗ trợ và có thể dẫn đến các ngoại lệ và lỗi.

Siêu thanh khoản là một sàn giao dịch phi tập trung (DEX). Sàn giao dịch phi tập trung hoạt động hơi khác một chút so với sàn giao dịch thông thường. Thay vì xác thực lệnh gọi API riêng tư bằng khóa API, lệnh gọi API riêng tư cần được ký bằng khóa riêng của ví của bạn (Chúng tôi khuyên bạn nên sử dụng Ví api cho việc này, được tạo trên Hyperliquid hoặc trong ví bạn chọn).
Điều này cần phải được cấu hình như thế này:```json
"exchange": {
    "name": "hyperliquid",
    "walletAddress": "your_eth_wallet_address",  // This should NOT be your API Wallet Address!
    "privateKey": "your_api_private_key",
    // ...
}
```* địa chỉ ví ở định dạng hex: `0x<40 ký tự hex>` - Có thể dễ dàng sao chép từ ví của bạn - và phải là địa chỉ ví chính của bạn, không phải Địa chỉ ví API của bạn.
* khóa riêng ở định dạng hex: `0x<64 ký tự hex>` - Sử dụng khóa mà Ví API hiển thị khi tạo.Hyperliquid handles deposits and withdrawals on the Arbitrum One chain, a Layer 2 scaling solution built on top of Ethereum. Hyperliquid uses USDC as quote / collateral. The process of depositing USDC on Hyperliquid requires a couple of steps, see [how to start trading](https://hyperliquid.gitbook.io/hyperliquid-docs/onboarding/how-to-start-trading) for details on what steps are needed.
!!! Lưu ý "Ghi chú sử dụng chung siêu lỏng"
    Hyperliquid không hỗ trợ lệnh thị trường, tuy nhiên ccxt sẽ mô phỏng lệnh thị trường bằng cách đặt lệnh giới hạn với độ trượt tối đa là 5%.  
    Thật không may, siêu thanh khoản chỉ cung cấp 5000 nến lịch sử, do đó, việc kiểm tra lại sẽ cần phải xây dựng nến lịch sử (bằng cách chờ và tải dữ liệu tăng dần theo thời gian) - hoặc sẽ bị giới hạn ở 5000 nến cuối cùng.

!!! Thông tin "Một số phương pháp hay nhất chung (không đầy đủ)"
    * Hãy cẩn thận với các cuộc tấn công vào chuỗi cung ứng, chẳng hạn như ngộ độc gói pip, v.v. Bất cứ khi nào bạn sử dụng khóa riêng của mình, hãy đảm bảo môi trường của bạn được an toàn.    * Don't use your actual wallet private key for trading. Use the Hyperliquid [API generator](https://app.hyperliquid.xyz/API) to create a separate API wallet.
* Không lưu trữ khóa riêng của ví thực tế của bạn trên máy chủ bạn sử dụng cho freqtrade. Thay vào đó hãy sử dụng khóa riêng của ví API. Chìa khóa này sẽ không cho phép rút tiền, chỉ giao dịch.
    * Luôn giữ kín cụm từ ghi nhớ và khóa riêng của bạn.
    * Không sử dụng cách ghi nhớ giống như cách bạn phải sao lưu khi khởi tạo ví phần cứng, việc sử dụng cùng một cách ghi nhớ về cơ bản sẽ xóa tính bảo mật của ví phần cứng của bạn.
    * Tạo một ví phần mềm khác, chỉ chuyển số tiền bạn muốn giao dịch sang ví đó và sử dụng ví đó để giao dịch trên Hyperliquid.
    * Nếu bạn có tiền mà bạn không muốn sử dụng để giao dịch (chẳng hạn như sau khi kiếm được lợi nhuận), hãy chuyển chúng trở lại ví phần cứng của bạn.


!!! Cảnh báo "Vaults và tài khoản phụ"
    Bạn chỉ có thể sử dụng vault hoặc tài khoản phụ - không thể sử dụng cả hai cùng một lúc.

### Tài khoản phụ siêu thanh khoản

Siêu thanh khoản cho phép bạn tạo tài khoản phụ với khối lượng giao dịch đủ trước đó.  
Để sử dụng tài khoản phụ với Freqtrade, bạn sẽ cần sử dụng mẫu cấu hình sau:``` json
"exchange": {
    "name": "hyperliquid",
    "walletAddress": "your_master_wallet_address", // Your master wallet address (not the API wallet or vault address - but not subaccount address).
    "privateKey": "your_api_private_key", // API wallet private key (see https://app.hyperliquid.xyz/API). You'll only need the private key.
    "ccxt_config": {
        "options": {
            "subAccountAddress": "your_subaccount_address" // Required if you want to use a subaccount.
        }
    },
    // ...
}
```Số dư và giao dịch của bạn bây giờ sẽ được sử dụng từ tài khoản phụ - và không còn từ tài khoản chính của bạn nữa.

### Vault siêu thanh khoản

Hyperliquid cho phép bạn tạo vault. Để sử dụng vault với Freqtrade, bạn sẽ cần sử dụng mẫu cấu hình sau:``` json
"exchange": {
    "name": "hyperliquid",
    "walletAddress": "your_vault_address", // Your vault wallet address (Must also be added below in the ccxt_config.options.vaultAddress field)
    "privateKey": "your_api_private_key", // API wallet private key (see https://app.hyperliquid.xyz/API). You'll only need the private key.
    "ccxt_config": {
        "options": {
            "vaultAddress": "your_vault_address", // Optional, only if you want to use a vault ... (vault address must also be added to walletAdress)
        }
    },
    // ...
}
```Số dư và giao dịch của bạn bây giờ sẽ được sử dụng từ kho tiền của bạn - và không còn từ tài khoản chính của bạn nữa.

### Dữ liệu siêu thanh khoản lịch sử

API Hyperliquid không cung cấp dữ liệu lịch sử ngoài lệnh gọi duy nhất để tìm nạp dữ liệu hiện tại, do đó không thể tải xuống dữ liệu vì dữ liệu đã tải xuống sẽ không cấu thành dữ liệu lịch sử thích hợp.

### DEX HIP-3

Hyperliquid hỗ trợ các sàn giao dịch phi tập trung HIP-3 (DEX), là các sàn giao dịch độc lập được xây dựng dựa trên cơ sở hạ tầng Hyperliquid.
Các DEX này hoạt động tương tự như sàn giao dịch Hyperliquid chính nhưng được cộng đồng tạo ra và quản lý.

Để giao dịch trên HIP-3 DEX với Freqtrade, bạn cần thêm chúng vào cấu hình của mình bằng tham số `hip3_dexes`:```json
"exchange": {
    "name": "hyperliquid",
    "walletAddress": "your_master_wallet_address",
    "privateKey": "your_api_private_key",
    "hip3_dexes": ["dex_name_1", "dex_name_2"]
}
```Thay thế `"dex_name_1"` và `"dex_name_2"` bằng tên thực của các DEX HIP-3 mà bạn muốn giao dịch (ví dụ: `vntl` và `xyz`).

!!! Cảnh báo "Tác động đến giới hạn hiệu suất và tỷ lệ"
    Mỗi HIP-3 DEX bạn thêm vào sẽ tác động đáng kể đến hiệu suất và giới hạn tốc độ của bot.

    * **Các lệnh gọi API bổ sung**: Đối với mỗi HIP-3 DEX được định cấu hình, Freqtrade cần thực hiện các lệnh gọi API bổ sung.
    * **Áp lực giới hạn tỷ lệ**: Các lệnh gọi API bổ sung góp phần vào giới hạn tỷ lệ nghiêm ngặt của Hyperliquid. Với nhiều DEX, bạn có thể đạt giới hạn tốc độ nhanh hơn hoặc nói đúng hơn là làm chậm hoạt động của bot do độ trễ được thực thi.

    Vui lòng chỉ thêm các DEX HIP-3 mà bạn tích cực giao dịch. Theo dõi nhật ký của bạn để biết các cảnh báo về giới hạn tốc độ hoặc các dấu hiệu hoạt động bị chậm lại và điều chỉnh cấu hình của bạn cho phù hợp.  
    Các DEX HIP-3 khác nhau cũng có thể sử dụng các loại tiền định giá khác nhau - vì vậy hãy đảm bảo chỉ thêm các DEX tương thích với loại tiền đặt cược của bạn để tránh sự chậm trễ không cần thiết.

!!! Lưu ý
    Các DEX HIP-3 chia sẻ cùng một ví và số lượng tài sản thế chấp miễn phí như tài khoản Hyperliquid chính của bạn. Giao dịch trên các DEX khác nhau sẽ ảnh hưởng đến số dư và số dư tài khoản tổng thể của bạn.

    Tên cặp cho cặp HIP-3 sẽ hơi khác so với cặp không phải HIP-3. Vui lòng sử dụng lệnh phụ `list-pairs` để đặt tên cặp chính xác cho tất cả các cặp cho các dex được chỉ định.

##Bitvavo

Nếu tài khoản của bạn được yêu cầu sử dụng operatorId, bạn có thể đặt nó trong tệp cấu hình như sau:``` json
"exchange": {
        "name": "bitvavo",
        "key": "",
        "secret": "",
        "ccxt_config": {
            "options": {
                "operatorId": "123567"
            }
        },
   }
```Bitvavo yêu cầu `operatorId` là số nguyên.

## Tất cả các trao đổi

Nếu bạn gặp lỗi liên tục với Nonce (như `InvalidNonce`), tốt nhất bạn nên tạo lại khóa API. Việc đặt lại Nonce rất khó và việc tạo lại các khóa API thường dễ dàng hơn.

## Ghi chú ngẫu nhiên cho các sàn giao dịch khác

* Sàn giao dịch Ocean (id trao đổi: `theocean`) sử dụng chức năng Web3 và yêu cầu cài đặt gói python `web3`:```shell
pip3 install web3
```### Lấy giá mới nhất / Nến chưa hoàn thiện

Hầu hết các sàn giao dịch đều trả lại nến chưa hoàn thiện hiện tại thông qua giao diện API OHLCV/klines của họ.
Theo mặc định, Freqtrade giả định rằng nến chưa hoàn thiện được lấy từ sàn giao dịch và loại bỏ nến cuối cùng giả sử đó là nến chưa hoàn chỉnh.

Bạn có thể kiểm tra xem sàn giao dịch của bạn có trả về những cây nến chưa hoàn chỉnh hay không bằng cách sử dụng [tập lệnh trợ giúp](developer.md#incomplete-candles) từ tài liệu của Contributor.

Do nguy cơ sơn lại, Freqtrade không cho phép bạn sử dụng cây nến chưa hoàn thiện này.

Tuy nhiên, nếu yêu cầu này dựa trên nhu cầu về mức giá mới nhất cho chiến lược của bạn - thì bạn có thể đạt được yêu cầu này bằng cách sử dụng [nhà cung cấp dữ liệu](strategy-customization.md#possible-options-for-dataprovider) từ trong chiến lược.

### Cấu hình trao đổi Freqtrade nâng cao

Bạn có thể định cấu hình các tùy chọn nâng cao bằng cách sử dụng cài đặt `_ft_has_params`, cài đặt này sẽ ghi đè Mặc định và hành vi dành riêng cho sàn giao dịch.

Các tùy chọn có sẵn được liệt kê trong lớp trao đổi dưới dạng `_ft_has_default`.

Ví dụ: để kiểm tra loại đơn đặt hàng `FOK` với Kraken và sửa đổi giới hạn nến thành 200 (vì vậy bạn chỉ nhận được 200 nến cho mỗi lệnh gọi API):```json
"exchange": {
    "name": "kraken",
    "_ft_has_params": {
        "order_time_in_force": ["GTC", "FOK"],
        "ohlcv_candle_limit": 200
        }
    //...
}
```!!! Cảnh báo
    Hãy đảm bảo hiểu đầy đủ tác động của các cài đặt này trước khi sửa đổi chúng.
    Việc sử dụng ghi đè `_ft_has_params` có thể dẫn đến hành vi không mong muốn và thậm chí có thể làm hỏng bot của bạn.
    Chúng tôi sẽ không thể cung cấp hỗ trợ cho các sự cố do cài đặt tùy chỉnh trong `_ft_has_params` gây ra.