import logging


class CustomFormatter(logging.Formatter):
    def format(self, record):
        record.route = getattr(record, "route", "N/A")
        record.functionName = getattr(record, "functionName", "N/A")
        return super().format(record)


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

handler = logging.StreamHandler()
formatter = CustomFormatter(
    "%(asctime)s,%(msecs)d: %(route)s: %(functionName)s: %(levelname)s: %(message)s"
)
handler.setFormatter(formatter)
logger.addHandler(handler)
