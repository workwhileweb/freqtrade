<!-- Auto-translated from docs/ by script. Please review technical terms. -->

# Vẽ đồ thị

Trang này giải thích cách vẽ biểu đồ giá, chỉ số và lợi nhuận.

!!! Cảnh báo "Không dùng nữa"
    Các lệnh được mô tả trong trang này (`plot-dataframe`, `plot-profit`) sẽ được coi là không dùng nữa và đang ở chế độ bảo trì.
    Điều này chủ yếu là do các vấn đề về hiệu suất mà ngay cả các ô có kích thước trung bình cũng có thể gây ra, nhưng cũng vì "lưu trữ tệp và mở tệp trong trình duyệt" không trực quan lắm từ góc độ giao diện người dùng.

    Mặc dù không có kế hoạch ngay lập tức để loại bỏ chúng nhưng chúng không được duy trì tích cực - và có thể bị loại bỏ trong thời gian ngắn nếu cần có những thay đổi lớn để duy trì hoạt động của chúng.
    
    Vui lòng sử dụng [FreqUI](freq-ui.md) cho nhu cầu vẽ đồ thị, điều này không gây khó khăn cho các vấn đề về hiệu suất tương tự.

## Cài đặt / Thiết lập

Các mô-đun vẽ đồ thị sử dụng thư viện Plotly. Bạn có thể cài đặt/nâng cấp cái này bằng cách chạy lệnh sau:``` bash
pip install -U -r requirements-plot.txt
```## Giá lô và các chỉ số

Lệnh phụ `freqtradeplot-dataframe` hiển thị một biểu đồ tương tác với ba ô phụ:

* Cốt truyện chính với chân nến và các chỉ báo theo giá (sma/ema)
* Thanh âm lượng
* Các chỉ báo bổ sung được chỉ định bởi `--indicators2`

![plot-dataframe](assets/plot-dataframe.png)

Các đối số có thể có:

--8<-- "lệnh/plot-dataframe.md"

Ví dụ:``` bash
freqtrade plot-dataframe -p BTC/ETH --strategy AwesomeStrategy
```Đối số `-p/--pairs` có thể được sử dụng để chỉ định các cặp bạn muốn vẽ.

!!! Lưu ý
    Lệnh phụ `freqtradeplot-dataframe` tạo ra một tệp cốt truyện cho mỗi cặp.

Chỉ định các chỉ số tùy chỉnh.
Sử dụng `--indicators1` cho ô chính và `--indicators2` cho ô phụ bên dưới (nếu các giá trị nằm trong phạm vi khác với giá).``` bash
freqtrade plot-dataframe --strategy AwesomeStrategy -p BTC/ETH --indicators1 sma ema --indicators2 macd
```### Ví dụ sử dụng khác

Để vẽ nhiều cặp, hãy phân tách chúng bằng dấu cách:``` bash
freqtrade plot-dataframe --strategy AwesomeStrategy -p BTC/ETH XRP/ETH
```Để vẽ một khoảng thời gian (để phóng to)``` bash
freqtrade plot-dataframe --strategy AwesomeStrategy -p BTC/ETH --timerange=20180801-20180805
```Để vẽ biểu đồ các giao dịch được lưu trữ trong cơ sở dữ liệu, hãy sử dụng `--db-url` kết hợp với `--trade-source DB`:``` bash
freqtrade plot-dataframe --strategy AwesomeStrategy --db-url sqlite:///tradesv3.dry_run.sqlite -p BTC/ETH --trade-source DB
```Để vẽ giao dịch từ kết quả kiểm tra ngược, hãy sử dụng `--export-filename <filename>```` bash
freqtrade plot-dataframe --strategy AwesomeStrategy --export-filename user_data/backtest_results/backtest-result.json -p BTC/ETH
```### Vẽ biểu đồ cơ bản về khung dữ liệu

![plot-dataframe2](asset/plot-dataframe2.png)

Lệnh phụ `plot-dataframe` yêu cầu kiểm tra lại dữ liệu, chiến lược và tệp kết quả kiểm tra lại hoặc cơ sở dữ liệu, chứa các giao dịch tương ứng với chiến lược.

Biểu đồ kết quả sẽ có các yếu tố sau:

* Tam giác xanh: Tín hiệu mua từ chiến lược. (Lưu ý: không phải mọi tín hiệu mua đều tạo ra giao dịch, hãy so sánh với các vòng tròn màu lục lam.)
* Tam giác màu đỏ: Tín hiệu bán từ chiến lược. (Ngoài ra, không phải mọi tín hiệu bán đều kết thúc giao dịch, so sánh với các ô vuông màu đỏ và xanh lục.)
* Vòng tròn màu lục lam: Điểm vào giao dịch.
* Red squares: Trade exit points for trades with loss or 0% profit.
* Hình vuông màu xanh lá cây: Điểm thoát giao dịch để có giao dịch sinh lời.
* Các chỉ báo có giá trị tương ứng với thang nến (ví dụ: SMA/EMA), như được chỉ định bằng `--indicators1`.
* Khối lượng (biểu đồ thanh ở cuối biểu đồ chính).
* Các chỉ báo có giá trị ở các thang đo khác nhau (ví dụ: MACD, RSI) bên dưới các thanh âm lượng, như được chỉ định bằng `--indicators2`.

!!! Lưu ý "Dải Bollinger"
    Dải Bollinger được tự động thêm vào biểu đồ nếu các cột `bb_lowband` và `bb_upperband` tồn tại và được vẽ dưới dạng một vùng màu xanh nhạt trải dài từ dải dưới đến dải trên.

#### Cấu hình cốt truyện nâng cao

Cấu hình sơ đồ nâng cao có thể được chỉ định trong chiến lược trong tham số `plot_config`.

Các tính năng bổ sung khi sử dụng `plot_config` bao gồm:

* Chỉ định màu sắc cho mỗi chỉ báo
* Chỉ định các ô phụ bổ sung
* Chỉ định các cặp chỉ báo để lấp đầy vùng ở giữa

Cấu hình ô mẫu bên dưới chỉ định màu cố định cho các chỉ báo. Nếu không, các ô liên tiếp có thể tạo ra các cách phối màu khác nhau mỗi lần, khiến việc so sánh trở nên khó khăn.
Nó cũng cho phép nhiều ô phụ hiển thị cả MACD và RSI cùng một lúc.

Loại lô có thể được cấu hình bằng phím `type`. Các loại có thể là:

* `scatter` tương ứng với một biểu đồ phân tán.
* `bar` tương ứng với một biểu đồ thanh.

Các tham số bổ sung cho hàm tạo `plotly.graph_objects.*` có thể được chỉ định trong `plotly` dict - những tham số này chỉ được hỗ trợ khi sử dụng Plotly làm thư viện vẽ đồ thị và sẽ bị bỏ qua khi sử dụng freq-ui.

Cấu hình mẫu với các nhận xét nội tuyến giải thích quy trình:``` python
@property
def plot_config(self):
    """
        There are a lot of solutions how to build the return dictionary.
        The only important point is the return value.
        Example:
            plot_config = {'main_plot': {}, 'subplots': {}}

    """
    plot_config = {}
    plot_config['main_plot'] = {
        # Configuration for main plot indicators.
        # Assumes 2 parameters, emashort and emalong to be specified.
        f'ema_{self.emashort.value}': {'color': 'red'},
        f'ema_{self.emalong.value}': {'color': '#CCCCCC'},
        # By omitting color, a random color is selected.
        'sar': {},
        # fill area between senkou_a and senkou_b
        'senkou_a': {
            'color': 'green', #optional
            'fill_to': 'senkou_b',
            'fill_label': 'Ichimoku Cloud', #optional
            'fill_color': 'rgba(255,76,46,0.2)', #optional
        },
        # plot senkou_b, too. Not only the area to it.
        'senkou_b': {}
    }
    plot_config['subplots'] = {
         # Create subplot MACD
        "MACD": {
            'macd': {'color': 'blue', 'fill_to': 'macdhist'},
            'macdsignal': {'color': 'orange'},
            'macdhist': {'type': 'bar', 'plotly': {'opacity': 0.9}}
        },
        # Additional subplot RSI
        "RSI": {
            'rsi': {'color': 'red'}
        }
    }

    return plot_config
```??? Lưu ý "Là thuộc tính (phương thức cũ)"
    Cũng có thể gán `plot_config` dưới dạng Thuộc tính (đây từng là cách mặc định).
    Điều này có nhược điểm là không có sẵn các tham số chiến lược, ngăn cản một số cấu hình nhất định hoạt động.``` python
        plot_config = {
            'main_plot': {
                # Configuration for main plot indicators.
                # Specifies `ema10` to be red, and `ema50` to be a shade of gray
                'ema10': {'color': 'red'},
                'ema50': {'color': '#CCCCCC'},
                # By omitting color, a random color is selected.
                'sar': {},
            # fill area between senkou_a and senkou_b
            'senkou_a': {
                'color': 'green', #optional
                'fill_to': 'senkou_b',
                'fill_label': 'Ichimoku Cloud', #optional
                'fill_color': 'rgba(255,76,46,0.2)', #optional
            },
            # plot senkou_b, too. Not only the area to it.
            'senkou_b': {}
            },
            'subplots': {
                # Create subplot MACD
                "MACD": {
                    'macd': {'color': 'blue', 'fill_to': 'macdhist'},
                    'macdsignal': {'color': 'orange'},
                    'macdhist': {'type': 'bar', 'plotly': {'opacity': 0.9}}
                },
                # Additional subplot RSI
                "RSI": {
                    'rsi': {'color': 'red'}
                }
            }
        }

    ```!!! Lưu ý
    Cấu hình trên giả định rằng `ema10`, `ema50`, `senkou_a`, `senkou_b`,
    `macd`, `macdsignal`, `macdhist` và `rsi` là các cột trong DataFrame được tạo bởi chiến lược.

