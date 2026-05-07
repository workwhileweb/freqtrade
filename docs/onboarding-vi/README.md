# Tài liệu onboarding (Tiếng Việt)

Bộ tài liệu này được biên soạn cho **thành viên mới** của repo
[freqtrade](https://github.com/freqtrade/freqtrade) — một crypto trading bot
mã nguồn mở viết bằng Python. Tài liệu bằng tiếng Việt, kèm thuật ngữ tiếng
Anh đặt trong ngoặc khi xuất hiện lần đầu để bạn dễ tra cứu chéo với docs gốc
ở [docs/](../).

## Mục lục

| # | File | Đối tượng | Nội dung |
|---|------|-----------|----------|
| 01 | [Nguyên tắc hoạt động](01-nguyen-tac-hoat-dong.md) | Tất cả | Triết lý, kiến trúc tổng thể, vòng đời bot, thuật ngữ |
| 02 | [Code flow chính](02-code-flow-chinh.md) | Coder | 4 luồng code chính (live, backtest, hyperopt, RPC) kèm sơ đồ |
| 03 | [Hướng dẫn build](03-huong-dan-build.md) | Coder / DevOps | Build dev env, wheel, Docker image, docs, FreqUI |
| 04 | [Cài đặt, chạy và sử dụng](04-cai-dat-chay-su-dung.md) | Người dùng cuối | Cài Docker / native, chạy dry-run, Telegram, UI |
| 05 | [Sử dụng nâng cao](05-su-dung-nang-cao.md) | Power user | Callbacks, FreqAI, hyperopt, leverage, plugin chain |
| 06 | [Hướng dẫn phát triển](06-huong-dan-phat-trien.md) | Coder muốn đóng góp | Cấu trúc package, test, debug, plugin/exchange dev |

## Cách đọc nhanh

- Mới hoàn toàn: đọc 01 → 04.
- Muốn viết strategy nâng cao: đọc 01 → 05.
- Muốn đóng góp PR / sửa core: đọc 01 → 02 → 06 (và tham khảo 03 cho build).

## Quy ước trong toàn bộ tài liệu

- Đường dẫn file dùng link tương đối, ví dụ
  [`freqtrade/freqtradebot.py`](../../freqtrade/freqtradebot.py).
- Thuật ngữ Anh đặt trong ngoặc lần đầu, ví dụ "chiến lược (strategy)".
- Lệnh shell mặc định viết cho **PowerShell trên Windows**; phần khác biệt
  với bash/zsh sẽ được nêu rõ.
- Nội dung được đối chiếu trực tiếp với mã nguồn nhánh hiện tại; nếu repo cập
  nhật, chỉnh số dòng/tên hàm cho đồng bộ.

> Tài liệu này **bổ sung** cho docs gốc của freqtrade, không thay thế. Trang
> chính thức (tiếng Anh) đầy đủ nhất nằm tại
> [https://www.freqtrade.io](https://www.freqtrade.io).
