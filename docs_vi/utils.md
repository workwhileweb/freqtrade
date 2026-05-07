<!-- Auto-translated from docs/ by script. Please review technical terms. -->

# Lệnh con tiện ích

Ngoài các chế độ chạy Giao dịch trực tiếp và Chạy khô, các lệnh phụ tối ưu hóa `backtesting` và `hyperopt` và lệnh phụ `download-data` chuẩn bị dữ liệu lịch sử, bot còn chứa một số lệnh phụ tiện ích. Chúng được mô tả trong phần này.

## Tạo thư mục người dùng

Tạo cấu trúc thư mục để giữ các tập tin của bạn cho freqtrade.
Cũng sẽ tạo ra các ví dụ về chiến lược và siêu thích hợp để bạn bắt đầu.
Có thể được sử dụng nhiều lần - sử dụng `--reset` sẽ đặt lại chiến lược mẫu và các tệp hyperopt về trạng thái mặc định của chúng.

--8<-- "lệnh/create-userdir.md"

!!! Cảnh báo
    Việc sử dụng `--reset` có thể dẫn đến mất dữ liệu vì thao tác này sẽ ghi đè lên tất cả các tệp mẫu mà không cần hỏi lại.```
├── backtest_results
├── data
├── hyperopt_results
├── hyperopts
│   ├── sample_hyperopt_loss.py
├── notebooks
│   └── strategy_analysis_example.ipynb
├── plot
└── strategies
    └── sample_strategy.py
```## Tạo cấu hình mới

Tạo một tệp cấu hình mới, đặt một số câu hỏi là những lựa chọn quan trọng cho cấu hình.

--8<-- "lệnh/new-config.md"

