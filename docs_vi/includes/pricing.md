<!-- Auto-translated from docs/ by script. Please review technical terms. -->

## Giá sử dụng cho đơn hàng

Giá cho các lệnh thông thường có thể được kiểm soát thông qua cấu trúc tham số `entry_pricing` cho các mục nhập giao dịch và `exit_pricing` cho các lệnh thoát giao dịch.
Giá luôn được truy xuất ngay trước khi đặt hàng, bằng cách truy vấn các mã giao dịch hoặc bằng cách sử dụng dữ liệu sổ đặt hàng.

!!! Ghi chú    Orderbook data used by Freqtrade are the data retrieved from exchange by the ccxt's function `fetch_order_book()`, i.e. are usually data from the L2-aggregated orderbook, while the ticker data are the structures returned by the ccxt's `fetch_ticker()`/`fetch_tickers()` functions. Refer to the ccxt library [documentation](https://github.com/ccxt/ccxt/wiki/Manual#market-data) for more details.
!!! Cảnh báo “Sử dụng lệnh thị trường”
    Vui lòng đọc phần [Định giá lệnh thị trường](#giá lệnh thị trường) khi sử dụng lệnh thị trường.

### Giá vào cửa

####Nhập mặt giá

Cài đặt cấu hình `entry_pricing.price_side` xác định phần của sổ đặt hàng mà bot tìm kiếm khi mua.

Sau đây hiển thị một sổ đặt hàng.``` explanation
...
103
102
101  # ask
-------------Current spread
99   # bid
98
97
...
```Nếu `entry_pricing.price_side` được đặt thành `"giá thầu"` thì bot sẽ sử dụng 99 làm giá vào.  
Cùng với đó, nếu `entry_pricing.price_side` được đặt thành `"ask"` thì bot sẽ sử dụng 101 làm giá vào.

Tùy thuộc vào hướng đặt hàng (_long_/_short_), điều này sẽ dẫn đến các kết quả khác nhau. Vì vậy, chúng tôi khuyên bạn nên sử dụng `"same"` hoặc `"other"` cho cấu hình này.
Điều này sẽ dẫn đến ma trận định giá sau:

| hướng | Đặt hàng | thiết lập | giá | thánh giá lây lan |
|------ |--------|-----|------|------|
| dài | mua | hỏi | 101 | vâng |
| dài | mua | giá thầu | 99 | không |
| dài | mua | giống nhau | 99 | không |
| dài | mua | khác | 101 | vâng |
| ngắn | bán | hỏi | 101 | không |
| ngắn | bán | giá thầu | 99 | vâng |
| ngắn | bán | giống nhau | 101 | không |
| ngắn | bán | khác | 99 | vâng |

Việc sử dụng mặt kia của sổ đặt hàng thường đảm bảo các đơn hàng được thực hiện nhanh hơn, nhưng bot cũng có thể phải trả nhiều hơn mức cần thiết.
Phí Taker thay vì phí Maker rất có thể sẽ được áp dụng ngay cả khi sử dụng lệnh mua giới hạn.
Ngoài ra, giá ở phía "bên kia" của chênh lệch giá sẽ cao hơn giá ở phía "giá thầu" trong sổ lệnh, do đó lệnh hoạt động tương tự như lệnh thị trường (tuy nhiên với mức giá tối đa).

#### Giá vào lệnh khi kích hoạt Sổ đặt hàng

Khi tham gia giao dịch với sổ đặt hàng được bật (`entry_pricing.use_order_book=True`), Freqtrade tìm nạp các mục nhập `entry_pricing.order_book_top` từ sổ đặt hàng và sử dụng mục nhập được chỉ định là `entry_pricing.order_book_top` ở phía được định cấu hình (`entry_pricing.price_side`) của sổ đặt hàng. 1 chỉ định mục nhập trên cùng trong sổ đặt hàng, trong khi 2 sẽ sử dụng mục nhập thứ 2 trong sổ đặt hàng, v.v.

#### Giá vào lệnh khi chưa kích hoạt Sổ đặt hàng

Phần sau đây sử dụng `side` làm `entry_pricing.price_side` được định cấu hình (mặc định là `"same"`).

Khi không sử dụng sổ đặt hàng (`entry_pricing.use_order_book=False`), Freqtrade sử dụng giá `phụ` tốt nhất từ ​​mã cổ phiếu nếu nó thấp hơn giá giao dịch `cuối cùng` từ mã cổ phiếu. Ngược lại (khi giá `phụ` cao hơn giá `cuối cùng`), nó sẽ tính tỷ giá giữa giá `phụ` và giá `cuối cùng` dựa trên `entry_pricing.price_last_balance`.

Thông số cấu hình `entry_pricing.price_last_balance` kiểm soát điều này. Giá trị `0,0` sẽ sử dụng giá `phụ`, trong khi `1.0` sẽ sử dụng giá `cuối cùng` và các giá trị giữa các giá trị nội suy giữa giá chào bán và giá cuối cùng.

#### Kiểm tra độ sâu của thị trường

Khi bật kiểm tra độ sâu thị trường (`entry_pricing.check_deep_of_market.enabled=True`), các tín hiệu vào lệnh được lọc dựa trên độ sâu sổ đặt hàng (tổng của tất cả số tiền) cho mỗi mặt sổ đặt hàng.

Sau đó, độ sâu bên `giá thầu` (mua) của sổ đặt hàng được chia cho độ sâu bên `ask` (bán) của sổ đặt hàng và kết quả là delta được so sánh với giá trị của thông số `entry_pricing.check_deep_of_market.bids_to_ask_delta`. Lệnh nhập chỉ được thực thi nếu delta của sổ đặt hàng lớn hơn hoặc bằng giá trị delta được định cấu hình.

!!! Lưu ý
    Giá trị delta dưới 1 có nghĩa là độ sâu của bên sổ đặt hàng `ask` (bán) lớn hơn độ sâu của bên sổ đặt hàng `bid` (mua), trong khi giá trị lớn hơn 1 có nghĩa là ngược lại (độ sâu của bên mua cao hơn độ sâu của bên bán).

### Giá thoát

#### Thoát khỏi bên giá

Cài đặt cấu hình `exit_pricing.price_side` xác định mức chênh lệch mà bot tìm kiếm khi thoát giao dịch.

Sau đây sẽ hiển thị một sổ đặt hàng:``` explanation
...
103
102
101  # ask
-------------Current spread
99   # bid
98
97
...
```Nếu `exit_pricing.price_side` được đặt thành `"ask"` thì bot sẽ sử dụng 101 làm giá thoát.  
Cùng với đó, nếu `exit_pricing.price_side` được đặt thành `"giá thầu"` thì bot sẽ sử dụng 99 làm giá thoát.

Tùy thuộc vào hướng đặt hàng (_long_/_short_), điều này sẽ dẫn đến các kết quả khác nhau. Vì vậy, chúng tôi khuyên bạn nên sử dụng `"same"` hoặc `"other"` cho cấu hình này.
Điều này sẽ dẫn đến ma trận định giá sau:

| Hướng | Đặt hàng | thiết lập | giá | thánh giá lây lan |
|------ |--------|-----|------|------|
| dài | bán | hỏi | 101 | không |
| dài | bán | giá thầu | 99 | vâng |
| dài | bán | giống nhau | 101 | không |
| dài | bán | khác | 99 | vâng |
| ngắn | mua | hỏi | 101 | vâng |
| ngắn | mua | giá thầu | 99 | không |
| ngắn | mua | giống nhau | 99 | không |
| ngắn | mua | khác | 101 | vâng |

#### Giá thoát khi bật Sổ đặt hàng

Khi thoát với sổ đặt hàng được bật (`exit_pricing.use_order_book=True`), Freqtrade tìm nạp các mục nhập `exit_pricing.order_book_top` trong sổ đặt hàng và sử dụng mục nhập được chỉ định là `exit_pricing.order_book_top` từ phía được định cấu hình (`exit_pricing.price_side`) làm giá thoát giao dịch.

1 chỉ định mục nhập trên cùng trong sổ đặt hàng, trong khi 2 sẽ sử dụng mục nhập thứ 2 trong sổ đặt hàng, v.v.

#### Giá thoát khi không kích hoạt Sổ đặt hàng

Phần sau đây sử dụng `side` làm `exit_pricing.price_side` được định cấu hình (mặc định là `"ask"`).

Khi không sử dụng sổ đặt hàng (`exit_pricing.use_order_book=False`), Freqtrade sử dụng giá `phụ` tốt nhất từ ​​mã cổ phiếu nếu nó cao hơn giá giao dịch `cuối cùng` từ mã cổ phiếu. Ngược lại (khi giá `phụ` thấp hơn giá `cuối cùng`), nó sẽ tính tỷ giá giữa giá `phụ` và giá `cuối cùng` dựa trên `exit_pricing.price_last_balance`.

Thông số cấu hình `exit_pricing.price_last_balance` kiểm soát điều này. Giá trị `0,0` sẽ sử dụng giá `side`, trong khi `1.0` sẽ sử dụng giá cuối cùng và các giá trị giữa các nội suy giữa `side` và giá cuối cùng.

### Định giá lệnh thị trường

Khi sử dụng lệnh thị trường, giá phải được cấu hình để sử dụng phía "chính xác" của sổ lệnh để cho phép phát hiện giá thực tế.
Giả sử cả điểm vào và điểm ra đều sử dụng lệnh thị trường, phải sử dụng cấu hình tương tự như sau``` jsonc
  "order_types": {
    "entry": "market",
    "exit": "market"
    // ...
  },
  "entry_pricing": {
    "price_side": "other",
    // ...
  },
  "exit_pricing":{
    "price_side": "other",
    // ...
  },
```Rõ ràng, nếu chỉ một bên sử dụng lệnh giới hạn thì có thể sử dụng các kết hợp giá khác nhau.