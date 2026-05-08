<!-- Auto-translated from docs/ by script. Please review technical terms. -->

# Phát triển

## Kiến trúc dự án

Kiến trúc và chức năng của FreqAI được khái quát hóa để khuyến khích phát triển các tính năng, chức năng, mô hình độc đáo, v.v.

Cấu trúc lớp và tổng quan thuật toán chi tiết được mô tả trong sơ đồ sau:

![hình ảnh](tài sản/freqai_algorithm-diagram.jpg)

Như được hiển thị, có ba đối tượng riêng biệt bao gồm FreqAI:

* **IFreqaiModel** - Một đối tượng liên tục duy nhất chứa tất cả logic cần thiết để thu thập, lưu trữ và xử lý dữ liệu, tính năng kỹ sư, chạy đào tạo và mô hình suy luận.
* **FreqaiDataKitchen** - Một đối tượng không cố định được tạo duy nhất cho từng nội dung/mô hình duy nhất. Ngoài siêu dữ liệu, nó còn chứa nhiều công cụ xử lý dữ liệu.
* **FreqaiDataDrawer** - Một đối tượng liên tục duy nhất chứa tất cả các dự đoán, mô hình và phương thức lưu/tải lịch sử.

Có nhiều [mô hình dự đoán] tích hợp sẵn (freqai-configuration.md#USE-other-prediction-models) kế thừa trực tiếp từ `IFreqaiModel`. Mỗi mô hình này có toàn quyền truy cập vào tất cả các phương thức trong `IFreqaiModel` và do đó có thể ghi đè bất kỳ chức năng nào trong số đó theo ý muốn. Tuy nhiên, người dùng nâng cao có thể sẽ tiếp tục ghi đè `fit()`, `train()`, `predict()` và `data_cleaning_train/predict()`.

## Xử lý dữ liệu

FreqAI hướng tới việc tổ chức các tệp mô hình, dữ liệu dự đoán và siêu dữ liệu theo cách đơn giản hóa quá trình xử lý hậu kỳ và tăng cường khả năng phục hồi sau sự cố bằng cách tải lại dữ liệu tự động. Dữ liệu được lưu trong cấu trúc tệp,`user_data_dir/models/`, chứa tất cả dữ liệu liên quan đến quá trình đào tạo và kiểm tra ngược. `FreqaiDataKitchen()` phụ thuộc rất nhiều vào cấu trúc tệp để đào tạo và suy luận phù hợp và do đó không nên sửa đổi theo cách thủ công.

### Cấu trúc tập tin

Cấu trúc tệp được tạo tự động dựa trên `mã định danh` mô hình được đặt trong [config](freqai-configuration.md#setting-up-the-configuration-file). Cấu trúc sau đây hiển thị nơi dữ liệu được lưu trữ để xử lý bài đăng:

| Cấu trúc | Mô tả |
|----------||-------------|
| `config_*.json` | Một bản sao của tệp cấu hình cụ thể của mô hình. |
| `history_predictions.pkl` | Một tệp chứa tất cả các dự đoán lịch sử được tạo trong suốt vòng đời của mô hình `mã định danh` trong quá trình triển khai trực tiếp. `histocal_predictions.pkl` được sử dụng để tải lại mô hình sau khi xảy ra sự cố hoặc thay đổi cấu hình. Một tập tin sao lưu luôn được giữ lại trong trường hợp tập tin chính bị hỏng. FreqAI **tự động** phát hiện lỗi và thay thế tệp bị lỗi bằng bản sao lưu. |
| `pair_dictionary.json` | Một tệp chứa hàng huấn luyện cũng như vị trí trên đĩa của mô hình được huấn luyện gần đây nhất. |
| `tàu phụ-*_TIMESTAMP` | Một thư mục chứa tất cả các tệp được liên kết với một mô hình, chẳng hạn như: <br>
|| `*_metadata.json` - Siêu dữ liệu cho mô hình, chẳng hạn như mức tối đa/phút chuẩn hóa, danh sách tính năng đào tạo dự kiến, v.v. <br>
|| `*_model.*` - Tệp mô hình được lưu vào đĩa để tải lại sau khi gặp sự cố. Có thể là `joblib` (lib tăng cường điển hình), `zip` (stable_baselines), `hd5` (loại máy ảnh), v.v. <br>
|| `*_pca_object.pkl` - Biến đổi [Phân tích thành phần chính (PCA)](freqai-feature-engineering.md#data-directionality-reduction-with-principal-comComponent-analysis) (nếu `principal_comComponent_analysis: True` được đặt trong cấu hình) sẽ được sử dụng để chuyển đổi các tính năng dự đoán không nhìn thấy. <br>|| `*_svm_model.pkl` - Mô hình [Máy ​​vectơ hỗ trợ (SVM)](freqai-feature-engineering.md#identifying-outliers-USE-a-support-vector-machine-svm) (nếu `use_SVM_to_remove_outliers: True` được đặt trong cấu hình) được sử dụng để phát hiện các ngoại lệ trong các tính năng dự đoán không nhìn thấy. <br>
|| `*_training_df.pkl` - Khung dữ liệu chứa tất cả các tính năng huấn luyện được sử dụng để huấn luyện mô hình `định danh`. Điều này được sử dụng để tính toán [Chỉ số khác biệt (DI)](freqai-feature-engineering.md#identifying-outliers-with-the-dissimilarity-index-di) và cũng có thể được sử dụng để xử lý hậu kỳ. <br>
|| `*_training_dates.df.pkl` - Ngày được liên kết với `trained_df.pkl`, rất hữu ích cho việc xử lý hậu kỳ. |

Cấu trúc tệp ví dụ sẽ trông như thế này:```
├── models
│   └── unique-id
│       ├── config_freqai.example.json
│       ├── historic_predictions.backup.pkl
│       ├── historic_predictions.pkl
│       ├── pair_dictionary.json
│       ├── sub-train-1INCH_1662821319
│       │   ├── cb_1inch_1662821319_metadata.json
│       │   ├── cb_1inch_1662821319_model.joblib
│       │   ├── cb_1inch_1662821319_pca_object.pkl
│       │   ├── cb_1inch_1662821319_svm_model.joblib
│       │   ├── cb_1inch_1662821319_trained_dates_df.pkl
│       │   └── cb_1inch_1662821319_trained_df.pkl
│       ├── sub-train-1INCH_1662821371
│       │   ├── cb_1inch_1662821371_metadata.json
│       │   ├── cb_1inch_1662821371_model.joblib
│       │   ├── cb_1inch_1662821371_pca_object.pkl
│       │   ├── cb_1inch_1662821371_svm_model.joblib
│       │   ├── cb_1inch_1662821371_trained_dates_df.pkl
│       │   └── cb_1inch_1662821371_trained_df.pkl
│       ├── sub-train-ADA_1662821344
│       │   ├── cb_ada_1662821344_metadata.json
│       │   ├── cb_ada_1662821344_model.joblib
│       │   ├── cb_ada_1662821344_pca_object.pkl
│       │   ├── cb_ada_1662821344_svm_model.joblib
│       │   ├── cb_ada_1662821344_trained_dates_df.pkl
│       │   └── cb_ada_1662821344_trained_df.pkl
│       └── sub-train-ADA_1662821399
│           ├── cb_ada_1662821399_metadata.json
│           ├── cb_ada_1662821399_model.joblib
│           ├── cb_ada_1662821399_pca_object.pkl
│           ├── cb_ada_1662821399_svm_model.joblib
│           ├── cb_ada_1662821399_trained_dates_df.pkl
│           └── cb_ada_1662821399_trained_df.pkl

```