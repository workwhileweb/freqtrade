<!-- Auto-translated from docs/ by script. Please review technical terms. -->

# Kỹ thuật tính năng

## Xác định các tính năng

Kỹ thuật tính năng cấp thấp được thực hiện trong chiến lược người dùng trong một tập hợp các hàm được gọi là `feature_engineering_*`. Các hàm này đặt `tính năng cơ bản` chẳng hạn như, `RSI`, `MFI`, `EMA`, `SMA`, thời gian trong ngày, khối lượng, v.v. `tính năng cơ bản` có thể là chỉ báo tùy chỉnh hoặc chúng có thể được nhập từ bất kỳ thư viện phân tích kỹ thuật nào mà bạn có thể tìm thấy. FreqAI được trang bị một bộ chức năng để đơn giản hóa nhanh chóng kỹ thuật tính năng quy mô lớn:

|  Chức năng | Mô tả |
|---------------|-------------|
| `feature_engineering_expand_all()` | Hàm tùy chọn này sẽ tự động mở rộng các tính năng đã xác định trên cấu hình được xác định `indicator_ Periods_candles`, `include_timeframes`, `include_shifted_candles` và `include_corr_pairs`.
| `feature_engineering_expand_basic()` | Hàm tùy chọn này sẽ tự động mở rộng các tính năng đã xác định trên cấu hình được xác định `include_timeframes`, `include_shifted_candles` và `include_corr_pairs`. Lưu ý: hàm này *không* mở rộng trên `indicator_ Periods_candles`.
| `feature_engineering_standard()` | Hàm tùy chọn này sẽ được gọi một lần với khung dữ liệu của khung thời gian cơ sở. Đây là hàm cuối cùng được gọi, có nghĩa là khung dữ liệu nhập hàm này sẽ chứa tất cả các tính năng và cột từ nội dung cơ sở được tạo bởi các hàm `feature_engineering_expand` khác. Hàm này là một nơi tốt để thực hiện việc trích xuất các đặc điểm ngoại lai tùy chỉnh (ví dụ: tsfresh). Chức năng này cũng là một vị trí phù hợp cho bất kỳ tính năng nào không được tự động mở rộng (ví dụ: ngày trong tuần).
| `set_freqai_target()` | Chức năng cần thiết để thiết lập mục tiêu cho mô hình. Tất cả các mục tiêu phải được thêm vào trước `&` để được nội bộ FreqAI công nhận.

Trong khi đó, kỹ thuật tính năng cấp cao được xử lý trong `"feature_parameters":{}` trong cấu hình FreqAI. Trong tệp này, có thể quyết định mở rộng tính năng quy mô lớn dựa trên `base_features`, chẳng hạn như "bao gồm các cặp tương quan" hoặc "bao gồm các khung thời gian cung cấp thông tin" hoặc thậm chí "bao gồm cả nến gần đây".

