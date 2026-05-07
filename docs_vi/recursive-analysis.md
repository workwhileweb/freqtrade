<!-- Auto-translated from docs/ by script. Please review technical terms. -->

# Phân tích đệ quy

Trang này giải thích cách xác thực chiến lược của bạn để phát hiện những điểm không chính xác do các vấn đề đệ quy với một số chỉ báo nhất định.

Công thức đệ quy xác định bất kỳ số hạng nào của dãy liên quan đến (các) số hạng trước nó. Một ví dụ về công thức đệ quy là a<sub>n</sub> = a<sub>n-1</sub> + b.

Tại sao điều này lại quan trọng đối với Freqtrade? Khi kiểm tra ngược, bot sẽ lấy đầy đủ dữ liệu của các cặp theo khoảng thời gian được chỉ định. Nhưng trong quá trình chạy khô/trực tiếp, bot sẽ bị giới hạn bởi lượng dữ liệu mà mỗi sàn giao dịch cung cấp.

Ví dụ: để tính toán một chỉ báo rất cơ bản được gọi là `bước`, giá trị của hàng đầu tiên luôn là 0, trong khi giá trị của các hàng tiếp theo bằng giá trị của hàng trước cộng với 1. Nếu tôi tính toán nó bằng cách sử dụng 1000 nến mới nhất thì giá trị `bước` của hàng đầu tiên là 0 và giá trị `bước` ở cây nến đóng cuối cùng là 999.

Điều gì xảy ra nếu tính toán chỉ sử dụng 500 cây nến mới nhất? Sau đó, thay vì 999, giá trị `bước` ở nến đóng cuối cùng là 499. Sự khác biệt về giá trị có nghĩa là kết quả backtest của bạn có thể khác với kết quả chạy thử/trực tiếp của bạn.

Lệnh `phân tích đệ quy` yêu cầu phải có sẵn dữ liệu lịch sử. Để tìm hiểu cách lấy dữ liệu cho các cặp và trao đổi mà bạn quan tâm,
hãy đi tới phần [Tải xuống dữ liệu](data-download.md) của tài liệu.

Lệnh này được xây dựng dựa trên việc chuẩn bị các độ dài dữ liệu khác nhau và tính toán các chỉ báo dựa trên chúng.
Điều này không tự kiểm tra lại chiến lược mà chỉ tính toán các chỉ số. Sau khi tính toán xong các chỉ báo của các giá trị nến khởi động khác nhau (`startup_candle_count`), giá trị của các hàng cuối cùng trên tất cả `startup_candle_count` được chỉ định sẽ được so sánh để xem mức độ chênh lệch mà chúng hiển thị so với phép tính cơ sở.

Cài đặt lệnh:

- Sử dụng tùy chọn `-p` để đặt cặp mong muốn của bạn để phân tích. Vì chúng ta chỉ xem xét các giá trị chỉ báo nên việc sử dụng nhiều hơn một cặp là không cần thiết. Tốt nhất nên sử dụng một cặp có mức giá tương đối cao và ít nhất có độ biến động vừa phải, chẳng hạn như BTC hoặc ETH, để tránh các vấn đề làm tròn có thể khiến kết quả không chính xác. Nếu không có cặp nào được đặt trên lệnh thì cặp được sử dụng cho phân tích này là cặp đầu tiên trong danh sách trắng.
- Nên đặt khoảng thời gian dài (ít nhất 5000 nến) để việc tính toán các chỉ báo ban đầu sẽ được sử dụng làm điểm chuẩn có rất ít hoặc không có vấn đề đệ quy. Ví dụ: đối với khung thời gian 5 phút, khoảng thời gian 5000 nến sẽ bằng 18 ngày.
- `--cache` bị buộc phải "none" để tránh tự động tải tính toán chỉ báo trước đó.

Ngoài việc kiểm tra công thức đệ quy, lệnh này còn thực hiện kiểm tra độ lệch nhìn trước đơn giản chỉ trên các giá trị chỉ báo. Để kiểm tra toàn bộ cái nhìn về phía trước, hãy sử dụng [Lookahead-analysis](lookahead-analysis.md).

## Tham chiếu lệnh phân tích đệ quy

--8<-- "lệnh/recursive-analysis.md"

### Tại sao nến khởi động mặc định có số lẻ được sử dụng?

