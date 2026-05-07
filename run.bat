@echo off
setlocal EnableExtensions
cd /d "%~dp0"

REM --- Thư mục dữ liệu trên host (map toàn bộ vào container) ---
set "USER_DATA=%~dp0user_data"
if not exist "%USER_DATA%" mkdir "%USER_DATA%"
if not exist "%USER_DATA%\logs" mkdir "%USER_DATA%\logs"
if not exist "%USER_DATA%\data" mkdir "%USER_DATA%\data"
if not exist "%USER_DATA%\strategies" mkdir "%USER_DATA%\strategies"
if not exist "%USER_DATA%\backtest_results" mkdir "%USER_DATA%\backtest_results"
if not exist "%USER_DATA%\hyperopt_results" mkdir "%USER_DATA%\hyperopt_results"
if not exist "%USER_DATA%\hyperopts" mkdir "%USER_DATA%\hyperopts"
if not exist "%USER_DATA%\notebooks" mkdir "%USER_DATA%\notebooks"
if not exist "%USER_DATA%\plot" mkdir "%USER_DATA%\plot"
if not exist "%USER_DATA%\freqaimodels" mkdir "%USER_DATA%\freqaimodels"

echo.
echo [1/2] Building Docker image "freqtrade:local" from current repo...
docker build -t freqtrade:local -f Dockerfile .
if errorlevel 1 (
  echo Build failed.
  exit /b 1
)

echo.
echo [2/2] Starting container with docker compose (user_data + config from .\user_data)...
docker compose -f docker-compose.local.yml up -d
if errorlevel 1 (
  echo Compose failed.
  exit /b 1
)

echo.
echo OK. Container: freqtrade-local
echo   Config:  .\user_data\config.json
echo   Logs:    .\user_data\logs\freqtrade.log
echo   DB:      .\user_data\tradesv3.sqlite
echo   UI/API:  http://127.0.0.1:8080
echo.
echo First-time setup (if chua co config):
echo   docker compose -f docker-compose.local.yml run --rm freqtrade create-userdir --userdir /freqtrade/user_data
echo   docker compose -f docker-compose.local.yml run --rm freqtrade new-config --config /freqtrade/user_data/config.json
echo.
echo Logs stream: docker compose -f docker-compose.local.yml logs -f
echo Stop:        docker compose -f docker-compose.local.yml down
endlocal
exit /b 0
