<!-- Auto-translated from docs/ by script. Please review technical terms. -->

#Đối tượng giao dịch

## Giao dịch

Vị trí mà freqtrade nhập vào được lưu trữ trong đối tượng `Trade` - đối tượng này được lưu vào cơ sở dữ liệu.
Đó là khái niệm cốt lõi của freqtrade - và là điều bạn sẽ gặp trong nhiều phần của tài liệu, rất có thể sẽ đưa bạn đến vị trí này.

Nó sẽ được chuyển đến chiến lược trong nhiều [cuộc gọi lại chiến lược](strategy-callbacks.md). Đối tượng được truyền cho chiến lược không thể được sửa đổi trực tiếp. Sửa đổi gián tiếp có thể xảy ra dựa trên kết quả gọi lại.

## Giao dịch - Thuộc tính có sẵn

Các thuộc tính / thuộc tính sau đây có sẵn cho từng giao dịch riêng lẻ - và có thể được sử dụng với `trade.<property>` (ví dụ: `trade.pair`).

|  Thuộc tính | Kiểu dữ liệu | Mô tả |
|----------||-------------|-------------|
| `cặp` | chuỗi | Cặp giao dịch này. |
| `safe_base_currency` | chuỗi | Lớp tương thích cho tiền tệ cơ sở. |
| `safe_quote_currency` | chuỗi | Lớp tương thích cho đồng tiền báo giá. |
| `là_open` | boolean | Giao dịch hiện đang mở hay đã được kết thúc. |
| `trao đổi` | chuỗi | Trao đổi nơi giao dịch này được thực hiện. |
| `open_rate` | phao | Tỷ giá mà giao dịch này được nhập ở mức (Tỷ lệ nhập trung bình trong trường hợp điều chỉnh giao dịch). |
| `open_rate_requested` | phao | Tỷ giá được yêu cầu khi giao dịch được mở. |
| `open_trade_value` | phao | Giá trị của giao dịch mở bao gồm phí. |
| `đóng_tỷ lệ` | phao | Tỷ lệ đóng - chỉ được đặt khi is_open = Sai. |
| `đóng_rate_requested` | phao | Tỷ lệ đóng được yêu cầu. |
| `safe_close_rate` | phao | Tỷ lệ đóng hoặc `close_rate_requested` hoặc 0,0 nếu không có sẵn. Chỉ có ý nghĩa khi giao dịch được đóng lại. |
| `số tiền đặt cược` | phao | Số tiền bằng tiền tệ Cổ phần (hoặc Báo giá). |
| `số tiền tối đa_cổ phần` | phao | Số tiền đặt cược tối đa đã được sử dụng trong giao dịch này (tổng của tất cả các lệnh Nhập đã được điền). |
| `số tiền` | phao | Số tiền bằng Tài sản / Tiền tệ cơ bản hiện đang sở hữu. Sẽ là 0,0 cho đến khi đơn hàng ban đầu được lấp đầy. |
| `số tiền_requested` | phao | Số tiền ban đầu được yêu cầu cho giao dịch này như một phần của lệnh nhập đầu tiên. |
| `ngày_mở` | ngày giờ | Dấu thời gian khi giao dịch được mở **thay vào đó hãy sử dụng `open_date_utc`** |
| `open_date_utc` | ngày giờ | Dấu thời gian khi giao dịch được mở - tính theo UTC. |
| `ngày_đóng` | ngày giờ | Dấu thời gian khi giao dịch được đóng **thay vào đó hãy sử dụng `close_date_utc`** |
| `đóng_ngày_utc` | ngày giờ | Dấu thời gian khi giao dịch được đóng - tính bằng UTC. |
| `đóng_lợi nhuận` | phao | Lợi nhuận tương đối tại thời điểm đóng giao dịch. `0,01` == 1% |
| `đóng_lợi nhuận_abs` | phao | Lợi nhuận tuyệt đối (bằng tiền đặt cược) tại thời điểm đóng giao dịch. |
| `lợi nhuận thực hiện` | phao | Lợi nhuận tuyệt đối đã được thực hiện (bằng tiền đặt cược) trong khi giao dịch vẫn mở. |
| `đòn bẩy` | phao | Đòn bẩy được sử dụng cho giao dịch này - mặc định là 1,0 trên thị trường giao ngay. |
| `nhập_thẻ` | chuỗi | Thẻ được cung cấp khi nhập thông qua cột `enter_tag` trong khung dữ liệu. |
| `lý do thoát` | chuỗi | Lý do tại sao giao dịch bị thoát. |
| `exit_order_status` | chuỗi | Trạng thái của lệnh thoát. |
| `chiến lược` | chuỗi | Tên chiến lược đã được sử dụng cho giao dịch này. |
| `khung thời gian` | int | Khung thời gian được sử dụng cho giao dịch này. |
| `là_ngắn` | boolean | Đúng cho các giao dịch bán, Sai nếu không. |
| `đơn đặt hàng` | Đặt hàng[] | Danh sách các đối tượng đặt lệnh gắn liền với giao dịch này (bao gồm cả lệnh đã khớp và lệnh đã hủy). |
| `ngày_last_fill_utc` | ngày giờ | Thời gian thực hiện lệnh cuối cùng. |
| `ngày_entry_fill_utc` | ngày giờ | Ngày của lệnh nhập được điền đầu tiên. || `entry_side` | "mua" / "bán" | Bên đặt hàng giao dịch đã được nhập. |
| `exit_side` | "mua" / "bán" | Bên đặt hàng sẽ dẫn đến việc thoát giao dịch/giảm vị trí. |
| `hướng_giao dịch` | "dài" / "ngắn" | Hướng giao dịch trong văn bản - dài hoặc ngắn. |
| `tỷ lệ tối đa` | phao | Giá cao nhất đạt được trong giao dịch này. Không chính xác 100%. |
| `tỷ lệ tối thiểu` | phao | Giá thấp nhất đạt được trong giao dịch này. Không chính xác 100%. |
| `nr_of_successful_entries` | int | Số lệnh nhập (đã điền) thành công. |
| `nr_of_successful_exits` | int | Số lệnh thoát (đã điền) thành công. |
| `has_open_position` | boolean | Đúng nếu có một vị thế mở (số tiền > 0) cho giao dịch này. Chỉ sai khi lệnh nhập ban đầu không được thực hiện. |
| `has_open_orders` | boolean | Có lệnh mở giao dịch (không bao gồm lệnh dừng lỗ). |
| `has_open_sl_orders` | boolean | Đúng nếu có lệnh dừng lỗ mở cho giao dịch này. |
| `open_orders` | Đặt hàng[] | Tất cả các lệnh mở cho giao dịch này không bao gồm các lệnh dừng lỗ. |
| `open_sl_orders` | Đặt hàng[] | Tất cả các lệnh dừng lỗ mở cho giao dịch này. |
| `hoàn toàn_canceled_entry_order_count` | int | Số lượng lệnh nhập bị hủy hoàn toàn. |
| `đã hủy_exit_order_count` | int | Số lượng lệnh thoát bị hủy. |

