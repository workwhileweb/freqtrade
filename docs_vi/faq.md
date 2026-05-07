<!-- Auto-translated from docs/ by script. Please review technical terms. -->

# Câu hỏi thường gặp về giao dịch thường xuyên

## Thị trường được hỗ trợ

Freqtrade hỗ trợ giao dịch giao ngay cũng như giao dịch tương lai cho một số sàn giao dịch được chọn. Vui lòng tham khảo [trang bắt đầu tài liệu](index.md#supported-futures-exchanges) để biết danh sách cập nhật các sàn giao dịch được hỗ trợ.

### Bot của tôi có thể mở các vị thế bán không?

Freqtrade có thể mở các vị thế bán trên thị trường tương lai.
Điều này đòi hỏi phải lập chiến lược cho việc này - và `"trading_mode": "tương lai"` trong cấu hình.
Trước tiên hãy đảm bảo đọc [trang tài liệu liên quan](đòn bẩy.md).

Trên thị trường giao ngay, trong một số trường hợp, bạn có thể sử dụng token giao ngay có đòn bẩy, phản ánh một cặp đảo ngược (ví dụ: BTCUP/USD, BTCDOWN/USD, ETHBULL/USD, ETHBEAR/USD,...) có thể được giao dịch với Freqtrade.

### Bot của tôi có thể giao dịch quyền chọn hoặc hợp đồng tương lai không?

Giao dịch tương lai được hỗ trợ cho các sàn giao dịch được chọn. Vui lòng tham khảo [trang bắt đầu tài liệu](index.md#supported-futures-exchanges) để biết danh sách cập nhật các sàn giao dịch được hỗ trợ.

## Mẹo & thủ thuật cho người mới bắt đầu

* Khi bạn làm việc với tệp chiến lược & hyperopt, bạn nên sử dụng trình chỉnh sửa mã thích hợp như VSCode hoặc PyCharm. Một trình soạn thảo mã tốt sẽ cung cấp tính năng đánh dấu cú pháp cũng như số dòng, giúp bạn dễ dàng tìm ra lỗi cú pháp (rất có thể được Freqtrade chỉ ra trong quá trình khởi động).

## Câu hỏi thường gặp về Freqtrade

### Freqtrade có thể mở song song nhiều vị thế trên cùng một cặp không?

Không. Freqtrade sẽ chỉ mở một vị thế cho mỗi cặp tại một thời điểm.
Tuy nhiên, bạn có thể sử dụng lệnh gọi lại [`just_trade_position()`](strategy-callbacks.md# adjustment-trade-position) để điều chỉnh vị thế mở.

Kiểm tra ngược cung cấp tùy chọn cho việc này trong `--eps` - tuy nhiên, tùy chọn này chỉ ở đó để làm nổi bật các tín hiệu "ẩn" và sẽ không hoạt động trực tiếp.

### freqtrade có hỗ trợ tài khoản sandbox không?

Không, nhưng bạn có thể sử dụng chế độ chạy thử để mô phỏng giao dịch mà không gặp rủi ro về tiền thật.

Thị trường hộp cát là các thị trường mô phỏng, riêng biệt - không phù hợp để thử nghiệm chiến lược của bạn trong môi trường thực tế.
Những thị trường này thường có sổ lệnh, tính thanh khoản và hành vi giao dịch khác nhau (thường có rất ít người tham gia) - điều này khiến chúng không phù hợp để thử nghiệm thực tế chiến lược của bạn.

### Bot không khởi động

Chạy bot với `freqtrade giao dịch --config config.json` hiển thị kết quả `freqtrade: không tìm thấy lệnh`.

Điều này có thể được gây ra bởi những lý do sau:

* Môi trường ảo không hoạt động.
  * Chạy `source .venv/bin/activate` để kích hoạt môi trường ảo.
* Quá trình cài đặt không hoàn tất thành công.
  * Vui lòng kiểm tra [Tài liệu cài đặt](installation.md).

### Bot khởi động nhưng ở chế độ STOPPED

Đảm bảo bạn đặt tùy chọn cấu hình `initial_state` thành `"running"` trong config.json của bạn

### Tôi đợi 5 phút rồi mà sao bot vẫn chưa thực hiện giao dịch nào?

* Tùy thuộc vào chiến lược gia nhập, số lượng xu được đưa vào danh sách trắng,
tình hình thị trường, v.v., có thể mất tới hàng giờ hoặc hàng ngày để tìm được điểm vào tốt
vị trí cho một giao dịch. Hãy kiên nhẫn!

* Việc kiểm tra ngược sẽ cho bạn biết đại khái số lượng giao dịch dự kiến ​​- nhưng điều đó sẽ không đảm bảo rằng chúng sẽ được phân bổ đồng đều theo thời gian - vì vậy bạn có thể có 20 giao dịch trong một ngày và 0 giao dịch trong những ngày còn lại trong tuần.

* Có thể do lỗi cấu hình. Tốt nhất là bạn nên kiểm tra nhật ký, chúng thường cho bạn biết liệu bot không nhận được tín hiệu mua (chỉ thông báo nhịp tim) hay có điều gì đó không ổn (lỗi / ngoại lệ trong nhật ký).

### Tôi đã thực hiện 12 giao dịch rồi, tại sao tổng lợi nhuận của tôi lại âm?Tôi hiểu sự thất vọng của bạn nhưng tiếc là 12 giao dịch chỉ là
không đủ để nói bất cứ điều gì. Nếu bạn chạy backtesting, bạn có thể thấy rằng
thuật toán hiện tại có lợi cho bạn, nhưng đó là sau
hàng nghìn giao dịch và thậm chí ở đó, bạn sẽ bị thua lỗ
những đồng tiền cụ thể mà bạn đã giao dịch hàng chục, thậm chí hàng trăm lần. Chúng tôi
tất nhiên là không ngừng hướng tới việc cải thiện bot nhưng nó sẽ _luôn luôn_ là một
cờ bạc, điều này sẽ mang lại cho bạn những chiến thắng khiêm tốn hàng tháng nhưng
bạn không thể nói nhiều từ một vài giao dịch.

### Tôi muốn thay đổi cấu hình. Tôi có thể làm điều đó mà không cần phải giết bot không?

Đúng. Bạn có thể chỉnh sửa cấu hình của mình và sử dụng lệnh `/reload_config` để tải lại cấu hình. Bot sẽ dừng lại, tải lại cấu hình và chiến lược và sẽ khởi động lại với cấu hình và chiến lược mới.

### Tại sao bot của tôi không bán mọi thứ nó đã mua?

Điều này được gọi là “bụi xu” và có thể xảy ra trên tất cả các sàn giao dịch.
Điều này xảy ra vì nhiều sàn giao dịch trừ phí từ "đơn vị tiền tệ nhận" - vì vậy bạn mua 100 COIN - nhưng bạn chỉ nhận được 99,9 COIN.
Vì COIN đang giao dịch với kích thước lô đầy đủ (bước 1COIN), bạn không thể bán 0,9 COIN (hoặc 99,9 COIN) - nhưng bạn cần làm tròn xuống 99 COIN.

Đây không phải là vấn đề về bot nhưng cũng sẽ xảy ra khi giao dịch thủ công.

Mặc dù freqtrade có thể xử lý việc này (nó sẽ bán 99 COIN), phí thường thấp hơn kích thước lô có thể giao dịch tối thiểu (bạn chỉ có thể giao dịch toàn bộ COIN chứ không phải 0,9 COIN).
Việc để lại bụi (0,9 COIN) trên sàn giao dịch thường có ý nghĩa, vì lần tiếp theo freqtrade mua COIN, nó sẽ ăn vào số dư nhỏ còn lại, lần này bán tất cả những gì nó đã mua và do đó số dư bụi sẽ giảm dần (mặc dù rất có thể nó sẽ không bao giờ đạt chính xác 0).

Nếu có thể (ví dụ: trên binance), việc sử dụng loại tiền tệ tính phí chuyên dụng của sàn giao dịch sẽ khắc phục được vấn đề này.
Trên binance, chỉ cần có BNB trong tài khoản của bạn và bật "Thanh toán phí bằng BNB" trong hồ sơ của bạn là đủ. Số dư BNB của bạn sẽ giảm dần (vì nó được dùng để trả phí) - nhưng bạn sẽ không còn gặp bụi nữa (Freqtrade sẽ bao gồm các khoản phí này khi tính toán lợi nhuận).
Các sàn giao dịch khác không cung cấp những khả năng như vậy, trong đó đơn giản là bạn sẽ phải chấp nhận hoặc chuyển sang một sàn giao dịch khác.

### Tôi đã gửi thêm tiền vào sàn giao dịch nhưng bot của tôi không nhận ra điều này

Freqtrade sẽ cập nhật số dư trao đổi khi cần thiết (Trước khi đặt hàng).
Lệnh gọi RPC (`/balance` của Telegram, lệnh gọi API tới `/balance`) có thể kích hoạt cập nhật ở mức tối đa. một lần mỗi giờ.

Nếu `điều chỉnh_trade_position` được bật (và bot có các giao dịch mở đủ điều kiện để điều chỉnh vị trí) - thì ví sẽ được làm mới mỗi giờ một lần.
Để buộc cập nhật ngay lập tức, bạn có thể sử dụng `/reload_config` - thao tác này sẽ khởi động lại bot.

### Tôi muốn sử dụng nến chưa hoàn thiện

Freqtrade sẽ không cung cấp nến không đầy đủ cho các chiến lược. Việc sử dụng nến không đầy đủ sẽ dẫn đến việc sơn lại và do đó dẫn đến các chiến lược mua "ma", điều này không thể vừa kiểm tra lại vừa xác minh sau khi chúng xảy ra.

Bạn có thể sử dụng dữ liệu thị trường "hiện tại" bằng cách sử dụng phương pháp sổ đặt hàng hoặc mã cổ phiếu của [dataprovider](strategy-customization.md#orderbookpair-maximum) - tuy nhiên, bạn không thể sử dụng phương pháp này trong quá trình kiểm tra ngược.

### Có cài đặt nào để chỉ Thoát các giao dịch đang được giữ và không thực hiện bất kỳ Mục nhập mới nào không?

Bạn có thể sử dụng lệnh `/stopentry` trong Telegram để ngăn chặn việc tham gia giao dịch trong tương lai, sau đó là `/forceexit all` (bán tất cả các giao dịch đang mở).

### Tôi đã bán vốn của bot và bây giờ có lỗi trong nhật kýFreqtrade giả định rằng các giao dịch mà nó mở chỉ được quản lý thông qua bot.  
Nếu bạn tình cờ (vô tình) bán vốn của bot, freqtrade sẽ cố gắng phục hồi bằng cách cố gắng tìm lại các lệnh trên sàn giao dịch.

Đây là cách tiếp cận nỗ lực tối đa và sẽ không hiệu quả trong mọi trường hợp, đặc biệt khi sử dụng các loại đơn đặt hàng không được freqtrade hỗ trợ (OCO, tảng băng trôi, v.v.) hoặc khi làm việc với các giao dịch cũ hơn (nơi sàn giao dịch không còn cung cấp đầy đủ thông tin đơn hàng).
Các giới hạn chính xác sẽ khác nhau giữa các sàn giao dịch - với các chi tiết thường được ghi lại trong tài liệu API của sàn giao dịch.

### Tôi muốn chạy nhiều bot trên cùng một máy

Vui lòng xem [Trang tài liệu thiết lập nâng cao](advanced-setup.md#running-multiple-instances-of-freqtrade).

### Tôi nhận được thông báo "Không thể tải Chiến lược" khi khởi động bot

Thông báo lỗi này được hiển thị khi bot không thể tải chiến lược.
Thông thường, bạn có thể sử dụng `freqtrade list-strategies` để liệt kê tất cả các chiến lược có sẵn. 
Đầu ra của lệnh này cũng sẽ bao gồm một cột trạng thái, cho biết liệu chiến lược có thể được tải hay không.

Vui lòng kiểm tra những điều sau:

* Bạn có đang sử dụng đúng tên chiến lược không? Tên chiến lược phân biệt chữ hoa chữ thường và phải tương ứng với tên lớp Chiến lược (không phải tên tệp!).
* Chiến lược có nằm trong thư mục `user_data/strategies` và có đuôi tệp `.py` không?
* Bot có hiển thị các cảnh báo khác trước lỗi này không? Có thể bạn đang thiếu một số phần phụ thuộc cho chiến lược - điều này sẽ được đánh dấu trong nhật ký.
* Trong trường hợp docker - thư mục chiến lược có được gắn chính xác không (kiểm tra phần ổ đĩa của tệp soạn thảo docker)?

### Tôi nhận được thông báo "Thiếu điền dữ liệu" trong nhật ký

Thông báo này chỉ là cảnh báo rằng những cây nến mới nhất đã thiếu nến trong đó.
Tùy thuộc vào sàn giao dịch, điều này có thể cho thấy cặp tiền này không có giao dịch trong khung thời gian bạn đang sử dụng - và sàn giao dịch chỉ trả lại nến có khối lượng.
Trên các cặp có khối lượng thấp, điều này xảy ra khá phổ biến.

Nếu điều này xảy ra với tất cả các cặp trong danh sách cặp, điều này có thể cho thấy thời gian ngừng hoạt động của sàn giao dịch gần đây. Vui lòng kiểm tra các kênh công khai của sàn giao dịch của bạn để biết chi tiết.

Bất kể lý do là gì, Freqtrade sẽ lấp đầy những cây nến này bằng những cây nến "trống", trong đó giá mở, cao, thấp và đóng được đặt bằng giá đóng của nến trước đó - và khối lượng trống. Trong biểu đồ, nó sẽ trông giống như một `_` - và được căn chỉnh theo cách các sàn giao dịch thường biểu thị nến có khối lượng bằng 0.

### Tôi nhận được thông báo "Đã phát hiện giá nhảy giữa 2 nến"

Thông báo này là cảnh báo rằng nến đã tăng giá > 30%.
Đây có thể là dấu hiệu cho thấy cặp tiền này đã ngừng giao dịch và một số trao đổi mã thông báo đã diễn ra (ví dụ: COCOS vào năm 2021 - nơi giá đã tăng từ 0,0000154 lên 0,01621).
Thông báo này thường đi kèm với ["Thiếu điền dữ liệu"](#im-getting-missing-data-fillup-messages-in-the-log) - vì giao dịch trên các cặp như vậy thường bị dừng trong một thời gian.

### Tôi muốn thiết lập lại cơ sở dữ liệu của bot

Để đặt lại cơ sở dữ liệu của bot, bạn có thể xóa cơ sở dữ liệu (theo mặc định là `tradesv3.sqlite` hoặc `tradesv3.dryrun.sqlite`) hoặc sử dụng url cơ sở dữ liệu khác thông qua `--db-url` (ví dụ: `sqlite:///mynewdatabase.sqlite`).

### Tôi nhận được thông báo "Lịch sử lỗi thời của cặp xxx" trong nhật ký

Bot đang cố gắng cho bạn biết rằng nó có cây nến cuối cùng đã lỗi thời (không phải cây nến hoàn chỉnh cuối cùng).
Do đó, Freqtrade sẽ không tham gia giao dịch cho cặp này - vì giao dịch dựa trên thông tin cũ thường không phải là điều mong muốn.

Cảnh báo này có thể chỉ ra một trong những vấn đề dưới đây:* Thời gian ngừng trao đổi -> Kiểm tra trang trạng thái trao đổi / blog / nguồn cấp dữ liệu twitter của bạn để biết chi tiết.
* Thời gian hệ thống sai -> Đảm bảo thời gian hệ thống của bạn là chính xác.
* Cặp gần như không được giao dịch -> Kiểm tra cặp trên trang web trao đổi, xem khung thời gian mà chiến lược của bạn sử dụng. Nếu cặp này không có bất kỳ khối lượng nào trong một số nến (thường được hiển thị bằng thanh "âm lượng 0" và "_" là nến), thì cặp này không có bất kỳ giao dịch nào trong khung thời gian này. Tốt nhất nên tránh những cặp này vì chúng có thể gây ra vấn đề khi thực hiện đơn hàng.
* Sự cố API -> API trả về dữ liệu sai (điều này chỉ xảy ra ở đây để cung cấp đầy đủ và không xảy ra với các sàn giao dịch được hỗ trợ).

### Tôi nhận được thông báo "Không thể sử dụng lại đồng hồ cho xxx" trong nhật ký

Đây là thông báo cho biết bot đã cố gắng sử dụng nến từ websocket nhưng sàn giao dịch không cung cấp thông tin chính xác.
Điều này có thể xảy ra nếu kết nối websocket bị gián đoạn - hoặc nếu cặp tiền này không có bất kỳ giao dịch nào xảy ra trong khung thời gian bạn đang sử dụng.

Freqtrade sẽ xử lý vấn đề này một cách khéo léo bằng cách quay lại API REST.
Mặc dù điều này làm cho quá trình lặp lại chậm hơn một chút (do lệnh gọi REST Api) - nhưng nó sẽ không gây ra bất kỳ vấn đề nào đối với hoạt động của bot.

### Tôi nhận được thông báo "Exchange XXX không hỗ trợ lệnh thị trường." tin nhắn và không thể chạy chiến lược của tôi

Như thông báo cho biết, sàn giao dịch của bạn không hỗ trợ lệnh thị trường và bạn có một trong các [loại lệnh](configuration.md/#hiểu-order_types) được đặt thành "thị trường". Chiến lược của bạn có thể được viết dành cho các sàn giao dịch khác và đặt lệnh "thị trường" cho lệnh "dừng lỗ", điều này đúng và thích hợp hơn đối với hầu hết các sàn giao dịch hỗ trợ lệnh thị trường (nhưng không phải cho Gate.io).

Để khắc phục điều này, hãy xác định lại loại lệnh trong chiến lược sử dụng "giới hạn" thay vì "thị trường":``` python
    order_types = {
        ...
        "stoploss": "limit",
        ...
    }
```Cách khắc phục tương tự sẽ được áp dụng trong tệp cấu hình, nếu loại đơn đặt hàng được xác định trong cấu hình tùy chỉnh của bạn chứ không phải trong chiến lược.

### Tôi đang cố gắng khởi động bot nhưng gặp lỗi về quyền API

Các lỗi như `Khóa API, IP hoặc quyền hành động không hợp lệ` có nghĩa chính xác như những gì chúng thực sự nói.  
Khóa API của bạn không hợp lệ (lỗi sao chép/dán? hãy kiểm tra khoảng trắng ở đầu/cuối trong cấu hình), đã hết hạn hoặc IP mà bạn đang chạy bot không được bật trong bảng điều khiển API của Exchange.  
Thông thường, sự cho phép "Giao dịch giao ngay" (hoặc quyền tương đương trong sàn giao dịch bạn sử dụng) sẽ cần thiết.  
Hợp đồng tương lai thường sẽ phải được kích hoạt cụ thể.

### Làm cách nào để tìm kiếm thứ gì đó trong nhật ký bot?

Theo mặc định, bot ghi nhật ký của nó vào luồng stderr. Điều này được triển khai theo cách này để bạn có thể dễ dàng tách các thông báo chẩn đoán của bot khỏi các kết quả Backtesting, Edge và Hyperopt, đầu ra khỏi các lệnh phụ tiện ích Freqtrade khác nhau, cũng như khỏi đầu ra của `print()` tùy chỉnh mà bạn có thể đã chèn vào chiến lược của mình. Vì vậy, nếu bạn cần tìm kiếm thông điệp tường trình bằng tiện ích grep, bạn cần chuyển hướng stderr sang thiết bị xuất chuẩn và bỏ qua thiết bị xuất chuẩn.

* Trong Unix shell, việc này thường có thể được thực hiện đơn giản như:```shell
$ freqtrade --some-options 2>&1 >/dev/null | grep 'something'
```(lưu ý, `2>&1` và `>/dev/null` nên được viết theo thứ tự này)

* Trình thông dịch Bash cũng hỗ trợ cái gọi là cú pháp thay thế quy trình, bạn có thể grep nhật ký cho một chuỗi có dạng như sau:```shell
$ freqtrade --some-options 2> >(grep 'something') >/dev/null
```hoặc```shell
$ freqtrade --some-options 2> >(grep -v 'something' 1>&2)
```* Bạn cũng có thể ghi bản sao thông điệp nhật ký Freqtrade vào một tệp bằng tùy chọn `--logfile`:```shell
$ freqtrade --logfile /path/to/mylogfile.log --some-options
```và sau đó grep nó như:```shell
$ cat /path/to/mylogfile.log | grep 'something'
```hoặc thậm chí nhanh chóng, khi bot hoạt động và tệp nhật ký phát triển:```shell
$ tail -f /path/to/mylogfile.log | grep 'something'
```từ một cửa sổ terminal riêng biệt.

Trên Windows, tùy chọn `--logfile` cũng được Freqtrade hỗ trợ và bạn có thể sử dụng lệnh `findstr` để tìm kiếm chuỗi quan tâm trong nhật ký:```
> type \path\to\mylogfile.log | findstr "something"
```## Mô-đun Hyperopt

###Tại sao freqtrade không hỗ trợ GPU?

Trước hết, hầu hết các thư viện chỉ báo đều không hỗ trợ GPU - do đó, việc tính toán chỉ báo sẽ có rất ít lợi ích.
Các cải tiến GPU sẽ chỉ áp dụng cho các phép tính gốc của gấu trúc - hoặc các phép tính do chính bạn viết.

GPU chỉ giỏi xử lý các con số (các phép toán dấu phẩy động).
Đối với hyperopt, chúng ta cần cả tính năng xử lý số (tìm tham số tiếp theo) và chạy mã python (chạy backtesting).
Do đó, GPU không quá phù hợp với hầu hết các phần của hyperopt.

Do đó, lợi ích của việc sử dụng GPU sẽ khá nhỏ - và sẽ không biện minh cho sự phức tạp được đưa ra khi cố gắng thêm hỗ trợ GPU.

Tuy nhiên, không có gì ngăn cản bạn sử dụng các chỉ báo hỗ trợ GPU trong chiến lược của mình nếu bạn nghĩ rằng bạn phải có điều này - tuy nhiên, bạn có thể sẽ thất vọng vì mức lợi nhuận nhỏ mang lại cho bạn (so với mức độ phức tạp).

### Tôi cần bao nhiêu epoch để có được kết quả Hyperopt tốt?

Theo mặc định Hyperopt được gọi mà không có tùy chọn dòng lệnh `-e`/`--epochs` sẽ chỉ
chạy 100 kỷ nguyên, nghĩa là 100 đánh giá về trình kích hoạt, bảo vệ của bạn, ... Quá ít
để tìm ra một kết quả tuyệt vời (trừ khi bạn rất may mắn), vì vậy bạn có thể
phải chạy nó với giá 10000 trở lên. Nhưng sẽ phải mất một thời gian vĩnh viễn để
tính toán.

Vì hyperopt sử dụng tìm kiếm Bayesian nên việc chạy quá nhiều kỷ nguyên có thể không mang lại kết quả tốt hơn.

Do đó, bạn nên chạy đi chạy lại trong khoảng 500-1000 kỷ nguyên cho đến khi đạt được tổng cộng ít nhất 10000 kỷ nguyên (hoặc hài lòng với kết quả). Bạn có thể đánh giá tốt nhất bằng cách xem kết quả - nếu bot tiếp tục khám phá các chiến lược tốt hơn thì tốt nhất bạn nên tiếp tục.```bash
freqtrade hyperopt --hyperopt-loss SharpeHyperOptLossDaily --strategy SampleStrategy -e 1000
```###Tại sao chạy hyperopt lâu?* Discovering a great strategy with Hyperopt takes time. Study www.freqtrade.io, the Freqtrade Documentation page, join the Freqtrade [discord community](https://discord.gg/p7nuUNVfP7). While you patiently wait for the most advanced, free crypto bot in the world, to hand you a possible golden strategy specially designed just for you.
* Nếu bạn thắc mắc tại sao có thể mất từ 20 phút đến vài ngày để thực hiện 1000 kỷ nguyên thì đây là một số câu trả lời:

Câu trả lời này được viết trong bản phát hành 0.15.1, khi chúng tôi có:

* 8 kích hoạt
* 9 bảo vệ: giả sử chúng ta đánh giá thậm chí 10 giá trị từ mỗi giá trị
* 1 phép tính điểm dừng: giả sử chúng ta cũng muốn đánh giá 10 giá trị từ đó

Cách tính sau đây vẫn còn rất thô và chưa chính xác lắm
nhưng nó sẽ đưa ra ý tưởng. Chỉ với những kích hoạt và bảo vệ này, có
đã có 8\*10^9\*10 đánh giá. Tổng cộng có khoảng 80 tỷ đánh giá.
Bạn đã thực hiện 100.000 đánh giá chưa? Xin chúc mừng, bạn đã thực hiện được khoảng 1/100 000
của không gian tìm kiếm, giả sử rằng bot không bao giờ kiểm tra cùng một tham số nhiều lần.

* Thời gian cần thiết để chạy 1000 kỷ nguyên hyperopt phụ thuộc vào những thứ như: CPU có sẵn, đĩa cứng, ram, khung thời gian, khoảng thời gian, cài đặt chỉ báo, số lượng chỉ báo, số lượng xu áp dụng chiến lược thử nghiệm hyperopt và số lượng giao dịch kết quả - có thể là 650 giao dịch trong một năm hoặc 100000 giao dịch tùy thuộc vào chiến lược nhắm đến lợi nhuận lớn bằng cách hiếm khi giao dịch hay cho nhiều giao dịch lợi nhuận thấp.

Ví dụ: Lợi nhuận 4% gấp 650 lần so với lợi nhuận 0,3% cho một giao dịch 10000 lần trong một năm. Nếu chúng tôi giả sử bạn đặt --timerange thành 365 ngày.

Ví dụ:
`freqtrade --config config.json --strategy SampleStrategy --hyperopt SampleHyperopt -e 1000 --timerange 20190601-20200601`

## Kênh chính thức

Freqtrade đang sử dụng độc quyền các kênh chính thức sau:* [Freqtrade discord server](https://discord.gg/p7nuUNVfP7)
* [Freqtrade documentation (https://freqtrade.io)](https://freqtrade.io)
* [Freqtrade github organization](https://github.com/freqtrade)
Không ai liên kết với dự án freqtrade sẽ hỏi bạn về khóa trao đổi của bạn hoặc bất kỳ điều gì khác khiến tiền của bạn có thể bị lợi dụng.
Nếu bạn được yêu cầu tiết lộ khóa trao đổi của mình hoặc gửi tiền đến một số ví ngẫu nhiên, vui lòng không làm theo các hướng dẫn này.

Việc không tuân theo các nguyên tắc này sẽ không phải là trách nhiệm của freqtrade.

## Chính sách hỗ trợWe provide free support for Freqtrade on our [Discord server](https://discord.gg/p7nuUNVfP7) and via GitHub issues.
Chúng tôi chỉ hỗ trợ bản phát hành gần đây nhất (ví dụ: 2025.8) và nhánh phát triển hiện tại (ví dụ: 2025.9-dev).

Nếu bạn đang sử dụng phiên bản cũ hơn, vui lòng làm theo [hướng dẫn nâng cấp](update.md) và xem sự cố của bạn đã được giải quyết chưa.

## "Mã thông báo Freqtrade"

Freqtrade không cung cấp mã thông báo tiền điện tử.

Các dịch vụ mã thông báo mà bạn tìm thấy trên internet đề cập đến Freqtrade, FreqAI hoặc freqUI phải được coi là lừa đảo, cố gắng khai thác sự phổ biến của freqtrade để thu lợi bất chính cho riêng họ.