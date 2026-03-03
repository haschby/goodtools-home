import logging
from application.ports.logger.loggerPort import LoggerPort
import json

class LoggerImplement(LoggerPort):
    def __init__(self, systemLogger: str):
        self._log = logging.getLogger(systemLogger)
        self._log.setLevel(logging.DEBUG)
        
        if not self._log.handlers:
            handler = logging.StreamHandler()
            handler.setFormatter(
                logging.Formatter(
                    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
                )
            )
            self._log.addHandler(handler)
        
    def error(self, msg: dict): self._log.error(f"⚠️ {json.dumps(msg, indent=2, default=str)}")
    def warning(self, msg: dict): self._log.warning(f"🔥 {json.dumps(msg, indent=2, default=str)}")
    def info(self, msg: dict): self._log.info(f"ℹ️ {json.dumps(msg, indent=2, default=str)}")
    def debug(self, msg: dict): self._log.debug(f"🚀 {json.dumps(msg, indent=2, default=str)}")
