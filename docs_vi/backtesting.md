<!-- Auto-translated from docs/ by script. Please review technical terms. -->

# Kiểm tra lại

Trang này giải thích cách xác thực hiệu suất chiến lược của bạn bằng cách sử dụng Backtesting.

Backtesting yêu cầu phải có sẵn dữ liệu lịch sử.
Để tìm hiểu cách lấy dữ liệu cho các cặp và trao đổi mà bạn quan tâm, hãy đi tới phần [Tải xuống dữ liệu](data-download.md) của tài liệu.

Kiểm tra ngược cũng có sẵn trong [chế độ máy chủ web](freq-ui.md#backtesting), cho phép bạn chạy kiểm tra ngược thông qua giao diện web.

## Tham chiếu lệnh Backtesting

--8<-- "commands/backtesting.md"

## Kiểm tra chiến lược của bạn bằng Backtesting

Bây giờ bạn đã có chiến lược Vào và Thoát tốt cũng như một số dữ liệu lịch sử, bạn muốn kiểm tra nóreal data. This is what we call [backtesting](https://en.wikipedia.org/wiki/Backtesting).
Việc kiểm tra ngược sẽ sử dụng các loại tiền điện tử (cặp) từ tệp cấu hình của bạn và tải dữ liệu nến lịch sử (OHLCV) từ `user_data/data/<exchange>` theo mặc định.
Nếu không có sẵn dữ liệu cho sự kết hợp trao đổi / cặp / khung thời gian, việc kiểm tra ngược sẽ yêu cầu bạn tải chúng xuống trước bằng cách sử dụng `freqtrade download-data`.
Để biết chi tiết về cách tải xuống, vui lòng tham khảo phần [Tải xuống dữ liệu](data-download.md) trong tài liệu.

Kết quả của việc kiểm tra lại sẽ xác nhận liệu bot của bạn có khả năng kiếm được lợi nhuận cao hơn là thua lỗ hay không.

Tất cả các tính toán lợi nhuận đều bao gồm phí và freqtrade sẽ sử dụng phí mặc định của sàn giao dịch để tính toán.

!!! Cảnh báo "Sử dụng danh sách cặp động để kiểm tra lại"
    Có thể sử dụng danh sách cặp động (không phải tất cả các trình xử lý đều được phép sử dụng ở chế độ kiểm tra ngược), tuy nhiên, nó phụ thuộc vào điều kiện thị trường hiện tại - điều này sẽ không phản ánh trạng thái lịch sử của danh sách cặp.
    Ngoài ra, khi sử dụng danh sách cặp không phải là StaticPairlist, khả năng tái tạo kết quả kiểm tra lại không thể được đảm bảo.
    Vui lòng đọc [tài liệu về danh sách cặp](plugins.md#pairlists) để biết thêm thông tin.

    Để đạt được kết quả có thể lặp lại, tốt nhất hãy tạo một danh sách cặp thông qua lệnh [`test-pairlist`](utils.md#test-pairlist) và sử dụng danh sách đó làm danh sách cặp tĩnh.

!!! Lưu ý
    Theo mặc định, Freqtrade sẽ xuất kết quả backtesting sang `user_data/backtest_results`.
    Các giao dịch đã xuất có thể được sử dụng để [phân tích thêm](#further-backtest-result-analysis) hoặc có thể được sử dụng bởi [lệnh phụ vẽ sơ đồ](plotting.md#plot-price-and-indicators) (`freqtradeplot-dataframe`) trong thư mục scripts.


### Số dư ban đầu

Việc kiểm tra lại sẽ yêu cầu số dư ban đầu, số dư này có thể được cung cấp dưới dạng đối số dòng lệnh `--dry-run-wallet <balance>` hoặc `--starting-balance <balance>` hoặc thông qua cài đặt cấu hình `dry_run_wallet`.
Số tiền này phải cao hơn `stake_amount`, nếu không bot sẽ không thể mô phỏng bất kỳ giao dịch nào.

### Số tiền đặt cược động

Backtest hỗ trợ [số tiền đặt cược động](configuration.md#dynamic-stake-amount) bằng cách định cấu hình `stake_amount` là `"không giới hạn"`, điều này sẽ chia số dư ban đầu thành các phần `max_open_trades`.
Lợi nhuận từ các giao dịch sớm sẽ dẫn đến số tiền đặt cược cao hơn sau đó, dẫn đến lợi nhuận gộp trong giai đoạn kiểm tra lại.

### Ví dụ về lệnh backtesting

Với dữ liệu nến 5 phút (OHLCV) (theo mặc định)```bash
freqtrade backtesting --strategy AwesomeStrategy
```Trong đó `--strategy AwesomeStrategy` / `-s AwesomeStrategy` đề cập đến tên lớp của chiến lược, nằm trong tệp python trong thư mục `user_data/strategies`.

---

Với dữ liệu nến 1 phút (OHLCV)```bash
freqtrade backtesting --strategy AwesomeStrategy --timeframe 1m
```---

Cung cấp số dư ban đầu tùy chỉnh là 1000 (bằng tiền đặt cọc)```bash
freqtrade backtesting --strategy AwesomeStrategy --dry-run-wallet 1000
```---

Sử dụng nguồn dữ liệu nến lịch sử trên đĩa (OHLCV) khác

Giả sử bạn đã tải xuống dữ liệu lịch sử từ sàn giao dịch Binance và giữ nó trong thư mục `user_data/data/binance-20180101`. 
Sau đó, bạn có thể sử dụng dữ liệu này để kiểm tra lại như sau:```bash
freqtrade backtesting --strategy AwesomeStrategy --datadir user_data/data/binance-20180101 
```---

So sánh nhiều chiến lược```bash
freqtrade backtesting --strategy-list SampleStrategy1 AwesomeStrategy --timeframe 5m
```Trong đó `SampleStrategy1` và `AwesomeStrategy` đề cập đến tên lớp của chiến lược.

---

Ngăn chặn xuất giao dịch vào tệp```bash
freqtrade backtesting --strategy backtesting --export none --config config.json 
```Chỉ sử dụng tùy chọn này nếu bạn chắc chắn rằng mình không muốn vẽ đồ thị hoặc phân tích kết quả thêm nữa.

---

Xuất giao dịch sang tệp chỉ định thư mục tùy chỉnh```bash
freqtrade backtesting --strategy backtesting --export trades --backtest-directory=user_data/custom-backtest-results
```---

Ngoài ra, vui lòng đọc về [giai đoạn khởi động chiến lược](strategy-customization.md#strategy-startup- Period).

---

Cung cấp giá trị phí tùy chỉnh

Đôi khi tài khoản của bạn có các khoản giảm phí nhất định (giảm phí bắt đầu từ một quy mô tài khoản nhất định hoặc khối lượng hàng tháng) mà ccxt không hiển thị.
Để giải quyết vấn đề này trong quá trình kiểm tra lại, bạn có thể sử dụng tùy chọn dòng lệnh `--fee` để cung cấp giá trị này cho việc kiểm tra lại.
Phí này phải là một tỷ lệ và sẽ được áp dụng hai lần (một lần khi vào giao dịch và một lần khi thoát giao dịch).

Ví dụ: nếu phí hoa hồng cho mỗi đơn hàng là 0,1% (tức là 0,001 được viết dưới dạng tỷ lệ), thì bạn sẽ chạy thử nghiệm ngược như sau:```bash
freqtrade backtesting --fee 0.001
```!!! Lưu ý
    Chỉ cung cấp tùy chọn này (hoặc tham số cấu hình tương ứng) nếu bạn muốn thử nghiệm các giá trị phí khác nhau. Theo mặc định, Backtesting lấy phí mặc định từ thông tin cặp trao đổi/thị trường.

---

Chạy backtest với tập kiểm tra nhỏ hơn bằng cách sử dụng khoảng thời gian

Sử dụng đối số `--timerange` để thay đổi số lượng bộ kiểm tra bạn muốn sử dụng.

Ví dụ: chạy thử nghiệm ngược với tùy chọn `--timerange=20190501-` sẽ sử dụng tất cả dữ liệu có sẵn bắt đầu từ ngày 1 tháng 5 năm 2019 từ dữ liệu đầu vào của bạn.```bash
freqtrade backtesting --timerange=20190501-
```Bạn cũng có thể chỉ định phạm vi ngày cụ thể.

Thông số kỹ thuật phạm vi thời gian đầy đủ:

- Sử dụng data đến 31/01/2018: `--timerange=-20180131`
- Sử dụng dữ liệu từ ngày 31/01/2018: `--timerange=20180131-`
- Sử dụng dữ liệu từ ngày 31/01/2018 đến ngày 01/03/2018 : `--timerange=20180131-20180301`
- Sử dụng dữ liệu giữa các dấu thời gian POSIX/epoch 1527595200 1527618600: `--timerange=1527595200-1527618600`

## Hiểu kết quả backtesting

Điều quan trọng nhất trong quá trình backtesting là hiểu được kết quả.

Kết quả backtesting sẽ như sau:```
                                               BACKTESTING REPORT                                                
┏━━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━┓
┃          Pair ┃ Trades ┃ Avg Profit % ┃  Tot Profit ┃ Tot Profit % ┃    Avg Duration ┃  Win  Draw  Loss  Win% ┃
┡━━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━┩
│ LTC/USDT:USDT │     16 │         1.01 │      56.882 │         5.69 │        16:16:00 │   16     0     0   100 │
│ ETC/USDT:USDT │     12 │         0.73 │      31.513 │         3.15 │         9:55:00 │   11     0     1  91.7 │
│ ETH/USDT:USDT │      8 │         0.69 │      18.659 │         1.87 │ 1 day, 13:55:00 │    7     0     1  87.5 │
│ XLM/USDT:USDT │     10 │          0.3 │      10.694 │         1.07 │        12:08:00 │    9     0     1  90.0 │
│ BTC/USDT:USDT │      8 │         0.22 │       7.502 │         0.75 │ 3 days, 1:24:00 │    6     0     2  75.0 │
│ XRP/USDT:USDT │      9 │        -0.13 │      -6.837 │        -0.68 │        21:18:00 │    8     0     1  88.9 │
│ DOT/USDT:USDT │      6 │        -0.39 │      -9.169 │        -0.92 │         5:35:00 │    4     0     2  66.7 │
│ ADA/USDT:USDT │      8 │        -1.75 │     -52.089 │        -5.21 │        11:38:00 │    6     0     2  75.0 │
│         TOTAL │     77 │         0.23 │      57.157 │         5.72 │        22:12:00 │   67     0    10  87.0 │
└───────────────┴────────┴──────────────┴─────────────┴──────────────┴─────────────────┴────────────────────────┘
                                             LEFT OPEN TRADES REPORT                                              
┏━━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━┓
┃          Pair ┃ Trades ┃ Avg Profit % ┃  Tot Profit ┃ Tot Profit % ┃     Avg Duration ┃  Win  Draw  Loss  Win% ┃
┡━━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━┩
│ BTC/USDT:USDT │      1 │        -4.14 │      -9.930 │        -0.99 │ 17 days, 8:00:00 │    0     0     1     0 │
│ ETC/USDT:USDT │      1 │        -4.24 │     -15.365 │        -1.54 │         10:40:00 │    0     0     1     0 │
│ DOT/USDT:USDT │      1 │        -5.29 │     -19.166 │        -1.92 │         11:30:00 │    0     0     1     0 │
│         TOTAL │      3 │        -4.56 │     -44.461 │        -4.45 │  6 days, 2:03:00 │    0     0     3     0 │
└───────────────┴────────┴──────────────┴─────────────┴──────────────┴──────────────────┴────────────────────────┘
                                              ENTER TAG STATS                                              
┏━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Enter Tag ┃ Entries ┃ Avg Profit % ┃  Tot Profit ┃ Tot Profit % ┃ Avg Duration ┃  Win  Draw  Loss  Win% ┃
┡━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━┩
│     OTHER │      77 │         0.23 │      57.157 │         5.72 │     22:12:00 │   67     0    10  87.0 │
│     TOTAL │      77 │         0.23 │      57.157 │         5.72 │     22:12:00 │   67     0    10  87.0 │
└───────────┴─────────┴──────────────┴─────────────┴──────────────┴──────────────┴────────────────────────┘
                                              EXIT REASON STATS                                               
┏━━━━━━━━━━━━━┳━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Exit Reason ┃ Exits ┃ Avg Profit % ┃  Tot Profit ┃ Tot Profit % ┃    Avg Duration ┃  Win  Draw  Loss  Win% ┃
┡━━━━━━━━━━━━━╇━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━┩
│         roi │    67 │         1.06 │     245.117 │        24.51 │        15:49:00 │   67     0     0   100 │
│ exit_signal │     4 │        -2.23 │     -31.226 │        -3.12 │  1 day, 8:38:00 │    0     0     4     0 │
│  force_exit │     3 │        -4.56 │     -44.461 │        -4.45 │ 6 days, 2:03:00 │    0     0     3     0 │
│   stop_loss │     3 │       -10.14 │    -112.273 │       -11.23 │  1 day, 3:05:00 │    0     0     3     0 │
│       TOTAL │    77 │         0.23 │      57.157 │         5.72 │        22:12:00 │   67     0    10  87.0 │
└─────────────┴───────┴──────────────┴─────────────┴──────────────┴─────────────────┴────────────────────────┘
                                                      MIXED TAG STATS                                                      
┏━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Enter Tag ┃ Exit Reason ┃ Trades ┃ Avg Profit % ┃  Tot Profit ┃ Tot Profit % ┃    Avg Duration ┃  Win  Draw  Loss  Win% ┃
┡━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━┩
│           │         roi │     67 │         1.06 │     245.117 │        24.51 │        15:49:00 │   67     0     0   100 │
│           │ exit_signal │      4 │        -2.23 │     -31.226 │        -3.12 │  1 day, 8:38:00 │    0     0     4     0 │
│           │  force_exit │      3 │        -4.56 │     -44.461 │        -4.45 │ 6 days, 2:03:00 │    0     0     3     0 │
│           │   stop_loss │      3 │       -10.14 │    -112.273 │       -11.23 │  1 day, 3:05:00 │    0     0     3     0 │
│     TOTAL │             │     77 │         0.23 │      57.157 │         5.72 │        22:12:00 │   67     0    10  87.0 │
└───────────┴─────────────┴────────┴──────────────┴─────────────┴──────────────┴─────────────────┴────────────────────────┘
                                   SUMMARY METRICS                                    
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Metric                                 ┃ Value                                     ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ Backtesting from                       │ 2025-07-01 00:00:00                       │
│ Backtesting to                         │ 2025-08-01 00:00:00                       │
│ Trading Mode                           │ Isolated Futures                          │
│ Max open trades                        │ 3                                         │
│                                        │                                           │
│ Total/Daily Avg Trades                 │ 77 / 2.48                                 │
│ Starting balance                       │ 1000 USDT                                 │
│ Final balance                          │ 1057.157 USDT                             │
│ Absolute profit                        │ 57.157 USDT                               │
│ Total profit %                         │ 5.72%                                     │
│ CAGR %                                 │ 92.41%                                    │
│ Sharpe (closed trades)                 │ 3.89                                      │
│ Sortino (closed trades)                │ 2.57                                      │
│ Calmar (closed trades)                 │ 43.03                                     │
│ SQN                                    │ 0.71                                      │
│ Profit factor                          │ 1.30                                      │
│ Expectancy (Ratio)                     │ 0.74 (0.04)                               │
│ Avg. daily profit                      │ 1.844 USDT                                │
│ Avg. stake amount                      │ 345.478 USDT                              │
│ Market change                          │ 30.51%                                    │
│ Total trade volume                     │ 53390.788 USDT                            │
│                                        │                                           │
│ Long / Short trades                    │ 67 / 10                                   │
│ Long / Short profit %                  │ 9.19% / -3.48%                            │
│ Long / Short profit USDT               │ 91.940 / -34.783                          │
│                                        │                                           │
│ Best Pair                              │ LTC/USDT:USDT 5.69%                       │
│ Worst Pair                             │ ADA/USDT:USDT -5.21%                      │
│ Best trade                             │ XRP/USDT:USDT 2.00%                       │
│ Worst trade                            │ ADA/USDT:USDT -10.17%                     │
│ Best day                               │ 27.031 USDT                               │
│ Worst day                              │ -47.826 USDT                              │
│ Days win/draw/lose                     │ 20 / 6 / 5                                │
│ Min/Max/Avg. Duration Winners          │ 0d 00:35 / 5d 18:15 / 0d 15:49            │
│ Min/Max/Avg. Duration Losers           │ 0d 10:40 / 17d 08:00 / 2d 17:00           │
│ Max Consecutive Wins / Loss            │ 36 / 3                                    │
│ Rejected Entry signals                 │ 258                                       │
│ Entry/Exit Timeouts                    │ 0 / 0                                     │
│                                        │                                           │
│ Min/Max balance (closed trades)        │ 1003.205 USDT / 1151.425 USDT             │
│ Max % of account underwater            │ 8.19%                                     │
│ Absolute drawdown                      │ 94.268 USDT (8.19%)                       │
│ Drawdown duration                      │ 9 days 08:50:00                           │
│ Profit at drawdown start               │ 151.425 USDT                              │
│ Profit at drawdown end                 │ 57.157 USDT                               │
│ Drawdown start                         │ 2025-07-22 15:10:00                       │
│ Drawdown end                           │ 2025-08-01 00:00:00                       │
│                                        │                                           │
│ Wallet based Metrics                   │                                           │
│ Min/Max balance (wallet balance)       │ 1000 USDT / 1151.425 USDT                 │
│ Min/Max balance dates (wallet balance) │ 2025-07-01 00:05:00 / 2025-07-22 15:15:00 │
│ Max % of account underwater (balance)  │ 5.01%                                     │
│ Absolute drawdown (wallet balance)     │ 54.76 USDT (4.76%)                        │
│ Drawdown duration                      │ 7 days 20:35:00                           │
│ Profit at drawdown start               │ 151.425 USDT                              │
│ Profit at drawdown end                 │ 96.664 USDT                               │
│ Drawdown start                         │ 2025-07-22 15:15:00                       │
│ Drawdown end                           │ 2025-07-30 11:50:00                       │
│ Sharpe (daily wallet balance)          │ 4.42                                      │
│ Sortino (daily wallet balance)         │ 4.35                                      │
│ Calmar (daily wallet balance)          │ 136.07                                    │
└────────────────────────────────────────┴───────────────────────────────────────────┘

Backtested 2025-07-01 00:00:00 -> 2025-08-01 00:00:00 | Max open trades : 3
                                                        STRATEGY SUMMARY                                                        
┏━━━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━┓
┃       Strategy ┃ Trades ┃ Avg Profit % ┃  Tot Profit ┃ Tot Profit % ┃ Avg Duration ┃  Win  Draw  Loss  Win% ┃       Drawdown ┃
┡━━━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━┩
│ SampleStrategy │     77 │         0.23 │      57.157 │         5.72 │     22:12:00 │   67     0    10  87.0 │ 94.268   8.19% │
└────────────────┴────────┴──────────────┴─────────────┴──────────────┴──────────────┴────────────────────────┴────────────────┘

```###Bảng báo cáo backtesting

Bảng đầu tiên chứa tất cả các giao dịch mà bot đã thực hiện, bao gồm cả "các giao dịch còn mở".

Dòng cuối cùng sẽ cung cấp cho bạn hiệu suất tổng thể của chiến lược,
đây:```
│         TOTAL │     77 │         0.22 │          54.774 │         5.48 │        22:12:00 │   67     0    10  87.0 │
```Bot đã thực hiện `77` giao dịch trong thời gian trung bình là `22:12:00`, với hiệu suất là `5,48%` (lợi nhuận), điều đó có nghĩa là nó đã kiếm được tổng cộng `54,774 USDT` bắt đầu với số vốn là 1000 USDT.

Cột `Lợi nhuận trung bình %` hiển thị lợi nhuận trung bình cho tất cả các giao dịch được thực hiện.
Thay vào đó, cột `Tot Profit %` hiển thị tổng % lợi nhuận liên quan đến số dư ban đầu.

Trong kết quả trên, chúng ta có số dư ban đầu là 1000 USDT và lợi nhuận tuyệt đối là 54,774 USDT - vì vậy `Tổng lợi nhuận %` sẽ là `(54,774 / 1000) * 100 ~= 5,48%`.

Hiệu suất chiến lược của bạn bị ảnh hưởng bởi chiến lược vào, chiến lược thoát cũng như bởi `roi_roi` tối thiểu` và `stop_loss` mà bạn đã đặt.

Ví dụ: nếu `roi_tối thiểu` của bạn chỉ là `"0": 0,01`, bạn không thể mong đợi bot kiếm được nhiều lợi nhuận hơn 1% (vì nó sẽ thoát mỗi khi giao dịch đạt 1%).```json
"minimal_roi": {
    "0":  0.01
},
```Mặt khác, nếu bạn đặt `minimal_roi` quá cao như `"0": 0,55`
(55%), gần như không có khả năng bot sẽ đạt được lợi nhuận này.
Do đó, hãy nhớ rằng hiệu suất của bạn là sự kết hợp không thể thiếu của tất cả các yếu tố khác nhau của chiến lược, cấu hình của bạn và các cặp tiền điện tử mà bạn đã thiết lập.

### Bảng giao dịch còn mở

Bảng thứ hai chứa tất cả các giao dịch mà bot phải `buộc_exit` vào cuối giai đoạn kiểm tra lại để hiển thị cho bạn bức tranh đầy đủ.
Điều này là cần thiết để mô phỏng hành vi thực tế, vì giai đoạn kiểm tra lại phải kết thúc vào một thời điểm nào đó, trong khi trên thực tế, bạn có thể để bot chạy mãi mãi.
Các giao dịch này cũng được bao gồm trong bảng đầu tiên, nhưng cũng được hiển thị riêng trong bảng này để rõ ràng.

### Nhập bảng thống kê thẻ

Bảng thứ ba cung cấp bảng phân tích các giao dịch theo thẻ nhập của chúng (ví dụ: `enter_long`, `enter_short`), hiển thị số lượng mục nhập, tỷ lệ phần trăm lợi nhuận trung bình, tổng lợi nhuận bằng loại tiền đặt cọc, tổng tỷ lệ phần trăm lợi nhuận, thời lượng trung bình và số lần thắng, hòa và thua cho mỗi thẻ.

###Bảng thống kê lý do thoát

Bảng thứ tư chứa bản tóm tắt lý do thoát (ví dụ: `exit_signal`, `roi`, `stop_loss`, `force_exit`). Bảng này có thể cho bạn biết khu vực nào cần cải thiện thêm (ví dụ: nếu nhiều giao dịch `exit_signal` bị thua lỗ, bạn nên nỗ lực cải thiện tín hiệu thoát hoặc cân nhắc việc vô hiệu hóa nó).

### Bảng thống kê thẻ hỗn hợp

Bảng thứ năm kết hợp các thẻ nhập và lý do thoát, cung cấp cái nhìn chi tiết về cách các thẻ nhập khác nhau hoạt động với các lý do thoát cụ thể. Điều này có thể giúp xác định sự kết hợp chiến lược vào và ra nào hiệu quả nhất.

### Số liệu tóm tắt

Thành phần cuối cùng của báo cáo backtest là bảng số liệu tóm tắt.
Nó chứa các số liệu chính về hiệu suất chiến lược của bạn trên dữ liệu kiểm tra lại.```
                                   SUMMARY METRICS                                    
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Metric                                 ┃ Value                                     ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ Backtesting from                       │ 2025-07-01 00:00:00                       │
│ Backtesting to                         │ 2025-08-01 00:00:00                       │
│ Trading Mode                           │ Isolated Futures                          │
│ Max open trades                        │ 3                                         │
│                                        │                                           │
│ Total/Daily Avg Trades                 │ 77 / 2.48                                 │
│ Starting balance                       │ 1000 USDT                                 │
│ Final balance                          │ 1057.157 USDT                             │
│ Absolute profit                        │ 57.157 USDT                               │
│ Total profit %                         │ 5.72%                                     │
│ CAGR %                                 │ 92.41%                                    │
│ Sharpe (closed trades)                 │ 3.89                                      │
│ Sortino (closed trades)                │ 2.57                                      │
│ Calmar (closed trades)                 │ 43.03                                     │
│ SQN                                    │ 0.71                                      │
│ Profit factor                          │ 1.30                                      │
│ Expectancy (Ratio)                     │ 0.74 (0.04)                               │
│ Avg. daily profit                      │ 1.844 USDT                                │
│ Avg. stake amount                      │ 345.478 USDT                              │
│ Market change                          │ 30.51%                                    │
│ Total trade volume                     │ 53390.788 USDT                            │
│                                        │                                           │
│ Long / Short trades                    │ 67 / 10                                   │
│ Long / Short profit %                  │ 9.19% / -3.48%                            │
│ Long / Short profit USDT               │ 91.940 / -34.783                          │
│                                        │                                           │
│ Best Pair                              │ LTC/USDT:USDT 5.69%                       │
│ Worst Pair                             │ ADA/USDT:USDT -5.21%                      │
│ Best trade                             │ XRP/USDT:USDT 2.00%                       │
│ Worst trade                            │ ADA/USDT:USDT -10.17%                     │
│ Best day                               │ 27.031 USDT                               │
│ Worst day                              │ -47.826 USDT                              │
│ Days win/draw/lose                     │ 20 / 6 / 5                                │
│ Min/Max/Avg. Duration Winners          │ 0d 00:35 / 5d 18:15 / 0d 15:49            │
│ Min/Max/Avg. Duration Losers           │ 0d 10:40 / 17d 08:00 / 2d 17:00           │
│ Max Consecutive Wins / Loss            │ 36 / 3                                    │
│ Rejected Entry signals                 │ 258                                       │
│ Entry/Exit Timeouts                    │ 0 / 0                                     │
│                                        │                                           │
│ Min/Max balance (closed trades)        │ 1003.205 USDT / 1151.425 USDT             │
│ Max % of account underwater            │ 8.19%                                     │
│ Absolute drawdown                      │ 94.268 USDT (8.19%)                       │
│ Drawdown duration                      │ 9 days 08:50:00                           │
│ Profit at drawdown start               │ 151.425 USDT                              │
│ Profit at drawdown end                 │ 57.157 USDT                               │
│ Drawdown start                         │ 2025-07-22 15:10:00                       │
│ Drawdown end                           │ 2025-08-01 00:00:00                       │
│                                        │                                           │
│ Wallet based Metrics                   │                                           │
│ Min/Max balance (wallet balance)       │ 1000 USDT / 1151.425 USDT                 │
│ Min/Max balance dates (wallet balance) │ 2025-07-01 00:05:00 / 2025-07-22 15:15:00 │
│ Max % of account underwater (balance)  │ 5.01%                                     │
│ Absolute drawdown (wallet balance)     │ 54.76 USDT (4.76%)                        │
│ Drawdown duration                      │ 7 days 20:35:00                           │
│ Profit at drawdown start               │ 151.425 USDT                              │
│ Profit at drawdown end                 │ 96.664 USDT                               │
│ Drawdown start                         │ 2025-07-22 15:15:00                       │
│ Drawdown end                           │ 2025-07-30 11:50:00                       │
│ Sharpe (daily wallet balance)          │ 4.42                                      │
│ Sortino (daily wallet balance)         │ 4.35                                      │
│ Calmar (daily wallet balance)          │ 136.07                                    │
└────────────────────────────────────────┴───────────────────────────────────────────┘
```- `Backtesting from` / `Backtesting to`: Phạm vi backtesting (thường được xác định bằng tùy chọn `--timerange`).
- `Chế độ giao dịch`: Giao dịch giao ngay hoặc tương lai.
- `Giao dịch mở tối đa`: Cài đặt `max_open_trades` (hoặc `--max-open-trades`) - hoặc số cặp trong danh sách cặp (bất kỳ giá trị nào thấp hơn).
- `Tổng số/Giao dịch trung bình hàng ngày`: Giống hệt với tổng số giao dịch của bảng kết quả kiểm tra lại / Tổng số giao dịch chia cho thời gian kiểm tra lại theo ngày (điều này sẽ cung cấp cho bạn thông tin về số lượng giao dịch mong đợi từ chiến lược).
- `Số dư ban đầu`: Số dư ban đầu - được cung cấp bởi ví chạy khô (cấu hình hoặc dòng lệnh).
- `Số dư cuối cùng`: Số dư cuối cùng - số dư đầu kỳ + lợi nhuận tuyệt đối.
- `Lợi nhuận tuyệt đối`: Lợi nhuận tính bằng tiền đặt cọc.
- `Tổng lợi nhuận %`: Tổng lợi nhuận. Đã căn chỉnh với `Tot Profit %` của hàng `TOTAL` từ bảng đầu tiên. Được tính bằng `(Vốn cuối cùng - Vốn ban đầu) / Vốn ban đầu`.
- `CAGR %`: Tốc độ tăng trưởng gộp hàng năm.
- `Sharpe (giao dịch đã đóng)`: Tỷ lệ Sharpe hàng năm chỉ bao gồm các giao dịch đã đóng (bỏ qua các giao dịch mở có lãi hoặc lỗ).
- `Sortino (giao dịch đã đóng)`: Tỷ lệ Sortino hàng năm chỉ bao gồm các giao dịch đã đóng (bỏ qua các giao dịch mở có lãi hoặc lỗ).
- `Calmar (giao dịch đã đóng)`: Tỷ lệ Calmar hàng năm chỉ bao gồm các giao dịch đã đóng (bỏ qua các giao dịch mở có lãi hoặc lỗ).
- `SQN`: Số chất lượng hệ thống (SQN) - của Van Tharp.
- `Hệ số lợi nhuận`: Tổng lợi nhuận của tất cả các giao dịch thắng chia cho tổng số tiền thua của tất cả các giao dịch thua.
- `Kỳ vọng (Tỷ lệ)`: Tỷ lệ kỳ vọng, là lãi hoặc lỗ trung bình trên mỗi giao dịch. Tỷ lệ kỳ vọng âm có nghĩa là chiến lược của bạn không mang lại lợi nhuận.
- `Trung bình. lợi nhuận hàng ngày`: Lợi nhuận trung bình mỗi ngày, được tính bằng `(Tổng lợi nhuận / Số ngày quay lại)`.
- `Trung bình. số tiền đặt cược`: Số tiền đặt cược trung bình, `stake_amount` hoặc mức trung bình khi sử dụng số tiền đặt cược động.
- `Thay đổi thị trường`: Thay đổi thị trường trong giai đoạn backtest. Được tính bằng mức trung bình của các thay đổi của tất cả các cặp từ nến đầu tiên đến nến cuối cùng sử dụng cột "đóng".
- `Tổng khối lượng giao dịch`: Khối lượng tạo ra trên sàn giao dịch để đạt được lợi nhuận trên.
- `Giao dịch mua / bán`: Phân chia số lượng giao dịch mua/bán (chỉ hiển thị khi thực hiện giao dịch bán).
- `Lợi nhuận mua / bán %`: Tỷ lệ phần trăm lợi nhuận cho các giao dịch mua và bán (chỉ hiển thị khi thực hiện giao dịch bán).
- `Lợi nhuận mua / bán USDT`: Lợi nhuận bằng tiền đặt cược cho các giao dịch mua và bán (chỉ hiển thị khi thực hiện giao dịch bán).
- `Cặp tốt nhất` / `Cặp tệ nhất`: Cặp hoạt động tốt nhất và kém nhất (dựa trên tổng phần trăm lợi nhuận) và `% tổng lợi nhuận` tương ứng của nó.
- `Giao dịch tốt nhất` / `Giao dịch tệ nhất`: Giao dịch thắng một lần lớn nhất và giao dịch thua lỗ lớn nhất.
- `Ngày tốt nhất` / `Ngày tồi tệ nhất`: Ngày tốt nhất và tồi tệ nhất dựa trên lợi nhuận hàng ngày.
- `Số ngày thắng/hòa/thua`: Số ngày thắng/thua (hòa thường là những ngày không đóng giao dịch).
- `Tối thiểu/Tối đa/Trung bình Người chiến thắng trong thời gian`: Khoảng thời gian tối thiểu, tối đa và trung bình cho các giao dịch thắng.
- `Tối thiểu/Tối đa/Trung bình Thời lượng giao dịch thua`: Khoảng thời gian tối thiểu, tối đa và trung bình cho các giao dịch thua lỗ.
- `Số Thắng/Thua Liên Tiếp Tối Đa`: Số lần thắng/thua liên tiếp tối đa liên tiếp.
- `Tín hiệu nhập bị từ chối`: Tín hiệu nhập giao dịch không thể thực hiện được do đã đạt đến `max_open_trades`.
- `Hết thời gian vào/ra`: Các lệnh vào/ra không được thực hiện (chỉ áp dụng nếu sử dụng giá tùy chỉnh).
- `Số dư tối thiểu/tối đa (giao dịch đã đóng)`: Số dư trên Ví thấp nhất và cao nhất trong khoảng thời gian kiểm tra lại dựa trên các giao dịch đã đóng.- `% tối đa của tài khoản dưới nước`: Tỷ lệ phần trăm tối đa tài khoản của bạn đã giảm từ đầu kể từ khi mô phỏng bắt đầu. Được tính bằng mức tối đa của `(Số dư tối đa - Số dư hiện tại) / (Số dư tối đa)`.
- `Rút tiền tuyệt đối`: Mức rút vốn tuyệt đối tối đa đã trải qua, bao gồm tỷ lệ phần trăm liên quan đến tài khoản được tính là `(Rút tiền tuyệt đối) / (DrawdownHigh + số dư ban đầu)`..
- `Rút tiền tuyệt đối (số dư ví)`: Mức rút vốn tuyệt đối tối đa dựa trên số dư chưa thực hiện, bao gồm tỷ lệ phần trăm liên quan đến tài khoản được tính là `(DrawdownHigh + startBalance)`.
- `Thời lượng rút vốn`: Khoảng thời gian rút vốn lớn nhất.
- `Lợi nhuận khi bắt đầu rút vốn` / `Lợi nhuận khi kết thúc rút vốn`: Lợi nhuận ở đầu và cuối thời gian rút vốn lớn nhất.
- `Drawdown start` / `Drawdown end`: Ngày giờ bắt đầu và kết thúc cho drawdown lớn nhất (cũng có thể được hiển thị thông qua lệnh phụ `plot-dataframe`).
- `Số dư tối thiểu/tối đa (số dư ví)`: Số dư Ví thấp nhất và cao nhất trong giai đoạn kiểm tra lại - bao gồm cả vốn gắn liền với các giao dịch mở.
- `Ngày số dư tối thiểu/tối đa (số dư ví)`: Ngày xảy ra số dư chưa thực hiện tối thiểu và tối đa.
- `Sharpe (số dư ví)` Tính toán tỷ lệ Sharpe hàng năm bao gồm cả lợi nhuận chưa thực hiện.
- `Sortino (số dư ví)` Tính tỷ lệ Sortino hàng năm bao gồm cả lợi nhuận chưa thực hiện.
- `Calmar (số dư ví)` Tính toán tỷ lệ Calmar hàng năm bao gồm cả lợi nhuận chưa thực hiện.

!!! Mẹo "Số liệu dựa trên ví"
    Các số liệu trong phần "Số liệu dựa trên ví" được tính toán dựa trên số dư chưa thực hiện, bao gồm vốn gắn liền với các giao dịch mở. Điều này cung cấp cái nhìn toàn diện hơn về hiệu suất của chiến lược vì nó tính đến cả lãi và lỗ đã thực hiện và chưa thực hiện.

### Phân tích hàng ngày / hàng tuần / hàng tháng / hàng năm

Bạn có thể xem tổng quan về kết quả hàng ngày, hàng tuần, hàng tháng hoặc hàng năm bằng cách sử dụng khóa chuyển `--breakdown <>`.

Để trực quan hóa số liệu phân tích hàng tháng và hàng năm, bạn có thể sử dụng như sau:``` bash
freqtrade backtesting --strategy MyAwesomeStrategy --breakdown month year
`````` output
                                 MONTH BREAKDOWN
┏━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━┓
┃      Month ┃ Trades ┃ Tot Profit USDT ┃ Profit Factor ┃  Win  Draw  Loss  Win% ┃
┡━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━┩
│ 31/01/2020 │     12 │          44.451 │          7.28 │   10     0     2  83.3 │
│ 29/02/2020 │     30 │           45.41 │          2.36 │   17     0    13  56.7 │
│ 31/03/2020 │     35 │         142.024 │          2.42 │   14     0    21  40.0 │
│ 30/04/2020 │     67 │         -23.692 │          0.81 │   24     0    43  35.8 │
...
...
│ 30/04/2025 │    203 │          -63.43 │          0.81 │   73     0   130  36.0 │
│ 31/05/2025 │    142 │         104.675 │          1.28 │   59     0    83  41.5 │
│ 30/06/2025 │    177 │          -1.014 │           1.0 │   85     0    92  48.0 │
│ 31/07/2025 │    155 │         232.762 │           1.6 │   63     0    92  40.6 │
└────────────┴────────┴─────────────────┴───────────────┴────────────────────────┘
                                  YEAR BREAKDOWN
┏━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━┓
┃       Year ┃ Trades ┃ Tot Profit USDT ┃ Profit Factor ┃  Win  Draw  Loss  Win% ┃
┡━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━┩
│ 31/12/2020 │    896 │         868.889 │          1.46 │  351     0   545  39.2 │
│ 31/12/2021 │   1778 │        4487.163 │          1.93 │  745     0  1033  41.9 │
│ 31/12/2022 │   1736 │          938.27 │          1.27 │  698     0  1038  40.2 │
│ 31/12/2023 │   1712 │        1677.126 │          1.68 │  670     0  1042  39.1 │
│ 31/12/2024 │   1609 │        3198.424 │          2.22 │  773     0   836  48.0 │
│ 31/12/2025 │   1042 │         716.174 │          1.33 │  420     0   622  40.3 │
└────────────┴────────┴─────────────────┴───────────────┴────────────────────────┘
```Đầu ra sẽ hiển thị các bảng chứa lợi nhuận tuyệt đối đã thực hiện (bằng tiền đặt cược) trong khoảng thời gian đã chọn, cùng với các số liệu thống kê bổ sung như số lượng giao dịch, hệ số lợi nhuận và phân bổ số tiền thắng, hòa và thua đã xảy ra (đóng) trong khoảng thời gian này.

### Bộ nhớ đệm kết quả Backtest

Để tiết kiệm thời gian, theo mặc định, backtest sẽ sử dụng lại kết quả được lưu trong bộ nhớ đệm từ ngày cuối cùng khi chiến lược và cấu hình được backtest khớp với chiến lược và cấu hình của backtest trước đó. Để buộc thực hiện backtest mới bất chấp kết quả hiện có cho một lần chạy giống hệt, hãy chỉ định tham số `--cache none`.

!!! Cảnh báo
    Bộ nhớ đệm tự động bị tắt đối với các khoảng thời gian mở (`--timerange 20210101-`), vì freqtrade không thể đảm bảo một cách đáng tin cậy rằng dữ liệu cơ bản không thay đổi. Nó cũng có thể sử dụng các kết quả được lưu trong bộ nhớ đệm nếu không nên thực hiện kiểm tra ngược ban đầu thiếu dữ liệu ở cuối, điều này đã được khắc phục bằng cách tải thêm dữ liệu xuống.
    Trong trường hợp này, vui lòng sử dụng `--cache none` một lần để thực hiện backtest mới.

### Phân tích thêm kết quả backtest

Để phân tích sâu hơn kết quả kiểm tra ngược của bạn, freqtrade sẽ xuất các giao dịch thành tệp theo mặc định.
Sau đó, bạn có thể tải các giao dịch để thực hiện phân tích sâu hơn như được hiển thị trong phần kiểm tra lại [phân tích dữ liệu](strategy_analysis_example.md#load-backtest-results-to-pandas-dataframe).

Ngoài ra, bạn có thể sử dụng freqtrade trong [chế độ máy chủ web](freq-ui.md#backtesting) để trực quan hóa kết quả backtest trong giao diện web.
Chế độ này cũng cho phép bạn tải các kết quả backtest hiện có để bạn có thể phân tích chúng mà không cần chạy lại backtest.  
Đối với chế độ này - `--notes "<notes>"` có thể được sử dụng để thêm ghi chú vào kết quả kiểm tra ngược, kết quả này sẽ được hiển thị trong giao diện web.

### Tệp đầu ra Backtest

Tệp đầu ra mà freqtrade tạo ra là tệp zip chứa các tệp sau:

- Báo cáo backtest ở định dạng json
- Dữ liệu thay đổi thị trường ở dạng lông vũ
- Một bản sao của tập tin chiến lược
- Một bản sao của các tham số chiến lược (nếu sử dụng tệp tham số)
- Một bản sao đã được làm sạch của tập tin cấu hình

Điều này sẽ đảm bảo các kết quả có thể lặp lại được - với giả định rằng có sẵn dữ liệu tương tự.

Chỉ có tệp chiến lược và tệp cấu hình được bao gồm trong tệp zip, các phần phụ thuộc cuối cùng không được bao gồm.

## Giả định được thực hiện bằng cách kiểm tra lại

Vì việc kiểm tra lại thiếu một số thông tin chi tiết về những gì xảy ra trong một ngọn nến nên cần phải có một số giả định:

- Trao đổi [giới hạn giao dịch](#trading-limits-in-backtesting) được tôn trọng
- Các mục nhập diễn ra ở mức giá mở trừ khi logic giá tùy chỉnh đã được chỉ định
- Tất cả lệnh được khớp ở mức giá yêu cầu (không trượt giá) miễn là giá nằm trong vùng cao/thấp của nến
- Tín hiệu thoát xảy ra ở giá mở của nến liên tiếp
- Thoát khỏi vị trí giao dịch miễn phí cho giao dịch mới với một cặp khác
- Tín hiệu thoát được ưu tiên hơn Stoploss, vì tín hiệu thoát được cho là kích hoạt khi nến mở
- ROI
  - Số lần thoát được so sánh với mức cao - nhưng giá trị ROI được sử dụng (ví dụ: ROI = 2%, cao=5% - do đó số lần thoát sẽ ở mức 2%)
  - Điểm thoát không bao giờ "dưới nến", do đó ROI 2% có thể dẫn đến thoát ở mức 2,4% nếu mức thấp là lợi nhuận 2,4%
  - Các mục nhập ROI có hiệu lực trên nến kích hoạt (ví dụ: `120: 0,02` cho nến 1 giờ, từ `60: 0,05`) sẽ sử dụng giá mở cửa của nến làm tỷ lệ thoát
  - Buộc thoát do `<N>=-1` các mục nhập ROI sử dụng giá trị thoát thấp, trừ khi N rơi vào nến mở (ví dụ: `120: -1` cho nến 1h)- Việc thoát lệnh dừng xảy ra chính xác ở mức giá dừng lỗ, ngay cả khi mức thấp thấp hơn, nhưng mức lỗ sẽ cao hơn `2 * phí` so với giá dừng lỗ
- Điểm dừng lỗ được đánh giá trước ROI trong một cây nến. Vì vậy, bạn thường có thể thấy nhiều giao dịch hơn với lý do thoát `stoploss` so với kết quả thu được với cùng một chiến lược ở chế độ Giao dịch khô/Giao dịch trực tiếp
- Mức thấp xảy ra trước mức cao để dừng lỗ, bảo vệ vốn trước
- Trailing stoploss
  - Trailing Stoploss chỉ được điều chỉnh nếu nó ở dưới mức thấp của nến (nếu không nó sẽ được kích hoạt)
  - Trên các nến vào lệnh giao dịch kích hoạt điểm dừng lỗ theo sau, giả định "mức chênh lệch tối thiểu" (`stop_posit_offset`) (thay vì mức cao) - và điểm dừng được tính từ thời điểm này. Quy tắc này KHÔNG áp dụng cho các trường hợp dừng lỗ tùy chỉnh vì không có thông tin nào về logic dừng lỗ.
  - Mức cao xảy ra trước - điều chỉnh mức dừng lỗ
  - Thấp sử dụng mức dừng lỗ đã điều chỉnh (vì vậy các lệnh thoát có chênh lệch cao-thấp lớn sẽ được kiểm tra lại chính xác)
  - ROI áp dụng trước điểm dừng treo, đảm bảo lợi nhuận được "giới hạn cao nhất" ở ROI nếu áp dụng cả ROI và điểm dừng treo
- Lý do thoát không giải thích giao dịch là dương hay âm, chỉ là điều gì đã kích hoạt lệnh thoát (điều này có thể trông kỳ lạ nếu sử dụng giá trị ROI âm)
- Trình tự đánh giá (nếu có nhiều tín hiệu xảy ra trên cùng một cây nến)
  - Tín hiệu thoát
  - Dừng lỗ
  - ROI
  - Trailing stoploss
- Đảo ngược vị thế (chỉ hợp đồng tương lai) xảy ra nếu tín hiệu vào lệnh theo hướng khác với hướng giao dịch đóng được kích hoạt tại nến mà giao dịch hiện tại đóng lại.

Dựa trên những giả định này, việc kiểm tra ngược sẽ cố gắng phản ánh giao dịch thực tế càng sát càng tốt. Tuy nhiên, việc kiểm tra lại sẽ **không bao giờ** thay thế việc chạy chiến lược ở chế độ chạy thử.
Ngoài ra, hãy nhớ rằng kết quả trong quá khứ không đảm bảo thành công trong tương lai.

Ngoài các giả định trên, tác giả chiến lược nên đọc kỹ phần [Những sai lầm thường gặp](strategy-customization.md#common-mistakes-when-development-strategies) để tránh sử dụng dữ liệu trong quá trình kiểm tra ngược không có sẵn trong điều kiện thị trường thực tế.

### Giới hạn giao dịch khi kiểm tra lại

Các sàn giao dịch có các giới hạn giao dịch nhất định, như tiền tệ cơ sở tối thiểu (và tối đa), hoặc tiền tệ đặt cược (báo giá) tối thiểu/tối đa.
Các giới hạn này thường được liệt kê trong tài liệu trao đổi dưới dạng "quy tắc giao dịch" hoặc tương tự và có thể khá khác nhau giữa các cặp khác nhau.

Kiểm tra ngược (cũng như chạy trực tiếp và chạy thử) tôn trọng các giới hạn này và sẽ đảm bảo rằng mức dừng lỗ có thể được đặt dưới giá trị này - vì vậy giá trị sẽ cao hơn một chút so với giá trị sàn giao dịch chỉ định.
Tuy nhiên, Freqtrade không có thông tin về giới hạn lịch sử.

Điều này có thể dẫn đến tình huống trong đó giới hạn giao dịch bị tăng cao bằng cách sử dụng giá lịch sử, dẫn đến số tiền tối thiểu > 50\$.

Ví dụ:

Số tiền có thể giao dịch tối thiểu của BTC là 0,001.
BTC giao dịch ở mức 22.000\$ hôm nay (0,001 BTC có liên quan đến điều này) - nhưng giai đoạn kiểm tra lại bao gồm các mức giá cao tới 50.000\$.
Mức tối thiểu hôm nay sẽ là `0,001 * 22_000` - hoặc 22\$.  
Tuy nhiên, giới hạn cũng có thể là 50$ - dựa trên `0,001 * 50_000` trong một số bối cảnh lịch sử.

#### Giới hạn độ chính xác của giao dịch

Hầu hết các sàn giao dịch đều đặt ra giới hạn chính xác về cả giá cả và số lượng, vì vậy bạn không thể mua 1,0020401 một cặp hoặc ở mức giá 1,24567123123.  
Thay vào đó, những mức giá và số tiền này sẽ được làm tròn hoặc cắt bớt (dựa trên định nghĩa trao đổi) theo độ chính xác giao dịch đã xác định.
Ví dụ: các giá trị trên có thể được làm tròn thành số 1,002 và giá là 1,24567.Các giá trị độ chính xác này dựa trên giới hạn trao đổi hiện tại (như được mô tả trong [phần trên](#trading-limits-in-backtesting)), vì không có sẵn giới hạn độ chính xác trước đây.

## Cải thiện độ chính xác của backtest

Một hạn chế lớn của việc kiểm tra lại là không thể biết giá di chuyển như thế nào trong nến (đã cao trước khi đóng cửa hay ngược lại?).
Vì vậy, giả sử bạn chạy backtesting với khung thời gian 1h thì sẽ có 4 mức giá cho cây nến đó (Mở, Cao, Thấp, Đóng).

Mặc dù việc kiểm tra ngược có một số giả định (đọc ở trên) về điều này - nhưng điều này không bao giờ có thể hoàn hảo và sẽ luôn bị sai lệch theo cách này hay cách khác.
Để giảm thiểu điều này, freqtrade có thể sử dụng khung thời gian thấp hơn (nhanh hơn) để mô phỏng chuyển động trong nến.

Để sử dụng điều này, bạn có thể thêm `--timeframe-detail 5m` vào lệnh kiểm tra ngược thông thường của mình.``` bash
freqtrade backtesting --strategy AwesomeStrategy --timeframe 1h --timeframe-detail 5m
```Điều này sẽ tải dữ liệu 1h (khung thời gian chính) cũng như dữ liệu 5 phút (khung thời gian chi tiết) cho phạm vi thời gian đã chọn.
Chiến lược sẽ được phân tích với khung thời gian 1h.
Các nến nơi hoạt động có thể diễn ra (có tín hiệu đang hoạt động, cặp tiền đang giao dịch) được đánh giá ở khung thời gian 5 phút.
Điều này sẽ cho phép mô phỏng chính xác hơn các chuyển động trong nến - và có thể dẫn đến các kết quả khác nhau, đặc biệt là trên các khung thời gian cao hơn.

Các mục nhập thường sẽ vẫn diễn ra khi nến chính mở cửa, tuy nhiên các vị trí giao dịch được giải phóng có thể được giải phóng sớm hơn (nếu tín hiệu thoát được kích hoạt trên nến 5m), sau đó có thể được sử dụng cho giao dịch mới của một cặp khác.

Tất cả các hàm gọi lại (`custom_exit()`, `custom_stoploss()`, ... ) sẽ chạy cho mỗi cây nến dài 5 phút sau khi giao dịch được mở (tức là 12 lần trong ví dụ trên về khung thời gian 1h và khung thời gian chi tiết 5 phút).

`--timeframe-detail` phải nhỏ hơn khung thời gian ban đầu, nếu không quá trình kiểm tra lại sẽ không bắt đầu được.

Rõ ràng điều này sẽ yêu cầu nhiều bộ nhớ hơn (dữ liệu 5 triệu lớn hơn dữ liệu 1 giờ) và cũng sẽ ảnh hưởng đến thời gian chạy (tùy thuộc vào số lượng giao dịch và thời lượng giao dịch).
Ngoài ra, dữ liệu phải có sẵn/tải xuống rồi.

!!! Mẹo
    Bạn có thể sử dụng chức năng này như là phần cuối cùng của quá trình phát triển chiến lược, để đảm bảo chiến lược của bạn không khai thác một trong các [giả định kiểm tra lại](#assumptions-made-by-backtesting). Các chiến lược hoạt động tốt tương tự với chế độ này cũng có cơ hội hoạt động tốt ở chế độ khô/trực tiếp (mặc dù chỉ thử nghiệm chuyển tiếp (chế độ khô) mới thực sự có thể xác nhận chiến lược).

??? Mẫu "Ví dụ cực kỳ khác biệt"
    Việc sử dụng `--timeframe-detail` trong một ví dụ điển hình (tất cả các cặp bên dưới đều có nến 10:00 với tín hiệu vào lệnh) có thể dẫn đến việc kiểm tra lại chuỗi Giao dịch sau với 1 max_open_trades:

    | Cặp | Thời gian vào | Thời gian thoát | Thời lượng |
    |------|-------------|----------| -------- |
    | BTC/USDT | 2024-01-01 10:00:00 | 2021-01-01 10:05:00 | 5m |
    | ETH/USDT | 2024-01-01 10:05:00 | 2021-01-01 10:15:00 | 10m |
    | XRP/USDT | 2024-01-01 10:15:00 | 2021-01-01 10:30:00 | 15m |
    | SOL/USDT | 2024-01-01 10:15:00 | 2021-01-01 11:05:00 | 50m |
    | BTC/USDT | 2024-01-01 11:05:00 | 2021-01-01 12:00:00 | 55m |

    Nếu không có chi tiết về khung thời gian, nó sẽ trông như sau:

    | Cặp | Thời gian vào | Thời gian thoát | Thời lượng |
    |------|-------------|----------| -------- |
    | BTC/USDT | 2024-01-01 10:00:00 | 2021-01-01 11:00:00 | 1h |
    | BTC/USDT | 2024-01-01 11:00:00 | 2021-01-01 12:00:00 | 1h |

    Sự khác biệt là đáng kể, vì không có dữ liệu chi tiết, chỉ các tín hiệu `max_open_trades` đầu tiên trên mỗi nến được đánh giá và các vị trí giao dịch chỉ được giải phóng ở cuối nến, cho phép mở giao dịch mới ở nến tiếp theo.


## Kiểm tra lại nhiều chiến lược

Để so sánh nhiều chiến lược, một danh sách các Chiến lược có thể được cung cấp để kiểm tra lại.

Điều này được giới hạn ở 1 giá trị khung thời gian cho mỗi lần chạy. Tuy nhiên, dữ liệu chỉ được tải một lần từ đĩa nên nếu bạn có nhiều
các chiến lược bạn muốn so sánh, điều này sẽ giúp tăng thời gian chạy tốt hơn.

Tất cả các Chiến lược được liệt kê cần phải nằm trong cùng một thư mục, trừ khi `--recursive-strategy-search` cũng được chỉ định, trong đó các thư mục con trong thư mục chiến lược cũng được xem xét.``` bash
freqtrade backtesting --timerange 20180401-20180410 --timeframe 5m --strategy-list Strategy001 Strategy002 --export trades
```Thao tác này sẽ lưu kết quả vào `user_data/backtest_results/backtest-result-<datetime>.json`, bao gồm kết quả cho cả `Strategy001` và `Strategy002`.
Sẽ có thêm một bảng so sánh thắng/thua của các chiến lược khác nhau (giống với hàng “Tổng” ở bảng đầu tiên).
Đầu ra chi tiết cho tất cả các chiến lược lần lượt sẽ có sẵn, vì vậy hãy nhớ cuộn lên để xem chi tiết cho mỗi chiến lược.```
================================================== STRATEGY SUMMARY ===================================================================
| Strategy    |  Trades |   Avg Profit % |   Tot Profit BTC |   Tot Profit % | Avg Duration   |  Wins |  Draws | Losses | Drawdown % |
|-------------+---------+----------------+------------------+----------------+----------------+-------+--------+--------+------------|
| Strategy1   |     429 |           0.36 |       0.00762792 |          76.20 | 4:12:00        |   186 |      0 |    243 |       45.2 |
| Strategy2   |    1487 |          -0.13 |      -0.00988917 |         -98.79 | 4:43:00        |   662 |      0 |    825 |     241.68 |
```## Bước tiếp theo

Tuyệt vời, chiến lược của bạn có lợi nhuận. Điều gì sẽ xảy ra nếu bot có thể cung cấp cho bạn các thông số tối ưu để sử dụng cho chiến lược của bạn?
Bước tiếp theo của bạn là tìm hiểu [cách tìm thông số tối ưu với Hyperopt](hyperopt.md)