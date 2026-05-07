# 04. Cài đặt, chạy và sử dụng Freqtrade

Mục tiêu: từ "máy trắng" đến "bot đang chạy dry-run với UI". Tài liệu này
viết cho **người dùng cuối** (end-user). Nếu bạn là coder muốn build từ
source / Docker image, đọc [03. Hướng dẫn build](03-huong-dan-build.md).

> Lệnh viết cho **PowerShell trên Windows**. Tương đương bash/zsh đặt
> ngay sau khi cú pháp khác.

## Mục lục

- [1. Hai con đường: Docker hay Native?](#1-hai-con-đường-docker-hay-native)
- [2. Cài đặt theo Docker (khuyến nghị)](#2-cài-đặt-theo-docker-khuyến-nghị)
- [3. Cài đặt native (qua setup.sh / setup.ps1)](#3-cài-đặt-native-qua-setupsh--setupps1)
- [4. Khởi tạo workspace `user_data`](#4-khởi-tạo-workspace-user_data)
- [5. Tạo và hiểu file config](#5-tạo-và-hiểu-file-config)
- [6. Tải dữ liệu lịch sử](#6-tải-dữ-liệu-lịch-sử)
- [7. Chạy backtest đầu tiên](#7-chạy-backtest-đầu-tiên)
- [8. Chạy dry-run](#8-chạy-dry-run)
- [9. Theo dõi & điều khiển bot](#9-theo-dõi--điều-khiển-bot)
- [10. Chuyển sang live trading](#10-chuyển-sang-live-trading)
- [11. Vận hành dài hạn](#11-vận-hành-dài-hạn)
- [12. Cập nhật & nâng cấp](#12-cập-nhật--nâng-cấp)
- [13. Câu hỏi thường gặp](#13-câu-hỏi-thường-gặp)

---

## 1. Hai con đường: Docker hay Native?

| Tiêu chí | Docker | Native (venv) |
|----------|--------|---------------|
| Setup | Nhanh, ít trục trặc | Cần TA-Lib, MSVC, Python… |
| Cập nhật | `docker compose pull` | `git pull && pip install -e .` |
| Hỗ trợ FreqAI RL | Cần image `:freqai_rl` | Cài thủ công PyTorch |
| Debug code | Khó hơn (mount source) | Dễ (live edit) |
| Hợp với | Mọi user, đặc biệt Windows | Coder, máy server Linux |

**Khuyến nghị**:

- Người dùng mới / Windows → **Docker**.
- Coder / hay sửa source → **Native** (xem
  [03. Hướng dẫn build](03-huong-dan-build.md)).

---

## 2. Cài đặt theo Docker (khuyến nghị)

Tham khảo gốc: [`docs/docker_quickstart.md`](../docker_quickstart.md).

### 2.1. Cài Docker Desktop

- Windows: [Docker Desktop for Windows](https://docs.docker.com/desktop/install/windows-install/)
  + WSL2.
- macOS: [Docker Desktop for Mac](https://docs.docker.com/desktop/install/mac-install/).
- Linux: [docker engine + docker compose plugin](https://docs.docker.com/engine/install/).

Sau khi cài xong, kiểm tra:

```powershell
docker --version
docker compose version
```

> Lưu ý Windows: **reboot** sau khi cài Docker. Nếu không, network bên
> trong container sẽ rất "ngẫu nhiên".

### 2.2. Quickstart

```powershell
# Tạo thư mục workspace
mkdir ft_userdata
cd ft_userdata

# Tải docker-compose.yml mẫu (stable)
Invoke-WebRequest `
  -Uri "https://raw.githubusercontent.com/freqtrade/freqtrade/stable/docker-compose.yml" `
  -OutFile "docker-compose.yml"

# Pull image
docker compose pull

# Tạo cấu trúc user_data/
docker compose run --rm freqtrade create-userdir --userdir user_data

# Tạo config (interactive)
docker compose run --rm freqtrade new-config --config user_data/config.json
```

```bash
# Linux/macOS
mkdir ft_userdata && cd ft_userdata
curl https://raw.githubusercontent.com/freqtrade/freqtrade/stable/docker-compose.yml -o docker-compose.yml
docker compose pull
docker compose run --rm freqtrade create-userdir --userdir user_data
docker compose run --rm freqtrade new-config --config user_data/config.json
```

Bot sẽ hỏi tương tác về:

- Sàn (Binance, Bybit, Kraken, OKX…).
- Tiền cơ sở (`stake_currency`).
- `dry_run` (mặc định `true` — **giữ nguyên** ban đầu).
- Có dùng FreqUI không.

Sau khi tạo xong, file `user_data/config.json` đã sẵn sàng. Khởi động:

```powershell
docker compose up -d
docker compose logs -f
```

Mở UI tại http://localhost:8080 (mặc định bind `127.0.0.1:8080` ở
[`docker-compose.yml`](../../docker-compose.yml) — chỉ truy cập từ chính
máy bạn).

### 2.3. Cập nhật strategy / config

- Sửa `user_data/config.json` (mặc định bot reload khi nhận
  `/reload_config` từ Telegram hoặc qua `docker compose restart`).
- Đổi strategy: chỉnh dòng `--strategy SampleStrategy` trong
  `docker-compose.yml` rồi `docker compose up -d`.

### 2.4. Image biến thể

Sửa `image:` trong `docker-compose.yml` thành một trong:

- `freqtradeorg/freqtrade:stable` (mặc định).
- `freqtradeorg/freqtrade:develop` (đầu dev).
- `freqtradeorg/freqtrade:stable_plot` / `develop_plot` (kèm `plotly`).
- `freqtradeorg/freqtrade:stable_freqai` / `develop_freqai`.
- `freqtradeorg/freqtrade:stable_freqairl` / `develop_freqairl`.

---

## 3. Cài đặt native (qua setup.sh / setup.ps1)

Xem chi tiết ở [03. Hướng dẫn build §3](03-huong-dan-build.md#3-build-môi-trường-dev). Tóm tắt
cho người dùng cuối:

### 3.1. Windows

```powershell
git clone https://github.com/freqtrade/freqtrade.git
cd freqtrade
git checkout stable

# Bật execution policy nếu cần
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\setup.ps1
.\.venv\Scripts\Activate.ps1

freqtrade --version
```

### 3.2. Linux/macOS

```bash
git clone https://github.com/freqtrade/freqtrade.git
cd freqtrade
git checkout stable

./setup.sh -i
source .venv/bin/activate
freqtrade --version
```

> Trên Raspberry Pi (armv7l), dùng image Docker `:armhf` thay vì cài
> native — nhiều dependency native (numpy, scipy, torch) không build
> được.

---

## 4. Khởi tạo workspace `user_data`

Workspace của bạn nằm tại `user_data/` (mount vào container hoặc cùng cấp
với venv). Cấu trúc chuẩn (xem
[`freqtrade/commands/deploy_commands.py`](../../freqtrade/commands/deploy_commands.py)
`start_create_userdir`):

```
user_data/
├── backtest_results/
├── data/
│   └── <exchange>/
├── hyperopt_results/
├── hyperopts/
│   └── sample_hyperopt_loss.py
├── logs/
├── notebooks/
│   └── strategy_analysis_example.ipynb
├── plot/
├── strategies/
│   └── sample_strategy.py
└── config.json
```

Tạo nhanh:

```powershell
freqtrade create-userdir --userdir user_data
freqtrade new-strategy --userdir user_data --strategy MyStrategy
```

`new-strategy` copy từ
[`freqtrade/templates/sample_strategy.py`](../../freqtrade/templates/sample_strategy.py)
và đổi tên class.

---

## 5. Tạo và hiểu file config

### 5.1. Sinh config bằng wizard

```powershell
freqtrade new-config --config user_data/config.json
```

Hoặc copy mẫu sẵn từ
[`config_examples/`](../../config_examples/):

- [`config_binance.example.json`](../../config_examples/config_binance.example.json) — spot Binance.
- [`config_kraken.example.json`](../../config_examples/config_kraken.example.json) — spot Kraken.
- [`config_full.example.json`](../../config_examples/config_full.example.json) — **mọi field** kèm comment.
- [`config_freqai.example.json`](../../config_examples/config_freqai.example.json) — bật FreqAI.

### 5.2. Các trường tối thiểu phải đặt

```jsonc
{
  "max_open_trades": 3,
  "stake_currency": "USDT",
  "stake_amount": 50,
  "tradable_balance_ratio": 0.99,
  "fiat_display_currency": "USD",
  "timeframe": "5m",
  "dry_run": true,
  "dry_run_wallet": 1000,
  "cancel_open_orders_on_exit": false,
  "trading_mode": "spot",
  "margin_mode": "",
  "exchange": {
    "name": "binance",
    "key": "",
    "secret": "",
    "ccxt_config": {},
    "ccxt_async_config": {},
    "pair_whitelist": ["BTC/USDT", "ETH/USDT"],
    "pair_blacklist": ["BNB/.*"]
  },
  "pairlists": [
    { "method": "StaticPairList" }
  ],
  "telegram": {
    "enabled": false
  },
  "api_server": {
    "enabled": true,
    "listen_ip_address": "127.0.0.1",
    "listen_port": 8080,
    "username": "freqtrader",
    "password": "đặt-mật-khẩu-mạnh"
  },
  "bot_name": "freqtrade",
  "initial_state": "running",
  "force_entry_enable": false,
  "internals": {
    "process_throttle_secs": 5
  }
}
```

> **Đừng** commit `config.json` chứa khoá API thật vào git.

Tài liệu đầy đủ mọi field: [`docs/configuration.md`](../configuration.md).

### 5.3. Validate config

```powershell
freqtrade show-config --config user_data/config.json
```

Lệnh này merge tất cả config + biến môi trường + mặc định, rồi in ra
config "đã giải quyết" (resolved). Lỗi schema sẽ raise
`ConfigurationError` ngay.

### 5.4. Biến môi trường

Có thể override field config bằng `FREQTRADE__<path>__<key>`. Ví dụ:

```powershell
$env:FREQTRADE__EXCHANGE__KEY = "abc"
$env:FREQTRADE__EXCHANGE__SECRET = "xyz"
$env:FREQTRADE__TELEGRAM__ENABLED = "true"
freqtrade trade --config user_data/config.json --strategy SampleStrategy
```

Logic ở
[`freqtrade/configuration/environment_vars.py`](../../freqtrade/configuration/environment_vars.py).

---

## 6. Tải dữ liệu lịch sử

Bắt buộc trước khi backtest. Tham khảo gốc
[`docs/data-download.md`](../data-download.md).

```powershell
# Tải 5m và 1h cho 30 ngày gần nhất
freqtrade download-data `
  --userdir user_data `
  --exchange binance `
  --pairs BTC/USDT ETH/USDT `
  --timeframes 5m 1h `
  --days 30
```

```bash
freqtrade download-data \
  --userdir user_data \
  --exchange binance \
  --pairs BTC/USDT ETH/USDT \
  --timeframes 5m 1h \
  --days 30
```

Liệt kê dữ liệu đã tải:

```powershell
freqtrade list-data --userdir user_data --exchange binance
```

Định dạng lưu trữ mặc định là `feather`. Để đổi: `--data-format-ohlcv parquet`
hoặc `json`. Convert giữa các định dạng: `freqtrade convert-data ...`.

---

## 7. Chạy backtest đầu tiên

```powershell
freqtrade backtesting `
  --userdir user_data `
  --config user_data/config.json `
  --strategy SampleStrategy `
  --timerange 20250101-20250201 `
  --timeframe 5m
```

Kết quả lưu vào `user_data/backtest_results/<timestamp>.json` và in bảng
ra console (per-pair, per-tag, per-month, per-weekday).

Để **so sánh nhiều strategy**:

```powershell
freqtrade backtesting `
  --userdir user_data `
  --strategy-list StrategyA StrategyB `
  --timerange 20250101-20250201
```

Xem report cũ:

```powershell
freqtrade backtesting-show --userdir user_data
```

---

## 8. Chạy dry-run

Đảm bảo `"dry_run": true` trong config rồi:

```powershell
freqtrade trade `
  --userdir user_data `
  --config user_data/config.json `
  --strategy SampleStrategy
```

Bot sẽ:

1. Kết nối sàn để lấy OHLCV/giá realtime.
2. **Mô phỏng** đặt lệnh — không bao giờ gửi order thật.
3. Lưu trade ảo vào DB `tradesv3.dryrun.sqlite`.
4. Phát message qua các kênh đã bật (Telegram, Webhook, REST/WS).

Khuyến nghị: **dry-run ít nhất 3–7 ngày** trước khi đụng tiền thật, để
quan sát behaviour với spread, slippage, partial fill thực tế.

Dừng bot:

- Ctrl+C ở terminal (SIGINT).
- `docker compose stop freqtrade` (Docker).
- `/stop` qua Telegram nếu đã bật.

---

## 9. Theo dõi & điều khiển bot

Có 4 lớp giao tiếp với bot, đều đi qua
[`RPCManager`](../../freqtrade/rpc/rpc_manager.py):

### 9.1. FreqUI (Web UI)

- Bật ở config: `api_server.enabled: true`.
- Truy cập http://localhost:8080.
- Đăng nhập bằng `username` / `password` đã đặt.
- Tính năng: dashboard, charts, trade list, force entry/exit, reload
  config, plot strategy, profit per pair/day/week/month.
- Tham khảo: [`docs/freq-ui.md`](../freq-ui.md),
  [`docs/rest-api.md`](../rest-api.md).

### 9.2. REST API

Tham khảo đầy đủ endpoint: [`docs/rest-api.md`](../rest-api.md). Một số
endpoint hay dùng:

- `GET /api/v1/status` — danh sách trade đang mở.
- `POST /api/v1/forceenter` — vào lệnh thủ công (cần
  `force_entry_enable: true`).
- `POST /api/v1/forceexit` — đóng lệnh thủ công.
- `POST /api/v1/reload_config` — reload config.
- `GET /api/v1/profit` — thống kê lợi nhuận.
- `GET /api/v1/balance` — số dư ví.

Lấy JWT token:

```powershell
$cred = "freqtrader:đặt-mật-khẩu-mạnh"
$enc  = [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes($cred))
Invoke-RestMethod -Method POST `
  -Uri "http://127.0.0.1:8080/api/v1/token/login" `
  -Headers @{ Authorization = "Basic $enc" }
```

### 9.3. Telegram

Tham khảo: [`docs/telegram-usage.md`](../telegram-usage.md). Cấu hình
config:

```jsonc
"telegram": {
  "enabled": true,
  "token": "<botfather-token>",
  "chat_id": "<your-chat-id>",
  "notification_settings": {
    "status": "on",
    "warning": "on",
    "startup": "on",
    "entry": "on",
    "exit": {
      "roi": "on",
      "stop_loss": "on",
      "trailing_stop_loss": "on",
      "exit_signal": "on"
    }
  }
}
```

Lệnh Telegram phổ biến (đã có trong
[`README.md`](../../README.md) §Telegram RPC commands):

- `/start`, `/stop`, `/stopentry`, `/reload_config`.
- `/status`, `/status table`.
- `/profit`, `/profit_long`, `/profit_short`, `/daily 7`, `/weekly 4`.
- `/forceexit <id>`, `/forceexit all`, `/fx <id>`.
- `/forceenter BTC/USDT long`.
- `/balance`, `/performance`, `/locks`.
- `/version`, `/help`.

### 9.4. Webhook

Đẩy event ra HTTP endpoint của bạn (Slack, Discord, hệ thống nội bộ).
Cấu hình mẫu: [`docs/webhook-config.md`](../webhook-config.md).

```jsonc
"webhook": {
  "enabled": true,
  "url": "https://hooks.slack.com/services/...",
  "format": "form",
  "webhookentry": { "value1": "Entry: {pair}", "value2": "{open_rate}", "value3": "{stake_amount}" },
  "webhookexit":  { "value1": "Exit: {pair}",  "value2": "{close_rate}", "value3": "{profit_amount}" }
}
```

---

## 10. Chuyển sang live trading

> **Cảnh báo nghiêm túc**: live trade = mất tiền thật khi sai. Đọc kỹ
> phần "Disclaimer" trong [README.md](../../README.md). Không thành viên
> nào của Freqtrade chịu trách nhiệm cho thua lỗ của bạn.

Checklist trước khi bật live:

- [ ] Đã backtest ≥ 3 timerange khác nhau, kết quả khả quan.
- [ ] Đã dry-run ≥ 3–7 ngày, P&L mô phỏng tương tự backtest.
- [ ] Đã hyperopt và **kiểm thử lại** trên dữ liệu chưa thấy.
- [ ] Đã chạy `freqtrade lookahead-analysis` và `freqtrade recursive-analysis` —
  không có cảnh báo.
- [ ] API key của sàn được tạo với **chỉ quyền giao dịch** (không
  withdraw, không margin nếu không dùng).
- [ ] IP whitelist trên sàn.
- [ ] Bật 2FA + dùng password manager riêng cho password REST/UI.
- [ ] `stake_amount` phù hợp với rủi ro (≤ 1% wallet / trade nếu mới).
- [ ] Quản lý process: systemd / docker `restart: unless-stopped`.

Đổi config:

```jsonc
{
  "dry_run": false,
  "exchange": {
    "name": "binance",
    "key": "<API_KEY>",
    "secret": "<API_SECRET>"
  },
  "db_url": "sqlite:///user_data/tradesv3.sqlite"
}
```

Khởi chạy lại:

```powershell
docker compose down
docker compose up -d
docker compose logs -f
```

Bot sẽ phát message `"started"` (Telegram) ngay khi vào live.

---

## 11. Vận hành dài hạn

### 11.1. Logs

- Native: log file định ở `--logfile` hoặc `internals.logfile`.
- Docker: `user_data/logs/freqtrade.log` (đã set trong
  `docker-compose.yml`).
- Mức log: `LOG_LEVEL=DEBUG` (env), hoặc `--verbose -v` / `-vv`.

### 11.2. systemd (native, Linux)

Repo có sẵn 2 unit file:

- [`freqtrade.service`](../../freqtrade.service).
- [`freqtrade.service.watchdog`](../../freqtrade.service.watchdog) — bật
  `internals.sd_notify` để watchdog tự kill khi heartbeat trễ.

```bash
sudo cp freqtrade.service.watchdog /etc/systemd/system/freqtrade.service
sudoedit /etc/systemd/system/freqtrade.service   # sửa USER, WorkingDirectory
sudo systemctl daemon-reload
sudo systemctl enable --now freqtrade
sudo systemctl status freqtrade
journalctl -u freqtrade -f
```

### 11.3. Backup

Quan trọng: **định kỳ backup** `user_data/`:

```powershell
Compress-Archive -Path user_data\* -DestinationPath "backups\freqtrade_$(Get-Date -Format yyyyMMdd_HHmmss).zip"
```

Đặc biệt: file `tradesv3.sqlite` (DB), `config.json`,
`hyperopt_results/`, `backtest_results/`, `strategies/`.

### 11.4. Khoá API & Pause

- `/stopentry` — bot không vào lệnh mới, vẫn quản lý trade đang mở.
- `/stop` — bot dừng hẳn (không quản lý trade nữa).
- `/forceexit all` — đóng tất cả lệnh ngay (bỏ qua ROI).
- Disable API trên sàn nếu phát hiện hành vi bất thường.

---

## 12. Cập nhật & nâng cấp

### 12.1. Docker

```powershell
docker compose pull
docker compose down
docker compose up -d
```

### 12.2. Native

```powershell
git pull
.\setup.ps1                 # Windows: chạy lại installer
# Hoặc thủ công:
# .\.venv\Scripts\Activate.ps1
# pip install -e ".[dev]"
freqtrade --version
```

```bash
git pull
./setup.sh -u
```

### 12.3. Migration cấu hình

Mỗi release lớn có thể có breaking change. Đọc
[`docs/updating.md`](../updating.md), thêm
[`docs/strategy_migration.md`](../strategy_migration.md) nếu chỉnh strategy.
Với strategy cũ, dùng `freqtrade strategy-updater` (xem
[`docs/commands/strategy-updater.md`](../commands/strategy-updater.md)).

### 12.4. Migration DB

Migration tự động khi bot khởi động (xem
[`freqtrade/persistence/migrations.py`](../../freqtrade/persistence/migrations.py)).
Nếu chuyển từ SQLite sang PostgreSQL: `freqtrade convert-db ...`.

---

## 13. Câu hỏi thường gặp

**Bot có cần chạy 24/7?**
Có, nếu strategy phụ thuộc tín hiệu trong nến đang chạy. Chỉ chạy theo
giờ là chấp nhận được nếu strategy chỉ giao dịch theo nến đóng.

**Backtest cho profit cao nhưng dry-run thì lỗ?**
Khả năng cao là **lookahead bias** hoặc **slippage**. Chạy
`freqtrade lookahead-analysis` và `freqtrade recursive-analysis`. Đọc
[`docs/lookahead-analysis.md`](../lookahead-analysis.md).

**Tôi có thể chạy nhiều bot song song?**
Được, mỗi bot phải có `db_url` riêng và `api_server.listen_port` riêng.
Multi-bot share tín hiệu: xem
[`docs/producer-consumer.md`](../producer-consumer.md).

**Bao nhiêu RAM/CPU là đủ?**
2GB RAM / 1 vCPU cho ≤ 30 cặp + 1 chiến lược đơn giản. FreqAI cần ≥ 4GB
RAM, 4 vCPU. RL training nên có GPU.

**Bot có hỗ trợ short không?**
Có, với futures/margin. Đặt `can_short = True` trong strategy và config
`trading_mode: futures`. Đọc [`docs/leverage.md`](../leverage.md).

**Có hỗ trợ DCA / partial exit?**
Có, bật `position_adjustment_enable = true`. Chi tiết trong
`adjust_trade_position` — [`docs/strategy-callbacks.md`](../strategy-callbacks.md#adjust-trade-position).

**Bot bị gọi rate-limit?**
Tăng `process_throttle_secs`, giảm số pair, dùng pairlist tối ưu hơn
(`AgeFilter`, `SpreadFilter` để bỏ pair "rác").

**Tôi muốn export lịch sử trade ra CSV?**
`freqtrade show-trades --print-json | jq ...`. Hoặc query trực tiếp
SQLite (xem [`docs/sql_cheatsheet.md`](../sql_cheatsheet.md)).

---

## Checklist 30 phút đầu tiên

- [ ] Cài Docker / venv.
- [ ] `create-userdir`, `new-config` (chọn dry-run, sàn ưa thích).
- [ ] `download-data` 30 ngày, 5m timeframe.
- [ ] `backtesting` với `SampleStrategy` để xác nhận setup ok.
- [ ] `trade` (dry-run) + `docker compose logs -f`.
- [ ] Mở UI ở http://localhost:8080 đăng nhập thành công.
- [ ] (tuỳ chọn) Bật Telegram, gửi `/status table`.

Tiếp theo: [05. Sử dụng nâng cao](05-su-dung-nang-cao.md).