Bạn nên bắt đầu từ các hàm `feature_engineering_*` mẫu trong chiến lược ví dụ được cung cấp từ nguồn (có trong `templates/FreqaiExampleStrategy.py`) để đảm bảo rằng các định nghĩa tính năng tuân theo các quy ước chính xác. Dưới đây là ví dụ về cách đặt chỉ báo và nhãn trong chiến lược:```python
    def feature_engineering_expand_all(self, dataframe: DataFrame, period, metadata, **kwargs) -> DataFrame:
        """
        *Only functional with FreqAI enabled strategies*
        This function will automatically expand the defined features on the config defined
        `indicator_periods_candles`, `include_timeframes`, `include_shifted_candles`, and
        `include_corr_pairs`. In other words, a single feature defined in this function
        will automatically expand to a total of
        `indicator_periods_candles` * `include_timeframes` * `include_shifted_candles` *
        `include_corr_pairs` numbers of features added to the model.

        All features must be prepended with `%` to be recognized by FreqAI internals.

        Access metadata such as the current pair/timeframe/period with:

        `metadata["pair"]` `metadata["tf"]`  `metadata["period"]`

        :param df: strategy dataframe which will receive the features
        :param period: period of the indicator - usage example:
        :param metadata: metadata of current pair
        dataframe["%-ema-period"] = ta.EMA(dataframe, timeperiod=period)
        """

        dataframe["%-rsi-period"] = ta.RSI(dataframe, timeperiod=period)
        dataframe["%-mfi-period"] = ta.MFI(dataframe, timeperiod=period)
        dataframe["%-adx-period"] = ta.ADX(dataframe, timeperiod=period)
        dataframe["%-sma-period"] = ta.SMA(dataframe, timeperiod=period)
        dataframe["%-ema-period"] = ta.EMA(dataframe, timeperiod=period)

        bollinger = qtpylib.bollinger_bands(
            qtpylib.typical_price(dataframe), window=period, stds=2.2
        )
        dataframe["bb_lowerband-period"] = bollinger["lower"]
        dataframe["bb_middleband-period"] = bollinger["mid"]
        dataframe["bb_upperband-period"] = bollinger["upper"]

        dataframe["%-bb_width-period"] = (
            dataframe["bb_upperband-period"]
            - dataframe["bb_lowerband-period"]
        ) / dataframe["bb_middleband-period"]
        dataframe["%-close-bb_lower-period"] = (
            dataframe["close"] / dataframe["bb_lowerband-period"]
        )

        dataframe["%-roc-period"] = ta.ROC(dataframe, timeperiod=period)

        dataframe["%-relative_volume-period"] = (
            dataframe["volume"] / dataframe["volume"].rolling(period).mean()
        )

        return dataframe

    def feature_engineering_expand_basic(self, dataframe: DataFrame, metadata, **kwargs) -> DataFrame:
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

        Access metadata such as the current pair/timeframe with:

        `metadata["pair"]` `metadata["tf"]`

        All features must be prepended with `%` to be recognized by FreqAI internals.

        :param df: strategy dataframe which will receive the features
        :param metadata: metadata of current pair
        dataframe["%-pct-change"] = dataframe["close"].pct_change()
        dataframe["%-ema-200"] = ta.EMA(dataframe, timeperiod=200)
        """
        dataframe["%-pct-change"] = dataframe["close"].pct_change()
        dataframe["%-raw_volume"] = dataframe["volume"]
        dataframe["%-raw_price"] = dataframe["close"]
        return dataframe

    def feature_engineering_standard(self, dataframe: DataFrame, metadata, **kwargs) -> DataFrame:
        """
        *Only functional with FreqAI enabled strategies*
        This optional function will be called once with the dataframe of the base timeframe.
        This is the final function to be called, which means that the dataframe entering this
        function will contain all the features and columns created by all other
        freqai_feature_engineering_* functions.

        This function is a good place to do custom exotic feature extractions (e.g. tsfresh).
        This function is a good place for any feature that should not be auto-expanded upon
        (e.g. day of the week).

        Access metadata such as the current pair with:

        `metadata["pair"]`

        All features must be prepended with `%` to be recognized by FreqAI internals.

        :param df: strategy dataframe which will receive the features
        :param metadata: metadata of current pair
        usage example: dataframe["%-day_of_week"] = (dataframe["date"].dt.dayofweek + 1) / 7
        """
        dataframe["%-day_of_week"] = (dataframe["date"].dt.dayofweek + 1) / 7
        dataframe["%-hour_of_day"] = (dataframe["date"].dt.hour + 1) / 25
        return dataframe

    def set_freqai_targets(self, dataframe: DataFrame, metadata, **kwargs) -> DataFrame:
        """
        *Only functional with FreqAI enabled strategies*
        Required function to set the targets for the model.
        All targets must be prepended with `&` to be recognized by the FreqAI internals.

        Access metadata such as the current pair with:

        `metadata["pair"]`

        :param df: strategy dataframe which will receive the targets
        :param metadata: metadata of current pair
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
```Trong ví dụ được trình bày, người dùng không muốn chuyển `bb_lowband` làm tính năng cho mô hình,
và do đó đã không thêm `%` vào trước nó. Tuy nhiên, người dùng muốn chuyển `bb_width` tới
mô hình để huấn luyện/dự đoán và do đó đã thêm vào trước nó `%`.

Sau khi đã xác định `các tính năng cơ bản`, bước tiếp theo là mở rộng chúng bằng cách sử dụng `feature_parameters` mạnh mẽ trong tệp cấu hình:```json
    "freqai": {
        //...
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
        //...
    }
````include_timeframes` trong cấu hình ở trên là các khung thời gian (`tf`) của mỗi lệnh gọi đến `feature_engineering_expand_*()` trong chiến lược. Trong trường hợp được trình bày, người dùng yêu cầu đưa các khung thời gian `5m`, `15m` và `4h` của `rsi`, `mfi`, `roc` và `bb_width` vào bộ tính năng.

