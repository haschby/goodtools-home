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
        
    def _format(self, msg):
        if isinstance(msg, (dict, list)):
            return json.dumps(msg, indent=2, default=str)
        return str(msg)

    def error(self, msg): self._log.error(f"⚠️ {self._format(msg)}")
    def warning(self, msg): self._log.warning(f"🔥 {self._format(msg)}")
    def info(self, msg): self._log.info(f"🚀 {self._format(msg)}")
    def debug(self, msg): self._log.debug(f"🚀 {self._format(msg)}")
