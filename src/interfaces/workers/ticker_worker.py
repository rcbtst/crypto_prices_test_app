from celery import Celery, signals

from src.config import settings
from src.infrastructure.di_config import ApplicationContainer
from src.infrastructure.logging import configure_logging

app = Celery("ticker_worker")

app.config_from_object("src.interfaces.workers.configs.ticker_worker")
app.conf.update(**settings.CELERY_TICKER_WORKER_EXTRA_CONFIG)

app.autodiscover_tasks(packages=["src.interfaces.workers.tasks"], related_name=None)

app.conf.beat_schedule = {
    "update_tickers_data_periodic": {
        "task": "update_tickers_data",
        "schedule": settings.APP_TICKER_UPDATE_TASK_SCHEDULE_INTERVAL,
        "args": (settings.APP_TICKERS_TO_UPDATE,),
    },
}


@signals.worker_process_init.connect
def init_worker(**kwargs: dict) -> None:
    container = ApplicationContainer()
    container.wire(
        packages=["src.interfaces.workers.tasks"],
    )


@signals.setup_logging.connect
def setup_logging(**kwargs: dict) -> None:
    log_level = kwargs.get("log_level", settings.LOG_LEVEL)
    configure_logging(log_level=log_level)
