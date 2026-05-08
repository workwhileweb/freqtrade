<!-- Auto-translated from docs/ by script. Please review technical terms. -->

# Tải xuống dữ liệu

## Lấy dữ liệu để backtesting và hyperopt

Để tải xuống dữ liệu (nến / OHLCV) cần thiết cho việc kiểm tra ngược và tối ưu hóa cao độ, hãy sử dụng lệnh `freqtrade download-data`.

Nếu không có tham số bổ sung nào được chỉ định, freqtrade sẽ tải xuống dữ liệu cho các khung thời gian `"1m"` và `"5m"` trong 30 ngày qua.
Trao đổi và các cặp sẽ đến từ `config.json` (nếu được chỉ định bằng `-c/--config`).
Nếu không cung cấp cấu hình, `--exchange` sẽ trở thành bắt buộc.

Bạn có thể sử dụng phạm vi thời gian tương đối (`--days 20`) hoặc điểm bắt đầu tuyệt đối (`--timerange 20200101-`). Đối với lượt tải xuống tăng dần, nên sử dụng phương pháp tương đối.

!!! Mẹo "Mẹo: Cập nhật dữ liệu hiện có"
    Nếu bạn đã có sẵn dữ liệu kiểm tra ngược trong thư mục dữ liệu của mình và muốn làm mới dữ liệu này cho đến ngày hôm nay, freqtrade sẽ tự động tính toán khoảng thời gian còn thiếu cho các cặp hiện có và quá trình tải xuống sẽ diễn ra từ thời điểm có sẵn mới nhất cho đến "bây giờ", không yêu cầu tham số `--days` hoặc `--timerange`. Freqtrade sẽ giữ lại dữ liệu có sẵn và chỉ tải xuống dữ liệu còn thiếu.  
    Nếu bạn đang cập nhật dữ liệu hiện có sau khi chèn các cặp mới mà bạn không có dữ liệu, hãy sử dụng tham số `--new-pairs-days xx`. Số ngày được chỉ định sẽ được tải xuống cho các cặp mới trong khi các cặp cũ sẽ chỉ được cập nhật với dữ liệu bị thiếu.  

### Cách sử dụng

--8<-- "lệnh/download-data.md"

!!! Mẹo "Tải xuống tất cả dữ liệu cho một loại tiền định giá"
    Thông thường, bạn sẽ muốn tải xuống dữ liệu cho tất cả các cặp tiền tệ định giá cụ thể. Trong những trường hợp như vậy, bạn có thể sử dụng cách viết tắt sau:
    `dữ liệu tải xuống freqtrade --exchange binance --pairs ".*/USDT" <...>`. Chuỗi "cặp" được cung cấp sẽ được mở rộng để chứa tất cả các cặp hoạt động trên sàn giao dịch.
    Để tải xuống dữ liệu cho các cặp không hoạt động (đã xóa), hãy thêm `--include-inactive-pairs` vào lệnh.

!!! Lưu ý "Giai đoạn khởi động"
    `download-data` là một lệnh độc lập với chiến lược. Ý tưởng là tải xuống một lượng lớn dữ liệu một lần, sau đó tăng dần lượng dữ liệu được lưu trữ.

    Vì lý do đó, `download-data` không quan tâm đến "giai đoạn khởi động" được xác định trong chiến lược. Người dùng có quyền tải xuống thêm ngày nếu quá trình kiểm tra ngược bắt đầu tại một thời điểm cụ thể (đồng thời tôn trọng khoảng thời gian khởi động).

### Bắt đầu tải xuống

Một lệnh rất đơn giản (giả sử có sẵn tệp `config.json`) có thể trông như sau.```bash
freqtrade download-data --exchange binance
```Thao tác này sẽ tải xuống dữ liệu nến lịch sử (OHLCV) cho tất cả các cặp tiền tệ được xác định trong cấu hình.

Ngoài ra, chỉ định các cặp trực tiếp```bash
freqtrade download-data --exchange binance --pairs ETH/USDT XRP/USDT BTC/USDT
```hoặc dưới dạng biểu thức chính quy (trong trường hợp này là để tải xuống tất cả các cặp USDT đang hoạt động)```bash
freqtrade download-data --exchange binance --pairs ".*/USDT"
```### Ghi chú khác

