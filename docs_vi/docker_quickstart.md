<!-- Auto-translated from docs/ by script. Please review technical terms. -->

# Sử dụng Freqtrade với Docker

Trang này giải thích cách chạy bot với Docker. Nó không có nghĩa là để làm việc ra khỏi hộp. Bạn vẫn cần phải đọc qua tài liệu và hiểu cách cấu hình nó đúng cách.

## Cài đặt Docker

Bắt đầu bằng cách tải xuống và cài đặt Docker/Docker Desktop cho nền tảng của bạn:* [Mac](https://docs.docker.com/docker-for-mac/install/)
* [Windows](https://docs.docker.com/docker-for-windows/install/)
* [Linux](https://docs.docker.com/install/)
!!! Thông tin "Cài đặt soạn thảo Docker"
    Tài liệu Freqtrade giả định việc sử dụng máy tính để bàn Docker (hoặc plugin soạn thảo docker).  
    Mặc dù cài đặt độc lập docker-compose vẫn hoạt động, nhưng nó sẽ yêu cầu thay đổi tất cả các lệnh `docker soạn thảo` từ `docker soạn thảo` thành `docker-compose` để hoạt động (ví dụ: `docker soạn thảo -d` sẽ trở thành `docker-compose up -d`).

??? Cảnh báo "Docker trên windows"
    Nếu bạn vừa cài đặt docker trên hệ thống windows, hãy đảm bảo khởi động lại hệ thống của bạn, nếu không, bạn có thể gặp phải các Sự cố không thể giải thích được liên quan đến kết nối mạng với vùng chứa docker.

## Giao dịch thường xuyên với dockerFreqtrade provides an official Docker image on [Dockerhub](https://hub.docker.com/r/freqtradeorg/freqtrade/), as well as a [docker compose file](https://github.com/freqtrade/freqtrade/blob/stable/docker-compose.yml) ready for usage.
!!! Lưu ý
    - Phần sau giả định rằng `docker` đã được cài đặt và có sẵn cho người dùng đã đăng nhập.
    - Tất cả các lệnh dưới đây đều sử dụng các thư mục tương đối và sẽ phải được thực thi từ thư mục chứa file `docker-compose.yml`.

### Docker khởi động nhanhCreate a new directory and place the [docker-compose file](https://raw.githubusercontent.com/freqtrade/freqtrade/stable/docker-compose.yml) in this directory.
``` bash
mkdir ft_userdata
cd ft_userdata/
# Download the docker-compose file from the repository
curl https://raw.githubusercontent.com/freqtrade/freqtrade/stable/docker-compose.yml -o docker-compose.yml

# Pull the freqtrade image
docker compose pull

# Create user directory structure
docker compose run --rm freqtrade create-userdir --userdir user_data

# Create configuration - Requires answering interactive questions
docker compose run --rm freqtrade new-config --config user_data/config.json
```Đoạn mã trên tạo một thư mục mới có tên `ft_userdata`, tải xuống tệp soạn thảo mới nhất và lấy hình ảnh freqtrade.
2 bước cuối cùng trong đoạn mã sẽ tạo thư mục có `user_data`, cũng như (tương tác) cấu hình mặc định dựa trên các lựa chọn của bạn.

!!! Câu hỏi "Làm cách nào để chỉnh sửa cấu hình bot?"
    Bạn có thể chỉnh sửa cấu hình bất kỳ lúc nào, có sẵn dưới dạng `user_data/config.json` (trong thư mục `ft_userdata`) khi sử dụng cấu hình trên.

    Bạn cũng có thể thay đổi cả Chiến lược và lệnh bằng cách chỉnh sửa phần lệnh của tệp `docker-compose.yml`.

#### Thêm chiến lược tùy chỉnh

1. Cấu hình hiện có sẵn dưới dạng `user_data/config.json`
2. Sao chép chiến lược tùy chỉnh vào thư mục `user_data/strategies/`
3. Thêm tên lớp của Chiến lược vào tệp `docker-compose.yml`

`SampleStrategy` được chạy theo mặc định.

!!! Nguy hiểm "`SampleStrategy` chỉ là bản demo!"
    `Chiến lược mẫu` có sẵn để bạn tham khảo và cung cấp cho bạn ý tưởng cho chiến lược của riêng bạn.
    Vui lòng luôn kiểm tra lại chiến lược của bạn và sử dụng thử nghiệm một thời gian trước khi mạo hiểm với tiền thật!
    Bạn sẽ tìm thấy thêm thông tin về việc phát triển Chiến lược trong [Tài liệu về chiến lược](strategy-customization.md).

Khi việc này hoàn tất, bạn đã sẵn sàng khởi chạy bot ở chế độ giao dịch (Giao dịch khô hoặc Giao dịch trực tiếp, tùy thuộc vào câu trả lời của bạn cho câu hỏi tương ứng bạn đã đưa ra ở trên).``` bash
docker compose up -d
```!!! Cảnh báo "Cấu hình mặc định"
    Mặc dù cấu hình được tạo hầu hết sẽ hoạt động nhưng bạn vẫn cần xác minh rằng tất cả các tùy chọn đều tương ứng với những gì bạn muốn (như Giá cả, danh sách cặp, ...) trước khi khởi động bot.

#### Truy cập giao diện người dùng

Nếu bạn đã chọn bật FreqUI ở bước `new-config`, bạn sẽ có sẵn freqUI tại cổng `localhost:8080`.

Bây giờ bạn có thể truy cập giao diện người dùng bằng cách nhập localhost:8080 vào trình duyệt của mình.

??? Lưu ý "Truy cập giao diện người dùng trên máy chủ từ xa"
    Nếu đang chạy trên VPS, bạn nên cân nhắc sử dụng đường hầm ssh hoặc thiết lập VPN (openVPN, wireguard) để kết nối với bot của mình.
    Điều này sẽ đảm bảo rằng freqUI không tiếp xúc trực tiếp với internet, điều này không được khuyến khích vì lý do bảo mật (freqUI không hỗ trợ https ngay từ đầu).
    Việc thiết lập các công cụ này không nằm trong hướng dẫn này, tuy nhiên bạn có thể tìm thấy nhiều hướng dẫn hay trên internet.
    Ngoài ra, vui lòng đọc phần [Cấu hình API với docker](rest-api.md#configuration-with-docker) để tìm hiểu thêm về cấu hình này.

#### Giám sát bot

Bạn có thể kiểm tra các phiên bản đang chạy bằng `docker soạn ps`.
Điều này sẽ liệt kê dịch vụ `freqtrade` là` đang chạy`. Nếu không phải như vậy, tốt nhất hãy kiểm tra nhật ký (xem điểm tiếp theo).

#### Docker soạn nhật ký

Nhật ký sẽ được ghi vào: `user_data/logs/freqtrade.log`.  
Bạn cũng có thể kiểm tra nhật ký mới nhất bằng lệnh `docker soạn log -f`.

#### Cơ sở dữ liệu

Cơ sở dữ liệu sẽ được đặt tại: `user_data/tradesv3.sqlite`

#### Cập nhật freqtrade bằng docker

Cập nhật freqtrade khi sử dụng `docker` chỉ đơn giản là chạy 2 lệnh sau:``` bash
# Download the latest image
docker compose pull
# Restart the image
docker compose up -d
```Điều này trước tiên sẽ kéo hình ảnh mới nhất và sau đó sẽ khởi động lại vùng chứa với phiên bản vừa kéo.

!!! Cảnh báo "Kiểm tra nhật ký thay đổi"
    Bạn phải luôn kiểm tra nhật ký thay đổi để biết các thay đổi đáng chú ý/các biện pháp can thiệp thủ công cần thiết và đảm bảo bot khởi động chính xác sau khi cập nhật.

### Chỉnh sửa tập tin docker-compose

Người dùng nâng cao có thể chỉnh sửa thêm tệp soạn thảo docker để bao gồm tất cả các tùy chọn hoặc đối số có thể có.

Tất cả các đối số freqtrade sẽ có sẵn bằng cách chạy `docker soạn run --rm freqtrade <lệnh> <đối số tùy chọn>`.

!!! Cảnh báo "`docker soạn` cho các lệnh giao dịch"
    Không nên chạy các lệnh giao dịch (`freqtrade giao dịch <...>`) thông qua `docker soạn run` - mà thay vào đó nên sử dụng `docker soạn lên -d`.
    Điều này đảm bảo rằng vùng chứa được khởi động đúng cách (bao gồm cả chuyển tiếp cổng) và sẽ đảm bảo rằng vùng chứa sẽ khởi động lại sau khi khởi động lại hệ thống.
    Nếu bạn định sử dụng freqUI, vui lòng đảm bảo điều chỉnh [cấu hình phù hợp](rest-api.md#configuration-with-docker), nếu không thì giao diện người dùng sẽ không khả dụng.

!!! Lưu ý "`docker soạn run --rm`"
    Bao gồm `--rm` sẽ loại bỏ vùng chứa sau khi hoàn thành và được khuyến nghị cao cho tất cả các chế độ ngoại trừ chế độ giao dịch (chạy với lệnh `freqtrade Trade`).

??? Lưu ý "Sử dụng docker mà không soạn docker"
    "`docker soạn thảo chạy --rm`" sẽ yêu cầu cung cấp tệp soạn thảo.
    Thay vào đó, một số lệnh freqtrade không yêu cầu xác thực, chẳng hạn như `list-pairs` có thể được chạy bằng "`docker run --rm`".  
    Ví dụ: `docker run --rm freqtradeorg/freqtrade:stable list-pairs --exchange binance --quote BTC --print-json`.  
    Điều này có thể hữu ích khi tìm nạp thông tin trao đổi để thêm vào `config.json` mà không ảnh hưởng đến vùng chứa đang chạy của bạn.

#### Ví dụ: Download data bằng docker

Tải xuống dữ liệu kiểm tra ngược trong 5 ngày cho cặp ETH/BTC và khung thời gian 1h từ Binance. Dữ liệu sẽ được lưu trữ trong thư mục `user_data/data/` trên máy chủ.``` bash
docker compose run --rm freqtrade download-data --pairs ETH/BTC --exchange binance --days 5 -t 1h
```Hãy truy cập [Tài liệu tải xuống dữ liệu](data-download.md) để biết thêm chi tiết về cách tải xuống dữ liệu.

#### Ví dụ: Backtest với docker

Chạy thử nghiệm ngược trong vùng chứa docker cho SampleStrategy và phạm vi thời gian được chỉ định của dữ liệu lịch sử, trên khung thời gian 5 phút:``` bash
docker compose run --rm freqtrade backtesting --config user_data/config.json --strategy SampleStrategy --timerange 20190801-20191001 -i 5m
```Hãy truy cập [Tài liệu Backtesting](backtesting.md) để tìm hiểu thêm.

### Các phần phụ thuộc bổ sung với docker

Nếu chiến lược của bạn yêu cầu các phần phụ thuộc không có trong hình ảnh mặc định - bạn sẽ cần phải xây dựng hình ảnh trên máy chủ của mình.For this, please create a Dockerfile containing installation steps for the additional dependencies (have a look at [docker/Dockerfile.custom](https://github.com/freqtrade/freqtrade/blob/develop/docker/Dockerfile.custom) for an example).
Sau đó, bạn cũng cần sửa đổi tệp `docker-compose.yml` và bỏ ghi chú bước xây dựng, cũng như đổi tên hình ảnh để tránh xung đột khi đặt tên.``` yaml
    image: freqtrade_custom
    build:
      context: .
      dockerfile: "./Dockerfile.<yourextension>"
```Sau đó, bạn có thể chạy `docker soạn build --pull` để xây dựng hình ảnh docker và chạy nó bằng các lệnh được mô tả ở trên.

### Vẽ đồ thị bằng docker

Các lệnh `freqtradeplot-profit` và `freqtradeplot-dataframe` ([Documentation](plotting.md)) có sẵn bằng cách thay đổi hình ảnh thành `*_plot` trong tệp `docker-compose.yml` của bạn.
Sau đó, bạn có thể sử dụng các lệnh này như sau:``` bash
docker compose run --rm freqtrade plot-dataframe --strategy AwesomeStrategy -p BTC/ETH --timerange=20180801-20180805
```Kết quả đầu ra sẽ được lưu trữ trong thư mục `user_data/plot` và có thể mở được bằng bất kỳ trình duyệt hiện đại nào.

### Phân tích dữ liệu bằng docker soạn

Freqtrade cung cấp tệp soạn thảo docker để khởi động máy chủ phòng thí nghiệm jupyter.
Bạn có thể chạy máy chủ này bằng lệnh sau:``` bash
docker compose -f docker/docker-compose-jupyter.yml up
```This will create a docker-container running jupyter lab, which will be accessible using `https://127.0.0.1:8888/lab`.
Vui lòng sử dụng liên kết được in trong bảng điều khiển sau khi khởi động để đăng nhập đơn giản hơn.

Vì một phần của hình ảnh này được tạo trên máy của bạn nên bạn nên thỉnh thoảng xây dựng lại hình ảnh để luôn cập nhật freqtrade (và các phần phụ thuộc).``` bash
docker compose -f docker/docker-compose-jupyter.yml build --no-cache
```## Khắc phục sự cố

### Docker trên Windows

* Lỗi: `"Dấu thời gian cho yêu cầu này nằm ngoài recvWindow."`  
  Các yêu cầu api thị trường yêu cầu đồng hồ được đồng bộ hóa nhưng thời gian trong vùng chứa docker sẽ thay đổi một chút về quá khứ theo thời gian.
  Để khắc phục sự cố này tạm thời, bạn cần chạy `wsl --shutdown` và khởi động lại docker (một cửa sổ bật lên trên windows 10 sẽ yêu cầu bạn làm như vậy).
  Một giải pháp lâu dài là lưu trữ bộ chứa docker trên máy chủ linux hoặc thỉnh thoảng khởi động lại wsl bằng bộ lập lịch.``` bash
  taskkill /IM "Docker Desktop.exe" /F
  wsl --shutdown
  start "" "C:\Program Files\Docker\Docker\Docker Desktop.exe"
  ```* Không thể kết nối với API (Windows)  
  Nếu bạn đang sử dụng windows và vừa cài đặt Docker (máy tính để bàn), hãy đảm bảo khởi động lại Hệ thống của bạn. Docker có thể gặp sự cố với kết nối mạng nếu không khởi động lại.
  Rõ ràng bạn cũng nên đảm bảo có [settings](#accessing-the-ui) tương ứng.

!!! Cảnh báo
    Do những điều trên, chúng tôi không khuyến nghị sử dụng docker trên windows để thiết lập sản xuất mà chỉ để thử nghiệm, tải xuống dữ liệu và kiểm tra lại.
    Tốt nhất hãy sử dụng linux-VPS để chạy freqtrade một cách đáng tin cậy.