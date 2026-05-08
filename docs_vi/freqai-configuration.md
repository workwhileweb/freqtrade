<!-- Auto-translated from docs/ by script. Please review technical terms. -->

# Cấu hình

FreqAI được định cấu hình thông qua [tệp cấu hình Freqtrade](configuration.md) điển hình và [Chiến lược Freqtrade](strategy-customization.md) tiêu chuẩn. Bạn có thể tìm thấy ví dụ về các tệp chiến lược và cấu hình FreqAI lần lượt trong `config_examples/config_freqai.example.json` và `freqtrade/templates/FreqaiExampleStrategy.py`.

## Thiết lập file cấu hình

 Mặc dù có rất nhiều tham số bổ sung để lựa chọn, như được đánh dấu trong [bảng tham số](freqai-parameter-table.md#parameter-table), cấu hình FreqAI tối thiểu phải bao gồm các tham số sau (giá trị tham số chỉ mang tính ví dụ):```json
    "freqai": {
        "enabled": true,
        "purge_old_models": 2,
        "train_period_days": 30,
        "backtest_period_days": 7,
        "identifier" : "unique-id",
        "feature_parameters" : {
            "include_timeframes": ["5m","15m","4h"],
            "include_corr_pairlist": [
                "ETH/USD",
                "LINK/USD",
                "BNB/USD"
            ],
            "label_period_candles": 24,
            "include_shifted_candles": 2,
            "indicator_periods_candles": [10, 20]
        },
        "data_split_parameters" : {
            "test_size": 0.25
        }
    }
```Cấu hình ví dụ đầy đủ có sẵn trong `config_examples/config_freqai.example.json`.

!!! Lưu ý
    `Mã định danh` thường bị người mới sử dụng bỏ qua, tuy nhiên, giá trị này đóng một vai trò quan trọng trong cấu hình của bạn. Giá trị này là ID duy nhất mà bạn chọn để mô tả một trong các lần chạy của mình. Giữ nguyên cho phép bạn duy trì khả năng phục hồi sau sự cố cũng như kiểm tra lại nhanh hơn. Ngay khi bạn muốn thử lần chạy mới (tính năng mới, mô hình mới, v.v.), bạn nên thay đổi giá trị này (hoặc xóa thư mục `user_data/models/unique-id`. Thông tin chi tiết hơn có trong [bảng tham số](freqai-parameter-table.md#feature-parameters).

## Xây dựng chiến lược FreqAI

Chiến lược FreqAI yêu cầu bao gồm các dòng mã sau trong [Chiến lược Freqtrade](strategy-customization.md) tiêu chuẩn:```python
    # user should define the maximum startup candle count (the largest number of candles
    # passed to any single indicator)
    startup_candle_count: int = 20

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:

        # the model will return all labels created by user in `set_freqai_targets()`
        # (& appended targets), an indication of whether or not the prediction should be accepted,
        # the target mean/std values for each of the labels created by user in
        # `set_freqai_targets()` for each training period.

        dataframe = self.freqai.start(dataframe, metadata, self)

        return dataframe

    def feature_engineering_expand_all(self, dataframe: DataFrame, period, **kwargs) -> DataFrame:
        """
        *Only functional with FreqAI enabled strategies*
        This function will automatically expand the defined features on the config defined
        `indicator_periods_candles`, `include_timeframes`, `include_shifted_candles`, and
        `include_corr_pairs`. In other words, a single feature defined in this function
        will automatically expand to a total of
        `indicator_periods_candles` * `include_timeframes` * `include_shifted_candles` *
        `include_corr_pairs` numbers of features added to the model.

        All features must be prepended with `%` to be recognized by FreqAI internals.

        :param df: strategy dataframe which will receive the features
        :param period: period of the indicator - usage example:
        dataframe["%-ema-period"] = ta.EMA(dataframe, timeperiod=period)
        """

        dataframe["%-rsi-period"] = ta.RSI(dataframe, timeperiod=period)
        dataframe["%-mfi-period"] = ta.MFI(dataframe, timeperiod=period)
        dataframe["%-adx-period"] = ta.ADX(dataframe, timeperiod=period)
        dataframe["%-sma-period"] = ta.SMA(dataframe, timeperiod=period)
        dataframe["%-ema-period"] = ta.EMA(dataframe, timeperiod=period)

        return dataframe

    def feature_engineering_expand_basic(self, dataframe: DataFrame, **kwargs) -> DataFrame:
        """
        *Only functional with FreqAI enabled strategies*
        This function will automatically expand the defined features on the config defined
        `include_timeframes`, `include_shifted_candles`, and `include_corr_pairs`.
        In other words, a single feature defined in this function
        will automatically expand to a total of
        `include_timeframes` * `include_shifted_candles` * `include_corr_pairs`
        numbers of features added to the model.

        Features defined here will *not* be automatically duplicated on user defined
        `indicator_periods_candles`

        All features must be prepended with `%` to be recognized by FreqAI internals.

        :param df: strategy dataframe which will receive the features
        dataframe["%-pct-change"] = dataframe["close"].pct_change()
        dataframe["%-ema-200"] = ta.EMA(dataframe, timeperiod=200)
        """
        dataframe["%-pct-change"] = dataframe["close"].pct_change()
        dataframe["%-raw_volume"] = dataframe["volume"]
        dataframe["%-raw_price"] = dataframe["close"]
        return dataframe

    def feature_engineering_standard(self, dataframe: DataFrame, **kwargs) -> DataFrame:
        """
        *Only functional with FreqAI enabled strategies*
        This optional function will be called once with the dataframe of the base timeframe.
        This is the final function to be called, which means that the dataframe entering this
        function will contain all the features and columns created by all other
        freqai_feature_engineering_* functions.

        This function is a good place to do custom exotic feature extractions (e.g. tsfresh).
        This function is a good place for any feature that should not be auto-expanded upon
        (e.g. day of the week).

        All features must be prepended with `%` to be recognized by FreqAI internals.

        :param df: strategy dataframe which will receive the features
        usage example: dataframe["%-day_of_week"] = (dataframe["date"].dt.dayofweek + 1) / 7
        """
        dataframe["%-day_of_week"] = (dataframe["date"].dt.dayofweek + 1) / 7
        dataframe["%-hour_of_day"] = (dataframe["date"].dt.hour + 1) / 25
        return dataframe

    def set_freqai_targets(self, dataframe: DataFrame, **kwargs) -> DataFrame:
        """
        *Only functional with FreqAI enabled strategies*
        Required function to set the targets for the model.
        All targets must be prepended with `&` to be recognized by the FreqAI internals.

        :param df: strategy dataframe which will receive the targets
        usage example: dataframe["&-target"] = dataframe["close"].shift(-1) / dataframe["close"]
        """
        dataframe["&-s_close"] = (
            dataframe["close"]
            .shift(-self.freqai_info["feature_parameters"]["label_period_candles"])
            .rolling(self.freqai_info["feature_parameters"]["label_period_candles"])
            .mean()
            / dataframe["close"]
            - 1
            )
        return dataframe
```Hãy lưu ý cách `feature_engineering_*()` là nơi [features](freqai-feature-engineering.md#feature-engineering) được thêm vào. Trong khi đó `set_freqai_targets()` thêm nhãn/mục tiêu. Chiến lược ví dụ đầy đủ có sẵn trong `templates/FreqaiExampleStrategy.py`.

!!! Lưu ý
    Không thể gọi hàm `self.freqai.start()` bên ngoài `populate_indicators()`.

!!! Lưu ý
    Các tính năng **phải** được xác định trong `feature_engineering_*()`. Xác định các tính năng FreqAI trong `populate_indicators()`
    sẽ khiến thuật toán thất bại ở chế độ trực tiếp/khô. Để thêm các tính năng tổng quát không liên quan đến một cặp hoặc khung thời gian cụ thể, bạn nên sử dụng `feature_engineering_standard()`
    (như được minh họa trong `freqtrade/templates/FreqaiExampleStrategy.py`).

## Các mẫu khóa khung dữ liệu quan trọng

Dưới đây là các giá trị bạn có thể mong đợi bao gồm/sử dụng bên trong khung dữ liệu chiến lược điển hình (`df[]`):

|  Khóa DataFrame | Mô tả |
|----------||-------------|
| `df['&*']` | Bất kỳ cột khung dữ liệu nào được thêm vào trước `&` trong `set_freqai_targets()` đều được coi là mục tiêu huấn luyện (nhãn) bên trong FreqAI (thường tuân theo quy ước đặt tên `&-s*`). Ví dụ: để dự đoán giá đóng cửa của 40 nến trong tương lai, bạn sẽ đặt `df['&-s_close'] = df['close'].shift(-self.freqai_info["feature_parameters"]["label_ Period_candles"])` với `"label_ Period_candles": 40` trong cấu hình. FreqAI đưa ra các dự đoán và gửi lại chúng dưới cùng một khóa (`df['&-s_close']`) để sử dụng trong `populate_entry/exit_trend()`. <br> **Loại dữ liệu:** Phụ thuộc vào đầu ra của mô hình.
| `df['&*_std/mean']` | Độ lệch chuẩn và giá trị trung bình của các nhãn được xác định trong quá trình đào tạo (hoặc theo dõi trực tiếp với `fit_live_predictions_candles`). Thường được sử dụng để hiểu mức độ hiếm của một dự đoán (sử dụng điểm z như được hiển thị trong `templates/FreqaiExampleStrategy.py` và được giải thích [tại đây](#creating-a-dynamic-target-threshold) để đánh giá tần suất quan sát thấy một dự đoán cụ thể trong quá trình đào tạo hoặc trước đây với `fit_live_predictions_candles`). <br> **Loại dữ liệu:** Phao.| `df['do_predict']` | Chỉ định một điểm dữ liệu ngoại lệ. Giá trị trả về là số nguyên từ -2 đến 2, cho bạn biết dự đoán đó có đáng tin cậy hay không. `do_predict==1` có nghĩa là dự đoán đó đáng tin cậy. Nếu Chỉ số khác biệt (DI, xem chi tiết [tại đây](freqai-feature-engineering.md#identifying-outliers-with-the-dissimilarity-index-di)) của điểm dữ liệu đầu vào cao hơn ngưỡng được xác định trong cấu hình, FreqAI sẽ trừ 1 từ `do_predict`, dẫn đến `do_predict==0`. Nếu `use_SVM_to_remove_outliers` đang hoạt động, Máy vectơ hỗ trợ (SVM, xem chi tiết [tại đây](freqai-feature-engineering.md#identifying-outliers-USE-a-support-vector-machine-svm)) cũng có thể phát hiện các ngoại lệ trong dữ liệu huấn luyện và dự đoán. Trong trường hợp này, SVM cũng sẽ trừ 1 từ `do_predict`. Nếu điểm dữ liệu đầu vào được SVM coi là ngoại lệ chứ không phải bởi DI hoặc ngược lại, thì kết quả sẽ là `do_predict==0`. Nếu cả DI và SVM đều coi điểm dữ liệu đầu vào là ngoại lệ, thì kết quả sẽ là `do_predict==-1`. Giống như SVM, nếu `use_DBSCAN_to_remove_outliers` đang hoạt động, DBSCAN (xem chi tiết [tại đây](freqai-feature-engineering.md#identifying-outliers-with-dbscan)) cũng có thể phát hiện các giá trị ngoại lệ và trừ 1 từ `do_predict`. Do đó, nếu cả SVM và DBSCAN đều đang hoạt động và xác định một điểm dữ liệu nằm trên ngưỡng DI là ngoại lệ, thì kết quả sẽ là `do_predict==-2`. Một trường hợp cụ thể là khi `do_predict == 2`, có nghĩa là mô hình đã hết hạn do vượt quá `expired_hours`. <br> **Loại dữ liệu:** Số nguyên từ -2 đến 2.
| `df['DI_values']` | Các giá trị Chỉ số khác biệt (DI) đại diện cho mức độ tin cậy mà FreqAI có trong dự đoán. DI thấp hơn có nghĩa là dự đoán gần với dữ liệu huấn luyện, tức là độ tin cậy dự đoán cao hơn. Xem thông tin chi tiết về DI [tại đây](freqai-feature-engineering.md#identifying-outliers-with-the-dissimilarity-index-di). <br> **Loại dữ liệu:** Phao.
| `df['%*']` | Bất kỳ cột khung dữ liệu nào được thêm vào trước `%` trong `feature_engineering_*()` đều được coi là một tính năng đào tạo. Ví dụ: bạn có thể đưa RSI vào bộ tính năng đào tạo (tương tự như trong `templates/FreqaiExampleStrategy.py`) bằng cách đặt `df['%-rsi']`. Xem thêm thông tin chi tiết về cách thực hiện việc này [tại đây](freqai-feature-engineering.md). <br> **Lưu ý:** Vì số lượng tính năng được thêm vào trước `%` có thể nhân lên rất nhanh (10 trong số hàng nghìn tính năng được thiết kế dễ dàng bằng cách sử dụng chức năng nhân của, ví dụ: `include_shifted_candles` và `include_timeframes` như được mô tả trong [bảng tham số](freqai-parameter-table.md)), nên các tính năng này sẽ bị xóa khỏi khung dữ liệu được trả về từ FreqAI cho chiến lược. Để giữ một loại đối tượng địa lý cụ thể cho mục đích vẽ đồ thị, bạn sẽ thêm nó bằng `%%` (xem chi tiết bên dưới). <br> **Loại dữ liệu:** Phụ thuộc vào tính năng do người dùng tạo.| `df['%%*']` | Bất kỳ cột khung dữ liệu nào được thêm vào trước `%%` trong `feature_engineering_*()` đều được coi là một tính năng đào tạo, giống như phần thêm vào trước `%` ở trên. Tuy nhiên, trong trường hợp này, các tính năng sẽ được trả về chiến lược vẽ và giám sát FreqUI/plot-dataframe trong Dry/Live/Backtesting <br> **Datatype:** Tùy thuộc vào tính năng do người dùng tạo. Xin lưu ý rằng các tính năng được tạo trong `feature_engineering_expand()` sẽ có giản đồ đặt tên FreqAI tự động tùy thuộc vào phần mở rộng mà bạn đã định cấu hình (ví dụ: `include_timeframes`, `include_corr_pairlist`, `indicators_ Periods_candles`, `include_shifted_candles`). Vì vậy, nếu bạn muốn vẽ đồ thị `%%-rsi` từ `feature_engineering_expand_all()`, sơ đồ đặt tên cuối cùng cho cấu hình đồ thị của bạn sẽ là: `%%-rsi- Period_10_ETH/USDT:USDT_1h` cho tính năng `rsi` với ` Period=10`, `timeframe=1h` và `pair=ETH/USDT:USDT` (`:USDT` được thêm vào nếu bạn đang sử dụng các cặp tương lai). Sẽ rất hữu ích nếu bạn chỉ cần thêm `print(dataframe.columns)` vào `populate_indicators()` sau `self.freqai.start()` để xem danh sách đầy đủ các tính năng có sẵn được trả về chiến lược cho mục đích lập biểu đồ.

## Đặt `startup_candle_count`

`startup_candle_count` trong chiến lược FreqAI cần được thiết lập theo cách tương tự như trong chiến lược Freqtrade tiêu chuẩn (xem chi tiết [tại đây](strategy-customization.md#strategy-startup- Period)). Giá trị này được Freqtrade sử dụng để đảm bảo cung cấp đủ lượng dữ liệu khi gọi `nhà cung cấp dữ liệu`, nhằm tránh bất kỳ NaN nào khi bắt đầu khóa đào tạo đầu tiên. Bạn có thể dễ dàng đặt giá trị này bằng cách xác định khoảng thời gian dài nhất (tính bằng đơn vị nến) được chuyển đến các hàm tạo chỉ báo (ví dụ: hàm TA-Lib). Trong ví dụ được trình bày, `startup_candle_count` là 20 vì đây là giá trị tối đa trong `indicators_ Periods_candles`.

!!! Lưu ý
    Có những trường hợp trong đó các hàm TA-Lib thực sự yêu cầu nhiều dữ liệu hơn chỉ `dấu chấm` đã được truyền, nếu không, tập dữ liệu tính năng sẽ được điền bằng NaN. Thông thường, nhân `startup_candle_count` với 2 luôn dẫn đến một tập dữ liệu đào tạo hoàn toàn miễn phí NaN. Do đó, cách an toàn nhất là nhân `startup_candle_count` dự kiến ​​với 2. Hãy chú ý thông báo nhật ký này để xác nhận rằng dữ liệu sạch:```
    2022-08-31 15:14:04 - freqtrade.freqai.data_kitchen - INFO - dropped 0 training points due to NaNs in populated dataset 4319.
    ```## Tạo ngưỡng mục tiêu động

Việc quyết định thời điểm tham gia hoặc thoát giao dịch có thể được thực hiện một cách năng động để phản ánh các điều kiện thị trường hiện tại. FreqAI cho phép bạn trả về thông tin bổ sung từ quá trình đào tạo mô hình (thông tin thêm [tại đây](freqai-feature-engineering.md#returning-bổ sung-thông tin-từ-đào tạo)). Ví dụ: các giá trị trả về `&*_std/mean` mô tả phân bổ thống kê của mục tiêu/nhãn *trong quá trình đào tạo gần đây nhất*. So sánh một dự đoán nhất định với các giá trị này cho phép bạn biết mức độ hiếm của dự đoán đó. Trong `templates/FreqaiExampleStrategy.py`, `target_roi` và `sell_roi` được xác định là cách giá trị trung bình 1,25 z-score, khiến cho những dự đoán gần với giá trị trung bình hơn sẽ bị lọc ra.```python
dataframe["target_roi"] = dataframe["&-s_close_mean"] + dataframe["&-s_close_std"] * 1.25
dataframe["sell_roi"] = dataframe["&-s_close_mean"] - dataframe["&-s_close_std"] * 1.25
```Để xem xét tập hợp *dự đoán lịch sử* nhằm tạo mục tiêu động thay vì thông tin từ quá trình đào tạo như đã thảo luận ở trên, bạn sẽ đặt `fit_live_predictions_candles` trong cấu hình thành số lượng nến dự đoán lịch sử mà bạn muốn sử dụng để tạo số liệu thống kê mục tiêu.```json
    "freqai": {
        "fit_live_predictions_candles": 300,
    }
```Nếu giá trị này được đặt, FreqAI ban đầu sẽ sử dụng các dự đoán từ dữ liệu huấn luyện và sau đó bắt đầu đưa ra dữ liệu dự đoán thực khi nó được tạo. FreqAI sẽ lưu dữ liệu lịch sử này để tải lại nếu bạn dừng và khởi động lại một mô hình có cùng `mã định danh`.

## Sử dụng các mô hình dự đoán khác nhau

FreqAI có nhiều thư viện mô hình dự đoán mẫu sẵn sàng để sử dụng thông qua cờ `--freqaimodel`. Các thư viện này bao gồm các mô hình hồi quy, phân loại và đa mục tiêu `LightGBM` và `XGBoost` và có thể được tìm thấy trong `freqai/prediction_models/`.

Các mô hình hồi quy và phân loại khác nhau ở mục tiêu mà chúng dự đoán - mô hình hồi quy sẽ dự đoán mục tiêu có giá trị liên tục, ví dụ như giá BTC sẽ như thế nào vào ngày mai, trong khi trình phân loại sẽ dự đoán mục tiêu có các giá trị riêng biệt, chẳng hạn như liệu giá BTC có tăng vào ngày mai hay không. Điều này có nghĩa là bạn phải chỉ định mục tiêu của mình một cách khác nhau tùy thuộc vào loại mô hình bạn đang sử dụng (xem chi tiết [bên dưới](#setting-model-targets)).

Tất cả các thư viện mô hình nói trên đều triển khai thuật toán cây quyết định tăng cường độ dốc. Tất cả đều hoạt động theo nguyên tắc học tập chung, trong đó các dự đoán từ nhiều người học đơn giản được kết hợp để có được dự đoán cuối cùng ổn định và khái quát hơn. Những người học đơn giản trong trường hợp này là cây quyết định. Tăng cường độ dốc đề cập đến phương pháp học, trong đó mỗi học đơn giản được xây dựng theo trình tự - học tiếp theo được sử dụng để cải thiện lỗi của học trước. Nếu muốn tìm hiểu thêm về các thư viện mô hình khác nhau, bạn có thể tìm thông tin trong các tài liệu tương ứng:* LightGBM: <https://lightgbm.readthedocs.io/en/v3.3.2/#>
* XGBoost: <https://xgboost.readthedocs.io/en/stable/#>
* CatBoost: <https://catboost.ai/en/docs/> (No longer actively supported since 2025.12)
There are also numerous online articles describing and comparing the algorithms. Some relatively lightweight examples would be [CatBoost vs. LightGBM vs. XGBoost — Which is the best algorithm?](https://towardsdatascience.com/catboost-vs-lightgbm-vs-xgboost-c80f40662924#:~:text=In%20CatBoost%2C%20symmetric%20trees%2C%20or,the%20same%20depth%20can%20differ.) and [XGBoost, LightGBM or CatBoost — which boosting algorithm should I use?](https://medium.com/riskified-technology/xgboost-lightgbm-or-catboost-which-boosting-algorithm-should-i-use-e7fda7bb36bc). Keep in mind that the performance of each model is highly dependent on the application and so any reported metrics might not be true for your particular use of the model.
Ngoài các mô hình đã có sẵn trong FreqAI, bạn cũng có thể tùy chỉnh và tạo các mô hình dự đoán của riêng mình bằng cách sử dụng lớp `IFreqaiModel`. Bạn được khuyến khích kế thừa `fit()`, `train()` và `predict()` để tùy chỉnh các khía cạnh khác nhau của quy trình đào tạo. Bạn có thể đặt các mô hình FreqAI tùy chỉnh trong `user_data/freqaimodels` - và freqtrade sẽ chọn chúng từ đó dựa trên tên `--freqaimodel` được cung cấp - tên này phải tương ứng với tên lớp của mô hình tùy chỉnh của bạn.
Đảm bảo sử dụng các tên duy nhất để tránh ghi đè các mô hình tích hợp sẵn.

### Đặt mục tiêu mô hình

#### Người hồi quy

Nếu bạn đang sử dụng một biến hồi quy, bạn cần chỉ định mục tiêu có các giá trị liên tục. FreqAI bao gồm nhiều biến hồi quy khác nhau, chẳng hạn như `LightGBMRegressor`thông qua cờ `--freqaimodel LightGBMRegressor`. Một ví dụ về cách bạn có thể đặt mục tiêu hồi quy để dự đoán giá 100 cây nến trong tương lai sẽ là```python
df['&s-close_price'] = df['close'].shift(-100)
```Nếu bạn muốn dự đoán nhiều mục tiêu, bạn cần xác định nhiều nhãn bằng cú pháp tương tự như trên.

#### Bộ phân loại

Nếu bạn đang sử dụng trình phân loại, bạn cần chỉ định mục tiêu có các giá trị riêng biệt. FreqAI bao gồm nhiều bộ phân loại khác nhau, chẳng hạn như `LightGBMClassifier` thông qua cờ `--freqaimodel LightGBMClassifier`. Nếu bạn chọn sử dụng trình phân loại, các lớp cần được đặt bằng chuỗi. Ví dụ: nếu bạn muốn dự đoán giá của 100 cây nến trong tương lai sẽ tăng hay giảm, bạn sẽ đặt```python
df['&s-up_or_down'] = np.where( df["close"].shift(-100) > df["close"], 'up', 'down')
```Nếu bạn muốn dự đoán nhiều mục tiêu, bạn phải chỉ định tất cả các nhãn trong cùng một cột nhãn. Ví dụ: bạn có thể thêm nhãn `same` để xác định nơi giá không thay đổi bằng cách đặt```python
df['&s-up_or_down'] = np.where( df["close"].shift(-100) > df["close"], 'up', 'down')
df['&s-up_or_down'] = np.where( df["close"].shift(-100) == df["close"], 'same', df['&s-up_or_down'])
```## Mô-đun PyTorch

### Bắt đầu nhanh

Cách dễ nhất để chạy nhanh mô hình pytorch là dùng lệnh sau (đối với tác vụ hồi quy):```bash
freqtrade trade --config config_examples/config_freqai.example.json --strategy FreqaiExampleStrategy --freqaimodel PyTorchMLPRegressor --strategy-path freqtrade/templates 
```!!! Lưu ý "Cài đặt/docker"
    Mô-đun PyTorch yêu cầu các gói lớn như `torch`, gói này phải được yêu cầu rõ ràng trong `./setup.sh -i` bằng cách trả lời "y" cho câu hỏi "Bạn cũng muốn các gói phụ thuộc cho freqai-rl hoặc PyTorch (cần thêm ~700mb dung lượng) [y/N]?".
    Người dùng thích docker nên đảm bảo họ sử dụng hình ảnh docker được gắn với `_freqaitorch`.
    Chúng tôi cung cấp tệp soạn thảo docker rõ ràng cho điều này trong `docker/docker-compose-freqai.yml` - có thể được sử dụng thông qua `docker soạn -f docker/docker-compose-freqai.yml run ...` - hoặc có thể được sao chép để thay thế tệp docker gốc.
    Tệp soạn thảo docker này cũng chứa một phần (đã bị vô hiệu hóa) để kích hoạt tài nguyên GPU trong vùng chứa docker. Điều này rõ ràng giả định rằng hệ thống có sẵn tài nguyên GPU.

    PyTorch đã bỏ hỗ trợ cho macOS x64 (thiết bị Apple dựa trên intel) trong phiên bản 2.3. Sau đó, freqtrade cũng ngừng hỗ trợ PyTorch trên nền tảng này.

!!! Nguy hiểm "Thông báo an ninh"
    Việc tải các mô hình đã lưu từ đĩa có thể gây ra sự cố bảo mật nếu sử dụng tệp mô hình từ xa (tệp bạn đã tải xuống từ Internet hoặc nhận được từ một nguồn không đáng tin cậy) do cần phải có `weights_only=False`, điều này có thể gây ra sự cố bảo mật.
    Miễn là bạn chỉ tải những mô hình mà bạn đã tự đào tạo thì sẽ không có rủi ro.

### Cấu trúc

####Người mẫu

Bạn có thể xây dựng kiến trúc Mạng thần kinh của riêng mình trong PyTorch bằng cách chỉ cần xác định lớp `nn.Module` bên trong tệp [`IFreqaiModel` tùy chỉnh](#USE-other-prediction-models) rồi sử dụng lớp đó trong hàm `def train()` của bạn. Dưới đây là một ví dụ về triển khai mô hình hồi quy logistic bằng PyTorch (nên được sử dụng với tiêu chí nn.BCELoss) cho các nhiệm vụ phân loại.```python

class LogisticRegression(nn.Module):
    def __init__(self, input_size: int):
        super().__init__()
        # Define your layers
        self.linear = nn.Linear(input_size, 1)
        self.activation = nn.Sigmoid()

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # Define the forward pass
        out = self.linear(x)
        out = self.activation(out)
        return out

class MyCoolPyTorchClassifier(BasePyTorchClassifier):
    """
    This is a custom IFreqaiModel showing how a user might setup their own 
    custom Neural Network architecture for their training.
    """

    @property
    def data_convertor(self) -> PyTorchDataConvertor:
        return DefaultPyTorchDataConvertor(target_tensor_type=torch.float)

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        config = self.freqai_info.get("model_training_parameters", {})
        self.learning_rate: float = config.get("learning_rate",  3e-4)
        self.model_kwargs: dict[str, Any] = config.get("model_kwargs",  {})
        self.trainer_kwargs: dict[str, Any] = config.get("trainer_kwargs",  {})

    def fit(self, data_dictionary: dict, dk: FreqaiDataKitchen, **kwargs) -> Any:
        """
        User sets up the training and test data to fit their desired model here
        :param data_dictionary: the dictionary holding all data for train, test,
            labels, weights
        :param dk: The datakitchen object for the current coin/model
        """

        class_names = self.get_class_names()
        self.convert_label_column_to_int(data_dictionary, dk, class_names)
        n_features = data_dictionary["train_features"].shape[-1]
        model = LogisticRegression(
            input_dim=n_features
        )
        model.to(self.device)
        optimizer = torch.optim.AdamW(model.parameters(), lr=self.learning_rate)
        criterion = torch.nn.CrossEntropyLoss()
        init_model = self.get_init_model(dk.pair)
        trainer = PyTorchModelTrainer(
            model=model,
            optimizer=optimizer,
            criterion=criterion,
            model_meta_data={"class_names": class_names},
            device=self.device,
            init_model=init_model,
            data_convertor=self.data_convertor,
            **self.trainer_kwargs,
        )
        trainer.fit(data_dictionary, self.splits)
        return trainer

```#### Huấn luyện viên

`PyTorchModelTrainer` thực hiện vòng lặp xe lửa PyTorch đặc trưng:
Xác định mô hình, hàm mất và trình tối ưu hóa của chúng tôi, sau đó di chuyển chúng đến thiết bị thích hợp (GPU hoặc CPU). Bên trong vòng lặp, chúng tôi lặp qua các lô trong bộ nạp dữ liệu, di chuyển dữ liệu đến thiết bị, tính toán dự đoán và mất mát, truyền ngược và cập nhật các tham số mô hình bằng trình tối ưu hóa. 

Ngoài ra, huấn luyện viên còn có trách nhiệm sau:
 - lưu và tải mô hình
 - chuyển đổi dữ liệu từ `pandas.DataFrame` sang `torch.Tensor`. 

#### Tích hợp với mô-đun Freqai 

Giống như tất cả các mô hình freqai, các mô hình PyTorch kế thừa `IFreqaiModel`. `IFreqaiModel` khai báo ba phương thức trừu tượng: `train`, `fit` và `predict`. chúng tôi triển khai các phương pháp này theo ba cấp độ phân cấp.
Từ trên xuống dưới:

1. `BasePyTorchModel` - Triển khai phương thức `train`. tất cả `BasePyTorch*` đều kế thừa nó. chịu trách nhiệm chuẩn bị dữ liệu chung (ví dụ: chuẩn hóa dữ liệu) và gọi phương thức `fit`. Đặt thuộc tính `device` được sử dụng bởi các lớp con. Đặt thuộc tính `model_type` được lớp cha sử dụng.
2. `BasePyTorch*` - Triển khai phương thức `dự đoán`. Ở đây, `*` đại diện cho một nhóm thuật toán, chẳng hạn như bộ phân loại hoặc bộ hồi quy. chịu trách nhiệm tiền xử lý dữ liệu, dự đoán và xử lý hậu kỳ nếu cần.
3. `PyTorch*Classifier` / `PyTorch*Regressor` - triển khai phương thức `fit`. chịu trách nhiệm về lỗi tàu chính, trong đó chúng tôi khởi tạo các đối tượng huấn luyện và mô hình.

![hình ảnh](assets/freqai_pytorch-diagram.png)

#### Ví dụ đầy đủ

Xây dựng bộ hồi quy PyTorch bằng mô hình MLP (perceptron đa lớp), tiêu chí MSELoss và trình tối ưu hóa AdamW.```python
class PyTorchMLPRegressor(BasePyTorchRegressor):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        config = self.freqai_info.get("model_training_parameters", {})
        self.learning_rate: float = config.get("learning_rate",  3e-4)
        self.model_kwargs: dict[str, Any] = config.get("model_kwargs",  {})
        self.trainer_kwargs: dict[str, Any] = config.get("trainer_kwargs",  {})

    def fit(self, data_dictionary: dict, dk: FreqaiDataKitchen, **kwargs) -> Any:
        n_features = data_dictionary["train_features"].shape[-1]
        model = PyTorchMLPModel(
            input_dim=n_features,
            output_dim=1,
            **self.model_kwargs
        )
        model.to(self.device)
        optimizer = torch.optim.AdamW(model.parameters(), lr=self.learning_rate)
        criterion = torch.nn.MSELoss()
        init_model = self.get_init_model(dk.pair)
        trainer = PyTorchModelTrainer(
            model=model,
            optimizer=optimizer,
            criterion=criterion,
            device=self.device,
            init_model=init_model,
            target_tensor_type=torch.float,
            **self.trainer_kwargs,
        )
        trainer.fit(data_dictionary)
        return trainer
```Ở đây, chúng ta tạo một lớp `PyTorchMLPRegressor` triển khai phương thức `fit`. Phương thức `fit` chỉ định các khối xây dựng đào tạo: mô hình, trình tối ưu hóa, tiêu chí và trình huấn luyện. Chúng tôi kế thừa cả `BasePyTorchRegressor` và `BasePyTorchModel`, trong đó cái trước triển khai phương thức `dự đoán` phù hợp với nhiệm vụ hồi quy của chúng tôi và cái sau triển khai phương thức huấn luyện.

??? Lưu ý "Đặt tên lớp cho bộ phân loại"
    Khi sử dụng trình phân loại, người dùng phải khai báo tên lớp (hoặc mục tiêu) bằng cách ghi đè thuộc tính `IFreqaiModel.class_names`. Điều này đạt được bằng cách đặt `self.freqai.class_names` trong chiến lược FreqAI bên trong phương thức `set_freqai_targets`.
    
    Ví dụ: nếu bạn đang sử dụng trình phân loại nhị phân để dự đoán biến động giá lên hoặc xuống, bạn có thể đặt tên lớp như sau:```python
    def set_freqai_targets(self, dataframe: DataFrame, metadata: dict, **kwargs) -> DataFrame:
        self.freqai.class_names = ["down", "up"]
        dataframe['&s-up_or_down'] = np.where(dataframe["close"].shift(-100) >
                                                  dataframe["close"], 'up', 'down')
    
        return dataframe
    ```    To see a full example, you can refer to the [classifier test strategy class](https://github.com/freqtrade/freqtrade/blob/develop/tests/strategy/strats/freqai_test_classifier.py).
#### Cải thiện hiệu suất với `torch.compile()`Torch provides a `torch.compile()` method that can be used to improve performance for specific GPU hardware. More details can be found [here](https://pytorch.org/tutorials/intermediate/torch_compile_tutorial.html). In brief, you simply wrap your `model` in `torch.compile()`:
```python
        model = PyTorchMLPModel(
            input_dim=n_features,
            output_dim=1,
            **self.model_kwargs
        )
        model.to(self.device)
        model = torch.compile(model)
```Sau đó tiến hành sử dụng mô hình như bình thường. Hãy nhớ rằng việc thực hiện này sẽ loại bỏ khả năng thực thi háo hức, điều đó có nghĩa là các lỗi và truy nguyên sẽ không mang lại nhiều thông tin.