* Để sử dụng một thư mục khác với mặc định cụ thể của sàn giao dịch, hãy sử dụng `--datadir user_data/data/some_directory`.
* Để thay đổi sàn giao dịch được sử dụng để tải xuống dữ liệu lịch sử từ đó, hãy sử dụng `--exchange <exchange>` - hoặc chỉ định một tệp cấu hình khác.
* Để sử dụng `pairs.json` từ một số thư mục khác, hãy sử dụng `--pairs-file some_other_dir/pairs.json`.
* Để tải xuống dữ liệu lịch sử nến (OHLCV) chỉ trong 10 ngày, hãy sử dụng `--days 10` (mặc định là 30 ngày).
* Để tải xuống dữ liệu lịch sử nến (OHLCV) từ điểm bắt đầu cố định, hãy sử dụng `--timerange 20200101-` - sẽ tải xuống tất cả dữ liệu từ ngày 1 tháng 1 năm 2020.
* Điểm bắt đầu đã cho sẽ bị bỏ qua nếu dữ liệu đã có sẵn, chỉ tải xuống dữ liệu còn thiếu cho đến ngày hôm nay.
* Sử dụng `--timeframes` để chỉ định khung thời gian nào tải xuống dữ liệu nến lịch sử (OHLCV). Mặc định là `--timeframes 1m 5m` sẽ tải xuống dữ liệu 1 phút và 5 phút.
* Để sử dụng trao đổi, khung thời gian và danh sách các cặp như được xác định trong tệp cấu hình của bạn, hãy sử dụng tùy chọn `-c/--config`. Với điều này, tập lệnh sử dụng danh sách trắng được xác định trong cấu hình làm danh sách các cặp tiền tệ để tải xuống dữ liệu và không yêu cầu tệp pair.json. Bạn có thể kết hợp `-c/--config` với hầu hết các tùy chọn khác.
* Khi tải xuống dữ liệu hợp đồng tương lai (`--giao dịch hợp đồng tương lai ở chế độ giao dịch` hoặc cấu hình chỉ định chế độ tương lai), freqtrade sẽ tự động tải xuống các loại nến cần thiết (ví dụ: nến `mark` và `funding_rate`) trừ khi được chỉ định khác thông qua `--candle-types`.

??? Lưu ý "Lỗi từ chối quyền"
    Nếu thư mục cấu hình `user_data` của bạn được tạo bởi docker, bạn có thể gặp lỗi sau:```
    cp: cannot create regular file 'user_data/data/binance/pairs.json': Permission denied
    ```Bạn có thể sửa các quyền của thư mục dữ liệu người dùng của mình như sau:```
    sudo chown -R $UID:$GID user_data
    ```### Tải xuống dữ liệu bổ sung trước khoảng thời gian hiện tại

Giả sử bạn đã tải xuống tất cả dữ liệu từ năm 2022 (`--timerange 20220101-`) - nhưng bây giờ bạn cũng muốn kiểm tra lại dữ liệu trước đó.
Bạn có thể làm như vậy bằng cách sử dụng cờ `--prepend`, kết hợp với `--timerange` - chỉ định ngày kết thúc.``` bash
freqtrade download-data --exchange binance --pairs ETH/USDT XRP/USDT BTC/USDT --prepend --timerange 20210101-20220101
```!!! Lưu ý
    Freqtrade sẽ bỏ qua ngày kết thúc ở chế độ này nếu có dữ liệu, cập nhật ngày kết thúc thành điểm bắt đầu dữ liệu hiện có.

### Định dạng dữ liệu

Freqtrade hiện hỗ trợ các định dạng dữ liệu sau:

* `feather` - một định dạng dữ liệu dựa trên Apache Arrow
* `json` - tập tin json "văn bản" đơn giản
* `jsongz` - phiên bản nén bằng gzip của tệp json
* `parquet` - kho dữ liệu dạng cột (chỉ OHLCV)

Theo mặc định, cả dữ liệu OHLCV và dữ liệu giao dịch đều được lưu trữ ở định dạng `lông`.

Điều này có thể được thay đổi thông qua các đối số dòng lệnh `--data-format-ohlcv` và `--data-format-trades` tương ứng.
Để duy trì thay đổi này, bạn cũng nên thêm đoạn mã sau vào cấu hình của mình để không phải chèn các đối số trên mỗi lần:``` jsonc
    // ...
    "dataformat_ohlcv": "feather",
    "dataformat_trades": "feather",
    // ...
```Nếu định dạng dữ liệu mặc định đã bị thay đổi trong quá trình tải xuống thì các khóa `dataformat_ohlcv` và `dataformat_trades` trong tệp cấu hình cũng cần được điều chỉnh theo định dạng dữ liệu đã chọn.

