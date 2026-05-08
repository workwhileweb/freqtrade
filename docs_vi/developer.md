<!-- Auto-translated from docs/ by script. Please review technical terms. -->

# Trợ giúp phát triển

Trang này dành cho các nhà phát triển của Freqtrade, những người muốn đóng góp cho cơ sở mã hoặc tài liệu Freqtrade hoặc những người muốn hiểu mã nguồn của ứng dụng họ đang chạy.All contributions, bug reports, bug fixes, documentation improvements, enhancements and ideas are welcome. We [track issues](https://github.com/freqtrade/freqtrade/issues) on [GitHub](https://github.com) and also have a dev channel on [discord](https://discord.gg/p7nuUNVfP7) where you can ask questions.
## Tài liệuDocumentation is available at [https://freqtrade.io](https://www.freqtrade.io/) and needs to be provided with every new feature PR.
Special fields for the documentation (like Note boxes, ...) can be found [here](https://squidfunk.github.io/mkdocs-material/reference/admonitions/).
Để kiểm tra tài liệu cục bộ, hãy sử dụng các lệnh sau.``` bash
pip install -r docs/requirements-docs.txt
mkdocs serve
```Thao tác này sẽ khởi động một máy chủ cục bộ (thường là trên cổng 8000) để bạn có thể xem liệu mọi thứ có giống như bạn mong muốn hay không.

## Thiết lập dành cho nhà phát triển

Để định cấu hình môi trường phát triển, bạn có thể sử dụng [DevContainer](#devcontainer-setup) được cung cấp hoặc sử dụng tập lệnh `setup.sh` và trả lời "y" khi được hỏi "Bạn có muốn cài đặt các phần phụ thuộc cho dev [y/N] không?".
Ngoài ra (ví dụ: nếu hệ thống của bạn không được tập lệnh setup.sh hỗ trợ), hãy làm theo quy trình cài đặt thủ công và chạy `pip3 install -r require-dev.txt` - theo sau là `pip3 install -e .[all]`.

Thao tác này sẽ cài đặt tất cả các công cụ cần thiết để phát triển, bao gồm `pytest`, `ruff`, `mypy` và `coveralls`.

Chạy lệnh sau để cài đặt tập lệnh git hook:``` bash
pre-commit install
```Các tập lệnh xác nhận trước này tự động kiểm tra các thay đổi của bạn trước mỗi lần xác nhận.  
Nếu tìm thấy bất kỳ vấn đề định dạng nào, cam kết sẽ không thành công và sẽ nhắc sửa lỗi.
Điều này làm giảm các lỗi CI không cần thiết, giảm gánh nặng bảo trì và cải thiện chất lượng mã.

Bạn có thể chạy kiểm tra theo cách thủ công khi cần thiết với `pre-commit run -a`.Before opening a pull request, please also familiarize yourself with our [Contributing Guidelines](https://github.com/freqtrade/freqtrade/blob/develop/CONTRIBUTING.md).
### Thiết lập DevcontainerThe fastest and easiest way to get started is to use [VSCode](https://code.visualstudio.com/) with the Remote container extension.
Điều này mang lại cho các nhà phát triển khả năng khởi động bot với tất cả các phần phụ thuộc bắt buộc *mà không* cần cài đặt bất kỳ phần phụ thuộc cụ thể nào của freqtrade trên máy cục bộ của bạn.

#### Phần phụ thuộc của Devcontainer* [VSCode](https://code.visualstudio.com/)
* [docker](https://docs.docker.com/install/)
* [Remote container extension documentation](https://code.visualstudio.com/docs/remote)
For more information about the [Remote container extension](https://code.visualstudio.com/docs/remote), best consult the documentation.
### Kiểm tra

Mã mới phải được bao phủ bởi các bài kiểm tra đơn vị cơ bản. Tùy thuộc vào mức độ phức tạp của tính năng, Người đánh giá có thể yêu cầu các bài kiểm tra chi tiết hơn.
Nếu cần, nhóm Freqtrade có thể hỗ trợ và hướng dẫn cách viết bài kiểm tra tốt (tuy nhiên, đừng mong đợi bất kỳ ai viết bài kiểm tra cho bạn).

#### Cách chạy thử nghiệm

Sử dụng `pytest` trong thư mục gốc để chạy tất cả các trường hợp kiểm thử có sẵn và xác nhận môi trường cục bộ của bạn được thiết lập chính xác

!!! Lưu ý "nhánh tính năng"
    Các thử nghiệm dự kiến sẽ vượt qua nhánh `phát triển` và `ổn định`. Các chi nhánh khác có thể đang được tiến hành và các thử nghiệm chưa hoạt động.

#### Kiểm tra nội dung nhật ký trong các bài kiểm tra

Freqtrade sử dụng 2 phương pháp chính để kiểm tra nội dung nhật ký trong các thử nghiệm là `log_has()` và `log_has_re()` (để kiểm tra bằng biểu thức chính quy, trong trường hợp thông báo nhật ký động).
Những thứ này có sẵn từ `conftest.py` và có thể được nhập vào bất kỳ mô-đun thử nghiệm nào.

Một kiểm tra mẫu trông như sau:``` python
from tests.conftest import log_has, log_has_re

def test_method_to_test(caplog):
    method_to_test()

    assert log_has("This event happened", caplog)
    # Check regex with trailing number ...
    assert log_has_re(r"This dynamic event happened and produced \d+", caplog)

```### Cấu hình gỡ lỗi

Để gỡ lỗi freqtrade, chúng tôi khuyên dùng VSCode (với phần mở rộng Python) với cấu hình khởi chạy sau (nằm trong `.vscode/launch.json`).
Thông tin chi tiết rõ ràng sẽ khác nhau giữa các thiết lập - nhưng điều này sẽ hữu ích để giúp bạn bắt đầu.``` json
{
    "name": "freqtrade trade",
    "type": "debugpy",
    "request": "launch",
    "module": "freqtrade",
    "console": "integratedTerminal",
    "args": [
        "trade",
        // Optional:
        // "--userdir", "user_data",
        "--strategy", 
        "MyAwesomeStrategy",
    ]
},
```Đối số dòng lệnh có thể được thêm vào trong mảng `"args"`.
Phương pháp này cũng có thể được sử dụng để gỡ lỗi một chiến lược bằng cách đặt các điểm dừng trong chiến lược.

Một thiết lập tương tự cũng có thể được thực hiện cho Pycharm - sử dụng `freqtrade` làm tên mô-đun và đặt các đối số dòng lệnh làm "tham số".

??? Mẹo "Sử dụng venv đúng"
    Khi sử dụng môi trường ảo (bạn nên làm như vậy), hãy đảm bảo rằng Trình chỉnh sửa của bạn đang sử dụng đúng môi trường ảo để tránh sự cố hoặc lỗi "nhập không xác định".

    ####Vscode

    Bạn có thể chọn môi trường chính xác trong VSCode bằng lệnh "Python: Select Interpreter" - lệnh này sẽ hiển thị cho bạn các môi trường mà tiện ích mở rộng được phát hiện.
    Nếu môi trường của bạn chưa được phát hiện, bạn cũng có thể chọn đường dẫn theo cách thủ công.

    #### Pycharm

    Trong pycharm, bạn có thể chọn Môi trường thích hợp trong cửa sổ "Chạy/Gỡ lỗi".
    ![Cấu hình gỡ lỗi Pycharm](assets/pycharm_debug.png)

!!! Lưu ý "Thư mục khởi động"
    Điều này giả định rằng bạn đã kiểm tra kho lưu trữ và trình soạn thảo được khởi động ở cấp gốc của kho lưu trữ (vì vậy pyproject.toml ở cấp cao nhất của kho lưu trữ của bạn).

##Xử lý lỗi

Tất cả các ngoại lệ Freqtrade đều kế thừa từ `FreqtradeException`.
Tuy nhiên, loại lỗi chung này không nên được sử dụng trực tiếp. Thay vào đó, tồn tại nhiều Ngoại lệ phụ chuyên biệt.

Dưới đây là phác thảo về hệ thống phân cấp kế thừa ngoại lệ:```
+ FreqtradeException
|
+---+ OperationalException
|   |
|   +---+ ConfigurationError
|
+---+ DependencyException
|   |
|   +---+ PricingError
|   |
|   +---+ ExchangeError
|       |
|       +---+ TemporaryError
|       |
|       +---+ DDosProtection
|       |
|       +---+ InvalidOrderException
|           |
|           +---+ RetryableOrderError
|           |
|           +---+ InsufficientFundsError
|
+---+ StrategyError
```---

## Plugin

### Danh sách cặp

Bạn có ý tưởng hay về thuật toán chọn cặp mới mà bạn muốn thử? Tuyệt vời.
Hy vọng bạn cũng muốn đóng góp điều này ngược dòng.

Dù động lực của bạn là gì - Điều này sẽ giúp bạn bắt đầu cố gắng phát triển Trình xử lý danh sách cặp mới.First of all, have a look at the [VolumePairList](https://github.com/freqtrade/freqtrade/blob/develop/freqtrade/plugins/pairlist/VolumePairList.py) Handler, and best copy this file with a name of your new Pairlist Handler.
Đây là một Trình xử lý đơn giản, tuy nhiên đây là một ví dụ điển hình về cách bắt đầu phát triển.

Tiếp theo, sửa đổi tên lớp của Trình xử lý (lý tưởng nhất là căn chỉnh tên này với tên tệp mô-đun).

Lớp cơ sở cung cấp một phiên bản của trao đổi (`self._exchange`), trình quản lý danh sách cặp (`self._pairlistmanager`), cũng như cấu hình chính (`self._config`), cấu hình dành riêng cho danh sách cặp (`self._pairlistconfig`) và vị trí tuyệt đối trong danh sách danh sách cặp.```python
        self._exchange = exchange
        self._pairlistmanager = pairlistmanager
        self._config = config
        self._pairlistconfig = pairlistconfig
        self._pairlist_pos = pairlist_pos
```!!! Mẹo
    Đừng quên đăng ký danh sách cặp của bạn trong `constants.py` dưới biến `AVAILABLE_PAIRLISTS` - nếu không nó sẽ không thể chọn được.

Bây giờ, hãy xem qua các phương pháp yêu cầu hành động:

#### Cấu hình danh sách cặp

Việc cấu hình cho chuỗi Trình xử lý danh sách cặp được thực hiện trong tệp cấu hình bot trong phần tử `"pairlists"`, một mảng các tham số cấu hình cho mỗi Trình xử lý danh sách cặp trong chuỗi.

Theo quy ước, `"number_assets"` được sử dụng để chỉ định số lượng cặp tối đa cần giữ trong danh sách cặp. Hãy làm theo điều này để đảm bảo trải nghiệm người dùng nhất quán.

Các thông số bổ sung có thể được cấu hình khi cần thiết. Ví dụ: `VolumePairList` sử dụng `"sort_key"` để chỉ định giá trị sắp xếp - tuy nhiên, bạn có thể thoải mái chỉ định bất cứ điều gì cần thiết để thuật toán tuyệt vời của bạn thành công và năng động.

#### short_desc

Trả về mô tả được sử dụng cho tin nhắn Telegram.

Phần này phải chứa tên của Trình xử lý danh sách cặp cũng như một mô tả ngắn chứa số lượng nội dung. Vui lòng làm theo định dạng `"PairlistName - cặp X trên/dưới"`.

#### danh sách cặp gen

Ghi đè phương thức này nếu Trình xử lý danh sách cặp có thể được sử dụng làm Trình xử lý danh sách cặp hàng đầu trong chuỗi, xác định danh sách cặp ban đầu, sau đó được xử lý bởi tất cả Trình xử lý danh sách cặp trong chuỗi. Ví dụ là `StaticPairList` và `VolumePairList`.

Điều này được gọi với mỗi lần lặp lại của bot (chỉ khi Trình xử lý danh sách cặp ở vị trí đầu tiên) - vì vậy hãy xem xét triển khai bộ nhớ đệm cho các phép tính nặng về điện toán/mạng.

Nó phải trả về danh sách cặp kết quả (sau đó có thể được chuyển vào chuỗi Trình xử lý danh sách cặp).

Việc xác thực là tùy chọn, lớp cha sẽ hiển thị `verify_blacklist(pairlist)` và `_whitelist_for_active_markets(pairlist)` để thực hiện lọc mặc định. Sử dụng điều này nếu bạn giới hạn kết quả của mình ở một số cặp nhất định - để kết quả cuối cùng không ngắn hơn mong đợi.

#### danh sách cặp lọc

Phương thức này được người quản lý danh sách cặp gọi cho mỗi Trình xử lý danh sách cặp trong chuỗi.

Điều này được gọi với mỗi lần lặp lại của bot - vì vậy hãy xem xét triển khai bộ nhớ đệm cho các phép tính nặng về điện toán/mạng.

Nó được chuyển qua một danh sách cặp (có thể là kết quả của các danh sách cặp trước đó) cũng như `tickers`, một phiên bản được tìm nạp trước của `get_tickers()`.

Việc triển khai mặc định trong lớp cơ sở chỉ đơn giản gọi phương thức `_validate_pair()` cho mỗi cặp trong danh sách cặp, nhưng bạn có thể ghi đè lên nó. Vì vậy, bạn nên triển khai `_validate_pair()` trong Trình xử lý danh sách cặp của mình hoặc ghi đè `filter_pairlist()` để làm việc khác.

Nếu bị ghi đè, nó phải trả về danh sách cặp kết quả (sau đó có thể được chuyển vào Trình xử lý danh sách cặp tiếp theo trong chuỗi).

Việc xác thực là tùy chọn, lớp cha hiển thị `verify_blacklist(pairlist)` và `_whitelist_for_active_markets(pairlist)` để thực hiện các bộ lọc mặc định. Sử dụng điều này nếu bạn giới hạn kết quả của mình ở một số cặp nhất định - để kết quả cuối cùng không ngắn hơn mong đợi.

Trong `VolumePairList`, điều này thực hiện các phương pháp sắp xếp khác nhau, xác thực sớm nên chỉ trả về số lượng cặp dự kiến.

##### vật mẫu``` python
    def filter_pairlist(self, pairlist: list[str], tickers: dict) -> List[str]:
        # Generate dynamic whitelist
        pairs = self._calculate_pairlist(pairlist, tickers)
        return pairs
```### Bảo vệ

Tốt nhất hãy đọc [Tài liệu bảo vệ](plugins.md#protections) để hiểu các biện pháp bảo vệ.
Hướng dẫn này hướng tới các Nhà phát triển muốn phát triển một biện pháp bảo vệ mới.

Không có biện pháp bảo vệ nào nên sử dụng trực tiếp datetime nhưng hãy sử dụng biến `date_now` được cung cấp để tính toán ngày. Điều này duy trì khả năng kiểm tra lại các biện pháp bảo vệ.

!!! Mẹo "Viết một biện pháp bảo vệ mới"
    Tốt nhất hãy sao chép một trong các Biện pháp bảo vệ hiện có để làm ví dụ điển hình.

#### Triển khai biện pháp bảo vệ mới

Tất cả các hoạt động triển khai Bảo vệ phải có `IPotection` làm lớp cha.
Vì lý do đó, họ phải thực hiện các phương pháp sau:* `short_desc()`
* `global_stop()`
* `stop_per_pair()`.

`global_stop()` và `stop_per_pair()` phải trả về một đối tượng ProtectionReturn, bao gồm:

* cặp khóa - boolean
* khóa cho đến khi - datetime - cho đến khi nào cặp tiền sẽ bị khóa (sẽ được làm tròn đến cây nến mới tiếp theo)
* lý do - chuỗi, được sử dụng để ghi và lưu trữ trong cơ sở dữ liệu
* lock_side - dài, ngắn hoặc '*'.

Phần `until` phải được tính bằng phương thức `feature_lock_end()` được cung cấp.

Tất cả Biện pháp bảo vệ phải sử dụng `"stop_duration"` / `"stop_duration_candles"` để xác định thời gian khóa một cặp (hoặc tất cả các cặp).
Nội dung này được cung cấp dưới dạng `self._stop_duration` cho mỗi Biện pháp bảo vệ.

Nếu biện pháp bảo vệ của bạn yêu cầu khoảng thời gian xem lại, vui lòng sử dụng `"lookback_ Period"` / `"lockback_ Period_candles"` để giữ cho tất cả các biện pháp bảo vệ được căn chỉnh.

#### Điểm dừng toàn cầu và điểm dừng cục bộ

Các biện pháp bảo vệ có thể có 2 cách khác nhau để ngừng giao dịch trong thời gian giới hạn :

* Mỗi cặp (cục bộ)
* Dành cho tất cả các cặp (toàn cầu)

##### Bảo vệ - mỗi cặp

Các biện pháp bảo vệ triển khai phương pháp tiếp cận theo cặp phải đặt `has_local_stop=True`.
Phương thức `stop_per_pair()` sẽ được gọi bất cứ khi nào giao dịch đóng (lệnh thoát đã hoàn tất).

##### Protections - bảo vệ toàn cầu

Các Biện pháp bảo vệ này sẽ thực hiện đánh giá trên tất cả các cặp và do đó cũng sẽ khóa tất cả các cặp khỏi giao dịch (được gọi là PairLock toàn cầu).
Bảo vệ toàn cầu phải đặt `has_global_stop=True` để được đánh giá cho các điểm dừng chung.
Phương thức `global_stop()` sẽ được gọi bất cứ khi nào giao dịch đóng (lệnh thoát đã hoàn tất).

##### Bảo vệ - tính toán thời gian kết thúc khóa

Các biện pháp bảo vệ nên tính toán thời gian kết thúc khóa dựa trên giao dịch cuối cùng mà nó xem xét.
Điều này tránh việc khóa lại nếu thời gian xem lại dài hơn thời gian khóa thực tế.

Lớp cha `IProtection` cung cấp một phương thức trợ giúp cho việc này trong `calcate_lock_end()`.

---

## Triển khai Exchange mới (WIP)

!!! Lưu ý
    Phần này là Công việc đang tiến triển và không phải là hướng dẫn đầy đủ về cách thử nghiệm một sàn giao dịch mới với Freqtrade.

!!! Lưu ý
    Đảm bảo sử dụng phiên bản cập nhật của CCXT trước khi chạy bất kỳ thử nghiệm nào dưới đây.
    Bạn có thể tải phiên bản ccxt mới nhất bằng cách chạy `pip install -U ccxt` với môi trường ảo được kích hoạt.
    Docker gốc không được hỗ trợ cho các thử nghiệm này, tuy nhiên, dev-container có sẵn sẽ hỗ trợ tất cả các hành động bắt buộc và cuối cùng là những thay đổi cần thiết.

Hầu hết các sàn giao dịch được CCXT hỗ trợ đều hoạt động tốt.

Nếu bạn cần triển khai một lớp trao đổi cụ thể, chúng sẽ được tìm thấy trong thư mục nguồn `freqtrade/exchange`. Bạn cũng cần thêm nội dung nhập vào `freqtrade/exchange/__init__.py` để logic tải nhận biết được sàn giao dịch mới.  
Chúng tôi khuyên bạn nên xem xét việc triển khai sàn giao dịch hiện tại để biết những gì có thể được yêu cầu.

!!! Cảnh báo
    Việc triển khai và thử nghiệm một sàn giao dịch có thể có rất nhiều thử nghiệm và sai sót, vì vậy hãy ghi nhớ điều này.
    Bạn cũng nên có một số kinh nghiệm phát triển vì đây không phải là nhiệm vụ dành cho người mới bắt đầu.

Để nhanh chóng kiểm tra các điểm cuối công khai của một sàn giao dịch, hãy thêm cấu hình cho sàn giao dịch của bạn vào `tests/exchange_online/conftest.py` và chạy các thử nghiệm này với `pytest --longrun test/exchange_online/test_ccxt_compat.py`.
Việc hoàn thành thành công các thử nghiệm này là một điểm cơ bản tốt (thực tế đó là một yêu cầu), tuy nhiên, những thử nghiệm này sẽ không đảm bảo chức năng trao đổi chính xác, vì điều này chỉ kiểm tra các điểm cuối công khai chứ không có điểm cuối riêng tư (như tạo đơn hàng hoặc tương tự).Ngoài ra, hãy thử sử dụng `freqtrade download-data` trong khoảng thời gian kéo dài (nhiều tháng) và xác minh rằng dữ liệu được tải xuống chính xác (không có lỗ hổng, khoảng thời gian được chỉ định đã thực sự được tải xuống).

Đây là những điều kiện tiên quyết để sàn giao dịch được liệt kê là Được hỗ trợ hoặc Cộng đồng đã thử nghiệm (được liệt kê trên trang chủ).
Dưới đây là những "tính năng bổ sung", sẽ giúp việc trao đổi tốt hơn (hoàn thiện tính năng) - nhưng không thực sự cần thiết đối với một trong 2 danh mục.

Các bài kiểm tra/bước bổ sung cần hoàn thành:

* Xác minh dữ liệu do `fetch_ohlcv()` cung cấp - và cuối cùng điều chỉnh `ohlcv_candle_limit` cho trao đổi này
* Kiểm tra phạm vi giới hạn sổ đặt hàng L2 (tài liệu API) - và cuối cùng được đặt khi cần thiết
* Kiểm tra xem số dư có hiển thị chính xác không (*)
* Tạo lệnh thị trường (*)
* Tạo lệnh giới hạn (*)
* Hủy đơn hàng (*)
* Hoàn tất giao dịch (nhập + thoát) (*)
  * So sánh kết quả tính toán giữa trao đổi và bot
  * Đảm bảo phí được áp dụng chính xác (kiểm tra cơ sở dữ liệu so với sàn giao dịch)

(*) Yêu cầu khóa API và Số dư trên sàn giao dịch.

### Dừng lỗ trên sàn giao dịch

Kiểm tra xem sàn giao dịch mới có hỗ trợ Stoploss trên các lệnh Exchange thông qua API của họ hay không.Since CCXT does not provide unification for Stoploss On Exchange yet, we'll need to implement the exchange-specific parameters ourselves. Best look at `binance.py` for an example implementation of this. You'll need to dig through the documentation of the Exchange's API on how exactly this can be done. [CCXT Issues](https://github.com/ccxt/ccxt/issues) may also provide great help, since others may have implemented something similar for their projects.
### Nến chưa hoàn thiện

Trong khi tìm nạp dữ liệu nến (OHLCV), chúng tôi có thể nhận được những cây nến không đầy đủ (tùy thuộc vào sàn giao dịch).
Để chứng minh điều này, chúng tôi sẽ sử dụng nến hàng ngày ("1d"`) để giữ mọi thứ đơn giản.
Chúng tôi truy vấn api (`ct.fetch_ohlcv()`) để biết khung thời gian và xem ngày của mục nhập cuối cùng. Nếu mục này thay đổi hoặc hiển thị ngày của một cây nến "chưa hoàn chỉnh" thì chúng ta nên bỏ mục này vì việc có những cây nến chưa hoàn thiện sẽ có vấn đề vì các chỉ báo cho rằng chỉ những cây nến hoàn chỉnh mới được chuyển đến chúng và sẽ tạo ra nhiều tín hiệu mua sai. Do đó, theo mặc định, chúng tôi sẽ loại bỏ cây nến cuối cùng vì cho rằng nó chưa hoàn chỉnh.

Để kiểm tra cách hoạt động của sàn giao dịch mới, bạn có thể sử dụng đoạn mã sau:``` python
import ccxt
from datetime import datetime, timezone
from freqtrade.data.converter import ohlcv_to_dataframe
ct = ccxt.binance()  # Use the exchange you're testing
timeframe = "1d"
pair = "BTC/USDT"  # Make sure to use a pair that exists on that exchange!
raw = ct.fetch_ohlcv(pair, timeframe=timeframe)

# convert to dataframe
df1 = ohlcv_to_dataframe(raw, timeframe, pair=pair, drop_incomplete=False)

print(df1.tail(1))
print(datetime.now(timezone.utc))
`````` output
                         date      open      high       low     close  volume  
499 2019-06-08 00:00:00+00:00  0.000007  0.000007  0.000007  0.000007   26264344.0  
2019-06-09 12:30:27.873327
```Đầu ra sẽ hiển thị mục nhập cuối cùng từ Exchange cũng như ngày UTC hiện tại.
Nếu ngày hiển thị cùng ngày thì nến cuối cùng có thể được coi là chưa hoàn chỉnh và nên bị loại bỏ (để nguyên cài đặt `"ohlcv_partial_candle"` từ lớp trao đổi không bị ảnh hưởng / Đúng). Nếu không, hãy đặt `"ohlcv_partial_candle"` thành `False` để không làm rơi Nến (hiển thị trong ví dụ trên).
Một cách khác là chạy lệnh này nhiều lần liên tiếp và quan sát xem âm lượng có thay đổi hay không (trong khi ngày vẫn giữ nguyên).

### Cập nhật mức đòn bẩy được lưu trong bộ nhớ đệm của binance

Việc cập nhật các cấp độ đòn bẩy phải được thực hiện thường xuyên - và yêu cầu một tài khoản được xác thực đã kích hoạt hợp đồng tương lai.``` python
import ccxt
import json
from pathlib import Path

exchange = ccxt.binance({
    'apiKey': '<apikey>',
    'secret': '<secret>',
    'options': {'defaultType': 'swap'}
    })
_ = exchange.load_markets()

lev_tiers = exchange.fetch_leverage_tiers()

# Assumes this is running in the root of the repository.
file = Path('freqtrade/exchange/binance_leverage_tiers.json')
json.dump(dict(sorted(lev_tiers.items())), file.open('w'), indent=2)

```Sau đó, tệp này sẽ được đóng góp ngược dòng để những người khác cũng có thể hưởng lợi từ việc này.

## Cập nhật sổ ghi chép mẫu

Để giữ cho sổ ghi chép jupyter được căn chỉnh với tài liệu, nên chạy phần sau sau khi cập nhật sổ ghi chép mẫu.``` bash
jupyter nbconvert --ClearOutputPreprocessor.enabled=True --inplace freqtrade/templates/strategy_analysis_example.ipynb
jupyter nbconvert --ClearOutputPreprocessor.enabled=True --to markdown freqtrade/templates/strategy_analysis_example.ipynb --stdout > docs/strategy_analysis_example.md
```## Kết quả tài liệu Backtest

Để tạo đầu ra backtest, vui lòng sử dụng các lệnh sau:``` bash
# Assume a dedicated user directory for this output
freqtrade create-userdir --userdir user_data_bttest/
# set can_short = True
sed -i "s/can_short: bool = False/can_short: bool = True/" user_data_bttest/strategies/sample_strategy.py

freqtrade download-data --timerange 20250625-20250801 --config tests/testdata/config.tests.usdt.json --userdir user_data_bttest/ -t 5m

freqtrade backtesting --config tests/testdata/config.tests.usdt.json -s SampleStrategy --userdir user_data_bttest/ --cache none --timerange 20250701-20250801
```## Tích hợp liên tục

Tài liệu này ghi lại một số quyết định được thực hiện cho Đường ống CI.

* CI chạy trên tất cả các biến thể hệ điều hành, Linux (ubuntu), macOS và Windows.
* Hình ảnh Docker được xây dựng cho các nhánh `ổn định` và `phát triển` và được xây dựng dưới dạng bản dựng đa nền tảng, hỗ trợ nhiều nền tảng thông qua cùng một thẻ.
* Hình ảnh Docker chứa phần phụ thuộc của Plot cũng có sẵn dưới dạng `stable_plot` và `develop_plot`.
* Hình ảnh Docker chứa một tệp, `/freqtrade/freqtrade_commit` chứa cam kết mà hình ảnh này dựa trên.
* Việc xây dựng lại hình ảnh docker đầy đủ được thực hiện mỗi tuần một lần theo lịch trình.
* Triển khai chạy trên Ubuntu.
* Tất cả các bài kiểm tra phải vượt qua để PR được hợp nhất thành `ổn định` hoặc `phát triển`.

## Tạo bản phát hành

Phần tài liệu này nhằm vào người bảo trì và chỉ ra cách tạo bản phát hành.

### Tạo nhánh phát hành

!!! Lưu ý
    Hãy đảm bảo rằng nhánh `ổn định` được cập nhật!

Trước tiên, hãy chọn một cam kết cách đây khoảng một tuần (không bao gồm các bổ sung mới nhất cho bản phát hành).``` bash
# create new branch
git checkout -b new_release <commitid>
```Xác định xem các sửa lỗi quan trọng có được thực hiện giữa cam kết này và trạng thái hiện tại hay không và cuối cùng chọn những lỗi này.

* Hợp nhất nhánh phát hành (ổn định) vào nhánh này.
* Chỉnh sửa `freqtrade/__init__.py` và thêm phiên bản khớp với ngày hiện tại (ví dụ `2025.7` cho tháng 7 năm 2025). Các phiên bản nhỏ có thể là `2025.7.1` nếu chúng tôi cần phát hành bản phát hành thứ hai vào tháng đó. Số phiên bản phải tuân theo các phiên bản được phép từ PEP0440 để tránh lỗi khi đẩy sang pypi.
* Cam kết phần này.
* Đẩy nhánh đó vào điều khiển từ xa và tạo PR đối với **nhánh ổn định**.
* Cập nhật phiên bản phát triển lên phiên bản tiếp theo theo mẫu `2025.8-dev`.

### Tạo nhật ký thay đổi từ các cam kết git``` bash
# Needs to be done before merging / pulling that branch.
git log --oneline --no-decorate --no-merges stable..new_release
```Để giữ nhật ký phát hành ngắn gọn, tốt nhất hãy gói toàn bộ nhật ký thay đổi git vào phần chi tiết có thể thu gọn.```markdown
<details>
<summary>Expand full changelog</summary>

... Full git changelog

</details>
```### Phát hành FreqUI

Nếu FreqUI đã được cập nhật đáng kể, hãy đảm bảo tạo bản phát hành trước khi hợp nhất nhánh phát hành.
Đảm bảo rằng freqUI CI trên bản phát hành đã hoàn tất và được thông qua trước khi hợp nhất bản phát hành.

### Tạo bản phát hành/thẻ github

Khi PR chống ổn định được hợp nhất (tốt nhất ngay sau khi hợp nhất):

* Sử dụng nút "Dự thảo bản phát hành mới" trong Giao diện người dùng Github (bản phát hành phần phụ).
* Sử dụng số phiên bản được chỉ định làm thẻ.
* Sử dụng "ổn định" làm tham chiếu (bước này diễn ra sau khi hợp nhất PR ở trên).
* Sử dụng nhật ký thay đổi ở trên làm nhận xét phát hành (dưới dạng khối mã).
* Sử dụng đoạn mã dưới đây cho bản phát hành mới

??? Mẹo "Mẫu phát hành"````
    --8<-- "includes/release_template.md"
    ````

## Phát hành

### pypi

!!! Cảnh báo "Phát hành thủ công"
    Quá trình này được tự động hóa như một phần của Github Actions.  
    Đẩy pypi thủ công không cần thiết.

??? ví dụ "Phát hành thủ công"
    Để tạo bản phát hành pypi theo cách thủ công, vui lòng chạy các lệnh sau:

    Yêu cầu bổ sung: `wheel`, `twine` (để tải lên), tài khoản trên pypi với quyền thích hợp.``` bash
    pip install -U build
    python -m build --sdist --wheel

    # For pypi test (to check if some change to the installation did work)
    twine upload --repository-url https://test.pypi.org/legacy/ dist/*

    # For production:
    twine upload dist/*
    ```Vui lòng không đẩy các bản không phát hành sang phiên bản pypi thực tế/hiệu quả.