<!-- Auto-translated from docs/ by script. Please review technical terms. -->

# Cài đặt

Trang này giải thích cách chuẩn bị môi trường để chạy bot.

Tài liệu freqtrade mô tả nhiều cách khác nhau để cài đặt freqtrade

* [Hình ảnh Docker](docker_quickstart.md) (trang riêng)
* [Cài đặt tập lệnh](#script-installation)
* [Cài đặt thủ công](#cài đặt thủ công)
* [Cài đặt bằng Conda](#installation-with-conda)

Vui lòng cân nhắc sử dụng [hình ảnh docker](docker_quickstart.md) dựng sẵn để bắt đầu nhanh chóng.

!!! Lưu ý "Đang cập nhật"
    Việc cập nhật freqtrade là điều quan trọng để [đảm bảo khả năng tương thích liên tục](update.md#why-update) với API của sàn giao dịch.
    Vui lòng tham khảo [hướng dẫn cập nhật](update.md) để biết chi tiết về cách cập nhật cài đặt của bạn.

!!! Lưu ý "Người dùng Windows"
    Chúng tôi **thực sự** khuyên người dùng Windows nên sử dụng [Docker](docker_quickstart.md) vì điều này sẽ hoạt động dễ dàng và mượt mà hơn nhiều (cũng an toàn hơn).

    Nếu điều đó là không thể, hãy thử sử dụng hệ thống con Windows Linux (WSL) - hướng dẫn Ubuntu/Linux sẽ hoạt động.
    Nếu bạn thực sự muốn cài đặt freqtrade nguyên bản trên Windows, tốt nhất hãy sử dụng tập lệnh cài đặt [`./setup.ps1`](#use-setupps1-windows).

    Ngoài ra, vui lòng đảm bảo sử dụng phiên bản Python 64 bit, vì phiên bản 32 bit có giới hạn bộ nhớ nghiêm trọng, điều này có thể tác động tiêu cực đến trải nghiệm của bạn với backtesting/hyperopt.

------

## Thông tin

Cách dễ nhất để cài đặt và chạy Freqtrade là sao chép kho lưu trữ bot Github rồi chạy tập lệnh `./setup.sh` (`./setup.ps1` cho Windows), nếu nó có sẵn cho nền tảng của bạn.

!!! Lưu ý "Cân nhắc phiên bản"
    Khi nhân bản kho lưu trữ, nhánh làm việc mặc định có tên `develop`. Nhánh này chứa tất cả các tính năng cuối cùng (có thể được coi là tương đối ổn định nhờ các thử nghiệm tự động).
    Nhánh `stable` chứa mã của bản phát hành cuối cùng (thường được thực hiện mỗi tháng một lần trên ảnh chụp nhanh khoảng một tuần trước của nhánh `develop` để tránh lỗi đóng gói, do đó có khả năng nó ổn định hơn).

!!! Ghi chú    Either [uv](https://docs.astral.sh/uv/), or Python3.11 or higher and the corresponding `pip` are assumed to be available. The install-script will warn you and stop if that's not the case. `git` is also needed to clone the Freqtrade repository.  
Ngoài ra, các tiêu đề python (`python<yourversion>-dev` / `python<yourversion>-devel`) phải có sẵn để quá trình cài đặt hoàn tất thành công.

!!! Cảnh báo "Đồng hồ cập nhật"
    Đồng hồ trên hệ thống chạy bot phải chính xác, được đồng bộ hóa với máy chủ NTP đủ thường xuyên để tránh các vấn đề khi liên lạc với các sàn giao dịch.

------

## Yêu cầu

Những yêu cầu này áp dụng cho cả [Cài đặt tập lệnh](#cài đặt tập lệnh) và [Cài đặt thủ công](#cài đặt thủ công).

!!! Lưu ý "Hệ thống ARM64"
    Nếu bạn đang chạy hệ thống ARM64 (như MacOS M1 hoặc Oracle VM), vui lòng sử dụng [docker](docker_quickstart.md) để chạy freqtrade.
    Mặc dù có thể cài đặt gốc bằng một số nỗ lực thủ công nhưng hiện tại điều này không được hỗ trợ.

### Hướng dẫn cài đặt* [Python >= 3.11](http://docs.python-guide.org/en/latest/starting/installation/)
* [pip](https://pip.pypa.io/en/stable/installing/)
* [git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
* [virtualenv](https://virtualenv.pypa.io/en/stable/installation.html) (Recommended)
### Mã cài đặt

Chúng tôi đã bao gồm/thu thập hướng dẫn cài đặt cho Ubuntu, MacOS và Windows. Đây là những nguyên tắc và thành công của bạn có thể khác nhau tùy theo các bản phân phối khác.
Các bước cụ thể của hệ điều hành được liệt kê đầu tiên, phần chung bên dưới là cần thiết cho tất cả các hệ thống.

!!! Lưu ý
    Python3.11 trở lên và pip tương ứng được coi là có sẵn.

=== "Debian/Ubuntu"
    #### Cài đặt các phụ thuộc cần thiết```bash
    # update repository
    sudo apt-get update

    # install packages
    sudo apt install -y python3-pip python3-venv python3-dev python3-pandas git curl
    ```=== "MacOS"
    #### Cài đặt các phụ thuộc cần thiết    Install [Homebrew](https://brew.sh/) if you don't have it already.
```bash
    # install packages
    brew install gettext libomp
    ```!!! Lưu ý
        Tập lệnh `setup.sh` sẽ cài đặt các phần phụ thuộc này cho bạn - giả sử brew được cài đặt trên hệ thống của bạn.

=== "RaspberryPi/Raspbian"    The following assumes the latest [Raspbian Buster lite image](https://www.raspberrypi.org/downloads/raspbian/).
Hình ảnh này được cài đặt sẵn python3.11, giúp dễ dàng thiết lập và chạy freqtrade.

    Đã thử nghiệm bằng Raspberry Pi 3 với hình ảnh Raspbian Buster lite, tất cả các bản cập nhật đều được áp dụng.```bash
    sudo apt-get install python3-venv libatlas-base-dev cmake curl libffi-dev
    # Use piwheels.org to speed up installation
    sudo echo "[global]\nextra-index-url=https://www.piwheels.org/simple" > tee /etc/pip.conf

    git clone https://github.com/freqtrade/freqtrade.git
    cd freqtrade

    bash setup.sh -i
    ```!!! Lưu ý "Thời gian cài đặt"
        Tùy thuộc vào tốc độ Internet của bạn và phiên bản Raspberry Pi, quá trình cài đặt có thể mất nhiều giờ để hoàn tất.
        Do đó, chúng tôi khuyên bạn nên sử dụng hình ảnh docker dựng sẵn cho Raspberry, bằng cách làm theo [Tài liệu khởi động nhanh Docker](docker_quickstart.md)

    !!! Lưu ý
        Ở trên không cài đặt phụ thuộc hyperopt. Để cài đặt những thứ này, vui lòng sử dụng `python3 -m pip install -e .[hyperopt]`.
        Chúng tôi không khuyên bạn nên chạy hyperopt trên Raspberry Pi, vì đây là một hoạt động rất tốn tài nguyên và cần được thực hiện trên máy mạnh.

------

## Kho lưu trữ Freqtrade

Freqtrade là một bot giao dịch tiền điện tử mã nguồn mở, có mã được lưu trữ trên `github.com````bash
# Download `develop` branch of freqtrade repository
git clone https://github.com/freqtrade/freqtrade.git

# Enter downloaded directory
cd freqtrade

# your choice (1): novice user
git checkout stable

# your choice (2): advanced user
git checkout develop
```(1) Lệnh này chuyển kho lưu trữ nhân bản sang sử dụng nhánh `ổn định`. Nó không cần thiết nếu bạn muốn ở lại nhánh (2) `develop`.

Sau này, bạn có thể chuyển đổi giữa các nhánh bất kỳ lúc nào bằng lệnh `git kiểm tra ổn định`/`git kiểm tra phát triển`.

??? Lưu ý "Cài đặt từ pypi"    An alternative way to install Freqtrade is from [pypi](https://pypi.org/project/freqtrade/). The downside is that this method requires ta-lib to be correctly installed beforehand, and is therefore currently not the recommended way to install Freqtrade.
``` bash
    pip install freqtrade
    ```------

## Cài đặt tập lệnh

Cách đầu tiên để cài đặt Freqtrade là sử dụng tập lệnh `./setup.sh` của Linux/MacOS được cung cấp để cài đặt tất cả các phần phụ thuộc và giúp bạn định cấu hình bot.

Đảm bảo bạn đáp ứng [Yêu cầu](#requirements) và đã tải xuống [Freqtrade repo](#freqtrade-repository).

### Sử dụng /setup.sh -install (Linux/MacOS)

Nếu bạn đang dùng Debian, Ubuntu hoặc MacOS, freqtrade sẽ cung cấp tập lệnh để cài đặt freqtrade.```bash
# --install, Install freqtrade from scratch
./setup.sh -i
```#### Các tùy chọn khác của tập lệnh /setup.sh

Bạn cũng có thể cập nhật, định cấu hình và đặt lại cơ sở mã của bot bằng `./setup.sh````bash
# --update, Command git pull to update.
./setup.sh -u
# --reset, Hard reset your develop/stable branch.
./setup.sh -r
``````
** --install **

With this option, the script will install the bot and most dependencies:
You will need to have git and python3.11+ installed beforehand for this to work.

* Mandatory software as: `ta-lib`
* Setup your virtualenv under `.venv/`

This option is a combination of installation tasks and `--reset`

** --update **

This option will pull the last version of your current branch and update your virtualenv. Run the script with this option periodically to update your bot.

** --reset **

This option will hard reset your branch (only if you are on either `stable` or `develop`) and recreate your virtualenv.
```#### Kích hoạt môi trường ảo của bạn

Mỗi lần bạn mở một thiết bị đầu cuối mới, bạn phải chạy `source .venv/bin/activate` để kích hoạt môi trường ảo của mình.```bash
# activate virtual environment
source ./.venv/bin/activate
```### Sử dụng ./setup.ps1 (Windows)

Tập lệnh sẽ hỏi bạn một số câu hỏi để xác định phần nào sẽ được cài đặt.```powershell
Set-ExecutionPolicy -ExecutionPolicy Bypass
cd freqtrade
. .\setup.ps1
```#### Kích hoạt môi trường ảo của bạn (Windows)```powershell
# activate virtual environment
. .\.venv\Scripts\Activate.ps1
```[Bây giờ bạn đã sẵn sàng](#bạn-sẵn sàng) chạy bot.

-----

## Cài đặt thủ công

Đảm bảo bạn đáp ứng [Yêu cầu](#requirements) và đã tải xuống [Freqtrade repo](#freqtrade-repository).

### Thiết lập môi trường ảo Python (virtualenv)

Bạn sẽ chạy freqtrade trong `môi trường ảo` riêng biệt```bash
# create virtualenv in directory /freqtrade/.venv
python3 -m venv .venv

# run virtualenv
source .venv/bin/activate
```### Cài đặt phụ thuộc python```bash
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
# install freqtrade
python3 -m pip install -e .
```[Bây giờ bạn đã sẵn sàng](#bạn-sẵn sàng) chạy bot.

### (Tùy chọn) Nhiệm vụ sau cài đặt

!!! Ghi chú    If you run the bot on a server, you should consider using [Docker](docker_quickstart.md) or a terminal multiplexer like `screen` or [`tmux`](https://en.wikipedia.org/wiki/Tmux) to avoid that the bot is stopped on logout.
Trên Linux với bộ phần mềm `systemd`, như một tác vụ sau cài đặt tùy chọn, bạn có thể muốn thiết lập bot để chạy dưới dạng `dịch vụ systemd` hoặc định cấu hình nó để gửi thông điệp tường trình đến các daemon `syslog`/`rsyslog` hoặc `journald`. Xem [Ghi nhật ký nâng cao](advanced-setup.md#advanced-logging) để biết chi tiết.

------

## Cài đặt với Conda

Freqtrade cũng có thể được cài đặt với Miniconda hoặc Anaconda. Chúng tôi khuyên bạn nên sử dụng Miniconda vì dung lượng cài đặt của nó nhỏ hơn. Conda sẽ tự động chuẩn bị và quản lý các phần phụ thuộc vào thư viện mở rộng của chương trình Freqtrade.

### Conda là gì?Conda is a package, dependency and environment manager for multiple programming languages: [conda docs](https://docs.conda.io/projects/conda/en/latest/index.html)
### Cài đặt bằng conda

#### Cài đặt Conda[Installing on linux](https://conda.io/projects/conda/en/latest/user-guide/install/linux.html#install-linux-silent)
[Installing on windows](https://conda.io/projects/conda/en/latest/user-guide/install/windows.html)
Trả lời tất cả các câu hỏi. Sau khi cài đặt, bắt buộc phải TẮT và BẬT lại thiết bị đầu cuối của bạn.

#### Tải xuống Freqtrade

Tải xuống và cài đặt freqtrade.```bash
# download freqtrade
git clone https://github.com/freqtrade/freqtrade.git

# enter downloaded directory 'freqtrade'
cd freqtrade      
```#### Tần suất cài đặt: Conda Environment```bash
conda create --name freqtrade python=3.12
```!!! Lưu ý "Tạo môi trường Conda"
    Lệnh conda `create -n` tự động cài đặt tất cả các phần phụ thuộc lồng nhau cho các thư viện đã chọn, cấu trúc chung của lệnh cài đặt là:```bash
    # choose your own packages
    conda env create -n [name of the environment] [python version] [packages]
    ```#### Vào/ra môi trường freqtrade

Để kiểm tra các môi trường có sẵn, gõ```bash
conda env list
```Nhập môi trường đã cài đặt```bash
# enter conda environment
conda activate freqtrade

# exit conda environment - don't do it now
conda deactivate
```Cài đặt phụ thuộc python cuối cùng với pip```bash
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
python3 -m pip install -e .
```[Bây giờ bạn đã sẵn sàng](#bạn-sẵn sàng) chạy bot.

### Các phím tắt quan trọng```bash
# list installed conda environments
conda env list

# activate base environment
conda activate

# activate freqtrade environment
conda activate freqtrade

#deactivate any conda environments
conda deactivate                              
```### Thông tin thêm về Anaconda

!!! Thông tin "Gói nặng mới"
    Có thể xảy ra trường hợp việc tạo môi trường Conda mới, chứa các gói đã chọn tại thời điểm tạo, sẽ mất ít thời gian hơn so với việc cài đặt một thư viện hoặc ứng dụng lớn, nặng vào môi trường đã thiết lập trước đó.

!!! Cảnh báo "cài đặt pip trong conda"
    Tài liệu của conda nói rằng KHÔNG nên sử dụng pip trong conda vì có thể xảy ra sự cố nội bộ.    However, they are rare. [Anaconda Blogpost](https://www.anaconda.com/blog/using-pip-in-a-conda-environment)
Tuy nhiên, đó là lý do tại sao kênh `conda-forge` được ưa thích hơn:

    * có nhiều thư viện hơn (ít cần `pip` hơn)
    * `conda-forge` hoạt động tốt hơn với `pip`
    * các thư viện mới hơn

Chúc bạn giao dịch vui vẻ!

------

## Bạn đã sẵn sàng

Bạn đã làm được điều này, vậy là bạn đã cài đặt freqtrade thành công.

### Khởi tạo cấu hình```bash
# Step 1 - Initialize user folder
freqtrade create-userdir --userdir user_data

# Step 2 - Create a new configuration file
freqtrade new-config --config user_data/config.json
```Bạn đã sẵn sàng chạy, hãy đọc [Cấu hình Bot](configuration.md), hãy nhớ bắt đầu bằng `dry_run: True` và xác minh rằng mọi thứ đều hoạt động.

Để tìm hiểu cách thiết lập cấu hình của bạn, vui lòng tham khảo trang tài liệu [Cấu hình Bot](configuration.md).

### Khởi động Bot```bash
freqtrade trade --config user_data/config.json --strategy SampleStrategy
```!!! Cảnh báo
    Bạn nên đọc qua phần còn lại của tài liệu, kiểm tra lại chiến lược bạn sẽ sử dụng và sử dụng thử nghiệm trước khi cho phép giao dịch bằng tiền thật.

-----

## Khắc phục sự cố

### Vấn đề thường gặp: "không tìm thấy lệnh"

Nếu bạn sử dụng cài đặt (1)`Script` hoặc (2)`Manual`, bạn cần chạy bot trong môi trường ảo. Nếu bạn gặp lỗi như dưới đây, hãy đảm bảo venv đang hoạt động.```bash
# if:
bash: freqtrade: command not found

# then activate your virtual environment
source ./.venv/bin/activate
```###Lỗi cài đặt MacOS

Các phiên bản MacOS mới hơn có thể cài đặt không thành công với các lỗi như `error: command 'g++' failed with exit status 1`.

Lỗi này sẽ yêu cầu cài đặt rõ ràng các Tiêu đề SDK, tiêu đề này không được cài đặt theo mặc định trong phiên bản MacOS này.
Đối với MacOS 10.14, điều này có thể được thực hiện bằng lệnh bên dưới.```bash
open /Library/Developer/CommandLineTools/Packages/macOS_SDK_headers_for_macOS_10.14.pkg
```Nếu tệp này không tồn tại thì có thể bạn đang sử dụng phiên bản MacOS khác, vì vậy, bạn có thể cần tham khảo trên Internet để biết chi tiết về độ phân giải cụ thể.

### Lỗi cài đặt Windows```bash
error: Microsoft Visual C++ 14.0 is required. Get it with "Microsoft Visual C++ Build Tools": http://landinghub.visualstudio.com/visual-cpp-build-tools
```Thật không may, nhiều gói yêu cầu biên dịch không cung cấp bánh xe dựng sẵn. Do đó, bắt buộc phải cài đặt và có sẵn trình biên dịch C/C++ cho môi trường python của bạn để sử dụng.You can download the Visual C++ build tools from [the Visual Studio website](https://visualstudio.microsoft.com/visual-cpp-build-tools/) and install "Desktop development with C++" in it's default configuration. Unfortunately, this is a heavy download / dependency so you might want to consider WSL2 or [docker compose](docker_quickstart.md) first.
![Cài đặt Windows](assets/windows_install.png)