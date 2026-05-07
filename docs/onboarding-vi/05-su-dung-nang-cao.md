# 05. Sử dụng nâng cao

Tài liệu này dành cho **power user** — đã chạy thành thạo dry-run, muốn
khai thác sâu các cơ chế nâng cao của Freqtrade. Mỗi mục đều dẫn link
sang docs gốc và file source để bạn đào sâu.

> Đọc trước: [01](01-nguyen-tac-hoat-dong.md) (vòng đời bot) và
> [04](04-cai-dat-chay-su-dung.md) (chạy/điều khiển bot).

## Mục lục

- [1. Strategy nâng cao](#1-strategy-nâng-cao)
- [2. Pairlist chain động](#2-pairlist-chain-động)
- [3. Protections](#3-protections)
- [4. Hyperopt nâng cao](#4-hyperopt-nâng-cao)
- [5. Backtest sâu & analysis](#5-backtest-sâu--analysis)
- [6. FreqAI](#6-freqai)
- [7. Futures / Leverage / Short](#7-futures--leverage--short)
- [8. Multi-bot — Producer/Consumer](#8-multi-bot--producerconsumer)
- [9. Webhook & tích hợp ngoài](#9-webhook--tích-hợp-ngoài)
- [10. Orderflow & dữ liệu trades](#10-orderflow--dữ-liệu-trades)
- [11. Vận hành nâng cao](#11-vận-hành-nâng-cao)
- [12. Plotting & data analysis](#12-plotting--data-analysis)
- [13. Migration & deprecated](#13-migration--deprecated)

---

## 1. Strategy nâng cao

Tham chiếu: [`docs/strategy-customization.md`](../strategy-customization.md),
[`docs/strategy-advanced.md`](../strategy-advanced.md),
[`docs/strategy-callbacks.md`](../strategy-callbacks.md).

### 1.1. Cấu trúc class

Mọi strategy kế thừa
[`IStrategy`](../../freqtrade/strategy/interface.py) (xem `INTERFACE_VERSION = 3`).
Các thuộc tính class quan trọng:

```python
class MyStrategy(IStrategy):
    INTERFACE_VERSION = 3
    can_short = False                 # bật short cho futures/margin
    timeframe = "5m"
    process_only_new_candles = True   # chỉ analyze khi có nến mới
    startup_candle_count = 200        # số nến cần warm-up trước tín hiệu

    minimal_roi = {"0": 0.04, "30": 0.02, "60": 0.01}
    stoploss = -0.10
    trailing_stop = False
    use_exit_signal = True
    exit_profit_only = False
    ignore_roi_if_entry_signal = False

    order_types = {
        "entry": "limit",
        "exit": "limit",
        "stoploss": "limit",
        "stoploss_on_exchange": False,
    }
    order_time_in_force = {"entry": "GTC", "exit": "GTC"}
    position_adjustment_enable = False
    max_entry_position_adjustment = 3

    plot_config = {...}
    protections = [...]               # có thể đặt ở config
```

### 1.2. Bộ ba bắt buộc

```python
def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
    dataframe["rsi"] = ta.RSI(dataframe, timeperiod=14)
    return dataframe

def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
    dataframe.loc[dataframe["rsi"] < 30, ["enter_long", "enter_tag"]] = (1, "rsi_oversold")
    return dataframe

def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
    dataframe.loc[dataframe["rsi"] > 70, ["exit_long", "exit_tag"]] = (1, "rsi_overbought")
    return dataframe
```

### 1.3. Callbacks nâng cao

Toàn bộ callback có sẵn (chi tiết
[`docs/strategy-callbacks.md`](../strategy-callbacks.md)):

| Callback | Mục đích |
|----------|----------|
| `bot_start(self)` | Init dữ liệu nội bộ khi bot khởi động |
| `bot_loop_start(self, current_time)` | Đầu mỗi iteration |
| `confirm_trade_entry(...)` | Cho phép / từ chối entry trước khi đặt lệnh |
| `confirm_trade_exit(...)` | Cho phép / từ chối exit |
| `custom_entry_price(...)` | Đặt giá entry tuỳ ý |
| `custom_exit_price(...)` | Đặt giá exit tuỳ ý |
| `custom_stake_amount(...)` | Đặt size lệnh tuỳ pair / điều kiện |
| `custom_stoploss(...)` | Tính stoploss động per-trade |
| `custom_exit(...)` | Quyết định thoát theo logic riêng |
| `custom_roi(...)` | Tuỳ chỉnh ROI theo pair (bật `use_custom_roi`) |
| `adjust_trade_position(...)` | DCA / partial exit |
| `adjust_order_price(...)` / `adjust_entry_price(...)` / `adjust_exit_price(...)` | Điều chỉnh giá lệnh đang mở |
| `check_entry_timeout(...)` / `check_exit_timeout(...)` | Quyết định huỷ order quá hạn |
| `order_filled(...)` | Hook khi lệnh khớp |
| `leverage(...)` | Chọn đòn bẩy (futures/margin) |
| `feature_engineering_*` | (FreqAI) tạo feature |
| `set_freqai_targets(...)` | (FreqAI) gán target |

### 1.4. Informative pairs

Lấy nến / chỉ báo từ pair khác (hoặc timeframe khác cùng pair):

```python
from freqtrade.strategy import informative

@informative("1h")
def populate_indicators_1h(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
    dataframe["ema_50"] = ta.EMA(dataframe, timeperiod=50)
    return dataframe

# Hoặc liệt kê tay:
def informative_pairs(self):
    return [("BTC/USDT", "1h"), ("ETH/USDT", "1h")]
```

Decorator `informative` ở
[`freqtrade/strategy/informative_decorator.py`](../../freqtrade/strategy/informative_decorator.py)
tự merge dataframe phụ vào dataframe chính (suffix `_1h`,
`_btc_usdt_1h`).

### 1.5. Hyperopt parameters trong strategy

```python
from freqtrade.strategy import IntParameter, DecimalParameter, CategoricalParameter

class MyStrategy(IStrategy):
    buy_rsi  = IntParameter(10, 40, default=30, space="buy")
    sell_rsi = IntParameter(60, 90, default=70, space="sell")
    use_atr  = CategoricalParameter([True, False], default=True, space="buy")
```

Hyperopt sẽ tự discover các param này (xem
[`freqtrade/strategy/parameters.py`](../../freqtrade/strategy/parameters.py)).

### 1.6. Lưu state per-trade qua `Trade.set_custom_data`

```python
trade.set_custom_data(key="entry_atr", value=atr_value)
val = trade.get_custom_data(key="entry_atr", default=None)
```

Lưu ở bảng `custom_data` (xem
[`freqtrade/persistence/custom_data.py`](../../freqtrade/persistence/custom_data.py)).

### 1.7. Strategy validation

```powershell
freqtrade list-strategies --userdir user_data
freqtrade strategy-updater --userdir user_data --strategy MyStrategy
freqtrade lookahead-analysis --userdir user_data --strategy MyStrategy --timerange 20250101-20250201
freqtrade recursive-analysis --userdir user_data --strategy MyStrategy --timerange 20250101-20250201
```

`lookahead-analysis` so sánh kết quả backtest từng phần để phát hiện
dùng giá tương lai. `recursive-analysis` phát hiện chỉ báo phụ thuộc
vào lịch sử "vô tận" (không hội tụ).

---

## 2. Pairlist chain động

Tham chiếu: [`docs/includes/pairlists.md`](../includes/pairlists.md),
[`docs/plugins.md`](../plugins.md).

Pairlist là chuỗi handler chạy theo thứ tự, plugin đầu tiên là
**generator**, các plugin sau là **filter** — xem code
[`freqtrade/plugins/pairlistmanager.py`](../../freqtrade/plugins/pairlistmanager.py).

### 2.1. Cấu hình ví dụ

```jsonc
"pairlists": [
  {
    "method": "VolumePairList",
    "number_assets": 30,
    "sort_key": "quoteVolume",
    "min_value": 0,
    "refresh_period": 1800
  },
  { "method": "AgeFilter", "min_days_listed": 30 },
  { "method": "PrecisionFilter" },
  { "method": "PriceFilter", "low_price_ratio": 0.01 },
  { "method": "SpreadFilter", "max_spread_ratio": 0.005 },
  {
    "method": "RangeStabilityFilter",
    "lookback_days": 10,
    "min_rate_of_change": 0.03,
    "refresh_period": 1440
  },
  { "method": "VolatilityFilter", "lookback_days": 7 },
  { "method": "FullTradesFilter" },
  { "method": "ShuffleFilter", "seed": 42 }
]
```

Danh sách built-in (hằng `AVAILABLE_PAIRLISTS`):

- Generator: `StaticPairList`, `VolumePairList`, `MarketCapPairList`,
  `PercentChangePairList`, `RemotePairList`, `ProducerPairList`,
  `CrossMarketPairList`.
- Filter: `AgeFilter`, `DelistFilter`, `FullTradesFilter`,
  `OffsetFilter`, `PerformanceFilter`, `PrecisionFilter`,
  `PriceFilter`, `RangeStabilityFilter`, `ShuffleFilter`,
  `SpreadFilter`, `VolatilityFilter`.

### 2.2. Test pairlist

```powershell
freqtrade test-pairlist --userdir user_data --config user_data/config.json
```

Lệnh này chạy chuỗi pairlist 1 lần và in whitelist kết quả — không cần
khởi động bot.

### 2.3. Pairlist từ remote / multi-bot

- `RemotePairList` — đọc whitelist từ URL (JSON) hoặc file. Hữu ích khi
  team chia sẻ whitelist tập trung.
- `ProducerPairList` — nhận whitelist từ bot khác qua kênh WebSocket
  (xem mục [§8](#8-multi-bot--producerconsumer)).

---

## 3. Protections

Tham chiếu: [`docs/includes/protections.md`](../includes/protections.md).

Protection chạy **sau khi trade đóng**, có thể khoá pair (per-pair) hoặc
tất cả pair (global). Cấu hình mẫu:

```jsonc
"protections": [
  {
    "method": "CooldownPeriod",
    "stop_duration_candles": 5
  },
  {
    "method": "MaxDrawdown",
    "lookback_period_candles": 48,
    "trade_limit": 20,
    "stop_duration_candles": 12,
    "max_allowed_drawdown": 0.2
  },
  {
    "method": "StoplossGuard",
    "lookback_period_candles": 24,
    "trade_limit": 4,
    "stop_duration_candles": 2,
    "only_per_pair": false,
    "only_per_side": false
  },
  {
    "method": "LowProfitPairs",
    "lookback_period_candles": 6,
    "trade_limit": 2,
    "stop_duration_candles": 60,
    "required_profit": 0.02
  }
]
```

Plugin built-in:

- `CooldownPeriod` — sau mỗi exit, khoá pair X candles.
- `StoplossGuard` — nếu N stoploss trong M candles → khoá.
- `MaxDrawdown` — drawdown tối đa trong window.
- `LowProfitPairs` — pair lợi nhuận thấp bị tạm khoá.

Tự viết protection: kế thừa
[`IProtection`](../../freqtrade/plugins/protections/iprotection.py) —
xem hướng dẫn ở [06](06-huong-dan-phat-trien.md#5-thêm-pairlist--protection).

---

## 4. Hyperopt nâng cao

Tham chiếu: [`docs/hyperopt.md`](../hyperopt.md),
[`docs/advanced-hyperopt.md`](../advanced-hyperopt.md).

### 4.1. Lệnh hyperopt cơ bản

```powershell
freqtrade hyperopt `
  --userdir user_data `
  --hyperopt-loss SharpeHyperOptLossDaily `
  --strategy MyStrategy `
  --spaces buy sell roi stoploss trailing `
  --epochs 500 `
  --timerange 20250101-20250301 `
  -j -1
```

`--spaces`: chọn không gian tham số (xem hằng `HYPEROPT_BUILTIN_SPACES`):
`buy`, `sell`, `enter`, `exit`, `roi`, `stoploss`, `trailing`,
`protection`, `trades`, `default`, `all`.

### 4.2. Loss functions sẵn

| Loss | Đặc điểm |
|------|----------|
| `ShortTradeDurHyperOptLoss` | Thưởng trade ngắn hạn, ROI cao |
| `OnlyProfitHyperOptLoss` | Tối đa profit thuần |
| `SharpeHyperOptLoss` / `SharpeHyperOptLossDaily` | Sharpe ratio |
| `SortinoHyperOptLoss` / `SortinoHyperOptLossDaily` | Sortino ratio |
| `CalmarHyperOptLoss` | Calmar (return / max DD) |
| `MaxDrawDownHyperOptLoss` | Phạt drawdown lớn |
| `MaxDrawDownRelativeHyperOptLoss` | Drawdown tương đối |
| `MaxDrawDownPerPairHyperOptLoss` | DD per pair |
| `ProfitDrawDownHyperOptLoss` | Profit cân với DD |
| `MultiMetricHyperOptLoss` | Tổng hợp nhiều metric |

### 4.3. Tự viết loss

Tạo `user_data/hyperopts/MyLoss.py` kế thừa
[`IHyperOptLoss`](../../freqtrade/optimize/hyperopt_loss/hyperopt_loss_interface.py):

```python
from datetime import datetime
import pandas as pd
from freqtrade.optimize.hyperopt import IHyperOptLoss

class MyLoss(IHyperOptLoss):
    @staticmethod
    def hyperopt_loss_function(
        results: pd.DataFrame, trade_count: int,
        min_date: datetime, max_date: datetime,
        config, processed, backtest_stats, *args, **kwargs
    ) -> float:
        if trade_count < 10:
            return 999
        profit_total = results["profit_ratio"].sum()
        avg_dur = results["trade_duration"].mean() / 60.0
        return -(profit_total) + avg_dur / 1000.0
```

Sau đó: `--hyperopt-loss MyLoss`. Liệt kê:

```powershell
freqtrade list-hyperoptloss --userdir user_data
```

### 4.4. Phân tích kết quả

```powershell
freqtrade hyperopt-list --userdir user_data --best --print-json
freqtrade hyperopt-show --userdir user_data -n 0
freqtrade hyperopt-show --userdir user_data --best --print-json | Out-File user_data/best.json
```

Áp dụng tham số đã hyperopt: copy block JSON xuất ra → paste vào
`buy_params` / `sell_params` của strategy, hoặc dùng
`freqtrade strategy-updater`.

### 4.5. Sampler tuỳ chỉnh

Optuna sampler được chọn qua `hyperopt_optimizer_class` (TPE mặc định).
Bạn có thể chỉnh seed (`--random-state`), số CPU job (`-j`), số epoch
(`--epochs`), `analyze_per_epoch` (qua config) để bật/tắt analyze giữa
các epoch.

---

## 5. Backtest sâu & analysis

Tham chiếu: [`docs/backtesting.md`](../backtesting.md),
[`docs/advanced-backtesting.md`](../advanced-backtesting.md).

### 5.1. Tham số mạnh

| Flag | Tác dụng |
|------|----------|
| `--timeframe-detail 1m` | Mô phỏng entry/exit chính xác hơn (intra-candle) |
| `--enable-protections` | Bật protection trong backtest |
| `--export signals` | Xuất signal để debug |
| `--breakdown day,week,month` | Báo cáo theo ngày/tuần/tháng |
| `--cache none` | Không tái dùng cache (luôn chạy lại) |
| `--strategy-list A B` | So sánh nhiều strategy cùng lúc |

### 5.2. Backtest analysis

```powershell
freqtrade backtesting-analysis --userdir user_data `
  --analysis-groups 0 1 2 3 4 5
```

Tham chiếu: [`docs/advanced-backtesting.md`](../advanced-backtesting.md).
Lệnh này nhóm trade theo enter_tag/exit_tag/pair/loại signal để bạn xem
chi tiết hơn báo cáo backtest mặc định.

### 5.3. Lookahead & recursive analysis

```powershell
freqtrade lookahead-analysis --userdir user_data `
  --strategy MyStrategy --timerange 20250101-20250201 `
  --max-slippage-trial 5

freqtrade recursive-analysis --userdir user_data `
  --strategy MyStrategy
```

Đặt **bắt buộc** trước khi đưa strategy vào live. Đọc
[`docs/lookahead-analysis.md`](../lookahead-analysis.md),
[`docs/recursive-analysis.md`](../recursive-analysis.md).

---

## 6. FreqAI

Tham chiếu: [`docs/freqai.md`](../freqai.md),
[`docs/freqai-configuration.md`](../freqai-configuration.md),
[`docs/freqai-feature-engineering.md`](../freqai-feature-engineering.md),
[`docs/freqai-running.md`](../freqai-running.md),
[`docs/freqai-reinforcement-learning.md`](../freqai-reinforcement-learning.md),
[`docs/freqai-parameter-table.md`](../freqai-parameter-table.md).

### 6.1. Bật FreqAI

```jsonc
"freqai": {
  "enabled": true,
  "purge_old_models": 2,
  "train_period_days": 30,
  "backtest_period_days": 7,
  "live_retrain_hours": 0,
  "expiration_hours": 0,
  "identifier": "myFreqaiUser1",
  "feature_parameters": {
    "include_timeframes": ["5m", "15m", "1h"],
    "include_corr_pairlist": ["BTC/USDT", "ETH/USDT"],
    "label_period_candles": 24,
    "include_shifted_candles": 2,
    "DI_threshold": 0.0,
    "weight_factor": 0.9,
    "principal_component_analysis": false,
    "use_SVM_to_remove_outliers": false,
    "indicator_periods_candles": [10, 20]
  },
  "data_split_parameters": {
    "test_size": 0.33,
    "shuffle": false
  },
  "model_training_parameters": {
    "n_estimators": 1000
  }
}
```

Strategy phải có `feature_engineering_expand_all`,
`feature_engineering_expand_basic`, `feature_engineering_standard`,
`set_freqai_targets`, và gọi `self.freqai.start(dataframe, metadata)`
trong `populate_indicators` — xem template
[`freqtrade/templates/FreqaiExampleStrategy.py`](../../freqtrade/templates/FreqaiExampleStrategy.py).

### 6.2. Mô hình built-in

`freqaimodel` (default): `LightGBMRegressor`. Khác có sẵn:

- `LightGBMRegressorMultiTarget`, `LightGBMClassifier`,
  `LightGBMClassifierMultiTarget`.
- `XGBoostRegressor`, `XGBoostClassifier`, multi-target tương tự.
- `CatboostRegressor`, `CatboostClassifier` (cần cài extra).
- `PyTorchTransformerRegressor`, `PyTorchMLPRegressor`,
  `PyTorchMLPClassifier`.
- RL: `ReinforcementLearner`, `ReinforcementLearner_multiproc`.

Liệt kê:

```powershell
freqtrade list-freqaimodels --userdir user_data
```

### 6.3. Chạy FreqAI dry-run

Cấu hình `freqai.enabled = true` rồi chạy bình thường:

```powershell
freqtrade trade --userdir user_data --strategy FreqaiExampleStrategy
```

Bot sẽ tự pre-download data → train per pair → predict per candle. Log
xuất ra `user_data/models/<identifier>/`.

### 6.4. Reinforcement Learning

Cần `[freqai_rl]` extra:

```powershell
pip install -e ".[freqai_rl]"
```

Cấu hình `model_training_parameters` cho `PPO`/`DQN`/... Tham khảo
[`docs/freqai-reinforcement-learning.md`](../freqai-reinforcement-learning.md).

---

## 7. Futures / Leverage / Short

Tham chiếu: [`docs/leverage.md`](../leverage.md).

### 7.1. Bật futures

```jsonc
"trading_mode": "futures",
"margin_mode": "isolated",
"exchange": {
  "name": "binance",
  "pair_whitelist": ["BTC/USDT:USDT", "ETH/USDT:USDT"]
}
```

Pair futures dạng `base/quote:settle` (settle = đồng thanh toán).

### 7.2. Strategy short

```python
class MyStrategy(IStrategy):
    can_short = True

    def populate_entry_trend(self, dataframe, metadata):
        # long
        dataframe.loc[<long-cond>, ["enter_long", "enter_tag"]] = (1, "L")
        # short
        dataframe.loc[<short-cond>, ["enter_short", "enter_tag"]] = (1, "S")
        return dataframe

    def leverage(self, pair, current_time, current_rate, proposed_leverage,
                 max_leverage, side, **kwargs) -> float:
        return min(max_leverage, 5.0)
```

### 7.3. Liquidation price

Tự tính & lưu, xem
[`freqtrade/leverage/liquidation_price.py`](../../freqtrade/leverage/liquidation_price.py).
Strategy có thể đọc qua `trade.liquidation_price` để custom logic.

### 7.4. Funding fees

Bot tự gọi `Exchange.fetch_funding_fees` định kỳ (futures hỗ trợ qua
ccxt) và cộng vào lợi nhuận trade. Trong dry-run, được giả lập từ funding
rate.

---

## 8. Multi-bot — Producer/Consumer

Tham chiếu: [`docs/producer-consumer.md`](../producer-consumer.md).

```mermaid
flowchart LR
    BotA[Bot A producer] -->|WS dataframe + signals| BotB[Bot B consumer]
    BotA -->|WS pairlist| BotB
```

### 8.1. Bot producer (phát dữ liệu)

```jsonc
"api_server": {
  "enabled": true,
  "listen_ip_address": "0.0.0.0",
  "listen_port": 8080,
  "ws_token": "<random-secret-string>",
  "username": "freqtrader",
  "password": "..."
}
```

### 8.2. Bot consumer (nhận dữ liệu)

```jsonc
"external_message_consumer": {
  "enabled": true,
  "producers": [
    {
      "name": "default",
      "host": "127.0.0.1",
      "port": 8080,
      "ws_token": "<random-secret-string>"
    }
  ],
  "wait_timeout": 300,
  "ping_timeout": 10,
  "sleep_time": 10,
  "remove_entry_exit_signals": false,
  "message_size_limit": 8
}
```

Strategy consumer dùng dataframe của producer:

```python
def populate_indicators(self, dataframe, metadata):
    pair_df, last_analyzed = self.dp.get_external_df(metadata["pair"], producer_name="default")
    # merge ...
```

Pairlist chéo: dùng `ProducerPairList`.

---

## 9. Webhook & tích hợp ngoài

Tham chiếu: [`docs/webhook-config.md`](../webhook-config.md).

Bật `"webhook": { "enabled": true, "url": "...", "format": "json" }`.
Mỗi sự kiện có template riêng:

- `webhookentry`, `webhookentryfill`, `webhookentrycancel`.
- `webhookexit`, `webhookexitfill`, `webhookexitcancel`.
- `webhookstatus`, `webhookprotection`.

Field thay thế (placeholder): `{pair}`, `{open_rate}`, `{close_rate}`,
`{stake_amount}`, `{profit_ratio}`, `{profit_amount}`, `{order_type}`,
`{exit_reason}`, ...

Discord: dùng `format: form` và URL webhook Discord.

---

## 10. Orderflow & dữ liệu trades

Tham chiếu: [`docs/advanced-orderflow.md`](../advanced-orderflow.md).

Bật `"exchange.use_public_trades": true` để bot gọi
`Exchange.fetch_trades` và tính orderflow (delta, imbalances). Strategy
có thể đọc các cột mới: `orderflow`, `imbalances`,
`stacked_imbalances_bid/ask`, `bid`, `ask`, `delta`, `total_trades`
(xem `ORDERFLOW_ADDED_COLUMNS` ở
[`freqtrade/constants.py`](../../freqtrade/constants.py)).

Note hiệu năng: orderflow cần nhiều dữ liệu trades, latency cao hơn —
cân nhắc tăng `process_throttle_secs`.

---

## 11. Vận hành nâng cao

Tham chiếu: [`docs/advanced-setup.md`](../advanced-setup.md),
[`docs/sql_cheatsheet.md`](../sql_cheatsheet.md).

### 11.1. Postgres / MySQL thay SQLite

```jsonc
"db_url": "postgresql+psycopg://user:pass@host:5432/freqtrade"
```

Migrate từ SQLite:

```powershell
freqtrade convert-db `
  --db-url-from sqlite:///user_data/tradesv3.sqlite `
  --db-url postgresql+psycopg://user:pass@host:5432/freqtrade
```

### 11.2. SQL cheatsheet

```sql
-- Tổng profit theo pair
SELECT pair,
       COUNT(*)               AS trades,
       SUM(close_profit_abs)  AS profit
FROM trades
WHERE is_open = 0
GROUP BY pair
ORDER BY profit DESC;

-- Drawdown trong 30 ngày
SELECT MIN(close_profit_abs)
FROM trades
WHERE close_date >= datetime('now', '-30 days');
```

Xem thêm [`docs/sql_cheatsheet.md`](../sql_cheatsheet.md).

### 11.3. CORS cho REST API

[`docs/includes/cors.md`](../includes/cors.md). Đặt
`api_server.CORS_origins = ["https://my.dashboard"]`.

### 11.4. Reload config qua API/Telegram

- Telegram: `/reload_config`.
- REST: `POST /api/v1/reload_config`.

Bot sẽ reload qua `Worker._reconfigure` — tạo `FreqtradeBot` mới, đóng
cái cũ (xem [01 §5.1–§5.2](01-nguyen-tac-hoat-dong.md)).

### 11.5. Performance tuning

- `process_throttle_secs`: tăng lên 30–60s nếu strategy chậm hoặc nhiều
  pair.
- `internals.heartbeat_interval`: 0 để tắt log heartbeat.
- `runmode: dry_run` không đặt lệnh thật; tuy nhiên vẫn tốn API call.
- Pin `process_only_new_candles = True` nếu strategy chỉ cần signal sau
  nến đóng — tiết kiệm CPU đáng kể.
- Disable cache: `--cache none` chỉ khi debug; production để cache mặc
  định.

---

## 12. Plotting & data analysis

Tham chiếu: [`docs/plotting.md`](../plotting.md),
[`docs/data-analysis.md`](../data-analysis.md),
[`docs/strategy_analysis_example.md`](../strategy_analysis_example.md),
[`docs/sql_cheatsheet.md`](../sql_cheatsheet.md).

### 12.1. Plot dataframe

```powershell
pip install -e ".[plot]"
freqtrade plot-dataframe --userdir user_data `
  --strategy MyStrategy --pair BTC/USDT --timerange 20250101-20250115
```

Output ở `user_data/plot/` dạng HTML.

### 12.2. Plot profit

```powershell
freqtrade plot-profit --userdir user_data `
  --strategy MyStrategy --timerange 20250101-20250201
```

### 12.3. Jupyter notebook

```powershell
pip install -e ".[jupyter]"
jupyter lab user_data/notebooks/strategy_analysis_example.ipynb
```

Notebook mẫu nằm tại
[`freqtrade/templates/strategy_analysis_example.ipynb`](../../freqtrade/templates/strategy_analysis_example.ipynb)
(copy vào userdir bằng `create-userdir`).

---

## 13. Migration & deprecated

- Đọc release notes trước khi update major:
  [GitHub Releases](https://github.com/freqtrade/freqtrade/releases).
- [`docs/updating.md`](../updating.md) — quy trình update.
- [`docs/strategy_migration.md`](../strategy_migration.md) — migrate
  strategy giữa các phiên bản interface.
- [`docs/deprecated.md`](../deprecated.md) — danh sách feature đã loại
  bỏ.
- Lệnh tự động: `freqtrade strategy-updater`.

---

## Checklist "đã làm chủ Freqtrade nâng cao"

- [ ] Hiểu rõ khác biệt callback live vs backtest, viết được strategy
      không bị lookahead.
- [ ] Đã cấu hình pairlist + protection chain phù hợp.
- [ ] Hyperopt thuần thục `--spaces` + custom loss.
- [ ] Chạy backtest analysis + lookahead/recursive analysis trước khi
      live.
- [ ] Hiểu pipeline FreqAI ít nhất ở mức configuration.
- [ ] Thử nghiệm futures + leverage trong dry-run.
- [ ] Set up multi-bot producer/consumer.
- [ ] Có chiến lược backup DB + config + strategy.

Tiếp theo: [06. Hướng dẫn phát triển](06-huong-dan-phat-trien.md).
