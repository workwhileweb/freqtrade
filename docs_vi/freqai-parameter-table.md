<!-- Auto-translated from docs/ by script. Please review technical terms. -->

#Bảng thông số

Bảng bên dưới sẽ liệt kê tất cả các thông số cấu hình có sẵn cho FreqAI. Một số tham số được minh họa trong `config_examples/config_freqai.example.json`.

Các tham số bắt buộc được đánh dấu là **Bắt buộc** và phải được đặt theo một trong các cách được đề xuất.

###Thông số cấu hình chung

|  Tham số | Mô tả |
|----------||-------------|
|  |  **Thông số cấu hình chung trong cây `config.freqai`**
| `tần số` | **Bắt buộc.** <br> Từ điển gốc chứa tất cả các tham số để kiểm soát FreqAI. <br> **Loại dữ liệu:** Từ điển.
| `chuyến_thời_gian` | **Bắt buộc.** <br> Số ngày sử dụng cho dữ liệu huấn luyện (chiều rộng của cửa sổ trượt). <br> **Loại dữ liệu:** Số nguyên dương.
| `backtest_thời_ngày` | **Bắt buộc.** <br> Số ngày để suy luận từ mô hình đã đào tạo trước khi trượt cửa sổ `train_ Period_days` được xác định ở trên và đào tạo lại mô hình trong quá trình kiểm tra lại (thông tin thêm [tại đây](freqai-running.md#backtesting)). Đây có thể là số ngày phân số, nhưng hãy lưu ý rằng `phạm vi thời gian` được cung cấp sẽ được chia cho số này để tạo ra số lượng đào tạo cần thiết để hoàn thành quá trình kiểm tra ngược. <br> **Loại dữ liệu:** Phao.
| `định danh` | **Bắt buộc.** <br> ID duy nhất cho kiểu máy hiện tại. Nếu các mô hình được lưu vào đĩa, `mã định danh` cho phép tải lại các mô hình/dữ liệu được đào tạo trước cụ thể. <br> **Loại dữ liệu:** Chuỗi.
| `live_retrain_hours` | Tần suất đào tạo lại trong quá trình chạy khô/trực tiếp. <br> **Loại dữ liệu:** Float > 0. <br> Mặc định: `0` (các mô hình đào tạo lại thường xuyên nhất có thể).
| `hết hạn_giờ` | Tránh đưa ra dự đoán nếu mô hình cũ hơn `expiration_hours`. <br> **Loại dữ liệu:** Số nguyên dương. <br> Mặc định: `0` (mô hình không bao giờ hết hạn).
| `purge_old_models` | Số lượng mô hình được lưu trên đĩa (không liên quan đến việc kiểm tra lại). Mặc định là 2, có nghĩa là các lần chạy khô/trực tiếp sẽ giữ lại 2 mẫu mới nhất trên đĩa. Đặt thành 0 sẽ giữ nguyên tất cả các kiểu máy. Tham số này cũng chấp nhận boolean để duy trì khả năng tương thích ngược. <br> **Loại dữ liệu:** Số nguyên. <br> Mặc định: `2`.
| `save_backtest_models` | Lưu mô hình vào đĩa khi chạy backtesting. Backtesting hoạt động hiệu quả nhất bằng cách lưu dữ liệu dự đoán và sử dụng lại chúng trực tiếp cho các lần chạy tiếp theo (khi bạn muốn điều chỉnh các tham số vào/ra). Việc lưu các mô hình kiểm tra lại vào đĩa cũng cho phép sử dụng các tệp mô hình tương tự để bắt đầu một phiên bản khô/trực tiếp với cùng một `mã định danh` mô hình. <br> **Loại dữ liệu:** Boolean. <br> Mặc định: `False` (không có mô hình nào được lưu).
| `fit_live_predictions_candles` | Số lượng nến lịch sử được sử dụng để tính toán số liệu thống kê mục tiêu (nhãn) từ dữ liệu dự đoán, thay vì từ tập dữ liệu huấn luyện (bạn có thể tìm thêm thông tin [tại đây](freqai-configuration.md#creating-a-dynamic-target-threshold)). <br> **Loại dữ liệu:** Số nguyên dương.
| `học_học liên tục` | Sử dụng trạng thái cuối cùng của mô hình được đào tạo gần đây nhất làm điểm bắt đầu cho mô hình mới, cho phép học tập tăng dần (bạn có thể tìm thêm thông tin [tại đây](freqai-running.md#continual-learning)). Hãy lưu ý rằng đây hiện là một cách tiếp cận ngây thơ đối với việc học tăng dần và có khả năng cao là trang bị quá mức/bị mắc kẹt ở mức tối thiểu cục bộ trong khi thị trường di chuyển khỏi mô hình của bạn. Chúng tôi có các kết nối ở đây chủ yếu cho mục đích thử nghiệm và do đó sẵn sàng cho các phương pháp tiếp cận hoàn thiện hơn để học hỏi liên tục trong các hệ thống hỗn loạn như thị trường tiền điện tử. <br> **Loại dữ liệu:** Boolean. <br> Mặc định: `Sai`.| `write_metrics_to_disk` | Thu thập thời gian đào tạo, thời gian suy luận và mức sử dụng CPU trong tệp json. <br> **Loại dữ liệu:** Boolean. <br> Mặc định: `Sai`
| `data_kitchen_thread_count` | <br> Chỉ định số lượng luồng bạn muốn sử dụng để xử lý dữ liệu (các phương pháp ngoại lệ, chuẩn hóa, v.v.). Điều này không ảnh hưởng đến số lượng chủ đề được sử dụng để đào tạo. Nếu người dùng không đặt nó (mặc định), FreqAI sẽ sử dụng số luồng tối đa - 2 (để lại 1 lõi vật lý cho Freqtrade bot và FreqUI) <br> **Datatype:** Số nguyên dương.
| `kích hoạt_tensorboard` | <br> Cho biết có hay không kích hoạt tensorboard cho các mô-đun hỗ trợ tensorboard (hiện tại là Học tăng cường, XGBoost, Catboost và PyTorch). Tensorboard cần cài đặt Torch, có nghĩa là bạn sẽ cần hình ảnh docker torch/RL hoặc bạn cần trả lời "có" cho câu hỏi cài đặt về việc bạn có muốn cài đặt Torch hay không. <br> **Loại dữ liệu:** Boolean. <br> Mặc định: `Đúng`.
| `wait_for_training_iteration_on_reload` | <br> Khi sử dụng /reload hoặc ctrl-c, hãy đợi quá trình lặp đào tạo hiện tại kết thúc trước khi hoàn tất việc tắt máy một cách nhẹ nhàng. Nếu được đặt thành `False`, FreqAI sẽ phá vỡ quá trình lặp đào tạo hiện tại, cho phép bạn tắt máy nhanh chóng hơn nhưng bạn sẽ mất quá trình lặp đào tạo hiện tại. <br> **Loại dữ liệu:** Boolean. <br> Mặc định: `Đúng`.

### Thông số tính năng

|  Tham số | Mô tả |
|----------||-------------|
|  |  **Các tham số tính năng trong từ điển phụ `freqai.feature_parameters`**
| `thông số tính năng` | Một từ điển chứa các tham số được sử dụng để thiết kế bộ tính năng. Thông tin chi tiết và ví dụ được hiển thị [tại đây](freqai-feature-engineering.md). <br> **Loại dữ liệu:** Từ điển.
| `include_timeframes` | Danh sách các khung thời gian mà tất cả chỉ báo trong `feature_engineering_expand_*()` sẽ được tạo. Danh sách này được thêm dưới dạng các tính năng vào bộ dữ liệu chỉ báo cơ sở. <br> **Loại dữ liệu:** Danh sách các khung thời gian (chuỗi).
| `include_corr_pairlist` | Danh sách các đồng tiền tương quan mà FreqAI sẽ thêm dưới dạng tính năng bổ sung cho tất cả các đồng tiền `pair_whitelist`. Tất cả các chỉ báo được đặt trong `feature_engineering_expand_*()` trong quá trình kỹ thuật tính năng (xem chi tiết [tại đây](freqai-feature-engineering.md)) sẽ được tạo cho mỗi đồng tiền tương quan. Các tính năng tiền xu tương quan được thêm vào bộ dữ liệu chỉ báo cơ sở. <br> **Loại dữ liệu:** Danh sách nội dung (chuỗi).
| `nhãn_thời_nến` | Số lượng nến trong tương lai mà nhãn được tạo. Điều này có thể được sử dụng trong `set_freqai_targets()` (xem `templates/FreqaiExampleStrategy.py` để biết cách sử dụng chi tiết). Tham số này không nhất thiết phải bắt buộc, bạn có thể tạo nhãn tùy chỉnh và chọn có sử dụng tham số này hay không. Vui lòng xem `templates/FreqaiExampleStrategy.py` để biết ví dụ về cách sử dụng. <br> **Loại dữ liệu:** Số nguyên dương.
| `include_shifted_candles` | Thêm các tính năng từ nến trước vào nến tiếp theo với mục đích bổ sung thông tin lịch sử. Nếu được sử dụng, FreqAI sẽ sao chép và chuyển tất cả các tính năng từ nến trước đó `include_shifted_candles` để có thông tin cho nến tiếp theo. <br> **Loại dữ liệu:** Số nguyên dương.
| `yếu tố trọng lượng` | Điểm dữ liệu tập tạ theo mức độ gần đây của chúng (xem chi tiết [tại đây](freqai-feature-engineering.md#weighting-features-for-temporal-importance)). <br> **Loại dữ liệu:** Số float dương (thường < 1).| `chỉ báo_max_thời_nến` | **Không còn được sử dụng (#7325)**. Được thay thế bằng `startup_candle_count` được đặt trong [strategy](freqai-configuration.md#building-a-freqai-strategy). `startup_candle_count` không phụ thuộc vào khung thời gian và xác định *thời gian* tối đa được sử dụng trong `feature_engineering_*()` để tạo chỉ báo. FreqAI sử dụng tham số này cùng với khung thời gian tối đa trong `include_time_frames` để tính toán số lượng điểm dữ liệu cần tải xuống sao cho điểm dữ liệu đầu tiên không bao gồm NaN. <br> **Loại dữ liệu:** Số nguyên dương.
| `chỉ báo_thời gian_nến` | Khoảng thời gian để tính toán các chỉ số. Các chỉ số được thêm vào tập dữ liệu chỉ báo cơ sở. <br> **Loại dữ liệu:** Danh sách số nguyên dương.
| `phân tích_thành phần_chính` | Tự động giảm kích thước của tập dữ liệu bằng cách sử dụng Phân tích thành phần chính. Xem thông tin chi tiết về cách hoạt động [tại đây](freqai-feature-engineering.md#data-directionality-reduction-with-principal-comComponent-analysis) <br> **Datatype:** Boolean. <br> Mặc định: `Sai`.
| `plot_feature_importances` | Tạo một biểu đồ tầm quan trọng của tính năng cho từng mô hình cho số lượng tính năng `plot_feature_importances` trên cùng/dưới cùng. Lô được lưu trữ trong `user_data/models/<identifier>/sub-train-<COIN>_<timestamp>.html`. <br> **Loại dữ liệu:** Số nguyên. <br> Mặc định: `0`.
| `DI_ngưỡng` | Kích hoạt việc sử dụng Chỉ số khác biệt để phát hiện ngoại lệ khi được đặt thành > 0. Xem chi tiết về cách hoạt động của chỉ số này [tại đây](freqai-feature-engineering.md#identifying-outliers-with-the-dissimilarity-index-di). <br> **Loại dữ liệu:** Số float dương (thường < 1).
| `use_SVM_to_remove_outliers` | Huấn luyện máy vectơ hỗ trợ để phát hiện và loại bỏ các ngoại lệ khỏi tập dữ liệu huấn luyện cũng như khỏi các điểm dữ liệu đến. Xem thông tin chi tiết về cách hoạt động [tại đây](freqai-feature-engineering.md#identifying-outliers-USE-a-support-vector-machine-svm). <br> **Loại dữ liệu:** Boolean.
| `svm_params` | Tất cả các tham số có sẵn trong `SGDOneClassSVM()` của Sklearn. Xem thông tin chi tiết về một số tham số chọn [tại đây](freqai-feature-engineering.md#identifying-outliers-USE-a-support-vector-machine-svm). <br> **Loại dữ liệu:** Từ điển.
| `use_DBSCAN_to_remove_outliers` | Phân cụm dữ liệu bằng thuật toán DBSCAN để xác định và loại bỏ các ngoại lệ khỏi dữ liệu huấn luyện và dự đoán. Xem thông tin chi tiết về cách thức hoạt động của nó [tại đây](freqai-feature-engineering.md#identifying-outliers-with-dbscan). <br> **Loại dữ liệu:** Boolean. 
| `độ lệch_tiêu chuẩn_tiếng ồn` | Nếu được đặt, FreqAI sẽ thêm tiếng ồn vào các tính năng đào tạo nhằm ngăn chặn tình trạng trang bị quá mức. FreqAI tạo ra các sai lệch ngẫu nhiên so với phân bố gaussian với độ lệch chuẩn là `noise_standard_deviation` và thêm chúng vào tất cả các điểm dữ liệu. `độ lệch_tiêu chuẩn_nhiễu` phải được giữ tương đối với không gian chuẩn hóa, tức là trong khoảng từ -1 đến 1. Nói cách khác, vì dữ liệu trong FreqAI luôn được chuẩn hóa ở trong khoảng từ -1 đến 1, nên `độ lệch_tiêu chuẩn: 0,05` sẽ dẫn đến 32% dữ liệu bị tăng/giảm ngẫu nhiên hơn 2,5% (tức là phần trăm dữ liệu nằm trong độ lệch chuẩn đầu tiên). <br> **Loại dữ liệu:** Số nguyên. <br> Mặc định: `0`.| `outlier_protection_percentage` | Bật để ngăn các phương pháp phát hiện ngoại lệ loại bỏ quá nhiều dữ liệu. Nếu nhiều hơn `outlier_protection_percentage` % số điểm được SVM hoặc DBSCAN phát hiện là ngoại lệ, FreqAI sẽ ghi lại thông báo cảnh báo và bỏ qua việc phát hiện ngoại lệ, tức là tập dữ liệu gốc sẽ được giữ nguyên. Nếu tính năng bảo vệ ngoại lệ được kích hoạt thì sẽ không có dự đoán nào được đưa ra dựa trên tập dữ liệu huấn luyện. <br> **Loại dữ liệu:** Phao. <br> Mặc định: `30`.
| `reverse_train_test_order` | Tách tập dữ liệu tính năng (xem bên dưới) và sử dụng phần tách dữ liệu mới nhất để đào tạo và kiểm tra khả năng phân tách dữ liệu trước đây. Điều này cho phép mô hình được huấn luyện đến điểm dữ liệu gần đây nhất, đồng thời tránh trang bị quá mức. Tuy nhiên, bạn nên cẩn thận tìm hiểu bản chất không chính thống của tham số này trước khi sử dụng nó. <br> **Loại dữ liệu:** Boolean. <br> Mặc định: `False` (không đảo ngược).
| `shuffle_after_split` | Chia dữ liệu thành tập huấn luyện và tập kiểm tra, sau đó trộn cả hai tập riêng lẻ. <br> **Loại dữ liệu:** Boolean. <br> Mặc định: `Sai`.
| `buffer_train_data_candles` | Cắt `buffer_train_data_candles` khỏi phần đầu và phần cuối của dữ liệu huấn luyện *sau khi* các chỉ báo được điền. Ví dụ sử dụng chính là khi dự đoán cực đại và cực tiểu, hàm argrelextrema không thể biết cực đại/cực tiểu ở các cạnh của phạm vi thời gian. Để cải thiện độ chính xác của mô hình, cách tốt nhất là tính toán argrelextrema trên toàn bộ phạm vi thời gian và sau đó sử dụng hàm này để cắt các cạnh (bộ đệm) của kernel. Trong trường hợp khác, nếu mục tiêu được đặt thành biến động giá đã thay đổi thì vùng đệm này là không cần thiết vì nến được dịch chuyển ở cuối khoảng thời gian sẽ là NaN và FreqAI sẽ tự động loại bỏ những giá trị đó khỏi tập dữ liệu huấn luyện.<br> **Datatype:** Integer. <br> Mặc định: `0`.

### Tham số phân chia dữ liệu

|  Tham số | Mô tả |
|----------||-------------|
|  |  **Tham số phân chia dữ liệu trong từ điển phụ `freqai.data_split_parameters`**| `data_split_parameters` | Include any additional parameters available from scikit-learn `test_train_split()`, which are shown [here](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.train_test_split.html) (external website). <br> **Datatype:** Dictionary.
| `kích thước kiểm tra` | Phần dữ liệu nên được sử dụng để kiểm tra thay vì đào tạo. <br> **Loại dữ liệu:** Số float dương < 1.
| `xáo trộn` | Xáo trộn các điểm dữ liệu huấn luyện trong quá trình huấn luyện. Thông thường, để không xóa thứ tự thời gian của dữ liệu trong dự báo chuỗi thời gian, giá trị này được đặt thành `Sai`. <br> **Loại dữ liệu:** Boolean. <br> Mặc định: `Sai`.

### Tham số huấn luyện mô hình

|  Tham số | Mô tả |
|----------||-------------|
|  |  **Các tham số đào tạo mô hình trong từ điển phụ `freqai.model_training_parameters`**| `model_training_parameters` | A flexible dictionary that includes all parameters available by the selected model library. For example, if you use `LightGBMRegressor`, this dictionary can contain any parameter available by the `LightGBMRegressor` [here](https://lightgbm.readthedocs.io/en/latest/pythonapi/lightgbm.LGBMRegressor.html) (external website). If you select a different model, this dictionary can contain any parameter from that model. A list of the currently available models can be found [here](freqai-configuration.md#using-different-prediction-models).  <br> **Datatype:** Dictionary.
| `n_ước tính` | Số lượng cây được tăng cường để phù hợp với việc huấn luyện mô hình. <br> **Loại dữ liệu:** Số nguyên.
| `tỷ lệ học tập` | Tăng cường tốc độ học tập trong quá trình đào tạo mô hình. <br> **Loại dữ liệu:** Phao.
| `n_jobs`, `thread_count`, `task_type` | Đặt số lượng luồng để xử lý song song và `task_type` (`gpu` hoặc `cpu`). Các thư viện mô hình khác nhau sử dụng các tên tham số khác nhau. <br> **Loại dữ liệu:** Phao.

### Tham số Học tăng cường

|  Tham số | Mô tả |
|----------||-------------|
|  |  **Các thông số học tập tăng cường trong từ điển phụ `freqai.rl_config`**
| `rl_config` | Từ điển chứa các tham số điều khiển cho mô hình Học tăng cường. <br> **Loại dữ liệu:** Từ điển.
| `xe_xe lửa` | Các bước thời gian huấn luyện sẽ được đặt dựa trên `train_cycles * số điểm dữ liệu huấn luyện. <br> **Loại dữ liệu:** Số nguyên.
| `max_trade_duration_candles`| Hướng dẫn đào tạo đại lý để giữ giao dịch dưới thời lượng mong muốn. Ví dụ về cách sử dụng được hiển thị trong `prediction_models/ReinforcementLearner.py` trong hàm `calcate_reward()` có thể tùy chỉnh. <br> **Loại dữ liệu:** int.| `model_type` | Model string from stable_baselines3 or SBcontrib. Available strings include: `'TRPO', 'ARS', 'RecurrentPPO', 'MaskablePPO', 'PPO', 'A2C', 'DQN'`. User should ensure that `model_training_parameters` match those available to the corresponding stable_baselines3 model by visiting their documentation. [PPO doc](https://stable-baselines3.readthedocs.io/en/master/modules/ppo.html) (external website) <br> **Datatype:** string.
| `loại_chính sách` | Một trong các loại chính sách có sẵn từ stable_baselines3 <br> **Datatype:** string.
| `max_training_drawdown_pct` | Mức giảm tối đa mà đại lý được phép trải qua trong quá trình đào tạo. <br> **kiểu dữ liệu:** float. <br> Mặc định: 0,8
| `cpu_count` | Số lượng luồng/cPU dành riêng cho quá trình đào tạo Học tăng cường (tùy thuộc vào việc `ReinforcementLearner_multiproc` có được chọn hay không). Theo mặc định, nên giữ nguyên giá trị này, giá trị này được đặt thành tổng số lõi vật lý trừ đi 1. <br> **Datatype:** int.
| `model_reward_parameters` | Các tham số được sử dụng bên trong hàm `calcate_reward()` có thể tùy chỉnh trong `ReinforcementLearner.py` <br> **Datatype:** int.
| `add_state_info` | Yêu cầu FreqAI đưa thông tin trạng thái vào bộ tính năng dành cho đào tạo và hội thảo. Các biến trạng thái hiện tại bao gồm thời gian giao dịch, lợi nhuận hiện tại, vị thế giao dịch. Điều này chỉ khả dụng trong các lần chạy khô/trực tiếp và được tự động chuyển thành sai để kiểm tra lại. <br> **Loại dữ liệu:** bool. <br> Mặc định: `Sai`.| `net_arch` | Network architecture which is well described in [`stable_baselines3` doc](https://stable-baselines3.readthedocs.io/en/master/guide/custom_policy.html#examples). In summary: `[<shared layers>, dict(vf=[<non-shared value network layers>], pi=[<non-shared policy network layers>])]`. By default this is set to `[128, 128]`, which defines 2 shared hidden layers with 128 units each.
| `ngẫu nhiên_bắt đầu_vị trí` | Chọn ngẫu nhiên điểm bắt đầu của mỗi tập để tránh trang bị quá mức. <br> **Loại dữ liệu:** bool. <br> Mặc định: `Sai`.
| `drop_ohlc_from_features` | Không bao gồm dữ liệu ohmc đã chuẩn hóa trong bộ tính năng được chuyển cho tổng đài viên trong quá trình đào tạo (ohlc sẽ vẫn được sử dụng để điều khiển môi trường trong mọi trường hợp) <br> **Loại dữ liệu:** Boolean. <br> **Mặc định:** `Sai`
| `thanh tiến trình` | Hiển thị thanh tiến trình với tiến độ hiện tại, thời gian đã trôi qua và thời gian còn lại ước tính. <br> **Loại dữ liệu:** Boolean. <br> Mặc định: `Sai`.

### tham số PyTorch

#### chung

|  Tham số | Mô tả |
|----------||-------------|
|  |  **Các tham số đào tạo mô hình trong từ điển phụ `freqai.model_training_parameters`**
| `tỷ lệ học tập` | Tốc độ học tập được chuyển đến trình tối ưu hóa. <br> **kiểu dữ liệu:** float. <br> Mặc định: `3e-4`.
| `model_kwargs` | Các tham số được truyền cho lớp mô hình. <br> **Loại dữ liệu:** dict. <br> Mặc định: `{}`.
| `huấn luyện viên_kwargs` | Các tham số được chuyển đến lớp huấn luyện viên. <br> **Loại dữ liệu:** dict. <br> Mặc định: `{}`.

#### trainer_kwargs

| Tham số | Mô tả |
|--------------|-------------|
|              |  **Các tham số đào tạo mô hình trong từ điển phụ `freqai.model_training_parameters.model_kwargs`**
| `n_epochs` | Tham số `n_epochs` là cài đặt quan trọng trong vòng đào tạo PyTorch giúp xác định số lần toàn bộ tập dữ liệu huấn luyện sẽ được sử dụng để cập nhật các tham số của mô hình. Một kỷ nguyên đại diện cho một lần vượt qua toàn bộ tập dữ liệu huấn luyện. Ghi đè `n_steps`. Phải đặt `n_epochs` hoặc `n_steps`. <br><br> **Loại dữ liệu:** int. không bắt buộc. <br> Mặc định: `10`.
| `n_bước` | Một cách khác để thiết lập `n_epochs` - số lần lặp đào tạo sẽ chạy. Việc lặp lại ở đây đề cập đến số lần chúng tôi gọi `optimizer.step()`. Bị bỏ qua nếu `n_epochs` được đặt. Phiên bản đơn giản của hàm: <br><br> n_epochs = n_steps / (n_obs / batch_size) <br><br> Động lực ở đây là `n_steps` dễ tối ưu hóa hơn và giữ ổn định trên các n_obs khác nhau - số lượng điểm dữ liệu.  <br> <br> **Loại dữ liệu:** int. không bắt buộc. <br> Mặc định: `Không`.
| `kích thước lô` | Kích thước của các lô sẽ sử dụng trong quá trình đào tạo. <br><br> **Loại dữ liệu:** int. <br> Mặc định: `64`.
| `sớm_dừng_kiên nhẫn` | Số lượng kỷ nguyên không cải thiện được tình trạng mất xác thực trước khi quá trình đào tạo bị dừng sớm. Điều này giúp ngăn ngừa tình trạng trang bị quá mức bằng cách tạm dừng đào tạo khi mô hình ngừng cải thiện. Đặt thành `0` để tắt tính năng dừng sớm. Yêu cầu phân tách kiểm tra/xác thực (`test_size > 0`). <br><br> **Loại dữ liệu:** int. <br> Mặc định: `0` (bị tắt).

### Tham số bổ sung

|  Tham số | Mô tả |
|----------||-------------|
|  |  **Thông số không liên quan**
| `freqai.keras` | Nếu mô hình đã chọn sử dụng Keras (điển hình cho các mô hình dự đoán dựa trên TensorFlow), cờ này cần được kích hoạt để việc lưu/tải mô hình tuân theo các tiêu chuẩn của Keras. <br> **Loại dữ liệu:** Boolean. <br> Mặc định: `Sai`.
| `freqai.conv_width` | Độ rộng của tensor đầu vào mạng thần kinh. Điều này thay thế nhu cầu dịch chuyển nến (`include_shifted_candles`) bằng cách cung cấp các điểm dữ liệu lịch sử dưới dạng chiều thứ hai của tensor. Về mặt kỹ thuật, tham số này cũng có thể được sử dụng cho các biến hồi quy, nhưng nó chỉ bổ sung thêm chi phí tính toán và không thay đổi việc huấn luyện/dự đoán mô hình. <br> **Loại dữ liệu:** Số nguyên. <br> Mặc định: `2`.| `freqai.reduce_df_footprint` | Viết lại tất cả các cột số thành float32/int32, với mục tiêu giảm mức sử dụng ram/đĩa và giảm thời gian đào tạo/suy luận. Tham số này được đặt ở cấp độ chính của tệp cấu hình Freqtrade (không phải bên trong FreqAI). <br> **Loại dữ liệu:** Boolean. <br> Mặc định: `Sai`.
| `freqai.override_exchange_check` | Ghi đè kiểm tra trao đổi để buộc FreqAI sử dụng các trao đổi có thể không có đủ dữ liệu lịch sử. Hãy chuyển điều này thành True nếu bạn biết mô hình và chiến lược FreqAI của mình không yêu cầu dữ liệu lịch sử. <br> **Loại dữ liệu:** Boolean. <br> Mặc định: `Sai`.