<!-- Auto-translated from docs/ by script. Please review technical terms. -->

# Dừng lỗ

Tham số cấu hình `stoploss` là tỷ lệ lỗ sẽ kích hoạt việc bán hàng.
Ví dụ: giá trị `-0,10` sẽ khiến bạn phải bán ngay lập tức nếu lợi nhuận giảm xuống dưới -10% cho một giao dịch nhất định. Tham số này là tùy chọn.
Tính toán mức dừng lỗ bao gồm phí, do đó mức dừng lỗ -10% được đặt chính xác dưới 10% so với điểm vào lệnh.

Hầu hết các tệp chiến lược đã bao gồm giá trị `stoploss` tối ưu.

!!! Thông tin
    Tất cả các thuộc tính dừng lỗ được đề cập trong tệp này có thể được đặt trong Chiến lược hoặc trong cấu hình.  
    <ins>Giá trị cấu hình sẽ ghi đè giá trị chiến lược.</ins>

## Dừng lỗ trên Exchange/Freqtrade

Các chế độ dừng lỗ đó có thể là *trên sàn giao dịch* hoặc *ngoài sàn giao dịch*.

Các chế độ này có thể được cấu hình với các giá trị sau:``` python
    'emergency_exit': 'market',
    'stoploss_on_exchange': False
    'stoploss_on_exchange_interval': 60,
    'stoploss_on_exchange_limit_ratio': 0.99
```Dừng lỗ khi trao đổi chỉ được hỗ trợ cho các sàn giao dịch sau và không phải tất cả các sàn giao dịch đều hỗ trợ cả lệnh dừng giới hạn và lệnh dừng thị trường.
Loại đơn đặt hàng sẽ bị bỏ qua nếu chỉ có một chế độ.

??? thông tin "Các loại trao đổi và dừng lỗ được hỗ trợ"
    
    --8<-- "bao gồm/exchange-features.md"

!!! Lưu ý “chặt cắt lỗ”
    Không đặt giá trị dừng lỗ quá thấp/chặt chẽ khi sử dụng lệnh dừng lỗ trên sàn giao dịch!  
    Nếu được đặt ở mức thấp/chặt chẽ, bạn sẽ có nguy cơ bỏ sót lệnh cao hơn và lệnh dừng lỗ sẽ không hoạt động.

!!! Cảnh báo "Dừng lỗ lỏng lẻo"
    Sử dụng mức dừng lỗ khi trao đổi với mức dừng lỗ rất rộng (ví dụ -1) có thể không đặt được lệnh dừng lỗ trên sàn giao dịch do hạn chế trao đổi.
    Trong trường hợp đó, bot sẽ chuyển sang sử dụng loại lệnh `exit_khẩn cấp` để đặt lệnh thị trường vì việc đặt lệnh dừng lỗ không thành công.
    Freqtrade hiện không thực hiện giới hạn để tránh tình trạng này, vì vậy vui lòng đảm bảo giá trị dừng lỗ của bạn nằm trong giới hạn hợp lý cho giao dịch của bạn hoặc vô hiệu hóa lệnh dừng lỗ khi trao đổi.

### Loại lệnh nào được sử dụng để dừng lỗ trên sàn giao dịch?

Loại lệnh dùng để dừng lỗ trên sàn giao dịch được xác định bởi giá trị `stoploss` và khả năng trao đổi.
Nếu sàn giao dịch đã chọn của bạn hỗ trợ cả lệnh dừng thị trường và lệnh dừng thị trường thì giá trị `stoploss` sẽ xác định loại lệnh nào được sử dụng cho lệnh dừng lỗ trên sàn giao dịch.
Nếu sàn giao dịch của bạn chỉ hỗ trợ một trong hai loại lệnh, bạn phải định cấu hình giá trị `stoploss` của mình cho phù hợp, nếu không bot sẽ không khởi động được.

### Tôi nên sử dụng loại lệnh nào để dừng lỗ trên sàn giao dịch?

Nếu chúng ta dịch hai loại lệnh dừng lỗ sang từ ngữ của con người - chúng sẽ giống như thế này:

* **stoploss-market** -> "khi lệnh dừng kích hoạt, hãy đưa tôi ra khỏi đây bằng bất cứ giá nào".
* **stoploss-limit** -> "khi kích hoạt lệnh dừng, hãy đặt lệnh giới hạn x% dưới giá dừng lỗ. Tôi chấp nhận mức lỗ "cắt lỗ + 1%" ở mức tệ nhất - nhưng nếu giá tăng cao hơn - tôi chấp nhận đợi giá quay trở lại với mình, có khả năng dẫn đến khoản lỗ lớn hơn nhiều so với "cắt lỗ + 1%".

Do đó, chúng tôi khuyên bạn nên sử dụng lệnh thị trường dừng lỗ bất cứ khi nào có thể, vì mục đích chính của lệnh dừng lỗ là giúp bạn thoát khỏi vị thế khi thị trường sụp đổ và trong những tình huống như vậy, bạn sẽ muốn thoát khỏi vị thế ngay lập tức ở mức giá tốt nhất hiện có, thay vì mạo hiểm lệnh giới hạn không được thực hiện và có khả năng gây ra tổn thất lớn hơn.
Lựa chọn cuối cùng là tùy thuộc vào bạn, nhưng vui lòng lưu ý đến rủi ro khi sử dụng lệnh giới hạn mức dừng lỗ, đặc biệt là trong các thị trường đầy biến động.

### stoploss_on_exchange và stoploss_on_exchange_limit_ratio

Bật hoặc Tắt tính năng dừng lỗ khi trao đổi.
Nếu mức dừng lỗ là *trên sàn giao dịch* thì có nghĩa là lệnh giới hạn mức dừng lỗ được đặt trên sàn giao dịch ngay sau khi lệnh mua được thực hiện. Điều này sẽ bảo vệ bạn trước những sự cố bất ngờ trên thị trường vì việc thực hiện lệnh diễn ra hoàn toàn trong sàn giao dịch và không có chi phí mạng tiềm năng.

Nếu `stoploss_on_exchange` sử dụng lệnh giới hạn thì sàn giao dịch cần có 2 mức giá, giá stoploss và giá Limit.  
`stoploss` xác định giá dừng nơi đặt lệnh giới hạn - và giới hạn phải thấp hơn giá này một chút.  
Nếu sàn giao dịch hỗ trợ cả lệnh dừng lỗ giới hạn và lệnh dừng lỗ thị trường thì giá trị của `stoploss` sẽ được sử dụng để xác định loại lệnh dừng lỗ.  

Ví dụ tính toán: chúng tôi đã mua tài sản ở mức 100\$.  
Giá dừng là 95\$, khi đó giới hạn sẽ là `95 * 0,99 = 94,05$` - vì vậy việc thực hiện lệnh giới hạn có thể xảy ra trong khoảng từ 95$ đến 94,05$.Ví dụ: giả sử lệnh dừng lỗ đang được trao đổi và lệnh dừng lỗ kéo dài được bật và thị trường đang đi lên thì bot sẽ tự động hủy lệnh dừng lỗ trước đó và đặt lệnh dừng lỗ mới có giá trị dừng cao hơn lệnh dừng lỗ trước đó.

!!! Lưu ý
    Nếu `stoploss_on_exchange` được bật và lệnh dừng lỗ được hủy thủ công trên sàn giao dịch thì bot sẽ tạo một lệnh dừng lỗ mới.

### dừng lỗ_on_exchange_interval

Trong trường hợp dừng lỗ khi trao đổi, có một tham số khác gọi là `stoploss_on_exchange_interval`. Điều này sẽ định cấu hình khoảng thời gian tính bằng giây mà bot sẽ kiểm tra mức dừng lỗ và cập nhật nó nếu cần.  
Bot không thể thực hiện những điều này cứ sau 5 giây (ở mỗi lần lặp), nếu không nó sẽ bị sàn giao dịch cấm.
Vì vậy, tham số này sẽ cho bot biết tần suất cập nhật lệnh dừng lỗ. Giá trị mặc định là 60 (1 phút).
Logic tương tự này sẽ áp dụng lại lệnh dừng lỗ trên sàn giao dịch nếu bạn vô tình hủy nó.

### loại dừng lỗ_price_type

