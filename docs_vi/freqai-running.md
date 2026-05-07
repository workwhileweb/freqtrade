<!-- Auto-translated from docs/ by script. Please review technical terms. -->

# Tần số chạy

Có hai cách để đào tạo và triển khai mô hình học máy thích ứng - triển khai trực tiếp và kiểm tra ngược lịch sử. Trong cả hai trường hợp, FreqAI chạy/mô phỏng việc đào tạo lại định kỳ các mô hình như trong hình sau:

![freqai-window](assets/freqai_moving-window.jpg)

## Triển khai trực tiếp

FreqAI có thể chạy khô/trực tiếp bằng lệnh sau:```bash
freqtrade trade --strategy FreqaiExampleStrategy --config config_freqai.example.json --freqaimodel LightGBMRegressor
```Khi ra mắt, FreqAI sẽ bắt đầu đào tạo một mô hình mới, với `mã định danh` mới, dựa trên cài đặt cấu hình. Sau khi đào tạo, mô hình sẽ được sử dụng để đưa ra dự đoán về các nến sắp tới cho đến khi có mô hình mới. Các mô hình mới thường được tạo thường xuyên nhất có thể, trong đó FreqAI quản lý hàng đợi nội bộ của các cặp tiền xu để cố gắng giữ cho tất cả các mô hình được cập nhật như nhau. FreqAI sẽ luôn sử dụng mô hình được đào tạo gần đây nhất để đưa ra dự đoán về dữ liệu trực tiếp đến. Nếu không muốn FreqAI đào tạo lại các mô hình mới thường xuyên nhất có thể, bạn có thể đặt `live_retrain_hours` để yêu cầu FreqAI đợi ít nhất số giờ đó trước khi đào tạo một mô hình mới. Ngoài ra, bạn có thể đặt `expired_hours` để báo cho FreqAI tránh đưa ra dự đoán về các mô hình cũ hơn số giờ đó.

