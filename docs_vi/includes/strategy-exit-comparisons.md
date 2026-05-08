<!-- Auto-translated from docs/ by script. Please review technical terms. -->

## Thoát so sánh logic

Freqtrade cho phép chiến lược của bạn triển khai logic thoát khác nhau bằng cách sử dụng các chức năng dựa trên tín hiệu hoặc dựa trên lệnh gọi lại.
Phần này nhằm mục đích so sánh từng chức năng khác nhau, giúp bạn chọn chức năng phù hợp nhất với nhu cầu của mình.

* **`populate_exit_trend()`** - Logic thoát dựa trên tín hiệu được vector hóa bằng cách sử dụng các chỉ báo trong khung dữ liệu chính
  ✅ **Sử dụng** để xác định tín hiệu thoát dựa trên các chỉ báo hoặc dữ liệu khác có thể được tính toán theo cách vectơ hóa.
  🚫 **Không sử dụng** để tùy chỉnh các điều kiện thoát cho từng giao dịch riêng lẻ hoặc nếu dữ liệu giao dịch là cần thiết để đưa ra quyết định thoát.
* **`custom_exit()`** - Logic thoát tùy chỉnh sẽ thoát hoàn toàn giao dịch ngay lập tức, được yêu cầu cho mọi giao dịch đang mở ở mỗi lần lặp lại vòng lặp bot cho đến khi giao dịch được đóng.
  ✅ **Sử dụng** để chỉ định các điều kiện thoát cho từng giao dịch riêng lẻ (bao gồm mọi lệnh điều chỉnh bổ sung sử dụng ` adjustment_trade_position()`) hoặc nếu dữ liệu giao dịch là cần thiết để đưa ra quyết định thoát, ví dụ: sử dụng dữ liệu lợi nhuận để thoát.
  🚫 **Không sử dụng** khi bạn muốn thoát bằng cách sử dụng dữ liệu dựa trên chỉ báo được vectơ hóa (thay vào đó hãy sử dụng tín hiệu `populate_exit_trend()` hoặc làm proxy cho `custom_stoploss()` và lưu ý rằng các lần thoát dựa trên tỷ lệ trong quá trình kiểm tra ngược có thể không chính xác.
* **`custom_stoploss()`** - Điểm dừng lỗ theo sau tùy chỉnh, được yêu cầu cho mọi giao dịch đang mở trong mỗi lần lặp lại cho đến khi giao dịch được đóng. Giá trị được trả về ở đây cũng được sử dụng cho [điểm dừng khi trao đổi](stoploss.md#stop-loss-on-exchangefreqtrade).  
  ✅ **Sử dụng** để tùy chỉnh logic dừng lỗ nhằm đặt mức dừng lỗ động dựa trên dữ liệu giao dịch hoặc các điều kiện khác.
  🚫 **Không sử dụng** để thoát giao dịch ngay lập tức dựa trên một điều kiện cụ thể. Sử dụng `custom_exit()` cho mục đích đó.
* **`custom_roi()`** - ROI tùy chỉnh, được gọi cho mọi giao dịch đang mở trong mỗi lần lặp cho đến khi giao dịch được đóng.
  ✅ **Sử dụng** để chỉ định ngưỡng ROI tối thiểu ("chốt lời") để thoát giao dịch ở mức ROI này tại một thời điểm nào đó trong thời gian giao dịch, dựa trên lợi nhuận hoặc các điều kiện khác.
  🚫 **Không sử dụng** để thoát giao dịch ngay lập tức dựa trên một điều kiện cụ thể. Sử dụng `custom_exit()`.
  🚫 **Không sử dụng** cho ROI tĩnh. Sử dụng `minimal_roi`.