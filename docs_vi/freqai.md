<!-- Auto-translated from docs/ by script. Please review technical terms. -->

![freqai-logo](assets/freqai_doc_logo.svg)

# Tần suất AI

## Giới thiệu

FreqAI là phần mềm được thiết kế để tự động hóa nhiều tác vụ khác nhau liên quan đến việc đào tạo mô hình học máy dự đoán nhằm tạo ra các dự báo thị trường dựa trên một tập hợp tín hiệu đầu vào. Nhìn chung, FreqAI đặt mục tiêu trở thành một hộp cát để dễ dàng triển khai các thư viện máy học mạnh mẽ trên dữ liệu thời gian thực ([details](#freqai-position-in-open-source-machine-learning-landscape)).

!!! Ghi chú    FreqAI is, and always will be, a not-for-profit, open source project. FreqAI does *not* have a crypto token, FreqAI does *not* sell signals, and FreqAI does not have a domain besides the present [freqtrade documentation](https://www.freqtrade.io/en/stable/freqai/).
Các tính năng bao gồm:

* **Đào tạo lại tự thích ứng** - Đào tạo lại các mô hình trong quá trình [triển khai trực tiếp](freqai-running.md#live-deployments) để tự thích ứng với thị trường một cách được giám sát
* **Kỹ thuật tính năng nhanh** - Tạo [bộ tính năng](freqai-feature-engineering.md#feature-engineering) (10k+ tính năng) phong phú dựa trên các chiến lược đơn giản do người dùng tạo
* **Hiệu suất cao** - Phân luồng cho phép đào tạo lại mô hình thích ứng trên một luồng riêng biệt (hoặc trên GPU nếu có) từ hoạt động suy luận mô hình (dự đoán) và giao dịch bot. Các mô hình và dữ liệu mới nhất được lưu trong RAM để suy luận nhanh
* **Kiểm tra lại thực tế** - Mô phỏng quá trình đào tạo tự thích ứng trên dữ liệu lịch sử bằng [mô-đun kiểm tra lại](freqai-running.md#backtesting) tự động hóa việc đào tạo lại
* **Khả năng mở rộng** - Kiến trúc tổng quát và mạnh mẽ cho phép kết hợp bất kỳ [thư viện/phương pháp học máy](freqai-configuration.md#using-other-prediction-models) nào có sẵn trong Python. Hiện có sẵn tám ví dụ, bao gồm bộ phân loại, bộ hồi quy và mạng nơ ron tích chập
* **Loại bỏ ngoại lệ thông minh** - Loại bỏ các ngoại lệ khỏi tập dữ liệu huấn luyện và dự đoán bằng nhiều [kỹ thuật phát hiện ngoại lệ](freqai-feature-engineering.md#outlier-Detection)
* **Khả năng phục hồi sau sự cố** - Lưu trữ các mô hình đã được đào tạo vào đĩa để giúp việc tải lại sau sự cố nhanh chóng và dễ dàng, đồng thời [xóa các tệp lỗi thời](freqai-running.md#purging-old-model-data) để duy trì các lần chạy khô/trực tiếp
* **Tự động chuẩn hóa dữ liệu** - [Chuẩn hóa dữ liệu](freqai-feature-engineering.md#building-the-data-pipeline) theo cách thông minh và an toàn về mặt thống kê
* **Tải xuống dữ liệu tự động** - Tính toán khoảng thời gian tải xuống dữ liệu và cập nhật dữ liệu lịch sử (trong quá trình triển khai trực tiếp)
* **Làm sạch dữ liệu đến** - Xử lý NaN một cách an toàn trước khi đào tạo và suy luận mô hình
* **Giảm kích thước** - Giảm kích thước của dữ liệu đào tạo thông qua [Phân tích thành phần chính](freqai-feature-engineering.md#data-directionality-reduction-with-principal-comComponent-analysis)
* **Triển khai nhóm bot** - Đặt một bot để huấn luyện mô hình trong khi nhóm [consumers](producer-consumer.md) sử dụng tín hiệu.

## Bắt đầu nhanh

Cách dễ nhất để kiểm tra nhanh FreqAI là chạy nó ở chế độ khô bằng lệnh sau:```bash
freqtrade trade --config config_examples/config_freqai.example.json --strategy FreqaiExampleStrategy --freqaimodel LightGBMRegressor --strategy-path freqtrade/templates
```Bạn sẽ thấy quá trình khởi động tải xuống dữ liệu tự động, sau đó là đào tạo và giao dịch đồng thời. 

!!! nguy hiểm "Không dành cho sản xuất"
    Chiến lược mẫu được cung cấp cùng với mã nguồn Freqtrade được thiết kế để trình diễn/thử nghiệm nhiều tính năng của FreqAI. Nó cũng được thiết kế để chạy trên các máy tính nhỏ để có thể được sử dụng làm điểm chuẩn giữa nhà phát triển và người dùng. Nó *không* được thiết kế để chạy trong sản xuất.

Bạn có thể tìm thấy chiến lược ví dụ, mô hình dự đoán và cấu hình để sử dụng làm điểm bắt đầu trong
`freqtrade/templates/FreqaiExampleStrategy.py`, `freqtrade/freqai/prediction_models/LightGBMRegressor.py`, và
`config_examples/config_freqai.example.json`, tương ứng.

## Cách tiếp cận chung

Bạn cung cấp cho FreqAI một bộ *chỉ báo cơ sở* tùy chỉnh (giống như trong [chiến lược Freqtrade điển hình](strategy-customization.md)) cũng như các giá trị mục tiêu (*nhãn*). Đối với mỗi cặp trong danh sách trắng, FreqAI đào tạo một mô hình để dự đoán các giá trị mục tiêu dựa trên thông tin đầu vào của các chỉ báo tùy chỉnh. Sau đó, các mô hình sẽ được đào tạo lại một cách nhất quán với tần suất định trước để thích ứng với điều kiện thị trường. FreqAI cung cấp khả năng cho cả chiến lược kiểm tra ngược (mô phỏng thực tế với việc đào tạo lại định kỳ về dữ liệu lịch sử) và triển khai các hoạt động chạy khô/trực tiếp. Trong điều kiện khô/sống, FreqAI có thể được đặt thành đào tạo lại liên tục trong luồng nền để giữ cho các mô hình luôn cập nhật nhất có thể.

Tổng quan về thuật toán, giải thích quy trình xử lý dữ liệu và cách sử dụng mô hình, được hiển thị bên dưới.

![freqai-algo](assets/freqai_algo.jpg)

### Từ vựng học máy quan trọng

**Tính năng** - các tham số, dựa trên dữ liệu lịch sử mà mô hình được đào tạo dựa trên đó. Tất cả các đặc điểm của một cây nến đều được lưu trữ dưới dạng vectơ. Trong FreqAI, bạn xây dựng tập dữ liệu tính năng từ bất kỳ thứ gì bạn có thể xây dựng trong chiến lược.

**Nhãn** - giá trị mục tiêu mà mô hình được huấn luyện hướng tới. Mỗi vectơ đặc trưng được liên kết với một nhãn duy nhất do bạn xác định trong chiến lược. Những nhãn này có chủ ý nhìn về tương lai và là những gì bạn đang huấn luyện mô hình để có thể dự đoán.

**Đào tạo** - quá trình "dạy" mô hình để khớp các bộ tính năng với các nhãn liên quan. Các loại mô hình khác nhau "học" theo những cách khác nhau, điều đó có nghĩa là mô hình này có thể tốt hơn mô hình khác đối với một ứng dụng cụ thể. Bạn có thể tìm thêm thông tin về các mô hình khác nhau đã được triển khai trong FreqAI [tại đây](freqai-configuration.md#USE-other-prediction-models).

**Huấn luyện dữ liệu** - một tập hợp con của tập dữ liệu tính năng được cung cấp cho mô hình trong quá trình đào tạo để "dạy" mô hình cách dự đoán mục tiêu. Dữ liệu này ảnh hưởng trực tiếp đến kết nối trọng lượng trong mô hình.

**Dữ liệu thử nghiệm** - một tập hợp con của bộ dữ liệu tính năng được sử dụng để đánh giá hiệu suất của mô hình sau khi đào tạo. Dữ liệu này không ảnh hưởng đến trọng số nút trong mô hình.

**Suy luận** - quá trình cung cấp dữ liệu mới chưa được nhìn thấy cho mô hình đã được đào tạo để đưa ra dự đoán. 

## Cài đặt điều kiện tiên quyết

Quá trình cài đặt Freqtrade thông thường sẽ hỏi bạn có muốn cài đặt các phần phụ thuộc FreqAI hay không. Bạn nên trả lời "có" cho câu hỏi này nếu bạn muốn sử dụng FreqAI. Nếu bạn không trả lời có, bạn có thể cài đặt thủ công các phần phụ thuộc này sau khi cài đặt bằng:``` bash
pip install -r requirements-freqai.txt
```!!! Lưu ý
    Catboost sẽ không được cài đặt trên các thiết bị có công suất thấp (mâm xôi) vì nó không cung cấp bánh xe cho nền tảng này.

### Cách sử dụng với docker

Nếu bạn đang sử dụng docker, một thẻ chuyên dụng có phần phụ thuộc FreqAI sẽ có sẵn dưới dạng `:freqai`. Như vậy - bạn có thể thay thế dòng hình ảnh trong tệp soạn thảo docker của mình bằng `image: freqtradeorg/freqtrade:stable_freqai`. Hình ảnh này chứa các phần phụ thuộc FreqAI thông thường. Tương tự như các bản cài đặt gốc, Catboost sẽ không khả dụng trên các thiết bị dựa trên ARM. Nếu bạn muốn sử dụng PyTorch hoặc Học tăng cường, bạn nên sử dụng thẻ đuốc hoặc thẻ RL, `image: freqtradeorg/freqtrade:stable_freqaitorch`, `image: freqtradeorg/freqtrade:stable_freqaitorl`.

!!! lưu ý "docker-compose-freqai.yml"
    Chúng tôi cung cấp tệp soạn thảo docker rõ ràng cho điều này trong `docker/docker-compose-freqai.yml` - có thể được sử dụng thông qua `docker soạn -f docker/docker-compose-freqai.yml run ...` - hoặc có thể được sao chép để thay thế tệp docker gốc. Tệp soạn thảo docker này cũng chứa một phần (đã bị vô hiệu hóa) để kích hoạt tài nguyên GPU trong vùng chứa docker. Điều này rõ ràng giả định rằng hệ thống có sẵn tài nguyên GPU.

### Vị trí của FreqAI trong bối cảnh học máy nguồn mở

Dự báo các hệ thống dựa trên chuỗi thời gian hỗn loạn, chẳng hạn như thị trường chứng khoán/tiền điện tử, đòi hỏi một bộ công cụ rộng rãi hướng đến việc thử nghiệm nhiều giả thuyết. May mắn thay, sự trưởng thành gần đây của các thư viện máy học mạnh mẽ (ví dụ: `scikit-learn`) đã mở ra nhiều khả năng nghiên cứu. Giờ đây, các nhà khoa học từ nhiều lĩnh vực khác nhau có thể dễ dàng tạo nguyên mẫu nghiên cứu của họ về vô số thuật toán học máy đã được thiết lập. Tương tự, các thư viện thân thiện với người dùng này cho phép "các nhà khoa học công dân" sử dụng các kỹ năng Python cơ bản của họ để khám phá dữ liệu. Tuy nhiên, việc tận dụng các thư viện máy học này trên các nguồn dữ liệu hỗn loạn hiện tại và lịch sử có thể khó khăn và tốn kém về mặt hậu cần. Ngoài ra, việc thu thập, lưu trữ và xử lý dữ liệu hiệu quả cũng là một thách thức khác nhau. [`FreqAI`](#freqai) nhằm mục đích cung cấp một khung nguồn mở tổng quát và có thể mở rộng nhằm mục đích triển khai trực tiếp mô hình thích ứng để dự báo thị trường. Khung `FreqAI` thực sự là một hộp cát cho thế giới phong phú của các thư viện máy học nguồn mở. Bên trong hộp cát `FreqAI`, người dùng nhận thấy họ có thể kết hợp nhiều thư viện của bên thứ ba để kiểm tra các giả thuyết sáng tạo trên nguồn dữ liệu hỗn loạn trực tiếp 24/7 miễn phí - dữ liệu trao đổi tiền điện tử. 

### Tần suất trích dẫnAIFreqAI is [published in the Journal of Open Source Software](https://joss.theoj.org/papers/10.21105/joss.04864). If you find FreqAI useful in your research, please use the following citation:
```bibtex
@article{Caulk2022, 
    doi = {10.21105/joss.04864},
    url = {https://doi.org/10.21105/joss.04864},
    year = {2022}, publisher = {The Open Journal},
    volume = {7}, number = {80}, pages = {4864},
    author = {Robert A. Caulk and Elin Törnquist and Matthias Voppichler and Andrew R. Lawless and Ryan McMullan and Wagner Costa Santos and Timothy C. Pogue and Johan van der Vlugt and Stefan P. Gehring and Pascal Schmidt},
    title = {FreqAI: generalizing adaptive modeling for chaotic time-series market forecasts},
    journal = {Journal of Open Source Software} } 
```## Những cạm bẫy thường gặp

Không thể kết hợp FreqAI với `VolumePairlists` động (hoặc bất kỳ bộ lọc danh sách cặp nào thêm và xóa các cặp một cách linh hoạt).
Điều này là vì lý do hiệu suất - FreqAI dựa vào việc đưa ra dự đoán/đào tạo lại nhanh chóng. Để làm được điều này một cách hiệu quả,
nó cần tải xuống tất cả dữ liệu huấn luyện khi bắt đầu phiên bản khô/trực tiếp. FreqAI lưu trữ và bổ sung
nến mới tự động cho các lần đào tạo lại trong tương lai. Điều này có nghĩa là nếu các cặp mới đến muộn hơn trong quá trình chạy khô do danh sách cặp âm lượng, thì dữ liệu đó sẽ không có sẵn. Tuy nhiên, FreqAI hoạt động với `ShufflePairlist` hoặc `VolumePairlist` để giữ cho tổng danh sách cặp không đổi (nhưng sắp xếp lại các cặp theo âm lượng).

## Tài liệu học tập bổ sung

Ở đây chúng tôi biên soạn một số tài liệu bên ngoài giúp cung cấp cái nhìn sâu hơn về các thành phần khác nhau của FreqAI:- [Real-time head-to-head: Adaptive modeling of financial market data using XGBoost and CatBoost](https://emergentmethods.medium.com/real-time-head-to-head-adaptive-modeling-of-financial-market-data-using-xgboost-and-catboost-995a115a7495)
- [FreqAI - from price to prediction](https://emergentmethods.medium.com/freqai-from-price-to-prediction-6fadac18b665)
## Ủng hộYou can find support for FreqAI in a variety of places, including the [Freqtrade discord](https://discord.gg/Jd8JYeWHc4), the dedicated [FreqAI discord](https://discord.gg/7AMWACmbjT), and in [github issues](https://github.com/freqtrade/freqtrade/issues).
## Tín dụng

FreqAI được phát triển bởi một nhóm cá nhân, những người đều đóng góp các kỹ năng cụ thể cho dự án.

Ý tưởng và phát triển phần mềm:
Robert Caulk @robcaulk

Tư duy lý thuyết và phân tích dữ liệu:
Elin Tornquist @th0rntwig

Đánh giá mã và động não về kiến trúc phần mềm:
@xmatthias

Phát triển phần mềm:
Wagner Costa @wagnercosta
Emre Suzen @aemr3
Timothy Pogue @wizrds

Thử nghiệm beta và báo cáo lỗi:
Stefan Gehring @bloodhunter4rc, @longyu, Andrew Lawless @paranoidandy, Pascal Schmidt @smidelis, Ryan McMullan @smarmau, Juha Nykänen @suikula, Johan van der Vlugt @jooopiert, Richárd Józsa @richardjosza