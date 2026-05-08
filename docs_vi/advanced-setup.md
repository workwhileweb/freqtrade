<!-- Auto-translated from docs/ by script. Please review technical terms. -->

# Nhiệm vụ nâng cao sau cài đặt

Trang này giải thích một số tác vụ nâng cao và tùy chọn cấu hình có thể được thực hiện sau khi cài đặt bot và có thể hữu ích trong một số môi trường.

Nếu bạn không biết những điều được đề cập ở đây có nghĩa là gì thì có thể bạn không cần nó.

## Chạy nhiều phiên bản của Freqtrade

Phần này sẽ hướng dẫn bạn cách chạy nhiều bot cùng lúc, trên cùng một máy.

###Những điều cần cân nhắc

* Sử dụng các tập tin cơ sở dữ liệu khác nhau.
* Sử dụng các bot Telegram khác nhau (yêu cầu nhiều tệp cấu hình khác nhau; chỉ áp dụng khi Telegram được bật).
* Sử dụng các cổng khác nhau (chỉ áp dụng khi máy chủ web Freqtrade REST API được bật).

### Các tệp cơ sở dữ liệu khác nhau

Để theo dõi các giao dịch, lợi nhuận, v.v. của bạn, freqtrade đang sử dụng cơ sở dữ liệu SQLite nơi lưu trữ nhiều loại thông tin khác nhau như các giao dịch bạn đã thực hiện trong quá khứ và (các) vị trí hiện tại bạn đang nắm giữ bất kỳ lúc nào. Điều này cho phép bạn theo dõi lợi nhuận của mình, nhưng quan trọng nhất là theo dõi hoạt động đang diễn ra nếu quá trình bot được khởi động lại hoặc bị chấm dứt đột ngột.

Theo mặc định, Freqtrade sẽ sử dụng các tệp cơ sở dữ liệu riêng biệt cho các bot chạy thử và trực tiếp (điều này giả định rằng không có url cơ sở dữ liệu nào được đưa ra trong cấu hình cũng như thông qua đối số dòng lệnh).
Đối với chế độ giao dịch trực tiếp, cơ sở dữ liệu mặc định sẽ là `tradesv3.sqlite` và đối với chế độ chạy thử, nó sẽ là `tradesv3.dryrun.sqlite`.

Đối số tùy chọn cho lệnh giao dịch được sử dụng để chỉ định đường dẫn của các tệp này là `--db-url`, yêu cầu url SQLAlchemy hợp lệ.
Vì vậy, khi bạn khởi động bot chỉ có các đối số cấu hình và chiến lược ở chế độ chạy thử, 2 lệnh sau sẽ có kết quả tương tự.``` bash
freqtrade trade -c MyConfig.json -s MyStrategy
# is equivalent to
freqtrade trade -c MyConfig.json -s MyStrategy --db-url sqlite:///tradesv3.dryrun.sqlite
```Điều đó có nghĩa là nếu bạn đang chạy lệnh giao dịch ở hai thiết bị đầu cuối khác nhau, chẳng hạn như để kiểm tra chiến lược của bạn cho cả giao dịch bằng USDT và trong một trường hợp khác cho giao dịch bằng BTC, bạn sẽ phải chạy chúng với các cơ sở dữ liệu khác nhau.

Nếu bạn chỉ định URL của cơ sở dữ liệu không tồn tại, freqtrade sẽ tạo một cơ sở dữ liệu có tên bạn đã chỉ định. Vì vậy, để kiểm tra chiến lược tùy chỉnh của bạn với tiền đặt cược BTC và USDT, bạn có thể sử dụng các lệnh sau (trong 2 thiết bị đầu cuối riêng biệt):``` bash
# Terminal 1:
freqtrade trade -c MyConfigBTC.json -s MyCustomStrategy --db-url sqlite:///user_data/tradesBTC.dryrun.sqlite
# Terminal 2:
freqtrade trade -c MyConfigUSDT.json -s MyCustomStrategy --db-url sqlite:///user_data/tradesUSDT.dryrun.sqlite
```Ngược lại, nếu bạn muốn thực hiện điều tương tự trong chế độ sản xuất, bạn cũng sẽ phải tạo ít nhất một cơ sở dữ liệu mới (ngoài cơ sở dữ liệu mặc định) và chỉ định đường dẫn đến cơ sở dữ liệu "trực tiếp", ví dụ:``` bash
# Terminal 1:
freqtrade trade -c MyConfigBTC.json -s MyCustomStrategy --db-url sqlite:///user_data/tradesBTC.live.sqlite
# Terminal 2:
freqtrade trade -c MyConfigUSDT.json -s MyCustomStrategy --db-url sqlite:///user_data/tradesUSDT.live.sqlite
```Để biết thêm thông tin về việc sử dụng cơ sở dữ liệu sqlite, chẳng hạn như nhập hoặc xóa giao dịch theo cách thủ công, vui lòng tham khảo [Bảng tính SQL](sql_cheatsheet.md).

