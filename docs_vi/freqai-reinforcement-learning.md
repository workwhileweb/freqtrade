<!-- Auto-translated from docs/ by script. Please review technical terms. -->

# Học tăng cường

!!! Lưu ý "Kích thước cài đặt"
    Các phần phụ thuộc của học tăng cường bao gồm các gói lớn chẳng hạn như `torch`, cần được yêu cầu rõ ràng trong `./setup.sh -i` bằng cách trả lời "y" cho câu hỏi "Bạn cũng muốn các gói phụ thuộc cho freqai-rl (cần thêm ~700mb dung lượng) [y/N]?".
    Người dùng thích docker nên đảm bảo họ sử dụng hình ảnh docker được gắn với `_freqairl`.

## Bối cảnh và thuật ngữ

### RL là gì và tại sao FreqAI cần nó?

Học tăng cường bao gồm hai thành phần quan trọng, *tác nhân* và *môi trường* đào tạo. Trong quá trình đào tạo đại lý, đại lý di chuyển qua từng nến dữ liệu lịch sử, luôn thực hiện 1 trong số các hành động: Vào lệnh mua, thoát lệnh dài, vào lệnh bán khống, thoát lệnh bán khống, trung tính). Trong quá trình đào tạo này, môi trường theo dõi hiệu suất của những hành động này và trao thưởng cho tổng đài viên theo `Calculate_reward()` do người dùng tùy chỉnh thực hiện (ở đây chúng tôi cung cấp phần thưởng mặc định để người dùng tiếp tục xây dựng nếu họ muốn [chi tiết tại đây](#creating-a-custom-reward-function)). Phần thưởng được sử dụng để huấn luyện trọng lượng trong mạng lưới thần kinh.

Thành phần quan trọng thứ hai trong quá trình triển khai FreqAI RL là việc sử dụng thông tin *trạng thái*. Thông tin trạng thái được đưa vào mạng ở mỗi bước, bao gồm lợi nhuận hiện tại, vị thế hiện tại và thời gian giao dịch hiện tại. Chúng được sử dụng để đào tạo tác nhân trong môi trường đào tạo và củng cố tác nhân ở trạng thái khô/trực tiếp (chức năng này không có sẵn trong quá trình kiểm tra ngược). *FreqAI + Freqtrade là sự kết hợp hoàn hảo cho cơ chế tăng cường này vì thông tin này luôn có sẵn trong quá trình triển khai trực tiếp.*

Học tăng cường là một tiến trình tự nhiên đối với FreqAI, vì nó bổ sung thêm một lớp mới về khả năng thích ứng và phản ứng thị trường mà Bộ phân loại và Bộ hồi quy không thể sánh được. Tuy nhiên, Bộ phân loại và Bộ hồi quy có những điểm mạnh mà RL không có, chẳng hạn như khả năng dự đoán mạnh mẽ. Các đại lý RL được đào tạo không đúng cách có thể tìm ra "gian lận" và "thủ thuật" để tối đa hóa phần thưởng mà không thực sự thắng bất kỳ giao dịch nào. Vì lý do này, RL phức tạp hơn và đòi hỏi mức độ hiểu biết cao hơn các Bộ phân loại và Bộ hồi quy thông thường.

### Giao diện RL

Với khung hiện tại, chúng tôi mong muốn hiển thị môi trường đào tạo thông qua tệp "mô hình dự đoán" chung, là đối tượng `BaseReinforcementLearner` được kế thừa bởi người dùng (ví dụ: `freqai/prediction_models/ReinforcementLearner`). Bên trong lớp người dùng này, môi trường RL có sẵn và được tùy chỉnh thông qua `MyRLEnv` như [hiển thị bên dưới](#creating-a-custom-reward-function).

Chúng tôi hình dung rằng phần lớn người dùng đang tập trung nỗ lực vào thiết kế sáng tạo của hàm `calate_reward()` [chi tiết tại đây](#creating-a-custom-reward-function), trong khi không chạm tới phần còn lại của môi trường. Những người dùng khác hoàn toàn không thể chạm vào môi trường và họ sẽ chỉ chơi với các cài đặt cấu hình và kỹ thuật tính năng mạnh mẽ đã tồn tại trong FreqAI. Trong khi đó, chúng tôi cho phép người dùng nâng cao tạo hoàn toàn các lớp mô hình của riêng họ.

Khung này được xây dựng trên stable_baselines3 (đèn pin) và phòng tập OpenAI cho lớp môi trường cơ sở. Nhưng nói chung, lớp mô hình được cách ly tốt. Do đó, việc bổ sung các thư viện cạnh tranh có thể dễ dàng được tích hợp vào khung hiện có. Đối với môi trường, nó kế thừa từ `gym.Env`, nghĩa là cần phải viết một môi trường hoàn toàn mới để chuyển sang một thư viện khác.

### Những cân nhắc quan trọngNhư đã giải thích ở trên, đại lý được "đào tạo" trong một "môi trường" giao dịch nhân tạo. Trong trường hợp của chúng tôi, môi trường đó có vẻ khá giống với môi trường kiểm tra lại Freqtrade thực sự, nhưng nó *KHÔNG*. Trên thực tế, môi trường đào tạo RL đơn giản hơn nhiều. Nó không kết hợp bất kỳ logic chiến lược phức tạp nào, chẳng hạn như các lệnh gọi lại như `custom_exit`, `custom_stoploss`, kiểm soát đòn bẩy, v.v. Thay vào đó, môi trường RL là sự thể hiện rất "thô" của thị trường thực sự, nơi đại lý có quyền tự do tìm hiểu chính sách (đọc: dừng lỗ, chốt lời, v.v.) được thực thi bởi `tính toán_reward()`. Vì vậy, điều quan trọng cần lưu ý là môi trường đào tạo tác nhân không giống với thế giới thực.

## Học tăng cường chạy bộ

Thiết lập và chạy mô hình Học tăng cường cũng giống như chạy Công cụ hồi quy hoặc Trình phân loại. Hai cờ giống nhau, `--freqaimodel` và `--strategy`, phải được xác định trên dòng lệnh:```bash
freqtrade trade --freqaimodel ReinforcementLearner --strategy MyRLStrategy --config config.json
```trong đó `ReinforcementLearner` sẽ sử dụng `ReinforcementLearner` theo mẫu từ `freqai/prediction_models/ReinforcementLearner` (hoặc một người dùng tùy chỉnh đã xác định một mẫu nằm trong `user_data/freqaimodels`). Mặt khác, chiến lược tuân theo cùng một cơ sở [kỹ thuật tính năng](freqai-feature-engineering.md) với `feature_engineering_*` là một Công cụ hồi quy điển hình. Sự khác biệt nằm ở việc tạo ra các mục tiêu, Học tăng cường không yêu cầu chúng. Tuy nhiên, FreqAI yêu cầu đặt giá trị mặc định (trung tính) trong cột hành động:```python
    def set_freqai_targets(self, dataframe, **kwargs) -> DataFrame:
        """
        *Only functional with FreqAI enabled strategies*
        Required function to set the targets for the model.
        All targets must be prepended with `&` to be recognized by the FreqAI internals.

        More details about feature engineering available:

        https://www.freqtrade.io/en/stable/freqai-feature-engineering

        :param df: strategy dataframe which will receive the targets
        usage example: dataframe["&-target"] = dataframe["close"].shift(-1) / dataframe["close"]
        """
        # For RL, there are no direct targets to set. This is filler (neutral)
        # until the agent sends an action.
        dataframe["&-action"] = 0
        return dataframe
```Hầu hết chức năng vẫn giống như đối với các Công cụ hồi quy thông thường, tuy nhiên, chức năng bên dưới cho thấy cách chiến lược phải chuyển dữ liệu giá thô cho đại lý để nó có quyền truy cập vào OHLCV thô trong môi trường đào tạo:```python
    def feature_engineering_standard(self, dataframe: DataFrame, **kwargs) -> DataFrame:
        # The following features are necessary for RL models
        dataframe[f"%-raw_close"] = dataframe["close"]
        dataframe[f"%-raw_open"] = dataframe["open"]
        dataframe[f"%-raw_high"] = dataframe["high"]
        dataframe[f"%-raw_low"] = dataframe["low"]
    return dataframe
```Cuối cùng, không có "nhãn" rõ ràng nào để tạo - thay vào đó cần gán cột `&-action` sẽ chứa các hành động của tác nhân khi được truy cập trong `populate_entry/exit_trends()`. Trong ví dụ hiện tại, hành động trung lập là 0. Giá trị này phải phù hợp với môi trường được sử dụng. FreqAI cung cấp hai môi trường, cả hai đều sử dụng 0 làm hành động trung lập.

Sau khi người dùng nhận ra rằng không có nhãn nào để đặt, họ sẽ sớm hiểu rằng tác nhân đang đưa ra quyết định ra vào "của riêng mình". Điều này làm cho việc xây dựng chiến lược khá đơn giản. Các tín hiệu vào và thoát đến từ tác nhân dưới dạng số nguyên - được sử dụng trực tiếp để quyết định các mục nhập và thoát trong chiến lược:```python
    def populate_entry_trend(self, df: DataFrame, metadata: dict) -> DataFrame:

        enter_long_conditions = [df["do_predict"] == 1, df["&-action"] == 1]

        if enter_long_conditions:
            df.loc[
                reduce(lambda x, y: x & y, enter_long_conditions), ["enter_long", "enter_tag"]
            ] = (1, "long")

        enter_short_conditions = [df["do_predict"] == 1, df["&-action"] == 3]

        if enter_short_conditions:
            df.loc[
                reduce(lambda x, y: x & y, enter_short_conditions), ["enter_short", "enter_tag"]
            ] = (1, "short")

        return df

    def populate_exit_trend(self, df: DataFrame, metadata: dict) -> DataFrame:
        exit_long_conditions = [df["do_predict"] == 1, df["&-action"] == 2]
        if exit_long_conditions:
            df.loc[reduce(lambda x, y: x & y, exit_long_conditions), "exit_long"] = 1

        exit_short_conditions = [df["do_predict"] == 1, df["&-action"] == 4]
        if exit_short_conditions:
            df.loc[reduce(lambda x, y: x & y, exit_short_conditions), "exit_short"] = 1

        return df
```Điều quan trọng cần lưu ý là `&-action` phụ thuộc vào môi trường mà chúng chọn sử dụng. Ví dụ trên hiển thị 5 hành động, trong đó 0 là trung lập, 1 là nhập long, 2 là thoát long, 3 là nhập ngắn và 4 là thoát ngắn.

## Định cấu hình Người học tăng cường

Để định cấu hình `Người học tăng cường`, từ điển sau phải tồn tại trong cấu hình `freqai`:```json
        "rl_config": {
            "train_cycles": 25,
            "add_state_info": true,
            "max_trade_duration_candles": 300,
            "max_training_drawdown_pct": 0.02,
            "cpu_count": 8,
            "model_type": "PPO",
            "policy_type": "MlpPolicy",
            "model_reward_parameters": {
                "rr": 1,
                "profit_aim": 0.025
            }
        }
```Parameter details can be found [here](freqai-parameter-table.md), but in general the `train_cycles` decides how many times the agent should cycle through the candle data in its artificial environment to train weights in the model. `model_type` is a string which selects one of the available models in [stable_baselines](https://stable-baselines3.readthedocs.io/en/master/)(external link).
!!! Lưu ý
    Nếu bạn muốn thử nghiệm `continual_learning` thì bạn nên đặt giá trị đó thành `true` trong từ điển cấu hình `freqai` chính. Điều này sẽ yêu cầu thư viện Học tăng cường tiếp tục đào tạo các mô hình mới từ trạng thái cuối cùng của các mô hình trước đó, thay vì đào tạo lại các mô hình mới từ đầu mỗi khi bắt đầu đào tạo lại.

!!! Ghi chú    Remember that the general `model_training_parameters` dictionary should contain all the model hyperparameter customizations for the particular `model_type`. For example, `PPO` parameters can be found [here](https://stable-baselines3.readthedocs.io/en/master/modules/ppo.html).
## Tạo chức năng phần thưởng tùy chỉnh

!!! nguy hiểm "Không dành cho sản xuất"
    Cảnh báo!
    Chức năng phần thưởng được cung cấp cùng với mã nguồn Freqtrade là sự giới thiệu chức năng được thiết kế để hiển thị/kiểm tra càng nhiều tính năng kiểm soát môi trường càng tốt. Nó cũng được thiết kế để chạy nhanh trên các máy tính nhỏ. Đây là điểm chuẩn, *không* dành cho sản xuất trực tiếp. Xin lưu ý rằng bạn sẽ cần tạo hàm custom_reward() của riêng mình hoặc sử dụng mẫu được tạo bởi những người dùng khác bên ngoài mã nguồn Freqtrade.

Khi bạn bắt đầu sửa đổi chiến lược và mô hình dự đoán, bạn sẽ nhanh chóng nhận ra một số khác biệt quan trọng giữa Người học tăng cường và Người hồi quy/Người phân loại. Thứ nhất, chiến lược không đặt giá trị mục tiêu (không có nhãn!). Thay vào đó, bạn đặt hàm `calcate_reward()` bên trong lớp `MyRLEnv` (xem bên dưới). Một `tính_reward()` mặc định được cung cấp bên trong `prediction_models/ReinforcementLearner.py` để minh họa các khối xây dựng cần thiết để tạo phần thưởng, nhưng đây *không* được thiết kế cho sản xuất. Người dùng *phải* tạo lớp mô hình học tăng cường tùy chỉnh của riêng mình hoặc sử dụng lớp mô hình được tạo sẵn từ bên ngoài mã nguồn Freqtrade và lưu nó vào `user_data/freqaimodels`. Nó nằm bên trong `feature_reward()` nơi có thể thể hiện các lý thuyết sáng tạo về thị trường. Ví dụ: bạn có thể thưởng cho đại lý của mình khi họ thực hiện giao dịch thắng và phạt đại lý khi thực hiện giao dịch thua lỗ. Hoặc có lẽ bạn muốn thưởng cho đại lý vì đã tham gia giao dịch và phạt đại lý vì đã ngồi giao dịch quá lâu. Dưới đây chúng tôi trình bày các ví dụ về cách tính toán tất cả các phần thưởng này:

!!! lưu ý "Gợi ý"
    Chức năng khen thưởng tốt nhất là chức năng có thể phân biệt liên tục và có quy mô phù hợp. Nói cách khác, việc thêm một hình phạt tiêu cực lớn vào một sự kiện hiếm gặp không phải là một ý tưởng hay và mạng lưới thần kinh sẽ không thể học được chức năng đó. Thay vào đó, tốt hơn là thêm một hình phạt tiêu cực nhỏ vào một sự kiện chung. Điều này sẽ giúp đại lý học nhanh hơn. Không chỉ điều này, bạn còn có thể giúp cải thiện tính liên tục của các phần thưởng/hình phạt bằng cách điều chỉnh chúng theo mức độ nghiêm trọng theo một số hàm tuyến tính/số mũ. Nói cách khác, bạn sẽ tăng dần mức phạt khi thời gian giao dịch tăng lên. Điều này tốt hơn là một hình phạt lớn duy nhất xảy ra tại một thời điểm.```python
from freqtrade.freqai.prediction_models.ReinforcementLearner import ReinforcementLearner
from freqtrade.freqai.RL.Base5ActionRLEnv import Actions, Base5ActionRLEnv, Positions


class MyCoolRLModel(ReinforcementLearner):
    """
    User created RL prediction model.

    Save this file to `freqtrade/user_data/freqaimodels`

    then use it with:

    freqtrade trade --freqaimodel MyCoolRLModel --config config.json --strategy SomeCoolStrat

    Here the users can override any of the functions
    available in the `IFreqaiModel` inheritance tree. Most importantly for RL, this
    is where the user overrides `MyRLEnv` (see below), to define custom
    `calculate_reward()` function, or to override any other parts of the environment.

    This class also allows users to override any other part of the IFreqaiModel tree.
    For example, the user can override `def fit()` or `def train()` or `def predict()`
    to take fine-tuned control over these processes.

    Another common override may be `def data_cleaning_predict()` where the user can
    take fine-tuned control over the data handling pipeline.
    """
    class MyRLEnv(Base5ActionRLEnv):
        """
        User made custom environment. This class inherits from BaseEnvironment and gym.Env.
        Users can override any functions from those parent classes. Here is an example
        of a user customized `calculate_reward()` function.

        Warning!
        This is function is a showcase of functionality designed to show as many possible
        environment control features as possible. It is also designed to run quickly
        on small computers. This is a benchmark, it is *not* for live production.
        """
        def calculate_reward(self, action: int) -> float:
            # first, penalize if the action is not valid
            if not self._is_valid(action):
                return -2
            pnl = self.get_unrealized_profit()

            factor = 100

            pair = self.pair.replace(':', '')

            # you can use feature values from dataframe
            # Assumes the shifted RSI indicator has been generated in the strategy.
            rsi_now = self.raw_features[f"%-rsi-period_10_shift-1_{pair}_"
                            f"{self.config['timeframe']}"].iloc[self._current_tick]

            # reward agent for entering trades
            if (action in (Actions.Long_enter.value, Actions.Short_enter.value)
                    and self._position == Positions.Neutral):
                if rsi_now < 40:
                    factor = 40 / rsi_now
                else:
                    factor = 1
                return 25 * factor

            # discourage agent from not entering trades
            if action == Actions.Neutral.value and self._position == Positions.Neutral:
                return -1
            max_trade_duration = self.rl_config.get('max_trade_duration_candles', 300)
            trade_duration = self._current_tick - self._last_trade_tick
            if trade_duration <= max_trade_duration:
                factor *= 1.5
            elif trade_duration > max_trade_duration:
                factor *= 0.5
            # discourage sitting in position
            if self._position in (Positions.Short, Positions.Long) and \
            action == Actions.Neutral.value:
                return -1 * trade_duration / max_trade_duration
            # close long
            if action == Actions.Long_exit.value and self._position == Positions.Long:
                if pnl > self.profit_aim * self.rr:
                    factor *= self.rl_config['model_reward_parameters'].get('win_reward_factor', 2)
                return float(pnl * factor)
            # close short
            if action == Actions.Short_exit.value and self._position == Positions.Short:
                if pnl > self.profit_aim * self.rr:
                    factor *= self.rl_config['model_reward_parameters'].get('win_reward_factor', 2)
                return float(pnl * factor)
            return 0.
```## Sử dụng Tensorboard

Các mô hình Học tăng cường được hưởng lợi từ việc theo dõi các số liệu đào tạo. FreqAI đã tích hợp Tensorboard để cho phép người dùng theo dõi hiệu suất đào tạo và đánh giá trên tất cả các đồng tiền và trên tất cả các khóa đào tạo lại. Tensorboard được kích hoạt thông qua lệnh sau:```bash
tensorboard --logdir user_data/models/unique-id
```trong đó `unique-id` là `mã định danh` được đặt trong tệp cấu hình `freqai`. Lệnh này phải được chạy trong một shell riêng để xem kết quả đầu ra trong trình duyệt tại 127.0.0.1:6006 (6006 là cổng mặc định được Tensorboard sử dụng).

![tensorboard](assets/tensorboard.jpg)

## Ghi nhật ký tùy chỉnh

FreqAI cũng cung cấp một trình ghi nhật ký tóm tắt theo từng tập tích hợp có tên là `self.tensorboard_log` để thêm thông tin tùy chỉnh vào nhật ký Tensorboard. Theo mặc định, hàm này đã được gọi một lần mỗi bước trong môi trường để ghi lại các hành động của tổng đài viên. Tất cả giá trị tích lũy cho tất cả các bước trong một tập sẽ được báo cáo vào cuối mỗi tập, sau đó là đặt lại toàn bộ tất cả các chỉ số về 0 để chuẩn bị cho tập tiếp theo.

`self.tensorboard_log` cũng có thể được sử dụng ở bất cứ đâu trong môi trường, ví dụ: nó có thể được thêm vào hàm `calate_reward` để thu thập thông tin chi tiết hơn về tần suất các phần khác nhau của phần thưởng được gọi:```python
    class MyRLEnv(Base5ActionRLEnv):
        """
        User made custom environment. This class inherits from BaseEnvironment and gym.Env.
        Users can override any functions from those parent classes. Here is an example
        of a user customized `calculate_reward()` function.
        """
        def calculate_reward(self, action: int) -> float:
            if not self._is_valid(action):
                self.tensorboard_log("invalid")
                return -2

```!!! Lưu ý
    Hàm `self.tensorboard_log()` được thiết kế để chỉ theo dõi các đối tượng tăng dần, tức là các sự kiện, hành động bên trong môi trường đào tạo. Nếu sự kiện quan tâm là số float thì số float có thể được chuyển làm đối số thứ hai, ví dụ: `self.tensorboard_log("float_metric1", 0,23)`. Trong trường hợp này các giá trị số liệu không được tăng lên.

## Chọn môi trường cơ sở

FreqAI cung cấp ba môi trường cơ bản, `Base3ActionRLEnvironment`, `Base4ActionEnvironment` và `Base5ActionEnvironment`. Đúng như tên gọi, môi trường được tùy chỉnh cho các tổng đài viên có thể chọn từ 3, 4 hoặc 5 hành động. `Base3ActionEnvironment` là đơn giản nhất, tác nhân có thể chọn giữ, mua hoặc bán. Môi trường này cũng có thể được sử dụng cho các bot chỉ dài (nó tự động tuân theo cờ `can_short` từ chiến lược), trong đó dài là điều kiện nhập và ngắn là điều kiện thoát. Trong khi đó, trong `Base4ActionEnvironment`, tác nhân có thể vào lệnh mua, lệnh bán, giữ vị trí trung lập hoặc thoát. Cuối cùng, trong `Base5ActionEnvironment`, tác nhân có các hành động tương tự như Base4, nhưng thay vì một hành động thoát duy nhất, nó tách biệt thoát dài và thoát ngắn. Những thay đổi chính xuất phát từ việc lựa chọn môi trường bao gồm:

* các hành động có sẵn trong `price_reward`
* các hành động được thực hiện bởi chiến lược người dùng

Tất cả các môi trường do FreqAI cung cấp đều kế thừa từ một đối tượng môi trường bất khả tri về hành động/vị trí được gọi là `BaseEnvironment`, chứa tất cả logic được chia sẻ. Kiến trúc được thiết kế để dễ dàng tùy chỉnh. Tùy chỉnh đơn giản nhất là `calate_reward()` (xem chi tiết [tại đây](#creating-a-custom-reward-function)). Tuy nhiên, các tùy chỉnh có thể được mở rộng hơn nữa sang bất kỳ chức năng nào trong môi trường. Bạn có thể thực hiện việc này bằng cách ghi đè các hàm đó bên trong `MyRLEnv` của mình trong tệp mô hình dự đoán. Hoặc để có những tùy chỉnh nâng cao hơn, bạn nên tạo một môi trường hoàn toàn mới kế thừa từ `BaseEnvironment`.

!!! Lưu ý
    Chỉ `Base3ActionRLEnv` mới có thể thực hiện đào tạo/giao dịch dài hạn (đặt thuộc tính chiến lược người dùng `can_short = False`).