Giá trị mặc định cho nến khởi động là số lẻ. Khi bot tìm nạp dữ liệu nến từ API của sàn giao dịch, nến cuối cùng là nến đang được bot kiểm tra và phần dữ liệu còn lại là "nến khởi động".Ví dụ: Binance cho phép 1000 nến cho mỗi lệnh gọi API. Khi bot nhận được 1000 cây nến, cây nến cuối cùng là "nến hiện tại" và 999 cây nến trước đó là "nến khởi động". Bằng cách đặt số lượng nến khởi động là 1000 thay vì 999, bot sẽ cố gắng lấy 1001 nến thay thế. API trao đổi sau đó sẽ gửi dữ liệu nến ở dạng phân trang, tức là trong trường hợp API Binance, đây sẽ là hai nhóm - một nhóm có độ dài 1000 và nhóm khác có độ dài 1. Điều này dẫn đến việc bot nghĩ rằng chiến lược cần 1001 nến dữ liệu, và do đó, nó sẽ tải xuống dữ liệu có giá trị 2000 nến, nghĩa là sẽ có 1 "nến hiện tại" và 1999 "nến khởi nghiệp".

Hơn nữa, các sàn giao dịch giới hạn số lượng lệnh gọi API hàng loạt liên tiếp, ví dụ: Binance cho phép 5 cuộc gọi. Trong trường hợp này, chỉ có thể tải xuống 5000 nến từ API Binance mà không đạt giới hạn tốc độ API, nghĩa là `startup_candle_count` tối đa bạn có thể có là 4999.

Xin lưu ý rằng giới hạn nến này có thể được các sàn giao dịch thay đổi trong tương lai mà không cần thông báo trước.

### Lệnh hoạt động như thế nào?

- Đầu tiên, việc tính toán chỉ báo ban đầu được thực hiện bằng cách sử dụng khoảng thời gian được cung cấp để tạo điểm chuẩn cho các giá trị chỉ báo.
- Sau khi thiết lập điểm chuẩn, nó sẽ thực hiện các lần chạy bổ sung cho từng giá trị số lượng nến khởi động khác nhau.
- Lệnh sau đó sẽ so sánh các giá trị chỉ báo ở các hàng nến cuối cùng và báo cáo sự khác biệt trong bảng.

## Hiểu kết quả phân tích đệ quy

Đây là ví dụ về bảng kết quả đầu ra trong đó ít nhất một chỉ báo có vấn đề về công thức đệ quy:```
| indicators   | 20      | 40      | 80     | 100    | 150     | 300     | 999    |
|--------------+---------+---------+--------+--------+---------+---------+--------|
| rsi_30       | nan%    | -6.025% | 0.612% | 0.828% | -0.140% | 0.000%  | 0.000% |
| rsi_14       | 24.141% | -0.876% | 0.070% | 0.007% | -0.000% | -0.000% | -      |
```Các tiêu đề cột cho biết `startup_candle_count` khác nhau được sử dụng trong phân tích. Các giá trị trong bảng biểu thị phương sai của các chỉ số được tính toán so với giá trị chuẩn.

`nan%` có nghĩa là không thể tính được giá trị của chỉ báo đó do thiếu dữ liệu. Trong ví dụ này, bạn không thể tính RSI có độ dài 30 chỉ với 21 nến (1 nến hiện tại + 20 nến khởi động).

Người dùng nên đánh giá bảng theo từng chỉ báo để quyết định xem liệu `startup_candle_count` được chỉ định có dẫn đến phương sai đủ nhỏ để chỉ báo không có bất kỳ ảnh hưởng nào đến các điểm vào và/hoặc thoát hay không.

Do đó, việc nhắm đến phương sai bằng 0 tuyệt đối (được hiển thị bằng giá trị `-`) có thể không phải là lựa chọn tốt nhất, vì một số chỉ báo có thể yêu cầu bạn sử dụng `startup_candle_count` dài như vậy để có phương sai bằng 0.

## Hãy cẩn thận

- `phân tích đệ quy` sẽ chỉ tính toán và so sánh các giá trị chỉ báo ở hàng cuối cùng. Bảng đầu ra báo cáo sự khác biệt phần trăm giữa các phép tính số lượng nến khởi động khác nhau và phép tính điểm chuẩn ban đầu. Việc nó có bất kỳ tác động thực tế nào đến các điểm vào và ra của bạn hay không đều không được đưa vào.
- Kịch bản lý tưởng là các chỉ báo sẽ không có phương sai (hoặc ít nhất là rất gần 0%) mặc dù nến khởi động rất đa dạng. Trên thực tế, các chỉ báo như EMA đang sử dụng công thức đệ quy để tính toán các giá trị chỉ báo, do đó, mục tiêu không nhất thiết là có phương sai tỷ lệ phần trăm bằng 0, mà phải có phương sai đủ thấp (và do đó `startup_candle_count` đủ cao) để đệ quy vốn có trong chỉ báo sẽ không có bất kỳ tác động thực sự nào đến các quyết định giao dịch.
- `phân tích đệ quy` sẽ chỉ chạy các phép tính trên (các) trình trang trí `populate_indicators` và `@informative`. Nếu bạn đặt bất kỳ phép tính chỉ báo nào vào `populate_entry_trend` hoặc `populate_exit_trend` thì nó sẽ không được tính toán.