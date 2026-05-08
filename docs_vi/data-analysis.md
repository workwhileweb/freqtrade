<!-- Auto-translated from docs/ by script. Please review technical terms. -->

# Phân tích dữ liệu bot bằng sổ ghi chép Jupyter

Bạn có thể phân tích kết quả kiểm tra ngược và lịch sử giao dịch một cách dễ dàng bằng sổ ghi chép Jupyter. Sổ ghi chép mẫu được đặt tại `user_data/notebooks/` sau khi khởi tạo thư mục người dùng với `freqtrade create-userdir --userdir user_data`.

## Bắt đầu nhanh với docker

Freqtrade cung cấp tệp soạn thảo docker để khởi động máy chủ phòng thí nghiệm jupyter.
Bạn có thể chạy máy chủ này bằng lệnh sau: `docker soạn -f docker/docker-compose-jupyter.yml up`This will create a dockercontainer running jupyter lab, which will be accessible using `https://127.0.0.1:8888/lab`.
Vui lòng sử dụng liên kết được in trong bảng điều khiển sau khi khởi động để đăng nhập đơn giản hơn.

Để biết thêm thông tin, vui lòng truy cập phần [Phân tích dữ liệu với Docker](docker_quickstart.md#data-analysis-USE-docker-compose).

### Lời khuyên chuyên nghiệp* See [jupyter.org](https://jupyter.org/documentation) for usage instructions.
* Don't forget to start a Jupyter notebook server from within your conda or venv environment or use [nb_conda_kernels](https://github.com/Anaconda-Platform/nb_conda_kernels)*
* Sao chép sổ tay mẫu trước khi sử dụng để những thay đổi của bạn không bị ghi đè trong bản cập nhật freqtrade tiếp theo.

### Sử dụng môi trường ảo với cài đặt Jupyter trên toàn hệ thống

Đôi khi, bạn có thể muốn sử dụng cài đặt sổ ghi chép Jupyter trên toàn hệ thống và sử dụng kernel jupyter từ môi trường ảo.
Điều này ngăn bạn cài đặt bộ jupyter đầy đủ nhiều lần trên mỗi hệ thống và cung cấp một cách dễ dàng để chuyển đổi giữa các tác vụ (freqtrade / các tác vụ phân tích khác).

Để tính năng này hoạt động, trước tiên hãy kích hoạt môi trường ảo của bạn và chạy các lệnh sau:``` bash
# Activate virtual environment
source .venv/bin/activate

pip install ipykernel
ipython kernel install --user --name=freqtrade
# Restart jupyter (lab / notebook)
# select kernel "freqtrade" in the notebook
```!!! Ghi chú    This section is provided for completeness, the Freqtrade Team won't provide full support for problems with this setup and will recommend to install Jupyter in the virtual environment directly, as that is the easiest way to get jupyter notebooks up and running. For help with this setup please refer to the [Project Jupyter](https://jupyter.org/) [documentation](https://jupyter.org/documentation) or [help channels](https://jupyter.org/community).
!!! Cảnh báo
    Một số tác vụ không hoạt động tốt trong sổ ghi chép. Ví dụ: bất kỳ điều gì sử dụng thực thi không đồng bộ đều là một vấn đề đối với Jupyter. Ngoài ra, điểm vào chính của freqtrade là shell cli, do đó, việc sử dụng python thuần trong sổ ghi chép sẽ bỏ qua các đối số cung cấp các đối tượng và tham số cần thiết cho các hàm trợ giúp. Bạn có thể cần đặt các giá trị đó hoặc tạo các đối tượng mong muốn theo cách thủ công.

## Quy trình làm việc được đề xuất

| Nhiệm vụ | Công cụ |
  --- | ---
Hoạt động của bot | CLI
Nhiệm vụ lặp đi lặp lại | Tập lệnh Shell
Phân tích và trực quan hóa dữ liệu | Sổ tay

1. Sử dụng CLI để

    * tải dữ liệu lịch sử
    * chạy backtest
    * chạy với dữ liệu thời gian thực
    * kết quả xuất khẩu

1. Thu thập các hành động này trong tập lệnh shell

    * lưu các lệnh phức tạp với các đối số
    * thực hiện các hoạt động nhiều bước
    * tự động hóa các chiến lược thử nghiệm và chuẩn bị dữ liệu để phân tích

1. Dùng sổ ghi chép để

    * trực quan hóa dữ liệu
    * Mangle và âm mưu để tạo ra những hiểu biết sâu sắc

## Đoạn mã tiện ích mẫu

### Thay đổi thư mục thành root

Sổ ghi chép Jupyter thực thi từ thư mục sổ ghi chép. Đoạn mã sau tìm kiếm gốc dự án, vì vậy các đường dẫn tương đối vẫn nhất quán.```python
import os
from pathlib import Path

# Change directory
# Modify this cell to insure that the output shows the correct path.
# Define all paths relative to the project root shown in the cell output
project_root = "somedir/freqtrade"
i=0
try:
    os.chdir(project_root)
    assert Path('LICENSE').is_file()
except:
    while i<4 and (not Path('LICENSE').is_file()):
        os.chdir(Path(Path.cwd(), '../'))
        i+=1
    project_root = Path.cwd()
print(Path.cwd())
```### Tải nhiều file cấu hình

Tùy chọn này có thể hữu ích để kiểm tra kết quả của việc chuyển nhiều cấu hình.
Điều này cũng sẽ chạy qua toàn bộ quá trình khởi tạo Cấu hình, do đó cấu hình được khởi tạo hoàn toàn để chuyển sang các phương thức khác.``` python
import json
from freqtrade.configuration import Configuration

# Load config from multiple files
config = Configuration.from_files(["config1.json", "config2.json"])

# Show the config in memory
print(json.dumps(config['original_config'], indent=2))
```Đối với môi trường Tương tác, hãy có cấu hình bổ sung chỉ định `user_data_dir` và chuyển cấu hình này vào cuối cùng, để bạn không phải thay đổi thư mục trong khi chạy bot.
Tốt nhất nên tránh các đường dẫn tương đối, vì đường dẫn này bắt đầu ở vị trí lưu trữ của sổ ghi chép jupyter, trừ khi thư mục bị thay đổi.``` json
{
    "user_data_dir": "~/.freqtrade/"
}
```### Tài liệu phân tích dữ liệu bổ sung

* [Gỡ lỗi chiến lược](strategy_analysis_example.md) - cũng có sẵn dưới dạng sổ ghi chép Jupyter (`user_data/notebooks/strategy_analysis_example.ipynb`)
* [Plotting](plotting.md)
* [Phân tích thẻ](advanced-backtesting.md)

Vui lòng gửi vấn đề hoặc Yêu cầu kéo nâng cao tài liệu này nếu bạn muốn chia sẻ ý tưởng về cách phân tích dữ liệu tốt nhất.