!!! Cảnh báo
    Chỉ những câu hỏi quan trọng mới được hỏi. Freqtrade cung cấp nhiều khả năng cấu hình hơn, được liệt kê trong [Tài liệu cấu hình](configuration.md#configuration-parameters)

### Tạo ví dụ cấu hình```
$ freqtrade new-config --config user_data/config_binance.json

? Do you want to enable Dry-run (simulated trades)?  Yes
? Please insert your stake currency: BTC
? Please insert your stake amount: 0.05
? Please insert max_open_trades (Integer or -1 for unlimited open trades): 3
? Please insert your desired timeframe (e.g. 5m): 5m
? Please insert your display Currency (for reporting): USD
? Select exchange  binance
? Do you want to enable Telegram?  No
```## Hiển thị cấu hình

Hiển thị tệp cấu hình (với các giá trị nhạy cảm được xử lý lại theo mặc định).
Đặc biệt hữu ích với [tách tệp cấu hình](configuration.md#multiple-configuration-files) hoặc [biến môi trường](configuration.md#environment-variables), trong đó lệnh này sẽ hiển thị cấu hình đã hợp nhất.

![Hiển thị đầu ra cấu hình](asset/show-config-output.png)

--8<-- "lệnh/show-config.md"``` output
Your combined configuration is:
{
  "exit_pricing": {
    "price_side": "other",
    "use_order_book": true,
    "order_book_top": 1
  },
  "stake_currency": "USDT",
  "exchange": {
    "name": "binance",
    "key": "REDACTED",
    "secret": "REDACTED",
    "ccxt_config": {},
    "ccxt_async_config": {},
  }
  // ...
}
```!!! Cảnh báo "Chia sẻ thông tin được cung cấp bởi lệnh này"
    Chúng tôi cố gắng xóa tất cả thông tin nhạy cảm đã biết khỏi đầu ra mặc định (không có `--show-sensitive`). 
    Tuy nhiên, vui lòng kiểm tra kỹ các giá trị nhạy cảm trong đầu ra của bạn để đảm bảo bạn không vô tình tiết lộ một số thông tin cá nhân.

## Tạo chiến lược mới

Tạo chiến lược mới từ một mẫu tương tự như SampleStrategy.
Tệp sẽ được đặt tên nội tuyến với tên lớp của bạn và sẽ không ghi đè lên các tệp hiện có.

Kết quả sẽ nằm trong `user_data/strategies/<strategyclassname>.py`.

--8<-- "commands/new-strategy.md"

### Cách sử dụng mẫu của chiến lược mới```bash
freqtrade new-strategy --strategy AwesomeStrategy
```Với thư mục người dùng tùy chỉnh```bash
freqtrade new-strategy --userdir ~/.freqtrade/ --strategy AwesomeStrategy
```Sử dụng mẫu nâng cao (điền tất cả các hàm và phương thức tùy chọn)```bash
freqtrade new-strategy --strategy AwesomeStrategy --template advanced
```## Chiến lược danh sách

Sử dụng lệnh phụ `list-strategies` để xem tất cả các chiến lược trong một thư mục cụ thể.

Lệnh con này rất hữu ích trong việc tìm kiếm các vấn đề trong môi trường của bạn với các chiến lược tải: các mô-đun có chiến lược có lỗi và không tải được được in màu đỏ (LOAD FAILED), trong khi các chiến lược có tên trùng lặp được in màu vàng (TÊN DUPLICATE).

--8<-- "lệnh/list-strategies.md"

!!! Cảnh báo
    Sử dụng các lệnh này sẽ cố tải tất cả các tệp python từ một thư mục. Đây có thể là một rủi ro bảo mật nếu các tệp không đáng tin cậy nằm trong thư mục này vì tất cả mã cấp mô-đun đều được thực thi.

Ví dụ: Tìm kiếm các thư mục chiến lược mặc định (trong userdir mặc định).``` bash
freqtrade list-strategies
```Ví dụ: Thư mục chiến lược tìm kiếm trong userdir.``` bash
freqtrade list-strategies --userdir ~/.freqtrade/
```Ví dụ: Tìm kiếm đường dẫn chiến lược chuyên dụng.``` bash
freqtrade list-strategies --strategy-path ~/.freqtrade/strategies/
```## Liệt kê các hàm Hyperopt-Loss

Sử dụng lệnh phụ `list-hyperoptloss` để xem tất cả các chức năng mất hyperopt có sẵn.

Nó cung cấp một danh sách nhanh tất cả các hàm mất mát có sẵn trong môi trường của bạn.

Lệnh con này có thể hữu ích trong việc tìm kiếm các sự cố trong môi trường của bạn với các hàm mất tải: các mô-đun có hàm Hyperopt-Loss có lỗi và không tải được được in màu đỏ (LOAD FAILED), trong khi các hàm hyperopt-Loss có tên trùng lặp được in màu vàng (TÊN TRỐNG).

--8<-- "lệnh/list-hyperoptloss.md"

## Liệt kê các mô hình tần số AI

Sử dụng lệnh phụ `list-freqaimodels` để xem tất cả các mô hình freqAI có sẵn.

Lệnh con này rất hữu ích trong việc tìm kiếm các vấn đề trong môi trường của bạn khi tải các mô hình freqAI: các mô-đun có mô hình có lỗi và không tải được sẽ được in màu đỏ (LOAD FAILED), trong khi các mô hình có tên trùng lặp được in màu vàng (TÊN DUPLICATE).

--8<-- "lệnh/list-freqaimodels.md"

## Trao đổi danh sách

Sử dụng lệnh phụ `list-exchanges` để xem các sàn giao dịch có sẵn cho bot.

--8<-- "lệnh/list-exchanges.md"

Ví dụ: xem các trao đổi có sẵn cho bot:```
$ freqtrade list-exchanges
Exchanges available for Freqtrade:
Exchange name       Supported    Markets                 Reason
------------------  -----------  ----------------------  ------------------------------------------------------------------------
binance             Official     spot, isolated futures
bitmart             Official     spot
bybit                            spot, isolated futures
gate                Official     spot, isolated futures
htx                 Official     spot
huobi                            spot
kraken              Official     spot
okx                 Official     spot, isolated futures
```!!! thông tin ""
    Đầu ra giảm để rõ ràng - các sàn giao dịch được hỗ trợ và sẵn có có thể thay đổi theo thời gian.

!!! Lưu ý "thiếu trao đổi opt"
    Các giá trị có "thiếu opt:" có thể cần cấu hình đặc biệt (ví dụ: sử dụng sổ đặt hàng nếu thiếu `fetchTickers`) - nhưng về mặt lý thuyết sẽ hoạt động (mặc dù chúng tôi không thể đảm bảo chúng sẽ hoạt động).

Ví dụ: xem tất cả các sàn giao dịch được thư viện ccxt hỗ trợ (bao gồm cả những sàn giao dịch 'xấu', tức là những sàn được biết là không hoạt động với Freqtrade)```
$ freqtrade list-exchanges -a
All exchanges supported by the ccxt library:
Exchange name       Valid    Supported    Markets                 Reason
------------------  -------  -----------  ----------------------  ---------------------------------------------------------------------------------
binance             True     Official     spot, isolated futures
bitflyer            False                 spot                    missing: fetchOrder. missing opt: fetchTickers.
bitmart             True     Official     spot
bybit               True                  spot, isolated futures
gate                True     Official     spot, isolated futures
htx                 True     Official     spot
kraken              True     Official     spot
okx                 True     Official     spot, isolated futures
```!!! thông tin ""
    Sản lượng giảm - các sàn giao dịch được hỗ trợ và sẵn có có thể thay đổi theo thời gian.

## Liệt kê các khung thời gian

Sử dụng lệnh phụ `list-timeframes` để xem danh sách các khung thời gian có sẵn để trao đổi.

--8<-- "lệnh/list-timeframes.md"

* Ví dụ: xem khung thời gian trao đổi 'binance', được đặt trong tệp cấu hình:```
$ freqtrade list-timeframes -c config_binance.json
...
Timeframes available for the exchange `binance`: 1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w, 1M
```* Ví dụ: liệt kê các sàn giao dịch có sẵn cho Freqtrade và in các khung thời gian được hỗ trợ bởi từng sàn đó:```
$ for i in `freqtrade list-exchanges -1`; do freqtrade list-timeframes --exchange $i; done
```## Liệt kê các cặp/liệt kê thị trường

Các lệnh phụ `list-pairs` và `list-markets` cho phép xem các cặp/thị trường có sẵn trên sàn giao dịch.

Các cặp là các thị trường có ký tự '/' giữa phần tiền cơ sở và phần tiền định giá trong biểu tượng thị trường.
Ví dụ: trong cặp 'ETH/BTC', 'ETH' là loại tiền cơ bản, trong khi 'BTC' là loại tiền định giá.

Đối với các cặp được giao dịch bởi Freqtrade, loại tiền định giá của cặp được xác định bởi giá trị của cài đặt cấu hình `stake_currency`.

Bạn có thể in thông tin về bất kỳ cặp/thị trường nào bằng các lệnh phụ này - và bạn có thể lọc đầu ra theo loại tiền định giá bằng cách sử dụng `--quote BTC` hoặc theo loại tiền cơ sở bằng cách sử dụng tùy chọn `--base ETH` tương ứng.

Các lệnh phụ này có cùng cách sử dụng và cùng một bộ tùy chọn khả dụng:

--8<-- "lệnh/list-pairs.md"

Theo mặc định, chỉ các cặp/thị trường đang hoạt động mới được hiển thị. Các cặp/thị trường đang hoạt động là những cặp hiện có thể được giao dịch trên sàn giao dịch.
Bạn có thể sử dụng tùy chọn `-a`/`-all` để xem danh sách tất cả các cặp/thị trường, bao gồm cả những cặp/thị trường không hoạt động.
Các cặp có thể được liệt kê là không thể giao dịch nếu giá giao dịch nhỏ nhất trên thị trường là rất nhỏ, tức là nhỏ hơn `1e-11` (`0,000000000001`)

Các cặp/thị trường được sắp xếp theo chuỗi ký hiệu của nó trong kết quả in ra.

### Ví dụ

* In danh sách các cặp hoạt động với đồng tiền định giá USD trên sàn giao dịch, được chỉ định theo mặc định
tệp cấu hình (tức là các cặp trên sàn giao dịch "Binance") ở định dạng JSON:```
$ freqtrade list-pairs --quote USD --print-json
```* In danh sách tất cả các cặp trên sàn giao dịch, được chỉ định trong tệp cấu hình `config_binance.json`
(tức là trên sàn giao dịch "Binance") với các loại tiền cơ bản BTC hoặc ETH và các loại tiền định giá USDT hoặc USD, làm
danh sách con người có thể đọc được với bản tóm tắt:```
$ freqtrade list-pairs -c config_binance.json --all --base BTC ETH --quote USDT USD --print-list
```* In tất cả các thị trường trên sàn giao dịch "Kraken", ở định dạng bảng:```
$ freqtrade list-markets --exchange kraken --all
```## Danh sách cặp thử nghiệm

Sử dụng lệnh phụ `test-pairlist` để kiểm tra cấu hình của [danh sách cặp động](plugins.md#pairlists).

Yêu cầu cấu hình với thuộc tính `danh sách cặp` được chỉ định.
Có thể được sử dụng để tạo danh sách cặp tĩnh được sử dụng trong quá trình kiểm tra ngược/hyperopt.

--8<-- "lệnh/test-pairlist.md"

### Ví dụ

Hiển thị danh sách trắng khi sử dụng [danh sách cặp động](plugins.md#pairlists).```
freqtrade test-pairlist --config config.json --quote USDT BTC
```## Chuyển đổi cơ sở dữ liệu

`freqtrade Convert-db` có thể được sử dụng để chuyển đổi cơ sở dữ liệu của bạn từ hệ thống này sang hệ thống khác (sqlite -> postgres, postgres -> postgres khác), di chuyển tất cả các giao dịch, đơn đặt hàng và Pairlocks.

Vui lòng tham khảo [tài liệu tương ứng](advanced-setup.md#use-a-other-database-system) để tìm hiểu về các yêu cầu đối với các hệ thống cơ sở dữ liệu khác nhau.

--8<-- "lệnh/convert-db.md"

!!! Cảnh báo
    Hãy đảm bảo chỉ sử dụng tính năng này trên cơ sở dữ liệu mục tiêu trống. Freqtrade sẽ thực hiện di chuyển thường xuyên nhưng có thể thất bại nếu các mục nhập đã tồn tại.

## Chế độ máy chủ web

!!! Cảnh báo "Thử nghiệm"
    Chế độ máy chủ web là một chế độ thử nghiệm để tăng năng suất phát triển chiến lược và hỗ trợ.
    Có thể vẫn còn lỗi - vì vậy nếu bạn tình cờ gặp phải những lỗi này, vui lòng báo cáo chúng là sự cố với github, cảm ơn.

Chạy freqtrade ở chế độ máy chủ web.
Freqtrade sẽ khởi động máy chủ web và cho phép FreqUI khởi động và kiểm soát các quá trình kiểm tra ngược.
Điều này có ưu điểm là dữ liệu sẽ không được tải lại giữa các lần chạy thử nghiệm ngược (miễn là khung thời gian và khoảng thời gian vẫn giống hệt nhau).
FreqUI cũng sẽ hiển thị kết quả backtesting.

--8<-- "lệnh/webserver.md"

### Chế độ máy chủ web - docker

Bạn cũng có thể sử dụng chế độ máy chủ web thông qua docker.
Việc khởi động vùng chứa một lần yêu cầu cấu hình cổng một cách rõ ràng vì các cổng không được hiển thị theo mặc định.
Bạn có thể sử dụng `docker soạn thảo chạy --rm -p 127.0.0.1:8080:8080 máy chủ web freqtrade` để khởi động vùng chứa một lần. Vùng chứa này sẽ bị xóa sau khi bạn dừng nó. Điều này giả định rằng cổng 8080 vẫn khả dụng và không có bot nào khác đang chạy trên cổng đó.

Ngoài ra, bạn có thể cấu hình lại tệp docker-compose để cập nhật lệnh:``` yml
    command: >
      webserver
      --config /freqtrade/user_data/config.json
```Bây giờ bạn có thể sử dụng `docker soạn thảo` để khởi động máy chủ web.
Điều này giả định rằng cấu hình đã kích hoạt và định cấu hình máy chủ web cho docker (cổng nghe = `0.0.0.0`).

!!! Mẹo
    Đừng quên đặt lại lệnh về lệnh giao dịch nếu bạn muốn khởi động bot trực tiếp hoặc chạy thử. 

## Hiển thị kết quả Backtest trước đó

Cho phép bạn hiển thị kết quả backtest trước đó.
Việc thêm `--show-pair-list` sẽ tạo ra một danh sách cặp được sắp xếp mà bạn có thể dễ dàng sao chép/dán vào cấu hình của mình (bỏ qua các cặp xấu).

??? Cảnh báo "Chiến lược trang bị quá mức"
    Chỉ sử dụng các cặp chiến thắng có thể dẫn đến một chiến lược được trang bị quá mức, chiến lược này sẽ không hoạt động tốt trên dữ liệu trong tương lai. Hãy đảm bảo kiểm tra rộng rãi chiến lược của bạn trong thời gian thử nghiệm trước khi mạo hiểm với tiền thật.

--8<-- "lệnh/backtesting-show.md"

## Phân tích backtest chi tiết

Phân tích kết quả backtest nâng cao.

Thông tin chi tiết hơn trong phần [Phân tích backtesting](advanced-backtesting.md#analyze-the-buyentry-and-sellexit-tags).

--8<-- "commands/backtesting-analysis.md"

## Liệt kê kết quả Hyperopt

Bạn có thể liệt kê các giai đoạn siêu tối ưu hóa mà mô-đun Hyperopt đã đánh giá trước đó bằng lệnh phụ `hyperopt-list`.

--8<-- "lệnh/hyperopt-list.md"

!!! Lưu ý
    `hyperopt-list` sẽ tự động sử dụng tệp kết quả hyperopt mới nhất có sẵn.
    Bạn có thể ghi đè điều này bằng cách sử dụng đối số `--hyperopt-filename` và chỉ định một tên tệp có sẵn khác (không có đường dẫn!).

### Ví dụ

Liệt kê tất cả kết quả, in chi tiết kết quả tốt nhất ở cuối:```
freqtrade hyperopt-list
```Chỉ liệt kê các thời kỳ có lợi nhuận dương. Không in chi tiết về kỷ nguyên tốt nhất để danh sách có thể được lặp lại trong một tập lệnh:```
freqtrade hyperopt-list --profitable --no-details
```## Hiển thị chi tiết kết quả Hyperopt

Bạn có thể hiển thị chi tiết về bất kỳ giai đoạn siêu tối ưu hóa nào được mô-đun Hyperopt đánh giá trước đó bằng lệnh phụ `hyperopt-show`.

--8<-- "lệnh/hyperopt-show.md"

!!! Lưu ý
    `hyperopt-show` sẽ tự động sử dụng tệp kết quả hyperopt mới nhất có sẵn.
    Bạn có thể ghi đè điều này bằng cách sử dụng đối số `--hyperopt-filename` và chỉ định một tên tệp có sẵn khác (không có đường dẫn!).

### Ví dụ

In chi tiết cho kỷ nguyên 168 (số kỷ nguyên được hiển thị bởi lệnh phụ `hyperopt-list` hoặc bởi chính Hyperopt trong quá trình chạy siêu tối ưu hóa):```
freqtrade hyperopt-show -n 168
```In dữ liệu JSON với thông tin chi tiết về kỷ nguyên tốt nhất gần đây nhất (tức là kỷ nguyên tốt nhất trong tất cả các kỷ nguyên):```
freqtrade hyperopt-show --best -n -1 --print-json --no-header
```## Hiển thị giao dịch

In các giao dịch đã chọn (hoặc tất cả) từ cơ sở dữ liệu ra màn hình.

--8<-- "commands/show-trades.md"

### Ví dụ

In các giao dịch với id 2 và 3 dưới dạng json``` bash
freqtrade show-trades --db-url sqlite:///tradesv3.sqlite --trade-ids 2 3 --print-json
```## Trình cập nhật chiến lược

Cập nhật các chiến lược được liệt kê hoặc tất cả các chiến lược trong thư mục chiến lược để tuân thủ v3.
Nếu lệnh chạy mà không có --strategy-list thì tất cả các chiến lược bên trong thư mục chiến lược sẽ được chuyển đổi.
Chiến lược ban đầu của bạn sẽ vẫn có sẵn trong thư mục `user_data/strategies_orig_updater/`.

!!! Cảnh báo "Kết quả chuyển đổi"
    Trình cập nhật chiến lược sẽ hoạt động theo cách tiếp cận "nỗ lực tốt nhất". Vui lòng thực hiện thẩm định và xác minh kết quả chuyển đổi.
    Chúng tôi cũng khuyên bạn nên chạy trình định dạng python (ví dụ: `định dạng ruff`) để định dạng kết quả một cách lành mạnh.

--8<-- "lệnh/chiến lược-updater.md"