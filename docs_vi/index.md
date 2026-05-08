<!-- Auto-translated from docs/ by script. Please review technical terms. -->

![freqtrade](assets/freqtrade_Poweredby.svg)[![Freqtrade CI](https://github.com/freqtrade/freqtrade/actions/workflows/ci.yml/badge.svg?branch=develop)](https://github.com/freqtrade/freqtrade/actions/workflows/ci.yml)
[![DOI](https://joss.theoj.org/papers/10.21105/joss.04864/status.svg)](https://doi.org/10.21105/joss.04864)
[![codecov](https://codecov.io/gh/freqtrade/freqtrade/branch/develop/graph/badge.svg?token=AD5BG3ATKI)](https://codecov.io/gh/freqtrade/freqtrade)
[![Documentation](https://readthedocs.org/projects/freqtrade/badge/)](https://www.freqtrade.io)
[![Discord Server](https://img.shields.io/badge/Freqtrade_Discord-4E4E4E?logo=discord)](https://discord.gg/p7nuUNVfP7)
<!-- Nút hành động GitHub -->[:octicons-star-16: Star](https://github.com/freqtrade/freqtrade){ .md-button .md-button--sm }
[:octicons-repo-forked-16: Fork](https://github.com/freqtrade/freqtrade/fork){ .md-button .md-button--sm }
[:octicons-download-16: Download](https://github.com/freqtrade/freqtrade/archive/stable.zip){ .md-button .md-button--sm }
## Giới thiệu

Freqtrade là bot giao dịch tiền điện tử mã nguồn mở và miễn phí được viết bằng Python. Nó được thiết kế để hỗ trợ tất cả các sàn giao dịch lớn và được kiểm soát thông qua Telegram hoặc webUI. Nó chứa các công cụ kiểm tra ngược, lập kế hoạch và quản lý tiền cũng như tối ưu hóa chiến lược bằng học máy.

!!! Nguy hiểm "TUYÊN BỐ TỪ CHỐI TRÁCH NHIỆM"
    Phần mềm này chỉ dành cho mục đích giáo dục. Đừng mạo hiểm với số tiền mà bạn sợ mất. SỬ DỤNG PHẦN MỀM RỦI RO CỦA RIÊNG BẠN. CÁC TÁC GIẢ VÀ TẤT CẢ CÁC ĐƠN VỊ LIÊN KẾT KHÔNG CHỊU TRÁCH NHIỆM VỀ KẾT QUẢ GIAO DỊCH CỦA BẠN.

    Luôn bắt đầu bằng cách chạy bot giao dịch trong Dry-run và không tham gia kiếm tiền trước khi bạn hiểu cách thức hoạt động của nó cũng như mức lãi/lỗ mà bạn sẽ mong đợi.

    Chúng tôi thực sự khuyên bạn nên có kỹ năng viết mã cơ bản và kiến ​​thức về Python. Đừng ngần ngại đọc mã nguồn và hiểu cơ chế của bot này, các thuật toán và kỹ thuật được triển khai trong đó.

![ảnh chụp màn hình freqtrade](assets/freqtrade-screenshot.png)

## Tính năng- Develop your Strategy: Write your strategy in python, using [pandas](https://pandas.pydata.org/). Example strategies to inspire you are available in the [strategy repository](https://github.com/freqtrade/freqtrade-strategies).
- Tải xuống dữ liệu thị trường: Tải xuống dữ liệu lịch sử của sàn giao dịch và các thị trường mà bạn có thể muốn giao dịch.
- Backtest: Kiểm tra chiến lược của bạn trên dữ liệu lịch sử đã tải xuống.
- Tối ưu hóa: Tìm các thông số tốt nhất cho chiến lược của bạn bằng cách sử dụng tính năng siêu tối ưu hóa sử dụng phương pháp học máy. Bạn có thể tối ưu hóa các thông số mua, bán, chốt lãi (ROI), dừng lỗ và dừng lỗ cho chiến lược của mình.
- Chọn thị trường: Tạo danh sách tĩnh của bạn hoặc sử dụng danh sách tự động dựa trên khối lượng và/hoặc giá giao dịch hàng đầu (không có sẵn trong quá trình kiểm tra lại). Bạn cũng có thể đưa vào danh sách đen một cách rõ ràng các thị trường mà bạn không muốn giao dịch.
- Chạy: Kiểm tra chiến lược của bạn bằng tiền mô phỏng (chế độ Dry-Run) hoặc triển khai nó bằng tiền thật (chế độ Giao dịch trực tiếp).
- Kiểm soát/Giám sát: Sử dụng Telegram hoặc WebUI (bắt đầu/dừng bot, hiển thị lãi/lỗ, tóm tắt hàng ngày, kết quả giao dịch mở hiện tại, v.v.).
- Phân tích: Có thể thực hiện phân tích sâu hơn trên dữ liệu Backtesting hoặc lịch sử giao dịch Freqtrade (cơ sở dữ liệu SQL), bao gồm các biểu đồ tiêu chuẩn tự động và các phương pháp tải dữ liệu vào [môi trường tương tác](data-analysis.md).

## Thị trường trao đổi được hỗ trợ

Vui lòng đọc [ghi chú cụ thể về trao đổi](exchanges.md) để tìm hiểu về các cấu hình đặc biệt, cuối cùng cần thiết cho mỗi lần trao đổi.

### Sàn giao dịch giao ngay được hỗ trợ- [X] [Binance](https://www.binance.com/)
- [X] [BingX](https://bingx.com/invite/0EM9RX)
- [X] [Bitget](https://www.bitget.com/)
- [X] [Bitmart](https://bitmart.com/)
- [X] [Bybit](https://bybit.com/)
- [X] [Gate.io](https://www.gate.io/ref/6266643)
- [X] [HTX](https://www.htx.com/)
- [X] [Hyperliquid](https://hyperliquid.xyz/) (A decentralized exchange, or DEX)
- [X] [Kraken](https://kraken.com/)
- [X] [OKX](https://okx.com/)
- [X] [MyOKX](https://okx.com/) (OKX EEA)
- [ ] [potentially many others through <img alt="ccxt" width="30px" src="assets/ccxt-logo.svg" />](https://github.com/ccxt/ccxt/). _(We cannot guarantee they will work)_
### Sàn giao dịch tương lai được hỗ trợ- [X] [Binance](https://www.binance.com/)
- [X] [Bitget](https://www.bitget.com/)
- [X] [Bybit](https://bybit.com/)
- [X] [Gate.io](https://www.gate.io/ref/6266643)
- [X] [Hyperliquid](https://hyperliquid.xyz/) (A decentralized exchange, or DEX)
- [X] [OKX](https://okx.com/)
- [X] [Kraken](https://www.kraken.com/features/futures)
Vui lòng đảm bảo đọc [ghi chú cụ thể về sàn giao dịch](exchanges.md), cũng như tài liệu [giao dịch với đòn bẩy](leverage.md) trước khi bắt đầu.

### Cộng đồng đã thử nghiệm

Các sàn giao dịch được cộng đồng xác nhận hoạt động:- [X] [Bitvavo](https://bitvavo.com/)
- [X] [Kucoin](https://www.kucoin.com/)
##Giới thiệu cộng đồng

--8<-- "bao gồm/showcase.md"

## Yêu cầu

### Yêu cầu về phần cứng

Để chạy bot này, chúng tôi khuyên bạn nên sử dụng phiên bản đám mây linux với tối thiểu:

-RAM 2GB
- Dung lượng ổ đĩa 1GB
- 2vCPU

### Yêu cầu phần mềm

- Docker (Được khuyến nghị)

Ngoài ra

- Python 3.11+
- pip (pip3)
- git
- TA-Lib
- virtualenv (Được khuyến nghị)

## Hỗ trợ

### Trợ giúp / Bất hòaFor any questions not covered by the documentation or for further information about the bot, or to simply engage with like-minded individuals, we encourage you to join the Freqtrade [discord server](https://discord.gg/p7nuUNVfP7).
## Sẵn sàng để thử?

Bắt đầu bằng cách đọc hướng dẫn cài đặt [dành cho docker](docker_quickstart.md) (được khuyến nghị) hoặc dành cho [cài đặt không có docker](installation.md).