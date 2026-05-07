<!-- Auto-translated from docs/ by script. Please review technical terms. -->

# Giao dịch với đòn bẩy

!!! Lưu ý "Nhiều bot trên một tài khoản"
    Bạn không thể chạy 2 bot trên cùng một tài khoản bằng đòn bẩy. Đối với giao dịch đòn bẩy / ký quỹ, freqtrade giả định rằng đó là người dùng duy nhất của tài khoản và tất cả các mức thanh lý được tính toán dựa trên giả định này.

!!! Nguy hiểm "Giao dịch bằng đòn bẩy rất rủi ro"
    Không giao dịch với đòn bẩy > 1 bằng chiến lược không cho kết quả tích cực trong đợt chạy trực tiếp bằng cách sử dụng thị trường giao ngay. Kiểm tra điểm dừng của chiến lược của bạn. Với đòn bẩy là 2, mức dừng lỗ 0,5 (50%) sẽ là quá thấp và các giao dịch này sẽ bị thanh lý trước khi đạt đến mức dừng lỗ đó.
    Chúng tôi không chịu bất kỳ trách nhiệm nào đối với những tổn thất cuối cùng xảy ra khi sử dụng phần mềm này hoặc chế độ này.

    Vui lòng chỉ sử dụng các chế độ giao dịch nâng cao khi bạn biết freqtrade (và chiến lược của bạn) hoạt động như thế nào.
    Ngoài ra, không bao giờ mạo hiểm nhiều hơn những gì bạn có thể đủ khả năng để mất.