### Nhiều phiên bản sử dụng docker

Để chạy nhiều phiên bản freqtrade bằng docker, bạn sẽ cần chỉnh sửa tệp docker-compose.yml và thêm tất cả các phiên bản bạn muốn dưới dạng dịch vụ riêng biệt. Hãy nhớ rằng, bạn có thể tách cấu hình của mình thành nhiều tệp, vì vậy, bạn nên nghĩ đến việc biến chúng thành mô-đun, sau đó nếu cần chỉnh sửa nội dung nào đó chung cho tất cả các bot, bạn có thể thực hiện việc đó trong một tệp cấu hình duy nhất.``` yml
---
version: '3'
services:
  freqtrade1:
    image: freqtradeorg/freqtrade:stable
    # image: freqtradeorg/freqtrade:develop
    # Use plotting image
    # image: freqtradeorg/freqtrade:develop_plot
    # Build step - only needed when additional dependencies are needed
    # build:
    #   context: .
    #   dockerfile: "./docker/Dockerfile.custom"
    restart: always
    container_name: freqtrade1
    volumes:
      - "./user_data:/freqtrade/user_data"
    # Expose api on port 8080 (localhost only)
    # Please read the https://www.freqtrade.io/en/stable/rest-api/ documentation
    # before enabling this.
     ports:
     - "127.0.0.1:8080:8080"
    # Default command used when running `docker compose up`
    command: >
      trade
      --logfile /freqtrade/user_data/logs/freqtrade1.log
      --db-url sqlite:////freqtrade/user_data/tradesv3_freqtrade1.sqlite
      --config /freqtrade/user_data/config.json
      --config /freqtrade/user_data/config.freqtrade1.json
      --strategy SampleStrategy
  
  freqtrade2:
    image: freqtradeorg/freqtrade:stable
    # image: freqtradeorg/freqtrade:develop
    # Use plotting image
    # image: freqtradeorg/freqtrade:develop_plot
    # Build step - only needed when additional dependencies are needed
    # build:
    #   context: .
    #   dockerfile: "./docker/Dockerfile.custom"
    restart: always
    container_name: freqtrade2
    volumes:
      - "./user_data:/freqtrade/user_data"
    # Expose api on port 8080 (localhost only)
    # Please read the https://www.freqtrade.io/en/stable/rest-api/ documentation
    # before enabling this.
    ports:
      - "127.0.0.1:8081:8080"
    # Default command used when running `docker compose up`
    command: >
      trade
      --logfile /freqtrade/user_data/logs/freqtrade2.log
      --db-url sqlite:////freqtrade/user_data/tradesv3_freqtrade2.sqlite
      --config /freqtrade/user_data/config.json
      --config /freqtrade/user_data/config.freqtrade2.json
      --strategy SampleStrategy

```Bạn có thể sử dụng bất kỳ quy ước đặt tên nào bạn muốn, freqtrade1 và 2 là tùy ý. Lưu ý rằng bạn sẽ cần sử dụng các tệp cơ sở dữ liệu, ánh xạ cổng và cấu hình điện tín khác nhau cho từng phiên bản, như đã đề cập ở trên. 

## Sử dụng hệ thống cơ sở dữ liệu khác