### Thuộc tính liên quan đến Dừng lỗ

|  Thuộc tính | Kiểu dữ liệu | Mô tả |
|----------||-------------|-------------|
| `dừng_lỗ` | phao | Giá trị tuyệt đối của mức dừng lỗ. |
| `dừng_lỗ_pct` | phao | Giá trị tương đối của mức dừng lỗ. |
| `ban_stop_loss` | phao | Giá trị tuyệt đối của mức dừng lỗ ban đầu. |
| `ban_stop_loss_pct` | phao | Giá trị tương đối của mức dừng lỗ ban đầu. |
| `stoploss_last_update_utc` | ngày giờ | Dấu thời gian của điểm dừng cuối cùng khi cập nhật lệnh trao đổi. |
| `stoploss_or_liquidation` | phao | Trả về mức giá dừng lỗ hoặc thanh lý hạn chế hơn và tương ứng với mức giá mà mức dừng lỗ sẽ kích hoạt. |

### Thuộc tính giao dịch tương lai/ký quỹ

|  Thuộc tính | Kiểu dữ liệu | Mô tả |
|----------||-------------|-------------|
| `giá thanh lý` | phao | Giá thanh lý cho các giao dịch có đòn bẩy. |
| `lãi suất` | phao | Lãi suất cho giao dịch ký quỹ. |
| `phí tài trợ` | phao | Tổng phí tài trợ cho các giao dịch tương lai. |

