<!-- Auto-translated from docs/ by script. Please review technical terms. -->

# Ví dụ phân tích chiến lược

Gỡ lỗi một chiến lược có thể tốn thời gian. Freqtrade cung cấp các chức năng trợ giúp để trực quan hóa dữ liệu thô.
Phần sau đây giả sử bạn làm việc với SampleStrategy, dữ liệu trong khung thời gian 5m từ Binance và đã tải chúng xuống thư mục dữ liệu ở vị trí mặc định.Please follow the [documentation](https://www.freqtrade.io/en/stable/data-download/) for more details.
## Thiết lập

### Thay đổi thư mục Working thành kho lưu trữ gốc```python
import os
from pathlib import Path


# Change directory
# Modify this cell to insure that the output shows the correct path.
# Define all paths relative to the project root shown in the cell output
project_root = "somedir/freqtrade"
i = 0
try:
    os.chdir(project_root)
    if not Path("LICENSE").is_file():
        i = 0
        while i < 4 and (not Path("LICENSE").is_file()):
            os.chdir(Path(Path.cwd(), "../"))
            i += 1
        project_root = Path.cwd()
except FileNotFoundError:
    print("Please define the project root relative to the current directory")
print(Path.cwd())
```### Định cấu hình môi trường Freqtrade```python
from freqtrade.configuration import Configuration


# Customize these according to your needs.

# Initialize empty configuration object
config = Configuration.from_files([])
# Optionally (recommended), use existing configuration file
# config = Configuration.from_files(["user_data/config.json"])

# Define some constants
config["timeframe"] = "5m"
# Name of the strategy class
config["strategy"] = "SampleStrategy"
# Location of the data
data_location = config["datadir"]
# Pair to analyze - Only use one pair here
pair = "BTC/USDT"
``````python
# Load data using values set above
from freqtrade.data.history import load_pair_history
from freqtrade.enums import CandleType


candles = load_pair_history(
    datadir=data_location,
    timeframe=config["timeframe"],
    pair=pair,
    data_format="json",  # Make sure to update this to your data
    candle_type=CandleType.SPOT,
)

# Confirm success
print(f"Loaded {len(candles)} rows of data for {pair} from {data_location}")
candles.head()
```## Load and run strategy
* Chạy lại mỗi khi tệp chiến lược được thay đổi```python
# Load strategy using values set above
from freqtrade.data.dataprovider import DataProvider
from freqtrade.resolvers import StrategyResolver


strategy = StrategyResolver.load_strategy(config)
strategy.dp = DataProvider(config, None, None)
strategy.ft_bot_start()

# Generate buy/sell signals using strategy
df = strategy.analyze_ticker(candles, {"pair": pair})
df.tail()
```### Hiển thị chi tiết giao dịch

* Lưu ý rằng việc sử dụng `data.head()` cũng có tác dụng, tuy nhiên hầu hết các chỉ báo đều có một số dữ liệu "khởi động" ở đầu khung dữ liệu.
* Một số vấn đề có thể xảy ra
    * Các cột có giá trị NaN ở cuối khung dữ liệu
    * Các cột được sử dụng trong hàm `crossed*()` với đơn vị hoàn toàn khác nhau
* So sánh với backtest đầy đủ
    * có 200 tín hiệu mua làm đầu ra cho một cặp từ `analyze_ticker()` không nhất thiết có nghĩa là 200 giao dịch sẽ được thực hiện trong quá trình kiểm tra lại.
    * Giả sử bạn chỉ sử dụng một điều kiện, chẳng hạn như `df['rsi'] < 30` làm điều kiện mua, điều này sẽ tạo ra nhiều tín hiệu "mua" cho từng cặp theo trình tự (cho đến khi rsi trả về > 29). Bot sẽ chỉ mua theo tín hiệu đầu tiên trong số này (và cũng chỉ khi vị trí giao dịch ("max_open_trades") vẫn khả dụng) hoặc theo một trong các tín hiệu ở giữa, ngay khi có "khe".```python
# Report results
print(f"Generated {df['enter_long'].sum()} entry signals")
data = df.set_index("date", drop=False)
data.tail()
```## Tải các đối tượng hiện có vào sổ ghi chép Jupyter

Các ô sau đây giả định rằng bạn đã tạo dữ liệu bằng cli.  
Chúng sẽ cho phép bạn tìm hiểu sâu hơn về kết quả của mình và thực hiện phân tích, nếu không sẽ khiến kết quả đầu ra rất khó tiêu hóa do quá tải thông tin.

### Tải kết quả backtest vào khung dữ liệu gấu trúc

Phân tích khung dữ liệu giao dịch (cũng được sử dụng bên dưới để vẽ đồ thị)```python
from freqtrade.data.btanalysis import load_backtest_data, load_backtest_stats


# if backtest_dir points to a directory, it'll automatically load the last backtest file.
backtest_dir = config["user_data_dir"] / "backtest_results"
# backtest_dir can also point to a specific file
# backtest_dir = (
#   config["user_data_dir"] / "backtest_results/backtest-result-2020-07-01_20-04-22.json"
# )
``````python
# You can get the full backtest statistics by using the following command.
# This contains all information used to generate the backtest result.
stats = load_backtest_stats(backtest_dir)

strategy = "SampleStrategy"
# All statistics are available per strategy, so if `--strategy-list` was used during backtest,
# this will be reflected here as well.
# Example usages:
print(stats["strategy"][strategy]["results_per_pair"])
# Get pairlist used for this backtest
print(stats["strategy"][strategy]["pairlist"])
# Get market change (average change of all pairs from start to end of the backtest period)
print(stats["strategy"][strategy]["market_change"])
# Maximum drawdown ()
print(stats["strategy"][strategy]["max_drawdown_abs"])
# Maximum drawdown start and end
print(stats["strategy"][strategy]["drawdown_start"])
print(stats["strategy"][strategy]["drawdown_end"])


# Get strategy comparison (only relevant if multiple strategies were compared)
print(stats["strategy_comparison"])
``````python
# Load backtested trades as dataframe
trades = load_backtest_data(backtest_dir)

# Show value-counts per pair
trades.groupby("pair")["exit_reason"].value_counts()
```## Vẽ đường lợi nhuận / vốn chủ sở hữu hàng ngày```python
# Plotting equity line (starting with 0 on day 1 and adding daily profit for each backtested day)

import pandas as pd
import plotly.express as px

from freqtrade.configuration import Configuration
from freqtrade.data.btanalysis import load_backtest_stats


# strategy = 'SampleStrategy'
# config = Configuration.from_files(["user_data/config.json"])
# backtest_dir = config["user_data_dir"] / "backtest_results"

stats = load_backtest_stats(backtest_dir)
strategy_stats = stats["strategy"][strategy]

df = pd.DataFrame(columns=["dates", "equity"], data=strategy_stats["daily_profit"])
df["equity_daily"] = df["equity"].cumsum()

fig = px.line(df, x="dates", y="equity_daily")
fig.show()
```### Tải kết quả giao dịch trực tiếp vào khung dữ liệu gấu trúc

Trong trường hợp bạn đã thực hiện một số giao dịch và muốn phân tích hiệu suất của mình```python
from freqtrade.data.btanalysis import load_trades_from_db


# Fetch trades from database
trades = load_trades_from_db("sqlite:///tradesv3.sqlite")

# Display results
trades.groupby("pair")["exit_reason"].value_counts()
```## Phân tích các giao dịch đã tải để biết tính song song của giao dịch
Điều này có thể hữu ích để tìm tham số `max_open_trades` tốt nhất, khi được sử dụng với kiểm tra ngược kết hợp với cài đặt `max_open_trades` rất cao.

`analyze_trade_parallelism()` trả về khung dữ liệu chuỗi thời gian với cột "open_trades", chỉ định số lượng giao dịch mở cho mỗi nến.```python
from freqtrade.data.btanalysis import analyze_trade_parallelism


# Analyze the above
parallel_trades = analyze_trade_parallelism(trades, "5m")

parallel_trades.plot()
```## Vẽ kết quả

Freqtrade cung cấp khả năng vẽ đồ thị tương tác dựa trên cốt truyện.```python
from freqtrade.plot.plotting import generate_candlestick_graph


# Limit graph period to keep plotly quick and reactive

# Filter trades to one pair
trades_red = trades.loc[trades["pair"] == pair]

data_red = data["2019-06-01":"2019-06-10"]
# Generate candlestick graph
graph = generate_candlestick_graph(
    pair=pair,
    data=data_red,
    trades=trades_red,
    indicators1=["sma20", "ema50", "ema55"],
    indicators2=["rsi", "macd", "macdsignal", "macdhist"],
)
``````python
# Show graph inline
# graph.show()

# Render graph in a separate window
graph.show(renderer="browser")
```## Vẽ lợi nhuận trung bình trên mỗi giao dịch dưới dạng biểu đồ phân phối```python
import plotly.figure_factory as ff


hist_data = [trades.profit_ratio]
group_labels = ["profit_ratio"]  # name of the dataset

fig = ff.create_distplot(hist_data, group_labels, bin_size=0.01)
fig.show()
```Vui lòng gửi vấn đề hoặc Yêu cầu kéo nâng cao tài liệu này nếu bạn muốn chia sẻ ý tưởng về cách phân tích dữ liệu tốt nhất.