<!-- Auto-translated from docs/ by script. Please review technical terms. -->

# Cấu hình bot

Freqtrade có nhiều tính năng và khả năng có thể cấu hình.
Theo mặc định, các cài đặt này được định cấu hình thông qua tệp cấu hình (xem bên dưới).

## File cấu hình Freqtrade

Bot sử dụng một tập hợp các tham số cấu hình trong quá trình hoạt động, tất cả đều tuân theo cấu hình bot. Nó thường đọc cấu hình của nó từ một tệp (tệp cấu hình Freqtrade).

Theo mặc định, bot tải cấu hình từ tệp `config.json`, nằm trong thư mục làm việc hiện tại.

Bạn có thể chỉ định một tệp cấu hình khác được bot sử dụng bằng tùy chọn dòng lệnh `-c/--config`.

Nếu bạn đã sử dụng phương pháp [Khởi động nhanh](docker_quickstart.md#docker-quick-start) để cài đặt
bot, tập lệnh cài đặt chắc hẳn đã tạo tệp cấu hình mặc định (`config.json`) cho bạn.

Nếu tệp cấu hình mặc định không được tạo, chúng tôi khuyên bạn nên sử dụng `freqtrade new-config --config user_data/config.json` để tạo tệp cấu hình cơ bản.

Tệp cấu hình Freqtrade phải được viết ở định dạng JSON.

Ngoài cú pháp JSON tiêu chuẩn, bạn có thể sử dụng các nhận xét `// ...` một dòng và nhiều dòng `/* ... */` trong tệp cấu hình của mình và dấu phẩy ở cuối trong danh sách tham số.

Đừng lo lắng nếu bạn không quen với định dạng JSON -- chỉ cần mở tệp cấu hình bằng trình chỉnh sửa bạn chọn, thực hiện một số thay đổi đối với các tham số bạn cần, lưu các thay đổi và cuối cùng, khởi động lại bot hoặc, nếu nó đã bị dừng trước đó, hãy chạy lại bot với những thay đổi bạn đã thực hiện đối với cấu hình. Bot xác thực cú pháp của tệp cấu hình khi khởi động và sẽ cảnh báo bạn nếu bạn mắc bất kỳ lỗi nào khi chỉnh sửa tệp đó, đồng thời chỉ ra các dòng có vấn đề.

### Biến môi trường

Đặt tùy chọn trong cấu hình Freqtrade thông qua các biến môi trường.
Điều này được ưu tiên hơn giá trị tương ứng trong cấu hình hoặc chiến lược.

Các biến môi trường phải có tiền tố `FREQTRADE__` để được tải vào cấu hình freqtrade.

`__` đóng vai trò là dấu phân cách cấp, vì vậy định dạng được sử dụng phải tương ứng với `FREQTRADE__{section___{key}`.
Như vậy - một biến môi trường được xác định là `export FREQTRADE__STAKE_AMOUNT=200` sẽ dẫn đến `{stake_amount: 200}`.

Một ví dụ phức tạp hơn có thể là `export FREQTRADE__EXCHANGE__KEY=<yourExchangeKey>` để giữ bí mật khóa trao đổi của bạn. Điều này sẽ di chuyển giá trị sang phần `exchange.key` của cấu hình.
Sử dụng lược đồ này, tất cả các cài đặt cấu hình cũng sẽ có sẵn dưới dạng các biến môi trường.

Xin lưu ý rằng các biến Môi trường sẽ ghi đè các cài đặt tương ứng trong cấu hình của bạn, nhưng Đối số dòng lệnh sẽ luôn thắng.

Ví dụ phổ biến:``` bash
FREQTRADE__TELEGRAM__CHAT_ID=<telegramchatid>
FREQTRADE__TELEGRAM__TOKEN=<telegramToken>
FREQTRADE__EXCHANGE__KEY=<yourExchangeKey>
FREQTRADE__EXCHANGE__SECRET=<yourExchangeSecret>
```Danh sách Json được phân tích cú pháp dưới dạng json - vì vậy bạn có thể sử dụng cách sau để đặt danh sách các cặp:``` bash
export FREQTRADE__EXCHANGE__PAIR_WHITELIST='["BTC/USDT", "ETH/USDT"]'
```!!! Lưu ý
    Các biến môi trường được phát hiện sẽ được ghi lại khi khởi động - vì vậy nếu bạn không thể tìm ra lý do tại sao một giá trị không như bạn nghĩ dựa trên cấu hình, hãy đảm bảo rằng giá trị đó không được tải từ một biến môi trường.

!!! Mẹo "Xác thực kết quả tổng hợp"
    Bạn có thể sử dụng [lệnh phụ show-config](utils.md#show-config) để xem cấu hình kết hợp cuối cùng.

??? Cảnh báo "Trình tự tải"
    Các biến môi trường được tải sau cấu hình ban đầu. Như vậy, bạn không thể cung cấp đường dẫn đến cấu hình thông qua các biến môi trường. Vui lòng sử dụng `--config path/to/config.json` cho việc đó.
    Điều này cũng áp dụng cho `user_dir` ở một mức độ nào đó. trong khi thư mục người dùng có thể được đặt thông qua các biến môi trường - cấu hình sẽ **không** được tải từ vị trí đó.

### Nhiều tệp cấu hình

Nhiều tệp cấu hình có thể được chỉ định và sử dụng bởi bot hoặc bot có thể đọc các tham số cấu hình của nó từ luồng đầu vào tiêu chuẩn của quy trình.

Bạn có thể chỉ định các tệp cấu hình bổ sung trong `add_config_files`. Các tệp được chỉ định trong tham số này sẽ được tải và hợp nhất với tệp cấu hình ban đầu. Các tập tin được giải quyết liên quan đến tập tin cấu hình ban đầu.
Điều này tương tự như việc sử dụng nhiều tham số `--config`, nhưng cách sử dụng đơn giản hơn vì bạn không phải chỉ định tất cả các tệp cho tất cả các lệnh.

!!! Mẹo "Xác thực kết quả tổng hợp"
    Bạn có thể sử dụng [lệnh phụ show-config](utils.md#show-config) để xem cấu hình kết hợp cuối cùng.

!!! Mẹo "Sử dụng nhiều file cấu hình để giữ bí mật"
    Bạn có thể sử dụng tệp cấu hình thứ 2 chứa bí mật của mình. Bằng cách đó, bạn có thể chia sẻ tệp cấu hình "chính" của mình trong khi vẫn giữ các khóa API cho riêng mình.
    Tệp thứ 2 chỉ nên chỉ định những gì bạn định ghi đè.
    Nếu một khóa nằm trong nhiều cấu hình thì "cấu hình được chỉ định cuối cùng" sẽ thắng (trong ví dụ trên là `config-private.json`).

    Đối với các lệnh một lần, bạn cũng có thể sử dụng cú pháp bên dưới bằng cách chỉ định nhiều tham số "--config".``` bash
    freqtrade trade --config user_data/config1.json --config user_data/config-private.json <...>
    ```Phần bên dưới tương đương với ví dụ trên - nhưng có 2 file cấu hình trong config, để sử dụng lại dễ dàng hơn.``` json title="user_data/config.json"
    "add_config_files": [
        "config1.json",
        "config-private.json"
    ]
    `````` bash
    freqtrade trade --config user_data/config.json <...>
    ```??? Lưu ý "xử lý xung đột cấu hình"
    Nếu cài đặt cấu hình giống nhau diễn ra trong cả `config.json` và `config-import.json`, thì cấu hình gốc sẽ thắng.
    Trong trường hợp bên dưới, `max_open_trades` sẽ là 3 sau khi hợp nhất - vì cấu hình "nhập" có thể sử dụng lại đã ghi đè khóa này.``` json title="user_data/config.json"
    {
        "max_open_trades": 3,
        "stake_currency": "USDT",
        "add_config_files": [
            "config-import.json"
        ]
    }
    `````` json title="user_data/config-import.json"
    {
        "max_open_trades": 10,
        "stake_amount": "unlimited",
    }
    ```Kết quả cấu hình kết hợp:``` json title="Result"
    {
        "max_open_trades": 3,
        "stake_currency": "USDT",
        "stake_amount": "unlimited"
    }
    ```Nếu có nhiều tệp trong phần `add_config_files` thì chúng sẽ được coi là ở các cấp giống hệt nhau, lần xuất hiện cuối cùng sẽ ghi đè cấu hình trước đó (trừ khi cha mẹ đã xác định khóa như vậy).

## Trình chỉnh sửa tự động hoàn tất và xác thực

Nếu bạn đang sử dụng trình chỉnh sửa hỗ trợ lược đồ JSON, bạn có thể sử dụng lược đồ do Freqtrade cung cấp để tự động hoàn thành và xác thực tệp cấu hình của mình bằng cách thêm dòng sau vào đầu tệp cấu hình của bạn:``` json
{
    "$schema": "https://schema.freqtrade.io/schema.json",
}
```??? Lưu ý "Phát triển phiên bản"    The develop schema is available as `https://schema.freqtrade.io/schema_dev.json` - though we recommend to stick to the stable version for the best experience.
## Thông số cấu hình

Bảng dưới đây sẽ liệt kê tất cả các thông số cấu hình có sẵn.

Freqtrade cũng có thể tải nhiều tùy chọn thông qua các đối số dòng lệnh (CLI) (xem đầu ra lệnh `--help` để biết chi tiết).

### Mức độ phổ biến của tùy chọn cấu hình

Mức độ phổ biến của tất cả các Tùy chọn như sau:

* Đối số CLI ghi đè bất kỳ tùy chọn nào khác
* [Biến môi trường](#biến môi trường)
* Các tệp cấu hình được sử dụng theo trình tự (tệp cuối cùng sẽ thắng) và ghi đè các cấu hình Chiến lược.
* Cấu hình chiến lược chỉ được sử dụng nếu chúng không được đặt thông qua cấu hình hoặc đối số dòng lệnh. Các tùy chọn này được đánh dấu bằng [Ghi đè chiến lược](#parameters-in-the-strategy) trong bảng bên dưới.

### Bảng tham số

Các tham số bắt buộc được đánh dấu là **Bắt buộc**, có nghĩa là chúng bắt buộc phải được đặt theo một trong các cách có thể.

|  Tham số | Mô tả |
|----------||-------------|
| `max_open_trades` | **Bắt buộc.** Số lượng giao dịch mở mà bot của bạn được phép có. Chỉ có thể thực hiện một giao dịch mở cho mỗi cặp, vì vậy độ dài danh sách cặp của bạn là một hạn chế khác có thể áp dụng. Nếu -1 thì nó bị bỏ qua (tức là các giao dịch mở có khả năng không giới hạn, bị giới hạn bởi danh sách cặp). [Thêm thông tin bên dưới](#configuring-amount-per-trade). [Ghi đè chiến lược](#parameters-in-the-strategy).<br> **Loại dữ liệu:** Số nguyên dương hoặc -1.
| `cổ phần_tiền tệ` | **Bắt buộc.** Loại tiền điện tử được sử dụng để giao dịch. <br> **Loại dữ liệu:** Chuỗi
| `số tiền đặt cược` | **Bắt buộc.** Số lượng tiền điện tử mà bot của bạn sẽ sử dụng cho mỗi giao dịch. Đặt nó thành `"không giới hạn"` để cho phép bot sử dụng tất cả số dư hiện có. [Thêm thông tin bên dưới](#configuring-amount-per-trade). <br> **Loại dữ liệu:** Số float dương hoặc `"không giới hạn"`.
| `tỷ lệ_cân bằng_có thể giao dịch` | Tỷ lệ trên tổng số dư tài khoản mà bot được phép giao dịch. [Thêm thông tin bên dưới](#configuring-amount-per-trade). <br>*Mặc định là `0,99` 99%).*<br> **Loại dữ liệu:** Số float dương giữa `0,1` và `1,0`.
| `có sẵn_vốn` | Vốn ban đầu có sẵn cho bot. Hữu ích khi chạy nhiều bot trên cùng một tài khoản trao đổi. [Thêm thông tin bên dưới](#configuring-amount-per-trade). <br> **Loại dữ liệu:** Số float dương.
| `sửa đổi_lần cuối_stake_amount` | Sử dụng số tiền đặt cược cuối cùng đã giảm nếu cần thiết. [Thêm thông tin bên dưới](#configuring-amount-per-trade). <br>*Mặc định là `false`.* <br> **Loại dữ liệu:** Boolean
| `tỷ lệ cổ phần cuối cùng_số tiền_min_` | Xác định số tiền đặt cược tối thiểu phải được để lại và thực hiện. Chỉ áp dụng cho số tiền đặt cược cuối cùng khi nó được sửa đổi thành giá trị giảm (tức là nếu `amend_last_stake_amount` được đặt thành `true`). [Thêm thông tin bên dưới](#configuring-amount-per-trade). <br>*Mặc định là `0,5`.* <br> **Loại dữ liệu:** Float (dưới dạng tỷ lệ)
| `số tiền_dự trữ_phần trăm` | Dự trữ một số tiền theo số tiền đặt cược tối thiểu theo cặp. Bot sẽ dự trữ `amount_reserve_percent` + giá trị dừng lỗ khi tính toán số tiền đặt cược tối thiểu của cặp để tránh bị từ chối giao dịch có thể xảy ra. <br>*Mặc định là `0,05` (5%).* <br> **Loại dữ liệu:** Tỷ lệ thả nổi dương.
| `khung thời gian` | Khung thời gian sử dụng (ví dụ: `1m`, `5m`, `15m`, `30m`, `1h` ...). Thường bị thiếu trong cấu hình và được chỉ định trong chiến lược. [Ghi đè chiến lược](#parameters-in-the-strategy). <br> **Loại dữ liệu:** Chuỗi
| `fiat_display_currency` | Tiền tệ Fiat được sử dụng để hiển thị lợi nhuận của bạn. [Thông tin thêm bên dưới](#giá trị nào có thể được sử dụng cho tiền pháp định_display_currency). <br> **Loại dữ liệu:** Chuỗi| `dry_run` | **Bắt buộc.** Xác định xem bot phải ở chế độ Dry Run hay chế độ sản xuất. <br>*Mặc định là `true`.* <br> **Loại dữ liệu:** Boolean
| `dry_run_wallet` | Xác định số tiền bắt đầu bằng tiền đặt cọc cho ví mô phỏng được sử dụng bởi bot chạy ở chế độ Dry Run. [Thông tin thêm bên dưới](#dry-run-wallet)<br>*Mặc định là `1000`.* <br> **Loại dữ liệu:** Float hoặc Dict
| `hủy_open_orders_on_exit` | Hủy các lệnh đang mở khi lệnh `/stop` RPC được ban hành, `Ctrl+C` được nhấn hoặc bot chết đột ngột. Khi được đặt thành `true`, điều này cho phép bạn sử dụng `/stop` để hủy các đơn đặt hàng chưa được thực hiện và được thực hiện một phần trong trường hợp thị trường sụp đổ. Nó không ảnh hưởng đến các vị trí mở. <br>*Mặc định là `false`.* <br> **Loại dữ liệu:** Boolean
| `process_only_new_candles` | Chỉ cho phép xử lý các chỉ báo khi nến mới xuất hiện. Nếu sai, mỗi vòng lặp điền các chỉ báo, điều này có nghĩa là cùng một cây nến được xử lý nhiều lần tạo ra tải hệ thống nhưng có thể hữu ích cho chiến lược của bạn phụ thuộc vào dữ liệu đánh dấu chứ không chỉ nến. [Ghi đè chiến lược](#parameters-in-the-strategy). <br>*Mặc định là `true`.* <br> **Loại dữ liệu:** Boolean
| `minimal_roi` | **Bắt buộc.** Đặt ngưỡng theo tỷ lệ mà bot sẽ sử dụng để thoát giao dịch. [Thêm thông tin bên dưới](#hiểu-minimal_roi). [Ghi đè chiến lược](#parameters-in-the-strategy). <br> **Loại dữ liệu:** Lệnh
| `dừng lỗ` |  **Bắt buộc.** Giá trị theo tỷ lệ của mức dừng lỗ được bot sử dụng. Xem thêm chi tiết trong [tài liệu về điểm dừng lỗ](stoploss.md). [Ghi đè chiến lược](#parameters-in-the-strategy).  <br> **Loại dữ liệu:** Float (dưới dạng tỷ lệ)
| `dừng_dừng` | Cho phép dừng lỗ theo sau (dựa trên `stoploss` trong tệp cấu hình hoặc chiến lược). Xem thêm chi tiết trong [tài liệu về điểm dừng lỗ](stoploss.md#trailing-stop-loss). [Ghi đè chiến lược](#parameters-in-the-strategy). <br> **Loại dữ liệu:** Boolean
| `trail_stop_tích cực` | Thay đổi điểm dừng lỗ khi đã đạt được lợi nhuận. Thông tin chi tiết hơn trong [tài liệu về điểm dừng lỗ](stoploss.md#trailing-stop-loss-other-posit-loss). [Ghi đè chiến lược](#parameters-in-the-strategy). <br> **Loại dữ liệu:** Phao
| `trailing_stop_posit_offset` | Bù đắp về thời điểm áp dụng `trailing_stop_posit`. Giá trị phần trăm phải dương. Thông tin chi tiết hơn trong [tài liệu về điểm dừng lỗ](stoploss.md#trailing-stop-loss-only-once-the-trade-has-reached-a-certain-offset). [Ghi đè chiến lược](#parameters-in-the-strategy). <br>*Mặc định là `0,0` (không có offset).* <br> **Loại dữ liệu:** Float
| `trailing_only_offset_is_reached` | Chỉ áp dụng mức dừng lỗ khi đạt đến mức bù. [tài liệu về điểm dừng lỗ](stoploss.md). [Ghi đè chiến lược](#parameters-in-the-strategy). <br>*Mặc định là `false`.* <br> **Loại dữ liệu:** Boolean
| `phí` | Phí sử dụng trong quá trình kiểm tra lại/chạy thử. Thông thường không nên được định cấu hình, điều này khiến freqtrade quay trở lại mức phí mặc định của sàn giao dịch. Đặt làm tỷ lệ (ví dụ: 0,001 = 0,1%). Phí được áp dụng hai lần cho mỗi giao dịch, một lần khi mua, một lần khi bán. <br> **Loại dữ liệu:** Float (dưới dạng tỷ lệ)
| `tương lai_tỷ lệ cấp vốn` | Tỷ lệ cấp vốn do người dùng chỉ định sẽ được sử dụng khi tỷ lệ cấp vốn lịch sử không có sẵn trên sàn giao dịch. Điều này không ghi đè lên tỷ lệ lịch sử thực tế. Bạn nên đặt giá trị này thành 0 trừ khi bạn đang thử nghiệm một loại tiền cụ thể và bạn hiểu tỷ lệ tài trợ sẽ ảnh hưởng như thế nào đến tính toán lợi nhuận của freqtrade. [Thông tin thêm tại đây](đòn bẩy.md#unavailable-funding-rates) <br>*Mặc định là `None`.*<br> **Loại dữ liệu:** Float| `chế độ giao dịch` | Chỉ định xem bạn muốn giao dịch thường xuyên, giao dịch bằng đòn bẩy hay giao dịch hợp đồng có giá bắt nguồn từ việc khớp giá tiền điện tử. [tài liệu đòn bẩy](đòn bẩy.md). <br>*Mặc định là `"spot"`.* <br> **Loại dữ liệu:** Chuỗi
| `lề_mode` | Khi giao dịch bằng đòn bẩy, điều này sẽ xác định xem tài sản thế chấp thuộc sở hữu của nhà giao dịch sẽ được chia sẻ hay tách biệt với từng cặp giao dịch [tài liệu về đòn bẩy](đòn bẩy.md). <br> **Loại dữ liệu:** Chuỗi
| `thanh lý_buffer` | Tỷ lệ xác định mức độ an toàn của mạng lưới an toàn được đặt giữa giá thanh lý và mức dừng lỗ để ngăn vị thế đạt đến giá thanh lý [tài liệu đòn bẩy](đòn bẩy.md). <br>*Mặc định là `0,05`.* <br> **Loại dữ liệu:** Float
| | **Thời gian chờ chưa được lấp đầy**
| `unfilledtimeout.entry` | **Bắt buộc.** Khoảng thời gian (tính bằng phút hoặc giây) bot sẽ đợi một lệnh nhập chưa được thực hiện hoàn tất, sau đó lệnh đó sẽ bị hủy. [Ghi đè chiến lược](#parameters-in-the-strategy).<br> **Loại dữ liệu:** Số nguyên
| `unfilledtimeout.exit` | **Bắt buộc.** Khoảng thời gian (tính bằng phút hoặc giây) bot sẽ đợi một lệnh thoát chưa được thực hiện hoàn tất, sau đó lệnh sẽ bị hủy và lặp lại ở mức giá hiện tại (mới), miễn là có tín hiệu. [Ghi đè chiến lược](#parameters-in-the-strategy).<br> **Loại dữ liệu:** Số nguyên
| `unfilledtimeout.unit` | Đơn vị để sử dụng trong cài đặt thời gian chờ không được thực hiện. Lưu ý: Nếu bạn đặt `unfilledtimeout.unit` thành "giây", "internals.process_throttle_secs" phải thấp hơn hoặc bằng thời gian chờ [Ghi đè chiến lược](#parameters-in-the-strategy). <br> *Mặc định là `"phút"`.* <br> **Loại dữ liệu:** Chuỗi
| `unfilltimeout.exit_timeout_count` | Bao nhiêu lần có thể thoát lệnh hết thời gian. Khi đạt đến số lượng thời gian chờ này, lối thoát khẩn cấp sẽ được kích hoạt. 0 để vô hiệu hóa và cho phép hủy đơn hàng không giới hạn. [Ghi đè chiến lược](#parameters-in-the-strategy).<br>*Mặc định là `0`.* <br> **Loại dữ liệu:** Số nguyên
| | **Giá cả**
| `entry_pricing.price_side` | Chọn mức chênh lệch mà bot nên xem xét để có được tỷ lệ vào lệnh. [Thông tin thêm bên dưới](#entry-price).<br> *Mặc định là `"same"`.* <br> **Loại dữ liệu:** Chuỗi (`ask`, `bid`, `same` hoặc `other`).
| `entry_pricing.price_last_balance` | **Bắt buộc.** Nội suy giá dự thầu. Thông tin thêm [bên dưới](#entry-price-without-orderbook-enabled).
| `entry_pricing.use_order_book` | Cho phép nhập bằng cách sử dụng tỷ giá trong [Nhập sổ đặt hàng](#entry-price-with-orderbook-enabled). <br> *Mặc định là `true`.*<br> **Loại dữ liệu:** Boolean
| `entry_pricing.order_book_top` | Bot sẽ sử dụng tỷ lệ N cao nhất trong Sổ đặt hàng "price_side" để tham gia giao dịch. tức là giá trị 2 sẽ cho phép bot chọn mục thứ 2 trong [Nhập sổ đặt hàng](#entry-price-with-orderbook-enabled). <br>*Mặc định là `1`.* <br> **Loại dữ liệu:** Số nguyên dương
| `giá_đầu vào. check_deep_of_market.enabled` | Không nhập nếu có sự khác biệt giữa lệnh mua và lệnh bán trong Sổ lệnh. [Kiểm tra độ sâu thị trường](#check-độ sâu thị trường). <br>*Mặc định là `false`.* <br> **Loại dữ liệu:** Boolean
| `giá_đầu vào. check_deep_of_market.bids_to_ask_delta` | Tỷ lệ chênh lệch giữa lệnh mua và lệnh bán tìm thấy trong Sổ lệnh. Giá trị dưới 1 nghĩa là quy mô lệnh bán lớn hơn, trong khi giá trị lớn hơn 1 nghĩa là quy mô lệnh mua cao hơn. [Kiểm tra độ sâu thị trường](#check-độ sâu thị trường) <br> *Mặc định là `0`.* <br> **Loại dữ liệu:** Float (dưới dạng tỷ lệ)| `exit_pricing.price_side` | Chọn mức chênh lệch mà bot sẽ xem xét để biết tỷ lệ thoát. [Thông tin thêm bên dưới](#exit-price-side).<br> *Mặc định là `"same"`.* <br> **Loại dữ liệu:** Chuỗi (`ask`, `bid`, `same` hoặc `other`).
| `exit_pricing.price_last_balance` | Nội suy giá thoát. Thông tin thêm [bên dưới](#exit-price-without-orderbook-enabled).
| `exit_pricing.use_order_book` | Cho phép thoát các giao dịch đang mở bằng cách sử dụng [Thoát sổ lệnh](#exit-price-with-orderbook-enabled). <br> *Mặc định là `true`.*<br> **Loại dữ liệu:** Boolean
| `exit_pricing.order_book_top` | Bot sẽ sử dụng tỷ lệ N cao nhất trong Sổ lệnh "price_side" để thoát. tức là giá trị 2 sẽ cho phép bot chọn tỷ lệ yêu cầu thứ 2 trong [Thoát sổ lệnh](#exit-price-with-orderbook-enabled)<br>*Mặc định là `1`.* <br> **Loại dữ liệu:** Số nguyên dương
| `tỷ lệ tùy chỉnh_giá_tối đa_khoảng cách` | Định cấu hình tỷ lệ khoảng cách tối đa giữa giá vào hoặc thoát hiện tại và tùy chỉnh. <br>*Mặc định là `0,02` 2%).*<br> **Loại dữ liệu:** Số float dương
| | **Xử lý lệnh/tín hiệu**
| `use_exit_signal` | Sử dụng các tín hiệu thoát do chiến lược tạo ra ngoài `roi tối thiểu`. <br>Đặt giá trị này thành sai sẽ vô hiệu hóa việc sử dụng cột `"exit_long"` và `"exit_short"`. Không ảnh hưởng đến các phương thức thoát khác (Cắt lỗ, ROI, lệnh gọi lại). [Ghi đè chiến lược](#parameters-in-the-strategy). <br>*Mặc định là `true`.* <br> **Loại dữ liệu:** Boolean
| `chỉ thoát_lợi nhuận` | Đợi cho đến khi bot đạt đến `exit_profit_offset` trước khi đưa ra quyết định thoát. [Ghi đè chiến lược](#parameters-in-the-strategy). <br>*Mặc định là `false`.* <br> **Loại dữ liệu:** Boolean
| `exit_profit_offset` | Tín hiệu thoát chỉ hoạt động trên giá trị này. Chỉ hoạt động kết hợp với `exit_profit_only=True`. [Ghi đè chiến lược](#parameters-in-the-strategy). <br>*Mặc định là `0,0`.* <br> **Loại dữ liệu:** Float (dưới dạng tỷ lệ)
| `bỏ qua_roi_if_entry_signal` | Không thoát nếu tín hiệu vào vẫn hoạt động. Cài đặt này được ưu tiên hơn `minimal_roi` và `use_exit_signal`. [Ghi đè chiến lược](#parameters-in-the-strategy). <br>*Mặc định là `false`.* <br> **Loại dữ liệu:** Boolean
| `bỏ qua_buying_hết hạn_nến_sau` | Chỉ định số giây cho đến khi tín hiệu mua không còn được sử dụng. <br> **Loại dữ liệu:** Số nguyên
| `loại_đơn hàng` | Định cấu hình loại lệnh tùy thuộc vào hành động ("entry"`, `"exit"`, `"stoploss"`, `"stoploss_on_exchange"`). [Thêm thông tin bên dưới](#hiểu-order_types). [Ghi đè chiến lược](#parameters-in-the-strategy).<br> **Loại dữ liệu:** Dict
| `order_time_in_force` | Cấu hình thời gian có hiệu lực cho các lệnh vào và thoát. [Thông tin thêm bên dưới](#hiểu-order_time_in_force). [Ghi đè chiến lược](#parameters-in-the-strategy). <br> **Loại dữ liệu:** Lệnh
| `vị trí_điều chỉnh_kích hoạt` | Cho phép chiến lược sử dụng điều chỉnh vị thế (mua hoặc bán bổ sung). [Thêm thông tin tại đây](strategy-callbacks.md# adjustment-trade-position). <br> [Ghi đè chiến lược](#parameters-in-the-strategy). <br>*Mặc định là `false`.*<br> **Loại dữ liệu:** Boolean
| `max_entry_position_điều chỉnh` | (Các) lệnh bổ sung tối đa cho mỗi giao dịch mở tính từ Lệnh nhập đầu tiên. Đặt nó thành `-1` cho các đơn hàng bổ sung không giới hạn. [Thêm thông tin tại đây](strategy-callbacks.md# adjustment-trade-position). <br> [Ghi đè chiến lược](#parameters-in-the-strategy). <br>*Mặc định là `-1`.*<br> **Loại dữ liệu:** Số nguyên dương hoặc -1
| | **Trao đổi**
| `trao đổi.name` | **Bắt buộc.** Tên của lớp trao đổi sẽ sử dụng. <br> **Loại dữ liệu:** Chuỗi| `trao đổi.key` | Khóa API để sử dụng để trao đổi. Chỉ bắt buộc khi bạn ở chế độ sản xuất.<br>**Giữ bí mật, không tiết lộ công khai.** <br> **Loại dữ liệu:** Chuỗi
| `trao đổi.bí mật` | API bí mật để sử dụng cho việc trao đổi. Chỉ bắt buộc khi bạn ở chế độ sản xuất.<br>**Giữ bí mật, không tiết lộ công khai.** <br> **Loại dữ liệu:** Chuỗi
| `trao đổi.password` | Mật khẩu API để sử dụng để trao đổi. Chỉ bắt buộc khi bạn ở chế độ sản xuất và đối với các sàn giao dịch sử dụng mật khẩu cho các yêu cầu API.<br>**Giữ bí mật, không tiết lộ công khai.** <br> **Loại dữ liệu:** Chuỗi
| `trao đổi.uid` | API uid để sử dụng cho việc trao đổi. Chỉ bắt buộc khi bạn ở chế độ sản xuất và đối với các sàn giao dịch sử dụng uid cho các yêu cầu API.<br>**Giữ bí mật, không tiết lộ công khai.** <br> **Loại dữ liệu:** Chuỗi
| `exchange.pair_whitelist` | Danh sách các cặp mà bot sẽ sử dụng để giao dịch và kiểm tra các giao dịch tiềm năng trong quá trình kiểm tra lại. Hỗ trợ các cặp biểu thức chính quy dưới dạng `.*/BTC`. Không được sử dụng bởi VolumePairList. [Thông tin thêm](plugins.md#pairlists-and-pairlist-handlers). <br> **Loại dữ liệu:** Danh sách
| `exchange.pair_blacklist` | Danh sách các cặp mà bot tuyệt đối phải tránh để giao dịch và kiểm tra lại. [Thông tin thêm](plugins.md#pairlists-and-pairlist-handlers). <br> **Loại dữ liệu:** Danh sách| `exchange.ccxt_config` | Additional CCXT parameters passed to both ccxt instances (sync and async). This is usually the correct place for additional ccxt configurations. Parameters may differ from exchange to exchange and are documented in the [ccxt documentation](https://docs.ccxt.com/#/README?id=overriding-exchange-properties-upon-instantiation). Please avoid adding exchange secrets here (use the dedicated fields instead), as they may be contained in logs. <br> **Datatype:** Dict
| `exchange.ccxt_sync_config` | Additional CCXT parameters passed to the regular (sync) ccxt instance. Parameters may differ from exchange to exchange and are documented in the [ccxt documentation](https://docs.ccxt.com/#/README?id=overriding-exchange-properties-upon-instantiation) <br> **Datatype:** Dict
| `exchange.ccxt_async_config` | Additional CCXT parameters passed to the async ccxt instance. Parameters may differ from exchange to exchange  and are documented in the [ccxt documentation](https://docs.ccxt.com/#/README?id=overriding-exchange-properties-upon-instantiation) <br> **Datatype:** Dict
| `trao đổi.enable_ws` | Cho phép sử dụng Websockets để trao đổi. <br>[Thông tin thêm](#taining-exchange-websockets).<br>*Mặc định là `true`.* <br> **Loại dữ liệu:** Boolean
| `exchange.markets_refresh_interval` | Khoảng thời gian tính bằng phút mà thị trường được tải lại. <br>*Mặc định là `60` phút.* <br> **Loại dữ liệu:** Số nguyên dương
| `trao đổi.skip_open_order_update` | Bỏ qua cập nhật lệnh mở khi khởi động nếu sàn giao dịch gây ra sự cố. Chỉ phù hợp trong điều kiện trực tiếp.<br>*Mặc định là `false`*<br> **Loại dữ liệu:** Boolean
| `trao đổi.unknown_fee_rate` | Giá trị dự phòng để sử dụng khi tính phí giao dịch. Điều này có thể hữu ích cho các sàn giao dịch có phí bằng loại tiền tệ không thể giao dịch. Giá trị được cung cấp ở đây sẽ được nhân với "chi phí".<br>*Mặc định là `None`*<br> **Datatype:** float
| `trao đổi.log_responses` | Ghi lại các phản hồi trao đổi có liên quan. Chỉ dành cho chế độ gỡ lỗi - hãy cẩn thận khi sử dụng.<br>*Mặc định là `false`*<br> **Loại dữ liệu:** Boolean
| `exchange.only_from_ccxt` | Ngăn chặn tải xuống dữ liệu từ data.binance.vision. Nếu đặt giá trị này là sai, tốc độ tải xuống có thể tăng đáng kể nhưng có thể gặp sự cố nếu trang web không khả dụng.<br>*Mặc định là `false`*<br> **Loại dữ liệu:** Boolean
| `thử nghiệm.block_bad_exchanges` | Chặn các sàn giao dịch được biết là không hoạt động với freqtrade. Để mặc định trừ khi bạn muốn kiểm tra xem sàn giao dịch đó có hoạt động hay không. <br>*Mặc định là `true`.* <br> **Loại dữ liệu:** Boolean
| | **Plugin**
| `danh sách cặp` | Xác định một hoặc nhiều danh sách cặp sẽ được sử dụng. [Thông tin thêm](plugins.md#pairlists-and-pairlist-handlers). <br>*Mặc định là `StaticPairList`.* <br> **Loại dữ liệu:** Danh sách các ký tự
| | **Điện tín**
| `telegram.enabled` | Cho phép sử dụng Telegram. <br> **Loại dữ liệu:** Boolean
| `telegram.token` | Mã thông báo bot Telegram của bạn. Chỉ bắt buộc nếu `telegram.enabled` là `true`. <br><br>**Giữ bí mật, không tiết lộ công khai.** <br> **Loại dữ liệu:** Chuỗi
| `telegram.chat_id` | Id tài khoản Telegram cá nhân của bạn. Chỉ bắt buộc nếu `telegram.enabled` là `true`. <br><br>**Giữ bí mật, không tiết lộ công khai.** <br> **Loại dữ liệu:** Chuỗi
| `telegram.balance_dust_level` | Mức độ bụi (bằng tiền đặt cược) - các loại tiền tệ có số dư dưới mức này sẽ không được hiển thị bằng `/ số dư`. <br> **kiểu dữ liệu:** thả nổi
| `telegram.reload` | Cho phép nút "tải lại" trên tin nhắn telegram. <br>*Mặc định là `true`.*<br> **Loại dữ liệu:** boolean
| `telegram.notification_settings.*` | Cài đặt thông báo chi tiết. Hãy tham khảo [telegram document](telegram-usage.md) để biết chi tiết.<br> **Datatype:** từ điển
| `telegram.allow_custom_messages` | Cho phép gửi tin nhắn Telegram từ các chiến lược thông qua chức năng dataprovider.send_msg(). <br> **Loại dữ liệu:** Boolean
| | **Webhook**
| `webhook.enabled` | Cho phép sử dụng thông báo Webhook <br> **Loại dữ liệu:** Boolean
| `webhook.url` | URL cho webhook. Chỉ bắt buộc nếu `webhook.enabled` là `true`. Xem [tài liệu webhook](webhook-config.md) để biết thêm chi tiết. <br> **Loại dữ liệu:** Chuỗi
| `webhook.entry` | Tải trọng để gửi khi nhập cảnh. Chỉ bắt buộc nếu `webhook.enabled` là `true`. Xem [tài liệu webhook](webhook-config.md) để biết thêm chi tiết. <br> **Loại dữ liệu:** Chuỗi
| `webhook.entry_cancel` | Tải trọng để gửi khi hủy lệnh nhập. Chỉ bắt buộc nếu `webhook.enabled` là `true`. Xem [tài liệu webhook](webhook-config.md) để biết thêm chi tiết. <br> **Loại dữ liệu:** Chuỗi| `webhook.entry_fill` | Tải trọng cần gửi theo lệnh nhập đã được điền. Chỉ bắt buộc nếu `webhook.enabled` là `true`. Xem [tài liệu webhook](webhook-config.md) để biết thêm chi tiết. <br> **Loại dữ liệu:** Chuỗi
| `webhook.exit` | Tải trọng để gửi khi thoát. Chỉ bắt buộc nếu `webhook.enabled` là `true`. Xem [tài liệu webhook](webhook-config.md) để biết thêm chi tiết. <br> **Loại dữ liệu:** Chuỗi
| `webhook.exit_cancel` | Tải trọng để gửi khi hủy lệnh thoát. Chỉ bắt buộc nếu `webhook.enabled` là `true`. Xem [tài liệu webhook](webhook-config.md) để biết thêm chi tiết. <br> **Loại dữ liệu:** Chuỗi
| `webhook.exit_fill` | Tải trọng cần gửi khi lệnh thoát đã được điền. Chỉ bắt buộc nếu `webhook.enabled` là `true`. Xem [tài liệu webhook](webhook-config.md) để biết thêm chi tiết. <br> **Loại dữ liệu:** Chuỗi
| `webhook.status` | Tải trọng để gửi trong các cuộc gọi trạng thái. Chỉ bắt buộc nếu `webhook.enabled` là `true`. Xem [tài liệu webhook](webhook-config.md) để biết thêm chi tiết. <br> **Loại dữ liệu:** Chuỗi
| `webhook.allow_custom_messages` | Cho phép gửi tin nhắn Webhook từ các chiến lược thông qua hàm dataprovider.send_msg(). <br> **Loại dữ liệu:** Boolean
| | **API còn lại / FreqUI / Nhà sản xuất-Người tiêu dùng**
| `api_server.enabled` | Cho phép sử dụng Máy chủ API. Xem [Tài liệu về máy chủ API](rest-api.md) để biết thêm chi tiết. <br> **Loại dữ liệu:** Boolean
| `api_server.listen_ip_address` | Ràng buộc địa chỉ IP. Xem [Tài liệu về máy chủ API](rest-api.md) để biết thêm chi tiết. <br> **Loại dữ liệu:** IPv4
| `api_server.listen_port` | Cổng ràng buộc. Xem [Tài liệu về máy chủ API](rest-api.md) để biết thêm chi tiết. <br><br>**Loại dữ liệu:** Số nguyên từ 1024 đến 65535
| `api_server.verbosity` | Ghi nhật ký chi tiết. `info` sẽ in tất cả các Cuộc gọi RPC, trong khi "lỗi" sẽ chỉ hiển thị lỗi. <br><br>**Loại dữ liệu:** Enum, `thông tin` hoặc `lỗi`. Mặc định là `thông tin`.
| `api_server.tên người dùng` | Tên người dùng cho máy chủ API. Xem [Tài liệu về máy chủ API](rest-api.md) để biết thêm chi tiết. <br><br> **Giữ bí mật, không tiết lộ công khai.**<br> **Loại dữ liệu:** Chuỗi
| `api_server.password` | Mật khẩu cho máy chủ API. Xem [Tài liệu về máy chủ API](rest-api.md) để biết thêm chi tiết. <br><br> **Giữ bí mật, không tiết lộ công khai.**<br> **Loại dữ liệu:** Chuỗi
| `api_server.ws_token` | Mã thông báo API cho Message WebSocket. Xem [Tài liệu về máy chủ API](rest-api.md) để biết thêm chi tiết.  <br><br>**Giữ bí mật, không tiết lộ công khai.** <br> **Loại dữ liệu:** Chuỗi
| `tên_bot` | Tên của bot. Được chuyển qua API tới khách hàng - có thể được hiển thị để phân biệt / đặt tên cho bot.<br> *Mặc định là `freqtrade`*<br> **Datatype:** String
| `external_message_consumer` | Bật [Chế độ nhà sản xuất/người tiêu dùng](producer-consumer.md) để biết thêm chi tiết. <br> **Loại dữ liệu:** Lệnh
| | **Khác**
| `trạng thái ban đầu` | Xác định trạng thái ứng dụng ban đầu. Nếu được đặt thành dừng thì bot phải được khởi động rõ ràng thông qua lệnh `/start` RPC. <br>*Mặc định là `đã dừng`.* <br> **Loại dữ liệu:** Enum, `đang chạy`, `tạm dừng` hoặc `đã dừng`
| `buộc_entry_enable` | Cho phép các Lệnh RPC để buộc thực hiện Giao dịch. Thêm thông tin dưới đây. <br> **Loại dữ liệu:** Boolean
| `vô hiệu hóa_dataframe_checks` | Vô hiệu hóa việc kiểm tra tính chính xác của khung dữ liệu OHLCV được trả về từ các phương thức chiến lược. Chỉ sử dụng khi có chủ ý thay đổi khung dữ liệu và hiểu bạn đang làm gì. [Ghi đè chiến lược](#parameters-in-the-strategy).<br> *Mặc định là `False`*. <br> **Loại dữ liệu:** Boolean| `internals.process_throttle_secs` | Đặt mức điều tiết quy trình hoặc thời lượng vòng lặp tối thiểu cho một vòng lặp bot. Giá trị tính bằng giây. <br>*Mặc định là `5` giây.* <br> **Loại dữ liệu:** Số nguyên dương
| `internals.heartbeat_interval` | In tin nhắn nhịp tim mỗi N giây. Đặt thành 0 để tắt thông báo nhịp tim. <br>*Mặc định là `60` giây.* <br> **Loại dữ liệu:** Số nguyên dương hoặc 0
| `internals.sd_notify` | Cho phép sử dụng giao thức sd_notify để thông báo cho người quản lý dịch vụ systemd về những thay đổi trong trạng thái bot và đưa ra các ping duy trì. Xem [tại đây](advanced-setup.md#configure-the-bot-running-as-a-systemd-service) để biết thêm chi tiết. <br> **Loại dữ liệu:** Boolean
| `chiến lược` | **Bắt buộc** Xác định lớp Chiến lược để sử dụng. Nên đặt thông qua `--strategy NAME`. <br> **Loại dữ liệu:** Tên lớp
| `đường dẫn chiến lược` | Thêm đường dẫn tra cứu chiến lược bổ sung (phải là một thư mục). <br> **Loại dữ liệu:** Chuỗi
| `đệ quy_chiến lược_tìm kiếm` | Đặt thành `true` để tìm kiếm đệ quy các thư mục con bên trong `user_data/strategies` cho một chiến lược. <br> **Loại dữ liệu:** Boolean
| `dữ liệu người dùng_dir` | Thư mục chứa dữ liệu người dùng. <br> *Mặc định là `./user_data/`*. <br> **Loại dữ liệu:** Chuỗi
| `db_url` | Khai báo URL cơ sở dữ liệu để sử dụng. LƯU Ý: Giá trị mặc định này là `sqlite:///tradesv3.dryrun.sqlite` nếu `dry_run` là `true` và là `sqlite:///tradesv3.sqlite` cho các phiên bản sản xuất. <br> **Datatype:** Chuỗi, chuỗi kết nối SQLAlchemy
| `tệp nhật ký` | Chỉ định tên logfile. Sử dụng chiến lược cuộn để xoay tệp nhật ký cho 10 tệp với giới hạn 1 MB cho mỗi tệp. <br> **Loại dữ liệu:** Chuỗi
| `add_config_files` | Các tập tin cấu hình bổ sung. Các tệp này sẽ được tải và hợp nhất với tệp cấu hình hiện tại. Các tệp được phân giải tương ứng với tệp ban đầu.<br> *Mặc định là `[]`*. <br> **Loại dữ liệu:** Danh sách các chuỗi
| `dataformat_ohlcv` | Định dạng dữ liệu được sử dụng để lưu trữ dữ liệu lịch sử nến (OHLCV). <br> *Mặc định là `lông`*. <br> **Loại dữ liệu:** Chuỗi
| `dataformat_trades` | Định dạng dữ liệu để sử dụng để lưu trữ dữ liệu giao dịch lịch sử. <br> *Mặc định là `lông`*. <br> **Loại dữ liệu:** Chuỗi
| `reduce_df_footprint` | Viết lại tất cả các cột số thành float32/int32, với mục tiêu giảm mức sử dụng ram/đĩa (và giảm backtesting/hyperopt và trong FreqAI). <br> Mặc định: `Sai`. <br> **Loại dữ liệu:** Boolean.
| `log_config` | Từ điển chứa cấu hình nhật ký để ghi nhật ký python. [thông tin thêm](advanced-setup.md#advanced-logging) <br> Mặc định: `FtRichHandler` <br> **Datatype:** dict.

### Các thông số trong chiến lược

Các tham số sau có thể được đặt trong tệp cấu hình hoặc chiến lược.
Các giá trị được đặt trong tệp cấu hình luôn ghi đè các giá trị được đặt trong chiến lược.* `minimal_roi`
* `timeframe`
* `stoploss`
* `max_open_trades`
* `trailing_stop`
* `trailing_stop_positive`
* `trailing_stop_positive_offset`
* `trailing_only_offset_is_reached`
* `use_custom_stoploss`
* `process_only_new_candles`
* `order_types`
* `order_time_in_force`
* `unfilledtimeout`
* `disable_dataframe_checks`
* `use_exit_signal`
* `exit_profit_only`
* `exit_profit_offset`
* `ignore_roi_if_entry_signal`
* `ignore_buying_expired_candle_after`
* `position_adjustment_enable`
* `max_entry_position_adjustment`
### Định cấu hình số tiền trên mỗi giao dịch

Có một số phương pháp để định cấu hình số tiền đặt cược mà bot sẽ sử dụng để tham gia giao dịch. Tất cả các phương pháp đều tôn trọng [cấu hình số dư khả dụng](#tradable-balance) như được giải thích bên dưới.

#### Cổ phần giao dịch tối thiểu

Số tiền đặt cược tối thiểu sẽ phụ thuộc vào trao đổi và cặp và thường được liệt kê trong các trang hỗ trợ trao đổi.

Giả sử số tiền có thể giao dịch tối thiểu cho XRP/USD là 20 XRP (do sàn giao dịch đưa ra) và giá là 0,6\$, số tiền đặt cược tối thiểu để mua cặp này là `20 * 0,6 ~= 12`.
Sàn giao dịch này cũng có giới hạn đối với USD - trong đó tất cả các đơn đặt hàng phải > 10\$ - tuy nhiên điều này không áp dụng trong trường hợp này.

Để đảm bảo thực hiện an toàn, freqtrade sẽ không cho phép mua với số tiền đặt cược là 10,1\$, thay vào đó, nó sẽ đảm bảo rằng có đủ không gian để đặt mức dừng lỗ bên dưới cặp (+ phần bù, được xác định bởi `amount_reserve_percent`, mặc định là 5%).

Với mức dự trữ là 5%, số tiền đặt cược tối thiểu sẽ là ~12,6\$ (`12 * (1 + 0,05)`). Nếu chúng ta tính đến mức dừng lỗ 10% trên đó - chúng ta sẽ có giá trị ~14\$ (`12,6 / (1 - 0,1)`).

Để hạn chế tính toán này trong trường hợp giá trị dừng lỗ lớn, giới hạn tiền đặt cược tối thiểu được tính toán sẽ không bao giờ cao hơn 50% so với giới hạn thực.

!!! Cảnh báo
    Vì giới hạn trên các sàn giao dịch thường ổn định và không được cập nhật thường xuyên nên một số cặp có thể hiển thị giới hạn tối thiểu khá cao, đơn giản vì giá đã tăng lên rất nhiều kể từ lần điều chỉnh giới hạn cuối cùng của sàn giao dịch. Freqtrade điều chỉnh số tiền đặt cược theo giá trị này, trừ khi nó lớn hơn > 30% so với số tiền đặt cược được tính toán/mong muốn - trong trường hợp đó giao dịch bị từ chối.

#### Ví chạy khô

Khi chạy ở chế độ chạy khô, bot sẽ sử dụng ví mô phỏng để thực hiện giao dịch. Số dư ban đầu của ví này được xác định bởi `dry_run_wallet` (mặc định là 1000).
Đối với các trường hợp phức tạp hơn, bạn cũng có thể gán từ điển cho `dry_run_wallet` để xác định số dư ban đầu cho từng loại tiền tệ.```json
"dry_run_wallet": {
    "BTC": 0.01,
    "ETH": 2,
    "USDT": 1000
}
```Tùy chọn dòng lệnh (`--dry-run-wallet`) có thể được sử dụng để ghi đè giá trị cấu hình, nhưng chỉ cho giá trị float, không phải cho từ điển. Nếu bạn muốn sử dụng từ điển, vui lòng điều chỉnh tệp cấu hình.

!!! Lưu ý
    Số dư không phải bằng tiền tệ đặt cược sẽ không được sử dụng để giao dịch nhưng được hiển thị như một phần của số dư trên ví.
    Trên các sàn giao dịch ký quỹ chéo, số dư ví có thể được sử dụng để tính toán tài sản thế chấp có sẵn cho giao dịch.

#### Số dư có thể giao dịch

Theo mặc định, bot giả định rằng `số tiền hoàn chỉnh - 1%` thuộc quyền sử dụng của nó và khi sử dụng [số tiền đặt cược động](#dynamic-stake-amount), nó sẽ chia toàn bộ số dư thành các nhóm `max_open_trades` cho mỗi giao dịch.
Freqtrade sẽ dành 1% cho các khoản phí cuối cùng khi tham gia giao dịch và do đó sẽ không chạm vào khoản phí đó theo mặc định.

Bạn có thể định cấu hình số tiền "chưa được chạm tới" bằng cách sử dụng cài đặt `tradable_balance_ratio`.

Ví dụ: nếu bạn có sẵn 10 ETH trong ví của mình trên sàn giao dịch và `tradable_balance_ratio=0,5` (là 50%), thì bot sẽ sử dụng số tiền tối đa là 5 ETH để giao dịch và coi đây là số dư khả dụng. Phần còn lại của ví không bị ảnh hưởng bởi các giao dịch.

!!! Nguy hiểm
    **Không** được sử dụng cài đặt này khi chạy nhiều bot trên cùng một tài khoản. Thay vào đó, vui lòng xem [Vốn khả dụng cho bot](#sign-available-capital).

!!! Cảnh báo
    Cài đặt `tradable_balance_ratio` áp dụng cho số dư hiện tại (số dư tự do + bị ràng buộc trong giao dịch). Do đó, giả sử số dư ban đầu là 1000, cấu hình có `tradable_balance_ratio=0,99` sẽ không đảm bảo rằng 10 đơn vị tiền tệ sẽ luôn có sẵn trên sàn giao dịch. Ví dụ: số tiền miễn phí có thể giảm xuống còn 5 đơn vị nếu tổng số dư giảm xuống 500 (do thua hoặc rút số dư).

#### Chỉ định vốn khả dụng

Để tận dụng tối đa lợi nhuận gộp khi sử dụng nhiều bot trên cùng một tài khoản trao đổi, bạn sẽ muốn giới hạn mỗi bot ở một số dư ban đầu nhất định.
Điều này có thể được thực hiện bằng cách đặt `available_capital` thành số dư ban đầu mong muốn.

Giả sử tài khoản của bạn có 10000 USDT và bạn muốn chạy 2 chiến lược khác nhau trên sàn giao dịch này.
Bạn sẽ đặt `available_capital=5000` - cấp cho mỗi bot số vốn ban đầu là 5000 USDT.
Sau đó, bot sẽ chia đều số dư ban đầu này thành các nhóm `max_open_trades`.
Các giao dịch có lợi nhuận sẽ dẫn đến tăng quy mô đặt cược cho bot này - mà không ảnh hưởng đến quy mô đặt cược của bot kia.

Việc điều chỉnh `available_capital` yêu cầu tải lại cấu hình để có hiệu lực. Việc điều chỉnh `available_capital` sẽ thêm sự khác biệt giữa `available_capital` trước đó và `available_capital` mới. Giảm vốn khả dụng khi giao dịch được mở không thoát khỏi giao dịch. Khoản chênh lệch sẽ được trả lại vào ví khi giao dịch kết thúc. Kết quả của việc này khác nhau tùy thuộc vào biến động giá giữa thời điểm điều chỉnh và thoát giao dịch.

!!! Cảnh báo "Không tương thích với `tradable_balance_ratio`"
    Việc đặt tùy chọn này sẽ thay thế mọi cấu hình của `tradable_balance_ratio`.

#### Sửa đổi số tiền đặt cược cuối cùng

Giả sử chúng ta có số dư có thể giao dịch là 1000 USDT, `stake_amount=400` và `max_open_trades=3`.
Bot sẽ mở 2 giao dịch và sẽ không thể lấp đầy vị trí giao dịch cuối cùng vì 400 USDT được yêu cầu không còn nữa vì 800 USDT đã được gắn vào các giao dịch khác.Để khắc phục điều này, tùy chọn `amend_last_stake_amount` có thể được đặt thành `True`, điều này sẽ cho phép bot giảm số tiền stake_amount xuống số dư khả dụng để lấp đầy vị trí giao dịch cuối cùng.

Trong ví dụ trên, điều này có nghĩa là:

* Giao dịch 1: 400 USDT
* Giao dịch 2: 400 USDT
* Giao dịch 3: 200 USDT

!!! Lưu ý
    Tùy chọn này chỉ áp dụng với [Số tiền đặt cược tĩnh](#static-stake-amount) - vì [Số tiền đặt cược động](#dynamic-stake-amount) chia đều số dư.

!!! Lưu ý
    Số tiền đặt cược cuối cùng tối thiểu có thể được định cấu hình bằng cách sử dụng `last_stake_amount_min_ratio` - mặc định là 0,5 (50%). Điều này có nghĩa là số tiền đặt cược tối thiểu từng được sử dụng là `stake_amount * 0,5`. Điều này tránh số tiền đặt cược rất thấp, gần bằng số tiền có thể giao dịch tối thiểu cho cặp tiền và có thể bị sàn giao dịch từ chối.

#### Số tiền đặt cược tĩnh

Cấu hình `stake_amount` định cấu hình tĩnh số lượng tiền tệ đặt cược mà bot của bạn sẽ sử dụng cho mỗi giao dịch.

Giá trị cấu hình tối thiểu là 0,0001, tuy nhiên, vui lòng kiểm tra mức giao dịch tối thiểu trên sàn giao dịch của bạn để biết loại tiền đặt cược bạn đang sử dụng để tránh sự cố.

Cài đặt này hoạt động kết hợp với `max_open_trades`. Vốn tối đa tham gia vào các giao dịch là `stake_amount * max_open_trades`.
Ví dụ: bot sẽ sử dụng nhiều nhất (0,05 BTC x 3) = 0,15 BTC, giả sử cấu hình là `max_open_trades=3` và `stake_amount=0,05`.

!!! Lưu ý
    Cài đặt này tôn trọng [cấu hình số dư khả dụng](#tradable-balance).

#### Số tiền đặt cược động

Ngoài ra, bạn có thể sử dụng số tiền đặt cược động, số tiền này sẽ sử dụng số dư khả dụng trên sàn giao dịch và chia đều cho số lượng giao dịch được phép (`max_open_trades`).

Để định cấu hình điều này, hãy đặt `stake_amount="unlimited"`. Chúng tôi cũng khuyên bạn nên đặt `tradable_balance_ratio=0,99` (99%) - để giữ số dư tối thiểu cho các khoản phí cuối cùng.

Trong trường hợp này, số tiền giao dịch được tính như sau:```python
currency_balance / (max_open_trades - current_open_trades)
```Để cho phép bot giao dịch tất cả `stake_currency` có sẵn trong tài khoản của bạn (trừ `tradable_balance_ratio`) được đặt```json
"stake_amount" : "unlimited",
"tradable_balance_ratio": 0.99,
```!!! Mẹo "Lợi nhuận gộp"
    Cấu hình này sẽ cho phép tăng/giảm tiền đặt cược tùy thuộc vào hiệu suất của bot (đặt cược thấp hơn nếu bot thua, tiền đặt cược cao hơn nếu bot có thành tích thắng vì có số dư cao hơn) và sẽ dẫn đến lợi nhuận gộp.

!!! Lưu ý "Khi sử dụng Chế độ Dry-Run"
    Khi sử dụng `"stake_amount" : "không giới hạn",` kết hợp với Dry-Run, Backtesting hoặc Hyperopt, số dư sẽ được mô phỏng bắt đầu bằng số tiền đặt cược `dry_run_wallet` sẽ tăng lên.
    Do đó, điều quan trọng là phải đặt `dry_run_wallet` thành một giá trị hợp lý (chẳng hạn như 0,05 hoặc 0,01 đối với BTC và 1000 hoặc 100 đối với USDT), nếu không, nó có thể mô phỏng các giao dịch với 100 BTC (hoặc nhiều hơn) hoặc 0,05 USDT (hoặc ít hơn) cùng một lúc - có thể không tương ứng với số dư thực khả dụng của bạn hoặc nhỏ hơn giới hạn trao đổi tối thiểu đối với số tiền đặt hàng đối với loại tiền đặt cược.

#### Số tiền đặt cược động có điều chỉnh vị trí

Khi bạn muốn sử dụng điều chỉnh vị trí với số tiền đặt cược không giới hạn, bạn cũng phải triển khai `custom_stake_amount` để trả về một giá trị tùy thuộc vào chiến lược của bạn.
Giá trị thông thường sẽ nằm trong khoảng 25% - 50% số tiền đặt cược được đề xuất, nhưng phụ thuộc nhiều vào chiến lược của bạn và số tiền bạn muốn để lại trong ví làm bộ đệm điều chỉnh vị trí.

Ví dụ: nếu điều chỉnh vị thế của bạn giả định rằng nó có thể thực hiện thêm 2 lần mua với cùng số tiền đặt cược thì bộ đệm của bạn phải là 66,6667% số tiền đặt cược không giới hạn được đề xuất ban đầu.

Hoặc một ví dụ khác nếu việc điều chỉnh vị thế của bạn giả định rằng nó có thể thực hiện thêm 1 lần mua với số tiền gấp 3 lần số tiền đặt cược ban đầu thì `custom_stake_amount` sẽ trả lại 25% số tiền đặt cược được đề xuất và để lại 75% cho những điều chỉnh vị trí có thể xảy ra sau này.

--8<-- "bao gồm/prices.md"

## Chi tiết cấu hình khác

### Hiểu tối thiểu_roi

Tham số cấu hình `minimal_roi` là một đối tượng JSON trong đó khóa là khoảng thời gian
tính bằng phút và giá trị là ROI tối thiểu theo tỷ lệ.
Xem ví dụ dưới đây:```json
"minimal_roi": {
    "40": 0.0,    # Exit after 40 minutes if the profit is not negative
    "30": 0.01,   # Exit after 30 minutes if there is at least 1% profit
    "20": 0.02,   # Exit after 20 minutes if there is at least 2% profit
    "0":  0.04    # Exit immediately if there is at least 4% profit
},
```Hầu hết các tệp chiến lược đều đã bao gồm giá trị `minimal_roi` tối ưu.
Tham số này có thể được đặt trong tệp Chiến lược hoặc Cấu hình. Nếu bạn sử dụng nó trong tập tin cấu hình, nó sẽ ghi đè lên
giá trị `minimal_roi` từ tệp chiến lược.
Nếu nó không được đặt trong Chiến lược hoặc Cấu hình, thì giá trị mặc định là 1000% `{"0": 10}` sẽ được sử dụng và ROI tối thiểu sẽ bị vô hiệu hóa trừ khi giao dịch của bạn tạo ra lợi nhuận 1000%.

!!! Lưu ý "Trường hợp đặc biệt buộc phải thoát sau một thời gian cụ thể"
    Một trường hợp đặc biệt sử dụng `"<N>": -1` làm ROI. Điều này buộc bot phải thoát giao dịch sau N Phút, bất kể giao dịch đó là tích cực hay tiêu cực, do đó thể hiện lệnh thoát bắt buộc có giới hạn thời gian.

### Hiểu Force_entry_enable

Tham số cấu hình `force_entry_enable` cho phép sử dụng các lệnh buộc nhập (`/forcelong`, `/forceshort`) thông qua Telegram và API REST.
Vì lý do bảo mật, tính năng này bị tắt theo mặc định và freqtrade sẽ hiển thị thông báo cảnh báo khi khởi động nếu được bật.
Ví dụ: bạn có thể gửi `/forceenter ETH/BTC` tới bot, điều này sẽ dẫn đến việc freqtrade mua cặp này và giữ nó cho đến khi tín hiệu thoát thông thường (ROI, stoploss, /forceexit) xuất hiện.

Điều này có thể nguy hiểm với một số chiến lược, vì vậy hãy cẩn thận khi sử dụng.

Xem [tài liệu telegram](telegram-usage.md) để biết chi tiết về cách sử dụng.

### Bỏ qua nến hết hạn

Khi làm việc với các khung thời gian lớn hơn (ví dụ: 1 giờ trở lên) và sử dụng giá trị `max_open_trades` thấp, nến cuối cùng có thể được xử lý ngay khi có vị trí giao dịch. Khi xử lý cây nến cuối cùng, điều này có thể dẫn đến tình huống không nên sử dụng tín hiệu mua trên cây nến đó. Ví dụ: khi sử dụng một điều kiện trong chiến lược mà bạn sử dụng điểm chéo, điểm đó có thể đã trôi qua quá lâu để bạn có thể bắt đầu giao dịch trên đó.

Trong những trường hợp này, bạn có thể bật chức năng bỏ qua các nến vượt quá khoảng thời gian được chỉ định bằng cách đặt `ignore_buying_expired_candle_after` thành số dương, cho biết số giây sau đó tín hiệu mua sẽ hết hạn.

Ví dụ: nếu chiến lược của bạn đang sử dụng khung thời gian 1 giờ và bạn chỉ muốn mua trong vòng 5 phút đầu tiên khi có nến mới xuất hiện, bạn có thể thêm cấu hình sau vào chiến lược của mình:``` json
  {
    //...
    "ignore_buying_expired_candle_after": 300,
    // ...
  }
```!!! Lưu ý
    Cài đặt này sẽ đặt lại với mỗi cây nến mới, do đó, nó sẽ không ngăn các tín hiệu cố định thực thi trên cây nến thứ 2 hoặc thứ 3 mà chúng đang hoạt động. Tốt nhất hãy sử dụng bộ chọn "kích hoạt" cho tín hiệu mua, tín hiệu này chỉ hoạt động đối với một nến.

### Hiểu loại_đơn hàng

Tham số cấu hình `order_types` ánh xạ các hành động (`entry`, `exit`, `stoploss`, `emergency_exit`, `force_exit`, `force_entry`) thành các loại đơn đặt hàng (`market`, `limit`, ...) cũng như định cấu hình mức dừng lỗ trên sàn giao dịch và xác định mức dừng lỗ trên khoảng thời gian cập nhật sàn giao dịch tính bằng giây.

Điều này cho phép nhập lệnh bằng lệnh giới hạn, thoát bằng lệnh giới hạn và tạo điểm dừng bằng lệnh thị trường.
Nó cũng cho phép thiết lập
lệnh dừng lỗ "trên sàn giao dịch" có nghĩa là lệnh dừng lỗ sẽ được đặt ngay lập tức sau khi lệnh mua được thực hiện.

`order_types` được đặt trong tệp cấu hình sẽ ghi đè toàn bộ các giá trị được đặt trong chiến lược, vì vậy bạn cần định cấu hình toàn bộ từ điển `order_types` ở một nơi.

Nếu điều này được định cấu hình thì cần phải có 4 giá trị sau (`entry`, `exit`, `stoploss` và `stoploss_on_exchange`), nếu không, bot sẽ không khởi động được.

Để biết thông tin về (`emergency_exit`,`force_exit`, `force_entry`, `stoploss_on_exchange`,`stoploss_on_exchange_interval`,`stoploss_on_exchange_limit_ratio`) vui lòng xem tài liệu dừng lỗ [dừng lỗ khi trao đổi](stoploss.md)

Cú pháp cho chiến lược:```python
order_types = {
    "entry": "limit",
    "exit": "limit",
    "emergency_exit": "market",
    "force_entry": "market",
    "force_exit": "market",
    "stoploss": "market",
    "stoploss_on_exchange": False,
    "stoploss_on_exchange_interval": 60,
    "stoploss_on_exchange_limit_ratio": 0.99,
}
```Cấu hình:```json
"order_types": {
    "entry": "limit",
    "exit": "limit",
    "emergency_exit": "market",
    "force_entry": "market",
    "force_exit": "market",
    "stoploss": "market",
    "stoploss_on_exchange": false,
    "stoploss_on_exchange_interval": 60
}
```!!! Lưu ý "Hỗ trợ lệnh thị trường"
    Không phải tất cả các sàn giao dịch đều hỗ trợ lệnh "thị trường".
    Thông báo sau sẽ được hiển thị nếu sàn giao dịch của bạn không hỗ trợ lệnh thị trường:
    `"Exchange <yourexchange> không hỗ trợ các lệnh thị trường."` và bot sẽ từ chối bắt đầu.

!!! Cảnh báo “Sử dụng lệnh thị trường”
    Vui lòng đọc kỹ phần [Định giá lệnh thị trường](#giá lệnh thị trường) khi sử dụng lệnh thị trường.

!!! Lưu ý "Dừng lỗ khi trao đổi"
    `order_types.stoploss_on_exchange_interval` không bắt buộc. Đừng thay đổi giá trị của nó nếu bạn
    không chắc chắn về việc bạn đang làm. Để biết thêm thông tin về cách hoạt động của lệnh dừng lỗ, vui lòng
    tham khảo [tài liệu về điểm dừng lỗ](stoploss.md).

    Nếu `order_types.stoploss_on_exchange` được bật và lệnh dừng lỗ được hủy thủ công trên sàn giao dịch thì bot sẽ tạo một lệnh dừng lỗ mới.

!!! Cảnh báo "Cảnh báo: lỗi order_types.stoploss_on_exchange"
    Nếu vì lý do nào đó, việc dừng lỗ khi tạo sàn giao dịch không thành công thì "thoát khẩn cấp" sẽ được bắt đầu. Theo mặc định, thao tác này sẽ thoát giao dịch bằng lệnh thị trường. Loại lệnh cho thoát khẩn cấp có thể được thay đổi bằng cách đặt giá trị `emergency_exit` trong từ điển `order_types` - tuy nhiên, điều này không được khuyến khích.

### Hiểu order_time_in_force

Tham số cấu hình `order_time_in_force` xác định chính sách mà lệnh được thực thi trên sàn giao dịch.  
Thời gian có hiệu lực thường được sử dụng là:

**GTC (Tốt cho đến khi bị hủy):**

Đây hầu hết là thời gian mặc định có hiệu lực. Điều đó có nghĩa là đơn hàng sẽ vẫn được trao đổi cho đến khi người dùng hủy. Nó có thể được thực hiện đầy đủ hoặc một phần. Nếu hoàn thành một phần, phần còn lại sẽ ở lại sàn giao dịch cho đến khi bị hủy.

**FOK (Điền hoặc tiêu diệt):**

Điều đó có nghĩa là nếu lệnh không được thực hiện ngay lập tức VÀ đầy đủ thì lệnh đó sẽ bị sàn giao dịch hủy bỏ.

**IOC (Ngay lập tức hoặc Đã hủy):**

Nó giống như FOK (ở trên) ngoại trừ nó có thể được đáp ứng một phần. Phần còn lại sẽ tự động bị sàn giao dịch hủy bỏ.

Không nhất thiết phải được khuyến nghị vì điều này có thể dẫn đến khớp lệnh một phần dưới quy mô giao dịch tối thiểu.

**PO (Chỉ đăng):**

Chỉ đăng đơn đặt hàng. Đơn đặt hàng được đặt dưới dạng đơn đặt hàng của nhà sản xuất hoặc bị hủy.
Điều này có nghĩa là đơn hàng phải được đặt trên sổ đặt hàng ít nhất một thời gian ở trạng thái chưa được thực hiện.

Vui lòng kiểm tra [Tài liệu trao đổi](exchanges.md) để biết các giá trị thời gian có hiệu lực được hỗ trợ cho hoạt động trao đổi của bạn.

#### cấu hình time_in_force

Tham số `order_time_in_force` chứa một lệnh có thời gian vào và ra trong các giá trị chính sách bắt buộc.
Điều này có thể được đặt trong tệp cấu hình hoặc trong chiến lược.
Các giá trị được đặt trong tệp cấu hình sẽ ghi đè các giá trị trong chiến lược, tuân theo [quy tắc ưu tiên](#configuration-option-prevalence) thông thường.

Các giá trị có thể là: `GTC` (mặc định), `FOK` hoặc `IOC`.``` python
"order_time_in_force": {
    "entry": "GTC",
    "exit": "GTC"
},
```!!! Cảnh báo
    Vui lòng không thay đổi giá trị mặc định trừ khi bạn biết mình đang làm gì và đã nghiên cứu tác động của việc sử dụng các giá trị khác nhau cho trao đổi cụ thể của mình.


### Chuyển đổi tiền pháp định

Freqtrade sử dụng API Coingecko để chuyển đổi giá trị đồng xu thành giá trị tiền pháp định tương ứng cho các báo cáo của Telegram.
Loại tiền FIAT có thể được đặt trong tệp cấu hình là `fiat_display_currency`.

Việc xóa hoàn toàn `fiat_display_currency` khỏi cấu hình sẽ bỏ qua việc khởi tạo coingecko và sẽ không hiển thị bất kỳ chuyển đổi tiền tệ FIAT nào. Điều này không có tầm quan trọng đối với hoạt động chính xác của bot.

#### Những giá trị nào có thể được sử dụng cho fiat_display_currency?

Tham số cấu hình `fiat_display_currency` đặt loại tiền cơ sở sẽ sử dụng cho
chuyển đổi từ tiền xu sang tiền pháp định trong báo cáo của bot Telegram.

Các giá trị hợp lệ là:```json
"AUD", "BRL", "CAD", "CHF", "CLP", "CNY", "CZK", "DKK", "EUR", "GBP", "HKD", "HUF", "IDR", "ILS", "INR", "JPY", "KRW", "MXN", "MYR", "NOK", "NZD", "PHP", "PKR", "PLN", "RUB", "SEK", "SGD", "THB", "TRY", "TWD", "ZAR", "USD"
```Ngoài các loại tiền tệ fiat, một loạt các loại tiền điện tử được hỗ trợ.

Các giá trị hợp lệ là:```json
"BTC", "ETH", "XRP", "LTC", "BCH", "BNB"
```#### Vấn đề về giới hạn tỷ giá của Coingecko

Trên một số dải IP, coingecko bị giới hạn tỷ lệ rất nhiều.
Trong những trường hợp như vậy, bạn có thể muốn thêm khóa API coinecko của mình vào cấu hình.``` json
{
    "fiat_display_currency": "USD",
    "coingecko": {
        "api_key": "your-api",
        "is_demo": true
    }
}
```Freqtrade hỗ trợ cả khóa API Demo và Pro coinecko.

Khóa API Coingecko KHÔNG cần thiết để bot hoạt động chính xác.
Nó chỉ được sử dụng để chuyển đổi tiền xu sang tiền pháp định trong các báo cáo Telegram, thường hoạt động mà không cần khóa API.

## Tiêu thụ Websockets trao đổi

Freqtrade có thể sử dụng ổ cắm web thông qua ccxt.pro.

Freqtrade nhằm mục đích đảm bảo dữ liệu luôn có sẵn.
Nếu kết nối websocket không thành công (hoặc bị vô hiệu hóa), bot sẽ quay trở lại các lệnh gọi API REST.

Nếu bạn gặp sự cố mà bạn nghi ngờ là do websockets gây ra, bạn có thể tắt các sự cố này thông qua cài đặt `exchange.enable_ws`, cài đặt này mặc định là true.```jsonc
"exchange": {
    // ...
    "enable_ws": false,
    // ...
}
```Nếu bạn được yêu cầu sử dụng proxy, vui lòng tham khảo [phần proxy](#using-a-proxy-with-freqtrade) để biết thêm thông tin.

!!! Thông tin "Triển khai"
    Chúng tôi đang triển khai tính năng này một cách chậm rãi để đảm bảo tính ổn định cho bot của bạn.
    Hiện tại, việc sử dụng bị giới hạn ở các luồng dữ liệu ohlcv.
    Nó cũng bị giới hạn ở một số sàn giao dịch, với các sàn giao dịch mới được bổ sung liên tục.

## Sử dụng chế độ Chạy khô

Chúng tôi khuyên bạn nên khởi động bot ở chế độ Chạy khô để xem bot của bạn sẽ hoạt động như thế nào
hành xử và hiệu suất của chiến lược của bạn là gì. Ở chế độ Chạy khô,
bot không lấy tiền của bạn. Nó chỉ chạy mô phỏng trực tiếp mà không có
tạo ra các giao dịch trên sàn giao dịch.

1. Chỉnh sửa tệp cấu hình `config.json` của bạn.
2. Chuyển `dry-run` thành `true` và chỉ định `db_url` cho cơ sở dữ liệu lưu trữ lâu bền.```json
"dry_run": true,
"db_url": "sqlite:///tradesv3.dryrun.sqlite",
```3. Xóa khóa và bí mật API Exchange của bạn (thay đổi chúng bằng giá trị trống hoặc thông tin xác thực giả):```json
"exchange": {
    "name": "binance",
    "key": "key",
    "secret": "secret",
    ...
}
```Sau khi hài lòng với hiệu suất bot của mình chạy ở chế độ Chạy khô, bạn có thể chuyển nó sang chế độ sản xuất.

!!! Lưu ý
    Ví mô phỏng có sẵn trong chế độ chạy thử và sẽ có số vốn ban đầu là `dry_run_wallet` (mặc định là 1000).

### Những cân nhắc khi chạy thử

* Khóa API có thể được cung cấp hoặc không. Chỉ các hoạt động Chỉ đọc (tức là các hoạt động không làm thay đổi trạng thái tài khoản) trên sàn giao dịch mới được thực hiện ở chế độ chạy thử.
* Ví (`/balance`) được mô phỏng dựa trên `dry_run_wallet`.
* Đơn hàng được mô phỏng và sẽ không được đưa lên sàn giao dịch.
* Lệnh thị trường được thực hiện dựa trên khối lượng sổ đặt hàng tại thời điểm đặt lệnh, với độ trượt tối đa là 5%.
* Giới hạn các đơn đặt hàng được thực hiện khi giá đạt đến mức xác định - hoặc hết thời gian chờ dựa trên cài đặt `thời gian chờ chưa thực hiện`.
* Lệnh giới hạn sẽ được chuyển đổi thành lệnh thị trường nếu chúng vượt qua giá hơn 1% và sẽ được thực hiện ngay lập tức dựa trên các quy tắc lệnh thị trường thông thường (xem điểm về Lệnh thị trường ở trên).
* Kết hợp với `stoploss_on_exchange`, giá stop_loss được coi là đã được lấp đầy.
* Các lệnh mở (không phải giao dịch được lưu trữ trong cơ sở dữ liệu) được giữ mở sau khi bot khởi động lại, với giả định rằng chúng không được thực hiện khi ngoại tuyến.

## Chuyển sang chế độ sản xuất

Ở chế độ sản xuất, bot sẽ thu hút tiền của bạn. Hãy cẩn thận, vì một chiến lược sai lầm có thể khiến bạn mất hết tiền.
Hãy nhận biết những gì bạn đang làm khi chạy nó ở chế độ sản xuất.

Khi chuyển sang chế độ Sản xuất, vui lòng đảm bảo sử dụng cơ sở dữ liệu mới/khác để tránh các giao dịch chạy thử làm ảnh hưởng đến số tiền trao đổi của bạn và cuối cùng làm hỏng số liệu thống kê của bạn.

### Thiết lập tài khoản trao đổi của bạn

Bạn sẽ cần tạo Khóa API (thông thường bạn nhận được `khóa` và `bí mật`, một số sàn giao dịch yêu cầu `mật khẩu` bổ sung) từ trang web Exchange và bạn sẽ cần chèn khóa này vào các trường thích hợp trong cấu hình hoặc khi được lệnh `freqtrade new-config` yêu cầu.
Khóa API thường chỉ được yêu cầu cho giao dịch trực tiếp (giao dịch bằng tiền thật, bot chạy ở "chế độ sản xuất", thực hiện lệnh thực trên sàn giao dịch) và không bắt buộc đối với bot chạy ở chế độ chạy khô (mô phỏng giao dịch). Khi thiết lập bot ở chế độ chạy thử, bạn có thể điền các giá trị trống vào các trường này.

### Để chuyển bot của bạn sang chế độ sản xuất

**Chỉnh sửa tệp `config.json` của bạn.**

**Chuyển chế độ chạy thử thành sai và đừng quên điều chỉnh URL cơ sở dữ liệu của bạn nếu được đặt:**```json
"dry_run": false,
```**Chèn khóa API Exchange của bạn (thay đổi chúng bằng khóa API giả):**```json
{
    "exchange": {
        "name": "binance",
        "key": "af8ddd35195e9dc500b9a6f799f6f5c93d89193b",
        "secret": "08a9dc6db3d7b53e1acebd9275677f4b0a04f1a5",
        //"password": "", // Optional, not needed by all exchanges)
        // ...
    }
    //...
}
```Bạn cũng nên đảm bảo đọc phần [Exchanges](exchanges.md) trong tài liệu để biết chi tiết cấu hình tiềm năng cụ thể cho sàn giao dịch của bạn.

!!! Gợi ý "Hãy giữ bí mật của bạn"
    Để giữ bí mật bí mật của bạn, chúng tôi khuyên bạn nên sử dụng cấu hình thứ 2 cho khóa API của mình.
    Chỉ cần sử dụng đoạn mã trên trong tệp cấu hình mới (ví dụ: `config-private.json`) và giữ cài đặt của bạn trong tệp này.
    Sau đó, bạn có thể khởi động bot bằng `freqtrade Trade --config user_data/config.json --config user_data/config-private.json <...>` để tải khóa của bạn.

    **KHÔNG BAO GIỜ** chia sẻ tệp cấu hình riêng tư hoặc khóa trao đổi của bạn với bất kỳ ai!

## Sử dụng proxy với Freqtrade

Để sử dụng proxy với freqtrade, hãy xuất cài đặt proxy của bạn bằng cách sử dụng các biến `"HTTP_PROXY"` và `"HTTPS_PROXY"` được đặt thành các giá trị thích hợp.
Điều này sẽ áp dụng cài đặt proxy cho mọi thứ (telegram, coinecko, ...) **ngoại trừ** cho các yêu cầu trao đổi.``` bash
export HTTP_PROXY="http://addr:port"
export HTTPS_PROXY="http://addr:port"
freqtrade
```### Yêu cầu trao đổi proxy

Để sử dụng proxy cho các kết nối trao đổi - bạn sẽ phải xác định proxy như một phần của cấu hình ccxt.``` json
{ 
  "exchange": {
    "ccxt_config": {
      "httpsProxy": "http://addr:port",
      "wsProxy": "http://addr:port",
    }
  }
}
```For more information on available proxy types, please consult the [ccxt proxy documentation](https://docs.ccxt.com/#/README?id=proxy).
## Bước tiếp theo

Bây giờ bạn đã định cấu hình config.json của mình, bước tiếp theo là [khởi động bot của bạn](bot-usage.md).