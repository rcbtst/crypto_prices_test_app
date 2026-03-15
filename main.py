from src.infrastructure.logging import configure_logging
from src.interfaces.rest_api import setup_app

configure_logging()
app = setup_app()
