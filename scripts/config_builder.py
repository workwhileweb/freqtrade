"""
Freqtrade Quick Config Builder (Gradio form).

- Liet ke 10 template config trong user_data/config_templates/
- Cho user chon template + exchange + stake_currency + dry_run + telegram + ...
- Sinh JSON config, preview va luu vao user_data/config.json (co backup .bak)
- Tuy chon: restart docker container ngay sau khi save

Run:
    python scripts/config_builder.py            # mac dinh mo http://127.0.0.1:7860
    python scripts/config_builder.py --port 7860 --share

CLI fallback (khong can Gradio):
    python scripts/config_builder.py --cli --template safe_spot --exchange binance \
        --stake USDT --wallet 100 --dry-run --save
"""
from __future__ import annotations

import argparse
import copy
import json
import os
import shutil
import subprocess
import sys
import datetime as _dt
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = REPO_ROOT / "user_data" / "config_templates"
CONFIG_PATH = REPO_ROOT / "user_data" / "config.json"
COMPOSE_FILE = REPO_ROOT / "docker-compose.local.yml"

EXCHANGES = ["binance", "kucoin", "okx", "bybit", "gate", "kraken", "htx", "mexc"]
STAKE_CURRENCIES = ["USDT", "USDC", "BTC", "ETH", "BUSD"]