Freqtrade đang sử dụng SQLAlchemy, hỗ trợ nhiều hệ thống cơ sở dữ liệu khác nhau. Như vậy, vô số hệ thống cơ sở dữ liệu cần được hỗ trợ.Freqtrade does not depend or install any additional database driver. Please refer to the [SQLAlchemy docs](https://docs.sqlalchemy.org/en/14/core/engines.html#database-urls) on installation instructions for the respective database systems.
Các hệ thống sau đã được thử nghiệm và được biết là hoạt động với freqtrade:

* sqlite (mặc định)
* PostgreSQL
* MariaDB

!!! Cảnh báo
    Bằng cách sử dụng một trong các hệ thống cơ sở dữ liệu dưới đây, bạn xác nhận rằng bạn biết cách quản lý hệ thống đó. Nhóm freqtrade sẽ không cung cấp bất kỳ hỗ trợ nào về thiết lập hoặc bảo trì (hoặc sao lưu) các hệ thống cơ sở dữ liệu bên dưới.

###PostgreSQL

Cài đặt:
` cài đặt pip "psycopg [nhị phân]"`

Cách sử dụng:
`... --db-url postgresql+psycopg://<username>:<password>@localhost:5432/<database>`

Freqtrade sẽ tự động tạo các bảng cần thiết khi khởi động.

Nếu đang chạy các phiên bản Freqtrade khác nhau, bạn phải thiết lập một cơ sở dữ liệu cho mỗi phiên bản hoặc sử dụng những người dùng/lược đồ khác nhau cho kết nối của mình.

### MariaDB / MySQL

Freqtrade hỗ trợ MariaDB bằng cách sử dụng SQLAlchemy, hỗ trợ nhiều hệ thống cơ sở dữ liệu khác nhau.

Cài đặt:
`pip cài đặt pymysql`

Cách sử dụng:
`... --db-url mysql+pymysql://<username>:<password>@localhost:3306/<database>`



## Định cấu hình bot chạy dưới dạng dịch vụ systemd

Sao chép tệp `freqtrade.service` vào thư mục người dùng systemd của bạn (thường là `~/.config/systemd/user`) và cập nhật `WorkingDirectory` và `ExecStart` để phù hợp với thiết lập của bạn.

!!! Lưu ý
    Một số hệ thống nhất định (như Raspbian) không tải tệp đơn vị dịch vụ từ thư mục người dùng. Trong trường hợp này, sao chép `freqtrade.service` vào `/etc/systemd/user/` (yêu cầu quyền siêu người dùng).

Sau đó, bạn có thể khởi động daemon bằng:```bash
systemctl --user start freqtrade
```Để việc này được duy trì liên tục (chạy khi người dùng đăng xuất), bạn cần bật `linger` cho người dùng freqtrade của mình.```bash
sudo loginctl enable-linger "$USER"
```Nếu bạn chạy bot dưới dạng dịch vụ, bạn có thể sử dụng trình quản lý dịch vụ systemd làm bot giám sát phần mềm freqtrade 
trạng thái và khởi động lại nó trong trường hợp thất bại. Nếu tham số `internals.sd_notify` được đặt thành true trong 
cấu hình hoặc tùy chọn dòng lệnh `--sd-notify` được sử dụng, bot sẽ gửi tin nhắn ping liên tục tới systemd 
sử dụng giao thức sd_notify (thông báo systemd) và cũng sẽ cho systemd biết trạng thái hiện tại của nó (Đang chạy, Tạm dừng hoặc Đã dừng) 
khi nó thay đổi. 

Tệp `freqtrade.service.watchdog` chứa ví dụ về tệp cấu hình đơn vị dịch vụ sử dụng systemd 
với tư cách là cơ quan giám sát.

!!! Lưu ý
    Giao tiếp sd_notify giữa bot và trình quản lý dịch vụ systemd sẽ không hoạt động nếu bot chạy trong vùng chứa Docker.

## Ghi nhật ký nâng cao

Freqtrade sử dụng mô-đun ghi nhật ký mặc định do python cung cấp.Python allows for extensive [logging configuration](https://docs.python.org/3/library/logging.config.html#logging.config.dictConfig) in this regard - way more than what can be covered here.
Định dạng ghi nhật ký mặc định (đầu ra thiết bị đầu cuối có màu) được thiết lập theo mặc định nếu không cung cấp `log_config` trong cấu hình freqtrade của bạn.
Việc sử dụng `--logfile logfile.log` sẽ kích hoạt RotatingFileHandler.

Nếu bạn không hài lòng với định dạng nhật ký hoặc với cài đặt mặc định được cung cấp cho RotatingFileHandler, bạn có thể tùy chỉnh việc ghi nhật ký theo ý thích của mình bằng cách thêm cấu hình `log_config` vào (các) tệp cấu hình freqtrade của bạn.

Cấu hình mặc định trông gần giống như bên dưới, với trình xử lý tệp được cung cấp nhưng không được bật vì `tên tệp` được nhận xét.
Bỏ ghi chú dòng này và cung cấp đường dẫn/tên tệp hợp lệ để kích hoạt nó.``` json hl_lines="5-7 13-16 27"
{
  "log_config": {
      "version": 1,
      "formatters": {
          "basic": {
              "format": "%(message)s"
          },
          "standard": {
              "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
          }
      },
      "handlers": {
          "console": {
              "class": "freqtrade.loggers.ft_rich_handler.FtRichHandler",
              "formatter": "basic"
          },
          "file": {
              "class": "logging.handlers.RotatingFileHandler",
              "formatter": "standard",
              // "filename": "someRandomLogFile.log",
              "maxBytes": 10485760,
              "backupCount": 10
          }
      },
      "root": {
          "handlers": [
              "console",
              // "file"
          ],
          "level": "INFO",
      }
  }
}
```!!! Lưu ý "các dòng được đánh dấu"
    Các dòng được đánh dấu trong khối mã ở trên xác định trình xử lý Rich và thuộc về nhau.
    Trình định dạng "tiêu chuẩn" và "tệp" sẽ thuộc về FileHandler.

Mỗi trình xử lý phải sử dụng một trong các trình định dạng đã xác định (theo tên), lớp của nó phải có sẵn và phải là lớp ghi nhật ký hợp lệ.
Để thực sự sử dụng trình xử lý, nó phải nằm trong phần "trình xử lý" bên trong phân đoạn "gốc".
Nếu phần này bị bỏ qua, freqtrade sẽ không cung cấp đầu ra (dù sao trong trình xử lý không được định cấu hình).

!!! Mẹo "Cấu hình nhật ký rõ ràng"
    Chúng tôi khuyên bạn nên trích xuất cấu hình ghi nhật ký từ tệp cấu hình freqtrade chính của mình và cung cấp cấu hình đó cho bot của bạn thông qua chức năng [nhiều tệp cấu hình](configuration.md#multiple-configuration-files). Điều này sẽ tránh việc sao chép mã không cần thiết.

---

Trên nhiều hệ thống Linux, bot có thể được cấu hình để gửi thông điệp tường trình của nó tới các dịch vụ hệ thống `syslog` hoặc `journald`. Đăng nhập vào máy chủ `syslog` từ xa cũng có sẵn trên Windows. Các giá trị đặc biệt cho tùy chọn dòng lệnh `--logfile` có thể được sử dụng cho việc này.

### Đăng nhập vào nhật ký hệ thống

Để gửi thông báo nhật ký Freqtrade tới dịch vụ `syslog` cục bộ hoặc từ xa, hãy sử dụng tùy chọn thiết lập `"log_config"` để định cấu hình ghi nhật ký.``` json
{
  // ...
  "log_config": {
    "version": 1,
    "formatters": {
      "syslog_fmt": {
        "format": "%(name)s - %(levelname)s - %(message)s"
      }
    },
    "handlers": {
      // Other handlers? 
      "syslog": {
         "class": "logging.handlers.SysLogHandler",
          "formatter": "syslog_fmt",
          // Use one of the other options above as address instead? 
          "address": "/dev/log"
      }
    },
    "root": {
      "handlers": [
        // other handlers
        "syslog",
        
      ]
    }

  }
}
```[Trình xử lý nhật ký bổ sung](#advanced-logging) có thể cần phải được định cấu hình để chẳng hạn như cũng có đầu ra nhật ký trong bảng điều khiển.

#### Sử dụng nhật ký hệ thống

Thông điệp tường trình được gửi đến `syslog` với tiện ích `user`. Vì vậy, bạn có thể nhìn thấy chúng bằng các lệnh sau:

* `tail -f /var/log/user`, hoặc
* cài đặt trình xem đồ họa toàn diện (ví dụ: 'Trình xem tệp nhật ký' cho Ubuntu).

Trên nhiều hệ thống, `syslog` (`rsyslog`) tìm nạp dữ liệu từ `journald` (và ngược lại), do đó, cả syslog hoặc tạp chí đều có thể được sử dụng và các tin nhắn có thể được xem bằng cả `journalctl` và tiện ích xem nhật ký hệ thống. Bạn có thể kết hợp điều này theo bất kỳ cách nào phù hợp với bạn hơn.

Đối với `rsyslog`, các tin nhắn từ bot có thể được chuyển hướng sang một tệp nhật ký chuyên dụng riêng. Để đạt được điều này, hãy thêm```
if $programname startswith "freqtrade" then -/var/log/freqtrade.log
```vào một trong các tệp cấu hình rsyslog, ví dụ như ở cuối `/etc/rsyslog.d/50-default.conf`.

Đối với `syslog` (`rsyslog`), chế độ giảm có thể được bật. Điều này sẽ làm giảm số lượng tin nhắn lặp lại. Ví dụ: nhiều tin nhắn Heartbeat của bot sẽ được giảm xuống thành một tin nhắn duy nhất khi không có gì khác xảy ra với bot. Để đạt được điều này, hãy đặt trong `/etc/rsyslog.conf`:```
# Filter duplicated messages
$RepeatedMsgReduction on
```#### Địa chỉ nhật ký hệ thống

Địa chỉ nhật ký hệ thống có thể là ổ cắm miền Unix (tên tệp ổ cắm) hoặc đặc tả ổ cắm UDP, bao gồm địa chỉ IP và cổng UDP, được phân tách bằng ký tự `:`.

Vì vậy, sau đây là ví dụ về các địa chỉ có thể:

* `"address": "/dev/log"` -- đăng nhập vào syslog (rsyslog) bằng socket `/dev/log`, phù hợp với hầu hết các hệ thống.
* `"address": "/var/run/syslog"` -- đăng nhập vào syslog (rsyslog) bằng socket `/var/run/syslog`. Sử dụng cái này trên MacOS.
* `"address": "localhost:514"` -- đăng nhập vào syslog cục bộ bằng ổ cắm UDP, nếu nó lắng nghe trên cổng 514.
* `"address": "<ip>:514"` -- đăng nhập vào nhật ký hệ thống từ xa tại địa chỉ IP và cổng 514. Điều này có thể được sử dụng trên Windows để ghi nhật ký từ xa vào máy chủ nhật ký hệ thống bên ngoài.

??? Thông tin "Không dùng nữa - định cấu hình nhật ký hệ thống qua dòng lệnh"
    `--logfile syslog:<syslog_address>` -- gửi thông điệp tường trình đến dịch vụ `syslog` bằng cách sử dụng `<syslog_address>` làm địa chỉ nhật ký hệ thống.

    Địa chỉ nhật ký hệ thống có thể là ổ cắm miền Unix (tên tệp ổ cắm) hoặc đặc tả ổ cắm UDP, bao gồm địa chỉ IP và cổng UDP, được phân tách bằng ký tự `:`.

    Vì vậy, sau đây là những ví dụ về cách sử dụng có thể:

    * `--logfile syslog:/dev/log` -- đăng nhập vào syslog (rsyslog) bằng socket `/dev/log`, phù hợp với hầu hết các hệ thống.
    * `--logfile syslog` -- giống như trên, phím tắt cho `/dev/log`.
    * `--logfile syslog:/var/run/syslog` -- đăng nhập vào syslog (rsyslog) bằng socket `/var/run/syslog`. Sử dụng cái này trên MacOS.
    * `--logfile syslog:localhost:514` -- đăng nhập vào syslog cục bộ bằng ổ cắm UDP, nếu nó lắng nghe trên cổng 514.
    * `--logfile syslog:<ip>:514` -- đăng nhập vào syslog từ xa tại địa chỉ IP và cổng 514. Điều này có thể được sử dụng trên Windows để ghi nhật ký từ xa vào máy chủ syslog bên ngoài.

### Đang đăng nhập vào tạp chí

Điều này cần cài đặt gói python `cysystemd` làm phần phụ thuộc (`pip install cysystemd`), gói này không có sẵn trên Windows. Do đó, toàn bộ chức năng ghi nhật ký không có sẵn cho bot chạy trên Windows.

Để gửi thông báo nhật ký Freqtrade tới dịch vụ hệ thống `journald`, hãy thêm đoạn mã cấu hình sau vào cấu hình của bạn.``` json
{
  // ...
  "log_config": {
    "version": 1,
    "formatters": {
      "journald_fmt": {
        "format": "%(name)s - %(levelname)s - %(message)s"
      }
    },
    "handlers": {
      // Other handlers? 
      "journald": {
         "class": "cysystemd.journal.JournaldLogHandler",
          "formatter": "journald_fmt",
      }
    },
    "root": {
      "handlers": [
        // .. 
        "journald",
        
      ]
    }

  }
}
```[Trình xử lý nhật ký bổ sung](#advanced-logging) có thể cần phải được định cấu hình để chẳng hạn như cũng có đầu ra nhật ký trong bảng điều khiển.

Thông điệp tường trình được gửi tới `journald` với tiện ích `user`. Vì vậy, bạn có thể nhìn thấy chúng bằng các lệnh sau:

* `journalctl -f` -- hiển thị các thông điệp tường trình Freqtrade được gửi tới `journald` cùng với các thông điệp tường trình khác được `journald` tìm nạp.
* `journalctl -f -u freqtrade.service` -- lệnh này có thể được sử dụng khi bot chạy dưới dạng dịch vụ `systemd`.

Có rất nhiều tùy chọn khác trong tiện ích `journalctl` để lọc tin nhắn, xem trang hướng dẫn sử dụng tiện ích này.

Trên nhiều hệ thống, `syslog` (`rsyslog`) tìm nạp dữ liệu từ `journald` (và ngược lại), vì vậy cả `--logfile syslog` hoặc `--logfile tạp chí` đều có thể được sử dụng và các tin nhắn có thể được xem bằng cả `journalctl` và tiện ích xem nhật ký hệ thống. Bạn có thể kết hợp điều này theo bất kỳ cách nào phù hợp với bạn hơn.

??? Thông tin "Không dùng nữa - định cấu hình tạp chí thông qua dòng lệnh"
    Để gửi thông điệp nhật ký Freqtrade tới dịch vụ hệ thống `journald`, hãy sử dụng tùy chọn dòng lệnh `--logfile` với giá trị ở định dạng sau:

    `--logfile tạp chí` -- gửi thông điệp tường trình tới `journald`.

### Định dạng nhật ký dưới dạng JSON

Thay vào đó, bạn cũng có thể định cấu hình luồng đầu ra mặc định để sử dụng định dạng JSON.The "fmt_dict" attribute defines the keys for the json output - as well as the [python logging LogRecord attributes](https://docs.python.org/3/library/logging.html#logrecord-attributes).
Cấu hình bên dưới sẽ thay đổi đầu ra mặc định thành JSON. Tuy nhiên, trình định dạng tương tự cũng có thể được sử dụng kết hợp với `RotatingFileHandler`.
Chúng tôi khuyên bạn nên giữ một định dạng ở dạng con người có thể đọc được.``` json
{
  // ...
  "log_config": {
    "version": 1,
    "formatters": {
       "json": {
          "()": "freqtrade.loggers.json_formatter.JsonFormatter",
          "fmt_dict": {
              "timestamp": "asctime",
              "level": "levelname",
              "logger": "name",
              "message": "message"
          }
      }
    },
    "handlers": {
      // Other handlers? 
      "jsonStream": {
          "class": "logging.StreamHandler",
          "formatter": "json"
      }
    },
    "root": {
      "handlers": [
        // .. 
        "jsonStream",
        
      ]
    }

  }
}
```