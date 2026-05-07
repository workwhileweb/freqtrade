@echo off
setlocal EnableExtensions
cd /d "%~dp0"

REM Freqtrade Quick Config Builder launcher
REM Mo Gradio form de chon template + sinh user_data/config.json + (tuy chon) restart docker

REM ---------------------------------------------------------------
REM 1) Tim Python
REM ---------------------------------------------------------------
set "PY="
where py >nul 2>&1 && set "PY=py -3"
if "%PY%"=="" (
  where python >nul 2>&1 && set "PY=python"
)
if "%PY%"=="" (
  echo.
  echo [LOI] Khong tim thay Python tren PATH.
  echo Cai Python 3.10+ tu https://www.python.org/downloads/  roi chay lai run nay.
  exit /b 1
)
echo [INFO] Dung Python: %PY%

REM ---------------------------------------------------------------
REM 2) Venv rieng cho config builder de khong dung den freqtrade env
REM ---------------------------------------------------------------
set "VENV=%~dp0.cb_venv"
if not exist "%VENV%\Scripts\python.exe" (
  echo [INFO] Tao venv: %VENV%
  %PY% -m venv "%VENV%"
  if errorlevel 1 (
    echo [LOI] Khong tao duoc venv.
    exit /b 1
  )
)
set "VPY=%VENV%\Scripts\python.exe"

REM ---------------------------------------------------------------
REM 3) Cai Gradio neu chua co
REM ---------------------------------------------------------------
"%VPY%" -c "import gradio" 2>nul
if errorlevel 1 (
  echo [INFO] Cai Gradio vao venv (lan dau co the cham 1-2 phut)...
  "%VPY%" -m pip install --upgrade pip >nul
  "%VPY%" -m pip install "gradio>=4.40,<6"
  if errorlevel 1 (
    echo [LOI] Cai Gradio that bai.
    exit /b 1
  )
)

REM ---------------------------------------------------------------
REM 4) Mo browser
REM ---------------------------------------------------------------
set "PORT=7860"
echo.
echo [INFO] Mo Quick Config Builder tai http://127.0.0.1:%PORT%
echo [INFO] Bam Ctrl+C trong cua so nay de tat khi xong.
echo.
"%VPY%" "%~dp0scripts\config_builder.py" --host 127.0.0.1 --port %PORT%

endlocal
exit /b 0
