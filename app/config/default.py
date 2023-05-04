from logging import DEBUG


class DefaultConfig:
    API_TITLE = "Flask API"
    API_VERSION = 0.1


class LogConfig:
    LOG_FORMAT = (
        f"%(log_color)s%(asctime)s.%(msecs)03d [%(levelname)s] (%(name)s) %(message)s"
    )
    LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
    LOG_LEVEL = DEBUG