!!! Cảnh báo "Chỉ áp dụng cho hợp đồng tương lai"
    `stoploss_price_type` chỉ áp dụng cho thị trường tương lai (trên các sàn giao dịch nếu có).  
    Freqtrade sẽ thực hiện xác thực cài đặt này khi khởi động, không khởi động được nếu cài đặt không hợp lệ cho sàn giao dịch của bạn đã được chọn.
    Các loại giá được hỗ trợ sẽ khác nhau giữa mỗi sàn giao dịch. Vui lòng kiểm tra với sàn giao dịch của bạn xem sàn hỗ trợ loại giá nào.  
    Ở thị trường giao ngay, cài đặt này bị bỏ qua và không được xác thực vì hầu hết các sàn giao dịch chỉ hỗ trợ một loại giá cho lệnh dừng lỗ trên thị trường giao ngay.

Lệnh dừng lỗ trên sàn giao dịch trên thị trường tương lai có thể kích hoạt ở các loại giá khác nhau.
Việc đặt tên cho các mức giá này trong thuật ngữ trao đổi thường khác nhau, nhưng thường là cái gì đó xoay quanh "cuối cùng" (hoặc "giá hợp đồng"), "mã hiệu" và "chỉ số".

Các giá trị được chấp nhận cho cài đặt này là `"last"`, `"mark"` và `"index"` - freqtrade sẽ tự động chuyển sang loại API tương ứng và đặt lệnh [stoploss on Exchange](#stoploss_on_exchange-and-stoploss_on_exchange_limit_ratio) tương ứng.

### buộc_thoát

`force_exit` là một giá trị tùy chọn, mặc định có cùng giá trị với `exit` và được sử dụng khi gửi lệnh `/forceexit` từ Telegram hoặc từ Rest API.

### buộc_entry

`force_entry` là một giá trị tùy chọn, mặc định có cùng giá trị với `entry` và được sử dụng khi gửi lệnh `/forceentry` từ Telegram hoặc từ Rest API.

###lối thoát khẩn cấp

`emergency_exit` là một giá trị tùy chọn, mặc định là `thị trường` và được sử dụng khi việc tạo điểm dừng lỗ trên các lệnh trao đổi không thành công.
Dưới đây là giá trị mặc định được sử dụng nếu không thay đổi trong tệp chiến lược hoặc cấu hình.

Ví dụ từ tệp chiến lược:``` python
order_types = {
    "entry": "limit",
    "exit": "limit",
    "emergency_exit": "market",
    "stoploss": "market",
    "stoploss_on_exchange": True,
    "stoploss_on_exchange_interval": 60,
    "stoploss_on_exchange_limit_ratio": 0.99
}
```## Loại dừng lỗ

Ở giai đoạn này, bot chứa các chế độ hỗ trợ dừng lỗ sau:

1. Dừng lỗ tĩnh.
2. Dừng lỗ kéo dài.
3. Trailing stop loss, tùy chỉnh lỗ dương.
4. Chỉ dừng lỗ khi giao dịch đã đạt đến một mức bù đắp nhất định.
5. [Chức năng dừng lỗ tùy chỉnh](strategy-callbacks.md#custom-stoploss)

### Dừng lỗ tĩnh

Điều này rất đơn giản, bạn xác định mức dừng lỗ của x (dưới dạng tỷ lệ của giá, tức là x * 100% giá). Điều này sẽ cố gắng bán tài sản khi khoản lỗ vượt quá khoản lỗ được xác định.

Ví dụ về lệnh dừng lỗ:``` python
    stoploss = -0.10
```Ví dụ: phép toán đơn giản:

* bot mua một tài sản ở mức giá 100$
* mức dừng lỗ được xác định ở mức -10%
* lệnh dừng lỗ sẽ được kích hoạt khi tài sản giảm xuống dưới 90$

### Lệnh dừng lỗ kéo dài

Giá trị ban đầu cho giá trị này là `stoploss`, giống như bạn xác định mức Dừng lỗ tĩnh của mình.
Để kích hoạt lệnh cắt lỗ theo sau:``` python
    stoploss = -0.10
    trailing_stop = True
```Điều này bây giờ sẽ kích hoạt một thuật toán, thuật toán này sẽ tự động tăng mức dừng lỗ mỗi khi giá tài sản của bạn tăng lên.

Ví dụ: phép toán đơn giản:

* bot mua một tài sản ở mức giá 100$
* mức dừng lỗ được xác định ở mức -10%
* lệnh dừng lỗ sẽ được kích hoạt khi tài sản giảm xuống dưới 90$
* giả sử tài sản hiện tăng lên 102$
* mức dừng lỗ bây giờ sẽ là -10% của 102$ = 91,8$
* bây giờ tài sản giảm giá trị xuống 101\$, mức dừng lỗ sẽ vẫn là 91,8$ và sẽ kích hoạt ở mức 91,8$.

Tóm lại: Điểm dừng lỗ sẽ được điều chỉnh luôn ở mức -10% so với mức giá cao nhất được quan sát.

### Trailing stop loss, mức giảm dương khác nhau

Bạn cũng có thể có mức dừng lỗ mặc định khi giao dịch mua của bạn đang ở mức đỏ (phí mua), nhưng khi bạn đạt được kết quả dương (hoặc mức bù mà bạn xác định), hệ thống sẽ sử dụng mức dừng lỗ mới, với một giá trị khác.
Ví dụ: mức dừng lỗ mặc định của bạn là -10%, nhưng khi bạn đã đạt được lợi nhuận (ví dụ 0,1%), một mức dừng lỗ khác sẽ được sử dụng.

!!! Lưu ý
    Nếu bạn muốn mức dừng lỗ chỉ được thay đổi khi bạn hòa vốn để kiếm được lợi nhuận (điều mà hầu hết người dùng muốn), vui lòng tham khảo phần tiếp theo với [bật offset](#trailing-stop-loss-only-once-the-trade-has-reached-a-certain-offset).

Cả hai giá trị đều yêu cầu đặt `trailing_stop` thành true và `trailing_stop_posit` bằng một giá trị.``` python
    stoploss = -0.10
    trailing_stop = True
    trailing_stop_positive = 0.02
    trailing_stop_positive_offset = 0.0
    trailing_only_offset_is_reached = False  # Default - not necessary for this example
```Ví dụ: phép toán đơn giản:

* bot mua một tài sản ở mức giá 100$
* mức dừng lỗ được xác định ở mức -10%
* lệnh dừng lỗ sẽ được kích hoạt khi tài sản giảm xuống dưới 90$
* giả sử tài sản hiện tăng lên 102$
* mức dừng lỗ bây giờ sẽ là -2% của 102$ = 99,96$ (mức dừng lỗ 99,96$ sẽ bị khóa và sẽ theo mức tăng giá tài sản với -2%)
* bây giờ tài sản giảm giá trị xuống 101\$, mức dừng lỗ sẽ vẫn là 99,96$ và sẽ kích hoạt ở mức 99,96$

0,02 sẽ chuyển thành mức dừng lỗ -2%.
Trước đó, `stoploss` được sử dụng cho lệnh dừng lỗ sau.

!!! Mẹo "Sử dụng phần bù để thay đổi điểm dừng của bạn"
    Sử dụng `trailing_stop_ Positive_offset` để đảm bảo rằng điểm dừng lỗ mới của bạn sẽ có lãi bằng cách đặt `trailing_stop_ Positive_offset` cao hơn `trailing_stop_posit`. Giá trị dừng lỗ mới đầu tiên của bạn sau đó sẽ có lợi nhuận bị khóa.

    Ví dụ với phép toán đơn giản:``` python
        stoploss = -0.10
        trailing_stop = True
        trailing_stop_positive = 0.02
        trailing_stop_positive_offset = 0.03
    ```* bot mua một tài sản ở mức giá 100$
    * mức dừng lỗ được xác định ở mức -10%, do đó, mức dừng lỗ sẽ được kích hoạt khi tài sản giảm xuống dưới 90$
    * giả sử tài sản hiện tăng lên 102$
    * mức dừng lỗ bây giờ sẽ ở mức 91,8$ - thấp hơn 10% so với tỷ lệ cao nhất được quan sát
    * giả sử tài sản hiện tăng lên 103,5$ (trên mức bù được định cấu hình)
    * mức dừng lỗ bây giờ sẽ là -2% của 103,5$ = 101,43$
    * bây giờ tài sản giảm giá trị xuống 102\$, mức dừng lỗ sẽ vẫn là 101,43$ và sẽ kích hoạt khi giá phá vỡ dưới 101,43$

### Trailing stop loss chỉ khi giao dịch đã đạt đến một mức bù đắp nhất định

Bạn cũng có thể giữ mức dừng lỗ tĩnh cho đến khi đạt được mức bù và sau đó theo dõi giao dịch để chốt lời khi thị trường quay đầu.

Nếu `trailing_only_offset_is_reached = True` thì điểm dừng lỗ cuối chỉ được kích hoạt khi đạt đến mức bù. Cho đến lúc đó, mức dừng lỗ vẫn ở mức `stoploss` đã được định cấu hình và không kéo dài.
Việc để giá trị này là `trailing_only_offset_is_reached=False` sẽ cho phép điểm dừng lỗ theo sau bắt đầu theo sau ngay khi giá tài sản tăng cao hơn giá nhập ban đầu.

Tùy chọn này có thể được sử dụng có hoặc không có `trailing_stop_posit`, nhưng sử dụng `trailing_stop_ Positive_offset` làm phần bù.

Cấu hình (bù đắp bằng giá mua + 3%):``` python
    stoploss = -0.10
    trailing_stop = True
    trailing_stop_positive = 0.02
    trailing_stop_positive_offset = 0.03
    trailing_only_offset_is_reached = True
```Ví dụ: phép toán đơn giản:

* bot mua một tài sản ở mức giá 100$
* mức dừng lỗ được xác định ở mức -10%
* lệnh dừng lỗ sẽ được kích hoạt khi tài sản giảm xuống dưới 90$
* điểm dừng lỗ sẽ vẫn ở mức 90$ trừ khi tài sản tăng lên hoặc cao hơn mức bù đắp được định cấu hình
* giả sử tài sản hiện tăng lên 103$ (trong đó chúng tôi đã định cấu hình phần bù)
* mức dừng lỗ bây giờ sẽ là -2% của 103$ = 100,94$
* bây giờ tài sản giảm giá trị xuống 101\$, mức dừng lỗ sẽ vẫn là 100,94$ và sẽ kích hoạt ở mức 100,94$

!!! Mẹo
    Đảm bảo có giá trị này (`trailing_stop_ Positive_offset`) thấp hơn ROI tối thiểu, nếu không ROI tối thiểu sẽ được áp dụng trước và bán giao dịch.

## Dừng lỗ và Đòn bẩy

Dừng lỗ nên được coi là "rủi ro đối với giao dịch này" - do đó, mức dừng lỗ 10% đối với giao dịch 100 đô la có nghĩa là bạn sẵn sàng mất 10 đô la (10%) cho giao dịch này - điều này sẽ xảy ra nếu giá giảm 10%.

Khi sử dụng đòn bẩy, nguyên tắc tương tự cũng được áp dụng - với lệnh dừng lỗ xác định rủi ro trong giao dịch (số tiền bạn sẵn sàng thua).

Do đó, mức dừng lỗ 10% đối với giao dịch 10 lần sẽ kích hoạt mức giá di chuyển 1%.
Nếu số tiền đặt cược của bạn (vốn tự có) là 100$ - giao dịch này sẽ là 1000$ ở mức gấp 10 lần (sau đòn bẩy).
Nếu giá di chuyển 1% - bạn đã mất 10$ vốn của chính mình - do đó lệnh dừng lỗ sẽ được kích hoạt trong trường hợp này.

Đảm bảo nhận thức được điều này và tránh sử dụng mức dừng lỗ quá chặt (với đòn bẩy 10 lần, rủi ro 10% có thể là quá ít để cho phép giao dịch "thở" một chút).

## Thay đổi điểm dừng lỗ trên các giao dịch đang mở

Có thể thay đổi mức dừng lỗ trên một giao dịch đang mở bằng cách thay đổi giá trị trong cấu hình hoặc chiến lược và sử dụng lệnh `/reload_config` (cách khác, dừng hoàn toàn và khởi động lại bot cũng có tác dụng).

Giá trị dừng lỗ mới sẽ được áp dụng cho các giao dịch đang mở (và các thông báo nhật ký tương ứng sẽ được tạo).

### Hạn chế

Không thể thay đổi giá trị điểm dừng nếu `trailing_stop` được bật và điểm dừng đã được điều chỉnh.