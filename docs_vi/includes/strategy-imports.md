<!-- Auto-translated from docs/ by script. Please review technical terms. -->

## Nhập khẩu cần thiết cho chiến lược

Khi tạo chiến lược, bạn sẽ cần nhập các mô-đun và lớp cần thiết. Việc nhập khẩu sau đây là cần thiết cho một chiến lược:

Theo mặc định, chúng tôi khuyên bạn nên nhập các nội dung sau làm đường cơ sở cho chiến lược của mình:
Điều này sẽ bao gồm tất cả các hoạt động nhập cần thiết để chức năng freqtrade hoạt động.
Rõ ràng là bạn có thể thêm nhiều lượt nhập khẩu nếu cần cho chiến lược của mình.``` python
# flake8: noqa: F401
# isort: skip_file
# --- Do not remove these imports ---
import numpy as np
import pandas as pd
from datetime import datetime, timedelta, timezone
from pandas import DataFrame
from typing import Dict, Optional, Union, Tuple

from freqtrade.strategy import (
    IStrategy,
    Trade, 
    Order,
    PairLocks,
    informative,  # @informative decorator
    # Hyperopt Parameters
    BooleanParameter,
    CategoricalParameter,
    DecimalParameter,
    IntParameter,
    RealParameter,
    # timeframe helpers
    timeframe_to_minutes,
    timeframe_to_next_date,
    timeframe_to_prev_date,
    # Strategy helper functions
    merge_informative_pair,
    stoploss_from_absolute,
    stoploss_from_open,
)

# --------------------------------
# Add your lib to import here
import talib.abstract as ta
from technical import qtpylib
```