# ---------------------------------------------------------------------------
# Defaults shared across templates
# ---------------------------------------------------------------------------
DEFAULT_ENTRY_PRICING = {
    "price_side": "same",
    "use_order_book": True,
    "order_book_top": 1,
    "price_last_balance": 0.0,
    "check_depth_of_market": {"enabled": False, "bids_to_ask_delta": 1},
}
DEFAULT_EXIT_PRICING = {
    "price_side": "same",
    "use_order_book": True,
    "order_book_top": 1,
}
DEFAULT_ORDER_TYPES = {
    "entry": "limit",
    "exit": "limit",
    "emergency_exit": "market",
    "force_entry": "market",
    "force_exit": "market",
    "stoploss": "market",
    "stoploss_on_exchange": False,
    "stoploss_on_exchange_interval": 60,
}
DEFAULT_ORDER_TIME_IN_FORCE = {"entry": "GTC", "exit": "GTC"}
DEFAULT_UNFILLEDTIMEOUT = {"entry": 10, "exit": 10, "exit_timeout_count": 0, "unit": "minutes"}
DEFAULT_TG_NOTIFICATIONS = {
    "status": "on",
    "warning": "on",
    "startup": "on",
    "entry": "on",
    "entry_fill": "on",
    "exit": {
        "roi": "on",
        "emergency_exit": "on",
        "force_exit": "on",
        "exit_signal": "on",
        "trailing_stop_loss": "on",
        "stop_loss": "on",
        "stoploss_on_exchange": "on",
        "custom_exit": "on",
    },
    "exit_cancel": "on",
    "entry_cancel": "on",
    "protection_trigger": "on",
    "protection_trigger_global": "on",
    "show_candle": "off",
    "strategy_msg": "on",
}
DEFAULT_API_SERVER = {
    "enabled": True,
    "listen_ip_address": "0.0.0.0",
    "listen_port": 8080,
    "verbosity": "error",
    "enable_openapi": True,
    "jwt_secret_key": "CHANGE_ME_RANDOM_HEX",
    "CORS_origins": [],
    "username": "freqtrader",
    "password": "freqtrade123",
    "ws_token": "CHANGE_ME_RANDOM",
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def list_templates() -> list[dict[str, Any]]:
    if not TEMPLATES_DIR.exists():
        return []
    items = []
    for p in sorted(TEMPLATES_DIR.glob("*.json")):
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
            data["_file"] = p.name
            items.append(data)
        except Exception as exc:
            print(f"[WARN] Cannot parse {p.name}: {exc}", file=sys.stderr)
    return items


def load_current_config() -> dict[str, Any]:
    if CONFIG_PATH.exists():
        try:
            return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
        except Exception:
            return {}
    return {}


def template_label(t: dict[str, Any]) -> str:
    m = t["meta"]
    risk = m.get("risk_level", "?")
    return f"[{risk:>9}] {m['name_vi']}  —  {m['description_vi']}"


def get_template(template_id: str) -> dict[str, Any]:
    for t in list_templates():
        if t["meta"]["id"] == template_id:
            return t
    raise ValueError(f"Template not found: {template_id}")


def build_config(
    template_id: str,
    exchange: str,
    stake_currency: str,
    dry_run: bool,
    dry_run_wallet: float,
    max_open_trades_override: str | int | None,
    telegram_enabled: bool,
    telegram_token: str,
    telegram_chat_id: str,
    pair_whitelist_override: str,
    keep_api_server: bool,
) -> dict[str, Any]:
    t = get_template(template_id)
    overlay = t["config_overlay"]
    meta = t["meta"]
    is_futures = overlay.get("trading_mode") == "futures"

    if pair_whitelist_override.strip():
        pairs = [p.strip() for p in pair_whitelist_override.replace("\n", ",").split(",") if p.strip()]
    else:
        pairs_map = (t.get("futures_pairs_by_stake") if is_futures else t.get("pairs_by_stake")) or {}
        pairs = list(pairs_map.get(stake_currency) or pairs_map.get("USDT") or [])

    current = load_current_config()
    api_server = copy.deepcopy(current.get("api_server")) if keep_api_server and current.get("api_server") else copy.deepcopy(DEFAULT_API_SERVER)

    if max_open_trades_override in ("", None):
        max_trades = int(overlay.get("max_open_trades", 3))
    else:
        max_trades = int(max_open_trades_override)

    config: dict[str, Any] = {
        "$schema": "https://schema.freqtrade.io/schema.json",
        "_template": meta["id"],
        "_template_name": meta["name_vi"],
        "_template_description": meta["description_vi"],
        "_template_risk_level": meta.get("risk_level", "unknown"),
        "_template_recommended_leverage": meta.get("recommended_leverage"),

        "max_open_trades": max_trades,
        "stake_currency": stake_currency,
        "stake_amount": overlay.get("stake_amount", "unlimited"),
        "tradable_balance_ratio": overlay.get("tradable_balance_ratio", 0.99),
        "fiat_display_currency": "USD",
        "timeframe": overlay.get("timeframe", "5m"),

        "dry_run": bool(dry_run),
        "dry_run_wallet": float(dry_run_wallet),
        "cancel_open_orders_on_exit": False,

        "trading_mode": overlay.get("trading_mode", "spot"),
        "margin_mode": overlay.get("margin_mode", ""),

        "position_adjustment_enable": overlay.get("position_adjustment_enable", False),
        "max_entry_position_adjustment": overlay.get("max_entry_position_adjustment", -1),

        "minimal_roi": overlay.get("minimal_roi", {"60": 0.01, "30": 0.02, "0": 0.04}),
        "stoploss": overlay.get("stoploss", -0.10),
        "process_only_new_candles": overlay.get("process_only_new_candles", True),

        "unfilledtimeout": dict(DEFAULT_UNFILLEDTIMEOUT),
        "entry_pricing": copy.deepcopy(DEFAULT_ENTRY_PRICING),
        "exit_pricing": copy.deepcopy(DEFAULT_EXIT_PRICING),
        "order_types": copy.deepcopy(DEFAULT_ORDER_TYPES),
        "order_time_in_force": dict(DEFAULT_ORDER_TIME_IN_FORCE),

        "exchange": {
            "name": exchange,
            "key": "",
            "secret": "",
            "ccxt_config": {},
            "ccxt_async_config": {},
            "pair_whitelist": pairs,
            "pair_blacklist": list(overlay.get("pair_blacklist", [])),
        },
        "pairlists": copy.deepcopy(overlay.get("pairlists", [{"method": "StaticPairList"}])),

        "telegram": {
            "enabled": bool(telegram_enabled),
            "token": telegram_token.strip() if telegram_token.strip() else "REPLACE_WITH_YOUR_TELEGRAM_BOT_TOKEN",
            "chat_id": telegram_chat_id.strip() if telegram_chat_id.strip() else "REPLACE_WITH_YOUR_CHAT_ID",
            "notification_settings": copy.deepcopy(DEFAULT_TG_NOTIFICATIONS),
            "reload": True,
            "balance_dust_level": 0.01,
        },

        "api_server": api_server,

        "strategy": meta.get("default_strategy", "SampleStrategy"),
        "bot_name": "freqtrade",
        "initial_state": "running",
        "force_entry_enable": False,
        "internals": {"process_throttle_secs": 5},
    }

    if is_futures and overlay.get("liquidation_buffer") is not None:
        config["liquidation_buffer"] = overlay["liquidation_buffer"]

    return config


def backup_existing_config() -> Path | None:
    if not CONFIG_PATH.exists():
        return None
    ts = _dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    bak = CONFIG_PATH.with_suffix(f".json.bak.{ts}")
    shutil.copy2(CONFIG_PATH, bak)
    return bak


def save_config(config: dict[str, Any], dest: Path | None = None) -> Path:
    target = dest or CONFIG_PATH
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(config, indent=4, ensure_ascii=False) + "\n", encoding="utf-8")
    return target