## Phương thức lớp

Sau đây là các phương thức lớp - trả về thông tin chung và thường dẫn đến một truy vấn rõ ràng đối với cơ sở dữ liệu.
Chúng có thể được sử dụng làm `Trade.<method>` - ví dụ: `open_trades = Trade.get_open_trade_count()`

!!! Cảnh báo "Backtesting/hyperopt"
    Hầu hết các phương pháp sẽ hoạt động ở cả chế độ backtesting/hyperopt và live/dry.
    Trong quá trình kiểm tra ngược, nó bị giới hạn ở mức sử dụng trong [gọi lại chiến lược](strategy-callbacks.md). Việc sử dụng trong các phương thức `populate_*()` không được hỗ trợ và sẽ dẫn đến kết quả sai.

### get_trades_proxy

Khi chiến lược của bạn cần một số thông tin về các giao dịch hiện tại (mở hoặc đóng) - tốt nhất bạn nên sử dụng `Trade.get_trades_proxy()`.

Cách sử dụng:``` python
from freqtrade.persistence import Trade
from datetime import timedelta

# ...
trade_hist = Trade.get_trades_proxy(pair='ETH/USDT', is_open=False, open_date=current_date - timedelta(days=2))

```

`get_trades_proxy()` supports the following keyword arguments. All arguments are optional - calling `get_trades_proxy()` without arguments will return a list of all trades in the database.

* `pair` e.g. `pair='ETH/USDT'`
* `is_open` e.g. `is_open=False`
* `open_date` e.g. `open_date=current_date - timedelta(days=2)`
* `close_date` e.g. `close_date=current_date - timedelta(days=5)`

### get_open_trade_count

Get the number of currently open trades

``` python
from freqtrade.persistence import Trade
# ...
open_trades = Trade.get_open_trade_count()
```### get_total_closed_profit

Truy xuất tổng lợi nhuận mà bot đã tạo ra cho đến nay.
Tổng hợp `close_profit_abs` cho tất cả các giao dịch đã đóng.``` python
from freqtrade.persistence import Trade

# ...
profit = Trade.get_total_closed_profit()
```### tổng_open_trades_stakes

Truy xuất tổng số stake_amount hiện có trong giao dịch.``` python
from freqtrade.persistence import Trade

# ...
profit = Trade.total_open_trades_stakes()
```## Phương thức lớp không được hỗ trợ trong backtesting/hyperopt

Các phương thức lớp sau không được hỗ trợ ở chế độ backtesting/hyperopt.

### đạt được_hiệu suất tổng thể

Truy xuất hiệu suất tổng thể - tương tự như lệnh telegram `/performance`.``` python
from freqtrade.persistence import Trade

# ...
if self.config['runmode'].value in ('live', 'dry_run'):
    performance = Trade.get_overall_performance()
```Giá trị trả về mẫu: ETH/BTC có 5 giao dịch, với tổng lợi nhuận là 1,5% (tỷ lệ 0,015).``` json
{"pair": "ETH/BTC", "profit": 0.015, "count": 5}
```### khối lượng giao dịch nhận được

Nhận tổng khối lượng giao dịch dựa trên đơn đặt hàng.``` python
from freqtrade.persistence import Trade

# ...
volume = Trade.get_trading_volume()
```## Đối tượng đặt hàng

