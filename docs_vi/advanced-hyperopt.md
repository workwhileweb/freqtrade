<!-- Auto-translated from docs/ by script. Please review technical terms. -->

# Hyperopt nâng cao

Trang này giải thích một số chủ đề Hyperopt nâng cao có thể yêu cầu cao hơn
kỹ năng mã hóa và kiến thức Python hơn là tạo ra sự tối ưu hóa thứ tự
lớp học.

## Tạo và sử dụng hàm mất tùy chỉnh

Để sử dụng lớp hàm mất tùy chỉnh, hãy đảm bảo rằng hàm `hyperopt_loss_function` được xác định trong lớp mất hyperopt tùy chỉnh của bạn.
Đối với mẫu bên dưới, bạn cần thêm tham số dòng lệnh `--hyperopt-loss SuperDuperHyperOptLoss` vào lệnh gọi hyperopt của mình để chức năng này được sử dụng.A sample of this can be found below, which is identical to the Default Hyperopt loss implementation. A full sample can be found in [userdata/hyperopts](https://github.com/freqtrade/freqtrade/blob/develop/freqtrade/templates/sample_hyperopt_loss.py).
``` python
from datetime import datetime
from typing import Any, Dict

from pandas import DataFrame

from freqtrade.constants import Config
from freqtrade.optimize.hyperopt import IHyperOptLoss

TARGET_TRADES = 600
EXPECTED_MAX_PROFIT = 3.0
MAX_ACCEPTED_TRADE_DURATION = 300

class SuperDuperHyperOptLoss(IHyperOptLoss):
    """
    Defines the default loss function for hyperopt
    """

    @staticmethod
    def hyperopt_loss_function(
        *,
        results: DataFrame,
        trade_count: int,
        min_date: datetime,
        max_date: datetime,
        config: Config,
        processed: dict[str, DataFrame],
        backtest_stats: dict[str, Any],
        starting_balance: float,
        **kwargs,
    ) -> float:
        """
        Objective function, returns smaller number for better results
        This is the legacy algorithm (used until now in freqtrade).
        Weights are distributed as follows:
        * 0.4 to trade duration
        * 0.25: Avoiding trade loss
        * 1.0 to total profit, compared to the expected value (`EXPECTED_MAX_PROFIT`) defined above
        """
        total_profit = results['profit_ratio'].sum()
        trade_duration = results['trade_duration'].mean()

        trade_loss = 1 - 0.25 * exp(-(trade_count - TARGET_TRADES) ** 2 / 10 ** 5.8)
        profit_loss = max(0, 1 - total_profit / EXPECTED_MAX_PROFIT)
        duration_loss = 0.4 * min(trade_duration / MAX_ACCEPTED_TRADE_DURATION, 1)
        result = trade_loss + profit_loss + duration_loss
        return result
```Hiện tại, các đối số là:

* `kết quả`: DataFrame chứa các giao dịch kết quả.
    Các cột sau đây có sẵn trong kết quả (tương ứng với tệp đầu ra của việc kiểm tra ngược khi được sử dụng với `--export giao dịch`):  
    `cặp, tỷ lệ lợi nhuận, lợi nhuận_abs, ngày mở, tỷ lệ mở, phí_mở, ngày đóng, tỷ lệ đóng, phí_đóng, số tiền, thời gian giao dịch, is_open, exit_reason, stake_amount, min_rate, max_rate, stop_loss_ratio, stop_loss_abs`
* `trade_count`: Số lượng giao dịch (giống với `len(results)`)
* `min_date`: Ngày bắt đầu của khoảng thời gian được sử dụng
* `min_date`: Ngày kết thúc của khoảng thời gian được sử dụng
* `config`: Đối tượng cấu hình được sử dụng (Lưu ý: Không phải tất cả các tham số liên quan đến chiến lược sẽ được cập nhật tại đây nếu chúng là một phần của không gian hyperopt).
* `processed`: Dict of Dataframes với cặp là khóa chứa dữ liệu được sử dụng để kiểm tra ngược.
* `backtest_stats`: Kiểm tra lại số liệu thống kê sử dụng cùng định dạng với cấu trúc con "chiến lược" của tệp kiểm tra lại. Bạn có thể xem các trường có sẵn trong `generate_strategy_stats()` trong `optimize_reports.py`.
* `starting_balance`: Số dư ban đầu được sử dụng để kiểm tra lại.

Hàm này cần trả về một số dấu phẩy động (`float`). Những con số nhỏ hơn sẽ được hiểu là kết quả tốt hơn. Các thông số và sự cân bằng cho việc này tùy thuộc vào bạn.

!!! Lưu ý
    Hàm này được gọi một lần trong mỗi kỷ nguyên - vì vậy hãy đảm bảo tối ưu hóa hàm này nhất có thể để không làm chậm quá trình tăng tốc một cách không cần thiết.

!!! Lưu ý "`*args` và `**kwargs`"
    Vui lòng giữ nguyên các đối số `*args` và `**kwargs` trong giao diện để cho phép chúng tôi mở rộng giao diện này trong tương lai.

## Ghi đè các khoảng trắng được xác định trước

Để ghi đè một khoảng trắng được xác định trước (`roi_space`, `generate_roi_table`, `stoploss_space`, `trailing_space`, `max_open_trades_space`), hãy xác định một lớp lồng nhau có tên Hyperopt và xác định các khoảng trắng cần thiết như sau:```python
from freqtrade.optimize.space import Categorical, Dimension, Integer, SKDecimal

class MyAwesomeStrategy(IStrategy):
    class HyperOpt:
        # Define a custom stoploss space.
        def stoploss_space():
            return [SKDecimal(-0.05, -0.01, decimals=3, name='stoploss')]

        # Define custom ROI space
        def roi_space() -> List[Dimension]:
            return [
                Integer(10, 120, name='roi_t1'),
                Integer(10, 60, name='roi_t2'),
                Integer(10, 40, name='roi_t3'),
                SKDecimal(0.01, 0.04, decimals=3, name='roi_p1'),
                SKDecimal(0.01, 0.07, decimals=3, name='roi_p2'),
                SKDecimal(0.01, 0.20, decimals=3, name='roi_p3'),
            ]

        def generate_roi_table(params: Dict) -> dict[int, float]:

            roi_table = {}
            roi_table[0] = params['roi_p1'] + params['roi_p2'] + params['roi_p3']
            roi_table[params['roi_t3']] = params['roi_p1'] + params['roi_p2']
            roi_table[params['roi_t3'] + params['roi_t2']] = params['roi_p1']
            roi_table[params['roi_t3'] + params['roi_t2'] + params['roi_t1']] = 0

            return roi_table

        def trailing_space() -> List[Dimension]:
            # All parameters here are mandatory, you can only modify their type or the range.
            return [
                # Fixed to true, if optimizing trailing_stop we assume to use trailing stop at all times.
                Categorical([True], name='trailing_stop'),

                SKDecimal(0.01, 0.35, decimals=3, name='trailing_stop_positive'),
                # 'trailing_stop_positive_offset' should be greater than 'trailing_stop_positive',
                # so this intermediate parameter is used as the value of the difference between
                # them. The value of the 'trailing_stop_positive_offset' is constructed in the
                # generate_trailing_params() method.
                # This is similar to the hyperspace dimensions used for constructing the ROI tables.
                SKDecimal(0.001, 0.1, decimals=3, name='trailing_stop_positive_offset_p1'),

                Categorical([True, False], name='trailing_only_offset_is_reached'),
        ]

        # Define a custom max_open_trades space
        def max_open_trades_space() -> List[Dimension]:
            return [
                Integer(-1, 10, name='max_open_trades'),
            ]
```!!! Lưu ý
    Tất cả các phần ghi đè đều là tùy chọn và có thể được trộn/kết hợp khi cần thiết.

## Tham số động

Các tham số cũng có thể được xác định một cách linh hoạt, nhưng phải có sẵn cho phiên bản sau khi lệnh gọi lại [`bot_start()`](strategy-callbacks.md#bot-start) được gọi.``` python

class MyAwesomeStrategy(IStrategy):

    def bot_start(self, **kwargs) -> None:
        self.buy_adx = IntParameter(20, 30, default=30, optimize=True)

    # ...
```!!! Cảnh báo
    Các tham số được tạo theo cách này sẽ không hiển thị trong số lượng tham số `list-strategies`.

## Ghi đè công cụ ước tính cơ sở

Bạn có thể xác định bộ lấy mẫu optuna của riêng mình cho Hyperopt bằng cách triển khai `generate_estimator()` trong lớp con Hyperopt.```python
class MyAwesomeStrategy(IStrategy):
    class HyperOpt:
        def generate_estimator(dimensions: List['Dimension'], **kwargs):
            return "NSGAIIISampler"

```Possible values are either one of "NSGAIISampler", "TPESampler", "GPSampler", "CmaEsSampler", "NSGAIIISampler", "QMCSampler" (Details can be found in the [optuna-samplers documentation](https://optuna.readthedocs.io/en/stable/reference/samplers/index.html)), or "an instance of a class that inherits from `optuna.samplers.BaseSampler`".
Ví dụ, một số nghiên cứu sẽ cần thiết để tìm các Bộ lấy mẫu bổ sung (từ optunahub).

!!! Lưu ý
    Mặc dù công cụ ước tính tùy chỉnh có thể được cung cấp, nhưng với tư cách là Người dùng, bạn có trách nhiệm nghiên cứu các thông số có thể có và phân tích/hiểu thông số nào nên được sử dụng.
    Nếu bạn không chắc chắn về điều này, tốt nhất hãy sử dụng một trong các Mặc định ("NSGAIIISampler"` đã được chứng minh là linh hoạt nhất) mà không cần thêm tham số.

??? Ví dụ "Sử dụng `AutoSampler` từ Optunahub"    [AutoSampler docs](https://hub.optuna.org/samplers/auto_sampler/)
Cài đặt các phụ thuộc cần thiết``` bash
    pip install optunahub cmaes torch scipy
    ```Triển khai `generate_estimator()` trong chiến lược của bạn``` python
    # ...
    from freqtrade.strategy.interface import IStrategy
    from typing import List
    import optunahub
    # ... 

    class my_strategy(IStrategy):
        class HyperOpt:
            def generate_estimator(dimensions: List["Dimension"], **kwargs):
                if "random_state" in kwargs.keys():
                    return optunahub.load_module("samplers/auto_sampler").AutoSampler(seed=kwargs["random_state"])
                else:
                    return optunahub.load_module("samplers/auto_sampler").AutoSampler()

    ```Rõ ràng cách tiếp cận tương tự sẽ có hiệu quả đối với tất cả các hỗ trợ optuna Samplers khác.

## Tùy chọn không gian

Đối với các không gian bổ sung, tối ưu hóa scikit (kết hợp với Freqtrade) cung cấp các loại không gian sau:

* `Categorical` - Chọn từ danh sách các danh mục (ví dụ: `Categorical(['a', 'b', 'c'], name="cat")`)
* `Số nguyên` - Chọn từ một phạm vi số nguyên (ví dụ: `Số nguyên(1, 10, name='rsi')`)
* `SKDecimal` - Chọn từ một dãy số thập phân có độ chính xác hạn chế (ví dụ: `SKDecimal(0,1, 0,5, số thập phân=3, name='adx')`). *Chỉ có sẵn với freqtrade*.
* `Real` - Chọn từ một dãy số thập phân với độ chính xác hoàn toàn (ví dụ: `Real(0,1, 0,5, name='adx')`

Bạn có thể nhập tất cả những thứ này từ `freqtrade.optimize.space`, mặc dù `Categorical`, `Integer` và `Real` chỉ là bí danh cho các Không gian tối ưu hóa scikit tương ứng của chúng. `SKDecimal` được cung cấp bởi freqtrade để tối ưu hóa nhanh hơn.``` python
from freqtrade.optimize.space import Categorical, Dimension, Integer, SKDecimal, Real  # noqa
```!!! Gợi ý "SKDecimal so với Real"
    Chúng tôi khuyên bạn nên sử dụng `SKDecimal` thay vì khoảng trắng `Real` trong hầu hết các trường hợp. Mặc dù không gian Thực cung cấp độ chính xác đầy đủ (lên tới ~16 chữ số thập phân) - nhưng độ chính xác này hiếm khi cần thiết và dẫn đến thời gian tăng cường kéo dài không cần thiết.

    Giả sử định nghĩa một không gian khá nhỏ (`SKDecimal(0.10, 0.15, số thập phân=2, name='xxx')`) - SKDecimal sẽ có 5 khả năng (`[0.10, 0.11, 0.12, 0.13, 0.14, 0.15]`).

    Mặt khác, một không gian thực tương ứng `Real(0,10, 0,15 name='xxx')` có số lượng khả năng gần như không giới hạn (`[0,10, 0,010000000001, 0,010000000002, ... 0,0149999999999, 0,01500000000]`).