!!! Cảnh báo
    Các đối số `plotly` chỉ được hỗ trợ với thư viện âm mưu và sẽ không hoạt động với freq-ui.

!!! Lưu ý "Điều chỉnh vị thế giao dịch"
    Nếu sử dụng `position_ adjustment_enable` / ` adjustment_trade_position()`, giá mua ban đầu của giao dịch được tính trung bình trên nhiều lệnh và giá bắt đầu giao dịch rất có thể sẽ xuất hiện bên ngoài phạm vi nến.

## Âm mưu lợi nhuận

![plot-profit](assets/plot-profit.png)

Lệnh phụ `plot-profit` hiển thị biểu đồ tương tác với ba biểu đồ:

* Giá đóng cửa trung bình cho tất cả các cặp.
* Lợi nhuận tóm tắt được thực hiện bằng cách kiểm tra lại.
Lưu ý rằng đây không phải là lợi nhuận thực tế mà chỉ là ước tính.
* Lợi nhuận cho mỗi cặp cá nhân.
* Tính song song của các giao dịch.
* Dưới nước (Giai đoạn rút tiền).

Biểu đồ đầu tiên giúp bạn nắm bắt được diễn biến chung của thị trường.

Biểu đồ thứ hai sẽ hiển thị liệu thuật toán của bạn có hoạt động hay không.
Có lẽ bạn muốn một thuật toán có thể tạo ra những khoản lợi nhuận nhỏ một cách đều đặn hoặc một thuật toán hoạt động ít thường xuyên hơn nhưng tạo ra những biến động lớn.
Biểu đồ này cũng sẽ làm nổi bật thời điểm bắt đầu (và kết thúc) của khoảng thời gian rút vốn tối đa.

Biểu đồ thứ ba có thể hữu ích để phát hiện các ngoại lệ, các sự kiện theo cặp khiến lợi nhuận tăng đột biến.

Biểu đồ thứ tư có thể giúp bạn phân tích tính song song của giao dịch, cho biết tần suất max_open_trades đã được tối đa hóa.

Các tùy chọn có thể có cho lệnh phụ `freqtrade cốt truyện-lợi nhuận`:

--8<-- "lệnh/plot-profit.md"

Đối số `-p/--pairs`, có thể được sử dụng để giới hạn các cặp được xem xét cho phép tính này.

Ví dụ:

Sử dụng tệp xuất backtest tùy chỉnh``` bash
freqtrade plot-profit  -p LTC/BTC --export-filename user_data/backtest_results/backtest-result.json
```Sử dụng cơ sở dữ liệu tùy chỉnh``` bash
freqtrade plot-profit  -p LTC/BTC --db-url sqlite:///tradesv3.sqlite --trade-source DB
`````` bash
freqtrade --datadir user_data/data/binance_save/ plot-profit -p LTC/BTC
```