Đối tượng `Order` đại diện cho một lệnh trên sàn giao dịch (hoặc một lệnh mô phỏng ở chế độ chạy thử).
Đối tượng `Order` sẽ luôn được gắn với [`Trade`](#trade-object) tương ứng của nó và chỉ thực sự có ý nghĩa trong bối cảnh giao dịch.

### Thứ tự - Thuộc tính có sẵn

một đối tượng Đặt hàng thường được gắn vào một giao dịch.
Hầu hết các thuộc tính ở đây có thể là Không có vì chúng phụ thuộc vào phản hồi trao đổi.

|  Thuộc tính | Kiểu dữ liệu | Mô tả |
|----------||-------------|-------------|
| `thương mại` | Thương mại | Đối tượng giao dịch lệnh này được đính kèm |
| `ft_pair` | chuỗi | Ghép nối đơn hàng này dành cho |
| `ft_is_open` | boolean | đơn hàng vẫn còn mở phải không? |
| `ft_order_side` | chuỗi | Bên đặt lệnh ('mua', 'bán' hoặc 'cắt lỗ') |
| `ft_cancel_reason` | chuỗi | Lý do đơn hàng bị hủy |
| `ft_order_tag` | chuỗi | Thẻ đặt hàng tùy chỉnh |
| `order_id` | chuỗi | ID đơn hàng trao đổi |
| `loại_đơn hàng` | chuỗi | Loại lệnh được xác định trên sàn giao dịch - thường là thị trường, giới hạn hoặc dừng lỗ || `status` | string | Status as defined by [ccxt's order structure](https://docs.ccxt.com/#/README?id=order-structure). Usually open, closed, expired, canceled or rejected |
| `bên` | chuỗi | mua hoặc bán |
| `giá` | phao | Giá đặt lệnh tại |
| `trung bình` | phao | Giá trung bình khớp lệnh tại |
| `số tiền` | phao | Số tiền bằng tiền tệ cơ bản |
| `đầy` | phao | Số tiền đã điền (bằng loại tiền cơ bản) (thay vào đó hãy sử dụng `safe_filled`) |
| `safe_fill` | phao | Số tiền đã điền (bằng tiền cơ sở) - được đảm bảo không có |
| `số tiền an toàn` | phao | Số tiền - giảm về ft_amount nếu Không có |
| `giá_an toàn` | phao | Giá - giảm trở lại mức trung bình, giá, stop_price, ft_price |
| `safe_placement_price` | phao | Giá đặt lệnh |
| `còn lại` | phao | Số tiền còn lại (thay vào đó hãy sử dụng `safe_remaining`) |
| `safe_remaining` | phao | Số tiền còn lại - được lấy từ sàn giao dịch hoặc được tính toán. |
| `chi phí an toàn` | phao | Chi phí của đơn hàng - đảm bảo không có Không có |
| `safe_fee_base` | phao | Phí bằng loại tiền cơ sở - đảm bảo không có Không có |
| `safe_amount_after_fee` | phao | Số tiền sau khi trừ phí |
| `chi phí` | phao | Chi phí của lệnh - thường ở mức trung bình * được thực hiện (*Trao đổi phụ thuộc vào giao dịch tương lai, có thể bao gồm chi phí có hoặc không có đòn bẩy và có thể có trong hợp đồng.*) |
| `dừng_giá` | phao | Giá dừng cho lệnh dừng. Trống cho các lệnh không dừng lỗ. |
| `số tiền đặt cược` | phao | Số tiền đặt cọc được sử dụng cho lệnh này. |
| `stake_amount_fill` | phao | Số tiền đặt cọc đã điền được sử dụng cho lệnh này. |
| `ngày_đặt_hàng` | ngày giờ | Ngày tạo đơn hàng **thay vào đó hãy sử dụng `order_date_utc`** |
| `ngày_đặt hàng_utc` | ngày giờ | Ngày tạo đơn hàng (theo giờ UTC) |
| `ngày_đơn_hàng` | ngày giờ |  Ngày điền đơn hàng **thay vào đó hãy sử dụng `order_filled_utc`** |
| `order_fill_utc` | ngày giờ | Ngày điền đơn hàng |
| `ngày_update_đặt_hàng` | ngày giờ | Ngày cập nhật đơn hàng cuối cùng |