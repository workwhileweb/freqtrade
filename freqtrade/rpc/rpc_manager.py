"""
This module contains class to manage RPC communications (Telegram, API, ...)
"""

import logging
from collections import deque

from freqtrade.constants import Config
from freqtrade.enums import NO_ECHO_MESSAGES, RPCMessageType
from freqtrade.i18n import get_default_language, translate
from freqtrade.rpc import RPC, RPCHandler
from freqtrade.rpc.rpc_types import RPCSendMsg


logger = logging.getLogger(__name__)


class RPCManager:
    """
    Class to manage RPC objects (Telegram, API, ...)
    """

    def __init__(self, freqtrade) -> None:
        """Initializes all enabled rpc modules"""
        self.registered_modules: list[RPCHandler] = []
        self._rpc = RPC(freqtrade)
        config = freqtrade.config
        # Enable telegram
        if config.get("telegram", {}).get("enabled", False):
            logger.info("Enabling rpc.telegram ...")
            from freqtrade.rpc.telegram import Telegram

            self.registered_modules.append(Telegram(self._rpc, config))

        # Enable discord
        if config.get("discord", {}).get("enabled", False):
            logger.info("Enabling rpc.discord ...")
            from freqtrade.rpc.discord import Discord

            self.registered_modules.append(Discord(self._rpc, config))

        # Enable Webhook
        if config.get("webhook", {}).get("enabled", False):
            logger.info("Enabling rpc.webhook ...")
            from freqtrade.rpc.webhook import Webhook

            self.registered_modules.append(Webhook(self._rpc, config))

        # Enable local rest api server for cmd line control
        if config.get("api_server", {}).get("enabled", False):
            logger.info("Enabling rpc.api_server")
            from freqtrade.rpc.api_server import ApiServer

            apiserver = ApiServer(config)
            apiserver.add_rpc_handler(self._rpc)
            self.registered_modules.append(apiserver)

    def cleanup(self) -> None:
        """Stops all enabled rpc modules"""
        logger.info("Cleaning up rpc modules ...")
        while self.registered_modules:
            mod = self.registered_modules.pop()
            logger.info(f"Cleaning up rpc.{mod.name} ...")
            mod.cleanup()
            del mod

    def send_msg(self, msg: RPCSendMsg) -> None:
        """
        Send given message to all registered rpc modules.
        A message consists of one or more key value pairs of strings.
        e.g.:
        {
            'status': 'stopping bot'
        }
        """
        if msg.get("type") not in NO_ECHO_MESSAGES:
            logger.info(f"Sending rpc message: {msg}")
        for mod in self.registered_modules:
            logger.debug("Forwarding message to rpc.%s", mod.name)
            try:
                mod.send_msg(msg)
            except NotImplementedError:
                logger.error(f"Message type '{msg['type']}' not implemented by handler {mod.name}.")
            except Exception:
                logger.exception(f"Exception occurred within RPC module {mod.name}")

    def process_msg_queue(self, queue: deque) -> None:
        """
        Process all messages in the queue.
        """
        while queue:
            msg = queue.popleft()
            logger.info(f"Sending rpc strategy_msg: {msg}")
            for mod in self.registered_modules:
                if mod._config.get(mod.name, {}).get("allow_custom_messages", False):
                    mod.send_msg(
                        {
                            "type": RPCMessageType.STRATEGY_MSG,
                            "msg": msg,
                        }
                    )

    def startup_messages(self, config: Config, pairlist, protections) -> None:
        lang = get_default_language(config)
        if config["dry_run"]:
            self.send_msg(
                {
                    "type": RPCMessageType.WARNING,
                    "status": translate("rpc.startup.dry_run_warning", lang),
                }
            )
        stake_currency = config["stake_currency"]
        stake_amount = config["stake_amount"]
        minimal_roi = config["minimal_roi"]
        stoploss = config["stoploss"]
        trailing_stop = config["trailing_stop"]
        timeframe = config["timeframe"]
        exchange_name = config["exchange"]["name"]
        if config["exchange"].get("demo_trading"):
            exchange_name += " (demo trading)"
        strategy_name = config.get("strategy", "")
        pos_adjust_enabled = translate(
            "rpc.startup.on" if config["position_adjustment_enable"] else "rpc.startup.off", lang
        )
        self.send_msg(
            {
                "type": RPCMessageType.STARTUP,
                "status": translate(
                    "rpc.startup.summary",
                    lang,
                    exchange_name=exchange_name,
                    stake_amount=stake_amount,
                    stake_currency=stake_currency,
                    minimal_roi=minimal_roi,
                    stoploss_label=translate(
                        "rpc.startup.trailing_stoploss" if trailing_stop else "rpc.startup.stoploss",
                        lang,
                    ),
                    stoploss=stoploss,
                    pos_adjust_enabled=pos_adjust_enabled,
                    timeframe=timeframe,
                    strategy_name=strategy_name,
                ),
            }
        )
        self.send_msg(
            {
                "type": RPCMessageType.STARTUP,
                "status": translate(
                    "rpc.startup.search_pairs",
                    lang,
                    stake_currency=stake_currency,
                    pairlist=pairlist.short_desc(),
                ),
            }
        )
        if len(protections.name_list) > 0:
            prots = "\n".join([p for prot in protections.short_desc() for k, p in prot.items()])
            # Best-effort normalization to keep protection summaries localized consistently.
            if lang == "vi":
                replacements = {
                    " for ": " trong ",
                    " candles": " nến",
                    " candle": " nến",
                    " minutes": " phút",
                    " minute": " phút",
                    "drawdown": "sụt giảm",
                }
                for src, dst in replacements.items():
                    prots = prots.replace(src, dst)
            self.send_msg(
                {
                    "type": RPCMessageType.STARTUP,
                    "status": translate("rpc.startup.protections", lang, protections=prots),
                }
            )