Bạn có thể yêu cầu đưa từng tính năng đã xác định vào các cặp thông tin bằng cách sử dụng `include_corr_pairlist`. Điều này có nghĩa là bộ tính năng sẽ bao gồm tất cả các tính năng từ `feature_engineering_expand_*()` trên tất cả `include_timeframes` cho từng cặp tương quan được xác định trong cấu hình (`ETH/USD`, `LINK/USD` và `BNB/USD` trong ví dụ được trình bày).

`include_shifted_candles` cho biết số lượng nến trước đó cần đưa vào bộ tính năng. Ví dụ: `include_shifted_candles: 2` yêu cầu FreqAI bao gồm 2 nến trước đây cho mỗi tính năng trong bộ tính năng.

Tổng cộng, số tính năng mà người dùng chiến lược ví dụ được trình bày đã tạo là: độ dài của `include_timeframes` * không. các tính năng trong `feature_engineering_expand_*()` * độ dài của `include_corr_pairlist` * không. `include_shifted_candles` * độ dài của `indicator_ Periods_candles`
 $= 3 * 3 * 3 * 2 * 2 = 108$.
 
!!! lưu ý "Tìm hiểu thêm về kỹ thuật tính năng sáng tạo"    Check out our [medium article](https://emergentmethods.medium.com/freqai-from-price-to-prediction-6fadac18b665) geared toward helping users learn how to creatively engineer features.
### Giành quyền kiểm soát tốt hơn đối với các hàm `feature_engineering_*` với `siêu dữ liệu`

Tất cả các hàm `feature_engineering_*` và `set_freqai_targets()` đều được chuyển qua một từ điển `siêu dữ liệu` chứa thông tin về `cặp`, `tf` (khung thời gian) và `thời gian` mà FreqAI đang tự động hóa để xây dựng tính năng. Do đó, người dùng có thể sử dụng `siêu dữ liệu` bên trong các hàm `feature_engineering_*` làm tiêu chí để chặn/đặt trước các tính năng cho các khung thời gian, khoảng thời gian, cặp nhất định, v.v.```python
def feature_engineering_expand_all(self, dataframe: DataFrame, period, metadata, **kwargs) -> DataFrame:
    if metadata["tf"] == "1h":
        dataframe["%-roc-period"] = ta.ROC(dataframe, timeperiod=period)
```Điều này sẽ chặn không cho `ta.ROC()` được thêm vào bất kỳ khung thời gian nào ngoài `"1h"`.

### Trả lại thông tin bổ sung từ quá trình đào tạo

Các số liệu quan trọng có thể được trả về chiến lược khi kết thúc mỗi khóa đào tạo mô hình bằng cách gán chúng cho `dk.data['extra_returns_per_train']['my_new_value'] = XYZ` bên trong lớp mô hình dự đoán tùy chỉnh. 

FreqAI lấy `my_new_value` được gán trong từ điển này và mở rộng nó để phù hợp với khung dữ liệu được trả về chiến lược. Sau đó, bạn có thể sử dụng các chỉ số được trả về trong chiến lược của mình thông qua `dataframe['my_new_value']`. Một ví dụ về cách sử dụng các giá trị trả về trong FreqAI là các giá trị `&*_mean` và `&*_std` được dùng để [tạo ngưỡng mục tiêu động](freqai-configuration.md#creating-a-dynamic-target-threshold).

Một ví dụ khác, trong đó người dùng muốn sử dụng số liệu trực tiếp từ cơ sở dữ liệu giao dịch, được hiển thị bên dưới:```json
    "freqai": {
        "extra_returns_per_train": {"total_profit": 4}
    }
```Bạn cần đặt từ điển chuẩn trong cấu hình để FreqAI có thể trả về các hình dạng khung dữ liệu phù hợp. Các giá trị này có thể sẽ bị mô hình dự đoán ghi đè, nhưng trong trường hợp mô hình chưa đặt chúng hoặc cần một giá trị ban đầu mặc định thì các giá trị đặt trước sẽ được trả về.

### Tính năng cân nhắc tầm quan trọng theo thời gian

FreqAI cho phép bạn đặt `weight_factor` để tính trọng số dữ liệu gần đây mạnh hơn dữ liệu trong quá khứ thông qua hàm mũ:

$$ W_i = \exp(\frac{-i}{\alpha*n}) $$

trong đó $W_i$ là trọng số của điểm dữ liệu $i$ trong tổng số điểm dữ liệu $n$. Dưới đây là hình minh họa tác động của các hệ số trọng số khác nhau lên các điểm dữ liệu trong một bộ tính năng.

![hệ số trọng lượng](assets/freqai_weight-factor.jpg)

## Xây dựng đường dẫn dữ liệu

Theo mặc định, FreqAI xây dựng quy trình động dựa trên cài đặt cấu hình của người dùng. Các cài đặt mặc định rất mạnh mẽ và được thiết kế để hoạt động với nhiều phương pháp khác nhau. Hai bước này là `MinMaxScaler(-1,1)` và `VarianceThreshold` để loại bỏ bất kỳ cột nào có phương sai 0. Người dùng có thể kích hoạt các bước khác với nhiều thông số cấu hình hơn. Ví dụ: nếu người dùng thêm `use_SVM_to_remove_outliers: true` vào cấu hình `freqai`, thì FreqAI sẽ tự động thêm [`SVMOutlierExtractor`](#identifying-outliers-USE-a-support-vector-machine-svm) vào quy trình. Tương tự, người dùng có thể thêm `principal_comComponent_analysis: true` vào cấu hình `freqai` để kích hoạt PCA. [Chỉ số khác biệt](#identifying-outliers-with-the-dissimilarity-index-di) được kích hoạt với `DI_threshold: 1`. Cuối cùng, nhiễu cũng có thể được thêm vào dữ liệu với `noise_standard_deviation: 0,1`. Cuối cùng, người dùng có thể thêm loại bỏ ngoại lệ [DBSCAN](#identifying-outliers-with-dbscan) bằng `use_DBSCAN_to_remove_outliers: true`.

!!! lưu ý "Có thêm thông tin"
    Vui lòng xem lại [bảng tham số](freqai-parameter-table.md) để biết thêm thông tin về các tham số này.


### Tùy chỉnh đường ống

Người dùng được khuyến khích tùy chỉnh đường dẫn dữ liệu theo nhu cầu của họ bằng cách xây dựng đường dẫn dữ liệu của riêng họ. Điều này có thể được thực hiện bằng cách chỉ cần đặt `dk.feature_pipeline` thành đối tượng `Pipeline` mong muốn bên trong hàm `IFreqaiModel` `train()` hoặc nếu họ không muốn chạm vào hàm `train()`, họ có thể ghi đè các hàm `define_data_pipeline`/`define_label_pipeline` trong `IFreqaiModel` của họ:

!!! lưu ý "Có thêm thông tin"    FreqAI uses the [`DataSieve`](https://github.com/emergentmethods/datasieve) pipeline, which follows the SKlearn pipeline API, but adds, among other features, coherence between the X, y, and sample_weight vector point removals, feature removal, feature name following. 
```python
from datasieve.transforms import SKLearnWrapper, DissimilarityIndex
from datasieve.pipeline import Pipeline
from sklearn.preprocessing import QuantileTransformer, StandardScaler
from freqai.base_models import BaseRegressionModel


class MyFreqaiModel(BaseRegressionModel):
    """
    Some cool custom model
    """
    def fit(self, data_dictionary: Dict, dk: FreqaiDataKitchen, **kwargs) -> Any:
        """
        My custom fit function
        """
        model = cool_model.fit()
        return model

    def define_data_pipeline(self) -> Pipeline:
        """
        User defines their custom feature pipeline here (if they wish)
        """
        feature_pipeline = Pipeline([
            ('qt', SKLearnWrapper(QuantileTransformer(output_distribution='normal'))),
            ('di', ds.DissimilarityIndex(di_threshold=1))
        ])

        return feature_pipeline
    
    def define_label_pipeline(self) -> Pipeline:
        """
        User defines their custom label pipeline here (if they wish)
        """
        label_pipeline = Pipeline([
            ('qt', SKLearnWrapper(StandardScaler())),
        ])

        return label_pipeline
```Here, you are defining the exact pipeline that will be used for your feature set during training and prediction. You can use *most* SKLearn transformation steps by wrapping them in the `SKLearnWrapper` class as shown above. In addition, you can use any of the transformations available in the [`DataSieve` library](https://github.com/emergentmethods/datasieve). 
Bạn có thể dễ dàng thêm phép biến đổi của riêng mình bằng cách tạo một lớp kế thừa từ bộ dữ liệu `BaseTransform` và triển khai các phương thức `fit()`, `transform()` và `inverse_transform()` của bạn:```python
from datasieve.transforms.base_transform import BaseTransform
# import whatever else you need

class MyCoolTransform(BaseTransform):
    def __init__(self, **kwargs):
        self.param1 = kwargs.get('param1', 1)

    def fit(self, X, y=None, sample_weight=None, feature_list=None, **kwargs):
        # do something with X, y, sample_weight, or/and feature_list
        return X, y, sample_weight, feature_list

    def transform(self, X, y=None, sample_weight=None,
                  feature_list=None, outlier_check=False, **kwargs):
        # do something with X, y, sample_weight, or/and feature_list
        return X, y, sample_weight, feature_list

    def inverse_transform(self, X, y=None, sample_weight=None, feature_list=None, **kwargs):
        # do/dont do something with X, y, sample_weight, or/and feature_list
        return X, y, sample_weight, feature_list
```!!! lưu ý "Gợi ý"
    Bạn có thể định nghĩa lớp tùy chỉnh này trong cùng tệp với `IFreqaiModel` của mình.

### Di chuyển `IFreqaiModel` tùy chỉnh sang Đường ống mới

Nếu bạn đã tạo `IFreqaiModel` tùy chỉnh của riêng mình với hàm `train()`/`predict()` tùy chỉnh, *và* bạn vẫn dựa vào `data_cleaning_train/predict()`, thì bạn sẽ cần phải di chuyển sang quy trình mới. Nếu mô hình của bạn *không* dựa vào `data_cleaning_train/predict()` thì bạn không cần phải lo lắng về việc di chuyển này.

Bạn có thể tìm thêm thông tin chi tiết về quá trình di chuyển [tại đây](strategy_migration.md#freqai-new-data-pipeline).

## Phát hiện ngoại lệ

Thị trường chứng khoán và tiền điện tử phải chịu mức độ nhiễu không theo khuôn mẫu cao dưới dạng các điểm dữ liệu ngoại lệ. FreqAI triển khai nhiều phương pháp khác nhau để xác định các ngoại lệ đó và từ đó giảm thiểu rủi ro.

### Xác định các ngoại lệ bằng Chỉ số khác biệt (DI)

Chỉ số khác biệt (DI) nhằm mục đích định lượng độ không chắc chắn liên quan đến từng dự đoán do mô hình đưa ra. 

Bạn có thể yêu cầu FreqAI xóa các điểm dữ liệu ngoại lệ khỏi tập dữ liệu huấn luyện/kiểm tra bằng DI bằng cách đưa câu lệnh sau vào cấu hình:```json
    "freqai": {
        "feature_parameters" : {
            "DI_threshold": 1
        }
    }
```Điều này sẽ thêm bước `DissimilarityIndex` vào `feature_pipeline` của bạn và đặt ngưỡng thành 1. DI cho phép loại bỏ các dự đoán là ngoại lệ (không tồn tại trong không gian tính năng mô hình) do mức độ chắc chắn thấp. Để làm như vậy, FreqAI đo khoảng cách giữa mỗi điểm dữ liệu huấn luyện (vectơ đặc trưng), $X_{a}$ và tất cả các điểm dữ liệu huấn luyện khác:

$$ d_{ab} = \sqrt{\sum_{j=1}^p(X_{a,j}-X_{b,j})^2} $$

trong đó $d_{ab}$ là khoảng cách giữa các điểm được chuẩn hóa $a$ và $b$, và $p$ là số lượng đối tượng, tức là độ dài của vectơ $X$. Khoảng cách đặc trưng, $\overline{d}$, đối với một tập hợp các điểm dữ liệu huấn luyện chỉ đơn giản là giá trị trung bình của khoảng cách trung bình:

$$ \overline{d} = \sum_{a=1}^n(\sum_{b=1}^n(d_{ab}/n)/n) $$

$\overline{d}$ định lượng mức độ phân tán của dữ liệu huấn luyện, được so sánh với khoảng cách giữa vectơ tính năng dự đoán mới, $X_k$ và tất cả dữ liệu huấn luyện:

$$ d_k = \arg \min d_{k,i} $$

Điều này cho phép ước tính Chỉ số khác biệt như sau:

$$ DI_k = d_k/\overline{d} $$

Bạn có thể điều chỉnh DI thông qua `DI_threshold` để tăng hoặc giảm phép ngoại suy của mô hình được đào tạo. `DI_threshold` cao hơn có nghĩa là DI nhẹ nhàng hơn và cho phép sử dụng các dự đoán ở xa dữ liệu huấn luyện trong khi `DI_threshold` thấp hơn có tác dụng ngược lại và do đó loại bỏ nhiều dự đoán hơn.

Dưới đây là hình mô tả DI cho tập dữ liệu 3D.

![DI](tài sản/freqai_DI.jpg)

### Xác định các ngoại lệ bằng Máy vectơ hỗ trợ (SVM)

Bạn có thể yêu cầu FreqAI xóa các điểm dữ liệu ngoại lệ khỏi tập dữ liệu huấn luyện/kiểm tra bằng Máy vectơ hỗ trợ (SVM) bằng cách đưa câu lệnh sau vào cấu hình:```json
    "freqai": {
        "feature_parameters" : {
            "use_SVM_to_remove_outliers": true
        }
    }
```Điều này sẽ thêm bước `SVMOutlierExtractor` vào `feature_pipeline` của bạn. SVM sẽ được huấn luyện về dữ liệu huấn luyện và mọi điểm dữ liệu mà SVM cho là nằm ngoài không gian đặc trưng sẽ bị xóa.

Bạn có thể chọn cung cấp các tham số bổ sung cho SVM, chẳng hạn như `shuffle` và `nu` thông qua từ điển `feature_parameters.svm_params` trong config.

Tham số `shuffle` theo mặc định được đặt thành `False` để đảm bảo kết quả nhất quán. Nếu nó được đặt thành `True`, việc chạy SVM nhiều lần trên cùng một tập dữ liệu có thể dẫn đến các kết quả khác nhau do `max_iter` ở mức thấp để thuật toán đạt được `tol` được yêu cầu. Việc tăng `max_iter` giải quyết được vấn đề này nhưng khiến quy trình mất nhiều thời gian hơn.

Tham số `nu`, *rất* theo nghĩa rộng, là số lượng điểm dữ liệu được coi là ngoại lệ và phải nằm trong khoảng từ 0 đến 1.

### Xác định các ngoại lệ bằng DBSCAN

Bạn có thể định cấu hình FreqAI để sử dụng DBSCAN để phân cụm và xóa các ngoại lệ khỏi tập dữ liệu huấn luyện/kiểm tra hoặc các ngoại lệ đến khỏi dự đoán bằng cách kích hoạt `use_DBSCAN_to_remove_outliers` trong cấu hình:```json
    "freqai": {
        "feature_parameters" : {
            "use_DBSCAN_to_remove_outliers": true
        }
    }
```Thao tác này sẽ thêm bước `DataSieveDBSCAN` vào `feature_pipeline` của bạn. Đây là một thuật toán học máy không giám sát, phân cụm dữ liệu mà không cần biết nên có bao nhiêu cụm.

Với một số điểm dữ liệu $N$ và khoảng cách $\varepsilon$, DBSCAN phân cụm tập dữ liệu bằng cách đặt tất cả các điểm dữ liệu có $N-1$ các điểm dữ liệu khác trong khoảng cách $\varepsilon$ làm *điểm cốt lõi*. Một điểm dữ liệu nằm trong khoảng cách $\varepsilon$ tính từ *điểm lõi* nhưng không có $N-1$ điểm dữ liệu khác trong khoảng cách $\varepsilon$ tính từ chính nó được coi là *điểm cạnh*. Khi đó, một cụm là tập hợp các *điểm cốt lõi* và *điểm biên*. Các điểm dữ liệu không có điểm dữ liệu nào khác ở khoảng cách $<\varepsilon$ được coi là ngoại lệ. Hình bên dưới hiển thị một cụm có $N = 3$.

![dbscan](tài sản/freqai_dbscan.jpg)FreqAI uses `sklearn.cluster.DBSCAN` (details are available on scikit-learn's webpage [here](https://scikit-learn.org/stable/modules/generated/sklearn.cluster.DBSCAN.html) (external website)) with `min_samples` ($N$) taken as 1/4 of the no. of time points (candles) in the feature set. `eps` ($\varepsilon$) is computed automatically as the elbow point in the *k-distance graph* computed from the nearest neighbors in the pairwise distances of all data points in the feature set.
### Giảm kích thước dữ liệu bằng Phân tích thành phần chính

Bạn có thể giảm kích thước của các tính năng của mình bằng cách kích hoạt phân tích thành phần chính trong cấu hình:```json
    "freqai": {
        "feature_parameters" : {
            "principal_component_analysis": true
        }
    }
```Điều này sẽ thực hiện PCA trên các đối tượng địa lý và giảm số chiều của chúng sao cho phương sai được giải thích của tập dữ liệu là >= 0,999. Việc giảm kích thước dữ liệu giúp việc đào tạo mô hình nhanh hơn và do đó cho phép tạo ra các mô hình cập nhật hơn.