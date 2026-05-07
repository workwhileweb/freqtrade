# 03. Hướng dẫn build

Tài liệu này tập trung vào **build** Freqtrade dưới mọi dạng artefact:
môi trường phát triển (dev env), wheel/sdist Python, Docker image,
FreqUI, và bộ docs MkDocs. Phần "cài đặt để dùng" đặt ở
[04. Cài đặt, chạy và sử dụng](04-cai-dat-chay-su-dung.md).

> Lệnh được viết cho **PowerShell trên Windows**. Bạn sẽ thấy các block
> tương đương cho **bash/zsh** ngay bên dưới khi cú pháp khác.

## Mục lục

- [1. Yêu cầu hệ thống](#1-yêu-cầu-hệ-thống)
- [2. Lấy mã nguồn](#2-lấy-mã-nguồn)
- [3. Build môi trường dev](#3-build-môi-trường-dev)
- [4. Build wheel & sdist (PyPI artefact)](#4-build-wheel--sdist-pypi-artefact)
- [5. Build Docker image](#5-build-docker-image)
- [6. Build FreqUI](#6-build-frequi)
- [7. Build tài liệu MkDocs](#7-build-tài-liệu-mkdocs)
- [8. Lệnh kiểm tra build](#8-lệnh-kiểm-tra-build)
- [9. Build lại / Reset môi trường](#9-build-lại--reset-môi-trường)
- [10. Troubleshooting build](#10-troubleshooting-build)

---

## 1. Yêu cầu hệ thống

| Yêu cầu | Phiên bản | Ghi chú |
|---------|-----------|---------|
| Python | ≥ 3.11 (hỗ trợ 3.11–3.14) | Khai báo trong [`pyproject.toml`](../../pyproject.toml) `requires-python` |
| pip | mới nhất | `python -m pip install --upgrade pip` |
| git | bất kỳ | Cần để `git pull`, build version commit |
| TA-Lib (C library) | 0.4.x → < 0.7 | Wrapper `TA-Lib<0.7` ở `pyproject.toml` |
| Docker (tuỳ chọn) | 24+ | Cho build image / chạy container |
| Node.js (tuỳ chọn) | 20+ | Chỉ khi build FreqUI từ nguồn |
| MSVC Build Tools (Windows) | 2022+ | Cần khi build TA-Lib hoặc một số wheel native |

Yêu cầu chi tiết kèm hướng dẫn cài TA-Lib trên từng OS có ở
[`docs/installation.md`](../installation.md). Nếu bạn dùng Docker, bạn
**không** cần TA-Lib trên máy host.

Phần cứng tối thiểu (theo [README.md](../../README.md)): 2GB RAM, 1GB
disk, 2 vCPU.

---

## 2. Lấy mã nguồn

```powershell
# Trên Windows / PowerShell
git clone https://github.com/freqtrade/freqtrade.git
cd freqtrade
git checkout develop          # hoặc 'stable' cho phiên bản ổn định
```

```bash
# Trên Linux / macOS
git clone https://github.com/freqtrade/freqtrade.git
cd freqtrade
git checkout develop
```

Repo mặc định nằm trên branch `develop`. Nhánh
[`stable`](https://github.com/freqtrade/freqtrade/tree/stable) chứa
release đã đóng gói.

---

## 3. Build môi trường dev

Có **ba cách** chính. Chọn theo sở thích / OS.

### 3.1. Cách 1 — Script `setup.ps1` (Windows)

Script tự động: detect Python (3.11–3.14), tạo venv `.venv`, cài
requirements, cài freqtrade ở chế độ editable (`pip install -e .`), cài
FreqUI.

```powershell
# Bật execution policy lần đầu nếu cần
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\setup.ps1
```

Khi prompt yêu cầu chọn "requirement files", chọn:

- `A` (`requirements.txt`) — tối thiểu để chạy.
- Hoặc nhiều file qua dấu phẩy: `A,B,C` để cài thêm dev/hyperopt/freqai.

Sau khi chạy xong, kích hoạt venv:

```powershell
.\.venv\Scripts\Activate.ps1
freqtrade --version
```

Mã nguồn script: [`setup.ps1`](../../setup.ps1).

### 3.2. Cách 2 — Script `setup.sh` (Linux / macOS)

```bash
chmod +x setup.sh
./setup.sh -i        # full install (mandatory deps + venv)
source .venv/bin/activate
freqtrade --version
```

Script sẽ hỏi:

- *Install dependencies for development?* → `y` để cài
  [`requirements-dev.txt`](../../requirements-dev.txt) (tự kích hoạt
  pre-commit).
- *Plot?* → `y` để cài [`requirements-plot.txt`](../../requirements-plot.txt).
- *Hyperopt?* → `y` để cài [`requirements-hyperopt.txt`](../../requirements-hyperopt.txt).
- *FreqAI?* → `y` để cài [`requirements-freqai.txt`](../../requirements-freqai.txt).
- *FreqAI RL?* → `y` để cài thêm
  [`requirements-freqai-rl.txt`](../../requirements-freqai-rl.txt) (PyTorch + sb3).

Tham khảo các flag: `-i` install, `-u` update, `-r` reset, `-p` plot.

### 3.3. Cách 3 — Thủ công (mọi OS)

Chỉ dùng `pip`/`uv`. Linh hoạt nhất, hợp với Devcontainer / CI.

```powershell
# Tạo venv
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip wheel

# Cài full (dev + tất cả tuỳ chọn)
pip install -e ".[dev]"

# Hoặc cài từng phần:
# pip install -e ".[plot]"
# pip install -e ".[hyperopt]"
# pip install -e ".[freqai]"
# pip install -e ".[freqai_rl]"
# pip install -e ".[all]"        # tất cả tuỳ chọn không kèm dev
# pip install -e ".[develop]"    # chỉ tooling dev (pytest, ruff, mypy...)

# Cài pre-commit hook
pre-commit install
```

Các "extras" được khai báo ở
[`pyproject.toml`](../../pyproject.toml) phần
`[project.optional-dependencies]`:

| Extra | Cài thêm |
|-------|----------|
| `plot` | `plotly` |
| `hyperopt` | `optuna`, `cmaes`, `filelock`, `scikit-learn`, `scipy` |
| `freqai` | `lightgbm`, `xgboost`, `tensorboard`, `datasieve`, … |
| `freqai_rl` | `gymnasium`, `sb3-contrib`, `stable-baselines3`, `torch`, `tqdm` |
| `develop` | `pytest`, `pytest-*`, `mypy`, `ruff`, `pre-commit`, `time-machine`, ... |
| `jupyter` | `jupyter`, `ipykernel`, `nbconvert`, `nbstripout` |
| `all` | `plot + hyperopt + freqai + freqai_rl + jupyter` |
| `dev` | `all + develop` |

> Khuyến nghị: **dùng `[dev]` trong môi trường phát triển local**, dùng
> `[all]` cho user nâng cao không cần test/lint.

### 3.4. Cách 4 — Devcontainer (VSCode)

Repo cung cấp sẵn devcontainer ở
[`.devcontainer/`](../../.devcontainer/). Mở repo trong VSCode, cài
extension "Dev Containers", chọn "Reopen in Container". Container đã có
TA-Lib, Python, tooling — bạn chỉ việc code.

---

## 4. Build wheel & sdist (PyPI artefact)

Dành cho release và phân phối. Build dùng PEP 517/518:

```powershell
# Cài tooling
pip install --upgrade build twine

# Build cả sdist (.tar.gz) và wheel (.whl)
python -m build --sdist --wheel
```

Artefact xuất ra `dist/`:

```
dist/
├── freqtrade-<version>-py3-none-any.whl
└── freqtrade-<version>.tar.gz
```

`build-system` trong [`pyproject.toml`](../../pyproject.toml) khai báo:

```toml
[build-system]
requires = ["setuptools >= 64.0.0", "wheel"]
build-backend = "setuptools.build_meta"
```

Phiên bản lấy động từ
[`freqtrade/__init__.py`](../../freqtrade/__init__.py) `__version__`
(ví dụ `2026.5-dev` + commit hash khi đang trên dev branch).

Kiểm tra wheel trên TestPyPI trước khi push lên production:

```powershell
twine upload --repository-url https://test.pypi.org/legacy/ dist/*
```

Cần wheel/sdist phụ trợ (`ft_client`)? Xem
[`ft_client/README.md`](../../ft_client/README.md) — package này build
độc lập.

---

## 5. Build Docker image

### 5.1. Image chính (mặc định)

Dockerfile chính: [`Dockerfile`](../../Dockerfile). Base
`python:3.14.3-slim-trixie` + 2 stage (`python-deps` build wheel, `runtime-image` chạy
gọn nhẹ).

```powershell
docker build -t freqtrade:local .
```

Build có argument tuỳ chỉnh (ví dụ build từ một SHA cụ thể):

```powershell
docker build --build-arg "FREQTRADE_COMMIT=$(git rev-parse HEAD)" -t freqtrade:local .
```

Khi container chạy, freqtrade vào ENTRYPOINT `freqtrade` với CMD mặc
định `trade`. Cấu hình mount qua
[`docker-compose.yml`](../../docker-compose.yml) ánh xạ
`./user_data:/freqtrade/user_data`.

### 5.2. Image biến thể trong [`docker/`](../../docker/)

| Dockerfile | Mục đích |
|------------|----------|
| [`docker/Dockerfile.armhf`](../../docker/Dockerfile.armhf) | Build cho ARM 32-bit (Raspberry Pi 3/4) |
| [`docker/Dockerfile.plot`](../../docker/Dockerfile.plot) | Image kèm `plotly` |
| [`docker/Dockerfile.jupyter`](../../docker/Dockerfile.jupyter) | Image có Jupyter (cho notebook) |
| [`docker/Dockerfile.freqai`](../../docker/Dockerfile.freqai) | Image kèm dependencies FreqAI |
| [`docker/Dockerfile.freqai_rl`](../../docker/Dockerfile.freqai_rl) | Image FreqAI + RL (PyTorch) |
| [`docker/Dockerfile.custom`](../../docker/Dockerfile.custom) | Template để bạn extend với dependency riêng |

Ví dụ build `freqtrade:plot`:

```powershell
docker build -f docker/Dockerfile.plot -t freqtrade:plot .
```

### 5.3. Multi-arch build (CI)

CI chính thức dùng `buildx` để build cho `linux/amd64` + `linux/arm64`
(và `linux/arm/v7` cho `armhf`). Xem mục "Continuous integration" trong
[`docs/developer.md`](../developer.md). Lệnh tham khảo:

```powershell
docker buildx create --use --name ft-builder
docker buildx build --platform linux/amd64,linux/arm64 -t myorg/freqtrade:dev --push .
```

### 5.4. Tự build image custom

[`docker/Dockerfile.custom`](../../docker/Dockerfile.custom) là điểm
khởi đầu phổ biến để **thêm thư viện** (ví dụ một strategy bạn muốn pin
phiên bản). Sau khi sửa file, đổi build context trong
`docker-compose.yml`:

```yaml
build:
  context: .
  dockerfile: ./docker/Dockerfile.custom
```

Sau đó:

```powershell
docker compose build
docker compose up -d
```

---

## 6. Build FreqUI

FreqUI ([repo riêng](https://github.com/freqtrade/frequi)) là webapp
Vue.js. Bạn có hai lựa chọn:

### 6.1. Cài bản đã build sẵn (khuyến nghị)

`freqtrade install-ui` tải release mới nhất từ GitHub vào
`freqtrade/rpc/api_server/ui/installed/`:

```powershell
freqtrade install-ui
```

Code lệnh:
[`freqtrade/commands/deploy_ui.py`](../../freqtrade/commands/deploy_ui.py).

Cập nhật:

```powershell
freqtrade install-ui --erase
```

### 6.2. Build từ nguồn (nâng cao)

Chỉ làm khi bạn fork FreqUI để custom UI:

```powershell
git clone https://github.com/freqtrade/frequi.git
cd frequi
npm install
npm run build
# Copy dist/ vào <freqtrade-repo>/freqtrade/rpc/api_server/ui/installed/
```

---

## 7. Build tài liệu MkDocs

Bộ docs gốc tiếng Anh được build bằng
[mkdocs-material](https://squidfunk.github.io/mkdocs-material/), config
ở [`mkdocs.yml`](../../mkdocs.yml).

```powershell
pip install -r docs/requirements-docs.txt
mkdocs serve            # dev server localhost:8000
mkdocs build            # build static site vào ./site/
```

Khi viết docs mới, bạn nên:

- Đặt file `.md` trong [`docs/`](../).
- Đăng ký vào `nav` của [`mkdocs.yml`](../../mkdocs.yml) (file không
  được liệt kê sẽ không hiển thị trên trang chính thức).
- Test render: `mkdocs serve` rồi mở http://localhost:8000.

> Bộ docs `onboarding-vi` này (tài liệu bạn đang đọc) **không** được
> đưa vào `nav` để giữ site gốc nguyên vẹn — đây là tài liệu nội bộ
> của workspace.

---

## 8. Lệnh kiểm tra build

Sau mỗi lần build (đặc biệt sau install lại), chạy bộ "smoke test" sau
để chắc chắn:

```powershell
# 1. Phiên bản
freqtrade --version

# 2. CLI hoạt động
freqtrade --help
freqtrade trade --help

# 3. Test toàn bộ
pytest -q
# Hoặc chỉ chạy nhanh:
pytest -q -x

# 4. Lint + format
ruff check .
ruff format --check .

# 5. Type-check
mypy freqtrade

# 6. Pre-commit
pre-commit run -a

# 7. List sàn / strategy / hyperopt loss / pairlist (smoke check)
freqtrade list-exchanges
freqtrade list-strategies --strategy-path freqtrade/templates/
freqtrade list-hyperoptloss
freqtrade list-freqaimodels
```

Tham chiếu CI:
[`.github/workflows/`](../../.github/workflows/) cùng cấu hình
pre-commit ở
[`.pre-commit-config.yaml`](../../.pre-commit-config.yaml).

---

## 9. Build lại / Reset môi trường

### 9.1. Linux/macOS dùng `setup.sh`

```bash
./setup.sh -r       # hard reset (nuke .venv, recreate, cài lại)
./setup.sh -u       # update deps + git pull
```

### 9.2. Windows / thủ công

```powershell
# Xoá venv cũ
Remove-Item -Recurse -Force .venv

# Tạo lại
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip wheel
pip install -e ".[dev]"
pre-commit install
```

### 9.3. Dọn cache build

```powershell
Remove-Item -Recurse -Force build, dist, .pytest_cache, .mypy_cache, .ruff_cache, *.egg-info
```

```bash
rm -rf build dist .pytest_cache .mypy_cache .ruff_cache *.egg-info
```

---

## 10. Troubleshooting build

| Triệu chứng | Nguyên nhân thường gặp | Cách xử lý |
|-------------|------------------------|------------|
| `ERROR: TA-Lib library not found` khi `pip install` | Chưa cài C library TA-Lib | Cài qua `apt`/`brew`/MSI Windows; xem [`docs/installation.md`](../installation.md) |
| `Microsoft Visual C++ 14.0 or greater is required` | Thiếu MSVC build tools | Cài [Visual Studio Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/) |
| `pre-commit not found` | Bỏ qua bước install | `pip install pre-commit && pre-commit install` |
| `mypy: too many errors` | Kéo deps mới có type stubs khác | `pip install -U "freqtrade[develop]"` rồi `pre-commit run -a` |
| `pytest` chậm hoặc treo | Test online cần `--longrun` | Chạy `pytest -m "not longrun"` để bỏ qua |
| Docker build fail tại stage `python-deps` | Cache hỏng | `docker builder prune -af` rồi build lại |
| `freqtrade install-ui` lỗi 404 | Mạng / GitHub rate-limit | Đợi rồi thử lại, hoặc clone FreqUI build thủ công (mục 6.2) |
| `mkdocs serve` lỗi `python-markdown-math` | Thiếu deps docs | `pip install -r docs/requirements-docs.txt` |
| Lỗi `numpy.dtype size changed` khi import | Mismatch numpy/pandas/talib | Cài lại sạch theo `requirements.txt` |
| `freqtrade --version` không in được commit hash | Đứng ngoài git repo (ví dụ trong wheel) | Bình thường — `__init__.py` fallback |

> Không tìm thấy lỗi của bạn ở đây? Mở
> [issue tracker](https://github.com/freqtrade/freqtrade/issues) hoặc
> Discord (xem [`README.md`](../../README.md)).

---

## Checklist build "đã sẵn sàng phát triển"

- [ ] `python --version` ≥ 3.11.
- [ ] `pip list | findstr freqtrade` (Windows) hoặc `pip list | grep freqtrade` cho thấy bản editable (`/path/to/repo`).
- [ ] `freqtrade --version` chạy được.
- [ ] `pytest -q -x` pass (có thể skip một số test online).
- [ ] `pre-commit run -a` không cảnh báo.
- [ ] `mkdocs serve` mở được trang chủ docs gốc.
- [ ] `docker build -t freqtrade:local .` thành công.

Tiếp theo: [04. Cài đặt, chạy và sử dụng](04-cai-dat-chay-su-dung.md).