def restart_docker(timeout: int = 60) -> tuple[bool, str]:
    if not COMPOSE_FILE.exists():
        return False, f"Khong tim thay {COMPOSE_FILE}. Bo qua restart."
    try:
        out = subprocess.run(
            ["docker", "compose", "-f", str(COMPOSE_FILE), "restart", "freqtrade"],
            capture_output=True, text=True, timeout=timeout, cwd=str(REPO_ROOT),
        )
        ok = out.returncode == 0
        msg = (out.stdout or "") + (out.stderr or "")
        return ok, msg.strip() or ("OK" if ok else "Failed")
    except FileNotFoundError:
        return False, "Khong tim thay 'docker'. Cai Docker Desktop hoac dong PATH."
    except Exception as exc:
        return False, f"Restart loi: {exc}"


# ---------------------------------------------------------------------------
# Gradio UI
# ---------------------------------------------------------------------------
def launch_gradio(host: str = "127.0.0.1", port: int = 7860, share: bool = False) -> None:
    try:
        import gradio as gr
    except ImportError:
        print("[FATAL] Gradio chua duoc cai. Chay:  pip install gradio", file=sys.stderr)
        sys.exit(1)

    templates = list_templates()
    if not templates:
        print(f"[FATAL] Khong co template nao trong {TEMPLATES_DIR}", file=sys.stderr)
        sys.exit(1)

    template_choices = [(template_label(t), t["meta"]["id"]) for t in templates]
    default_template_id = templates[0]["meta"]["id"]

    def on_template_change(template_id: str, stake_currency: str):
        try:
            t = get_template(template_id)
        except ValueError:
            return "", "", "", "", ""
        meta = t["meta"]
        overlay = t["config_overlay"]
        is_futures = overlay.get("trading_mode") == "futures"
        pairs_map = (t.get("futures_pairs_by_stake") if is_futures else t.get("pairs_by_stake")) or {}
        pairs = list(pairs_map.get(stake_currency) or pairs_map.get("USDT") or [])

        info = (
            f"### {meta['name_vi']}\n"
            f"- **Risk level:** `{meta.get('risk_level','?')}`\n"
            f"- **Strategy:** `{meta.get('default_strategy','SampleStrategy')}`\n"
            f"- **Trading mode:** `{overlay.get('trading_mode')}` "
            f"({overlay.get('margin_mode') or 'n/a'}, leverage `{meta.get('recommended_leverage') or '1x'}`)\n"
            f"- **Timeframe:** `{overlay.get('timeframe','5m')}`\n"
            f"- **Max trades:** `{overlay.get('max_open_trades')}`\n"
            f"- **Stoploss:** `{overlay.get('stoploss')}`  •  **ROI:** `{overlay.get('minimal_roi')}`\n"
            f"- **Pairlists:** `{[p['method'] for p in overlay.get('pairlists', [])]}`\n"
            f"- **Recommended wallet:** `{meta.get('recommended_wallet')}`\n"
            f"- **Tags:** `{', '.join(meta.get('tags', []))}`\n"
        )
        notes = t.get("_notes_vi") or ""
        if notes:
            info += f"\n> {notes}\n"

        pair_text = "\n".join(pairs) if pairs else "(template dung pairlist dynamic — pair_whitelist se duoc bo trong khi build)"
        return (
            info,
            pair_text,
            int(overlay.get("max_open_trades", 3)),
            int(meta.get("recommended_wallet", 100)),
            "",
        )

    def on_generate(template_id, exchange, stake, dry_run, wallet, max_trades,
                    tg_enabled, tg_token, tg_chat, pair_override, keep_api):
        try:
            cfg = build_config(
                template_id=template_id,
                exchange=exchange,
                stake_currency=stake,
                dry_run=dry_run,
                dry_run_wallet=wallet,
                max_open_trades_override=max_trades,
                telegram_enabled=tg_enabled,
                telegram_token=tg_token or "",
                telegram_chat_id=tg_chat or "",
                pair_whitelist_override=pair_override or "",
                keep_api_server=keep_api,
            )
            text = json.dumps(cfg, indent=4, ensure_ascii=False)
            return text, gr.update(value="Da generate. Xem lai roi bam Save."), cfg
        except Exception as exc:
            return "", gr.update(value=f"LOI: {exc}"), None

    def on_save(state_cfg, also_restart):
        if not state_cfg:
            return "Chua generate config. Bam **Generate** truoc."
        bak = backup_existing_config()
        path = save_config(state_cfg)
        msg = [f"Saved -> {path}"]
        if bak:
            msg.append(f"Backup -> {bak.name}")
        if also_restart:
            ok, out = restart_docker()
            msg.append(("Restart OK\n" if ok else "Restart FAILED\n") + out)
        return "\n".join(msg)

    with gr.Blocks(title="Freqtrade Quick Config Builder") as demo:
        cfg_state = gr.State(value=None)

        gr.Markdown(
            "# Freqtrade Quick Config Builder\n"
            "Chon template + tham so → Generate → Save (+ tuy chon restart docker container)."
        )

        with gr.Row():
            with gr.Column(scale=1):
                gr.Markdown("## 1. Template")
                template = gr.Dropdown(choices=template_choices, value=default_template_id, label="Trade scenario template")
                template_info = gr.Markdown()

                gr.Markdown("## 2. Sa giao dich & Stake")
                exchange = gr.Dropdown(choices=EXCHANGES, value="binance", label="Exchange")
                stake = gr.Dropdown(choices=STAKE_CURRENCIES, value="USDT", label="Stake currency")
                dry_run = gr.Checkbox(value=True, label="Dry-run (gia lap, an toan)")
                wallet = gr.Number(value=100, label="dry_run_wallet (USDT)", precision=2)
                max_trades = gr.Number(value=3, label="Override max_open_trades (de trong = giu nguyen template)", precision=0)

                gr.Markdown("## 3. Pair whitelist (override)")
                pair_override = gr.Textbox(
                    label="Override pair_whitelist (cach nhau bang dau phay/xuong dong, de trong = mac dinh template)",
                    lines=4, placeholder="BTC/USDT, ETH/USDT, ...",
                )

                gr.Markdown("## 4. Telegram & API server")
                tg_enabled = gr.Checkbox(value=False, label="Bat Telegram")
                tg_token = gr.Textbox(label="Telegram bot TOKEN", value="")
                tg_chat = gr.Textbox(label="Telegram CHAT_ID", value="")
                keep_api = gr.Checkbox(value=True, label="Giu nguyen api_server (username/password/jwt) tu config hien tai")

                generate_btn = gr.Button("Generate config", variant="primary")
                gr.Markdown("## 5. Hanh dong sau khi generate")
                also_restart = gr.Checkbox(value=True, label="Restart docker container sau khi save")
                save_btn = gr.Button("Save -> user_data/config.json", variant="primary")

            with gr.Column(scale=2):
                gr.Markdown("## Template default pairs")
                pair_default = gr.Code(language=None, label="Default pair_whitelist", interactive=False, lines=8)

                gr.Markdown("## Generated config preview")
                preview = gr.Code(language="json", label="config.json preview", lines=28)
                status = gr.Markdown()
                save_status = gr.Code(language=None, label="Save status", lines=6)

        template.change(
            on_template_change, inputs=[template, stake],
            outputs=[template_info, pair_default, max_trades, wallet, preview],
        )
        stake.change(
            on_template_change, inputs=[template, stake],
            outputs=[template_info, pair_default, max_trades, wallet, preview],
        )

        generate_btn.click(
            on_generate,
            inputs=[template, exchange, stake, dry_run, wallet, max_trades, tg_enabled, tg_token, tg_chat, pair_override, keep_api],
            outputs=[preview, status, cfg_state],
        )
        save_btn.click(on_save, inputs=[cfg_state, also_restart], outputs=[save_status])

        # initial render
        demo.load(
            on_template_change, inputs=[template, stake],
            outputs=[template_info, pair_default, max_trades, wallet, preview],
        )

    print(f"\n[OK] Mo trinh duyet: http://{host}:{port}")
    demo.launch(
        server_name=host,
        server_port=port,
        share=share,
        inbrowser=True,
        show_error=True,
    )


