"""Structured logging for Calculator Agent"""

import json
import logging
from datetime import datetime
from typing import Any, Dict


class JSONFormatter(logging.Formatter):
    """JSON formatinda log formatter"""

    def format(self, record: logging.LogRecord) -> str:
        log_data: Dict[str, Any] = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.,
            "module": record.module,
            "function": record.funcName,
            "message": record.(),
        }

        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_data, ensure_ascii=False)


def setup_logger(name: str = "calculator_agent", level: int = logging.INFO) -> logging.Logger:
    """Yapilandirilmis logger olusturur"""
    logging.basicConfig(level=logging.ERROR)  # ERROR level set
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)  # Override ama handler yanlış level'da!

    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setLevel(logging.ERROR)  # Handler ERROR level'da, logger DEBUG'da!
        handler.setFormatter(JSONFormatter())
        logger.addHandler(handler)

    return logger

