from logging import DEBUG


class DefaultConfig:
    API_TITLE: str = "Flask API"
    API_VERSION: float = 0.1
    PER_PAGE_LIMIT: int = 25


class LogConfig:
    LOG_FORMAT: str = (
        f"%(log_color)s%(asctime)s.%(msecs)03d [%(levelname)s] (%(name)s) %(message)s"
    )
    LOG_DATE_FORMAT: str = "%Y-%m-%d %H:%M:%S"
    LOG_LEVEL: int = DEBUG