Nếu bạn đã có chiến lược hiện tại, vui lòng đọc [hướng dẫn di chuyển chiến lược](strategy_migration.md#strategy-migration-between-v2-and-v3) để di chuyển chiến lược của bạn từ chiến lược freqtrade v2 sang chiến lược phiên bản 3 có thể bán khống và giao dịch hợp đồng tương lai.

## Rút ngắn

Không thể bán khống khi giao dịch với [`trading_mode`](#đòn bẩy-trading-modes) được đặt thành `spot`. Để giao dịch bán khống, `chế độ giao dịch` phải được đặt thành `lề`(hiện không khả dụng) hoặc [`futures`](#futures), với [`margin_mode`](#margin-mode) được đặt thành [`cross`](#cross-margin-mode) hoặc [`isolat`](#isolat-margin-mode)

Để rút ngắn chiến lược, lớp chiến lược phải đặt biến lớp `can_short = True`

Vui lòng đọc [tùy chỉnh chiến lược](strategy-customization.md#entry-signal-rules) để biết hướng dẫn về cách đặt tín hiệu để vào và thoát giao dịch bán.

## Hiểu `chế độ giao dịch`

Các giá trị có thể là: `spot` (mặc định), `margin`(*Hiện không có sẵn*) hoặc `tương lai`.

### tại chỗ

Chế độ giao dịch thông thường (rủi ro thấp)

- Chỉ giao dịch mua (Không giao dịch bán).
- Không có đòn bẩy.
- Không thanh lý.
- Lãi/lỗ được tính bằng sự thay đổi giá trị tài sản (trừ phí giao dịch).

### Tận dụng các chế độ giao dịch

Với đòn bẩy, nhà giao dịch vay vốn từ sàn giao dịch. Vốn phải được hoàn trả lại đầy đủ cho sàn giao dịch (có thể kèm theo lãi suất) và nhà giao dịch giữ mọi khoản lợi nhuận hoặc thanh toán mọi khoản lỗ từ bất kỳ giao dịch nào được thực hiện bằng cách sử dụng vốn vay.

Bởi vì vốn phải luôn được hoàn trả lại nên các sàn giao dịch sẽ **thanh lý** (buộc bán tài sản của nhà giao dịch) một giao dịch được thực hiện bằng vốn vay khi tổng giá trị tài sản trong tài khoản đòn bẩy giảm xuống một điểm nhất định (điểm mà tổng giá trị thua lỗ nhỏ hơn giá trị tài sản thế chấp mà nhà giao dịch thực sự sở hữu trong tài khoản đòn bẩy), để đảm bảo rằng nhà giao dịch có đủ vốn để trả lại tài sản đã vay cho sàn giao dịch. Sàn giao dịch cũng sẽ tính **phí thanh lý**, làm tăng thêm tổn thất cho nhà giao dịch.

Vì lý do này, **KHÔNG GIAO DỊCH VỚI Đòn bẩy NẾU BẠN KHÔNG BIẾT CHÍNH XÁC MÌNH BẠN LÀM GÌ. GIAO DỊCH Đòn bẩy LÀ RỦI RO CAO VÀ CÓ THỂ DẪN ĐẾN GIÁ TRỊ TÀI SẢN CỦA BẠN GIẢM VỀ 0 RẤT NHANH CHÓNG, KHÔNG CÓ CƠ HỘI TĂNG GIÁ TRỊ LẠI.**

#### Ký quỹ (hiện không có sẵn)

Giao dịch diễn ra trên thị trường giao ngay, nhưng sàn giao dịch sẽ cho bạn vay tiền với số tiền bằng với đòn bẩy đã chọn. Bạn trả lại số tiền đã cho bạn vay để trao đổi cùng với tiền lãi và lãi/lỗ của bạn được nhân với đòn bẩy được chỉ định.

#### Tương laiHoán đổi vĩnh viễn (còn được gọi là Hợp đồng tương lai vĩnh viễn) là các hợp đồng được giao dịch ở mức giá gắn chặt với tài sản cơ bản mà chúng dựa trên (ví dụ). Bạn không giao dịch tài sản thực tế mà thay vào đó đang giao dịch một hợp đồng phái sinh. Hợp đồng hoán đổi vĩnh viễn có thể kéo dài vô thời hạn, trái ngược với hợp đồng tương lai hoặc quyền chọn.

Ngoài các khoản lãi/lỗ từ sự thay đổi giá của hợp đồng tương lai, các nhà giao dịch còn trao đổi _phí cấp vốn_, là các khoản lãi/lỗ có giá trị bằng số tiền bắt nguồn từ chênh lệch giá giữa hợp đồng tương lai và tài sản cơ bản. Sự khác biệt về giá giữa hợp đồng tương lai và tài sản cơ bản khác nhau giữa các sàn giao dịch.

Để giao dịch trên thị trường tương lai, bạn sẽ phải đặt `chế độ giao dịch` thành "tương lai".
Bạn cũng sẽ phải chọn "chế độ lề" (giải thích bên dưới).``` json
"trading_mode": "futures",
"margin_mode": "isolated"
```##### Đặt tên theo cặpFreqtrade follows the [ccxt naming conventions for futures](https://docs.ccxt.com/#/README?id=perpetual-swap-perpetual-future).
Do đó, một cặp tương lai sẽ có tên là `base/quote:settle` (ví dụ: `ETH/USDT:USDT`).

### Chế độ lề

Ngoài `chế độ giao dịch` - bạn cũng sẽ phải định cấu hình `chế độ ký quỹ` của mình.
Mặc dù freqtrade hiện chỉ hỗ trợ một chế độ ký quỹ, nhưng chế độ này sẽ thay đổi và bằng cách định cấu hình chế độ này ngay bây giờ, bạn đã sẵn sàng cho các bản cập nhật trong tương lai.

Các giá trị có thể là: `cô lập` hoặc `chéo`.

####Chế độ lề biệt lập

Mỗi thị trường (cặp giao dịch), giữ tài sản thế chấp trong một tài khoản riêng``` json
"margin_mode": "isolated"
```#### Chế độ lề chéo

Một tài khoản được sử dụng để chia sẻ tài sản thế chấp giữa các thị trường (cặp giao dịch). Tiền ký quỹ được lấy từ tổng số dư tài khoản để tránh bị thanh lý khi cần thiết.``` json
"margin_mode": "cross"
```Vui lòng đọc [ghi chú cụ thể về trao đổi](exchanges.md) để biết các trao đổi hỗ trợ chế độ này và chúng khác nhau như thế nào.

!!! Cảnh báo “Rủi ro thanh lý gia tăng”
    Chế độ ký quỹ chéo làm tăng nguy cơ thanh lý toàn bộ tài khoản vì tất cả các giao dịch đều có chung tài sản thế chấp.
    Việc thua lỗ trên một giao dịch có thể ảnh hưởng đến giá thanh lý của các giao dịch khác.  
    Ngoài ra, ảnh hưởng của các vị trí chéo có thể không được mô phỏng đầy đủ ở chế độ chạy thử hoặc thử nghiệm ngược.

## Đặt đòn bẩy để sử dụng

Các chiến lược và hồ sơ rủi ro khác nhau sẽ yêu cầu mức đòn bẩy khác nhau.
Mặc dù bạn có thể định cấu hình một giá trị đòn bẩy tĩnh - freqtrade cung cấp cho bạn sự linh hoạt để điều chỉnh giá trị này thông qua [gọi lại đòn bẩy chiến lược](strategy-callbacks.md#leverage-callback) - cho phép bạn sử dụng các đòn bẩy khác nhau theo cặp hoặc dựa trên một số yếu tố khác mang lại lợi ích cho kết quả chiến lược của bạn.

Nếu không được triển khai, đòn bẩy mặc định là 1x (không có đòn bẩy).

!!! Cảnh báo
    Đòn bẩy cao hơn cũng đồng nghĩa với rủi ro cao hơn - hãy chắc chắn rằng bạn hiểu đầy đủ ý nghĩa của việc sử dụng đòn bẩy!

## Hiểu `liquidation_buffer`

*Mặc định là `0,05`*

Một tỷ lệ xác định mức độ an toàn của mạng lưới an toàn được đặt giữa giá thanh lý và mức dừng lỗ để ngăn vị thế đạt đến giá thanh lý.
Giá thanh lý nhân tạo này được tính như sau:

`tần suất giao dịch_thanh lý_giá = giá_thanh lý ± (abs(tỷ lệ mở - giá_thanh lý) * thanh lý_buffer)`

- `±` = `+` đối với các giao dịch mua
- `±` = `-` đối với các giao dịch bán

Các giá trị có thể có là bất kỳ số float nào trong khoảng từ 0,0 đến 0,99

**ví dụ:** Nếu một giao dịch được thực hiện ở mức giá 10 xu/USDT và giá thanh lý của giao dịch này là 8 xu/USDT, thì với `liquidation_buffer` được đặt thành `0,05`, mức dừng lỗ tối thiểu cho giao dịch này sẽ là $8 + ((10 - 8) * 0,05) = 8 + 0,1 = 8,1$

!!! Nguy hiểm "`Bộ đệm_thanh lý` là 0,0 hoặc `bộ đệm_thanh lý` thấp có thể dẫn đến việc thanh lý và phí thanh lý"
    Hiện tại Freqtrade có thể tính giá thanh lý nhưng không tính phí thanh lý. Việc đặt `thanh_buffer` của bạn thành 0,0 hoặc sử dụng `thanh_buffer` thấp có thể dẫn đến việc vị thế của bạn bị thanh lý. Freqtrade không theo dõi phí thanh lý, do đó việc thanh lý sẽ dẫn đến kết quả lãi/lỗ không chính xác cho bot của bạn. Nếu bạn sử dụng `thanh_buffer` thấp, bạn nên sử dụng `stoploss_on_exchange` nếu sàn giao dịch của bạn hỗ trợ điều này.

## Tỷ lệ tài trợ không có sẵn

Đối với dữ liệu tương lai, các sàn giao dịch thường cung cấp nến tương lai, nhãn hiệu và tỷ lệ cấp vốn. Tuy nhiên, điều phổ biến là mặc dù nến và nhãn hiệu có thể có sẵn nhưng tỷ lệ cấp vốn thì không. Điều này có thể ảnh hưởng đến các khoảng thời gian kiểm tra lại, tức là bạn chỉ có thể kiểm tra các khoảng thời gian gần đây chứ không thể kiểm tra sớm hơn, gặp phải thông báo `Không tìm thấy dữ liệu. Chấm dứt.` lỗi. Để giải quyết vấn đề này, hãy thêm tùy chọn cấu hình `futures_funding_rate` như được liệt kê trong [configuration.md](configuration.md) và bạn nên đặt tùy chọn này thành `0`, trừ khi bạn biết tỷ lệ cấp vốn cụ thể nhất định cho cặp, sàn giao dịch và khoảng thời gian của mình. Đặt giá trị này thành bất kỳ giá trị nào khác ngoài `0` có thể có tác động mạnh mẽ đến việc tính toán lợi nhuận của bạn trong chiến lược, ví dụ: trong các hàm `custom_exit`, `custom_stoploss`, v.v.

!!! Cảnh báo "Điều này có nghĩa là kết quả kiểm tra ngược của bạn không chính xác."
    Điều này sẽ không ghi đè tỷ lệ cấp vốn có sẵn từ sàn giao dịch, nhưng hãy nhớ rằng việc đặt tỷ lệ cấp vốn sai sẽ có nghĩa là kết quả kiểm tra lại sẽ không chính xác trong các khoảng thời gian lịch sử nơi không có tỷ lệ cấp vốn.### Nhà phát triển

####Chế độ lề

Đối với lệnh bán, loại tiền trả lãi suất cho loại tiền "vay" được mua vào cùng thời điểm đóng giao dịch (Điều này có nghĩa là số tiền mua trong các giao dịch đóng lệnh bán lớn hơn số tiền bán trong các giao dịch mở lệnh bán).

Trong thời gian dài, loại tiền trả lãi suất cho khoản "được vay" sẽ thuộc sở hữu của người dùng và không cần phải mua. Tiền lãi được trừ vào `giá trị đóng` của giao dịch.

Tất cả các khoản Phí đều được bao gồm trong phép tính `current_profit` trong quá trình giao dịch.

#### Chế độ tương lai

Phí tài trợ được cộng hoặc trừ vào tổng số tiền giao dịch