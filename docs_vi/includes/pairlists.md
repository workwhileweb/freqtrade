<!-- Auto-translated from docs/ by script. Please review technical terms. -->

## Danh sách cặp và Trình xử lý danh sách cặp

Trình xử lý danh sách cặp xác định danh sách các cặp (danh sách cặp) mà bot nên giao dịch. Chúng được định cấu hình trong phần `danh sách cặp` của cài đặt cấu hình.

Trong cấu hình của mình, bạn có thể sử dụng Danh sách cặp tĩnh (được xác định bởi Trình xử lý danh sách cặp [`StaticPairList`](#static-pair-list)) và Danh sách cặp động (được xác định bởi [`VolumePairList`](#volume-pair-list), [`CrossMarketPairList`](#crossmarketpairlist), [`MarketCapPairlist`](#marketcappairlist) và [`PercentChangePairList`](#percent-change-pair-list) Trình xử lý danh sách cặp).

Ngoài ra, [`AgeFilter`](#agefilter), [`DelistFilter`](#delistfilter), [`PrecisionFilter`](#precisionfilter), [`PriceFilter`](#pricefilter), [`ShuffleFilter`](#shufflefilter), [`SpreadFilter`](# Spreadfilter) và [`VolatilityFilter`](#volatilityfilter) hoạt động như Bộ lọc danh sách cặp, xóa một số cặp nhất định và/hoặc di chuyển vị trí của họ trong danh sách cặp đôi.

Nếu nhiều Trình xử lý danh sách cặp được sử dụng, chúng sẽ được xâu chuỗi và sự kết hợp của tất cả các Trình xử lý danh sách cặp sẽ tạo thành danh sách cặp kết quả mà bot sử dụng để giao dịch và kiểm tra ngược. Trình xử lý danh sách cặp được thực thi theo trình tự chúng được định cấu hình. Bạn có thể xác định `StaticPairList`, `VolumePairList`, `ProducerPairList`, `RemotePairList`, `MarketCapPairList`, `PercentChangePairList` hoặc `CrossMarketPairList` làm Trình xử lý danh sách cặp bắt đầu.

Các thị trường không hoạt động luôn bị xóa khỏi danh sách cặp kết quả. Các cặp được đưa vào danh sách đen rõ ràng (những cặp trong cài đặt cấu hình `pair_blacklist`) cũng luôn bị xóa khỏi danh sách cặp kết quả.

### Cặp danh sách đen

Danh sách đen cặp (được định cấu hình thông qua `exchange.pair_blacklist` trong cấu hình) không cho phép một số cặp nhất định giao dịch.
Việc này có thể đơn giản như loại trừ `DOGE/BTC` - việc này sẽ loại bỏ chính xác cặp này.

Danh sách đen cặp cũng hỗ trợ các ký tự đại diện (theo kiểu biểu thức chính quy) - vì vậy `BNB/.*` sẽ loại trừ TẤT CẢ các cặp bắt đầu bằng BNB.
Bạn cũng có thể sử dụng cái gì đó như `.*DOWN/BTC` hoặc `.*UP/BTC` để loại trừ mã thông báo đòn bẩy (kiểm tra quy ước đặt tên theo cặp cho sàn giao dịch của bạn!)

### Trình xử lý danh sách cặp có sẵn

* [`StaticPairList`](#static-pair-list) (mặc định, nếu không được định cấu hình khác)
* [`VolumePairList`](#volume-pair-list)
* [`PercentChangePairList`](#percent-change-pair-list)
* [`ProducerPairList`](#producerpairlist)
* [`RemotePairList`](#remotepairlist)
* [`MarketCapPairList`](#marketcappairlist)
* [`CrossMarketPairList`](#crossmarketpairlist)
* [`AgeFilter`](#agefilter)
* [`DelistFilter`](#delistfilter)
* [`FullTradesFilter`](#fulltradesfilter)
* [`OffsetFilter`](#offsetfilter)
* [`PerformanceFilter`](#performancefilter)
* [`PrecisionFilter`](#precisionfilter)
* [`PriceFilter`](#pricefilter)
* [`ShuffleFilter`](#shufflefilter)
* [`SpreadFilter`](#s Lanfilter)
* [`RangeStabilityFilter`](#rangestabilityfilter)
* [`Bộ lọc biến động`](#bộ lọc biến động)

!!! Mẹo "Kiểm tra danh sách cặp"
    Cấu hình danh sách cặp đôi có thể khá khó khăn để thực hiện đúng. Tốt nhất hãy sử dụng freqUI trong [chế độ máy chủ web](freq-ui.md#webserver-mode) hoặc lệnh phụ tiện ích [`test-pairlist`](utils.md#test-pairlist) để kiểm tra nhanh cấu hình Danh sách cặp của bạn.

#### Danh sách cặp tĩnh

Theo mặc định, phương thức `StaticPairList` được sử dụng, phương thức này sử dụng danh sách trắng cặp được xác định tĩnh từ cấu hình. Danh sách cặp cũng hỗ trợ các ký tự đại diện (theo kiểu biểu thức chính quy) - vì vậy `.*/BTC` sẽ bao gồm tất cả các cặp có BTC làm cổ phần.Nó sử dụng cấu hình từ `exchange.pair_whitelist` và `exchange.pair_blacklist`, trong ví dụ dưới đây, sẽ giao dịch BTC/USDT và ETH/USDT - và sẽ ngăn giao dịch BNB/USDT.

Cả hai tham số `pair_*list` đều hỗ trợ biểu thức chính quy - vì vậy các giá trị như `.*/USDT` sẽ cho phép giao dịch tất cả các cặp không có trong danh sách đen.```json
"exchange": {
    "name": "...",
    // ... 
    "pair_whitelist": [
        "BTC/USDT",
        "ETH/USDT",
        // ...
    ],
    "pair_blacklist": [
        "BNB/USDT",
        // ...
    ]
},
"pairlists": [
    {"method": "StaticPairList"}
],
```Theo mặc định, chỉ cho phép các cặp hiện đang được kích hoạt.
Để bỏ qua việc xác thực cặp đối với các thị trường đang hoạt động, hãy đặt `"allow_inactive": true` trong cấu hình `StaticPairList`.
Điều này có thể hữu ích cho việc kiểm tra lại các cặp đã hết hạn (như thị trường giao ngay hàng quý).

Khi được sử dụng ở vị trí "theo dõi" (ví dụ: sau VolumePairlist), tất cả các cặp trong `'pair_whitelist'` sẽ được thêm vào cuối danh sách cặp.

#### Danh sách cặp khối lượng

`VolumePairList` sử dụng việc sắp xếp/lọc các cặp theo khối lượng giao dịch của chúng. Nó chọn các cặp trên cùng `number_assets` với cách sắp xếp dựa trên `sort_key` (chỉ có thể là `quoteVolume`).

Khi được sử dụng trong chuỗi Trình xử lý danh sách cặp ở vị trí không dẫn đầu (sau StaticPairList và các Bộ lọc danh sách cặp khác), `VolumePairList` xem xét kết quả đầu ra của Trình xử lý danh sách cặp trước đó, thêm việc sắp xếp/lựa chọn các cặp theo khối lượng giao dịch.

Khi được sử dụng ở vị trí dẫn đầu trong chuỗi Trình xử lý danh sách cặp, cài đặt cấu hình `pair_whitelist` sẽ bị bỏ qua. Thay vào đó, `VolumePairList` chọn những tài sản hàng đầu từ tất cả các thị trường có sẵn với loại tiền tệ cổ phần phù hợp trên sàn giao dịch.

Cài đặt `refresh_ Period` cho phép xác định khoảng thời gian (tính bằng giây), tại đó danh sách cặp sẽ được làm mới. Mặc định là những năm 1800 (30 phút).
Bộ đệm danh sách cặp (`refresh_ Period`) trên `VolumePairList` chỉ áp dụng để tạo danh sách cặp.
Các trường hợp lọc (không phải vị trí đầu tiên trong danh sách) sẽ không áp dụng bất kỳ bộ nhớ đệm nào (ngoài các nến lưu vào bộ nhớ đệm trong suốt thời gian của nến ở chế độ nâng cao) và sẽ luôn sử dụng dữ liệu cập nhật.

`VolumePairList` được mặc định dựa trên dữ liệu mã đánh dấu từ sàn giao dịch, theo báo cáo của thư viện ccxt:

* `quoteVolume` là số lượng tiền định giá (cổ phần) được giao dịch (mua hoặc bán) trong 24 giờ qua.```json
"pairlists": [
    {
        "method": "VolumePairList",
        "number_assets": 20,
        "sort_key": "quoteVolume",
        "min_value": 0,
        "max_value": 8000000,
        "refresh_period": 1800
    }
],
```Bạn có thể xác định âm lượng tối thiểu bằng `min_value` - thao tác này sẽ lọc ra các cặp có âm lượng thấp hơn giá trị được chỉ định trong khoảng thời gian đã chỉ định.
Ngoài ra, bạn cũng có thể xác định âm lượng tối đa bằng `max_value` - sẽ lọc ra các cặp có âm lượng cao hơn giá trị được chỉ định trong khoảng thời gian đã chỉ định.

##### VolumePairList Chế độ nâng cao

`VolumePairList` cũng có thể hoạt động ở chế độ nâng cao để tạo khối lượng trong một khoảng thời gian nhất định với kích thước nến được chỉ định. Nó sử dụng dữ liệu lịch sử nến của sàn giao dịch, xây dựng mức giá điển hình (được tính bằng (mở+cao+thấp)/3) và nhân giá điển hình với khối lượng của mỗi nến. Tổng là `quoteVolume` trong phạm vi đã cho. Điều này cho phép các kịch bản khác nhau, để có âm lượng mượt mà hơn, khi sử dụng phạm vi dài hơn với kích thước nến lớn hơn hoặc ngược lại khi sử dụng phạm vi ngắn với nến nhỏ.

Để thuận tiện, bạn có thể chỉ định `ngày nhìn lại`, điều này có nghĩa là nến 1 ngày sẽ được sử dụng cho lượt xem lại. Trong ví dụ bên dưới, danh sách cặp sẽ được tạo dựa trên 7 ngày qua:```json
"pairlists": [
    {
        "method": "VolumePairList",
        "number_assets": 20,
        "sort_key": "quoteVolume",
        "min_value": 0,
        "refresh_period": 86400,
        "lookback_days": 7
    }
],
```!!! Cảnh báo "Phạm vi nhìn lại và thời gian làm mới"
    Khi được sử dụng cùng với `lookback_days` và `lookback_timeframe`, `refresh_ Period` không được nhỏ hơn kích thước nến tính bằng giây. Vì điều này sẽ dẫn đến các yêu cầu không cần thiết tới API trao đổi.

!!! Cảnh báo "Ý nghĩa về hiệu suất khi sử dụng phạm vi xem lại"
    Nếu được sử dụng ở vị trí đầu tiên kết hợp với xem lại, việc tính toán khối lượng dựa trên phạm vi có thể tiêu tốn thời gian và tài nguyên vì nó tải xuống nến cho tất cả các cặp có thể giao dịch. Do đó, chúng tôi khuyên bạn nên sử dụng phương pháp tiêu chuẩn với `VolumeFilter` để thu hẹp danh sách cặp để tính toán phạm vi âm lượng sâu hơn.

??? Mẹo "Sàn giao dịch không được hỗ trợ"
    Trên một số sàn giao dịch (như Gemini), VolumePairList thông thường không hoạt động vì api vốn không cung cấp khối lượng 24 giờ. Điều này có thể được giải quyết bằng cách sử dụng dữ liệu nến để xây dựng khối lượng.
    Để mô phỏng đại khái âm lượng 24h, bạn có thể sử dụng cấu hình sau.
    Xin lưu ý rằng các danh sách cặp này sẽ chỉ được làm mới một lần mỗi ngày.```json
    "pairlists": [
        {
            "method": "VolumePairList",
            "number_assets": 20,
            "sort_key": "quoteVolume",
            "min_value": 0,
            "refresh_period": 86400,
            "lookback_days": 1
        }
    ],
    ```Bạn có thể sử dụng cách tiếp cận phức tạp hơn bằng cách sử dụng `khung_thời gian xem lại` cho kích thước nến và `thời gian xem lại` chỉ định số lượng nến. Ví dụ này sẽ xây dựng các cặp khối lượng dựa trên khoảng thời gian kéo dài 3 ngày của nến 1 giờ:```json
"pairlists": [
    {
        "method": "VolumePairList",
        "number_assets": 20,
        "sort_key": "quoteVolume",
        "min_value": 0,
        "refresh_period": 3600,
        "lookback_timeframe": "1h",
        "lookback_period": 72
    }
],
```!!! Lưu ý
    `VolumePairList` không hỗ trợ chế độ kiểm tra lại.

#### Danh sách cặp phần trăm thay đổi

`PercentChangePairList` lọc và sắp xếp các cặp dựa trên phần trăm thay đổi về giá của chúng trong 24 giờ qua hoặc bất kỳ khung thời gian xác định nào như một phần của các tùy chọn nâng cao. Điều này cho phép các nhà giao dịch tập trung vào các tài sản đã trải qua biến động giá đáng kể, dù tích cực hay tiêu cực.

**Tùy chọn cấu hình**

* `number_assets`: Chỉ định số lượng cặp hàng đầu cần chọn dựa trên phần trăm thay đổi trong 24 giờ.
* `min_value`: Đặt ngưỡng thay đổi phần trăm tối thiểu. Các cặp có phần trăm thay đổi dưới giá trị này sẽ bị lọc ra.
* `max_value`: Đặt ngưỡng thay đổi phần trăm tối đa. Các cặp có phần trăm thay đổi trên giá trị này sẽ bị lọc ra.
* `sort_direction`: Chỉ định thứ tự các cặp được sắp xếp dựa trên phần trăm thay đổi của chúng. Chấp nhận hai giá trị: `asc` cho thứ tự tăng dần và `desc` cho thứ tự giảm dần.
* `refresh_ Period`: Xác định khoảng thời gian (tính bằng giây) mà danh sách cặp sẽ được làm mới. Mặc định là 1800 giây (30 phút).
* `lookback_days`: Số ngày nhìn lại. Khi `lookback_days` được chọn, `lookback_timeframe` được mặc định là 1 ngày.
* `lookback_timeframe`: Khung thời gian sử dụng cho giai đoạn xem lại.
* `lookback_ Period`: Số kỳ cần xem lại.

Khi PercentChangePairList được sử dụng sau các Trình xử lý danh sách cặp khác, nó sẽ hoạt động trên đầu ra của các trình xử lý đó. Nếu nó là Trình xử lý danh sách cặp hàng đầu, nó sẽ chọn các cặp từ tất cả các thị trường có sẵn với loại tiền đặt cọc được chỉ định.

`PercentChangePairList` sử dụng dữ liệu mã cổ phiếu từ sàn giao dịch, được cung cấp qua thư viện ccxt:
Phần trăm thay đổi được tính là sự thay đổi về giá trong 24 giờ qua.

??? Lưu ý "Trao đổi không được hỗ trợ"
    Trên một số sàn giao dịch (như HTX), PercentChangePairList thông thường không hoạt động vì api vốn không cung cấp sự thay đổi phần trăm về giá trong 24 giờ. Điều này có thể được giải quyết bằng cách sử dụng dữ liệu nến để tính phần trăm thay đổi. Để mô phỏng đại khái sự thay đổi phần trăm trong 24 giờ, bạn có thể sử dụng cấu hình sau. Xin lưu ý rằng các danh sách cặp này sẽ chỉ được làm mới một lần mỗi ngày.```json
    "pairlists": [
        {
            "method": "PercentChangePairList",
            "number_assets": 20,
            "min_value": 0,
            "refresh_period": 86400,
            "lookback_days": 1
        }
    ],
    ```**Cấu hình ví dụ để đọc từ mã **```json
"pairlists": [
    {
        "method": "PercentChangePairList",
        "number_assets": 15,
        "min_value": -10,
        "max_value": 50
    }
],
```Trong cấu hình này:

1. 15 cặp hàng đầu được chọn dựa trên phần trăm thay đổi giá cao nhất trong 24 giờ qua.
2. Chỉ những cặp có phần trăm thay đổi từ -10% đến 50% mới được xem xét.

**Cấu hình ví dụ để đọc từ nến**```json
"pairlists": [
    {
        "method": "PercentChangePairList",
        "number_assets": 15,
        "sort_key": "percentage",
        "min_value": 0,
        "refresh_period": 3600,
        "lookback_timeframe": "1h",
        "lookback_period": 72
    }
],
```Ví dụ này xây dựng các cặp phần trăm thay đổi dựa trên khoảng thời gian luân phiên là 3 ngày của nến 1 giờ bằng cách sử dụng `khung thời gian xem lại` cho kích thước nến và `thời gian xem lại` chỉ định số lượng nến.

Phần trăm thay đổi về giá được tính bằng công thức sau, biểu thị phần trăm chênh lệch giữa giá đóng của nến hiện tại và giá đóng của nến trước đó, như được xác định theo khung thời gian và khoảng thời gian xem lại đã chỉ định:

$$ Phần trăm thay đổi = (\frac{Đóng hiện tại - Đóng trước đó}{Đóng trước}) * 100 $$

!!! Cảnh báo "Phạm vi nhìn lại và thời gian làm mới"
    Khi được sử dụng cùng với `lookback_days` và `lookback_timeframe`, `refresh_ Period` không được nhỏ hơn kích thước nến tính bằng giây. Vì điều này sẽ dẫn đến các yêu cầu không cần thiết tới API trao đổi.

!!! Cảnh báo "Ý nghĩa về hiệu suất khi sử dụng phạm vi xem lại"
    Nếu được sử dụng ở vị trí đầu tiên kết hợp với xem lại, việc tính toán phần trăm thay đổi dựa trên phạm vi có thể tiêu tốn thời gian và tài nguyên vì nó tải xuống nến cho tất cả các cặp có thể giao dịch. Do đó, chúng tôi khuyên bạn nên sử dụng phương pháp tiêu chuẩn với `PercentChangePairList` để thu hẹp danh sách cặp xuống để tính toán phần trăm thay đổi thêm.

!!! Lưu ý "Kiểm tra lại"
    `PercentChangePairList` không hỗ trợ chế độ kiểm tra lại.

#### Danh sách cặp nhà sản xuất

Với `ProducerPairList`, bạn có thể sử dụng lại danh sách cặp từ [Producer](producer-consumer.md) mà không cần xác định rõ ràng danh sách cặp trên mỗi người tiêu dùng.

Cần có [Chế độ tiêu dùng](producer-consumer.md) để danh sách cặp này hoạt động.

Danh sách cặp đôi sẽ thực hiện kiểm tra các cặp hoạt động dựa trên cấu hình trao đổi hiện tại để tránh cố gắng giao dịch trên các thị trường không hợp lệ.

Bạn có thể giới hạn độ dài của danh sách cặp bằng tham số tùy chọn `number_assets`. Việc sử dụng `"number_assets"=0` hoặc bỏ qua khóa này sẽ dẫn đến việc sử dụng lại tất cả các cặp nhà sản xuất hợp lệ cho thiết lập hiện tại.```json
"pairlists": [
    {
        "method": "ProducerPairList",
        "number_assets": 5,
        "producer_name": "default",
    }
],
```!!! Mẹo "Kết hợp danh sách cặp"
    Danh sách cặp này có thể được kết hợp với tất cả các danh sách cặp và bộ lọc khác để giảm bớt danh sách cặp và cũng có thể hoạt động như một danh sách cặp "bổ sung", bên cạnh các cặp đã được xác định.
    `ProducerPairList` cũng có thể được sử dụng nhiều lần theo trình tự, kết hợp các cặp từ nhiều nhà sản xuất.
    Rõ ràng trong các cấu hình phức tạp như vậy, Nhà sản xuất có thể không cung cấp dữ liệu cho tất cả các cặp, vì vậy chiến lược phải phù hợp với việc này.

####Danh sách RemotePairList

Nó cho phép người dùng tìm nạp danh sách cặp từ máy chủ từ xa hoặc tệp json được lưu trữ cục bộ trong thư mục freqtrade, cho phép cập nhật động và tùy chỉnh danh sách cặp giao dịch.

RemotePairList được xác định trong phần danh sách cặp của cài đặt cấu hình. Nó sử dụng các tùy chọn cấu hình sau:```json
"pairlists": [
    {
        "method": "RemotePairList",
        "mode": "whitelist",
        "processing_mode": "filter",
        "pairlist_url": "https://example.com/pairlist",
        "number_assets": 10,
        "refresh_period": 1800,
        "keep_pairlist_on_failure": true,
        "read_timeout": 60,
        "bearer_token": "my-bearer-token",
        "save_to_file": "user_data/filename.json" 
    }
]
```Tùy chọn `mode` tùy chọn chỉ định xem danh sách cặp nên được sử dụng làm `danh sách đen` hay `danh sách trắng`. Giá trị mặc định là "danh sách trắng".

Tùy chọn `processing_mode` tùy chọn trong cấu hình RemotePairList xác định cách xử lý danh sách cặp đã truy xuất. Nó có thể có hai giá trị: "filter" hoặc "append". Giá trị mặc định là "bộ lọc".

Tùy chọn `number_assets` tùy chọn trong cấu hình RemotePairList xác định số lượng cặp sẽ được trả về nếu được sử dụng trong `chế độ` danh sách trắng. Theo mặc định, tất cả các cặp sẽ được trả về. Trong danh sách đen `mode`, tùy chọn này sẽ bị bỏ qua.

Trong chế độ "bộ lọc", danh sách cặp được truy xuất sẽ được sử dụng làm bộ lọc. Chỉ các cặp có trong cả danh sách cặp ban đầu và danh sách cặp được truy xuất mới được đưa vào danh sách cặp cuối cùng. Các cặp khác được lọc ra.

Ở chế độ "chắp thêm", danh sách cặp đã truy xuất sẽ được thêm vào danh sách cặp ban đầu. Tất cả các cặp từ cả hai danh sách đều được đưa vào danh sách cặp cuối cùng mà không cần lọc.

Tùy chọn `pairlist_url` chỉ định URL của máy chủ từ xa nơi đặt danh sách cặp hoặc đường dẫn đến tệp cục bộ (nếu file:/// được thêm vào trước). Điều này cho phép người dùng sử dụng máy chủ từ xa hoặc tệp cục bộ làm nguồn cho danh sách cặp.

Tùy chọn `save_to_file`, khi được cung cấp tên tệp hợp lệ, sẽ lưu danh sách cặp đã xử lý vào tệp đó ở định dạng JSON. Tùy chọn này là tùy chọn và theo mặc định, danh sách cặp không được lưu vào tệp.

??? Ví dụ "Ví dụ về nhiều bot với danh sách cặp chia sẻ"

    `save_to_file` có thể được sử dụng để lưu danh sách cặp vào một tệp bằng Bot1:```json
    "pairlists": [
        {
            "method": "RemotePairList",
            "mode": "whitelist",
            "pairlist_url": "https://example.com/pairlist",
            "number_assets": 10,
            "refresh_period": 1800,
            "keep_pairlist_on_failure": true,
            "read_timeout": 60,
            "save_to_file": "user_data/filename.json" 
        }
    ]
    ```Tệp danh sách cặp đã lưu này có thể được tải bởi Bot2 hoặc bất kỳ bot bổ sung nào có cấu hình này:```json
    "pairlists": [
        {
            "method": "RemotePairList",
            "mode": "whitelist",
            "pairlist_url": "file:///user_data/filename.json",
            "number_assets": 10,
            "refresh_period": 10,
            "keep_pairlist_on_failure": true,
        }
    ]
    ```Người dùng có trách nhiệm cung cấp máy chủ hoặc tệp cục bộ trả về một đối tượng JSON có cấu trúc sau:```json
{
    "pairs": ["XRP/USDT", "ETH/USDT", "LTC/USDT"],
    "refresh_period": 1800
}
```Thuộc tính `pairs` phải chứa danh sách các chuỗi có cặp giao dịch sẽ được bot sử dụng. Thuộc tính `refresh_ Period` là tùy chọn và chỉ định số giây mà danh sách cặp sẽ được lưu vào bộ đệm trước khi được làm mới.

Tùy chọn `keep_pairlist_on_failure` chỉ định xem có nên sử dụng danh sách cặp đã nhận trước đó hay không nếu máy chủ từ xa không thể truy cập được hoặc trả về lỗi. Giá trị mặc định là đúng.

`read_timeout` tùy chọn chỉ định lượng thời gian tối đa (tính bằng giây) để chờ phản hồi từ nguồn từ xa, Giá trị mặc định là 60.

`bearer_token` tùy chọn sẽ được bao gồm trong Tiêu đề ủy quyền của yêu cầu.

!!! Lưu ý
    Trong trường hợp xảy ra lỗi máy chủ, danh sách cặp nhận được lần cuối sẽ được giữ lại nếu `keep_pairlist_on_failure` được đặt thành true, khi được đặt thành false, danh sách cặp trống sẽ được trả về.

#### MarketCapPairList

`MarketCapPairList` sử dụng việc sắp xếp/lọc các cặp theo thứ hạng vốn hóa thị trường của chúng dựa trên CoinGecko. Danh sách cặp được trả về sẽ được sắp xếp dựa trên thứ hạng vốn hóa thị trường của chúng nếu được sử dụng trong `chế độ` danh sách trắng.```json
"pairlists": [
    {
        "method": "MarketCapPairList",
        "number_assets": 20,
        "max_rank": 50,
        "refresh_period": 86400,
        "mode": "whitelist",
        "categories": ["layer-1"]
    }
]
````number_assets` xác định số lượng cặp tối đa được danh sách cặp trả về nếu được sử dụng trong `chế độ` danh sách trắng. Trong `mode` danh sách đen, cài đặt này sẽ bị bỏ qua.

`max_rank` sẽ xác định thứ hạng tối đa được sử dụng trong việc tạo/lọc danh sách cặp. Dự kiến, một số đồng xu trong vốn hóa thị trường `max_rank` hàng đầu sẽ không được đưa vào danh sách cặp kết quả vì không phải tất cả các cặp đều có cặp giao dịch đang hoạt động trong kết hợp thị trường/cổ phần/trao đổi ưa thích của bạn.  
Mặc dù hỗ trợ sử dụng `max_rank` lớn hơn 250 nhưng bạn không nên làm vậy vì nó sẽ gây ra nhiều lệnh gọi API tới CoinGecko, điều này có thể dẫn đến các vấn đề về giới hạn tốc độ.

Cài đặt `refresh_ Period` xác định khoảng thời gian (tính bằng giây) mà tại đó dữ liệu xếp hạng vốn hóa thị trường sẽ được làm mới. Mặc định là 86.400 giây (1 ngày). Bộ đệm danh sách cặp (`refresh_ Period`) áp dụng cho cả việc tạo danh sách cặp (khi ở vị trí đầu tiên trong danh sách) và các phiên bản lọc (khi không ở vị trí đầu tiên trong danh sách).

Cài đặt `mode` xác định liệu plugin sẽ lọc trong (danh sách trắng `mode`) hay lọc ra (danh sách đen `mode`) các đồng tiền được xếp hạng vốn hóa thị trường hàng đầu. Theo mặc định, plugin sẽ ở chế độ danh sách trắng.The `categories` setting specifies the [coingecko categories](https://www.coingecko.com/en/categories) from which to select coins from. The default is an empty list `[]`, meaning no category filtering is applied.
If an incorrect category string is chosen, the plugin will print the available categories from CoinGecko and fail. The category should be the ID of the category, for example, for `https://www.coingecko.com/en/categories/layer-1`, the category ID would be `layer-1`. You can pass multiple categories such as `["layer-1", "meme-token"]` to select from several categories.
Các đồng tiền như 1000PEPE/USDT hoặc KPEPE/USDT:USDT được phát hiện trên cơ sở nỗ lực tốt nhất, với tiền tố `1000` và `K` được sử dụng để nhận dạng chúng.

!!! Cảnh báo "Nhiều danh mục"
    Mỗi danh mục được thêm vào tương ứng với một lệnh gọi API tới CoinGecko. Bạn càng thêm nhiều danh mục thì quá trình tạo danh sách cặp sẽ càng mất nhiều thời gian, điều này có thể gây ra vấn đề về giới hạn tỷ lệ.

!!! Nguy hiểm "Biểu tượng trùng lặp trong coinecko"
    Coingecko thường có các biểu tượng trùng lặp, trong đó cùng một biểu tượng được sử dụng cho các đồng tiền khác nhau. Freqtrade sẽ sử dụng biểu tượng này và cố gắng tìm kiếm nó trên sàn giao dịch. Nếu biểu tượng tồn tại - nó sẽ được sử dụng. Tuy nhiên, Freqtrade sẽ không kiểm tra xem biểu tượng _intend_ có phải là biểu tượng của coinecko hay không. Điều này đôi khi có thể dẫn đến kết quả không mong muốn, đặc biệt là trên các đồng tiền có khối lượng thấp hoặc với các danh mục đồng meme.

#### CrossMarketPairList

Tạo hoặc lọc các cặp dựa trên tính sẵn có của chúng trên thị trường đối diện.

Cài đặt `pairs_exist_on` xác định liệu các cặp sẽ tồn tại trên cả thị trường giao ngay và thị trường tương lai (`both_markets`) hay chỉ tồn tại trên chế độ giao dịch được chỉ định (`current_market_only`). Theo mặc định, plugin sẽ ở cài đặt `both_markets`, có nghĩa là các cặp trong danh sách cho phép phải tồn tại trên cả thị trường giao ngay và thị trường tương lai.

####Bộ lọc tuổi

Xóa các cặp đã được niêm yết trên sàn giao dịch ít hơn `min_days_list` ngày (mặc định là `10`) hoặc nhiều hơn `max_days_list` ngày (mặc định `None` có nghĩa là vô tận).

Khi các cặp lần đầu tiên được niêm yết trên sàn giao dịch, chúng có thể bị giảm giá và biến động lớn.
trong vài ngày đầu tiên khi cặp tiền này trải qua giai đoạn khám phá giá. Bot thường có thể
bị phát hiện đang mua trước khi cặp tiền này giảm giá xong.

Bộ lọc này cho phép freqtrade bỏ qua các cặp cho đến khi chúng được liệt kê trong ít nhất `min_days_list` ngày và được liệt kê trước `max_days_list`.

#### Bộ lọc xóa danh sách

Xóa các cặp sẽ bị hủy niêm yết trên sàn giao dịch tối đa `max_days_from_now` ngày kể từ bây giờ (mặc định là `0` sẽ xóa tất cả các cặp bị xóa trong tương lai bất kể thời điểm hiện tại là bao xa). Hiện tại bộ lọc này chỉ hỗ trợ các sàn giao dịch sau:

!!! Lưu ý "Trao đổi có sẵn"
    Bộ lọc xóa danh sách có sẵn trên Bybit Futures, Bitget Futures và Binance, trong đó Binance Futures sẽ hoạt động ở cả chế độ khô và trực tiếp, trong khi Binance Spot bị giới hạn ở chế độ trực tiếp (vì lý do kỹ thuật).

!!! Cảnh báo "Đang kiểm tra lại"
    `DelistFilter` không hỗ trợ chế độ kiểm tra lại.

#### Bộ lọc giao dịch đầy đủ

Thu gọn danh sách trắng để chỉ bao gồm các cặp trong giao dịch khi vị trí giao dịch đã đầy (khi `max_open_trades` không được đặt thành `-1` trong cấu hình).

Khi các ô giao dịch đã đầy, không cần tính toán chỉ báo của các cặp còn lại (trừ các cặp thông tin) vì không thể mở giao dịch mới. Bằng cách thu hẹp danh sách trắng chỉ còn các cặp đang giao dịch, bạn có thể cải thiện tốc độ tính toán và giảm mức sử dụng CPU. Khi vị trí giao dịch trống (giao dịch bị đóng hoặc giá trị `max_open_trades` trong cấu hình tăng lên), thì danh sách trắng sẽ trở lại trạng thái bình thường.

Khi sử dụng nhiều bộ lọc danh sách cặp, bạn nên đặt bộ lọc này ở vị trí thứ hai ngay bên dưới danh sách cặp chính để khi các vị trí giao dịch đã đầy, bot không phải tải xuống dữ liệu cho các bộ lọc còn lại.

!!! Cảnh báo "Đang kiểm tra lại"
    `FullTradesFilter` không hỗ trợ chế độ kiểm tra lại.

####Bộ lọc bù đắp

Bù đắp danh sách cặp đến bằng một giá trị `offset` nhất định.Để làm ví dụ, nó có thể được sử dụng cùng với `VolumeFilter` để loại bỏ các cặp âm lượng X trên cùng. Hoặc để chia danh sách cặp lớn hơn trên hai phiên bản bot.

Ví dụ để xóa 10 cặp đầu tiên khỏi danh sách cặp và lấy 20 cặp tiếp theo (lấy các mục 10-30 trong danh sách ban đầu):```json
"pairlists": [
    // ...
    {
        "method": "OffsetFilter",
        "offset": 10,
        "number_assets": 20
    }
],
```!!! Cảnh báo
    Khi `OffsetFilter` được sử dụng để phân chia danh sách cặp lớn hơn giữa nhiều bot kết hợp với `VolumeFilter`
    không thể đảm bảo rằng các cặp sẽ không trùng nhau do khoảng thời gian làm mới hơi khác nhau đối với
    `Bộ lọc âm lượng`.

!!! Lưu ý
    Phần bù lớn hơn tổng chiều dài của danh sách cặp đến sẽ dẫn đến danh sách cặp trống.

####Bộ lọc hiệu suất

Sắp xếp các cặp theo hiệu suất giao dịch trong quá khứ như sau:

1. Hiệu suất tích cực.
2. Chưa đóng giao dịch nào.
3. Hiệu suất tiêu cực.

Số lượng giao dịch được sử dụng như một công cụ ngắt kết quả.

Bạn có thể sử dụng tham số `phút` để chỉ xem xét hiệu suất của X phút vừa qua (cửa sổ cuộn).
Không xác định tham số này (hoặc đặt thành 0) sẽ sử dụng hiệu suất mọi thời đại.

Tham số `min_profit` tùy chọn (dưới dạng tỷ lệ -> cài đặt `0,01` tương ứng với 1%) xác định lợi nhuận tối thiểu mà một cặp phải được xem xét.
Các cặp dưới mức này sẽ bị lọc ra.
Không nên sử dụng tham số này mà không có `phút` vì nó có thể dẫn đến một danh sách cặp trống mà không có cách nào để khôi phục.```json
"pairlists": [
    // ...
    {
        "method": "PerformanceFilter",
        "minutes": 1440,  // rolling 24h
        "min_profit": 0.01  // minimal profit 1%
    }
],
```Vì Bộ lọc này sử dụng hiệu suất trước đây của bot nên nó sẽ có một khoảng thời gian khởi động - và chỉ nên được sử dụng sau khi bot có vài 100 giao dịch trong cơ sở dữ liệu.

!!! Cảnh báo "Đang kiểm tra lại"
    `PerformanceFilter` không hỗ trợ chế độ kiểm tra lại.

####Bộ lọc chính xác

Lọc các đồng tiền có giá trị thấp không cho phép đặt mức dừng lỗ.

Cụ thể, các cặp bị đưa vào danh sách đen nếu chênh lệch từ một phần trăm trở lên trong giá dừng là do làm tròn chính xác trên sàn giao dịch, tức là `làm tròn(stop_price) <= làm tròn(stop_price * 0,99)`. Ý tưởng là tránh các đồng tiền có giá trị RẤT gần với ranh giới giao dịch thấp hơn của chúng, không cho phép thiết lập mức dừng lỗ thích hợp.

!!! Mẹo "PrecisionFilter là vô nghĩa đối với giao dịch tương lai"
    Những điều trên không áp dụng cho quần short. Và trong thời gian dài, về lý thuyết, giao dịch sẽ được thanh lý trước.

!!! Cảnh báo "Đang kiểm tra lại"
    `PrecisionFilter` không hỗ trợ chế độ kiểm tra ngược bằng nhiều chiến lược.

####Bộ lọc giá

`PriceFilter` cho phép lọc các cặp theo giá. Hiện tại các bộ lọc giá sau được hỗ trợ:* `min_price`
* `max_price`
* `max_value`
* `low_price_ratio`
Cài đặt `min_price` sẽ xóa các cặp có giá thấp hơn giá được chỉ định. Điều này rất hữu ích nếu bạn muốn tránh giao dịch các cặp giá quá thấp.
Tùy chọn này bị tắt theo mặc định và sẽ chỉ áp dụng nếu được đặt thành > 0.

Cài đặt `max_price` sẽ xóa các cặp có giá cao hơn giá được chỉ định. Điều này rất hữu ích nếu bạn chỉ muốn giao dịch các cặp giá thấp.
Tùy chọn này bị tắt theo mặc định và sẽ chỉ áp dụng nếu được đặt thành > 0.

Cài đặt `max_value` sẽ xóa các cặp có thay đổi giá trị tối thiểu cao hơn giá trị được chỉ định.
Điều này rất hữu ích khi sàn giao dịch có giới hạn không cân bằng. Ví dụ: nếu kích thước bước = 1 (vì vậy bạn chỉ có thể mua 1, hoặc 2 hoặc 3 chứ không phải 1,1 xu) - và giá khá cao (như 20\$) vì đồng xu đã tăng mạnh kể từ lần điều chỉnh giới hạn cuối cùng.
Do đó, bạn chỉ có thể mua với giá 20\$ hoặc 40\$ - chứ không thể mua với giá 25\$.
Trên các sàn giao dịch khấu trừ phí từ loại tiền nhận (ví dụ: binance) - điều này có thể dẫn đến số tiền/số tiền có giá trị cao không thể bán được vì số tiền thấp hơn giới hạn một chút.

Cài đặt `tỷ lệ_giá_thấp` sẽ loại bỏ các cặp có mức tăng 1 đơn vị giá (pip) cao hơn tỷ lệ `tỷ lệ_giá_thấp`.
Tùy chọn này bị tắt theo mặc định và sẽ chỉ áp dụng nếu được đặt thành > 0.

Đối với `PriceFilter`, ít nhất một trong các cài đặt `min_price`, `max_price` hoặc `low_price_ratio` của nó phải được áp dụng.

Ví dụ tính toán:

Độ chính xác về giá tối thiểu đối với SHITCOIN/BTC là 8 số thập phân. Nếu giá của nó là 0,00000011 - một bước giá ở trên sẽ là 0,00000012, cao hơn ~ 9% so với giá trị trước đó. Bạn có thể lọc cặp này bằng cách sử dụng PriceFilter với `tỷ lệ_giá_thấp` được đặt thành 0,09 (9%) hoặc với `min_price` được đặt thành 0,00000011 tương ứng.

!!! Cảnh báo “Cặp giá thấp”
    Các cặp giá thấp có "chuyển động 1 pip" cao rất nguy hiểm vì chúng thường kém thanh khoản và cũng có thể không đặt được mức dừng lỗ mong muốn, điều này thường có thể dẫn đến thua lỗ cao do giá cần được làm tròn đến mức giá có thể giao dịch tiếp theo - vì vậy thay vì có mức dừng lỗ là -5%, bạn có thể kết thúc với mức dừng lỗ -9% chỉ do làm tròn giá.

####Bộ lọc ngẫu nhiên

Xáo trộn (ngẫu nhiên) các cặp trong danh sách cặp. Nó có thể được sử dụng để ngăn bot giao dịch một số cặp thường xuyên hơn những cặp khác khi bạn muốn tất cả các cặp được xử lý với mức độ ưu tiên như nhau.

Theo mặc định, ShuffleFilter sẽ xáo trộn các cặp một lần cho mỗi cây nến.
Để xáo trộn trên mỗi lần lặp, hãy đặt `"shuffle_ần số"` thành `"lặp"` thay vì mặc định là `"nến"`.``` json
    {
        "method": "ShuffleFilter", 
        "shuffle_frequency": "candle",
        "seed": 42
    }

```!!! Mẹo
    Bạn có thể đặt giá trị `seed` cho Danh sách cặp này để thu được kết quả có thể lặp lại, điều này có thể hữu ích cho các phiên kiểm tra lại lặp đi lặp lại. Nếu `seed` không được đặt, các cặp sẽ được xáo trộn theo thứ tự ngẫu nhiên không thể lặp lại. ShuffleFilter sẽ tự động phát hiện các mã chạy và chỉ áp dụng `seed` cho các chế độ kiểm tra ngược - nếu giá trị `seed` được đặt.

#### Bộ lọc lây lan

Loại bỏ các cặp có sự khác biệt giữa yêu cầu và giá thầu cao hơn tỷ lệ đã chỉ định, `max_ Spread_ratio` (mặc định là `0,005`).

Ví dụ:

Nếu giá thầu tối đa `DOGE/BTC` là 0,00000026 và giá yêu cầu tối thiểu là 0,00000027, thì tỷ lệ được tính như sau: `1 - giá thầu/bán ~= 0,037` là `> 0,005` và cặp này sẽ bị lọc ra.

#### Bộ lọc ổn định phạm vi

Xóa các cặp trong đó chênh lệch giữa mức thấp nhất thấp nhất và mức cao nhất cao nhất trong `lookback_days` ngày ở dưới `min_rate_of_change` hoặc cao hơn `max_rate_of_change`. Vì đây là bộ lọc yêu cầu dữ liệu bổ sung nên kết quả được lưu vào bộ nhớ đệm cho `refresh_ Period`.

Trong ví dụ dưới đây:
Nếu phạm vi giao dịch trong 10 ngày qua là <1% hoặc >99%, hãy xóa cặp này khỏi danh sách trắng.```json
"pairlists": [
    {
        "method": "RangeStabilityFilter",
        "lookback_days": 10,
        "min_rate_of_change": 0.01,
        "max_rate_of_change": 0.99,
        "refresh_period": 86400
    }
]
```Việc thêm `"sort_direction": "asc"` hoặc `"sort_direction": "desc"` sẽ bật sắp xếp cho danh sách cặp này.

!!! Mẹo
    Bộ lọc này có thể được sử dụng để tự động loại bỏ các cặp tiền ổn định, có phạm vi giao dịch rất thấp và do đó cực kỳ khó giao dịch kiếm lời.
    Ngoài ra, nó cũng có thể được sử dụng để tự động loại bỏ các cặp có phương sai cực cao/thấp trong một khoảng thời gian nhất định.

####Bộ lọc biến độngVolatility is the degree of historical variation of a pairs over time, it is measured by the standard deviation of logarithmic daily returns. Returns are assumed to be normally distributed, although actual distribution might be different. In a normal distribution, 68% of observations fall within one standard deviation and 95% of observations fall within two standard deviations. Assuming a volatility of 0.05 means that the expected returns for 20 out of 30 days is expected to be less than 5% (one standard deviation). Volatility is a positive ratio of the expected deviation of return and can be greater than 1.00. Please refer to the wikipedia definition of [`volatility`](https://en.wikipedia.org/wiki/Volatility_(finance)).
Bộ lọc này sẽ loại bỏ các cặp nếu mức biến động trung bình trong `ngày nhìn lại` là dưới mức `biến động tối thiểu` hoặc cao hơn `biến động tối đa`. Vì đây là bộ lọc yêu cầu dữ liệu bổ sung nên kết quả được lưu vào bộ nhớ đệm cho `refresh_ Period`.

Bộ lọc này có thể được sử dụng để thu hẹp các cặp của bạn ở mức độ biến động nhất định hoặc tránh các cặp có mức độ biến động cao.

Trong ví dụ dưới đây:
Nếu độ biến động trong 10 ngày qua không nằm trong khoảng 0,05-0,50, hãy xóa cặp này khỏi danh sách trắng. Bộ lọc được áp dụng cứ sau 24 giờ.```json
"pairlists": [
    {
        "method": "VolatilityFilter",
        "lookback_days": 10,
        "min_volatility": 0.05,
        "max_volatility": 0.50,
        "refresh_period": 86400
    }
]
```Việc thêm `"sort_direction": "asc"` hoặc `"sort_direction": "desc"` sẽ bật chế độ sắp xếp cho danh sách cặp này.

### Ví dụ đầy đủ về Trình xử lý danh sách cặp

Ví dụ bên dưới liệt kê danh sách đen `BNB/BTC`, sử dụng `VolumePairList` với nội dung `20`, sắp xếp các cặp theo `quoteVolume`, sau đó lọc các cặp bị xóa trong tương lai bằng cách sử dụng [`DelistFilter`](#delistfilter) và [`AgeFilter`](#agefilter) để xóa các cặp được liệt kê cách đây chưa đầy 10 ngày. Sau đó, [`PrecisionFilter`](#precisionfilter) và [`PriceFilter`](#pricefilter) được áp dụng, lọc tất cả nội dung có 1 đơn vị giá > 1%. Sau đó, [`SpreadFilter`](# spreadfilter) và [`VolatilityFilter`](#volatilityfilter) được áp dụng và các cặp cuối cùng được xáo trộn với tập hợp hạt giống ngẫu nhiên thành một giá trị được xác định trước.```json
"exchange": {
    "pair_whitelist": [],
    "pair_blacklist": ["BNB/BTC"]
},
"pairlists": [
    {
        "method": "VolumePairList",
        "number_assets": 20,
        "sort_key": "quoteVolume"
    },
    {
        "method": "DelistFilter",
        "max_days_from_now": 0,
    },
    {"method": "AgeFilter", "min_days_listed": 10},
    {"method": "PrecisionFilter"},
    {"method": "PriceFilter", "low_price_ratio": 0.01},
    {"method": "SpreadFilter", "max_spread_ratio": 0.005},
    {
        "method": "RangeStabilityFilter",
        "lookback_days": 10,
        "min_rate_of_change": 0.01,
        "refresh_period": 86400
    },
    {
        "method": "VolatilityFilter",
        "lookback_days": 10,
        "min_volatility": 0.05,
        "max_volatility": 0.50,
        "refresh_period": 86400
    },
    {"method": "ShuffleFilter", "seed": 42}
],
```