Các mô hình đã đào tạo theo mặc định được lưu vào đĩa để cho phép sử dụng lại trong quá trình kiểm tra ngược hoặc sau sự cố. Bạn có thể chọn [xóa các mô hình cũ](#purging-old-model-data) để tiết kiệm dung lượng ổ đĩa bằng cách đặt `"purge_old_models": true` trong cấu hình.

Để bắt đầu chạy thử/trực tiếp từ một mô hình backtest đã lưu (hoặc từ một phiên chạy khô/trực tiếp bị lỗi trước đó), bạn chỉ cần chỉ định `mã nhận dạng` của mô hình cụ thể:```json
    "freqai": {
        "identifier": "example",
        "live_retrain_hours": 0.5
    }
```Trong trường hợp này, mặc dù FreqAI sẽ bắt đầu với một mô hình được đào tạo trước nhưng nó vẫn sẽ kiểm tra xem đã trôi qua bao nhiêu thời gian kể từ khi mô hình được đào tạo. Nếu đã hết `live_retrain_hours` kể từ khi kết thúc mô hình được tải, FreqAI sẽ bắt đầu đào tạo một mô hình mới.

### Tải dữ liệu tự động

FreqAI tự động tải xuống lượng dữ liệu thích hợp cần thiết để đảm bảo việc đào tạo mô hình thông qua `train_ Period_days` và `startup_candle_count` được xác định (xem [bảng tham số](freqai-parameter-table.md) để biết mô tả chi tiết về các tham số này). 

### Lưu dữ liệu dự đoán

Tất cả các dự đoán được thực hiện trong suốt vòng đời của một mô hình `mã nhận dạng` cụ thể đều được lưu trữ trong `histocal_predictions.pkl` để cho phép tải lại sau khi xảy ra sự cố hoặc có thay đổi đối với cấu hình.

### Xóa dữ liệu mô hình cũ

FreqAI lưu trữ các tệp mô hình mới sau mỗi lần đào tạo thành công. Những tập tin này trở nên lỗi thời khi các mô hình mới được tạo ra để thích ứng với điều kiện thị trường mới. Nếu bạn định để FreqAI chạy trong thời gian dài với tần suất đào tạo lại cao, bạn nên bật `purge_old_models` trong cấu hình:```json
    "freqai": {
        "purge_old_models": 4,
    }
```Thao tác này sẽ tự động xóa tất cả các mô hình cũ hơn bốn mô hình được đào tạo gần đây nhất để tiết kiệm dung lượng ổ đĩa. Việc nhập "0" sẽ không bao giờ xóa bất kỳ mô hình nào.

## Kiểm tra lại

Mô-đun kiểm tra lại FreqAI có thể được thực thi bằng lệnh sau:```bash
freqtrade backtesting --strategy FreqaiExampleStrategy --strategy-path freqtrade/templates --config config_examples/config_freqai.example.json --freqaimodel LightGBMRegressor --timerange 20210501-20210701
```Nếu lệnh này chưa bao giờ được thực thi với tệp cấu hình hiện có, FreqAI sẽ huấn luyện một mô hình mới
cho mỗi cặp, cho mỗi cửa sổ kiểm tra lại trong `--timerange` được mở rộng.

Chế độ backtesting yêu cầu [tải xuống dữ liệu cần thiết](#downloading-data-to-cover-the-full-backtest- Period) trước khi triển khai (không giống như ở chế độ khô/trực tiếp trong đó FreqAI tự động xử lý việc tải xuống dữ liệu). Bạn nên cẩn thận khi xem xét rằng phạm vi thời gian của dữ liệu được tải xuống lớn hơn phạm vi thời gian kiểm tra lại. Điều này là do FreqAI cần dữ liệu trước khoảng thời gian backtest mong muốn để huấn luyện mô hình sẵn sàng đưa ra dự đoán về cây nến đầu tiên trong khoảng thời gian backtest đã đặt. Bạn có thể tìm thêm thông tin chi tiết về cách tính toán dữ liệu để tải xuống [tại đây](#deciding-the-size-of-the-sliding-training-window-and-backtesting-duration).

!!! Lưu ý "Tái sử dụng mô hình"
    Sau khi quá trình đào tạo hoàn tất, bạn có thể thực hiện lại quá trình kiểm tra lại với cùng một tệp cấu hình và
    FreqAI sẽ tìm các mô hình đã được đào tạo và tải chúng thay vì dành thời gian đào tạo. Điều này rất hữu ích
    nếu bạn muốn điều chỉnh (hoặc thậm chí siêu thích) các tiêu chí mua và bán bên trong chiến lược. Nếu bạn
    *muốn* đào tạo lại một mô hình mới có cùng tệp cấu hình, bạn chỉ cần thay đổi `mã định danh`.
    Bằng cách này, bạn có thể quay lại sử dụng bất kỳ mô hình nào bạn muốn bằng cách chỉ định `mã định danh`.

!!! Lưu ý
    Backtest gọi `set_freqai_targets()` một lần cho mỗi cửa sổ backtest (trong đó số lượng cửa sổ là khoảng thời gian backtest đầy đủ chia cho tham số `backtest_ Period_days`). Làm điều này có nghĩa là các mục tiêu mô phỏng hành vi khô khan/sống động mà không có sự thiên vị về phía trước. Tuy nhiên, việc xác định các tính năng trong `feature_engineering_*()` được thực hiện một lần trong toàn bộ khoảng thời gian đào tạo. Điều này có nghĩa là bạn phải chắc chắn rằng các tính năng không hướng tới tương lai.
    Bạn có thể tìm thêm thông tin chi tiết về xu hướng nhìn về phía trước trong [Những sai lầm thường gặp](strategy-customization.md#common-mistakes-when-development-strategies).

---

### Lưu dữ liệu dự đoán backtesting

Để cho phép điều chỉnh chiến lược của bạn (**không phải** các tính năng!), FreqAI sẽ tự động lưu dự đoán trong quá trình kiểm tra ngược để chúng có thể được sử dụng lại cho các lần kiểm tra ngược và chạy trực tiếp trong tương lai bằng cách sử dụng cùng một mô hình `mã định danh`. Điều này mang lại sự nâng cao hiệu suất hướng đến việc cho phép **siêu chọn cấp độ cao** các tiêu chí vào/ra.

Một thư mục bổ sung có tên `backtesting_predictions`, chứa tất cả các dự đoán được lưu trữ ở định dạng `feather`, sẽ được tạo trong thư mục `unique-id`.

Để thay đổi **tính năng** của mình, bạn **phải** đặt một `mã định danh` mới trong cấu hình để báo hiệu cho FreqAI đào tạo các mô hình mới.

Để lưu các mô hình được tạo trong một lần kiểm tra ngược cụ thể để bạn có thể bắt đầu triển khai trực tiếp từ một trong số chúng thay vì đào tạo một mô hình mới, bạn phải đặt `save_backtest_models` thành `True` trong config.

!!! Lưu ý
    Để đảm bảo mô hình có thể được sử dụng lại, freqAI sẽ gọi chiến lược của bạn với khung dữ liệu có độ dài 1. 
    Nếu chiến lược của bạn yêu cầu nhiều dữ liệu hơn mức này để tạo ra các tính năng tương tự, thì bạn không thể sử dụng lại các dự đoán kiểm tra ngược để triển khai trực tiếp và cần cập nhật `mã định danh` cho mỗi lần kiểm tra ngược mới.

!!! Nguy hiểm "Thông báo an ninh"
    Việc tải các mô hình đã lưu từ đĩa có thể gây ra sự cố bảo mật nếu sử dụng tệp mô hình từ xa (tệp bạn đã tải xuống từ Internet hoặc nhận được từ một nguồn không đáng tin cậy) do cần phải có `weights_only=False`, điều này có thể gây ra sự cố bảo mật.Miễn là bạn chỉ tải những mô hình mà bạn đã tự đào tạo thì sẽ không có rủi ro.

### Backtest dự đoán được thu thập trực tiếp

FreqAI cho phép bạn sử dụng lại các dự đoán lịch sử trực tiếp thông qua tham số backtest `--freqai-backtest-live-models`. Điều này có thể hữu ích khi bạn muốn sử dụng lại các dự đoán được tạo trong quá trình khô/chạy để so sánh hoặc nghiên cứu khác.

Không được thông báo tham số `--timerange` vì nó sẽ được tính toán tự động thông qua dữ liệu trong tệp dự đoán lịch sử.

### Đang tải xuống dữ liệu để bao gồm toàn bộ thời gian backtest

Đối với việc triển khai trực tiếp/khô, FreqAI sẽ tự động tải xuống dữ liệu cần thiết. Tuy nhiên, để sử dụng chức năng kiểm tra ngược, bạn cần tải xuống dữ liệu cần thiết bằng cách sử dụng `download-data` (chi tiết [tại đây](data-download.md#data-downloading)). Bạn cần chú ý cẩn thận để hiểu lượng dữ liệu *bổ sung* cần được tải xuống để đảm bảo rằng có đủ lượng dữ liệu đào tạo *trước* khi bắt đầu khoảng thời gian kiểm tra lại. Bạn có thể ước tính gần đúng lượng dữ liệu bổ sung bằng cách di chuyển ngày bắt đầu của phạm vi thời gian ngược lại `train_thời_ngày` và `startup_candle_count` (xem [bảng tham số](freqai-parameter-table.md) để biết mô tả chi tiết về các tham số này) tính từ thời điểm bắt đầu phạm vi thời gian kiểm tra ngược mong muốn. 

Ví dụ: để kiểm tra lại `--timerange 20210501-20210701` bằng cách sử dụng [example config](freqai-configuration.md#setting-up-the-configuration-file) đặt `train_ Period_days` thành 30, cùng với `startup_candle_count: 40` trong tối đa `include_timeframes` là 1h, ngày bắt đầu cho nhu cầu dữ liệu được tải xuống là `20210501` - 30 ngày - 40 * 1h / 24 giờ = 20210330 (sớm hơn 31,7 ngày so với thời điểm bắt đầu khoảng thời gian đào tạo mong muốn).

### Quyết định kích thước của cửa sổ đào tạo trượt và thời gian kiểm tra lại

Phạm vi thời gian kiểm tra lại được xác định bằng tham số `--timerange` điển hình trong tệp cấu hình. Khoảng thời gian của khoảng thời gian đào tạo trượt được đặt theo `train_ Period_days`, trong khi `backtest_ Period_days` là khoảng thời gian kiểm tra lại trượt, cả về số ngày (`backtest_ Period_days` có thể
một biểu tượng nổi để biểu thị việc đào tạo lại hàng ngày ở chế độ trực tiếp/khô). Trong [cấu hình ví dụ](freqai-configuration.md#setting-up-the-configuration-file) (được tìm thấy trong `config_examples/config_freqai.example.json`), người dùng đang yêu cầu FreqAI sử dụng thời gian đào tạo là 30 ngày và kiểm tra lại trong 7 ngày tiếp theo. Sau khi đào tạo mô hình, FreqAI sẽ kiểm tra lại trong 7 ngày tiếp theo. Sau đó, "cửa sổ trượt" sẽ chuyển tiếp về phía trước một tuần (mô phỏng việc đào tạo lại FreqAI một lần mỗi tuần ở chế độ trực tiếp) và mô hình mới sử dụng 30 ngày trước đó (bao gồm cả 7 ngày được mô hình trước đó sử dụng để kiểm tra lại) để đào tạo. Điều này được lặp lại cho đến khi kết thúc `--timerange`.  Điều này có nghĩa là nếu bạn đặt `--timerange 20210501-20210701`, FreqAI sẽ đào tạo 8 mô hình riêng biệt ở cuối `--timerange` (vì phạm vi đầy đủ bao gồm 8 tuần).

!!! Ghi chúMặc dù cho phép `backtest_ Period_days` dạng phân số, nhưng bạn nên lưu ý rằng `--timerange` được chia cho giá trị này để xác định số lượng mô hình mà FreqAI sẽ cần huấn luyện nhằm backtest toàn bộ phạm vi. Ví dụ: bằng cách đặt `--timerange` là 10 ngày và `backtest_ Period_days` là 0,1, FreqAI sẽ cần đào tạo 100 mô hình mỗi cặp để hoàn thành backtest đầy đủ. Vì lý do này, quá trình đào tạo thích ứng FreqAI thực sự sẽ mất một thời gian *rất* dài. Cách tốt nhất để kiểm tra đầy đủ một mô hình là chạy thử và để nó huấn luyện liên tục. Trong trường hợp này, việc kiểm tra lại sẽ mất cùng khoảng thời gian như chạy thử.

## Xác định thời gian hết hạn của mô hình

Trong chế độ khô/trực tiếp, FreqAI đào tạo từng cặp xu một cách tuần tự (trên các luồng/GPU riêng biệt từ bot Freqtrade chính). Điều này có nghĩa là luôn có sự chênh lệch về độ tuổi giữa các người mẫu. Nếu bạn đang huấn luyện trên 50 cặp và mỗi cặp cần 5 phút để huấn luyện thì mẫu cũ nhất sẽ hoạt động được hơn 4 giờ. Điều này có thể không mong muốn nếu thang thời gian đặc trưng (mục tiêu thời gian giao dịch) cho một chiến lược nhỏ hơn 4 giờ. Bạn có thể quyết định chỉ thực hiện các mục giao dịch nếu mô hình có tuổi đời ít hơn một số giờ nhất định bằng cách đặt `expiration_hours` trong tệp cấu hình:```json
    "freqai": {
        "expiration_hours": 0.5,
    }
```Trong cấu hình ví dụ được trình bày, người dùng sẽ chỉ cho phép dự đoán trên các mô hình có tuổi đời dưới 1/2 giờ.

## Kiểm soát quá trình học mẫu

Các tham số đào tạo mô hình là duy nhất cho thư viện máy học đã chọn. FreqAI cho phép bạn đặt bất kỳ tham số nào cho bất kỳ thư viện nào bằng cách sử dụng từ điển `model_training_parameters` trong config. Cấu hình mẫu (có trong `config_examples/config_freqai.example.json`) hiển thị một số tham số mẫu được liên kết với `Catboost` và `LightGBM`, nhưng bạn có thể thêm bất kỳ tham số nào có sẵn trong các thư viện đó hoặc bất kỳ thư viện máy học nào khác mà bạn chọn triển khai.Data split parameters are defined in `data_split_parameters` which can be any parameters associated with scikit-learn's `train_test_split()` function. `train_test_split()` has a parameters called `shuffle` which allows to shuffle the data or keep it unshuffled. This is particularly useful to avoid biasing training with temporally auto-correlated data. More details about these parameters can be found the [scikit-learn website](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.train_test_split.html) (external website).
Tham số cụ thể của FreqAI `label_ Period_candles` xác định độ chênh lệch (số lượng nến trong tương lai) được sử dụng cho `nhãn`. Trong [cấu hình mẫu](freqai-configuration.md#setting-up-the-configuration-file được trình bày), người dùng đang yêu cầu `nhãn` là 24 ngọn nến trong tương lai.

## Học tập liên tục

Bạn có thể chọn áp dụng kế hoạch học tập liên tục bằng cách đặt `"continual_learning": true` trong config. Bằng cách bật `continual_learning`, sau khi đào tạo mô hình ban đầu từ đầu, các khóa đào tạo tiếp theo sẽ bắt đầu từ trạng thái mô hình cuối cùng của khóa đào tạo trước đó. Điều này mang lại cho mô hình mới một "bộ nhớ" về trạng thái trước đó. Theo mặc định, giá trị này được đặt thành `False`, nghĩa là tất cả các mô hình mới đều được đào tạo từ đầu mà không có dữ liệu đầu vào từ các mô hình trước đó.

???+ nguy hiểm "Việc học liên tục thực thi một không gian tham số không đổi"
    Vì `continual_learning` có nghĩa là không gian tham số mô hình *không thể* thay đổi giữa các lần huấn luyện, nên `principal_comComponent_analysis` sẽ tự động bị tắt khi `continual_learning` được bật. Gợi ý: PCA thay đổi không gian tham số và số lượng tính năng, tìm hiểu thêm về PCA [tại đây](freqai-feature-engineering.md#data-directionality-reduction-with-principal-comComponent-analysis).

???+ nguy hiểm "Chức năng thử nghiệm"
    Hãy lưu ý rằng đây hiện là một cách tiếp cận ngây thơ đối với việc học tăng dần và có khả năng cao là trang bị quá mức/bị mắc kẹt ở mức tối thiểu cục bộ trong khi thị trường di chuyển khỏi mô hình của bạn. Chúng tôi có sẵn các cơ chế trong FreqAI chủ yếu cho mục đích thử nghiệm và để sẵn sàng cho các phương pháp tiếp cận hoàn thiện hơn nhằm học hỏi liên tục trong các hệ thống hỗn loạn như thị trường tiền điện tử.

## Hyperopt

Bạn có thể tăng cường sử dụng lệnh tương tự như đối với [hyperopt Freqtrade điển hình](hyperopt.md):```bash
freqtrade hyperopt --hyperopt-loss SharpeHyperOptLoss --strategy FreqaiExampleStrategy --freqaimodel LightGBMRegressor --strategy-path freqtrade/templates --config config_examples/config_freqai.example.json --timerange 20220428-20220507
````hyperopt` yêu cầu bạn phải tải xuống trước dữ liệu theo cách tương tự như khi bạn thực hiện [kiểm tra lại](#backtesting). Ngoài ra, bạn phải xem xét một số hạn chế khi cố gắng áp dụng các chiến lược FreqAI:

- Tham số hyperopt `--analyze-per-epoch` không tương thích với FreqAI.
- Không thể tăng cường chỉ báo trong các hàm `feature_engineering_*()` và `set_freqai_targets()`. Điều này có nghĩa là bạn không thể tối ưu hóa các tham số mô hình bằng hyperopt. Ngoài ngoại lệ này, có thể tối ưu hóa tất cả [dấu cách] khác (hyperopt.md#running-hyperopt-with-smaller-search-space).
- Hướng dẫn backtesting cũng áp dụng cho hyperopt.

Phương pháp tốt nhất để kết hợp hyperopt và FreqAI là tập trung vào ngưỡng/tiêu chí vào/ra tối ưu. Bạn cần tập trung vào các tham số siêu tối ưu không được sử dụng trong các tính năng của bạn. Ví dụ: bạn không nên cố gắng tăng cường độ dài cửa sổ cuộn trong quá trình tạo tính năng hoặc bất kỳ phần nào của cấu hình FreqAI làm thay đổi dự đoán. Để tối ưu hóa chiến lược FreqAI một cách hiệu quả, FreqAI lưu trữ các dự đoán dưới dạng khung dữ liệu và tái sử dụng chúng. Do đó, yêu cầu chỉ áp dụng ngưỡng/tiêu chí vào/ra.

Một ví dụ điển hình về tham số siêu thích hợp trong FreqAI là ngưỡng cho [Chỉ số khác biệt (DI)](freqai-feature-engineering.md#identifying-outliers-with-the-dissimilarity-index-di) `DI_values` mà chúng tôi coi các điểm dữ liệu là ngoại lệ:```python
di_max = IntParameter(low=1, high=20, default=10, space='buy', optimize=True, load=True)
dataframe['outlier'] = np.where(dataframe['DI_values'] > self.di_max.value/10, 1, 0)
```Hyperopt cụ thể này sẽ giúp bạn hiểu `DI_values` thích hợp cho không gian tham số cụ thể của bạn.

## Sử dụng Tensorboard

!!! lưu ý "Có sẵn"    FreqAI includes tensorboard for a variety of models, including XGBoost, all PyTorch models, Reinforcement Learning, and Catboost. If you would like to see Tensorboard integrated into another model type, please open an issue on the [Freqtrade GitHub](https://github.com/freqtrade/freqtrade/issues)
!!! nguy hiểm "Yêu cầu"
    Việc ghi nhật ký bảng kéo yêu cầu hình ảnh cài đặt/đèn pin FreqAI.


Cách dễ nhất để sử dụng tensorboard là đảm bảo `freqai.activate_tensorboard` được đặt thành `True` (cài đặt mặc định) trong tệp cấu hình của bạn, chạy FreqAI, sau đó mở một shell riêng và chạy:```bash
cd freqtrade
tensorboard --logdir user_data/models/unique-id
```trong đó `unique-id` là `mã định danh` được đặt trong tệp cấu hình `freqai`. Lệnh này phải được chạy trong một shell riêng nếu bạn muốn xem kết quả đầu ra trong trình duyệt của mình tại 127.0.0.1:6060 (6060 là cổng mặc định được Tensorboard sử dụng).

![tensorboard](assets/tensorboard.jpg)


!!! lưu ý "Tắt kích hoạt để cải thiện hiệu suất"
    Việc ghi nhật ký bảng kéo có thể làm chậm quá trình đào tạo và cần được ngừng hoạt động để sử dụng trong sản xuất.