# ---------------------------------------------------------------------------
# CLI fallback
# ---------------------------------------------------------------------------
def cli_mode(args: argparse.Namespace) -> int:
    if args.list:
        for t in list_templates():
            m = t["meta"]
            print(f"  - {m['id']:<24} [{m.get('risk_level','?'):>9}] {m['name_vi']} - {m['description_vi']}")
        return 0

    if not args.template:
        print("Error: --template required (or use --list)", file=sys.stderr)
        return 2

    cfg = build_config(
        template_id=args.template,
        exchange=args.exchange,
        stake_currency=args.stake,
        dry_run=args.dry_run or not args.live,
        dry_run_wallet=args.wallet,
        max_open_trades_override=args.max_trades,
        telegram_enabled=args.telegram,
        telegram_token=args.tg_token or "",
        telegram_chat_id=args.tg_chat or "",
        pair_whitelist_override=args.pairs or "",
        keep_api_server=not args.reset_api,
    )

    text = json.dumps(cfg, indent=4, ensure_ascii=False)
    if args.save:
        bak = backup_existing_config()
        path = save_config(cfg)
        print(f"Saved -> {path}")
        if bak:
            print(f"Backup -> {bak}")
        if args.restart:
            ok, out = restart_docker()
            print(("Restart OK" if ok else "Restart FAILED") + ":")
            print(out)
    else:
        print(text)
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="Freqtrade Quick Config Builder")
    ap.add_argument("--cli", action="store_true", help="Chay che do CLI thay vi mo Gradio UI")
    ap.add_argument("--list", action="store_true", help="Liet ke template (CLI mode)")
    ap.add_argument("--template", help="ID template (vd: safe_spot)")
    ap.add_argument("--exchange", default="binance", choices=EXCHANGES)
    ap.add_argument("--stake", default="USDT", choices=STAKE_CURRENCIES)
    ap.add_argument("--wallet", type=float, default=100.0)
    ap.add_argument("--max-trades", type=int, default=None)
    ap.add_argument("--dry-run", action="store_true", default=True)
    ap.add_argument("--live", action="store_true", help="Tat dry-run (CAN THAN!)")
    ap.add_argument("--telegram", action="store_true")
    ap.add_argument("--tg-token", default="")
    ap.add_argument("--tg-chat", default="")
    ap.add_argument("--pairs", default="")
    ap.add_argument("--reset-api", action="store_true", help="Khong giu api_server hien tai (dat lai mac dinh)")
    ap.add_argument("--save", action="store_true", help="Ghi vao user_data/config.json")
    ap.add_argument("--restart", action="store_true", help="Restart docker compose sau khi save")

    ap.add_argument("--port", type=int, default=int(os.environ.get("CONFIG_BUILDER_PORT", "7860")))
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--share", action="store_true")

    args = ap.parse_args()

    if args.cli or args.list:
        return cli_mode(args)

    launch_gradio(host=args.host, port=args.port, share=args.share)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