!!! Lưu ý
    Bạn có thể chuyển đổi giữa các định dạng dữ liệu bằng cách sử dụng phương thức [convert-data](#sub-command-convert-data) và [convert-trade-data](#sub-command-convert-trade-data).

####So sánh định dạng dữ liệu

Các so sánh sau đây đã được thực hiện với dữ liệu sau và bằng cách sử dụng lệnh `time` linux.```
Found 6 pair / timeframe combinations.
+----------+-------------+--------+---------------------+---------------------+
|     Pair |   Timeframe |   Type |                From |                  To |
|----------+-------------+--------+---------------------+---------------------|
| BTC/USDT |          5m |   spot | 2017-08-17 04:00:00 | 2022-09-13 19:25:00 |
| ETH/USDT |          1m |   spot | 2017-08-17 04:00:00 | 2022-09-13 19:26:00 |
| BTC/USDT |          1m |   spot | 2017-08-17 04:00:00 | 2022-09-13 19:30:00 |
| XRP/USDT |          5m |   spot | 2018-05-04 08:10:00 | 2022-09-13 19:15:00 |
| XRP/USDT |          1m |   spot | 2018-05-04 08:11:00 | 2022-09-13 19:22:00 |
| ETH/USDT |          5m |   spot | 2017-08-17 04:00:00 | 2022-09-13 19:20:00 |
+----------+-------------+--------+---------------------+---------------------+
```Việc tính thời gian đã được thực hiện một cách không khoa học lắm bằng lệnh sau, lệnh này buộc phải đọc dữ liệu vào bộ nhớ.``` bash
time freqtrade list-data --show-timerange --data-format-ohlcv <dataformat>
```|  Định dạng | Kích thước | thời gian |
|----------||-------------|-------------|
| `lông` | 72Mb | 3,5 giây |
| `json` | 149Mb | 25,6 giây |
| `jsongz` | 39Mb | 27 giây |
| `sàn gỗ` | 83Mb | 3,8 giây |

Kích thước đã được lấy từ tổ hợp giao ngay 1 triệu BTC/USDT trong khoảng thời gian được chỉ định ở trên.

Để có sự kết hợp giữa hiệu suất/kích thước tốt nhất, chúng tôi khuyên bạn nên sử dụng định dạng lông vũ hoặc sàn gỗ mặc định.

### Tệp cặp

Để thay thế cho danh sách trắng từ `config.json`, bạn có thể sử dụng tệp `pairs.json`.
Ví dụ: nếu bạn đang sử dụng Binance:

* tạo một thư mục `user_data/data/binance` và sao chép hoặc tạo tệp `pairs.json` trong thư mục đó.
* cập nhật tệp `pairs.json` để chứa các cặp tiền tệ bạn quan tâm.```bash
mkdir -p user_data/data/binance
touch user_data/data/binance/pairs.json
```Định dạng của tệp `pairs.json` là một danh sách json đơn giản.
Được phép trộn các loại tiền tệ đặt cược khác nhau đối với tệp này vì nó chỉ được sử dụng để tải xuống.``` json
[
    "ETH/BTC",
    "ETH/USDT",
    "BTC/USDT",
    "XRP/ETH"
]
```!!! Lưu ý
    Tệp `pairs.json` chỉ được sử dụng khi không tải cấu hình nào (ngầm bằng cách đặt tên hoặc thông qua cờ `--config`).
    Bạn có thể buộc sử dụng tệp này thông qua `--pairs-file pair.json` - tuy nhiên, chúng tôi khuyên bạn nên sử dụng danh sách cặp từ bên trong cấu hình, thông qua cài đặt `exchange.pair_whitelist` hoặc `pairs` trong cấu hình.

## Lệnh phụ chuyển đổi dữ liệu

--8<-- "lệnh/convert-data.md"

### Ví dụ chuyển đổi dữ liệu

Lệnh sau sẽ chuyển đổi tất cả dữ liệu nến (OHLCV) có sẵn trong `~/.freqtrade/data/binance` từ json sang jsongz, tiết kiệm dung lượng ổ đĩa trong quá trình này.
Nó cũng sẽ xóa các tệp dữ liệu json gốc (tham số `--erase`).``` bash
freqtrade convert-data --format-from json --format-to jsongz --datadir ~/.freqtrade/data/binance -t 5m 15m --erase
```## Lệnh phụ chuyển đổi dữ liệu giao dịch

--8<-- "lệnh/convert-trade-data.md"

### Ví dụ chuyển đổi giao dịch

Lệnh sau sẽ chuyển đổi tất cả dữ liệu giao dịch có sẵn trong `~/.freqtrade/data/kraken` từ jsongz sang json.
Nó cũng sẽ xóa các tệp dữ liệu jsong gốc (tham số `--erase`).``` bash
freqtrade convert-trade-data --format-from jsongz --format-to json --datadir ~/.freqtrade/data/kraken --erase
```## Lệnh phụ giao dịch với ohlcv

Khi bạn cần sử dụng `--dl-trades` (chỉ kraken) để tải xuống dữ liệu, việc chuyển đổi dữ liệu giao dịch sang dữ liệu ohlcv là bước cuối cùng.
Lệnh này sẽ cho phép bạn lặp lại bước cuối cùng này cho các khung thời gian bổ sung mà không cần tải lại dữ liệu.

--8<-- "lệnh/giao dịch-to-ohlcv.md"

### Ví dụ chuyển đổi từ giao dịch sang ohlcv``` bash
freqtrade trades-to-ohlcv --exchange kraken -t 5m 1h 1d --pairs BTC/EUR ETH/EUR
```## Dữ liệu danh sách lệnh phụ

Bạn có thể lấy danh sách dữ liệu đã tải xuống bằng lệnh phụ `list-data`.

--8<-- "lệnh/list-data.md"

### Dữ liệu danh sách ví dụ```bash
> freqtrade list-data --userdir ~/.freqtrade/user_data/

              Found 33 pair / timeframe combinations.
┏━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━┓
┃          Pair ┃                                 Timeframe ┃ Type ┃
┡━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━┩
│       ADA/BTC │     5m, 15m, 30m, 1h, 2h, 4h, 6h, 12h, 1d │ spot │
│       ADA/ETH │     5m, 15m, 30m, 1h, 2h, 4h, 6h, 12h, 1d │ spot │
│       ETH/BTC │     5m, 15m, 30m, 1h, 2h, 4h, 6h, 12h, 1d │ spot │
│      ETH/USDT │                  5m, 15m, 30m, 1h, 2h, 4h │ spot │
└───────────────┴───────────────────────────────────────────┴──────┘

```Hiển thị tất cả dữ liệu giao dịch bao gồm từ/đến phạm vi thời gian``` bash
> freqtrade list-data --show --trades
                     Found trades data for 1 pair.                     
┏━━━━━━━━━┳━━━━━━┳━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━┓
┃    Pair ┃ Type ┃                From ┃                  To ┃ Trades ┃
┡━━━━━━━━━╇━━━━━━╇━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━┩
│ XRP/ETH │ spot │ 2019-10-11 00:00:11 │ 2019-10-13 11:19:28 │  12477 │
└─────────┴──────┴─────────────────────┴─────────────────────┴────────┘

```## Dữ liệu giao dịch (đánh dấu)

Theo mặc định, lệnh phụ `download-data` tải xuống dữ liệu Nến (OHLCV). Hầu hết các sàn giao dịch cũng cung cấp dữ liệu giao dịch lịch sử thông qua API của họ.
Dữ liệu này có thể hữu ích nếu bạn cần nhiều khung thời gian khác nhau vì nó chỉ được tải xuống một lần và sau đó được lấy mẫu lại cục bộ theo các khung thời gian mong muốn.

Vì dữ liệu này mặc định lớn nên các tệp sử dụng định dạng tệp lông theo mặc định. Chúng được lưu trữ trong thư mục dữ liệu của bạn với quy ước đặt tên là `<pair>-trades.feather` (`ETH_BTC-trades.feather`). Chế độ gia tăng cũng được hỗ trợ, như đối với dữ liệu OHLCV lịch sử, do đó, việc tải xuống dữ liệu mỗi tuần một lần với `--days 8` sẽ tạo ra một kho lưu trữ dữ liệu gia tăng.

Để sử dụng chế độ này, chỉ cần thêm `--dl-trades` vào cuộc gọi của bạn. Điều này sẽ hoán đổi phương thức tải xuống để tải xuống các giao dịch.
Nếu `--convert` cũng được cung cấp, bước lấy mẫu lại sẽ tự động diễn ra và cuối cùng ghi đè dữ liệu OHLCV hiện có cho các kết hợp cặp/khung thời gian nhất định.

!!! Cảnh báo "Không sử dụng"
    Bạn không nên sử dụng tính năng này trừ khi bạn là người dùng kraken (Kraken không cung cấp dữ liệu OHLCV lịch sử).  
    Hầu hết các sàn giao dịch khác đều cung cấp đầy đủ lịch sử cho dữ liệu OHLCV, do đó, việc tải xuống nhiều khung thời gian thông qua phương pháp đó vẫn sẽ nhanh hơn rất nhiều so với việc tải xuống dữ liệu giao dịch.

!!! Lưu ý "Người dùng Kraken"
    Người dùng Kraken nên đọc [điều này](exchanges.md#histoire-kraken-data) trước khi bắt đầu tải xuống dữ liệu.

    Kraken Futures sử dụng các bản tải xuống OHLCV tiêu chuẩn và không yêu cầu `--dl-trades`.

Cuộc gọi ví dụ:```bash
freqtrade download-data --exchange kraken --pairs XRP/EUR ETH/EUR --days 20 --dl-trades
```!!! Lưu ý
    Mặc dù phương pháp này sử dụng lệnh gọi không đồng bộ nhưng sẽ chậm vì nó yêu cầu kết quả của lệnh gọi trước đó để tạo yêu cầu tiếp theo tới sàn giao dịch.

## Bước tiếp theo

Tuyệt vời, bây giờ bạn đã tải xuống một số dữ liệu, vì vậy bây giờ bạn có thể bắt đầu [kiểm tra lại](backtesting.md) chiến lược của mình.